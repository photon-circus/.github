# Changelog

All notable changes to the Photon Circus organization standards are documented in this file.

Entries under `Unreleased` are effective when merged to `main`; the heading
means that they have not yet been collected into a later numbered snapshot.

## Unreleased

Last updated: 2026-08-22 UTC

### Added

- Add an explicitly non-normative Rust xtask field guide based on three
  peripheral-driver migrations and current task-runner patterns across Rust
  technical repositories. It records cross-platform and single-entry-point
  benefits; workspace-boundary options; configuration, self-test, dependency,
  partial-run, path-safety, generated-evidence, and hosted-CI tradeoffs; observed
  failures; and a bounded migration approach without prescribing an xtask
  layout, command set, configuration format, dependency set, or migration.
- Add `env` as the peripheral-driver class token for environmental sensors that
  combine barometric pressure and temperature, with optional humidity.
- Add a non-normative peripheral-driver evidence-registry example and
  remediation guide. They demonstrate atomic documentary and device
  propositions; affirmative and located-negative observations; supporting,
  refuting, or unresolved evidence; honest undefined states; shared provenance
  with independent downstream consequences;
  demand-driven capture; scoped physical observations; permanent tombstones;
  and structural-only automation without prescribing a filename, schema,
  identifier spelling, completeness audit, or organization-wide migration.
- Add non-normative Rust peripheral-driver documentation guidance for
  proportional file decomposition, repository and package README roles, status
  disclosures, source capture, and contributor and agent documentation.
- Require a device behavioral model to say how it handles an establishing input
  that covers only part of an observable, keeping the remainder unavailable,
  reporting it distinguishably, or declaring an abstraction for it, with a
  matching anti-pattern, review prompt, template field, and brief step. This
  closes the case where a latched or set-only observable becomes partly
  source-backed and the rest is silently completed.
- Add a non-normative Rust workspace integration note for repositories that
  locally choose an unpublished model crate, covering dependency direction,
  test-side adapters, path-development-dependency policy, package verification,
  and single-declaration documentation without making that packaging required.
- Add non-normative device-model implementation resources: a procedural agent
  brief that requires the normative core and one intake/declaration template
  that graduates into existing maintained documentation.
- Add a non-normative deferred design record that preserves device-model
  coordination seams, settled boundary findings, explicit reopening triggers,
  and expected ownership without prematurely specifying a shared harness.
- Add repository-specific contribution instructions for standards and
  organization-default changes, including classification, evidence,
  documentation checks, auditor tests, and approval boundaries. These
  instructions do not add downstream repository requirements.
- Add a non-normative device behavioral model working specification that
  distinguishes an independently derived driver-test model from stubs,
  transcript fakes, simulators, integration scaffolding, and physical evidence.
- Add `switch` as the peripheral-driver class token for multi-channel digital
  bus switches, and add `ph-tca954x-switch` to the active standards-audit
  cohort.
- Add `touch` as the peripheral-driver class token for capacitive touch and
  proximity controllers, and add `ph-mpr121-touch` to the active standards-audit
  cohort.
- Add `gpio` as the peripheral-driver class token for general-purpose digital
  I/O expanders, and add `ph-mcp23x17-gpio` to the active standards-audit
  cohort.
- Add `buck` as the class token for step-down converter design and validation,
  and add `ph-mp1584-buck` to the active standards-audit cohort.
- Add `pmon` as the peripheral-driver class token for digital current,
  voltage, and power monitors, and add `ph-ina226-230-231-pmon` to the active
  standards-audit cohort.
- Public organization profile introducing Photon Circus, its engineering principles, featured projects, and adopted repository standards.
- Shared bug-report, feature-proposal, and pull-request templates that preserve bounded scope, evidence provenance, compatibility decisions, and explicit handoffs across repositories without local overrides.
- Read-only repository standards auditor producing Markdown and JSON evidence without remediation authority or GitHub write operations.
- Peripheral-driver release and evidence profile defining a proportional base
  repository, explicit validation status, additive model and physical evidence,
  and a non-speculative handoff to future shared tooling.
- Peripheral-driver bootstrap design intent (2026-08-12 UTC) defining a
  disposable feature survey, consumer-driven proposition promotion, bounded
  task packets, independent driver/model/conformance lanes, temporary workspace
  boundaries, durable artifact graduation, and the future home for reusable
  local tooling. This preserves a repeatable path from data sheet to reviewable
  driver without preloading speculative artifacts, turning uncertainty into
  maintainer work, or making self-validating implementations part of the product
  repository.
- Add a non-normative peripheral-driver evidence resource pack with a
  conditional `docs/SOURCES.toml` example, exact-byte provenance, stable
  proposition guidance, tri-state redistribution posture, explicit ownership
  boundaries, demand-driven physical evidence, and legacy-contract remediation.

### Changed

- Clarify that the live `main` branch is the adopted authority, that normative
  changes take effect on merge, and that `Unreleased` means not yet collected
  into a later numbered snapshot. Rename the `0.1.0` header metadata as a
  numbered baseline so it is not mistaken for the full current contents.
- Tighten technology-neutral canonical-verification guidance around documented
  invocation scope, working-directory support, partial profiles, aggregate
  success, skipped or indeterminate work, fail-fast summaries, and the exact
  release-candidate invocation.
- Require an ordinary peripheral-driver software release to rest on a passing,
  documented release-candidate invocation of the canonical CI entry point that
  includes every applicable check in the profile's CI contract, rather than on
  any passing canonical-CI run. Declare the Peripheral Driver Release and
  Evidence Profile an adopted normative profile in its own header so its
  obligations are not read as guidance.
- Broaden the non-normative xtask field guide to Rust technical repositories,
  including reusable capability libraries, and add current organization-pattern
  review, task-command classification, side-effect boundaries, alias bootstrap
  and root identity, runner self-verification, generated-evidence finalization,
  and copied-tooling maintenance choices without prescribing an xtask layout or
  requiring implementation migrations.
- Treat every structurally detected local-CI candidate as manual review rather
  than presenting `scripts/ci.sh` filename presence as standards compliance.
  Discover nested `*/xtask/Cargo.toml` candidates and report exact paths so
  operational tools and thin launchers can be distinguished during review.
  Distinguish missing or unrecognized Domain metadata from a valid nontechnical
  classification when audit applicability depends on Domain.
- Make the canonical-local-CI requirement technology-neutral: a technical
  repository still has one documented implementation with honest outcomes, but
  it may expose a POSIX script, `cargo xtask ci`, or another justified local
  entry point. Align driver documentation and contribution examples, and teach
  the read-only structural auditor to surface conventional Cargo xtask paths for
  semantic review instead of treating the absence of `scripts/ci.sh` as a
  failure. This does not make xtask or any xtask architecture an organization
  requirement.
- Normatively require every applicable retained device or documentary
  proposition consumed by driver behavior, model behavior, conformance,
  physical evidence, or bug disposition to have one permanent identifier
  resolving to a stable referent and to exact provenance for retained evidence.
  Downstream artifacts share that identity while owning
  their interpretations independently; the normative behavioral-model standard
  now requires shared proposition identity without shared implementation or
  execution-artifact identity. A checkbox, review owner, or promise such as
  `maintainer will validate` is not evidence and cannot establish a claim. The
  rule applies prospectively and on touch; it creates no retrospective
  completeness audit or release block.
- Non-normatively align the peripheral-driver bootstrap, documentation guide,
  model aids, and resource pack around demand-driven proposition capture and the
  distinction between supporting, refuting, unresolved, and undefined evidence.
  An unconsumed source fact creates no maintained artifact, and an unsupported
  model behavior may remain honestly unsupported until a current consumer has a
  feasible discriminating question.
- Withdraw the non-normative hardware-contract TOML example whose approval
  states and owner-review fields could turn missing evidence into maintainer
  work. Replace it with the smaller Markdown evidence example. Existing
  contracts may be remediated in place when a proposition is touched or the
  contract is already causing contradictory claims; this change requires no
  organization-wide migration or completeness audit.
- Make the inherited root contribution and security files safe organization-wide
  fallbacks that defer to repository-local guidance, preserve the
  standards-repository workflow in a dedicated guide, and provide a safe
  bootstrap when a private security-reporting channel is not yet advertised.
- Clarify in the required-files table and peripheral-driver profile that
  publishing a package or shipping another versioned deliverable triggers
  repository-level `CHANGELOG.md` and `RELEASING.md` requirements, including for
  Experimental repositories. This organization baseline does not itself require
  those files in a distributed archive and does not override stricter
  repository-specific release contracts. Make the auditor treat missing
  publication-triggered documents as a `MANUAL_REVIEW` surface when lifecycle
  alone cannot determine applicability.
- Separate peripheral-driver distribution, software maturity, and evidence so
  publication does not imply hardware qualification. Replace the blanket
  crates.io prohibition with intentional prerelease and ordinary software
  release paths; require lifecycle-matching prerelease metadata from a new
  driver's initial version, an explicit migration for existing `0.1.0`
  manifests, nondecreasing lifecycle transitions, release-document obligations
  for every published artifact, and a release-CI version check. Make model
  conformance, physical observation, and `ph-hil` qualification conditional,
  claim-scoped concerns rather than existence or publication gates. Assign
  distinct oracle ownership to driver unit tests, scripted transport tests,
  device-model tests, driver-versus-model conformance, and `ph-hil`, while
  preserving DMC-009's deferred identity and comparison-artifact boundary.
- Refine the non-normative device-model implementation and review aids to
  require source-domain checks for minimum-trace values, explicit pre-frontier
  assertions and duration totals in temporal partition tests, and review of
  redundant lifecycle/status representations. These prompts address concrete
  false-pass and model-auditability failures without prescribing a support
  library, DSL, state-machine representation, or coordinator API.
- Clarify that deterministic device models must not invent convenient
  observable initial values when sources declare no reset value, and that the
  accepted input domain includes operation shapes, values, and field
  combinations which must be validated before dependent effects are committed.
  Require callable adapters to preserve ordinary model limitations rather than
  panic or fabricate a device response. Refine the non-normative implementation
  brief, declaration prompts, anti-patterns, and review questions around a
  minimum useful execution trace, explicit initialization, rejection
  boundaries, and proportional discrimination evidence. These refinements are
  supported by the first VEML7700 model exercise.
- Adopt the responsibility, fidelity, independence, validation, and source
  boundaries of the former device behavioral model working specification as a
  normative core while retaining its rationale, examples, anti-patterns, and
  review prompts as non-normative guidance. Add implementation guardrails
  learned from the first simple-model smoke test: packaging does not define
  independence; conformance consumers may depend on both implementations;
  persistent stimulus levels are idempotent; model limitations remain distinct
  from device refusals; source-undeclared sequences are not invented; and
  model, adapter, documentation, and policy complexity remains proportional to
  current behavioral value. Define the normative core as an inherited decision
  set for independently acting contributors and AI agents, including an
  evidence-based admission test and an escalation path when a settled or
  deferred boundary proves insufficient.
- Refine the device behavioral model working specification: the model is an
  explicit-input sink that consumes relative duration and applied stimuli
  without owning world time, environmental truth, topology, or orchestration;
  shared semantic boundaries make models useful in focused CI before a common
  coordinator exists; coordinator APIs remain deferred; and evidence-backed
  silicon variants preserve observed differences without silently overwriting
  the datasheet baseline or another supported variant.
- Update the active audit cohort for the pre-publication rename from
  `ph-ads1115-adc` to `ph-ads1x15-adc`.

## 0.1.0 - 2026-08-11

**What this release delivers.** This first standards release gives Photon Circus repositories a shared language for bounded scope, lifecycle, naming, documentation, licensing, contributions, feature development, verification, CI, branch protection, and releases. It was created so strong local engineering can remain maintainable as the organization grows, while allowing experiments to stay honest experiments and requiring supported work to carry reproducible evidence.

### Added

- Repository Lifecycle and Domain classifications.
- Bounded-scope and invariant-ownership principles.
- Prospective `ph-` naming and peripheral-driver class tokens.
- README, documentation, changelog, and licensing requirements.
- MIT as the default license with justified Apache-2.0 exceptions.
- Contribution and hardware-evidence guidance.
- Feature proposal, independent-PR, and first-class rejection practices.
- Local-first CI for private repositories and bounded hosted CI for public releases.
- `main` as the default for future repositories, with existing branch names grandfathered.
- Lifecycle-sensitive branch protection, release, and adoption rules.

### Known issues

- Organization-wide templates, property assignment, repository audits, and ruleset rollout remain follow-up adoption work.
