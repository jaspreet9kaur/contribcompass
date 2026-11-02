"""Read a bounded set of local community documents, without running a project."""

from dataclasses import asdict, dataclass
from pathlib import Path
import os
import re
import stat

MAX_BYTES = 131072
MAX_ENTRIES = 2048
MAX_TOTAL_BYTES = 2097152
EXTENSIONS = ("", ".md", ".rst", ".txt", ".markdown")


@dataclass(frozen=True)
class Finding:
    id: str
    title: str
    status: str
    evidence: tuple
    action: str
    limitation: str


class Documents:
    def __init__(self, root):
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("Target must be a local directory.")
        self.warnings = set()
        self.cache = {}
        self.bytes_read = 0

    def safe(self, path):
        """Reject links, Windows reparse points and special filesystem objects."""
        current = self.root
        for part in path.relative_to(self.root).parts:
            current = current / part
            try:
                info = current.lstat()
            except FileNotFoundError:
                return False
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                self.warnings.add("A linked document or directory was skipped.")
                return False
            if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):
                self.warnings.add("A special filesystem object was skipped.")
                return False
        return True

    def entries(self, relative):
        if relative in self.cache:
            return self.cache[relative]
        folder = self.root / relative
        found = []
        try:
            if self.safe(folder) and folder.is_dir():
                with os.scandir(folder) as stream:
                    for index, entry in enumerate(stream):
                        if index >= MAX_ENTRIES:
                            self.warnings.add("A directory exceeded the entry limit; discovery is incomplete.")
                            break
                        found.append(entry.name)
        except OSError:
            self.warnings.add("A directory could not be listed; discovery is incomplete.")
        self.cache[relative] = sorted(found, key=lambda value: (value.casefold(), value))
        return self.cache[relative]

    def read(self, relative):
        path = self.root / relative
        try:
            if not self.safe(path) or not path.is_file():
                return None
            before = path.lstat()
            if before.st_nlink != 1 or before.st_size > MAX_BYTES:
                self.warnings.add("A hard-linked or oversized document was skipped.")
                return None
            if self.bytes_read + before.st_size > MAX_TOTAL_BYTES:
                self.warnings.add("The total document byte budget was reached; discovery is incomplete.")
                return None
            with path.open("rb") as stream:
                opened = os.fstat(stream.fileno())
                if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                    self.warnings.add("A document changed during inspection and was skipped.")
                    return None
                raw = stream.read(MAX_BYTES + 1)
                self.bytes_read += len(raw)
            if self.bytes_read > MAX_TOTAL_BYTES:
                self.warnings.add("The total document byte budget was reached; discovery is incomplete.")
                return None
            if len(raw) > MAX_BYTES:
                self.warnings.add("An oversized document was skipped.")
                return None
            return raw.decode("utf-8-sig")
        except (OSError, UnicodeError):
            self.warnings.add("An unreadable or non-UTF-8 document was skipped.")
            return None

    def locate(self, names, folders=("", ".github", "docs")):
        for folder in folders:
            for name in self.entries(folder):
                if name.casefold() in names:
                    relative = (Path(folder) / name).as_posix()
                    text = self.read(relative)
                    if text is not None and text.strip():
                        return relative, text
        return None


def headings(text):
    """Find Markdown ATX/setext headings outside fenced blocks, with line numbers."""
    lines = text.splitlines()
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[marker.end():].strip():
                fence = None
            continue
        if fence is not None:
            continue
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            yield index + 1, match.group(1)
        elif line.strip() and index + 1 < len(lines) and re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[index + 1]):
            yield index + 1, line.strip()


def scan(root):
    docs = Documents(root)
    results = []
    records = {}
    specs = (
        ("readme", "Project overview", ("readme",), "Explain the problem, intended users, and a minimal working example."),
        ("license", "License document", ("license", "copying", "licence"), "Choose a license you have rights to grant and include its full text."),
        ("contributing", "Contribution guide", ("contributing",), "Document local setup, tests, and how changes are reviewed."),
        ("conduct", "Community conduct", ("code_of_conduct", "code-of-conduct"), "Describe community expectations and a real reporting route."),
        ("security", "Security reporting", ("security",), "Provide a private reporting route and supported-version policy."),
    )
    for rule, title, stems, action in specs:
        names = {stem + extension for stem in stems for extension in EXTENSIONS}
        record = docs.locate(names)
        records[rule] = record
        results.append(Finding(rule, title, "present" if record else "missing",
                               (record[0],) if record else (), action,
                               "Nonempty document discovery only; content, legal validity and reporting routes need human review."))

    for rule, title, pattern, action in (
        ("setup", "Setup instructions", r"\b(install\w*|setup|set up|getting started|quick\s*start|development|run locally)\b", "Add a setup section with prerequisites and an example command."),
        ("tests", "Test instructions", r"\b(test\w*|validation|verif\w*)\b", "Explain how to run tests and what a successful run means."),
    ):
        evidence = []
        for key in ("readme", "contributing"):
            record = records[key]
            if record:
                for number, heading in headings(record[1]):
                    if re.search(pattern, heading, re.IGNORECASE):
                        evidence.append(f"{record[0]}:{number}")
        results.append(Finding(rule, title, "present" if evidence else "missing", tuple(evidence), action,
                               "Heading heuristic only. Commands are never executed; other document formats and languages may need manual review."))

    for rule, title, folder, suffixes, action in (
        ("issues", "Issue templates", ".github/ISSUE_TEMPLATE", (".md", ".yml", ".yaml"), "Add a bug template requesting reproducible steps and expected behavior."),
        ("ci", "GitHub Actions workflows", ".github/workflows", (".yml", ".yaml"), "Add appropriate automated checks, or document your existing CI provider."),
    ):
        evidence = []
        for name in docs.entries(folder):
            if name.casefold() == "config.yml" and rule == "issues":
                continue
            if name.casefold().endswith(suffixes):
                relative = (Path(folder) / name).as_posix()
                text = docs.read(relative)
                if text is not None and text.strip():
                    evidence.append(relative)
            if len(evidence) >= 64:
                docs.warnings.add("Evidence was limited to 64 documents per directory.")
                break
        results.append(Finding(rule, title, "present" if evidence else "missing", tuple(evidence), action,
                               "File presence only; templates and workflows are not parsed or executed. Other CI providers are not detected."))

    # A skipped document can conceal evidence: never treat incomplete discovery as absence.
    if docs.warnings:
        results = [Finding(item.id, item.title, "unknown" if item.status == "missing" else item.status,
                           item.evidence, item.action, item.limitation) for item in results]
    return {
        "schema_version": 1,
        "tool": "ContribCompass",
        "findings": [asdict(item) for item in results],
        "summary": {status: sum(item.status == status for item in results) for status in ("present", "missing", "unknown")},
        "warnings": sorted(docs.warnings),
        "limits": {"bytes_per_document": MAX_BYTES, "total_document_bytes": MAX_TOTAL_BYTES, "entries_per_directory": MAX_ENTRIES, "evidence_per_directory": 64},
        "limitations": [
            "Local onboarding evidence only; not a security audit or license compliance review.",
            "Only root, .github, docs, issue templates and GitHub workflow locations are considered; no recursive code scan.",
            "No GitHub organization-level community defaults, external documentation, Git history or adoption metrics are checked.",
            "Use a stable local snapshot. This reader is not a sandbox for a concurrently hostile filesystem.",
        ],
    }
