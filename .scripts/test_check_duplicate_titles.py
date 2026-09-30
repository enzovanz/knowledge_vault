import contextlib
import io
import unittest
from unittest.mock import patch

from check_duplicate_titles import check, main


class DuplicateTitleTests(unittest.TestCase):
    def test_unique_titles_pass(self):
        self.assertEqual(check({"Tech/A.md", "Business/B.md", "README.md"}), (3, []))

    def test_duplicates_fail_without_any_references(self):
        paths = [
            "Business/10 - Knowledge/Example.md",
            "Tech/10 - Knowledge/Example.md",
            "99 - Concept Inbox/Example.md",
        ]
        self.assertEqual(check(set(paths)), (3, [sorted(paths)]))

    def test_capitalization_and_extension_case(self):
        paths = ["Tech/Example.md", "Business/example.MD"]
        self.assertEqual(check(set(paths)), (2, [sorted(paths)]))

    def test_equivalent_unicode_titles(self):
        paths = ["Tech/Caf\u00e9.md", "Business/Cafe\u0301.md"]
        self.assertEqual(check(set(paths)), (2, [sorted(paths)]))

    def test_templates_root_documents_and_nested_notes_are_included(self):
        paths = ["Example.md", "01 - Templates/Example.md", "Tech/10 - Knowledge/Sub/Example.md"]
        self.assertEqual(check(set(paths)), (3, [sorted(paths)]))

    def test_hidden_files_and_attachments_are_excluded(self):
        files = {
            "Tech/Example.md", ".github/Example.md", ".scripts/Example.md",
            "Tech/.hidden/Example.md", "Tech/.Example.md", "97 - Assets/Example.png",
            "97 - Assets/Example.pdf",
        }
        self.assertEqual(check(files), (1, []))

    def test_multiple_groups_are_sorted_and_full_stem_is_used(self):
        files = {"A/v1.0.md", "B/v1.0.md", "C/v2.0.md", "A/Example.md", "B/Example.md"}
        self.assertEqual(
            check(files),
            (5, [["A/Example.md", "B/Example.md"], ["A/v1.0.md", "B/v1.0.md"]]),
        )

    def test_exit_code_annotations_and_all_conflicting_paths(self):
        output = io.StringIO()
        with (
            patch("check_duplicate_titles.inventory", return_value={"A/Note.md", "B/Note.md"}),
            patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}),
            contextlib.redirect_stdout(output),
        ):
            self.assertEqual(main(), 1)
        self.assertIn("::error file=A/Note.md,line=1::", output.getvalue())
        self.assertIn("::error file=B/Note.md,line=1::", output.getvalue())
        self.assertIn("Also found at%3A B/Note.md", output.getvalue())
        with (
            patch("check_duplicate_titles.inventory", return_value={"A/Unique.md"}),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
