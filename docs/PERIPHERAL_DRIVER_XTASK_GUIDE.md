# Rust xtask field guide for Photon Circus technical repositories

Status: **Explicitly non-normative field notes**

Evidence snapshot: **2026-08-22 UTC**

## Purpose and boundary

This guide records experience from repository-local `xtask` crates in Rust
technical repositories, including peripheral drivers and reusable capability
libraries. It began with three shell-to-xtask driver migrations and now also
reflects a default-branch review of task-runner patterns across Photon Circus.
It supplements the technology-neutral
[canonical local CI standard](../REPOSITORY_STANDARDS.md#141-canonical-local-ci).

The standard requires an initial verification entry point for promotion to
Incubating, reproducible local CI for promotion to Active, and recommends one
canonical routine verification implementation for technical repositories. This
guide does **not** require Rust, the name `xtask`, a particular directory,
workspace relationship, command set, configuration format, dependency policy,
result vocabulary, or migration. It is not a template or an xtask conformance
profile.

Peripheral-driver repositories additionally remain subject to the
[CI contract](PERIPHERAL_DRIVER_PROFILE.md#ci-contract) and
[software publication gate](PERIPHERAL_DRIVER_PROFILE.md#software-publication-gate)
when they apply. When such a peripheral-driver runner executes a device
behavioral model or driver-versus-device-model conformance check, the
[normative validation-layer rules](DEVICE_BEHAVIORAL_MODEL_STANDARD.md#7-validation-layers-normative)
control the claims those checks establish. Task-runner design does not
extend those driver-specific obligations to capability libraries or strengthen
or weaken them where they do apply.

An `xtask` crate does not by itself identify the canonical verification gate.
Repositories also use task binaries for generation, firmware build and flash,
hardware operation, artifact inspection, and maintainer utilities. Establish
which command, if any, owns routine verification before applying gate-specific
advice. A mixed task binary can contain mutating or hardware-operating commands
while keeping its canonical verification command free of tracked-source,
hardware, credential, and publication effects.

The original review covered two public implementations at pinned revisions and
one private implementation. The 2026-08-22 follow-up enumerated recursive
default-branch trees across 35 accessible organization repositories, then
classified every manifest whose path ended in `xtask/Cargo.toml` through its
manifest, documentation, source, and workflow role. It found 11 xtask crates:
nine canonical verification gates and two operational utilities. These counts
are a time-bounded census, not a target or adoption metric.

Private repository identity and details are intentionally not reproduced here;
only lessons that can be stated without disclosing private content are
included. Public references are evidence of what was observed, not designated
examples to copy.

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
| Separate verification and mutation commands | CI could detect generated-source or snapshot drift without changing the reviewed tree | Tracked-write, hardware, credential, and publication effects still needed explicit command names and documentation |

A useful default is that the canonical verification command does not rewrite
tracked sources, publish, tag, create a release, use publication credentials,
or operate physical hardware. Explicit commands such as `generate`,
`schema --write`, or `flash` can still belong in the same binary; the boundary
applies to the authoritative gate, not every task command.

The SHT4x implementation demonstrated the full local/hosted shape: its workflow
installed hosted prerequisites and then called the same `cargo xtask ci` used
locally. Its migration and later evidence refinements are recorded in
[PR #49](https://github.com/photon-circus/ph-sht4x-hts/pull/49) and
[PR #51](https://github.com/photon-circus/ph-sht4x-hts/pull/51).

## Crate-boundary choices

The three public snapshots show that an xtask can be an ordinary workspace
member, a member outside `default-members`, or a separate excluded workspace.
The table describes choices rather than templates and does not inventory the
private implementation.

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

Test alias bootstrap and direct-binary root discovery separately. An upward
search can select a nested tool workspace when its marker is too generic, while
a root-relative alias can fail before that search runs.

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

A defensible generated-evidence lifecycle is:

1. Remove or invalidate stale final and incomplete records before work starts.
2. Write progressive diagnostics only to an explicitly incomplete or temporary
   path.
3. Add a claim only after the operation supporting it has completed.
4. Publish the final record only after every claimed check succeeds.
5. Bind the final record to the relevant commit, run, artifact, and environment.
6. Test that failure or termination before finalization cannot leave
   authoritative-looking output.

A same-filesystem rename is one implementation technique. The important
property is that an incomplete run cannot leave a record presented as complete.

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

Once runner code interprets policy, configuration, paths, archives, generated
artifacts, or evidence, including its formatting, linting, focused tests, and
dependency checks in the maintained gate is a useful default. If the repository
deliberately excludes one of those checks, make the omission visible beside the
canonical command. Merely compiling and executing the runner does not exercise
its rejection behavior.

### Copied gate code could fork silently

Correctness-sensitive runner code was copied across repositories for archive
comparison, path handling, configuration, dependency checks, and evidence
writing. Copying can be a reasonable starting point, but fixes can then diverge
without a visible compatibility boundary.

When substantially identical invariant-heavy code appears in multiple
repositories, make an explicit local choice:

- Extract a versioned shared crate or tool.
- Retain local copies with recorded provenance and an update or comparison
  strategy.
- Document why the implementations have intentionally diverged.

This applies the organization-level signal for
[recurring verification gaps](../REPOSITORY_STANDARDS.md#11-contribution-and-hardware-evidence).
It is a design prompt, not a requirement to centralize small
repository-specific gates.

### Migration did not imply all scripting moved

The original public migration examples replaced their local verification
scripts. They did not thereby automate release authorization, version
selection, tagging, publication, secrets, hardware operation, or every
maintainer command. Moving a task into xtask is useful when it improves a
bounded workflow; “no scripts” is not itself an engineering outcome.

## Questions worth answering locally

These prompts are review aids, not requirements.

### Entry point and scope

- What exact command is canonical, and from which directories does it work?
- Which task commands are verification gates, generators, release verifiers,
  firmware or hardware operations, or maintainer utilities?
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
- Which lockfile bootstraps the runner, and does the alias use `--locked`
  whenever reproducibility depends on that committed lockfile, regardless of
  workspace membership?
- Can host-only dependencies change the product lockfile, package, MSRV, target
  graph, or feature resolution in an unintended way?

### Process and platform behavior

- Are programs launched directly with explicit argument and environment arrays,
  or does a hidden shell reintroduce quoting and platform dependencies?
- How are repository roots, non-UTF-8 paths, separators, executable suffixes,
  exit statuses, signals, and child output handled?
- Can the alias start from every documented directory, independently of whether
  an already-built runner can find the repository root?
- Does root discovery use repository-distinctive identity rather than a generic
  `Cargo.toml`, especially when examples, consumers, or tools are nested
  workspaces?
- Which Cargo bootstrap variables and flags are deliberately inherited,
  removed, or pinned for nested Cargo invocations?
- Has the command run from clean checkouts on every documented contributor
  platform, including native Windows and Linux when both are claimed, with the
  line-ending policy contributors actually use?
- Which checks require a network, registry index, installed target, or external
  binary, and how is absence classified?

### Checks and configuration

- Does each automated pass assert an invariant, or merely run and print a tool?
- What happens when a config field, placeholder, profile, step name, document
  marker, or expected output is missing, duplicated, empty, or unused?
- Does the maintained gate execute the runner's own negative and configuration
  tests, rather than only proving that the runner compiles?
- Can an empty, duplicate, or narrowed configured step list still emit broad
  success wording?
- Would a representative defect make each important guard fail?
- Is an external config file buying reviewability, or has a short command list
  become a general task DSL without a second consumer?
- When a peripheral-driver runner checks device propositions or
  physical-evidence records, is automation limited to the
  [closed structural invariants suitable for automation](peripheral-driver-resources/README.md#proportionate-automation),
  leaving semantic evidence sufficiency to review?

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
   Classify each task command by authority and side effect.
2. Record the old gate's check order and semantics, including known false
   passes, manual inspections, skips, platform assumptions, and dirty-tree
   behavior. Parity does not require preserving a defect.
3. Choose the smallest crate boundary and command surface that fits the current
   repository. Choose repository identity, alias bootstrap scope, and lock
   enforcement deliberately. Keep policy in Rust until external data has a
   concrete editing or reuse advantage.
4. Run old and new gates on the same revision where feasible. Compare verdicts,
   then exercise representative failures and missing prerequisites rather than
   comparing only green output.
5. Test behavior from clean clones and nested directories on every documented
   contributor platform, including native Windows and Linux when both are
   claimed. Include the repository's actual line-ending configuration.
6. Make partial profiles, selected steps, generated artifacts, and release
   evidence explicitly non-interchangeable. Keep verification separate from
   tracked-file, hardware, credential, and publication effects.
7. Update README, contribution, release, agent, and hosted-workflow references
   in the same bounded change. Remove the superseded implementation once parity
   and intended corrections are established.
8. Run or explicitly disclose the xtask's own formatting, linting, focused
   tests, and dependency checks according to the chosen tooling boundary, then
   record any remaining manual or external prerequisite honestly.
9. If correctness-sensitive code was copied from another repository, record its
   provenance and update strategy.

## Public evidence snapshots

- [`ph-color` at `a7989e3`](https://github.com/photon-circus/ph-color/tree/a7989e3d329d1b15dc9ba8b01a1728faab4151e9/xtask)
  shows a reusable capability-library runner kept outside the workspace's
  default members, with generation separated from verification and a bounded
  hosted selection of the same gate.
- [`ph-sht4x-hts` at `af521e9`](https://github.com/photon-circus/ph-sht4x-hts/tree/af521e978f780528bbfd6b601d0fca06a3810f44/xtask)
  shows a workspace-member runner with validated repository configuration,
  coverage evidence, a fail-closed aggregate result, and a thin hosted caller.
- [`ph-veml7700-als` at `aa69aa5`](https://github.com/photon-circus/ph-veml7700-als/tree/aa69aa523d88e51553c8d9761fd8b436be1751cd/xtask)
  shows a separate host-tool workspace, explicit profiles and selected steps,
  modular checks, release-evidence handling, and review-driven negative-case
  hardening.

These snapshots are time-bounded implementation evidence. Later repository
changes may invalidate individual observations, and none of these
implementations is an organization template.
