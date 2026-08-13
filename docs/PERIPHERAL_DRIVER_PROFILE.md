# Pre-`ph-hil` Peripheral Driver Profile

This is the reusable development profile for unpublished Photon Circus
peripheral drivers that do not yet have reviewed physical evidence.

Its purpose is to let a driver become coherent, testable, and publicly
inspectable without blocking on a speculative hardware-in-the-loop system or
pretending that a host model proves silicon behavior.

## Status contract

A pre-qualification driver:

- is `Experimental` or `Incubating`;
- may be private or public in the Photon Circus organization;
- is not published to crates.io;
- has no MCU, board, BSP, or firmware example;
- makes no hardware-in-the-loop, electrical, timing, or silicon-support claim.

For Rust crates, the package manifest contains:

```toml
publish = false
```

This is a qualification lock, not merely protection against accidental early
publication. It remains in place until reviewed `ph-hil` evidence satisfies the
publication gate.

## Required public warning

The repository README and crate-level documentation place this warning near the
status or usage introduction, adapted only for the lifecycle name and device:

> [!WARNING]
> **Incubating — datasheet-model verification only.**
> This driver is verified against an independent behavioral mock derived from
> documented datasheet behavior. It does not yet have reviewed `ph-hil` evidence
> from physical silicon, is not published to crates.io, and must not be treated
> as hardware-qualified.

An Experimental repository substitutes **Experimental** without weakening the
rest of the warning.

## Minimal repository shape

The pre-qualification repository contains only what establishes the modeled
driver contract:

- the narrow driver implementation;
- an independently implemented datasheet-derived behavioral mock;
- explicit datasheet revisions, interpretations, assumptions, and ambiguities;
- tests that exercise the public driver through the mock transport;
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

## Behavioral mock contract

The mock represents the device side of the abstract transport. It is derived
from the datasheet contract independently from the driver and should model the
observable state transitions needed to test supported operations.

Behavioral models used under this profile must conform to the normative
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

Pre-qualification CI establishes only modeled software claims. It should:

1. format and lint with warnings treated as failures;
2. test pure codecs and error paths;
3. run the public driver against the behavioral mock;
4. compile documented features and supported bare-metal targets;
5. build documentation;
6. audit dependencies and licenses where applicable;
7. construct and inspect the package without publishing it.

Passing CI means the driver remains compatible with the declared behavioral
model. It does not mean the model matches silicon.

## Surface provided to `ph-hil`

The driver repository gives future `ph-hil` work a bounded, non-speculative
surface:

- the public driver operations and stated guarantees;
- the behavioral model and its fidelity boundary;
- deterministic test cases and expected observations;
- named datasheet sources and inferred behavior;
- unresolved ambiguities and physical-only claims;
- supported target and feature scope.

`ph-hil` owns the later physical execution, fixture, evidence, and assessment
format. Those contracts are added when the `ph-hil` product defines them, not
invented independently in each driver.

## Qualification and publication gate

Before crates.io publication or promotion to `Active`:

- `ph-hil` must exercise the supported driver claims against physical silicon;
- evidence must identify the exact driver revision, device, carrier, fixture,
  tool versions, and test scope;
- model-versus-silicon discrepancies must be resolved in the mock, driver,
  contract, or documented limitation;
- the reviewed evidence record must be linked from the repository;
- the release artifact and changelog must be verified after the evidence-bound
  changes are assembled.

There is no documentation-only or maintainer-approval override for this gate.
The driver may remain public and useful as Experimental or Incubating while the
qualification work is unavailable.
