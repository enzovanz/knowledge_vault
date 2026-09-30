import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from check_properties import main, validate


CONCEPT = "Tech/10 - Knowledge/Example.md"
RESOURCE = "Tech/90 - Resources/Example.md"
MOC = "Tech/00 - Home/Example MOC.md"
VALID_CONCEPT = "---\ntype: concept\ndomain: software engineering\ncreated: 2026-09-30\n---\n"


class PropertyCheckerTests(unittest.TestCase):
    def test_valid_concept_with_quoted_or_unquoted_date(self):
        self.assertEqual(validate(CONCEPT, VALID_CONCEPT), [])
        self.assertEqual(validate(CONCEPT, VALID_CONCEPT.replace("2026-09-30", '"2026-09-30"')), [])

    def test_resources_and_mocs_do_not_require_created(self):
        resource = "---\ntype: resource\ndomain: finance\nresource_type: book\nauthor:\n  - Someone\n---"
        moc = "---\ntype: moc\ndomain: finance\n---"
        self.assertEqual(validate(RESOURCE, resource), [])
        self.assertEqual(validate(MOC, moc), [])

    def test_finished_notes_and_mocs_require_frontmatter(self):
        for source in (CONCEPT, RESOURCE, MOC):
            with self.subTest(source=source):
                self.assertEqual(validate(source, "A note."), ["Missing required YAML frontmatter"])

    def test_captures_and_home_pages_can_omit_frontmatter(self):
        for source in (
            "99 - Concept Inbox/Idea.md",
            "98 - Concept Backlog/Tech/Idea.md",
            "100 - Resource Inbox/Book.md",
            "00 - Home/Enzo Knowledge Base.md",
            "Tech/00 - Home/Tech Knowledge.md",
        ):
            with self.subTest(source=source):
                self.assertEqual(validate(source, "A rough note."), [])

    def test_capture_metadata_is_validated_when_present(self):
        self.assertTrue(validate("99 - Concept Inbox/Idea.md", "---\ntype: concept\n---"))

    def test_templates_and_repository_docs_are_exempt(self):
        for source in ("01 - Templates/Concept Template.md", "README.md", "LEARNING-example.md"):
            with self.subTest(source=source):
                self.assertEqual(validate(source, "---\ncreated: {{date:YYYY-MM-DD}}\n---"), [])

    def test_missing_required_fields(self):
        errors = validate(CONCEPT, "---\ntype: concept\n---")
        self.assertTrue(any("domain" in error for error in errors))
        self.assertTrue(any("created" in error for error in errors))

    def test_invalid_type_or_folder_role(self):
        for kind in ("unknown", "[concept]", "resource"):
            with self.subTest(kind=kind):
                errors = validate(CONCEPT, VALID_CONCEPT.replace("type: concept", f"type: {kind}"))
                self.assertTrue(any("type must" in error for error in errors))

    def test_domain_must_be_nonempty_lowercase_text(self):
        for domain in ("", "Software Engineering", '" finance "', "[finance]", "123"):
            with self.subTest(domain=domain):
                text = VALID_CONCEPT.replace("domain: software engineering", f"domain: {domain}")
                self.assertTrue(any("domain" in error for error in validate(CONCEPT, text)))

    def test_invalid_calendar_dates_and_formats(self):
        for created in (
            "2026-02-30", '"2026-9-1"', '"tomorrow"', "2026-09-30T10:00:00",
            "null", "[2026-09-30]", "true",
        ):
            with self.subTest(created=created):
                self.assertTrue(validate(CONCEPT, VALID_CONCEPT.replace("2026-09-30", created)))

    def test_optional_created_is_validated(self):
        text = "---\ntype: moc\ndomain: finance\ncreated: yesterday\n---"
        self.assertTrue(any("created" in error for error in validate(MOC, text)))

    def test_resource_type_is_required_and_restricted(self):
        for value in ("", "novel", "[book]"):
            text = f"---\ntype: resource\ndomain: finance\nresource_type: {value}\n---"
            self.assertTrue(any("resource_type" in error for error in validate(RESOURCE, text)))

    def test_malformed_yaml_and_duplicate_properties(self):
        for text in (
            "---\ntype: concept", "---\n- concept\n---", "---\n---",
            "---\ntype: [\n---", "---\ntype: concept\ntype: resource\n---",
            "---\n[]: value\n---", "---\nx: !!python/object:builtins.object {}\n---",
        ):
            with self.subTest(text=text):
                self.assertTrue(validate(CONCEPT, text))

    def test_line_endings_and_bom(self):
        self.assertEqual(validate(CONCEPT, "\ufeff" + VALID_CONCEPT.replace("\n", "\r\n")), [])

    def test_exit_status_and_annotations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / CONCEPT
            path.parent.mkdir(parents=True)
            path.write_text("No properties.", encoding="utf-8")
            output = io.StringIO()
            with (
                patch("check_properties.ROOT", root),
                patch("check_properties.inventory", return_value={CONCEPT}),
                patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(main(), 1)
                self.assertIn(f"::error file={CONCEPT},line=1::", output.getvalue())
                path.write_text(VALID_CONCEPT, encoding="utf-8")
                self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
