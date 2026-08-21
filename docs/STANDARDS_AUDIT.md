# Repository standards audit

The repository standards auditor collects evidence. It does not remediate findings and has no authority to change anything it reports.

## Authority boundary

The auditor:

- makes only authenticated HTTP `GET` requests through `gh api`;
- never creates or edits repository files, issues, pull requests, branches, releases, properties, rules, or settings;
- has no remediation, fix, apply, or enforcement mode;
- exits successfully when evidence collection succeeds, even if the report contains `FAIL` findings;
- treats every finding as input to a later, separately reviewed decision.

Only execution and configuration errors produce a non-zero exit status. A report must never be interpreted as authorization for repository changes, visibility changes, lifecycle transitions, tagging, publishing, or releases.

The auditor writes only the two requested report files on the local filesystem. This local output is evidence, not remediation.

## Requirements

- Git Bash or another POSIX-compatible shell
- GitHub CLI authenticated with access to the repositories being audited
- Python 3 using only the standard library

## Usage

From the `.github` repository:

```sh
./scripts/audit-repositories.sh
./scripts/audit-repositories.sh --repo ph-eventing
./scripts/audit-repositories.sh --scope all
./scripts/audit-repositories.sh --output-dir ./audit-output
```

The default scope is the reviewed active cohort in `standards/audit-policy.json`. Explicit `--repo` arguments override the scope. The policy also records grandfathered default branches so historical names are not silently presented as violations.

## Outputs

The selected output directory receives:

- `repository-standards-audit.json` for machine processing;
- `repository-standards-audit.md` for human review.

Each check reports exactly one of:

- `PASS` — the machine-observable requirement is satisfied;
- `FAIL` — machine evidence contradicts a mandatory requirement;
- `WARN` — a noncanonical or incomplete posture needs attention;
- `MANUAL_REVIEW` — intent, provenance, content quality, or another judgment cannot be inferred safely;
- `NOT_APPLICABLE` — the deterministic lifecycle, visibility, or domain profile does not require the check.

A skipped or unobservable condition is never reported as `PASS`.

## Initial limits

The first version checks only facts that can be gathered safely from repository metadata, custom properties, trees, and default-branch protection. It does not claim to prove:

- documentation quality;
- whether a recognized script or Cargo alias actually implements the documented
  canonical gate; a `local_ci` `PASS` therefore asserts only that exactly one
  candidate entry point is present and that it sits at the canonical path named
  in Section 14.1, never that the file is the documented gate, that it is the
  single implementation, or that its outcomes are honest;
- whether a repository with no recognized entry-point file has no canonical gate,
  because a documented command can be a bare tool invocation that leaves no
  distinctive path in the tree; `local_ci` therefore reports `MANUAL_REVIEW`
  rather than `FAIL`, and names each candidate it does observe;
- whether a repository is actually published;
- whether an `AGENTS.md` or code of conduct is warranted;
- workflow pinning, permissions, boundedness, or semantic coverage;
- license provenance or compatibility;
- hardware correctness;
- whether a known exception remains justified.

Those conditions remain explicit manual-review surfaces. Any later expansion must preserve the evidence-only authority boundary.
