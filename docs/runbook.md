# Runbook

## Common incidents

### Agent run stuck in `RUNNING`
Likely cause: an external API call (RxNorm/OpenFDA/Anthropic) hung past
the `httpx` timeout without raising — check `tenacity` retry logs in
`app/tools/base_tool.py`. Mitigation: add a hard wall-clock timeout around
`graph.astream(...)` in `interaction_service.py`.

### Critique agent returning malformed JSON frequently
Check `app/agents/nodes/critique_agent.py` — on JSON parse failure the
system fails closed to `pending_review`, so patient safety isn't at risk,
but a spike in this indicates prompt drift after a model version bump.
Compare against `eval/golden_datasets/edge_cases.jsonl` scenario
`critique_agent_api_failure`.

### RxNorm API returning 429s
NLM's public API has undocumented informal rate limits. Add a Redis-backed
request-rate limiter in `app/tools/rxnorm_client.py` and consider caching
interaction lookups per RxCUI pair for 24h (interaction data changes
infrequently).

## On-call escalation
Any incident affecting the `escalation_agent` routing logic (urgent findings
not reaching the review queue) should page immediately — this is the
patient-safety-critical path.
