# Checks and limits

All checks inspect local evidence only. None establishes that a project is secure, legally compliant, widely used, or eligible for sponsorship.

| ID | Evidence | Important limitation |
| --- | --- | --- |
| readme | Nonempty README in root, .github or docs | Does not assess accuracy or usefulness |
| license | Nonempty LICENSE, LICENCE or COPYING | Does not identify an OSI-approved license or verify rights |
| contributing | Nonempty CONTRIBUTING | Does not verify commands or review practices |
| conduct | CODE_OF_CONDUCT or CODE-OF-CONDUCT | Reporting contact may be missing or unmonitored |
| security | Nonempty SECURITY | Does not verify a private reporting channel |
| setup | Setup-related heading in discovered README or CONTRIBUTING | English Markdown heading heuristic only |
| tests | Test-related heading in discovered README or CONTRIBUTING | Never executes commands; no test-pass claim |
| issues | Nonempty .md/.yml/.yaml in .github/ISSUE_TEMPLATE | config.yml alone does not count; schema validity not checked |
| ci | Nonempty .yml/.yaml in .github/workflows | Not a YAML parser; other providers and remote CI state unobserved |

Document matching is case-insensitive with no extension or .md/.rst/.txt/.markdown. Discovery prioritizes root, then .github, then docs; when multiple documents match, the first nonempty readable match is used. Linked, special, hard-linked, oversized and invalid-UTF-8 documents are skipped. Missing supported evidence becomes `unknown` if any discovery warning occurs; this conservative behavior avoids presenting incomplete discovery as definite absence. A `present` check can have partial evidence when warnings exist.

Bounds: 128 KiB per document, 2 MiB total document reads, 2,048 entries listed per directory and 64 workflow/template evidence paths per check. The byte budget includes repeated reads. If a directory exceeds its cap, the inspected subset can depend on filesystem enumeration order; the warning reports that discovery is incomplete. Output ordering is stable for the observed subset.

Use a stable snapshot. Filesystem identity checks reduce accidental replacement reads but do not provide atomic isolation against a hostile concurrent writer, directory replacement or all platform-specific race conditions. No recursion, source execution or repository configuration loading occurs.

## JSON contract

`schema_version` is 1. `findings` contains objects with `id`, `title`, `status`, `evidence`, `action`, `limitation`. Status is one of `present`, `missing`, `unknown`. Evidence is an array of relative paths, optionally followed by `:line`. Lines are one-based. `summary` counts each status. `warnings`, `limits` and `limitations` describe incomplete coverage.

Consumers should select by rule ID, accept additional fields, and reject unsupported schema versions. JSON escapes controls but preserves the underlying filename data; downstream terminal or HTML consumers must escape it for their own output context. Text and Markdown reports are intended for human review, not machine parsing.
