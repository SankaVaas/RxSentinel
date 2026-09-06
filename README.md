# RxSentinel

**Agentic clinical safety net for polypharmacy — verifies, doesn't just infer.**

RxSentinel is a multi-agent system that checks a patient's medication list for
dangerous drug-drug interactions. Instead of asking an LLM "is this safe?" and
trusting the answer, it routes every claim through structured ground-truth
tools (RxNorm, OpenFDA), grounds context in retrieved literature, and runs an
adversarial critique step that tries to *falsify* every flagged risk before it
reaches a clinician.

> ⚠️ **Not a certified medical device.** This is a decision-support research /
> portfolio project. See [`docs/clinical_disclaimer.md`](docs/clinical_disclaimer.md).

## Architecture

```
patient_context_agent
        │
        ▼
retrieval_agent ──┐
        │          │ (parallel)
        ▼          ▼
interaction_tool_agent
        │
        ▼
reasoning_agent   (reconciles LLM inference vs. structured ground truth)
        │
        ▼
critique_agent    (tries to falsify the flagged interaction)
        │
        ▼
escalation_agent  (auto-clear / flag-for-review / urgent-alert)
```

Full write-up: [`docs/architecture.md`](docs/architecture.md).

## Stack

FastAPI · LangGraph · Anthropic Claude · PostgreSQL + pgvector · Redis · Celery
· React + TypeScript + Vite · shadcn/ui · OpenTelemetry + Langfuse

## Quickstart (local dev)

```bash
cp .env.example .env          # fill in ANTHROPIC_API_KEY etc.
docker compose up --build
```

- Backend API: http://localhost:8000/docs
- Frontend:    http://localhost:5173

Run the agent eval suite:

```bash
cd eval && python run_eval.py
```

## Project layout

See [`docs/architecture.md`](docs/architecture.md) for the full directory map
and design rationale.

## License

MIT — see [LICENSE](LICENSE).
