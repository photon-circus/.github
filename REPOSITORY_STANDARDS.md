# Photon Circus Repository Standards v0.1

Status: **Adopted**

Version: **0.1.0**

Adopted: **2026-08-11 UTC**

Applies to: repositories owned by the Photon Circus GitHub organization

Photon Circus builds deterministic, bare-metal software and hardware for embedded systems, instruments, and strange machines. These standards give each repository a clear identity, a bounded responsibility, reproducible engineering evidence, and an honest maintenance posture.

They define a common floor. They do not require every experiment to become a polished product, and they do not require every repository to use the same depth of verification.

## 1. Normative language

The terms **must**, **must not**, **required**, **should**, **should not**, and **may** express the strength of a rule.

- **Must** and **required** identify an obligation.
- **Should** identifies the expected default; deviations require a documented reason.
- **May** identifies an optional practice.

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
| `hts` | Humidity and temperature sensor |
| `imu` | Inertial measurement unit |
| `mac` | Network media-access controller |
| `nor` | NOR flash memory |
| `pmon` | Digital current, voltage, and power monitor |
| `rtc` | Real-time clock/calendar |
| `touch` | Capacitive touch and proximity controller |

New tokens may be added when a real project requires them. Synonyms should not be introduced casually.

### 5.2 Shared capabilities

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
| `CHANGELOG.md` | Every non-Experimental repository |
| `CONTRIBUTING.md` | Public Incubating, Active, and Maintenance repositories |
| `SECURITY.md` | Public Active and Maintenance repositories |
| `RELEASING.md` | Published packages and versioned deliverables |
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
- Use release headings in the form `## X.Y.Z - YYYY-MM-DD`.
- Dates use UTC and ISO 8601 format.
- Organize entries under applicable headings: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`, `Documentation`, and `Known issues`.
- Mark breaking changes explicitly with `**Breaking:**`.
- Describe observable behavior and engineering consequences, not merely filenames or commit activity.
- Preserve known limitations until they are resolved.
- Move accumulated `Unreleased` entries into the release when publishing.

When a release introduces a major new feature or substantial capability, it must include a value statement immediately below the release heading. The statement explains:

1. Why the feature was added.
2. Which problem or limitation it addresses.
3. What value it provides.
4. Which important cost, constraint, or trade-off it introduces.

A list of APIs is not a substitute for a value statement.

Experimental repositories may maintain a changelog but are not required to do so. Establishing a changelog is part of leaving Experimental status.

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

### 10.1 Pre-`ph-hil` peripheral-driver profile

This profile applies to organization-owned peripheral-driver repositories and
crates that have not been published and do not yet have reviewed physical
evidence from `ph-hil`.

Before `ph-hil` qualification, a driver is a datasheet-derived executable
hypothesis. It may be developed privately or made public, but it:

- must remain `Experimental` or `Incubating`;
- must remain unpublished to crates.io, with Rust packages using
  `publish = false`;
- must state prominently that verification is against a datasheet-derived
  behavioral mock and does not constitute hardware-in-the-loop or silicon
  evidence;
- must not claim physical-device support, electrical correctness, timing
  accuracy, or silicon validation;
- must not include MCU, BSP, board, or firmware examples before hardware
  qualification;
- must not carry speculative `ph-hil` firmware, fixture definitions, plans,
  schemas, evidence policies, build shims, or capability inventories.

The pre-qualification repository should contain only the narrow driver, its
datasheet-derived behavioral mock, explicit assumptions and ambiguities,
driver-versus-mock tests, supported-target compilation, documentation, and the
ordinary repository policy required by its lifecycle.

The mock is an executable model of device-side behavior, not a second copy of
the driver. It should be implemented independently from the datasheet contract
and must not reuse driver codecs or sequencing logic in ways that make tests
tautological. CI runs the public driver against this model and establishes only
that driver changes remain compatible with the modeled behavior.

`ph-hil` qualification later compares the driver and behavioral model claims
with physical silicon. Any discrepancy must update the contract, mock, driver,
or stated limitation before qualification is accepted. Maintainer discretion,
a passing host test, compilation, or a mock result is not a substitute for this
physical evidence.

Crates.io publication and promotion to `Active` require reviewed `ph-hil`
evidence tied to the exact driver revision and supported hardware scope. This
gate is not waived because the crate is otherwise complete or useful. Existing
already-published drivers are not retroactively unpublished, but should adopt
the evidence boundary when making new support claims.

The reusable warning, minimal repository shape, CI contract, and qualification
handoff are defined in the
[`Pre-ph-hil Peripheral Driver Profile`](docs/PERIPHERAL_DRIVER_PROFILE.md).

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

Contributor reports are valuable field evidence. Documentation must remain clear about what maintainers have independently reproduced.

Changes affecting registers, timing, reset, interrupts, electrical configuration, endianness, or bus behavior should identify their evidence source. Mock or simulated behavior must not silently become a universal hardware claim.

Unresolved observations may be accepted when the change is otherwise valuable, but they must be recorded as known limitations or follow-up work.

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

Technical repositories should provide one canonical verification script, normally:

```text
scripts/ci.sh
```

The script should:

- Use a POSIX-compatible shell.
- Run on Linux and under Git Bash on Windows.
- Be the single implementation of the routine verification gate.
- Report pass, failure, and skipped checks distinctly.

Parallel Bash and PowerShell implementations of the same gate should not be maintained. A skipped check is not a passed check.

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

This is optional. A pinned toolchain and one reliable local script are sufficient for simpler projects. `ph-eventing` is the public reference for the more rigorous model.

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
- Use `vX.Y.Z` Git tags.
- Maintain a changelog.
- Document the release process.
- Identify the supported toolchain or compatibility range.
- Verify the packaged artifact, not only the working tree.
- Create a GitHub Release containing the corresponding changelog section.

Before 1.0, a breaking change increments the minor version. When compatibility impact is uncertain, take the larger defensible bump.

### 17.1 Release branches

A `release/X.Y.Z` branch is required when multiple accepted feature PRs must be assembled into one published version. A small release represented by one independently verified PR may use a simpler documented process.

The release process should:

1. Assemble accepted changes on the release branch.
2. Open the merge-back PR as a draft early.
3. Preserve review history when routing accepted PRs.
4. Keep later work outside the release branch.
5. Apply shared fixes upstream-first.
6. Close the changelog only after release changes are assembled.
7. Run the complete matrix against the combined release.
8. Record the evidence environment.
9. Inspect exact package and artifact contents.
10. Tag the verified release commit.
11. Publish and create the GitHub Release.
12. Merge the release branch back promptly.
13. Reopen `Unreleased` and remove the completed release branch.

The exact artifact being released—not its individual component PRs—is what must be verified.

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
