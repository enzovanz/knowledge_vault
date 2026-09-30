"""Check local file targets in the vault's Markdown notes."""

import os
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]


def wikilink(state, silent):
    start = state.pos
    opening = start + 1 if state.src.startswith("![[", start) else start
    if not state.src.startswith("[[", opening):
        return False
    end = state.src.find("]]", opening + 2)
    if end < 0 or "\n" in state.src[opening:end]:
        return False
    if not silent:
        token = state.push("wikilink", "", 0)
        token.content = state.src[opening + 2:end].split("|", 1)[0]
    state.pos = end + 2
    return True


def links(text):
    """Yield (target, is_wikilink, containing_block_line) outside code."""
    # Frontmatter is metadata, not Markdown. Keep its line count for diagnostics.
    text = re.sub(
        r"\A---\r?\n.*?\r?\n---(?:\r?\n|$)",
        lambda match: "\n" * match[0].count("\n"),
        text,
        count=1,
        flags=re.S,
    )
    parser = MarkdownIt("commonmark").enable("table")
    parser.inline.ruler.before("link", "wikilink", wikilink)
    for block in parser.parse(text):
        if block.type != "inline":
            continue
        line = block.map[0] + 1
        for token in block.children or []:
            if token.type == "wikilink":
                yield token.content, True, line
            elif token.type == "link_open":
                yield token.attrGet("href"), False, line
            elif token.type == "image":
                yield token.attrGet("src"), False, line


def target_paths(target, source, files, wiki=False):
    """Return matching file paths, or None for external/same-note links."""
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
        return None
    # Decode after splitting: %23 can be part of a filename.
    path = target.split("#", 1)[0]
    if not wiki:
        path = path.split("?", 1)[0]
    path = unquote(path).strip()
    if not path:
        return None

    names = (path, path + ".md")
    relative = path.startswith(("./", "../"))
    rooted = path.startswith("/")
    parent = posixpath.dirname(source)
    matches = set()
    for name in names:
        candidates = (
            [posixpath.normpath(name.lstrip("/"))]
            if rooted
            else [
                posixpath.normpath(posixpath.join(parent, name)),
                posixpath.normpath(name),
            ]
        )
        if relative:
            candidates = candidates[:1]
        matches.update(candidate for candidate in candidates if candidate in files)
        # Obsidian permits shortest unique paths, including bare note titles.
        if not relative and not rooted:
            matches.update(file for file in files if file.endswith("/" + name))
    return matches


def target_exists(target, source, files, wiki=False):
    matches = target_paths(target, source, files, wiki)
    return matches is None or bool(matches)


def inventory(root):
    """Include tracked and new files, excluding Git-ignored local state."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return {
        name
        for name in result.stdout.decode("utf-8").split("\0")
        if name and (root / name).is_file()
    }


def check(root, files):
    failures = []
    count = 0
    notes = sorted(file for file in files if file.endswith(".md"))
    for source in notes:
        for target, wiki, line in links((root / source).read_text(encoding="utf-8")):
            count += 1
            if not target_exists(target, source, files, wiki):
                failures.append((source, line, target))
    return notes, count, failures


def escape_annotation(value):
    return (
        value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        .replace(",", "%2C").replace(":", "%3A")
    )


def main():
    notes, count, failures = check(ROOT, inventory(ROOT))
    for source, line, target in failures:
        print(f"{source}:{line}: Missing file: {target}")
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(
                f"::error file={escape_annotation(source)},line={line}::"
                f"Missing file: {escape_annotation(target)}"
            )
    print(
        f"Checked {len(notes)} Markdown files and {count} links; "
        f"{len(failures)} missing file target(s)."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
