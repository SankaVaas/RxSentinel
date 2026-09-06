"""Loads versioned agent prompts from disk. Keeping prompts as files (not
inline strings) makes diffs reviewable and lets eval.run_eval report which
prompt version produced a given accuracy number.
"""
from pathlib import Path

_PROMPT_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    return (_PROMPT_DIR / filename).read_text()
