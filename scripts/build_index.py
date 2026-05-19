"""Build the hybrid retrieval index.

Index is built over the union of train + val rows. Test-row paragraphs are
NOT indexed: even though `exclude_row_ids` would block them, keeping the
test corpus out entirely avoids any accidental cross-fold leakage.

Run after prepare_data.py:
    python scripts/build_index.py
"""
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_split
from src.retriever import HybridRetriever, build_corpus_from_rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(PROJECT_ROOT / "data"))
    ap.add_argument("--out-dir", default=str(PROJECT_ROOT / "outputs" / "index"))
    ap.add_argument("--dense-model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--no-bm25", action="store_true")
    ap.add_argument("--no-dense", action="store_true")
    ap.add_argument("--include-test", action="store_true",
                    help="Also index test-set paragraphs (default: train+val only)")
    args = ap.parse_args()

    split = load_split(args.data_dir)
    rows = list(split.get("train", [])) + list(split.get("val", []))
    if args.include_test:
        rows += list(split.get("test", []))
    print(f"[build_index] {len(rows)} rows -> building paragraph corpus")

    passages = build_corpus_from_rows(rows)
    print(f"[build_index] {len(passages)} passages")

    retriever = HybridRetriever(
        passages=passages,
        dense_model_name=args.dense_model,
        device=args.device,
        use_bm25=not args.no_bm25,
        use_dense=not args.no_dense,
    )
    retriever.build(verbose=True)
    retriever.save(args.out_dir)
    print(f"[build_index] saved index to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
