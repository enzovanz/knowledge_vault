"""Require every developed note to be linked directly from a same-domain MOC."""

import os
from pathlib import PurePosixPath

from check_links import ROOT, escape_annotation, inventory, links, target_paths
from check_properties import frontmatter


EXCLUDED_ROOTS = {
    "00 - Home", "01 - Templates", "97 - Assets", "98 - Concept Backlog",
    "99 - Concept Inbox", "100 - Resource Inbox",
}


def domain_folder(source, folder):
    parts = PurePosixPath(source).parts
    if (
        len(parts) >= 3 and parts[1] == folder
        and parts[0] not in EXCLUDED_ROOTS and not parts[0].startswith(".")
    ):
        return parts[0]
    return None


def check(root, files):
    notes = {
        source: domain_folder(source, "10 - Knowledge")
        for source in files
        if source.endswith(".md") and domain_folder(source, "10 - Knowledge")
    }
    covered = set()
    moc_count = 0
    for source in sorted(files):
        domain = domain_folder(source, "00 - Home")
        if not source.endswith(".md") or domain is None:
            continue
        text = (root / source).read_text(encoding="utf-8")
        try:
            metadata = frontmatter(text)
        except ValueError:
            # The property checker reports malformed metadata.
            continue
        if metadata is None or metadata.get("type") != "moc":
            continue
        moc_count += 1
        for target, wiki, _ in links(text):
            matches = target_paths(target, source, files, wiki)
            # A non-unique title cannot establish which note the MOC references.
            if matches is not None and len(matches) == 1:
                matched = next(iter(matches))
                if notes.get(matched) == domain:
                    covered.add(matched)
    return len(notes), moc_count, sorted(notes.keys() - covered)


def main():
    note_count, moc_count, uncovered = check(ROOT, inventory(ROOT))
    for source in uncovered:
        domain = domain_folder(source, "10 - Knowledge")
        message = f"No direct reference from a {domain}/00 - Home/ MOC."
        print(f"{source}:1: {message}")
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(
                f"::error file={escape_annotation(source)},line=1::"
                f"{escape_annotation(message)}"
            )
    print(
        f"Checked {note_count} developed notes against {moc_count} MOCs; "
        f"{len(uncovered)} note(s) missing same-domain MOC coverage."
    )
    return 1 if uncovered else 0


if __name__ == "__main__":
    raise SystemExit(main())
