# Source research and design decisions

Research date: 2026-11-03. This is a bounded source review, not an exhaustive market study or a claim that this project is unique.

## REA routing

The user requested the installed reverse-engineer-anything skill. Its guidance routes complete source repositories to normal source tools and reserves REA analysis for artifacts or runtime questions that source does not answer. We followed that source route. No binary was decompiled, no REA engine was run, and no unobserved runtime behavior is claimed.

## References inspected

1. [TODO Group Repolinter README](https://github.com/todogroup/repolinter/blob/master/README.md) and [entry point](https://github.com/todogroup/repolinter/blob/master/index.js). Observed: the README says the project is archived. It describes configurable rules, multiple report formats, remote cloning and optional fixes. The entry point separates filesystem access, rules, fixes, axioms and output formatting. Design inference: an onboarding-specific tool can keep a much smaller boundary by avoiding remote acquisition, loaded rules and modifications. This is a product choice, not a demonstrated defect in Repolinter. Upstream license: Apache-2.0, as stated in its README. No upstream code or assets were copied.
2. [OpenSSF Scorecard architecture](https://github.com/ossf/scorecard/blob/main/ARCHITECTURE.md). Observed: collection, probes, evaluation and reporting are separated; checks can use repository-host data and auxiliary services without building the target. Design inference: show evidence separately from interpretation and make uncertainty visible. ContribCompass does not implement Scorecard checks, its scoring system, or its security claims. No upstream code or assets were copied.

The references were read through the connected GitHub service. This initial research is not pinned to a retained upstream commit, so future comparisons must resolve an exact revision before making change-over-time claims.

## Why this first version

The audience hypothesis is that maintainers and first-time contributors benefit from a short offline reading guide and explicit documentation gaps. A source-run, standard-library CLI is inexpensive to try and does not need paid Claude access to function. Unlike a repository-wide policy engine, it has nine fixed evidence checks. This is an unvalidated hypothesis; pilot feedback must determine whether further development is worthwhile.

The project does not inherit upstream stars, dependents, contributors, downloads or reputation. Adding files or passing the self-check does not establish ecosystem impact or sponsorship eligibility.
