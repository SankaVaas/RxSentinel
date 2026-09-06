# Critique Agent — System Prompt (reference copy)

See `app/agents/nodes/critique_agent.py::CRITIQUE_SYSTEM_PROMPT` for the
runtime version.

## Design notes
- Framed adversarially ("try to DISPROVE") rather than "double check" —
  in practice, review-framed prompts anchor on the original conclusion far
  more than falsification-framed prompts.
- Checks patient-context relevance explicitly (e.g. a renal-clearance
  interaction is irrelevant if eGFR is normal) — this is the check most
  likely to catch generic-literature-match false positives.
- Fails closed: if the critique step itself errors, the finding is NOT
  auto-cleared; it defaults to human review (see escalation_agent.py).
