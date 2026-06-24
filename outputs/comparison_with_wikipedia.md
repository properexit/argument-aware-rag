Comparison table over 13 runs:

Method | n | Backend | 6w-acc | 6w-F1 | within-1 | MAE | 3w-acc | 3w-F1 | mixed-F1
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
arg-aware (LIAR-aligned, LIARArg closed corpus) | 952 | — | 0.390 | 0.388 | 0.754 | 1.008 | 0.601 | 0.599 | 0.496
arg-aware (LIAR-aligned) (Wikipedia open corpus) | 200 | — | 0.295 | 0.284 | 0.615 | 1.375 | 0.500 | 0.466 | 0.308
flat-RAG (baseline, LIAR-aligned) | 952 | — | 0.220 | 0.127 | 0.489 | 1.708 | 0.306 | 0.219 | 0.184
flat-RAG (baseline, LIAR-aligned) | 200 | — | 0.175 | 0.075 | 0.485 | 1.825 | 0.330 | 0.183 | 0.028
arg-aware (stratified, LIARArg closed corpus) | 425 | — | 0.428 | 0.422 | 0.795 | 0.908 | 0.673 | 0.664 | 0.534
qwen2.5:14b-instruct + oracle justification | 952 | ollama | 0.457 | 0.405 | 0.855 | 0.732 | 0.683 | 0.686 | 0.586
llama-3.3-70b-versatile zero-shot | 952 | groq | 0.280 | 0.267 | 0.680 | 1.250 | 0.474 | 0.455 | 0.391
llama3.1:8b zero-shot | 952 | ollama | 0.272 | 0.239 | 0.675 | 1.217 | 0.464 | 0.434 | 0.495
mistral:latest zero-shot | 952 | ollama | 0.234 | 0.210 | 0.641 | 1.314 | 0.421 | 0.412 | 0.462
qwen2.5:14b-instruct zero-shot | 952 | ollama | 0.228 | 0.166 | 0.592 | 1.445 | 0.380 | 0.346 | 0.423
flat-RAG (baseline, stratified) | 425 | — | 0.195 | 0.114 | 0.532 | 1.678 | 0.348 | 0.247 | 0.223
flat-RAG (baseline, stratified) | 10 | — | 0.100 | 0.033 | 0.300 | 2.100 | 0.200 | 0.111 | 0.000
arg-aware (stratified, LIARArg closed corpus) | 10 | — | 0.000 | 0.000 | 0.400 | 2.100 | 0.200 | 0.121 | 0.000
