import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from check_moc_coverage import check, main


NOTE = "Tech/10 - Knowledge/Example.md"
MOC = "Tech/00 - Home/Navigation.md"
METADATA = "---\ntype: moc\ndomain: networking\n---\n"


class MocCoverageTests(unittest.TestCase):
    def scan(self, documents):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source, text in documents.items():
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            return check(root, set(documents))

    def test_moc_type_and_folder_domain_determine_coverage(self):
        # Neither the filename nor identical domain property values are required.
        note = "---\ntype: concept\ndomain: software engineering\n---"
        self.assertEqual(self.scan({NOTE: note, MOC: METADATA + "[[Example]]"}), (1, 1, []))

    def test_supported_link_forms(self):
        for reference in (
            "[[Example|Label]]", "[[Example#Heading]]", "![[Example]]",
            "[[Tech/10 - Knowledge/Example]]", "[[/Tech/10 - Knowledge/Example.md]]",
            "[[../10 - Knowledge/Example]]", "[Example](../10%20-%20Knowledge/Example.md)",
            "[Example][ref]\n\n[ref]: ../10%20-%20Knowledge/Example.md",
        ):
            with self.subTest(reference=reference):
                self.assertEqual(self.scan({NOTE: "", MOC: METADATA + reference})[2], [])

    def test_subfolders_are_checked(self):
        nested = "Tech/10 - Knowledge/Nested/Example.md"
        nested_moc = "Tech/00 - Home/Topics/Index.md"
        self.assertEqual(
            self.scan({nested: "", nested_moc: METADATA + "[[Nested/Example]]"}), (1, 1, [])
        )

    def test_one_moc_is_enough(self):
        documents = {
            NOTE: "", MOC: METADATA + "[[Example]]",
            "Tech/00 - Home/Other.md": METADATA,
        }
        self.assertEqual(self.scan(documents), (1, 2, []))

    def test_other_domain_moc_cannot_satisfy_coverage(self):
        documents = {NOTE: "", "Business/00 - Home/Index.md": METADATA + "[[Example]]"}
        self.assertEqual(self.scan(documents), (1, 1, [NOTE]))

    def test_moc_must_be_in_domain_home_folder(self):
        documents = {NOTE: "", "Tech/90 - Resources/Index.md": METADATA + "[[Example]]"}
        self.assertEqual(self.scan(documents), (1, 0, [NOTE]))

    def test_filename_alone_does_not_make_a_moc(self):
        for header in ("", "---\ntype: concept\n---\n", "---\ntype: [\n---\n"):
            with self.subTest(header=header):
                documents = {NOTE: "", "Tech/00 - Home/Example MOC.md": header + "[[Example]]"}
                self.assertEqual(self.scan(documents), (1, 0, [NOTE]))

    def test_indirect_links_do_not_count(self):
        second = "Tech/10 - Knowledge/Second.md"
        documents = {NOTE: "[[Second]]", second: "[[Example]]", MOC: METADATA + "[[Example]]"}
        self.assertEqual(self.scan(documents), (2, 1, [second]))

    def test_code_comments_queries_and_metadata_do_not_count(self):
        for content in (
            "`[[Example]]`", "```md\n[[Example]]\n```",
            "<!-- [[Example]] -->", "```query\npath:\"Tech/10 - Knowledge\"\n```",
            "[external](https://example.com/Example.md)", "[[#Example]]",
        ):
            with self.subTest(content=content):
                self.assertEqual(self.scan({NOTE: "", MOC: METADATA + content})[2], [NOTE])
        metadata_link = METADATA.replace("type: moc", "type: moc\nrelated: '[[Example]]'")
        self.assertEqual(self.scan({NOTE: "", MOC: metadata_link})[2], [NOTE])

    def test_excluded_folders_and_non_markdown_files(self):
        documents = {source: "" for source in (
            "99 - Concept Inbox/Example.md", "98 - Concept Backlog/Tech/Example.md",
            "Tech/90 - Resources/Example.md", "01 - Templates/Example.md",
            "100 - Resource Inbox/Example.md", "README.md",
            "Tech/10 - Knowledge/image.png", "01 - Templates/10 - Knowledge/Example.md",
        )}
        self.assertEqual(self.scan(documents), (0, 0, []))

    def test_missing_moc_leaves_note_uncovered(self):
        self.assertEqual(self.scan({NOTE: ""}), (1, 0, [NOTE]))

    def test_duplicate_titles_need_a_specific_path(self):
        other = "Business/10 - Knowledge/Example.md"
        documents = {NOTE: "", other: "", MOC: METADATA + "[[Example]]"}
        self.assertEqual(self.scan(documents)[2], sorted([NOTE, other]))
        documents[MOC] = METADATA + "[[/Tech/10 - Knowledge/Example]]"
        self.assertEqual(self.scan(documents)[2], [other])

    def test_exit_status_and_github_annotations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in (NOTE, MOC):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")
            output = io.StringIO()
            with (
                patch("check_moc_coverage.ROOT", root),
                patch("check_moc_coverage.inventory", return_value={NOTE, MOC}),
                patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(main(), 1)
                self.assertIn(f"::error file={NOTE},line=1::No direct reference", output.getvalue())
                (root / MOC).write_text(METADATA + "[[Example]]", encoding="utf-8")
                self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
