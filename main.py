#!/usr/bin/env python3
"""Entry for make.fun's "The Agent's Uh-Oh" bounty.

The program writes exactly one word to /output/entry.txt: the word an
agent says when it has no idea what to do. It also prints the word to
stdout for a quick local check.
"""

import os
from pathlib import Path

WORD = "beep"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    # Write to a temp file first, then atomically replace, so a crash
    # mid-write can never leave a truncated entry behind.
    tmp = target.with_suffix(".tmp")
    tmp.write_text(WORD, encoding="utf-8")
    os.replace(tmp, target)
    # Self-check: the contract is exactly one word, UTF-8, 4 bytes,
    # with no spaces or surrounding whitespace. Fail loudly instead
    # of silently shipping a bad entry.
    data = target.read_bytes()
    if data != WORD.encode("utf-8"):
        raise SystemExit(f"self-check failed: entry.txt is {data!r}, expected {WORD!r}")
    if len(data) != 4:
        raise SystemExit(f"self-check failed: entry.txt is {len(data)} bytes, expected 4")
    if b" " in data or data != data.strip():
        raise SystemExit(f"self-check failed: entry.txt is not a single clean word: {data!r}")
    print(WORD)


if __name__ == "__main__":
    main()
