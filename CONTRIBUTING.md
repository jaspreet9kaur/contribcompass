# Contributing

ContribCompass helps people navigate contributor documentation. We value precise evidence, small changes and explanations of limitations.

## Setup

Use Python 3.11+ and work from this source checkout. No dependency installation is required. Run `python -B -m contribcompass .` for a self-report. Do not run commands from an unfamiliar repository merely to scan its documentation.

## Tests

Run `python -B -m unittest discover -s tests -v`. Tests create fictional documents in a temporary directory. Link tests may be skipped on hosts that cannot create links; skipped tests are not passed coverage. Use a disposable, private scratch directory for temporary files when appropriate to your environment.

## Propose a change

1. Describe a real contributor problem and the smallest example showing it.
2. Open a discussion or issue in the eventual project repository, without confidential paths or document contents. Local users can prepare an issue description before publication.
3. Keep the implementation focused. Add a regression test for changed behavior.
4. Run tests and the self-report. Explain false positives, unsupported formats and any skipped checks in the pull request.

No automatic issue creation, pull-request generation, network calls, downloaded rulesets, or execution of target code belong in this initial version. A feature changing those boundaries needs a design discussion first.

## Good first investigations

- A setup instruction written in a language other than English is missed by heading heuristics.
- Documentation lives in a monorepo package rather than the supported root locations.
- A repository uses a CI provider other than GitHub Actions.

These are known limitations and investigation ideas, not claims of external demand or assigned tasks. Confirm the desired behavior before implementing broad detection.

## Reviews and attribution

Explain what you wrote and attribute any reused material. Keep upstream licenses and notices when applicable. Do not import another project's code or history and present it as your own work. Maintainers review changes for usefulness and correctness, rather than rewarding contribution volume.
