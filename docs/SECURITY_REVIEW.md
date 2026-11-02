# Application baseline review

Scope: local ContribCompass prototype, 2026-11-03. This is the user's baseline release review, not a comprehensive security audit, penetration test or production-security certification. No prior audit ledger is claimed.

## Architecture and boundaries

The user selects a local directory. The Python standard library reads only supported community-document locations and emits a report to stdout. The tool imports its own modules, never the target's modules; it does not load target configuration, execute commands, install packages or access the network. Reports contain relative filenames and check metadata, not document snippets. Target documentation and names are untrusted. The filesystem must be a stable snapshot; the process is not an isolation boundary against a concurrent malicious local writer.

## Checklist coverage

| Category | Status and evidence |
| --- | --- |
| Injection, SQL and command injection | Source-reviewed: no database, subprocess, shell invocation, eval, external rules or target imports in scanner/CLI. Functional regression checks verify a fixture setup.py is not executed. No adversarial sandbox execution claim. |
| XSS and output escaping | Source-reviewed and functional tests: Markdown escapes filename markup, text removes controls and bidi-format controls, JSON uses JSON escaping. No HTML renderer. Downstream consumers must escape JSON strings for their own context. |
| CSRF | Not applicable: no HTTP server, sessions or mutations. |
| Uploads, sizes, decoded data and storage | No upload endpoint. Local reads are bounded; skips and incomplete coverage are reported. Oversized and invalid-UTF-8 cases have functional tests. No archive extraction or report-file writer exists. |
| SSRF | Not applicable: scanner accepts local paths and makes no HTTP requests. On platforms supporting network filesystem paths, users must select a local snapshot; the tool does not provide a filesystem network-isolation sandbox. |
| Authentication, sessions and object authorization/IDOR | Not applicable: single-user local CLI with the invoking user's OS permissions, no multi-user service or object API. |
| Rate limiting | No service API. Local document bytes, directory entries and evidence counts are bounded and covered by functional tests; this is not an availability guarantee against a hostile filesystem. |
| Password storage and MFA | Not applicable: no accounts or password handling. |
| Server permissions and row/tenant isolation | Not applicable: no server, database or tenancy. Run with ordinary user privileges; the CLI does not elevate privileges. |
| Secrets, JWT and browser storage | Source-reviewed: no tokens, credential input, browser storage or JWT. Tests verify report output omits document contents and absolute target paths. Relative names may still reveal private project details; review before sharing. |
| Default credentials | Not applicable: none supplied or required. |
| CORS and webhook signatures/replay | Not applicable: no HTTP or webhook surfaces. |
| Source maps and sensitive UI/log/export data | No browser bundle or source maps. Source is deliberately public. Terminal/Markdown controls are escaped. CLI target errors avoid dumping local paths. No telemetry or logging. |
| Vulnerable dependencies | No third-party Python runtime packages. This is not a clean advisory scan: Python/OS advisories were not scanned. GitHub Actions are third-party development dependencies; commit refs were resolved from official APIs and pinned, with Dependabot configuration. Their current advisories and hosted runner images are not validated here. |
| Filesystem links and races | Source-reviewed: links, Windows reparse points and hard links are rejected; file identity compared before read. Link tests may skip depending on host capabilities; see VALIDATION.md. Not race-proof against concurrent ancestor replacement or special platform filesystem behavior. |

## Launch requirements and unvalidated checks

- Configure and verify private vulnerability and conduct reporting on the intended GitHub repository.
- Run the hosted CI matrix after publication; runner permissions and execution results are not established by the YAML file's presence.
- Perform a current advisory review of the chosen Python runtime and GitHub Actions before declaring a public supported release.
- No live probing or full security exploit validation was performed. Functional tests of agent-authored code and fictional fixtures do not establish an OS-enforced hostile-code sandbox. A future adversarial audit needs isolated execution with network, filesystem, resource and environment controls.
- Any future remote retrieval, user accounts, credential handling, automatic remediation or hosted service requires a new boundary review.
