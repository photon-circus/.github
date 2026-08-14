# Pre-`ph-hil` Peripheral Driver Profile

This is the reusable development profile for Photon Circus peripheral drivers
that do not yet have reviewed physical evidence, whether unpublished or
intentionally distributed as explicit SemVer prereleases.

Its purpose is to let a driver become coherent, testable, and publicly
inspectable without blocking on a speculative hardware-in-the-loop system or
pretending that a host model proves silicon behavior. Driver implementation,
behavioral-model conformance, and physical evidence are progressive,
claim-scoped layers; absence of a later layer limits claims rather than forcing
an earlier layer to implement speculative scaffolding.

## Status contract

A pre-qualification driver:

- is `Experimental` or `Incubating`;
- may be private or public in the Photon Circus organization;
- is either not published to a registry or is published only with an explicit
  SemVer prerelease identifier;
- has no MCU, board, BSP, or firmware example;
- makes no hardware-in-the-loop, electrical, timing, or silicon-support claim.

A newly created Rust package begins with a manifest version whose prerelease
identifier matches its lifecycle, normally:

```toml
version = "0.1.0-experimental.1"
```

or:

```toml
version = "0.1.0-incubating.1"
```

This applies even when `publish = false`. It keeps the package metadata honest
from its first build and prevents an ordinary version from being published
before its qualification boundary was recorded. Every later pre-qualification
manifest and registry version retains a prerelease component; changing the
numeric core does not bypass the gate.

It may produce a tagged release, packaged crate artifact, or crates.io
publication identified as an Experimental or Incubating prerelease. Publishing
reserves the crate name, enables ordinary dependency-based evaluation, and
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
major version is zero. Removing the prerelease component is the explicit
ordinary-release transition and requires the qualification gate below.

## Required public warning

The repository README and crate-level documentation place a warning near the
status or usage introduction that reports the validation actually achieved. A
driver with model-backed conformance may use:

> [!WARNING]
> **Incubating — datasheet-model verification only.**
> This driver is verified against an independent behavioral mock derived from
> documented datasheet behavior. It does not yet have reviewed `ph-hil` evidence
> from physical silicon and must not be treated as hardware-qualified. If
> published, it is available only as an explicit SemVer prerelease while this
> verification remains incomplete.

An Experimental repository substitutes **Experimental** without weakening the
rest of the warning.

A driver that does not yet have a behavioral model must not use the preceding
warning. It uses an equally prominent narrower warning, adapted for lifecycle
and device:

> [!WARNING]
> **Incubating — implementation validation only.**
> This driver has software tests for its implementation but has not yet been
> verified against an independent device behavioral model or reviewed `ph-hil`
> evidence from physical silicon. If published, it is available only as an
> explicit SemVer prerelease and must not be treated as datasheet-conformant or
> hardware-qualified.

## Minimal repository shape

The initial pre-qualification repository contains only what establishes the
implemented driver contract:

- the narrow driver implementation;
- explicit datasheet revisions, interpretations, assumptions, and ambiguities;
- implementation-focused unit and scripted transport tests appropriate to the
  code that exists;
- supported-target compilation;
- one canonical local CI entry point;
- lifecycle-appropriate README, changelog, license, contribution, security,
  release-lock, and agent guidance.

It does not bootstrap future `ph-hil` internals. Do not add placeholder firmware,
MCU applications, fixture definitions, bench files, execution plans, capability
inventories, evidence policies, schemas, build hooks, or generated pack
validators merely to anticipate the future integration.

Temporary implementation roles and work packets belong in GitHub issues, not
committed agent-persona directories.

An independently implemented datasheet-derived behavioral model, model tests,
and tests that exercise the public driver through that model are the next
additive layer. They are required before the corresponding public operations
are described as model-conformant, but incomplete modeling does not block an
honestly labeled driver-only prerelease. Coverage and limitations are recorded
per public operation or claim rather than implied for the whole crate.

## Behavioral mock contract

The mock represents the device side of the abstract transport. It is derived
from the datasheet contract independently from the driver and should model the
observable state transitions needed to test supported operations.

When present, behavioral models used under this profile must conform to the normative
sections of the
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

Pre-qualification CI establishes only the software claims for the validation
layers currently present. Every repository should:

1. format and lint with warnings treated as failures;
2. test pure codecs and error paths;
3. test focused transaction construction, sequencing, and injected transport
   failures where applicable;
4. compile documented features and supported bare-metal targets;
5. build documentation;
6. audit dependencies and licenses where applicable;
7. construct and inspect the package before any publication.

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

## Surface provided to `ph-hil`

The driver repository gives future `ph-hil` work a bounded, non-speculative
surface:

- the public driver operations and stated guarantees;
- the behavioral model and its fidelity boundary, when present;
- deterministic model-conformance cases and expected observations, when
  present;
- named datasheet sources and inferred behavior;
- unresolved ambiguities and physical-only claims;
- supported target and feature scope.

`ph-hil` owns the later physical execution, fixture, evidence, and assessment
format. The driver repository owns its claims and semantic procedures. Those
contracts are added when the `ph-hil` product defines them, not invented
independently in each driver. Reuse the semantic meaning of an existing
model-conformance case where practical, but do not require the host and physical
paths to share an adapter, test binary, or implementation. Once adopted, the
exact-major `ph-hil` capability contract is the sole behavioral case catalogue.

## Qualification and publication gate

Before crates.io publication of a version without a SemVer prerelease component
or promotion to `Active`:

- `ph-hil` must exercise the supported driver claims against physical silicon;
- evidence must identify the exact driver revision, device, carrier, fixture,
  tool versions, and test scope;
- model-versus-silicon discrepancies must be resolved in the mock, driver,
  contract, or documented limitation;
- the reviewed evidence record must be linked from the repository;
- the release artifact and changelog must be verified after the evidence-bound
  changes are assembled.

There is no documentation-only or maintainer-approval override for this gate.
The driver may remain public and useful—including through an explicit SemVer
prerelease—as Experimental or Incubating while the qualification work is
unavailable. Registry versions are permanent and cannot be overwritten, so a
prerelease publication remains an intentional release decision rather than an
automatic CI side effect.
