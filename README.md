# ContribCompass

Find the documentation a first-time contributor needs, and identify what is missing.

ContribCompass is a small, offline Python tool for maintainers and contributors. It reads a bounded set of local community documents, returns file and line references, and suggests the next documentation improvements. It never imports the inspected project's code, runs its commands, clones repositories, or calls a paid service.

**Status: initial local prototype, version 0.1.0.** No users, downloads, external contributors, sponsorship eligibility, or security certification are claimed. The name is provisional; registry and trademark availability have not been established.

## Quick start

Requires Python 3.11 or newer. Get the source:

```sh
git clone https://github.com/jaspreet9kaur/contribcompass.git
cd contribcompass
```

From this source checkout, no installation or third-party Python packages are needed:

```sh
python -B -m contribcompass /path/to/project
python -B -m contribcompass /path/to/project --format json
python -B -m contribcompass /path/to/project --format markdown
```

On Windows, a target can be a quoted path such as `"D:\\Projects\\example"`. Invoke the tool from this checkout; the target may be a separate local project. No Git repository metadata is required.

To save a report, redirect stdout using your shell. Review the report before publishing it: relative document names can still be private.

```sh
python -B -m contribcompass /path/to/project --format markdown > onboarding-report.md
```

## What you get

- Evidence for README, license, contribution guide, conduct policy, and security reporting documents.
- Setup and test section references, with source line numbers.
- Issue-template and GitHub Actions workflow discovery.
- A suggested document reading order and concrete next steps for missing evidence.
- Stable JSON schema version 1 and optional strict exit codes for CI.

Every finding is `present`, `missing`, or `unknown`. These are observations about supported local locations, not quality scores. A license file is not proof of a valid open-source license; a security policy is not proof of a secure project. See [checks and limits](docs/CHECKS.md).

## Example

For a directory containing `README.md` with an Installation heading on line 3:

```text
PRESENT: Project overview — README.md
PRESENT: Setup instructions — README.md:3
MISSING: Contribution guide — No evidence found in supported locations
  Next: Document local setup, tests, and how changes are reviewed.
```

This is an illustrative excerpt, not an adoption claim. Reports include per-check limitations.

## Tests

Run the standard-library tests from this checkout:

```sh
python -B -m unittest discover -s tests -v
python -B -m contribcompass . --strict
```

Exit codes: `0` means a report was produced; `1` means `--strict` found missing or unknown evidence; `2` means an invocation or target error. Without `--strict`, gaps do not fail the command.

## Privacy and trust boundary

The tool makes no network requests, asks for no credentials, and prints no document contents or absolute target paths. It only reads named community-document locations; it does not recursively scan source or inspect `.git`. Text and Markdown reports sanitize control characters, and Markdown escapes untrusted filenames. JSON preserves filename data through JSON escaping.

Symbolic links, Windows reparse points, hard-linked documents, special files, oversized documents, and invalid UTF-8 are skipped. File identity is compared before reading. Use a stable snapshot that another process cannot modify while scanning: this is not race-proof isolation from a hostile local writer. Reports written through shell redirection can overwrite the destination; choose the filename yourself.

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). Useful work includes evaluating real onboarding journeys, documenting false positives, and adding tests for document layouts. Discuss scope before a large implementation. Improvements should help a contributor, not merely increase a check count.

## Relationship to existing tools

[Repolinter](https://github.com/todogroup/repolinter) and [OpenSSF Scorecard](https://github.com/ossf/scorecard) informed the research. This is an independent implementation, not a fork, affiliated project, security scanner, or replacement for either tool. Their usage, stars, and impact do not belong to this project. See [research](docs/RESEARCH.md) and [roadmap](docs/ROADMAP.md).

## License

MIT. See [LICENSE](LICENSE).
