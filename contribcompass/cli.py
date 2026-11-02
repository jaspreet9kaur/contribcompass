"""Command-line and report formatting; output is written only to stdout."""

import argparse
import json
import re
import sys

from . import __version__
from .scanner import scan


def clean(value):
    return re.sub(r"[\x00-\x1f\x7f-\x9f\ud800-\udfff\u202a-\u202e\u2066-\u2069]", "?", str(value))


def markdown(value):
    return re.sub(r"([\\`*_{}\[\]<>()#!|])", r"\\\1", clean(value))


def render(report, format):
    if format == "json":
        return json.dumps(report, indent=2, ensure_ascii=True)
    escape = markdown if format == "markdown" else clean
    lines = ["# ContribCompass" if format == "markdown" else "ContribCompass", "",
             "Local contributor onboarding evidence. Presence does not verify documentation quality.", ""]
    for finding in report["findings"]:
        evidence = ", ".join(escape(value) for value in finding["evidence"]) or "No evidence found in supported locations"
        lines.append(f"- {finding['status'].upper()}: {finding['title']} - {evidence}")
        if finding["status"] != "present":
            lines.append("  Next: " + finding["action"])
        lines.append("  Limit: " + finding["limitation"])
    lines.extend(["", "Reading order:"])
    for rule in ("readme", "contributing", "conduct", "security", "license"):
        finding = next(item for item in report["findings"] if item["id"] == rule)
        for evidence in finding["evidence"]:
            lines.append("- " + escape(evidence))
    lines.extend(["", "Limitations:"])
    lines.extend("- " + item for item in report["limitations"])
    lines.extend("- " + item for item in report["warnings"])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect local contributor onboarding documents without executing project code.")
    parser.add_argument("path", nargs="?", default=".", help="Local project directory (default: current directory)")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if evidence is missing or unknown; normal reports exit 0")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)
    try:
        report = scan(args.path)
    except (OSError, ValueError, RuntimeError):
        print("Could not inspect the target. Supply an accessible, stable local directory.", file=sys.stderr)
        return 2
    print(render(report, args.format))
    return 1 if args.strict and (report["summary"]["missing"] or report["summary"]["unknown"]) else 0
