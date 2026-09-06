# Data Sources

| Source | Use | License / access notes |
|---|---|---|
| RxNorm / RxNav API | Structured drug-drug interaction ground truth, RxCUI normalization | Free, NIH/NLM public API. Rate-limited; cache aggressively. |
| OpenFDA drug label API | Boxed warnings, `drug_interactions` label sections | Free, public. Label data lags real-world approvals by weeks-months. |
| DailyMed | Secondary label source (SPL documents) | Free, public. |
| DrugBank | Richer interaction mechanism descriptions, drug taxonomy | **Requires an academic or commercial license** — not bundled with this repo. `app/rag/ingestion/load_drugbank.py` is a stub pending license acquisition. |
| PubMed / bioRxiv (future) | Case-report-level evidence for rare/emerging interactions | Free for abstracts; full text may require institutional access. Not yet wired into `retrieval_agent`. |

## Important caveat

RxNorm's interaction API (`interaction/list.json`) was deprecated by NLM in
early 2024 in favor of other NLM interaction resources in some
deployments — **verify current API availability before relying on this in
a real deployment** and check https://lhncbc.nlm.nih.gov/RxNav/APIs/ for the
current recommended endpoint at build time.
