# Rust xtask field guide for peripheral-driver repositories

Status: **Explicitly non-normative field notes**

Evidence snapshot: **2026-08-20 UTC**

## Purpose and boundary

This guide records experience from replacing shell-based local verification in
three Rust peripheral-driver repositories with repository-local `xtask` crates.
It supplements the technology-neutral
[canonical local CI standard](../REPOSITORY_STANDARDS.md#141-canonical-local-ci).

The standard expects one reproducible, documented entry point with honest
outcomes. This guide does **not** require Rust, the name `xtask`, a particular
directory, workspace relationship, command set, configuration format,
dependency policy, result vocabulary, or migration. It is not a template or an
xtask conformance profile.

The review covered two public implementations at pinned revisions and one
private implementation. Private repository identity and details are
intentionally not reproduced here; only lessons that can be stated without
disclosing private content are included. The public references are evidence of
what was observed, not designated examples to copy.

## Bottom line

An xtask was a good fit once a gate behaved like a program: it resolved paths,
spawned many tools, applied repository policy, parsed output or archives,
distinguished evidence states, or needed the same native behavior on Windows
and Linux. Direct process execution removed a Git Bash dependency and kept
arguments and paths out of shell interpolation.

The change was not free. Even a small translation added a second Rust package,
dependencies, compilation, and maintenance. The richer runners became
substantial applications with their own parsing, path-safety, testing,
dependency, and evidence-lifecycle obligations. A short, stable sequence of
Cargo commands can still be clearer as a small script.

## What held up well

| Observed property | Value it created | Remaining qualification |
| --- | --- | --- |
| One documented command | Contributors and automation had a common entry point | The superseded gate implementation had to be removed or reduced to a thin launcher |
| Direct `Command` execution with explicit arguments and environment | Avoided Bash/PowerShell quoting differences and ran natively on Windows | Portability still depended on path handling, executable discovery, child tools, and actual cross-platform tests |
| Repository-root anchoring | Some aliases could be invoked from nested workspace directories and still ran at the intended root | A root-relative alias can fail before xtask starts, while a compile-time root can bind a directly executed cached binary to the checkout where it was built |
| Thin hosted workflow | Local and hosted verification shared gate logic while the workflow retained runner setup, permissions, timeout, and concurrency | A local xtask alone did not establish that hosted CI used it |
| Typed repository configuration | Package names, targets, profiles, and evidence wording were reviewable separately from orchestration | Configuration added value only when every field and relationship was validated and consumed |
| Explicit pass, failure, skip, and indeterminate states | Missing tools or targets were not silently presented as successful checks | Fail-fast runners also needed to identify work that never ran, or describe their summaries more narrowly |
| Focused tests for policy and parsing | Negative cases caught silent weakening in gate logic | Task-runner tests mattered only when the maintained gate actually executed them |
| Evidence-bound summaries | A green software gate did not become a model, silicon, timing, or publication claim | Generated evidence also needed invalidation, completeness, and commit/run identity |

The SHT4x implementation demonstrated the full local/hosted shape: its workflow
installed hosted prerequisites and then called the same `cargo xtask ci` used
locally. Its migration and later evidence refinements are recorded in
[PR #49](https://github.com/photon-circus/ph-sht4x-hts/pull/49) and
[PR #51](https://github.com/photon-circus/ph-sht4x-hts/pull/51).

## Crate-boundary choices

The two public implementations already show that an xtask can be an ordinary
workspace member or a separate excluded workspace. A non-default workspace
member is another available tradeoff; the table describes choices rather than
inventorying the private implementation.

| Available relationship | Useful when | Cost to make explicit |
| --- | --- | --- |
| Ordinary workspace member | One lockfile, toolchain, formatter, and workspace command set are more valuable than graph separation | Default workspace operations can include the host tool, and its dependencies enter the root lockfile |
| Workspace member outside `default-members` | Default product commands should stay narrow while selected workspace-wide commands can still include the tool | The difference between default and full workspace scope can be missed in local commands or documentation |
| Excluded crate with its own `[workspace]` | Host-only dependencies and checks should not enter the product workspace or lockfile | The runner needs its own lockfile, update policy, lint/test commands, and explicit invocation from the root alias |

These are local tradeoffs. Directory spelling does not establish dependency
independence, and workspace exclusion does not establish that the task runner's
dependencies are reviewed. A repository can decide whether the runner belongs
in formatting, Clippy, tests, dependency/license checks, and routine updates,
then make the chosen scope visible.

At the reviewed VEML7700 revision, the separate-workspace alias used a
root-relative manifest path and did not add `--locked`. It worked from the
documented repository root but failed before xtask startup from a nested crate,
and the root workspace's locked fetch did not cover the separate task-runner
lockfile. This is not proof that either choice is universally wrong; it shows
that invocation scope and lock enforcement belong to the boundary decision.
See the pinned
[Cargo alias](https://github.com/photon-circus/ph-veml7700-als/blob/aa69aa523d88e51553c8d9761fd8b436be1751cd/.cargo/config.toml).

## What failed or stayed incomplete

### Partial work looked authoritative

An early VEML7700 runner allowed `--only` to select one step while reporting
`PASS (full)`. The release profile could also begin a release-evidence record
for that partial run. The fix labeled selected-step runs as non-authoritative
and rejected `--only` with the release profile. The
[review discussion](https://github.com/photon-circus/ph-veml7700-als/pull/93#discussion_r3825932960)
is a compact example of why command convenience and evidence authority need
separate states.

One edge remained at the reviewed revision: selecting a step that the bounded
profile classifies as skipped still exits successfully and prints `PASS` for a
one-step, one-skip run. The output also says the selection is partial, but a
skip has still become a successful process result. See the pinned
[`report.rs` result rule](https://github.com/photon-circus/ph-veml7700-als/blob/aa69aa523d88e51553c8d9761fd8b436be1751cd/xtask/src/report.rs#L59-L64).
Selection, execution, and aggregate success are separate questions.

### Configuration and checks could exist without doing useful work

The same migration found unused configuration, a configured value contradicted
by a hard-coded regular expression, a comparison that could never fail, a
missing document marker that silently disabled a check, and substring-based
section matching that selected the wrong heading. Typed deserialization caught
unknown fields, but it did not prove that known fields affected behavior or
that the check was mutation-sensitive. These defects and their fixes are
recorded in [VEML7700 PR #93](https://github.com/photon-circus/ph-veml7700-als/pull/93).

### Paths and cleanup became safety-critical code

One runner incorrectly collapsed a leading `..` while resolving links. Another
cleanup path was derived from configuration in a way that could have selected a
broader build directory after a future config edit. The corrected code refused
unsafe traversal and refused recursive cleanup when the destination did not
have the exact expected shape. Moving path logic into Rust made it testable; it
did not make it correct automatically.

### The gate could interfere with itself

A repository-wide source scan began scanning the new xtask's test fixtures and
failed on text that looked like a product claim identifier. Self-inclusion can
also distort coverage, packaging, policy scans, or dependency results. Each
check benefits from an explicit subject: product, model, conformance consumer,
task runner, or whole repository.

### Generated evidence could outlive the run that produced it

The SHT4x coverage work initially lost a successful first-layer result when a
later layer failed, while a stale summary file could survive and appear current.
The fixes preserved partial diagnostic information, invalidated the summary at
run start, and added regression tests. See the
[partial-result discussion](https://github.com/photon-circus/ph-sht4x-hts/pull/51#discussion_r3825386425)
and
[stale-summary discussion](https://github.com/photon-circus/ph-sht4x-hts/pull/51#discussion_r3825386429).
The remaining general question is broader: every generated evidence artifact
needs a clear invalidation point or an identity tying it to a complete run and
commit.

VEML7700 also exposed a stronger version of this risk at the reviewed revision.
Release evidence was written progressively to its final path, and the archive
record was added before later unpacked-package tests. A later failure could
therefore leave a partial record whose configured prose said those tests ran.
See the pinned
[`record_archive` call](https://github.com/photon-circus/ph-veml7700-als/blob/aa69aa523d88e51553c8d9761fd8b436be1751cd/xtask/src/checks/package.rs#L40-L56)
and
[`evidence.ron` wording](https://github.com/photon-circus/ph-veml7700-als/blob/aa69aa523d88e51553c8d9761fd8b436be1751cd/xtask/data/evidence.ron#L35-L44).
A temporary or explicitly incomplete record, followed by finalization only after
every claimed check passes, avoids that ambiguity.

### External tools remained external

Rust replaced shell orchestration, not `cargo-deny`, coverage tools, embedded
targets, Git, registry access, or platform policy. Missing-tool classification,
version checks, install instructions, network expectations, and hosted
provisioning still needed deliberate handling. SHT4x later moved hosted gate
tools to checksum-verified prebuilt binaries in
[PR #55](https://github.com/photon-circus/ph-sht4x-hts/pull/55),
without changing the local command.

### Running a command was not the same as checking its result

A subprocess can exit successfully after printing information that still
contradicts repository policy. Package listings, metadata, coverage reports,
and generated archives establish an invariant only when the runner parses or
otherwise asserts the relevant property. Human inspection remains valid when
it is named as manual review rather than presented as an automated pass.

### Task-runner quality could fall outside the gate

Product-focused package selection can omit the runner's focused tests, linting,
or host dependencies even while the runner compiles and executes. That may be a
deliberate scope choice, but broad success wording makes the boundary easy to
miss. Once an xtask parses policy, deletes artifacts, inspects packages, or
writes release evidence, treating its code and dependency graph as maintained
tooling is often the more honest description.

### Migration did not imply all scripting moved

The public examples replaced their local verification scripts. They did not
thereby automate release authorization, version selection, tagging,
publication, secrets, hardware operation, or every maintainer command. Moving a
task into xtask is useful when it improves a bounded workflow; “no scripts” is
not itself an engineering outcome.

## Questions worth answering locally

These prompts are review aids, not requirements.

### Entry point and scope

- What exact command is canonical, and from which directories does it work?
- What commands are intentionally partial, and can their output be mistaken for
  the complete or release gate?
- Are help, command listing, and unknown-argument errors proportionate to the
  size of the command surface?
- Does any retained shell or PowerShell file duplicate logic or only delegate?

### Product and tooling boundary

- Is the xtask a workspace member, a non-default member, or a separate
  workspace, and why is that boundary useful here?
- Which format, lint, test, dependency, advisory, license, and update checks
  include the task runner itself?
- If the runner has a separate lockfile, which command enforces and prefetches
  it, and does the root alias use `--locked` when reproducibility depends on it?
- Can host-only dependencies change the product lockfile, package, MSRV, target
  graph, or feature resolution in an unintended way?

### Process and platform behavior

- Are programs launched directly with explicit argument and environment arrays,
  or does a hidden shell reintroduce quoting and platform dependencies?
- How are repository roots, non-UTF-8 paths, separators, executable suffixes,
  exit statuses, signals, and child output handled?
- Has the command run from clean Windows and Linux checkouts, including the line
  ending policy contributors actually use?
- Which checks require a network, registry index, installed target, or external
  binary, and how is absence classified?

### Checks and configuration

- Does each automated pass assert an invariant, or merely run and print a tool?
- What happens when a config field, placeholder, profile, step name, document
  marker, or expected output is missing, duplicated, empty, or unused?
- Would a representative defect make each important guard fail?
- Is an external config file buying reviewability, or has a short command list
  become a general task DSL without a second consumer?

### Results and evidence

- Are failure, skip, indeterminate, and never-run work distinguishable?
- Is the runner deliberately fail-fast or exhaustive, and does its summary say
  only what it actually reports?
- Can a partial selector write, finalize, or retain authoritative release
  evidence?
- Are old reports removed safely before work starts, or bound to a run and
  commit so stale output cannot appear current?
- Does the final wording preserve the boundary between software checks, model
  agreement, physical observation, qualification, and publication?

### Local and hosted execution

- When hosted CI exists, does it call the canonical command instead of
  reimplementing the steps?
- Which setup remains correctly hosted-only: permissions, concurrency,
  timeouts, secrets, caches, and pinned installation actions?
- Is a bounded hosted profile visibly incomplete relative to the authoritative
  local or release gate?

## A bounded migration approach

1. Inventory the old scripts, workflow steps, release instructions, agent
   guidance, generated evidence, external tools, and every distinct outcome.
2. Record the old gate's check order and semantics, including known false
   passes, manual inspections, skips, platform assumptions, and dirty-tree
   behavior. Parity does not require preserving a defect.
3. Choose the smallest crate boundary and command surface that fits the current
   repository. Keep policy in Rust until external data has a concrete editing
   or reuse advantage.
4. Run old and new gates on the same revision where feasible. Compare verdicts,
   then exercise representative failures and missing prerequisites rather than
   comparing only green output.
5. Test native Windows and Linux behavior from clean clones and nested
   directories. Include the repository's actual line-ending configuration.
6. Make partial profiles, selected steps, generated artifacts, and release
   evidence explicitly non-interchangeable.
7. Update README, contribution, release, agent, and hosted-workflow references
   in the same bounded change. Remove the superseded implementation once parity
   and intended corrections are established.
8. Run the xtask's own focused tests and dependency checks according to the
   chosen tooling boundary, then record any remaining manual or external
   prerequisite honestly.

## Public evidence snapshots

- [`ph-sht4x-hts` at `af521e9`](https://github.com/photon-circus/ph-sht4x-hts/tree/af521e978f780528bbfd6b601d0fca06a3810f44/xtask)
  shows a workspace-member runner with validated repository configuration,
  coverage evidence, a fail-closed aggregate result, and a thin hosted caller.
- [`ph-veml7700-als` at `aa69aa5`](https://github.com/photon-circus/ph-veml7700-als/tree/aa69aa523d88e51553c8d9761fd8b436be1751cd/xtask)
  shows a separate host-tool workspace, explicit profiles and selected steps,
  modular checks, release-evidence handling, and review-driven negative-case
  hardening.

These snapshots are time-bounded implementation evidence. Later repository
changes may invalidate individual observations, and neither implementation is
an organization template.
