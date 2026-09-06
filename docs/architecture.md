# RxSentinel Architecture

## Why an agent graph, not a single LLM call

A single prompt like "check these medications for interactions" has three
failure modes that matter a lot in a clinical context:

1. **Hallucinated interactions** — the model states a risk that isn't real.
2. **Missed interactions** — the model doesn't recall a real, dangerous pair.
3. **Context-blind severity** — the model flags a mechanism that doesn't
   actually apply to this patient (e.g. renal clearance interaction in a
   patient with normal kidney function).

RxSentinel addresses each failure mode with a dedicated node rather than
hoping a bigger prompt fixes all three at once:

| Failure mode | Mitigation | Node |
|---|---|---|
| Hallucinated interaction | Verify against structured ground truth (RxNorm/OpenFDA) before any LLM reasoning | `interaction_tool_agent` |
| Missed interaction | Retrieve literature/label context per drug pair rather than relying on parametric recall | `retrieval_agent` |
| Context-blind severity | Explicit patient-context input (eGFR, hepatic function, age) to every reasoning step | `patient_context_agent`, `reasoning_agent`, `critique_agent` |
| Overreach / false positive reaching a clinician | Adversarial falsification pass before escalation | `critique_agent` |

## Agent graph

```
patient_context_agent
        │
        ▼
retrieval_agent
        │
        ▼
interaction_tool_agent
        │
        ▼
reasoning_agent
        │
        ▼
critique_agent
        │
        ▼
escalation_agent
```

Each node's input/output is persisted as an `AgentRunStep` row
(`app/models/agent_run.py`), making the whole run replayable and auditable —
this is what the frontend's `AgentTraceViewer` renders and what
`eval/run_eval.py` scores against golden datasets.

## Data flow contract

State shape lives in `app/agents/state.py` as a single `TypedDict`. Nodes
only ever add to or transform this state — see the reducer functions
(`operator.add` on list fields) so that LangGraph can merge partial updates
from nodes without one node's output clobbering another's.

## Why a critique agent specifically

Most agentic-RAG systems stop at "retrieve, then generate." The critique
node exists because in a safety-critical domain, the cost of a false
positive (alert fatigue, clinician trust erosion) and a false negative
(patient harm) are both severe — and an LLM asked to *generate* a finding is
architecturally biased toward confirming its own output. Asking a *second*,
adversarially-prompted call to falsify the first call's claim is a cheap way
to catch overreach before it reaches a human.

## What's stubbed vs. production-real in this scaffold

- **Real**: FastAPI app structure, SQLAlchemy models, LangGraph wiring, node
  logic, RxNorm/OpenFDA HTTP clients, audit trail persistence, React UI.
- **Stubbed (explicit `NotImplementedError` or TODO)**: embeddings provider
  wiring, pgvector ingestion pipelines, OIDC JWKS verification, Celery task
  bodies. These are the pieces that require external credentials/licensed
  data (DrugBank) or a deployment target to wire up meaningfully — the
  interfaces are in place so implementing them is additive, not a redesign.
