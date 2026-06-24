"""Build a Wikipedia retrieval index for Phase 1.5 (open-corpus evaluation).

What this does
──────────────
1. Stream the wikimedia/wikipedia dump from HuggingFace (no full download).
2. Filter to political/policy articles by title keyword OR take a random
   sample (configurable).
3. Split each article into paragraphs, drop short fragments and references.
4. Cap to --max-passages so the build stays manageable.
5. Reuse the existing HybridRetriever to build BM25 + dense embeddings.
6. Save to outputs/index_wikipedia/ in the same format as the LIAR-aligned
   index — drop-in replacement via run_pipeline.py --index-dir.

Why this exists
───────────────
Phase 1's retrieval corpus is LIARArg's own justification paragraphs — the
fact-checker's own work. That's a closed-corpus setup with known leakage
characteristics. Phase 1.5 swaps that corpus for Wikipedia — a real-world,
fact-checker-blind source — to test whether the argument-aware advantage
generalises beyond the curated dataset.

Typical run (1.5 days total wall-time)
──────────────────────────────────────
    # 1. Build the index (~3 hours on M3 for 150k passages with dense)
    python scripts/build_wikipedia_index.py

    # 2. Run the existing pipeline against the new corpus (~12 hours)
    caffeinate -i python -u scripts/run_pipeline.py \\
        --n 952 --data-dir data_liar \\
        --index-dir outputs/index_wikipedia \\
        --out-dir outputs/results_liar_wikipedia \\
        --verifier ollama --ollama-model qwen2.5:14b-instruct \\
        --device mps --prior-mode probabilistic

    # 3. Score and audit
    python scripts/recompute_metrics.py --results-dir outputs/results_liar_wikipedia
    python scripts/audit_disagreement.py --results-dir outputs/results_liar_wikipedia

Smoke-test before the full build
────────────────────────────────
    python scripts/build_wikipedia_index.py --max-articles 500 --max-passages 5000 \\
        --no-dense --out-dir outputs/index_wikipedia_smoke
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.retriever import HybridRetriever, Passage


# ────────────────────────────────────────────────────────────────────────────
# Topic filter — title-level keyword match
# ────────────────────────────────────────────────────────────────────────────
# Two categories: political-process terms (high-precision political articles)
# and policy-domain terms (where LIAR claims actually land — economy, health,
# immigration, etc.). Title is matched lowercase against any keyword.
POLITICS_KEYWORDS = [
    # Political-process / institutions
    "politics", "political", "election", "elections", "vote", "voting", "voter",
    "congress", "senate", "house of representatives", "presidency", "president",
    "presidential", "government", "administration", "governor", "legislature",
    "legislative", "constitution", "constitutional", "supreme court", "justice",
    "judiciary", "judicial", "executive order", "federal", "state government",
    "democrat", "democratic party", "republican", "republican party",
    "campaign", "ballot", "primary", "caucus", "filibuster", "impeachment",
    "treaty", "foreign policy", "diplomacy",
    # Policy domains common in LIAR claims
    "healthcare", "health care", "medicare", "medicaid", "social security",
    "tax", "taxation", "immigration", "border", "deportation",
    "climate change", "environment", "epa", "pollution",
    "education", "school", "student loan", "tuition",
    "gun control", "firearm", "second amendment",
    "abortion", "reproductive rights",
    "civil rights", "voting rights",
    "economy", "economic", "unemployment", "inflation", "deficit", "debt",
    "minimum wage", "labor", "union",
    "military", "defense", "war", "iraq", "afghanistan", "veteran",
    "trade", "tariff", "nafta", "wto",
    "obamacare", "affordable care act",
]


def matches_topic(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in POLITICS_KEYWORDS)


# ────────────────────────────────────────────────────────────────────────────
# Paragraph extraction
# ────────────────────────────────────────────────────────────────────────────
_PARA_SPLIT = re.compile(r"\n\n+")
# Skip these section headers and everything after — they're noise for retrieval
_NOISE_SECTIONS = re.compile(
    r"\n\s*(References|Bibliography|External links|See also|Further reading|Notes|Citations)\s*\n",
    flags=re.IGNORECASE,
)


def article_to_paragraphs(article_id: str, title: str, text: str,
                          max_paras_per_article: int = 8,
                          min_words: int = 30) -> list[Passage]:
    """Return well-formed paragraph passages from a single Wikipedia article.

    - Drops References / Bibliography / External-links sections (noise).
    - Drops paragraphs shorter than `min_words`.
    - Caps to `max_paras_per_article` (Wikipedia long-tail bias).
    """
    # Trim everything after the first noise-section header
    m = _NOISE_SECTIONS.search(text)
    if m:
        text = text[: m.start()]

    raw_paras = [p.strip() for p in _PARA_SPLIT.split(text) if p.strip()]

    passages: list[Passage] = []
    for j, p in enumerate(raw_paras):
        if len(p.split()) < min_words:
            continue
        # Drop infobox-y paragraphs (lots of pipes / linebreaks)
        if p.count("|") > 8 or p.count("\n") > 4:
            continue
        # Prepend the article title for retrieval boost — paragraphs alone
        # often miss context (e.g. a paragraph about "the bill" without
        # naming which bill). Title is short, doesn't dilute the embedding much.
        text_with_title = f"{title}: {p}"
        passages.append(Passage(
            passage_id=f"wiki::{article_id}::{j}",
            source_row_id=-1,            # sentinel — never matches LIARArg row IDs
            paragraph_index=j,
            text=text_with_title,
        ))
        if len(passages) >= max_paras_per_article:
            break
    return passages


# ────────────────────────────────────────────────────────────────────────────
# Wikipedia streaming
# ────────────────────────────────────────────────────────────────────────────
def stream_wikipedia_passages(
    max_passages: int,
    max_articles: int,
    topic_filter: bool,
    dataset_name: str,
    dataset_config: str,
    max_paras_per_article: int,
    min_words: int,
    progress_every: int = 1000,
) -> list[Passage]:
    """Stream Wikipedia, apply filter, paragraph-split, accumulate up to caps."""
    try:
        from datasets import load_dataset
    except ImportError:
        raise RuntimeError(
            "datasets not installed. Run: pip install datasets"
        )

    print(f"[wiki] streaming {dataset_name}/{dataset_config}")
    ds = load_dataset(dataset_name, dataset_config,
                      split="train", streaming=True)

    passages: list[Passage] = []
    n_articles_seen = 0
    n_articles_kept = 0
    t0 = time.time()

    for article in ds:
        n_articles_seen += 1
        if n_articles_seen > max_articles:
            break
        title = article.get("title", "") or ""
        if topic_filter and not matches_topic(title):
            continue
        text = article.get("text", "") or ""
        if not text:
            continue

        new = article_to_paragraphs(
            article_id=str(article.get("id", n_articles_seen)),
            title=title,
            text=text,
            max_paras_per_article=max_paras_per_article,
            min_words=min_words,
        )
        if new:
            passages.extend(new)
            n_articles_kept += 1

        if n_articles_seen % progress_every == 0:
            elapsed = time.time() - t0
            kept_rate = (n_articles_kept / n_articles_seen * 100
                         if n_articles_seen else 0)
            print(f"  [{n_articles_seen} articles seen | "
                  f"{n_articles_kept} kept ({kept_rate:.1f}%) | "
                  f"{len(passages)} passages | "
                  f"{elapsed:.0f}s]")

        if len(passages) >= max_passages:
            print(f"  hit --max-passages cap ({max_passages}); stopping stream")
            break

    print(f"[wiki] streaming done: {n_articles_seen} articles seen, "
          f"{n_articles_kept} kept, {len(passages)} passages")
    return passages


# ────────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--out-dir", default=str(PROJECT_ROOT / "outputs" / "index_wikipedia"))
    ap.add_argument("--max-passages", type=int, default=150_000,
                    help="Hard cap on indexed passages (default 150k, "
                         "~3× the LIARArg corpus size)")
    ap.add_argument("--max-articles", type=int, default=2_000_000,
                    help="Hard cap on articles streamed before stopping "
                         "(default 2M — basically all of EN Wikipedia; the "
                         "passage cap usually fires first)")
    ap.add_argument("--no-topic-filter", action="store_true",
                    help="Skip the politics-keyword title filter and take all "
                         "streamed articles. Useful for a baseline that isn't "
                         "topic-curated. NB: corpus quality drops sharply.")
    ap.add_argument("--max-paras-per-article", type=int, default=8,
                    help="Cap paragraphs per article to avoid long-article bias")
    ap.add_argument("--min-words", type=int, default=30,
                    help="Drop paragraphs shorter than this many words")
    ap.add_argument("--dataset", default="wikimedia/wikipedia")
    ap.add_argument("--dataset-config", default="20231101.en",
                    help="Wikipedia dump version. 20231101.en is the most "
                         "recent stable EN dump as of 2026.")
    ap.add_argument("--no-bm25", action="store_true")
    ap.add_argument("--no-dense", action="store_true",
                    help="Skip dense-embedding step. Build BM25-only for "
                         "fast iteration; add dense later by re-running "
                         "without this flag.")
    ap.add_argument("--dense-model",
                    default="sentence-transformers/all-MiniLM-L6-v2",
                    help="Must match the dense model the LIAR-aligned index "
                         "uses, so the run-pipeline retriever's encoder "
                         "matches the corpus embeddings.")
    ap.add_argument("--device", default="cpu",
                    help="cpu / mps / cuda. mps recommended on M-series Macs.")
    ap.add_argument("--dense-batch-size", type=int, default=64)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[build_wikipedia_index] out_dir         : {out_dir}")
    print(f"[build_wikipedia_index] max passages    : {args.max_passages}")
    print(f"[build_wikipedia_index] topic-filter    : "
          f"{'OFF' if args.no_topic_filter else 'politics keywords'}")
    print(f"[build_wikipedia_index] bm25            : "
          f"{'no' if args.no_bm25 else 'yes'}")
    print(f"[build_wikipedia_index] dense           : "
          f"{'no' if args.no_dense else f'yes ({args.dense_model})'}")

    # ── Stream + filter + chunk ───────────────────────────────────────────
    passages = stream_wikipedia_passages(
        max_passages=args.max_passages,
        max_articles=args.max_articles,
        topic_filter=not args.no_topic_filter,
        dataset_name=args.dataset,
        dataset_config=args.dataset_config,
        max_paras_per_article=args.max_paras_per_article,
        min_words=args.min_words,
    )

    if not passages:
        print("[build_wikipedia_index] no passages collected — exiting")
        return 1

    # ── Save raw passages immediately, so a crash during dense doesn't lose them
    passages_path = out_dir / "passages.jsonl"
    with open(passages_path, "w") as f:
        for p in passages:
            f.write(json.dumps({
                "passage_id": p.passage_id,
                "source_row_id": p.source_row_id,
                "paragraph_index": p.paragraph_index,
                "text": p.text,
            }) + "\n")
    print(f"[build_wikipedia_index] wrote {len(passages)} passages to "
          f"{passages_path}")

    # ── Build BM25 + dense via existing HybridRetriever ───────────────────
    retriever = HybridRetriever(
        passages=passages,
        dense_model_name=args.dense_model,
        device=args.device,
        use_bm25=not args.no_bm25,
        use_dense=not args.no_dense,
    )
    print("[build_wikipedia_index] building index "
          f"(bm25={not args.no_bm25}, dense={not args.no_dense})...")
    t0 = time.time()
    retriever.build(dense_batch_size=args.dense_batch_size, verbose=True)
    print(f"[build_wikipedia_index] build done in {(time.time()-t0)/60:.1f} min")

    # ── Persist (overwrites the passages.jsonl we wrote above with the
    # canonical HybridRetriever-formatted version + dense.npy + meta.json)
    retriever.save(str(out_dir))
    print(f"[build_wikipedia_index] index saved to {out_dir}")
    print(f"[build_wikipedia_index] ready to run:")
    print(f"  python scripts/run_pipeline.py --n 952 \\")
    print(f"    --data-dir data_liar \\")
    print(f"    --index-dir {out_dir} \\")
    print(f"    --out-dir outputs/results_liar_wikipedia \\")
    print(f"    --verifier ollama --ollama-model qwen2.5:14b-instruct "
          f"--device mps --prior-mode probabilistic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
