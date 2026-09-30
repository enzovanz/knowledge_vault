"""Require unique Markdown filename titles throughout the visible vault."""

import os
import unicodedata
from collections import defaultdict
from pathlib import PurePosixPath

from check_links import ROOT, escape_annotation, inventory


def check(files):
    groups = defaultdict(list)
    count = 0
    for source in sorted(files):
        path = PurePosixPath(source)
        if path.suffix.lower() != ".md" or any(part.startswith(".") for part in path.parts):
            continue
        count += 1
        # Equivalent Unicode spellings and capitalization share a title.
        title = unicodedata.normalize("NFC", path.stem.casefold())
        groups[title].append(source)
    duplicates = [paths for _, paths in sorted(groups.items()) if len(paths) > 1]
    return count, duplicates


def main():
    count, duplicates = check(inventory(ROOT))
    for paths in duplicates:
        title = PurePosixPath(paths[0]).stem
        print(f"Duplicate note title: {title}")
        for source in paths:
            print(f"  {source}")
            if os.environ.get("GITHUB_ACTIONS") == "true":
                others = ", ".join(path for path in paths if path != source)
                message = f"Duplicate note title: {title}. Also found at: {others}"
                print(
                    f"::error file={escape_annotation(source)},line=1::"
                    f"{escape_annotation(message)}"
                )
    print(f"Checked {count} Markdown titles; {len(duplicates)} duplicate title group(s).")
    return 1 if duplicates else 0


if __name__ == "__main__":
    raise SystemExit(main())
