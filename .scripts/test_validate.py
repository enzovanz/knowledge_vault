import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from validate import ROOT, main, run_checks, use_color


class ValidationRunnerTests(unittest.TestCase):
    def test_runs_all_checks_after_a_failure_and_colors_results(self):
        results = [
            subprocess.CompletedProcess([], 1, "missing note\n::error file=Note.md::Missing\n"),
            subprocess.CompletedProcess([], 0, "valid properties\n"),
            subprocess.CompletedProcess([], 0, "covered notes\n"),
            subprocess.CompletedProcess([], 0, "unique titles\n"),
        ]
        output = io.StringIO()
        with patch("validate.subprocess.run", side_effect=results) as run:
            with contextlib.redirect_stdout(output):
                self.assertEqual(run_checks(True), 1)
        self.assertEqual(run.call_count, 4)
        for call in run.call_args_list:
            self.assertEqual(call.args[0][0], sys.executable)
            self.assertEqual(call.kwargs["cwd"], ROOT)
        text = output.getvalue()
        self.assertIn("\033[31m[FAIL] Internal links\033[0m", text)
        self.assertIn("\033[32m[PASS] Note properties\033[0m", text)
        self.assertIn("\n::error file=Note.md::Missing\n", text)
        self.assertIn("3/4 checks passed; 1 failed.", text)

    def test_success_without_color(self):
        result = subprocess.CompletedProcess([], 0, "OK\n")
        output = io.StringIO()
        with patch("validate.subprocess.run", return_value=result):
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(["--color", "never"]), 0)
        self.assertIn("4/4 checks passed; 0 failed.", output.getvalue())
        self.assertNotIn("\033", output.getvalue())

    def test_start_error_is_reported_and_other_checks_continue(self):
        success = subprocess.CompletedProcess([], 0, "")
        output = io.StringIO()
        with patch("validate.subprocess.run", side_effect=[OSError("unavailable")] + [success] * 3):
            with contextlib.redirect_stdout(output):
                self.assertEqual(run_checks(False), 1)
        self.assertIn("Could not start check: unavailable", output.getvalue())
        self.assertIn("[PASS] Unique note titles", output.getvalue())

    def test_terminal_ci_and_no_color_preferences(self):
        with patch.dict("os.environ", {}, clear=True):
            with patch("validate.sys.stdout.isatty", return_value=True):
                self.assertTrue(use_color("auto"))
            with patch("validate.sys.stdout.isatty", return_value=False):
                self.assertFalse(use_color("auto"))
                with patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}):
                    self.assertTrue(use_color("auto"))
            with patch.dict("os.environ", {"NO_COLOR": "1", "GITHUB_ACTIONS": "true"}):
                self.assertFalse(use_color("auto"))
                self.assertTrue(use_color("always"))
                self.assertFalse(use_color("never"))

    def test_real_child_failure_stderr_and_subsequent_success(self):
        with tempfile.TemporaryDirectory() as directory:
            scripts = Path(directory)
            (scripts / "bad.py").write_text(
                "import sys\nprint('diagnostic', file=sys.stderr)\nsys.exit(2)\n",
                encoding="utf-8",
            )
            (scripts / "good.py").write_text("print('still ran')\n", encoding="utf-8")
            output = io.StringIO()
            with (
                patch("validate.SCRIPTS", scripts),
                patch("validate.CHECKS", (("Bad", "bad.py"), ("Good", "good.py"))),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(run_checks(False), 1)
            self.assertIn("diagnostic", output.getvalue())
            self.assertIn("still ran", output.getvalue())
            self.assertIn("1/2 checks passed; 1 failed.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
