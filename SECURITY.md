# Security reporting

## Supported versions

0.1.0 is an unreleased prototype. There is no supported production release or security-response SLA yet.

## Report privately

Use [GitHub private vulnerability reporting](https://github.com/jaspreet9kaur/contribcompass/security/advisories/new). The repository setting was enabled and verified on 2026-11-03. Actual notification delivery and maintainer response times have not been tested. Do not put exploit details, private documents, credentials, or personal information into public issues. No security email address or response SLA is claimed.

For a report, describe the affected version, input boundary, expected behavior, observed result and a minimal fictional fixture. Do not test against systems or data you do not own.

## Scope

The scanner reads local community documentation. It performs no network calls, dependency installation, subprocess execution, target imports, credential collection, or automated remediation. Use stable, trusted snapshots rather than hostile concurrently modified directories. Reading arbitrary local files is not a security sandbox. See [the baseline review](docs/SECURITY_REVIEW.md) for evidence and unresolved deployment checks.
