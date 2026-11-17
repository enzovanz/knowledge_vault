import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from check_moc_coverage import check
from check_resource_coverage import main


RESOURCE = "Tech/90 - Resources/Example.md"
MOC = "Tech/00 - Home/Navigation.md"
METADATA = "---\ntype: moc\ndomain: networking\n---\n"


class ResourceCoverageTests(unittest.TestCase):
    def scan(self, documents):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source, text in documents.items():
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            return check(root, set(documents), folder="90 - Resources")

    def test_missing_link_fails_even_without_resource_metadata(self):
        self.assertEqual(self.scan({RESOURCE: "", MOC: METADATA}), (1, 1, [RESOURCE]))

    def test_same_folder_domain_is_required_not_matching_domain_property(self):
        resource = "---\ntype: resource\ndomain: computer science\n---\n"
        self.assertEqual(self.scan({RESOURCE: resource, MOC: METADATA + "[[Example]]"}), (1, 1, []))
        self.assertEqual(self.scan({RESOURCE: resource, "Business/00 - Home/Index.md": METADATA + "[[Example]]"})[2], [RESOURCE])

    def test_supported_links(self):
        for reference in (
            "[[Example]]", "[[Example|Label]]", "[[Example#Heading]]", "![[Example]]",
            "[[Tech/90 - Resources/Example]]", "[[../90 - Resources/Example]]",
            "[Example](../90%20-%20Resources/Example.md)",
            "[Example][ref]\n\n[ref]: ../90%20-%20Resources/Example.md",
        ):
            with self.subTest(reference=reference):
                self.assertEqual(self.scan({RESOURCE: "", MOC: METADATA + reference})[2], [])

    def test_nested_resources_and_one_of_multiple_mocs(self):
        nested = "Tech/90 - Resources/Books/Example.md"
        self.assertEqual(self.scan({nested: "", MOC: METADATA,
                                   "Tech/00 - Home/Topics/Index.md": METADATA + "[[Books/Example]]"}), (1, 2, []))

    def test_only_processed_markdown_resources_are_required(self):
        documents = {path: "" for path in (
            "100 - Resource Inbox/Example.md", "Tech/10 - Knowledge/Example.md",
            "01 - Templates/90 - Resources/Example.md", "Tech/90 - Resources/image.png",
        )}
        self.assertEqual(self.scan(documents), (0, 0, []))

    def test_only_direct_links_from_mocs_in_domain_home_count(self):
        for source, content in (
            (MOC, "[[Example]]"),
            ("Tech/90 - Resources/Index.md", METADATA + "[[Example]]"),
            (MOC, METADATA + "<!-- [[Example]] -->"),
            (MOC, METADATA + "```query\npath:\"Tech/90 - Resources\"\n```"),
            (MOC, METADATA + "`[[Example]]`"),
            (MOC, METADATA + "[[Intermediate]]"),
        ):
            with self.subTest(source=source, content=content):
                self.assertIn(RESOURCE, self.scan({RESOURCE: "", source: content,
                              "Tech/10 - Knowledge/Intermediate.md": "[[Example]]"})[2])

    def test_ambiguous_title_needs_a_specific_path(self):
        other = "Business/90 - Resources/Example.md"
        documents = {RESOURCE: "", other: "", MOC: METADATA + "[[Example]]"}
        self.assertEqual(self.scan(documents)[2], sorted([RESOURCE, other]))
        documents[MOC] = METADATA + "[[/Tech/90 - Resources/Example]]"
        self.assertEqual(self.scan(documents)[2], [other])

    def test_command_exit_status_and_ci_annotation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / MOC).parent.mkdir(parents=True)
            (root / MOC).write_text(METADATA, encoding="utf-8")
            output = io.StringIO()
            with (
                patch("check_moc_coverage.ROOT", root),
                patch("check_moc_coverage.inventory", return_value={RESOURCE, MOC}),
                patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(main(), 1)
                self.assertIn(f"::error file={RESOURCE},line=1::No direct reference", output.getvalue())
                self.assertIn("1 processed resources", output.getvalue())
                (root / MOC).write_text(METADATA + "[[Example]]", encoding="utf-8")
                self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
