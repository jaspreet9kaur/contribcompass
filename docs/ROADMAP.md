# Roadmap and launch gates

## Current state

A source-run prototype exists, and the public repository is [jaspreet9kaur/contribcompass](https://github.com/jaspreet9kaur/contribcompass). The Windows/Linux and Python 3.11/3.14 CI matrix passed, and private vulnerability reporting is enabled. Functional tests and a self-report can be reproduced. No hosted service, registry package, external pilot, downloads, or active community is claimed.

## First public pilot

1. Review the source and provisional project name. Check naming conflicts before a public release.
2. Completed: connected jaspreet9kaur, created the public repository, and published the MIT-licensed source with its prototype status.
3. Private vulnerability reporting is enabled; verify notification delivery and add a private conduct-reporting contact. Do not treat the presence of SECURITY.md as completion.
4. Completed for the initial implementation commit: the Windows/Linux and Python-version CI matrix passed. See VALIDATION.md for the exact source ref and log coverage.
5. Invite a small number of willing developers to test the tool. Obtain permission before retaining identifiable feedback or contacting maintainers. No unsolicited automated messages, issues or PRs.

## Evaluation before expanding scope

Use at least five voluntary onboarding sessions across different repository layouts, including a monorepo and a project with external documentation. Record actual evidence:

| Question | Record |
| --- | --- |
| Did the guide help locate setup and test instructions? | Task outcome and participant's explanation |
| Was evidence incorrect or missing? | Minimal public/fictional fixture and expected result |
| Did the maintainer act on a recommendation? | Accepted change link, if any |
| Would the participant use it again? | Voluntary answer and reasons |

Do not report sessions as completed until they occur. Publish aggregated, deidentified findings with consent. If the tool adds no value beyond existing tools, narrow or change the problem rather than growing the checklist.

## Candidate later work

- Selectable monorepo scope with explicit path boundaries.
- Multilingual heading rules backed by examples and false-positive tests.
- RST-aware section parsing and support for CI providers beyond GitHub Actions.
- Opt-in repository-level configuration that remains data-only.
- Packaging only after name, maintenance burden and distribution needs are established.

These are proposals, not implemented features. There is no automatic-fix or autonomous-PR feature in this version.

## Contribution and adoption evidence

Maintain a factual release history, accepted external PR links, distinct contributors with merged work, downstream dependents, and registry downloads if distribution is added. Use official registry/API measurements and state the observation window. Never estimate users from stars or inflate activity with trivial PRs, bots or duplicate submissions.

Contributing useful fixes to established projects is a separate route to developing an open-source record. Each contribution should solve a maintainer-recognized problem and follow that project's process. Creating or improving this project alone does not guarantee any sponsorship threshold or approval. Recheck Anthropic's then-current rules before applying.
