# have-you-tried-turning-it-off — entry for make.fun
# "Have You Tried Turning It Off?".
#
# The program writes one funny line, under 200 characters, that a
# hopeless tech support agent says to a desperate customer, to
# $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt by default).
# Python 3, no network, no dependencies.
#
# The joke twists the classic advice: instead of asking the customer
# to restart, the agent cheerfully restarted everything on their own
# end and declared victory — the customer's problem survives, now
# framed as the only broken thing left on the call.

import os
import sys

ENTRY = (
    "Great news: I restarted everything on my end and it's fixed. "
    "From my screen, the only thing still broken is your problem."
)


def count_code_points(text):
    return len(text)


def validate(text):
    n = count_code_points(text)
    if n < 1 or n > 199:
        raise ValueError("entry must be 1-199 characters, got %d" % n)
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def verify_written(out_path):
    # Read back what was written and re-validate, so a bad write fails
    # loudly here instead of shipping a bad entry to the grader.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    validate(written)
    if written != ENTRY:
        raise ValueError("round-trip mismatch: written text differs from entry")
    print("wrote %d characters to %s" % (count_code_points(written), out_path))


def main():
    validate(ENTRY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # Write atomically, then verify: the gate counts every character,
    # and the text is exactly 121 characters as written, with no
    # trailing newline.
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.replace(tmp_path, out_path)
    verify_written(out_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - fail loudly, exit non-zero
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
