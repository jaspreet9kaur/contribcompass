# Security reporting

## Supported versions

0.1.0 is an unreleased prototype. There is no supported production release or security-response SLA yet.

## Report privately

Before public launch, the repository owner must enable GitHub private vulnerability reporting under repository Settings > Security, and verify a report can be received. That channel is not configured in this local source bundle. Do not put exploit details, private documents, credentials, or personal information into public issues. No monitored security email address is claimed.

For a report, describe the affected version, input boundary, expected behavior, observed result and a minimal fictional fixture. Do not test against systems or data you do not own.

## Scope

The scanner reads local community documentation. It performs no network calls, dependency installation, subprocess execution, target imports, credential collection, or automated remediation. Use stable, trusted snapshots rather than hostile concurrently modified directories. Reading arbitrary local files is not a security sandbox. See [the baseline review](docs/SECURITY_REVIEW.md) for evidence and unresolved deployment checks.
