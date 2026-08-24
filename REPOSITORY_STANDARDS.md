# Photon Circus Repository Standards v0.1

Status: **Adopted**

Numbered baseline: **0.1.0**

Baseline adopted: **2026-08-11 UTC**

Applies to: repositories owned by the Photon Circus GitHub organization

Photon Circus builds deterministic, bare-metal software and hardware for embedded systems, instruments, and strange machines. These standards give each repository a clear identity, a bounded responsibility, reproducible engineering evidence, and an honest maintenance posture.

They define a common floor. They do not require every experiment to become a polished product, and they do not require every repository to use the same depth of verification.

## 1. Normative language

The terms **must**, **must not**, **required**, **should**, **should not**, and **may** express the strength of a rule.

- **Must** and **required** identify an obligation.
- **Should** identifies the expected default; deviations require a documented reason.
- **May** identifies an optional practice.

The live default branch (`main`) is the adopted authority. A normative change
takes effect when it is merged to `main`. `Unreleased` in the changelog means
that the change has not yet been collected into a later numbered snapshot; it
does not mean the change is ineffective. A review, migration, or evidence
record that needs a reproducible authority should identify the exact commit
reviewed.

## 2. Governing principles

Photon Circus repositories follow these principles:

1. **Bounded scope precedes quality.** A repository can achieve high quality only when its claims, invariants, evidence, and definition of done are finite.
2. **Responsibilities belong at the lowest layer capable of enforcing them.** Device facts belong in drivers; board and application policy belong in integration; recurring invariant-heavy coupling belongs in a narrowly scoped shared crate.
3. **Claims require evidence.** Verification must follow the actual failure modes and guarantees of the repository.
4. **Constraints are documented, not hidden.** Known deviations, unsupported configurations, and deliberate trade-offs are part of the engineering contract.
5. **Hosted CI is bounded shared infrastructure.** It provides timely contributor feedback; complete engineering evidence may remain local.
6. **Experiments are valid outcomes.** Lifecycle labels describe expectations, not intellectual merit.

## 3. Repository identity

Every repository must have:

- A concise GitHub description explaining what it provides.
- A `Lifecycle` custom property.
- One or more `Domain` custom properties.
- Relevant GitHub topics for language, platform, device family, protocol, or purpose.
- A root `README.md`.
- A root `LICENSE`.

### 3.1 Lifecycle values

- **Experimental** — research, architectural exploration, an unbounded sandbox, or work whose supported contract is not yet established.
- **Incubating** — bounded work intended to become a supported component.
- **Active** — usable, documented, verified, and actively developed.
- **Maintenance** — supported, with limited new feature development.
- **Archived** — retained for historical or reference purposes; no further support is promised.

### 3.2 Domain values

Repositories use one or more of:

- `Firmware`
- `Hardware`
- `Libraries`
- `Tooling`
- `Experience`
- `Documentation`

### 3.3 Lifecycle transitions

#### Experimental to Incubating

The repository must have:

- A bounded responsibility and explicit non-goals.
- A clear README.
- A license.
- An initial verification entry point.
- Identified supported users, targets, or integration contexts.

#### Incubating to Active

The repository must have:

- A stable responsibility boundary.
- A changelog.
- Reproducible local CI.
- Supported targets and configurations documented.
- Contribution and security guidance where applicable.
- A release process for published or versioned deliverables.
- Default-branch protection.
- Bounded hosted CI when the repository is public.

#### Active to Maintenance

The repository must document:

- Its stable functionality and compatibility posture.
- Which fixes and updates remain in scope.
- That major feature development is no longer expected.

#### Maintenance to Archived

The repository must:

- State that further support is not promised.
- Identify a replacement or migration path when one exists.
- Preserve its license, changelog, release history, and historical context.

## 4. Bounded scope and invariant ownership

Every repository must define a bounded responsibility.

It must state:

- What problem it owns.
- Which invariants it is responsible for maintaining.
- Which users or components it serves.
- What evidence establishes that it works.
- What is explicitly outside its scope.
- What condition allows the work to be considered complete or stable.

Architecture, abstraction, documentation, and local code quality cannot substitute for this boundary. Individual components may be excellent while repository-level quality remains unable to converge if the repository continually absorbs new independent responsibilities.

### 4.1 Feature-admission test

A feature belongs in a repository only when it:

1. Directly strengthens or completes the declared responsibility.
2. Introduces invariants the repository is the correct layer to enforce.
3. Fits the repository's evidence and release model.
4. Does not silently add board, application, workflow, or unrelated domain policy.
5. Leaves the repository's non-goals intact.

A technically impressive implementation is not sufficient justification.

If the feature solves a distinct problem with independent invariants, it should become a narrowly scoped crate, a separate repository, an integration-layer component, application-specific code, or an explicitly Experimental investigation.

### 4.2 Shared-crate admission test

A shared crate is justified when it removes a recurring, bounded, invariant-heavy problem from multiple otherwise independent components.

It should have:

- A narrow recurring problem.
- Clear ownership, overload, and failure semantics.
- At least one credible integration use.
- Explicit non-goals.
- An independently testable contract.
- A reason it should not remain application integration code.

`ph-eventing` is the public reference example: it owns predictable producer/consumer handoff rather than attempting to become a general embedded runtime.

### 4.3 Repository cohesion

A repository may contain multiple crates when they:

- Serve one coherent responsibility boundary.
- Share contracts and release intent.
- Need coordinated development.
- Do not turn the repository into a general destination for adjacent problems.

Repository boundaries prevent invariant leakage; one-crate purity is not a goal by itself.

### 4.4 Scope-review signals

A repository should undergo a scope review when:

- New features repeatedly require new architectural layers.
- Independent device or application domains accumulate under one release boundary.
- A shared core becomes the default destination for unrelated abstractions.
- Verification expands continuously without retiring responsibility.
- Routine changes require understanding unrelated subsystems.
- The repository cannot state a short, stable value proposition.
- Non-goals are absent or repeatedly overridden.
- Extracted components cannot be reasoned about or released independently.

When a repository becomes unbounded, stop admitting unrelated capabilities, classify it honestly, preserve its research value, inventory its responsibilities, and extract coherent responsibilities into narrowly scoped components. Extraction is how valuable engineering becomes maintainable.

## 5. Naming

All new Photon Circus repositories and publishable organization-owned crates must use the `ph-` prefix.

Naming rules apply prospectively. Existing repositories and packages are not renamed as part of v0.1. Historical names are grandfathered unless a separate migration is explicitly approved.

### 5.1 Peripheral drivers

Peripheral-driver repositories and their primary packages use:

```text
ph-<part>-<class>
```

- `<part>` is the lowercase, path-safe device part or family identifier.
- `<class>` is a short standardized device-role token.
- The repository and primary published crate should use the same name.
- Rust import names follow Cargo's normal hyphen-to-underscore conversion.
- The greenfield Rust unit path is `crates/<part>`.

Initial class tokens:

| Token | Meaning |
| --- | --- |
| `adc` | Analog-to-digital converter |
| `als` | Ambient-light sensor |
| `env` | Environmental sensor combining barometric pressure and temperature, with optional humidity |
| `gpio` | General-purpose digital I/O expander |
| `hts` | Humidity and temperature sensor |
| `imu` | Inertial measurement unit |
| `mac` | Network media-access controller |
| `nor` | NOR flash memory |
| `pmon` | Digital current, voltage, and power monitor |
| `rtc` | Real-time clock/calendar |
| `touch` | Capacitive touch and proximity controller |
| `switch` | Multi-channel digital bus switch |

New tokens may be added when a real project requires them. Synonyms should not be introduced casually.

### 5.2 Hardware design libraries

Libraries that encode source-derived design equations or constraints for an
analog component, but do not control a digital peripheral, use the same bounded
part-and-class form:

```text
ph-<part>-<class>
```

Their README must state plainly that they are not device drivers, circuit
simulators, or hardware-qualification tools. Initial class tokens:

| Token | Meaning |
| --- | --- |
| `buck` | Step-down converter design and validation |

### 5.3 Shared capabilities

Repositories solving a reusable cross-component problem use:

```text
ph-<capability>
```

Subcrates may extend the identity with a bounded role:

```text
ph-<capability>-<role>
ph-<capability>-<role>-<implementation>
```

## 6. README contract

Every repository README must answer near the top:

1. What is this?
2. What is it for?
3. What state is it in?
4. What responsibility does it own?
5. What is outside its scope?
6. What constraints or trade-offs define it?
7. How is it built, tested, or inspected?

Incubating, Active, and Maintenance repositories should also document:

- Supported targets and toolchains.
- A minimal usage or bring-up example.
- Public API or hardware-interface expectations.
- Known limitations, hazards, and unsupported configurations.
- The verification commands maintainers actually run.

Claims should be specific. Prefer “fixed-capacity, `no_std`, no heap allocation” over “lightweight and embedded-friendly.”

## 7. Documentation requirements

| File | Requirement |
| --- | --- |
| `README.md` | Every repository |
| `LICENSE` | Every repository |
| `CHANGELOG.md` | Every non-Experimental repository and every repository with a published package or versioned deliverable |
| `CONTRIBUTING.md` | Public Incubating, Active, and Maintenance repositories |
| `SECURITY.md` | Public Active and Maintenance repositories |
| `RELEASING.md` | Every repository with a published package or versioned deliverable |
| `AGENTS.md` | Active technical repositories using coding agents or carrying non-obvious invariants |
| `CODEOWNERS` | Repositories with multiple maintainers or sensitive ownership boundaries |
| `CODE_OF_CONDUCT.md` | Public repositories accepting community contributions |

Files must contain repository-specific guidance. Empty boilerplate does not satisfy the requirement.

### 7.1 Agent documentation

`AGENTS.md` must not merely duplicate the README or public API documentation. It should capture information an agent cannot safely infer from source alone:

- The repository's priority order.
- Internal models and load-bearing invariants.
- Coupled edits the compiler cannot enforce.
- Known deviations and deliberate compromises.
- Commands that establish particular claims.
- Previously attempted and rejected approaches.
- Repository-specific operational traps.
- Documentation surfaces that must change together.

The governing rule is: record what is expensive to rediscover and cheap to get subtly wrong.

## 8. Changelog standard

Every non-Experimental repository must contain `CHANGELOG.md`.

The changelog follows the `ph-eventing` model:

- Begin with `# Changelog`.
- Maintain an `## Unreleased` section.
- For one published package or a synchronized package set, use release headings
  in the form `## X.Y.Z - YYYY-MM-DD`.
- Dates use UTC and ISO 8601 format.
- Organize entries under applicable headings: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`, `Documentation`, and `Known issues`.
- Mark breaking changes explicitly with `**Breaking:**`.
- Describe observable behavior and engineering consequences, not merely filenames or commit activity.
- Preserve known limitations until they are resolved.
- Move accumulated `Unreleased` entries into the release when publishing.

A workspace that versions published packages independently must make changelog
ownership unambiguous. It may use package-qualified root headings such as
`## <package> X.Y.Z - YYYY-MM-DD` with package-scoped entries under
`Unreleased`, or package-local changelogs using the ordinary heading form and
linked from the required root changelog. The repository must document the
chosen scheme. Each package release moves only its own accumulated entries and
maps them to the same package and version identified by its tag and GitHub
Release. The scheme applies prospectively; existing release headings are not
rewritten merely to adopt it.

When a release introduces a major new feature or substantial capability, it must include a value statement immediately below the release heading. The statement explains:

1. Why the feature was added.
2. Which problem or limitation it addresses.
3. What value it provides.
4. Which important cost, constraint, or trade-off it introduces.

A list of APIs is not a substitute for a value statement.

Unpublished Experimental repositories may maintain a changelog but are not
required to do so. Intentional publication or another versioned deliverable
triggers the changelog and release-documentation requirements regardless of
lifecycle. Establishing a changelog is otherwise part of leaving Experimental
status.

Archived repositories without reliable historical release records must still provide a changelog. It may state that detailed history predates the standard and direct readers to tags or commit history.

## 9. Licensing

Every repository must contain a root `LICENSE`, regardless of lifecycle, visibility, maturity, or publication status.

### 9.1 Default

The default Photon Circus license is the MIT License.

### 9.2 Apache-2.0 exception

Apache License 2.0 should be used when provenance, compatibility, patent terms, or substantial derivation from Apache-licensed upstream work makes it appropriate.

Repositories derived from upstream work must:

- Identify the upstream project and relevant source material.
- State when an implementation has been modified, translated, or transcoded.
- Preserve applicable copyright, attribution, and notice material.
- Avoid presenting derived work as entirely original.
- Record the licensing rationale when it is not obvious.

### 9.3 Consistency

The selected license must:

- Match package manifests and repository metadata.
- Be included in published packages and source distributions.
- Cover the repository contents clearly or identify separately licensed portions.
- Be reconsidered when upstream code, designs, generated assets, or documentation introduce additional obligations.

MIT is the default; a justified Apache-2.0 choice is not a standards violation.

## 10. Peripheral-driver and integration boundary

A peripheral driver makes supported operations on one physical device truthful and correct through declared abstract resource interfaces.

The driver owns, where applicable:

- Device facts, identity, legal encodings, and units.
- Register, command, and protocol behavior.
- Complete single-device operations.
- Device-required timing and bounded completion.
- State authority, invalidation, and resynchronization.
- Device-level errors, partial commit, and recovery semantics.
- Memory, DMA, interrupt, and concurrency invariants intrinsic to the peripheral.
- Abstract resource requirements necessary to uphold its guarantees.

Integration owns:

- Concrete bus, delay, clock, GPIO, power, reset, and memory resources.
- Board routing and electrical topology.
- Cross-component resource arbitration.
- Scheduling, sampling cadence, and workflow deadlines.
- Workflow retry, escalation, and application recovery policy.
- Multi-device coordination.
- System calibration and product-level accuracy.
- Logging, telemetry, user reporting, and operational policy.

The decision test is:

> Behavior required to make one supported device operation truthful belongs to the driver. Concrete resources, scheduling, composition, and application response belong to integration.

### 10.1 Peripheral-driver release and evidence profile

This profile applies to organization-owned peripheral-driver repositories and
crates. It separates three dimensions that must not be collapsed:

- **Distribution:** unpublished, SemVer prerelease, or ordinary release.
- **Software maturity:** repository lifecycle, API coherence, implementation
  validation, and release readiness.
- **Evidence:** implementation-tested, model-conformant, physically observed,
  or qualified behavior, recorded per operation or claim.

Publication does not imply model conformance, physical observation, hardware
qualification, or promotion to `Active`. Those claims require their own evidence
but are not prerequisites for a crate to exist or for a software-ready crate to
publish an ordinary release.

Normative requirements attach to claims and artifacts that actually exist. If a
crate claims model conformance, physical behavior, or `ph-hil` qualification, it
must satisfy the corresponding conditional contract. Missing additive
validation limits that claim; it must not invalidate narrower evidence or force
every crate to adopt the same model, fixture, schema, support library, or
integration structure.

Every newly created Rust peripheral-driver package must begin with a
lifecycle-matching SemVer prerelease version such as
`0.1.0-experimental.1` or `0.1.0-incubating.1`, even when
`publish = false`. An existing unpublished package with an ordinary local
version must replace it with the corresponding prerelease before its first
durable release. If that ordinary version was already tagged or published, it
remains grandfathered rather than being relabeled; any later prerelease must use
a higher numeric core, while any later ordinary release follows the software
release gate below. A lifecycle change must not decrease SemVer precedence.

Intentional registry publication triggers the documentation and release
requirements in Sections 7 and 17 regardless of lifecycle. CI must verify the
declared version state and inspect the package without publishing it; publication
remains a separate maintainer-controlled release action. An ordinary release is
a software distribution decision. It requires the ordinary repository release
contract, accurate limitations and evidence status, and a verified packaged
artifact, but not a complete behavioral model, `ph-hil` adoption, or hardware
qualification.

A behavioral model and driver-versus-model conformance tests are additive. They
become required only for behavior described as model-conformant. Physical
evidence becomes required only for the physical or qualification claim it is
offered to support. Where model and silicon evidence disagree, the affected
contract, model, driver, selected variant, or limitation must be reconciled
before either is used to support that claim.

MCU, BSP, board, firmware, model, and physical-test artifacts are admitted only
when they add current, bounded value. Their presence must not imply stronger
driver or hardware support than the retained evidence establishes. Speculative
`ph-hil` schemas, fixtures, build shims, or capability inventories remain
forbidden before a reviewed consumer requires them.

An additional universal driver requirement belongs in this profile only when it
protects a current cross-driver responsibility or evidence boundary, applies
proportionally across materially different devices, and does not depend on
unavailable or unsettled tooling. Otherwise it must be conditional on the
relevant claim or artifact, remain non-normative guidance, or be recorded as a
deferred decision.

The reusable status disclosure, minimal repository shape, CI contract, release
gate, and conditional qualification handoff are defined in the
[`Peripheral Driver Release and Evidence Profile`](docs/PERIPHERAL_DRIVER_PROFILE.md).

### 10.2 Stable device propositions

A peripheral-driver repository must assign a permanent, unambiguous identifier
to every retained device or documentary proposition used to justify driver
behavior, model behavior, a conformance expectation, a physical claim, or a bug
disposition. The identifier names one stable referent. It must never be reused
or redefined, and it must remain resolvable after the proposition is superseded
or split. A changed meaning receives a new identifier.

For existing repositories, this requirement applies when a proposition is
introduced, materially changed, newly cited by a downstream artifact, or used
to resolve a disagreement after adoption of this section. It does not require a
retrospective inventory or migration of untouched legacy facts. Incomplete
retrospective coverage is not by itself a release block.

The identifier must resolve to one canonical proposition and to exact,
resolvable provenance for every retained evidence item. When no retained item
decides the proposition, the record states that honestly rather than treating
missing evidence as approval, proof of the opposite behavior, or pending owner
work. A located source omission can establish only a documentary proposition
about that bounded search; it does not establish inverse device behavior.

A checkbox, review owner, or promise such as "maintainer will validate" is
workflow metadata. It must not substitute for proposition identity, provenance,
or evidence and does not establish a claim. Driver, model, conformance, physical
work, and bug disposition addressing the same proposition must cite the same
identifier while independently owning their consequences and implementations.
They state their local consequence and link to the canonical proposition rather
than maintaining another copy of its wording or provenance. The citation may
live in the nearest maintained contract or trace map; this section does not
require an identifier at every code site or extraction of every implicit
implementation fact.

The existence of a proposition or a lack of deciding evidence does not by itself
create a validation assignment or block a release. This section does not require
a particular file name, identifier spelling, registry schema, evidence-state
vocabulary, completeness audit, or exhaustive transcription of source material.

## 11. Contribution and hardware evidence

Public Incubating, Active, and Maintenance repositories must support contributor bug reports and pull requests.

Embedded bug-report templates should request, where applicable:

- Device and board revision.
- MCU and target triple.
- Bus or interface mode.
- Enabled features.
- Toolchain and package version.
- A minimal reproduction.
- Expected and observed behavior.
- Logs, traces, or register observations.
- Whether evidence came from hardware, simulation, or a mock.

Contributor reports are valuable field evidence. When a reported observation is
retained or used as physical evidence, its record should state whether and how
it was independently reproduced. "Not reproduced" is a sufficient status and
does not create reproduction work or erase the report.

Changes that rely on a device or documentary proposition follow Section 10.2.
Mock or simulated behavior must not silently become a universal hardware claim.

Unresolved observations retain their evidence state. A repository may create a
known limitation or follow-up when a current dependent claim or acceptance
criterion needs one and a feasible, discriminating completion condition can be
named; the evidence record itself does not require further work.

Recurring verification gaps are organization-level design signals. When the same invariant-heavy tooling problem appears across repositories, maintainers should consider extracting shared infrastructure rather than building incompatible local solutions repeatedly.

## 12. Feature development

Substantial features move through explicit exploration, proposal, implementation, and release stages.

### 12.1 Feature states

| State | Meaning |
| --- | --- |
| Exploratory | Problem and direction recorded; not implementation-ready |
| Proposed | Contract, boundaries, open questions, and evidence requirements defined |
| Committed | Maintainer decision made; expected to enter a release |
| Accepted | Implementation and evidence meet the bar |
| Rejected | Deliberately declined, with reasoning retained |
| Referential | Analysed and preserved, but not scheduled |

A document existing does not make a feature ready.

### 12.2 Proposal contents

Before implementation, a substantial proposal should state:

- The problem and user value.
- Why it belongs in the repository.
- Its behavioral contract.
- Architectural boundaries and non-goals.
- Ownership, overload, failure, and cancellation semantics where relevant.
- Compatibility and versioning impact.
- Open design questions.
- Evidence required for acceptance.
- The promotion bar for implementation.

Contracts should be independent of implementation details where practical. Tests and evidence should map back to specific claims.

### 12.3 Branch structure

For substantial feature cycles:

1. Merge the shared planning record first.
2. Use one candidate, one branch, and one pull request.
3. Avoid stacked feature PRs by default.
4. Resolve shared design decisions before dependent implementation begins.
5. Keep candidates independently acceptable or rejectable.
6. Add changelog entries beneath `Unreleased`.
7. Do not close `Unreleased` until release assembly is complete.
8. Synchronize open candidate branches after shared integration files change.

Dependencies should be sequenced by decisions, not deep branch stacks.

### 12.4 Rejection

Rejection is a first-class engineering result. A rejected feature should retain:

- The original problem and proposal.
- The rejecting evidence or reasoning.
- A `Rejected` status.
- Conditions under which it may be reconsidered.
- Reusable lessons in agent or architecture documentation.

## 13. Verification

Verification must be proportional to risk and follow the repository's actual failure modes.

The baseline for maintained software is:

- Formatting.
- Compilation.
- Unit or behavioral tests.
- Lints with warnings treated as failures.
- Documentation building or link validation where applicable.

Additional checks should be used when relevant:

- Embedded target compilation.
- Feature-combination checks.
- Hardware-in-the-loop testing.
- Miri or sanitizers for unsafe code.
- Loom or model checking for concurrency.
- Code-size regression checks.
- Cycle or latency measurements.
- Schematic or ERC validation.
- Reproducible fabrication-output checks.

A green host test is not sufficient evidence for target-specific, concurrent, unsafe, timing-sensitive, or physical behavior.

Experimental repositories may have incomplete automation, but the README must state what has and has not been verified.

## 14. Continuous integration

Photon Circus distinguishes authoritative local verification from bounded hosted CI.

### 14.1 Canonical local CI

Technical repositories should provide one canonical verification entry point.
Common forms include:

```text
scripts/ci.sh
cargo xtask ci
```

The repository should document the exact invocation, its supported working
directory or directories, and the scope it establishes.

The entry point should:

- Run on the contributor platforms documented by the repository.
- State any tools or environment it requires.
- Be the single implementation of the routine verification gate.
- Report pass, failure, and skipped checks distinctly.

A repository may expose local verification profiles or selectors through that
one implementation. Each documented verification invocation must identify the
scope it establishes and any work it may skip; profile names remain
repository-local.

An aggregate verification `PASS` asserts only the named invocation scope and
only when every check that scope claims to establish ran and passed. A partial
profile or selection must not be presented as complete or release verification.
Skipped and indeterminate work do not count as passed. A fail-fast runner may
stop at the first failure, but it must not claim that later work ran or that its
summary is exhaustive. A verification invocation that establishes no passing
check must not report aggregate `PASS`.

A shell implementation should use a POSIX-compatible shell and should run on
Linux and under Git Bash on Windows.
A repository may keep a thin compatibility launcher, but routine gate logic
should live in only one implementation. Parallel Bash and PowerShell
implementations of the same gate should not be maintained.

The explicitly non-normative
[`Rust xtask field guide for Photon Circus technical repositories`](docs/PERIPHERAL_DRIVER_XTASK_GUIDE.md)
records experience from several Rust repositories without prescribing an xtask
layout, command set, configuration format, or migration.

### 14.2 Private repositories

For complex private repositories, local CI is authoritative. Hosted workflows should remain minimal, manually dispatched, or disabled when they would consume shared Actions capacity without proportional value.

Private repositories should avoid large hosted matrices, frequent scheduled runs, and expensive automated analysis. Release or integration PRs should record required local evidence.

### 14.3 Public repositories

Released public software should provide bounded GitHub Actions CI for contributor feedback. It should cover appropriate inexpensive checks such as formatting, linting, unit tests, documentation, supported-target compilation, a limited feature matrix, and dependency or license checks.

Hosted CI should:

- Cancel superseded pull-request runs.
- Set reasonable timeouts.
- Avoid duplicated jobs.
- Expose one stable aggregate `ci` result for branch protection.
- Pin third-party Actions to immutable commit SHAs.
- Use least-privilege permissions.

### 14.4 Expensive checks

Expensive, specialized, or hardware-dependent verification normally remains offline, including:

- Hardware-in-the-loop execution.
- Large cross-target matrices.
- Miri sweeps and Loom model checking.
- Fuzzing and full coverage analysis.
- Code-size surveys and cycle measurements.
- Soak tests and reproducibility audits.
- Physical instrumentation and safety checks.

Remote CI must say when it covers only part of the release gate.

### 14.5 Reference environments

Complex repositories may provide a pinned Docker or equivalent reference environment. A useful reference environment pins otherwise drifting tools, stamps versions, and can be distributed prebuilt.

This is optional. A pinned toolchain and one reliable local entry point are sufficient for simpler projects. `ph-eventing` is the public reference for the more rigorous model.

## 15. Default branch and protection

### 15.1 Default branch

New repositories must use `main`.

Future documentation, workflows, examples, and release instructions should prefer `main`. Existing `master` branches are not renamed by v0.1. Any later rename must deliberately update workflows, protection, badges, links, metadata, scripts, and contribution guidance.

### 15.2 Protection profile

The default-branch protection reference profile is:

- Require one stable aggregate hosted check when an affordable hosted workflow exists.
- Require review conversations to be resolved.
- Prohibit force pushes.
- Prohibit branch deletion.
- Do not require linear history.
- Do not require signed commits.
- Do not require approving reviews for a solo-maintained repository.
- Permit maintainer or administrator bypass for recovery.
- Do not require the branch to be strictly up to date before merging.
- Permit merge, squash, and rebase methods.

Application by lifecycle:

- **Active:** protection required.
- **Maintenance:** protection required while changes are accepted.
- **Incubating:** protection enabled once reliable CI exists and required before promotion to Active.
- **Experimental:** optional.
- **Archived:** made read-only through archival status.

Private repositories are not required to consume hosted Actions merely to satisfy protection. Conversation resolution and destructive-operation protection may be enabled before a hosted status check is added.

## 16. Dependencies and supply chain

Dependencies are engineering decisions, especially in firmware.

Repositories should:

- Minimize runtime dependencies.
- Commit lockfiles where reproducible application or firmware builds benefit.
- Review dependencies for maintenance, licensing, target support, size, and runtime cost.
- Automate advisory and license checks where practical.
- Avoid unpinned Git dependencies unless the exception is documented.
- Keep dependency-update pull requests subject to normal CI and review.

“Zero dependencies” may be an intentional project constraint but is not an organization-wide requirement.

## 17. Versioning and releases

Published libraries and reusable components must:

- Use semantic versioning where practical.
- Use Git tags that identify the package and full SemVer version. A repository
  with one published package or a synchronized package set uses tags such as
  `v0.1.0` or `v0.1.0-experimental.1`. A workspace that versions published
  packages independently must document an unambiguous package-qualified form
  such as `<package>-v<semver>`.
- Maintain a changelog.
- Document the release process.
- Identify the supported toolchain or compatibility range.
- Verify the packaged artifact, not only the working tree.
- Create a GitHub Release containing the corresponding changelog section.

A GitHub Release for a SemVer prerelease must be marked as a prerelease. The
SemVer component of the release tag and the packaged version must match exactly.
A synchronized package set sharing one tag must share that version.

Before 1.0, a breaking change increments the minor version. When compatibility impact is uncertain, take the larger defensible bump.

### 17.1 Release branches

After a repository has published a package or versioned deliverable, each
substantial feature intended for a later published version under that release
boundary must be developed and reviewed on its own feature branch and pull
request. Accepted feature work must integrate into a `release/<semver>` branch
and must not enter the default branch except through that release branch's
merge-back after the verified release. This routing applies even when the
release contains only one substantial feature and does not replace Section
12.3.

This routing governs substantial feature work accepted after adoption of this
paragraph. It does not require rewriting default-branch history or reopening a
completed release. Work accepted before adoption and already present on the
default branch may enter the next release when the release record identifies
the transition; substantial work accepted afterward follows the routing above.

A `release/<semver>` branch, including the prerelease component when present,
is also required whenever multiple accepted feature PRs must be assembled into
one published version. A bounded correction, documentation-only release, or
release-machinery change represented by one independently verified PR may use a
simpler documented process only when the release contains no substantial
feature work.

References to `release/<semver>` in this section may use a documented,
unambiguous package-qualified form such as `release/<package>-<semver>` when a
workspace versions and releases published packages independently.

While a release branch accepts changes, pull requests into it must receive every
aggregate hosted check and conversation-resolution requirement applicable under
Section 15.2. Force pushes and premature deletion must be prohibited. Maintainer
or administrator bypass may remain available for recovery and for deliberate
branch deletion after release completion.

The release process should:

1. Assemble accepted changes on the release branch.
2. Open the merge-back PR as a draft early.
3. Preserve review history when routing accepted PRs.
4. Keep later work outside the release branch.
5. Apply shared fixes upstream-first.
6. Close the changelog only after release changes are assembled.
7. Freeze one exact release-candidate commit; any later change invalidates its
   release evidence.
8. Run the complete matrix against the combined release.
9. Record the evidence environment.
10. Inspect exact package and artifact contents.
11. Tag the verified release commit before irreversible publication.
12. Publish and create the GitHub Release.
13. Record the applicable publication or distribution outcome and GitHub
    Release before merge-back.
14. Merge the release branch back promptly.
15. Finalize the durable release record, reopen `Unreleased`, and remove the
    completed release branch.

The exact artifact being released—not its individual component PRs—is what must be verified.

### 17.2 Rust registry publication

This subsection applies to every organization-owned Cargo package intentionally
published to a registry, including shared capability libraries, tools, and
peripheral drivers. It applies to first releases, prereleases, and ordinary
releases regardless of repository lifecycle. An adopted organization profile
or stricter repository release contract may add claim-specific obligations, but
it must not replace or weaken this common software publication contract.

Before the first registry upload in a release, the release process must:

- Identify one clean release-candidate commit and the exact package set,
  versions, registries, and tags being released. A candidate change invalidates
  prior release evidence.
- Align each package version with its corresponding changelog heading, Git tag,
  GitHub Release identity, and any committed lockfile or release metadata that
  records it.
- Run the documented complete release-candidate invocation of the canonical
  verification entry point. Every applicable baseline check from Section 13
  and every repository-specific check designated by the release contract or
  needed for a supported release claim must run and pass. A failure, skipped
  applicable check, or indeterminate result blocks publication.
- Record the candidate commit, exact invocation, relevant environment and tool
  versions, and the result. A hosted subset or pull-request merge-result check
  must not be represented as exact-candidate release evidence.

Before uploading each selected package, the release process must:

- Run a publication dry run, then inspect and hash the resulting candidate
  `.crate` archive. Its digest identifies the inspected candidate; it does not
  by itself prove which bytes a later publication command uploads. Package
  construction, dry run, and upload must not use `--allow-dirty` or
  `--no-verify`; they use `--locked` when the repository declares its lockfile
  a release input.
- Use an upload mechanism that either transmits the inspected archive without
  reconstructing it or establishes deterministic reconstruction from unchanged
  inputs. A source-directory `cargo publish` invocation reconstructs the
  archive, even when it follows `cargo publish --dry-run`, so the dry run alone
  does not establish byte identity. The reconstruction path must use the same
  frozen candidate, Cargo version, package and registry selection, Cargo
  configuration, feature and lock options, and dependency resolution. No
  package input may change between inspection and upload, including an included
  generated or ignored file or a generated lockfile. If those controls cannot
  be established, the package must not be uploaded through a reconstructing
  client.
- Make package selection and the destination registry unambiguous in the
  documented invocation and manifest. A workspace release must not depend on
  an incidental working directory or default-member selection.
- Inspect the archive's file set, normalized manifest, README and license
  material, registry metadata, packaged links, dependency sources and version
  requirements, packaged lockfile when present, and Cargo-reported VCS metadata
  when Cargo emits it. When present, the VCS metadata must name the frozen
  candidate commit and expected repository-relative `path_in_vcs` and must not
  report a dirty worktree. Cargo documents this file as best-effort consistency
  evidence, not verified provenance. Retain a SHA-256 digest of the inspected
  candidate archive.
- Exercise supported consumer-visible claims from the packaged artifact where
  packaging can affect them, including documentation, examples, declared
  features, compatibility range, targets, or downstream consumption as
  applicable.

A workspace release must identify every package selected for publication,
every package deliberately excluded, each version and registry, internal
dependency order, and the tag or release identity associated with each
package. Each published package must satisfy the artifact checks independently.
The release process should use a workspace-aware dry run of the complete set
before the first upload when the documented release toolchain supports it.
Otherwise it must record the non-atomic partial-release risk and perform each
dependent package's construction and dry run after its predecessors are
available but before its own upload. Packages must be uploaded in dependency
order. A dependent package must not be uploaded until the registry serves the
intended dependency version named by the release record and that version
satisfies the packaged dependency requirement. Its dry run must resolve that
intended version, and the predecessor's registry artifact and checksum must be
verified before the dependent upload. Each completed upload must be recorded.
If a later package fails, stop, record the non-atomic partial release, and
resolve it without reusing or retargeting a published identity.

Every release identity must receive an annotated tag at the verified candidate
before its corresponding upload. The release process must push each tag and
resolve it back to the candidate commit before the upload begins. Canonical CI
and ordinary hosted contributor CI must not publish. Tagging, credentials,
upload, and GitHub Release creation are separately authorized release actions
performed manually by a maintainer or by a documented protected publishing
workflow bound to the verified candidate.

A publication-client timeout or ambiguous response must not be treated as proof
that no upload occurred. Before retrying, query the registry record and index
for the package and version. If publication remains uncertain, stop and record
the state rather than risk a duplicate or contradictory release action.

After upload, the release process must:

- Retrieve the registry's record and exact published archive, verify its digest
  against the inspected candidate, and repeat the material archive inspection
  required above on the published bytes. A digest mismatch means the inspected
  candidate was not the published artifact and fails release verification; a
  content inspection performed only before a reconstructing upload must not be
  attributed to the published archive. Compare Cargo-reported VCS metadata,
  when present, with the verified candidate commit as supporting evidence.
- Verify version availability and yank state, current package metadata, and
  ownership. For crates.io packages, verify the intended docs.rs result when
  documentation is part of the supported distribution surface. After a first
  publication, assign and verify every intended additional owner as soon as the
  registry permits.
- Exercise a fresh exact-version registry consumer for a reusable library when
  that check establishes supported downstream use not already proven from the
  packaged artifact.
- Create each GitHub Release from its existing tag, then complete the merge-back
  and branch cleanup in Section 17.1.
- Before merge-back, update a durable release record with the registry URL,
  published checksum, documentation and consumer results, GitHub Release, and
  every unavailable or failed post-publication check. Record the merge result
  when completing the release.

A release must not be given a GitHub Release or represented as verified until
every applicable post-publication check passes. When an irreversible upload
cannot be resolved in place, the process may close only as failed or incomplete
with the affected check and registry state recorded. Its branch may merge back
only to preserve the truthful published state and recovery work; it must not be
presented as a successful release. Correction uses a new version. A deliberate
decision to accept the release despite the failed check follows Section 19 and
must not retarget the tag or reuse the version.

A published version or tag must not be overwritten or retargeted. A correction
uses a new version; yanking a registry version does not make its identifier
reusable.

Before a package's first registry publication, the release process must also
confirm that its registry name and normalized forms are intended and available,
that publication metadata is complete, that the intended publishing principal
or team can authenticate, that at least one documented backup-owner,
registry-administrator, or registry-support recovery route is available, and
that the intended post-publication owners are named. When publication
accompanies a private-to-public visibility transition, the intended public Git
history must be reviewed for secrets and exposed identities. Installed GitHub
Apps, webhooks, deploy keys, Actions environments, stored secrets, and other
integrations whose access or exposure changes with that transition must be
reviewed. Public repository metadata, CI,
protection, and security settings must be confirmed against the lifecycle and
visibility requirements applicable under Sections 3, 14, and 15. These
transition checks need not be repeated for every later release unless the
relevant state changes.

This subsection governs publication actions performed after its adoption.
Existing registry versions, GitHub Releases, public tags, and completed release
records remain historical facts and must not be rewritten or recreated merely
to resemble this process. Existing repositories must align their documented
release process and applicable release-branch protection before their next
substantial post-publication feature cycle or registry publication, or record
an exception under Section 19.

The additional Rust, embedded, model, physical, and qualification checks in
Section 18 and adopted profiles remain claim-scoped. A repository must run them
when its release depends on those claims; their absence must not be turned into
an unrelated universal publication prerequisite.

## 18. Rust and embedded profile

Rust embedded repositories should document and enforce, as applicable:

- Pinned toolchain and minimum supported Rust version.
- `no_std`, allocation, and runtime-dependency claims.
- Supported compilation targets.
- Supported and incompatible feature combinations.
- Unsafe-code invariants and `SAFETY` rationale.
- Dependency, advisory, and license policy.
- Determinism, memory, code-size, and timing claims.
- Concurrency-specific evidence.
- Physical-device evidence and its limits.

This profile is applied proportionally. Not every project requires the verification depth used by `ph-eventing`.

## 19. Exceptions

A repository may deviate when the deviation is deliberate and documented.

The README or a linked standards section must record:

- What differs.
- Why it differs.
- Which risk or trade-off it creates.
- Whether it is temporary or intrinsic.
- Who approved it when approval is relevant.

Existing names are grandfathered under v0.1. Other historical repositories may receive staged remediation, but lifecycle, license, and honesty requirements still apply.

The organization values explicit constraints over ceremonial compliance.

## 20. Adoption

Adoption proceeds in this order:

1. Publish this standard in the organization `.github` repository.
2. Add lightweight shared issue and pull-request templates.
3. Classify every repository by Lifecycle and Domain.
4. Remediate missing licenses first.
5. Remediate descriptions and README contracts.
6. Add changelogs to non-Experimental repositories.
7. Establish canonical local CI.
8. Add bounded public CI where appropriate.
9. Apply branch protection according to lifecycle and visibility.
10. Add specialized documentation and evidence profiles proportionally.

The v0.1 rollout does not rename existing repositories or packages.

---

The shortest expression of the standard is:

> Name a repository for the narrow responsibility it owns, keep every invariant at the lowest layer capable of enforcing it, make every important claim testable, and never confuse architectural sophistication with bounded scope.
