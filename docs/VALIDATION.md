# Local validation

Recorded 2026-11-03 against the initial local prototype.

## Executed

`python -B -m unittest discover -s tests -v`

Result: 13 tests discovered, 11 passed, 2 skipped. The host could not create the symbolic and hard links required by those two tests. Their intended protections are source-reviewed, not demonstrated by this run.

The executed tests cover document discovery, exact heading line references, ignoring fenced examples, actionable gaps, presence-only semantics, empty and invalid documents, byte/discovery limits, output escaping, omission of contents and absolute target paths, no target-script execution, unchanged target files, JSON parsing and CLI exit codes. They use fictional fixtures, not external project code.

`python -B -m contribcompass . --strict`

Result: exit 0, nine present evidence categories and no discovery warnings. This is a documentation-presence self-check, not a claim of community readiness, reporting-channel configuration, code quality, adoption, security certification or sponsorship eligibility.

Temporary fixtures for the final run were directed to a task-local D: scratch directory. No dependency installation or paid service was required.

## GitHub Actions verification

[Checks run 41513378410](https://github.com/jaspreet9kaur/contribcompass/actions/runs/41513378410) passed for source commit `dd8bf9d6b39994fe452d6a315c3fe7cc7c88cb4f` on 2026-11-03 (Asia/Calcutta).

All four jobs succeeded: ubuntu-latest and windows-latest, each on Python 3.11 and 3.14. The Python 3.14 job logs on both operating systems explicitly show all 13 tests ran, including successful hard-link and symbolic-link cases. The 3.11 job statuses and test steps were verified successful; their detailed skip counts were not separately inspected. The workflow also ran the strict documentation self-check in all four jobs.

Private vulnerability reporting was enabled in the repository UI and its enabled state verified. No test report was submitted, and notification delivery remains untested.

## Not executed or established

- Current advisory scans for Python, runner images and GitHub Actions.
- A full adversarial audit or race-proof filesystem isolation.
- External usability sessions, maintainer adoption or package downloads.
- Private-report notification delivery and a private conduct-reporting contact.

See SECURITY_REVIEW.md and ROADMAP.md for the remaining launch work.
