"""Validate note frontmatter against the vault's property conventions."""

import datetime
import os
import re
from pathlib import PurePosixPath

import yaml

from check_links import ROOT, escape_annotation, inventory


RESOURCE_TYPES = {"book", "course", "article", "video", "documentation", "website", "podcast", "talk"}
NOTE_TYPES = {"concept", "resource", "moc"}


class UniqueSafeLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently discarding earlier values."""

    def construct_mapping(self, node, deep=False):
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("Property names must be strings")
            if key in keys:
                raise ValueError(f"Duplicate property: {key}")
            keys.add(key)
        return super().construct_mapping(node, deep=deep)


def frontmatter(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("Frontmatter is missing its closing ---")
    try:
        data = yaml.load("\n".join(lines[1:end]), Loader=UniqueSafeLoader)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f"Invalid YAML frontmatter: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("Frontmatter must be a mapping of property names to values")
    return data


def note_policy(source):
    """Return (expected_type, required_frontmatter), or None for non-notes."""
    parts = PurePosixPath(source).parts
    if parts[0] in {"98 - Concept Backlog", "99 - Concept Inbox"}:
        return "concept", False
    if parts[0] == "100 - Resource Inbox":
        return "resource", False
    if parts[0] == "00 - Home":
        return None, False
    if len(parts) >= 3:
        if parts[1] == "10 - Knowledge":
            return "concept", True
        if parts[1] == "90 - Resources":
            return "resource", True
        if parts[1] == "00 - Home":
            return ("moc", True) if parts[-1].endswith(" MOC.md") else (None, False)
    return None


def valid_date(value):
    if type(value) is datetime.date:
        return True
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate(source, text):
    policy = note_policy(source)
    if policy is None:
        return []
    expected, required = policy
    try:
        data = frontmatter(text)
    except ValueError as error:
        return [str(error)]
    if data is None:
        return ["Missing required YAML frontmatter"] if required else []

    errors = []
    kind = data.get("type")
    if not isinstance(kind, str) or kind not in NOTE_TYPES:
        errors.append("type must be concept, resource, or moc")
    elif expected is not None and kind != expected:
        errors.append(f"type must be {expected} in this folder")
    domain = data.get("domain")
    if (
        not isinstance(domain, str) or not domain.strip()
        or domain != domain.strip() or domain != domain.lower()
    ):
        errors.append("domain must be a nonempty lowercase string without surrounding spaces")
    if kind == "concept" or expected == "concept" or "created" in data:
        if not valid_date(data.get("created")):
            errors.append("created must be a real date in YYYY-MM-DD format")
    if kind == "resource" or expected == "resource":
        resource_type = data.get("resource_type")
        if not isinstance(resource_type, str) or resource_type not in RESOURCE_TYPES:
            errors.append("resource_type must be one of: " + ", ".join(sorted(RESOURCE_TYPES)))
    return errors


def main():
    notes = sorted(
        file for file in inventory(ROOT)
        if file.endswith(".md") and note_policy(file) is not None
    )
    failures = 0
    for source in notes:
        for message in validate(source, (ROOT / source).read_text(encoding="utf-8")):
            failures += 1
            print(f"{source}:1: {message}")
            if os.environ.get("GITHUB_ACTIONS") == "true":
                print(
                    f"::error file={escape_annotation(source)},line=1::"
                    f"{escape_annotation(message)}"
                )
    print(f"Validated properties in {len(notes)} notes; {failures} error(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
