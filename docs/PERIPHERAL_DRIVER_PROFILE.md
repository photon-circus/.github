# Peripheral Driver Release and Evidence Profile

This profile lets a Photon Circus peripheral driver become coherent, testable,
useful, and publishable without making unfinished models, physical tooling, or
shared integration contracts prerequisites for its existence or release.

It separates distribution, software maturity, and evidence. Requirements attach
to the claims and artifacts that actually exist. Model conformance, physical
observation, hardware qualification, and `ph-hil` integration are parallel,
additive concerns; missing coverage limits the affected claim rather than the
whole crate.

## Independent status dimensions and initial version

Each driver reports three dimensions independently:

- **Distribution:** unpublished, explicit SemVer prerelease, or ordinary
  release.
- **Software maturity:** `Experimental`, `Incubating`, `Active`, `Maintenance`,
  or `Archived`.
- **Evidence:** implementation-tested, model-conformant, physically observed,
  or qualified behavior, scoped to named operations or claims.

Publication does not imply model conformance, physical observation, hardware
qualification, or lifecycle promotion.

Every newly created Rust peripheral-driver package must begin with a manifest
version whose prerelease identifier matches its lifecycle, normally:

```toml
version = "0.1.0-experimental.1"
```

or:

```toml
version = "0.1.0-incubating.1"
```

This applies even when `publish = false`. CI must check the declared prerelease
state; the version string records policy but does not mechanically prevent an
ordinary publication by itself.

An existing unpublished package with an ordinary local version such as `0.1.0`
must replace it with `0.1.0-experimental.1` or the lifecycle-matching
equivalent before its first durable release. If `0.1.0` was already tagged or
published, it remains grandfathered rather than being relabeled. Any later
prerelease must use a higher numeric core such as `0.1.1-experimental.1`; any
later ordinary release follows the software release gate below. A lifecycle
transition must not decrease SemVer precedence.

It may produce a tagged release, packaged crate artifact, or crates.io
publication identified as an Experimental or Incubating prerelease. Publishing
reserves the crate name, enables explicit opt-in dependency evaluation, and
invites collaboration. It does not authorize a physical-device support claim or
elevate the validation status.

For Rust crates not intentionally distributed through a registry, the package
manifest contains:

```toml
publish = false
```

For an intentional crates.io prerelease, the manifest may additionally name the
registry explicitly:

```toml
version = "0.1.0-experimental.1"
publish = ["crates-io"]
```

Identifiers such as `experimental.N` and `incubating.N` communicate lifecycle;
the three-part numeric core remains required. A version such as `0.1.0` has no
prerelease component and is not an experimental publication merely because its
major version is zero. Removing the prerelease component is an intentional
software-release transition governed by the release gate below, not a
hardware-qualification claim.

## Required public warning

The packaged README and crate-level documentation place a status disclosure near
the status or usage introduction. It reports facts rather than a hypothetical:

> [!WARNING]
> **Lifecycle:** *Experimental, Incubating, or the current value*.
> **Distribution:** *unpublished, crates.io prerelease with exact version, or
> ordinary crates.io release with exact version*.
> **Model conformance:** *none, or the exact covered operations and important
> limitations*.
> **Physical evidence:** *none, physically observed scope, or the exact reviewed
> qualification and silicon scope*.
> Evidence and limitations apply only to the named operations; publication does
> not imply hardware qualification.

The disclosure may use prose, but it must preserve those facts. Complete model
coverage may name the declared supported public surface as a whole. Partial
coverage must name covered and uncovered operations or link to a packaged
coverage or limitations section. A link to an unpackaged issue or private record
is insufficient. Grandfathered ordinary releases report their actual version;
they must not claim to be available only as prereleases.

## Minimum repository shape

The minimum repository contains only what establishes its current driver
contract:

- the narrow driver implementation;
- stable proposition identifiers as they become applicable under the
  [organization evidence rule](../REPOSITORY_STANDARDS.md#102-stable-device-propositions),
  without a speculative inventory or retrospective migration of untouched
  legacy facts;
- implementation-focused unit and scripted transport tests appropriate to the
  code that exists;
- supported-target compilation;
- one canonical local CI entry point;
- lifecycle-appropriate README, changelog, license, contribution, security,
  release guidance, and agent guidance.

Publishing a package, or shipping any other versioned deliverable, triggers the
changelog and release-documentation requirements of the organization release
standard, including when the repository remains Experimental.

This requirement applies to the **repository**. The repository must contain
`CHANGELOG.md` and `RELEASING.md`. This profile does not require either file to
be included in a `.crate`, wheel, or other distributed archive. Their absence
from such an archive is not, by itself, a violation of this profile; a
repository-specific release contract may separately require archive inclusion.

MCU applications, board examples, firmware, models, fixtures, and other
integration artifacts are optional. Admit them when they add current bounded
value, label their evidence limits, and keep them outside the driver's
responsibility where appropriate. Do not add placeholder execution plans,
capability inventories, evidence policies, schemas, build hooks, or generated
pack validators merely to anticipate future `ph-hil` integration.

Temporary implementation roles and work packets belong in GitHub issues, not
committed agent-persona directories.

An independently implemented datasheet-derived behavioral model, model tests,
and tests that exercise the public driver through that model are the next
additive layer. They are required before the corresponding public operations
are described as model-conformant, but incomplete modeling does not block an
honestly labeled prerelease or ordinary software release. Coverage and
limitations are recorded per public operation or claim rather than implied for
the whole crate.

## Behavioral mock contract

The mock represents the device side of the abstract transport. It is derived
from the datasheet contract independently from the driver and should model the
observable state transitions needed to test supported operations.

When present, behavioral models used under this profile must conform to the
normative sections of the
[Device Behavioral Model Standard](DEVICE_BEHAVIORAL_MODEL_STANDARD.md). Its
remaining sections provide non-normative rationale and review guidance.

The mock must not reuse driver encoding, decoding, or sequencing logic where
doing so would cause the driver and oracle to repeat the same defect. Shared
types may be appropriate when they express public values; shared implementation
of the behavior being tested is not.

Mock fidelity and non-goals are explicit. Common non-goals include analog
behavior, oscillator tolerance, electrical timing, supply thresholds, pin
loading, undocumented reset behavior, and board topology.

## CI contract

Driver CI establishes only the software claims for the validation layers
currently present. Every repository should:

1. format and lint with warnings treated as failures;
2. test pure codecs and error paths;
3. test focused transaction construction, sequencing, and injected transport
   failures where applicable;
4. compile documented features and supported bare-metal targets;
5. build documentation;
6. audit dependencies and licenses where applicable;
7. verify that a release candidate's manifest version matches its declared
   prerelease or ordinary distribution state; and
8. construct and inspect the package without publishing it.

The version check is required, but this profile does not prescribe a shared
manifest-metadata schema or repository-local script. A prerelease candidate must
fail its release gate when the package version lacks the intended prerelease
component. Registry publication remains outside ordinary CI and requires the
documented maintainer-controlled release process.

Fixed datasheet-derived vectors in driver tests establish only the named local
transformation. Unit and scripted transport tests must not emulate device state
or be presented as model conformance merely because an independent behavioral
model is not yet available.

When a behavioral model exists, CI should additionally test the model's own
declared behavior and run every public driver operation claimed as
model-conformant against it. Model conformance is not required to exercise
implementation-only branches that are more honestly covered by unit or
scripted transport tests.

Passing CI means only that the validation layers named by the repository remain
green. When model conformance is present, it means the covered driver claims
remain compatible with the declared behavioral model. It does not mean the
model matches silicon.

## Conditional surface provided to `ph-hil`

The driver repository gives future `ph-hil` work a bounded, non-speculative
surface:

- the public driver operations and stated guarantees;
- the behavioral model and its fidelity boundary, when present;
- deterministic model-conformance cases and expected observations, when
  present;
- named datasheet sources and inferred behavior;
- unresolved ambiguities and physical-only claims;
- supported target and feature scope.

`ph-hil` owns physical execution, fixture, evidence, and assessment mechanics
when that integration is adopted. The driver repository owns its claims and
semantic procedures. Do not invent those contracts independently in each
driver.

Model and physical procedures that address the same device proposition cite the
same stable proposition identifier. They need not share a procedure, case or
trace identity, adapter, test binary, implementation, serialization schema, or
comparison artifact. Correspondence between those execution artifacts remains
deferred by [DMC-009](DEVICE_MODEL_COORDINATION_DEFERRED_DECISIONS.md); stable
proposition identity does not.
When a repository adopts a reviewed `ph-hil` contract, it follows that
contract's catalogue authority rather than creating a parallel inventory.

## Software publication gate

Intentional publication of any registry version triggers Sections 7 and 17 of
the organization standards regardless of lifecycle. A published prerelease uses
the full SemVer prerelease in its package version, Git tag, changelog heading,
and release identity, and its GitHub Release is marked as a prerelease.

An ordinary release is a software distribution decision. Before publishing a
version without a prerelease component, the repository must have:

- a bounded public API, documented limitations, and accurate lifecycle and
  evidence status;
- implementation-focused tests and supported-target compilation proportional
  to the driver;
- a passing canonical CI entry point;
- a changelog and documented release process; and
- a verified packaged artifact assembled through an intentional maintainer
  release action.

An ordinary release does not require a complete behavioral model, physical
evidence, hardware qualification, `ph-hil` availability, or `ph-hil` adoption.
It must not be described as establishing any of those claims. Registry versions
are permanent and cannot be overwritten, so prerelease and ordinary publication
remain deliberate release decisions rather than automatic CI side effects.

## Conditional evidence and qualification

Additional validation is claim-scoped:

- model-conformant operations require an independent model whose accepted
  domain covers those operations;
- physically observed behavior requires reviewed evidence identifying the exact
  driver revision, device, conditions, fixture, tools, and observation scope;
- a `ph-hil`-qualified claim additionally requires reviewed `ph-hil` evidence
  satisfying the adopted contract; and
- where model and silicon evidence disagree, the affected model, driver,
  contract, selected silicon variant, or limitation must be reconciled before
  either result supports that claim.

Publication and lifecycle promotion do not silently elevate evidence status.
Hardware qualification is not a prerequisite for publication, and lack of one
optional validation layer does not erase narrower evidence or block unrelated
claims.

An undefined proposition creates no hardware-validation assignment or release
gate. Optional bounded confirmation may be admitted for a named proposition;
only a dependent physical or qualification claim can require that evidence.
