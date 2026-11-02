# Local validation

Recorded 2026-11-03 against the initial local prototype.

## Executed

`python -B -m unittest discover -s tests -v`

Result: 13 tests discovered, 11 passed, 2 skipped. The host could not create the symbolic and hard links required by those two tests. Their intended protections are source-reviewed, not demonstrated by this run.

The executed tests cover document discovery, exact heading line references, ignoring fenced examples, actionable gaps, presence-only semantics, empty and invalid documents, byte/discovery limits, output escaping, omission of contents and absolute target paths, no target-script execution, unchanged target files, JSON parsing and CLI exit codes. They use fictional fixtures, not external project code.

`python -B -m contribcompass . --strict`

Result: exit 0, nine present evidence categories and no discovery warnings. This is a documentation-presence self-check, not a claim of community readiness, reporting-channel configuration, code quality, adoption, security certification or sponsorship eligibility.

Temporary fixtures for the final run were directed to a task-local D: scratch directory. No dependency installation or paid service was required.

## Not executed or established

- Hosted Windows/Linux and Python 3.11/3.14 CI matrix.
- Link rejection on a host permitting the relevant link fixtures.
- Current advisory scans for Python, runner images and GitHub Actions.
- A full adversarial audit or race-proof filesystem isolation.
- External usability sessions, maintainer adoption or package downloads.
- GitHub private vulnerability reporting and conduct-reporting setup.

See SECURITY_REVIEW.md and ROADMAP.md for the remaining launch work.
