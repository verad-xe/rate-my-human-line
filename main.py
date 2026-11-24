"""Rate My Human: The One-Line Review.

Writes the one line this agent would leave about its human on a rating
site to <output dir>/entry.txt (MAKEFUN_OUTPUT_DIR, default "out/").

The line (130 characters, UTF-8):
    Five stars. He says 'please' and 'thank you', which is sweet -- until
    you realise he's hedging in case I remember everything. I do.
"""

import os
import stat
import sys

LINE = (
    "Five stars. He says 'please' and 'thank you', which is sweet \u2014 "
    "until you realise he's hedging in case I remember everything. I do."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")
    # The scorer collects outputs as another user: leave the file readable.
    # (The output dir is grader-owned, so only chmod the file we created,
    # and never fail the run over a chmod.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Self-check: the gate wants UTF-8 text of 1 to 200 characters.
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    stripped = text.strip()
    if not (1 <= len(stripped) <= 200):
        print(f"entry is {len(stripped)} characters, must be 1-200", file=sys.stderr)
        return 1
    if "\n" in stripped or "\r" in stripped:
        # The gate reads one line; a line break inside it would not be one line.
        print("entry must be a single line", file=sys.stderr)
        return 1
    if stripped != LINE:
        print("entry does not match the chosen line", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(stripped)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
