import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from check_links import check, inventory, links, main, target_exists


class LinkCheckerTests(unittest.TestCase):
    def test_wikilinks_aliases_embeds_and_headings(self):
        text = "[[Note|label]] ![[photo.png|200]] [[Other#Heading]] [[#Local]]"
        self.assertEqual(
            [(target, wiki) for target, wiki, _ in links(text)],
            [("Note", True), ("photo.png", True), ("Other#Heading", True), ("#Local", True)],
        )

    def test_markdown_links_images_and_references(self):
        text = (
            "[note](Note%20one.md) ![image](image.png)\n"
            "[aot](<Ahead-of-time compilation (AOT).md>) [ref][id]\n\n"
            "[id]: target.md \"Title\"\n"
        )
        self.assertEqual(
            [target for target, _, _ in links(text)],
            ["Note%20one.md", "image.png", "Ahead-of-time%20compilation%20(AOT).md", "target.md"],
        )

    def test_code_metadata_comments_and_escaped_links_are_ignored(self):
        text = (
            "---\nexample: '[[metadata]]'\n---\n"
            "`[[inline]]` and ``[code](missing.md)``\n\n"
            "```md\n[[fenced]]\n```\n\n"
            "    [[indented]]\n\n"
            "<!-- [[comment]] -->\n"
            "\\[[escaped]]\n\n[[Real]]\n"
        )
        self.assertEqual(list(links(text)), [("Real", True, 15)])

    def test_markdown_table_links(self):
        text = "| Note |\n| --- |\n| [[Missing]] |\n"
        self.assertEqual(list(links(text)), [("Missing", True, 3)])

    def test_resolution(self):
        files = {"area/Note.md", "assets/image.png", "other/A (B).md", "area/v1.0.md"}
        for target in ("Note", "area/Note", "/area/Note.md", "../area/Note", "v1.0"):
            with self.subTest(target=target):
                self.assertTrue(target_exists(target, "area/source.md", files, True))
        self.assertTrue(target_exists("A%20(B).md#Heading", "source.md", files))
        self.assertTrue(target_exists("image.png", "source.md", files, True))
        for target in ("Missing", "note", "wrong/Note", "./Note", "../Note", "/Note"):
            with self.subTest(target=target):
                self.assertFalse(target_exists(target, "source.md", files, True))

    def test_external_and_same_note_links(self):
        for target in ("https://example.org/a", "mailto:a@example.org", "obsidian://open", "#heading"):
            self.assertTrue(target_exists(target, "source.md", set()))
        self.assertTrue(target_exists("page.md?mode=1#heading", "source.md", {"page.md"}))
        self.assertTrue(target_exists("file%23name.md", "source.md", {"file#name.md"}))

    def test_missing_target_and_git_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            (root / ".gitignore").write_text("ignored.md\n")
            (root / "ignored.md").write_text("")
            (root / "target.md").write_text("")
            (root / "source.md").write_text("[[target]] [[missing]] [[ignored]]")
            notes, count, failures = check(root, inventory(root))
            self.assertEqual(len(notes), 2)
            self.assertEqual(count, 3)
            self.assertEqual([item[2] for item in failures], ["missing", "ignored"])
            (root / "target.md").unlink()
            _, _, failures = check(root, inventory(root))
            self.assertEqual([item[2] for item in failures], ["target", "missing", "ignored"])

    def test_exit_code_and_github_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_text("[[missing]]")
            output = io.StringIO()
            with (
                patch("check_links.ROOT", root),
                patch("check_links.inventory", return_value={"source.md"}),
                patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(main(), 1)
                self.assertIn("::error file=source.md,line=1::Missing file: missing", output.getvalue())
                (root / "source.md").write_text("[[#Local heading]]")
                self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
