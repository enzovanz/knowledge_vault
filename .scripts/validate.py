"""Run every vault validation with a readable, optionally colored summary."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
CHECKS = (
    ("Internal links", "check_links.py"),
    ("Note properties", "check_properties.py"),
    ("MOC coverage", "check_moc_coverage.py"),
    ("Unique note titles", "check_duplicate_titles.py"),
)


def use_color(mode):
    if mode != "auto":
        return mode == "always"
    return "NO_COLOR" not in os.environ and (
        sys.stdout.isatty() or os.environ.get("GITHUB_ACTIONS") == "true"
    )


def display(text, passed, color):
    if color:
        text = f"\033[{'32' if passed else '31'}m{text}\033[0m"
    print(text)


def run_checks(color):
    failed = 0
    for label, script in CHECKS:
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / script)],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            passed = result.returncode == 0
            output = result.stdout
        except OSError as error:
            passed = False
            output = f"Could not start check: {error}"
        failed += not passed
        display(f"[{'PASS' if passed else 'FAIL'}] {label}", passed, color)
        for line in output.splitlines():
            if line.startswith("::"):
                # GitHub workflow commands must remain uncolored at column zero.
                print(line)
            else:
                display(f"  {line}", passed, color)
        print()
    display(
        f"{len(CHECKS) - failed}/{len(CHECKS)} checks passed; {failed} failed.",
        failed == 0,
        color,
    )
    return 1 if failed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--color", choices=("auto", "always", "never"), default="auto",
        help="Color output automatically, always, or never (default: auto).",
    )
    args = parser.parse_args(argv)
    return run_checks(use_color(args.color))


if __name__ == "__main__":
    raise SystemExit(main())
