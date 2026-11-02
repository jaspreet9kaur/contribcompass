import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from contribcompass.cli import main, render
from contribcompass.scanner import MAX_BYTES, headings, scan


class ScannerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def findings(self):
        return {item["id"]: item for item in scan(self.root)["findings"]}

    def test_empty_project_has_actionable_gaps_not_a_quality_score(self):
        report = scan(self.root)
        self.assertEqual(report["summary"], {"present": 0, "missing": 9, "unknown": 0})
        self.assertTrue(all(item["action"] and item["limitation"] for item in report["findings"]))
        self.assertNotIn("score", report)

    def test_common_locations_case_and_exact_evidence_lines(self):
        self.write("ReadMe.md", "# Demo\n\n## Getting started\nRun it.\n\nTests\n-----\nRun tests.\n")
        self.write("docs/CONTRIBUTING.md", "# Contributing\nDiscuss changes first.")
        self.write("LICENSE", "Example text, not a verified license.")
        result = self.findings()
        self.assertEqual(result["setup"]["evidence"], ("ReadMe.md:3",))
        self.assertEqual(result["tests"]["evidence"], ("ReadMe.md:6",))
        self.assertEqual(result["contributing"]["evidence"], ("docs/CONTRIBUTING.md",))
        self.assertEqual(result["license"]["status"], "present")
        self.assertIn("legal validity", result["license"]["limitation"])

    def test_fenced_examples_do_not_count_as_setup_or_test_instructions(self):
        self.write("README.md", "# Demo\n```md\n## Installation\n## Tests\n```\n~~~\nSetup\n=====\n~~~\n")
        result = self.findings()
        self.assertEqual(result["setup"]["status"], "missing")
        self.assertEqual(result["tests"]["status"], "missing")
        self.assertEqual(list(headings("````\n```\n## Tests\n````\n## Usage\n")), [(5, "Usage")])

    def test_ci_and_templates_are_presence_only_and_config_is_not_a_template(self):
        self.write(".github/ISSUE_TEMPLATE/config.yml", "blank_issues_enabled: false")
        self.write(".github/workflows/test.yml", "not valid yaml but nonempty")
        result = self.findings()
        self.assertEqual(result["issues"]["status"], "missing")
        self.assertEqual(result["ci"]["status"], "present")
        self.assertIn("not parsed", result["ci"]["limitation"])
        self.write(".github/ISSUE_TEMPLATE/bug.md", "# Bug report")
        self.assertEqual(self.findings()["issues"]["status"], "present")

    def test_empty_documents_do_not_count(self):
        self.write("README.md", " \n\t")
        self.assertEqual(self.findings()["readme"]["status"], "missing")

    def test_oversized_and_invalid_utf8_documents_make_absence_unknown(self):
        self.write("README.md", "X" * (MAX_BYTES + 1))
        report = scan(self.root)
        self.assertEqual(report["summary"]["unknown"], 9)
        self.assertTrue(report["warnings"])
        (self.root / "README.md").write_bytes(b"\xff\xfe")
        self.assertEqual(self.findings()["readme"]["status"], "unknown")

    def test_symlink_does_not_disclose_external_document(self):
        outside = self.root / "outside.txt"
        outside.write_text("# Installation\nprivate fixture", encoding="utf-8")
        try:
            (self.root / "README.md").symlink_to(outside)
        except OSError:
            self.skipTest("Host does not permit symlink creation")
        result = scan(self.root)
        self.assertEqual(result["summary"]["unknown"], 9)
        self.assertNotIn("private fixture", json.dumps(result))

    def test_hardlinks_are_skipped(self):
        self.write("source.txt", "# Tests\nfixture")
        try:
            os.link(self.root / "source.txt", self.root / "README.md")
        except OSError:
            self.skipTest("Host does not support hardlinks")
        self.assertEqual(self.findings()["readme"]["status"], "unknown")

    def test_discovery_limits_are_reported(self):
        self.write("README.md", "# Project")
        with patch("contribcompass.scanner.MAX_ENTRIES", 0):
            self.assertTrue(scan(self.root)["warnings"])
        with patch("contribcompass.scanner.MAX_TOTAL_BYTES", 1):
            self.assertEqual(self.findings()["readme"]["status"], "unknown")

    def test_report_does_not_include_contents_or_absolute_paths(self):
        self.write("README.md", "# Project\nfictional-secret-do-not-export")
        report = scan(self.root)
        for format in ("text", "markdown", "json"):
            output = render(report, format)
            self.assertNotIn("fictional-secret-do-not-export", output)
            self.assertNotIn(str(self.root), output)

    def test_report_escapes_untrusted_filenames_and_terminal_controls(self):
        report = scan(self.root)
        report["findings"][0]["evidence"] = ("<img>\x1b[31m\n|x.md",)
        self.assertNotIn("\x1b", render(report, "text"))
        self.assertNotIn("<img>", render(report, "markdown"))
        self.assertIn("\\<img\\>", render(report, "markdown"))
        self.assertEqual(json.loads(render(report, "json"))["schema_version"], 1)

    def test_target_scripts_are_never_imported_and_target_is_unchanged(self):
        self.write("setup.py", "raise RuntimeError('must never run')")
        self.write("README.md", "# Project")
        before = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        scan(self.root)
        after = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_cli_json_strict_and_invalid_target_exit_codes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main([str(self.root), "--format", "json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["summary"]["missing"], 9)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main([str(self.root), "--strict"]), 1)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main([str(self.root / "absent")]), 2)


if __name__ == "__main__":
    unittest.main()
