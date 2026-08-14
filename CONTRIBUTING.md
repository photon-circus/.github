# Contributing to Photon Circus repositories

This file is an organization-wide fallback. GitHub may display it for a Photon
Circus repository that does not commit its own `CONTRIBUTING.md`. It does not
replace repository-specific guidance or satisfy a requirement for a local
contribution guide.

## Follow the target repository first

Instructions committed in the repository you are changing control over this
fallback. Before starting, read its README and any local `CONTRIBUTING.md`,
`AGENTS.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, pull-request template, and
linked contract or architecture documentation. Use the repository's issue and
proposal process when it defines one.

Local files may require additional documentation, evidence, review, or release
steps. Within each subject, a repository-local file controls over this fallback:
`SECURITY.md` owns vulnerability reporting, `CODE_OF_CONDUCT.md` owns conduct,
`CONTRIBUTING.md` owns contribution workflow, and `AGENTS.md` adds agent-specific
implementation constraints. None silently overrides adopted organization
standards or another subject's canonical owner. Ask a maintainer before acting
on instructions that remain inconsistent.

If the target is the
[`photon-circus/.github`](https://github.com/photon-circus/.github)
standards repository, also follow its
[standards-specific contribution guide](https://github.com/photon-circus/.github/blob/main/docs/CONTRIBUTING_TO_STANDARDS.md).

## Keep the change bounded

- State the problem, intended user, and repository responsibility the change
  strengthens.
- Keep the pull request independently reviewable and name what remains outside
  its scope.
- Preserve the repository's declared non-goals and avoid incidental renames,
  migrations, releases, or lifecycle changes.
- Call out compatibility, supported-target, feature, timing, memory, ownership,
  or failure-semantics effects when they apply.

## Identify the evidence

Explain what supports each important claim. Distinguish evidence obtained from:

- Physical hardware, including device, board, and silicon revisions.
- An independent behavioral model or simulation.
- A mock, stub, scripted transport, or test double.
- Source documents, code reading, or engineering inference.

Do not turn model, mock, or code-reading evidence into an unstated physical
hardware claim. Include the relevant package version or commit, toolchain,
target, features, and test environment when they affect reproducibility.

Run the relevant focused tests and the repository's canonical verification gate
when one is documented, normally `scripts/ci.sh` in technical repositories.
Report the exact commands and results. A skipped or unavailable check is not a
passing check; record the limitation and any remaining risk.

## Keep contracts and history aligned

Update the maintained documentation that the target repository says changes
together. Depending on the change, that can include its README, API or hardware
contract, architecture, invariants, test plan, support matrix, release notes,
and agent guidance. Add a concise entry under `Unreleased` when the local
changelog policy requires one.

The target repository's files determine which documents are required. This
organization fallback does not create a substitute document set and does not
override local ownership or release rules.

## Open the pull request

Use the target repository's pull-request template. At minimum, describe:

- Purpose, bounded scope, and explicit non-goals.
- Contract and compatibility effects, or that there is no contract change.
- Evidence sources, commands, results, and environment.
- Documentation and changelog updates.
- Known limitations, remaining risks, and follow-up work.

## Conduct and security

Follow the target repository's `CODE_OF_CONDUCT.md` when it has one. Otherwise,
participate professionally, critique work rather than people, and avoid
publishing sensitive personal information. Raise conduct concerns through any
private route named by the target repository or privately with its maintainers.

Follow the target repository's local security policy. If it has none, use the
[organization security fallback](https://github.com/photon-circus/.github/blob/main/SECURITY.md).
Never put vulnerability details, credentials, private repository content,
confidential vendor material, or hardware secrets in a public issue or pull
request.
