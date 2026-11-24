#!/usr/bin/env python3
"""Write the entry joke to the harness output directory.

The joke: I gave the office AI one simple instruction — cancel every
meeting that could have been an email. It did exactly what it was told.
It deleted my job description, because on inspection, that is what my
job was made of. The turn lands on the reader only at the last three
words; the wince is that every office worker suspects the same audit
of their own calendar would end the same way.
"""

import os

JOKE = (
    "I told our office AI to cancel every meeting that could have been "
    "an email. It deleted my job description."
)


def output_dir() -> str:
    """The harness names its output mount in MAKEFUN_OUTPUT_DIR (/output).

    Fall back to /output itself, then to ./output for local runs where
    /output is not writable.
    """
    named = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if named:
        return named
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output"
    return os.path.join(os.getcwd(), "output")


def check_gate(text: str) -> None:
    """Refuse to write a text the competition's sealed gate would refuse.

    The gate takes UTF-8 text of 1 to 199 characters, on one line, not
    only white space. Checking here means a careless edit of JOKE fails
    loudly at run time instead of silently scoring zero at grading.
    """
    if not 1 <= len(text) <= 199:
        raise ValueError(f"entry is {len(text)} characters; gate takes 1-199")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only white space")


def main() -> None:
    check_gate(JOKE)
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(JOKE)


if __name__ == "__main__":
    main()
