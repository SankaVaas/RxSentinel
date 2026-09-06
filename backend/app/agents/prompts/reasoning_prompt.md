# Reasoning Agent — System Prompt (reference copy)

See `app/agents/nodes/reasoning_agent.py::REASONING_SYSTEM_PROMPT` for the
version actually used at runtime. This file exists so prompt changes are
reviewable in PRs without diffing Python logic, and so the eval harness
(`eval/run_eval.py`) can load prompt versions independently of code changes.

## Design notes
- Explicitly instructed to default to "low/low-confidence" over guessing —
  the failure mode we're defending against is confident overreach, not
  underclaiming.
- Every output field is grounded in the `evidence` list passed in; the model
  is never asked to recall drug interactions from parametric memory alone.
