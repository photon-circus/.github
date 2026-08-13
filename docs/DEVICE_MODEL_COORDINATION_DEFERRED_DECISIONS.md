# Device Model Coordination Deferred Decisions

Status: **Non-normative deferred design record**

Recorded: **2026-08-13 UTC**

This record preserves coordination findings discovered while defining the
device behavioral model boundary. It prevents those findings from surviving
only in pull-request discussion while avoiding premature design of a shared
support crate, execution harness, or coordinated simulator.

The device boundary itself is described by
[`DEVICE_BEHAVIORAL_MODEL_STANDARD.md`](DEVICE_BEHAVIORAL_MODEL_STANDARD.md).
That specification governs current model responsibilities. This record governs
neither implementations nor acceptance; it is a durable handoff for questions
whose concrete requirements do not yet exist.

## How to use this record

Each deferred decision has a stable identifier, records what is already known,
names what remains deliberately undecided, and defines a trigger for reopening
the question. When a decision is eventually made, update its status to
**Decided**, link the governing artifact, and retain the original context.
When replaced, mark it **Superseded** and link its successor rather than
deleting it.

A deferred entry is reopened only when:

1. its stated trigger occurs;
2. new evidence invalidates a recorded invariant; or
3. an implementation demonstrates that the current device boundary is
   insufficient.

Preference, API familiarity, or the existence of a convenient implementation
is not by itself a reopening trigger. A proposal that reopens an entry should
identify the trigger, concrete use case, affected participants, and observable
failure of leaving the choice deferred.

Actionable work should become a linked issue once it has an owner and a
testable completion condition. This record remains the durable index after
such issues close.

## Findings that are not deferred

The following boundaries are already established by the device-model standard
and should not be relitigated as coordinator API choices:

- Device models are deterministic predictors of declared device behavior.
- Models mutate only in response to explicit, ordered external inputs and
  remain quiescent between them.
- Models consume unit-bearing relative duration and do not own or store the
  harness's absolute `now`.
- Authoritative environmental state, physical evolution, topology, routing,
  and scheduling are external concerns.
- Models do not invent noise, jitter, drift, environmental variation, or other
  physics to appear realistic.
- Transport reads and writes may have documented device effects; diagnostic
  inspection must not conceal mutation.
- Unsupported fidelity is reported honestly rather than filled with plausible
  invented behavior.
- Datasheet-derived behavior remains independently reviewable, and
  evidence-backed silicon variants do not silently overwrite the baseline or
  another supported variant.
- Device models do not reference or mutate one another.

Revising one of these findings requires a direct change to the working
specification with evidence showing why the boundary is insufficient. It is
not an incidental consequence of choosing a coordinator implementation.

## Deferred decision index

| ID | Seam | Status | Reopening trigger | Expected owner |
| --- | --- | --- | --- | --- |
| DMC-001 | Duration representation and arithmetic | Deferred | Two independently authored models must share elapsed-duration values, or one model exposes a correctness failure that cannot be represented locally | Shared support crate |
| DMC-002 | Driver-delay integration | Deferred | A reusable harness must run a timing-sensitive driver against a model | Support crate or harness adapter |
| DMC-003 | Event-boundary discovery | Deferred | Advancing one or more models over large durations is measurably incorrect or impractical without discovering the next observable boundary | Shared support crate |
| DMC-004 | Transport timing and phase granularity | Deferred | A driver-visible behavior depends on a transaction phase that the existing abstract operation cannot express | Transport contract |
| DMC-005 | Cross-device signal coupling | Deferred | A test must connect independently participating models through device outputs and applied stimuli | Coordinated simulator |
| DMC-006 | Batching, simultaneity, ordering, and settlement | Deferred | One execution must coordinate two or more events whose ordering changes an observable result | Coordinated simulator |
| DMC-007 | Topology, participation, and delegation | Deferred | A reusable execution must attach multiple models or represent switches, muxes, bridges, or routed transports | Harness topology contract |
| DMC-008 | Mutation, failure atomicity, snapshot, and rollback | Deferred | A concrete execution requires speculative application, recovery, replay, or state comparison across participants | Support crate and coordinator |
| DMC-009 | Trace and HIL comparison artifacts | Deferred | `ph-hil` or another reviewed workflow requires a common replayable model/silicon observation format | `ph-hil` protocol |
| DMC-010 | Execution-policy provenance | Deferred | Results depend on coordinator-selected timing, coupling, range, or parameter policy and must be reproduced or compared | Harness evidence contract |

## DMC-001: Duration representation and arithmetic

**Status:** Deferred

### Preserved findings

- Duration is relative, non-negative, and unit-bearing.
- A model retains device progress needed for partition-consistent evolution.
- The harness owns advancement policy; the device owns source-backed
  consequences of the supplied duration.

### Deliberately undecided

- shared duration type and range;
- integer, rational, fixed-point, or other exact representation;
- resolution, quantization, rounding, saturation, and overflow behavior; and
- conversion rules between transport, driver-delay, and device resolutions.

### Reopening trigger

Reopen when two independently authored models must exchange duration through a
shared API, or when a concrete model cannot meet its declared timing semantics
without a shared representation decision.

## DMC-002: Driver-delay integration

**Status:** Deferred

### Preserved findings

- Timing-sensitive driver-versus-model tests must route driver delay intent to
  the same external advancement mechanism that supplies model duration.
- A no-op delay provider is not valid evidence for timing-sensitive behavior.
- A device model does not implement `DelayNs`, an executor, timers, or pin
  waits on behalf of the harness.

### Deliberately undecided

- adapter traits and ownership;
- synchronous versus asynchronous integration;
- whether delay advances all participants or a declared subset; and
- how driver delay interacts with pending transport or external stimuli.

### Reopening trigger

Reopen when a reusable harness must execute a timing-sensitive driver against
at least one behavioral model.

## DMC-003: Event-boundary discovery

**Status:** Deferred

### Preserved findings

- Models must remain correct for valid duration partitions under unchanged
  stimuli.
- A model need not report internal events that have no distinct modeled
  observation.
- Optimization machinery is not required merely because coordination may
  exist later.

### Deliberately undecided

- whether models expose a next-observable-boundary query;
- whether discovery is predictive, advisory, or exact;
- representation of no-boundary and unbounded cases; and
- coordinator behavior when multiple boundaries coincide.

### Reopening trigger

Reopen when large advances across one or more real models are measurably
incorrect or impractical without event discovery.

## DMC-004: Transport timing and phase granularity

**Status:** Deferred

### Preserved findings

- Documented transaction boundaries that alter device behavior belong in the
  model's accepted abstraction.
- Device refusal and unsupported model fidelity are different outcomes.
- Already committed effects must not be silently erased when unsupported
  behavior becomes apparent later in an abstract transaction.

### Deliberately undecided

- transaction duration and phase decomposition;
- response linearization and rejection timing;
- representation of START, STOP, chip-select, repeated-start, abort, or
  partial-transfer boundaries; and
- whether a transport operation and its elapsed duration are one input or
  several ordered inputs.

### Reopening trigger

Reopen when a driver-observable, source-backed behavior depends on a transport
phase that the existing model boundary cannot express honestly.

## DMC-005: Cross-device signal coupling

**Status:** Deferred

### Preserved findings

- Devices expose outputs and accept externally supplied stimuli.
- Devices do not reference, schedule, or mutate other devices.
- Signal coupling between participating devices is distinct from hierarchical
  forwarding of a transport operation through a switch, mux, or bridge.

### Deliberately undecided

- zero-duration or delta-cycle settlement;
- positive coupling latency;
- superdense-time or other same-frontier representation;
- propagation and feedback rules; and
- how analog or electrical coupling is abstracted before becoming a device
  stimulus.

### Reopening trigger

Reopen when a concrete test must connect the output of one independently
participating model to the stimulus of another.

## DMC-006: Batching, simultaneity, ordering, and settlement

**Status:** Deferred

### Preserved findings

- Input order is part of deterministic execution provenance when it affects an
  observable result.
- The device model does not choose global ordering or publish a shared
  temporal frontier.
- Calling inputs simultaneous does not by itself define evaluation semantics.

### Deliberately undecided

- pre-state versus incrementally updated evaluation;
- tie-breaking among same-frontier actions;
- transitive propagation within a frontier;
- feedback convergence and oscillation handling; and
- commit and failure semantics across participating models.

### Reopening trigger

Reopen when a real coordinated execution contains two or more events whose
ordering or settlement changes a supported observation.

## DMC-007: Topology, participation, and delegation

**Status:** Deferred

### Preserved findings

- Board topology and model attachment are external to device-specific state.
- A switch or mux owns its documented selection behavior, not the inventory or
  physical state of downstream devices.
- A focused test can directly supply one model without creating a world
  object.

### Deliberately undecided

- participant registration and identity;
- attachment lifetime and dynamic topology;
- addressing and routing ownership;
- hierarchical transport delegation; and
- selection of which participants advance for a given external action.

### Reopening trigger

Reopen when a reusable execution must coordinate multiple attached models or
represent a routed transport path.

## DMC-008: Mutation, failure atomicity, snapshot, and rollback

**Status:** Deferred

### Preserved findings

- The semantic transition is deterministic for the same initial state and
  ordered inputs.
- The device-model standard does not prescribe in-place mutation or value
  semantics.
- Inspection represented as pure must not mutate device state.

### Deliberately undecided

- `&mut` versus value-returning transition APIs;
- copy, clone, serialization, or opaque snapshot requirements;
- rollback after participant or routing failure;
- atomic versus partially committed multi-model advancement; and
- replay guarantees.

### Reopening trigger

Reopen when a concrete coordinator requires speculative execution, recovery,
replay, state branching, or failure atomicity across participants.

## DMC-009: Trace and HIL comparison artifacts

**Status:** Deferred

### Preserved findings

- Model success is not physical evidence.
- A silicon disagreement may implicate the driver, model, source
  interpretation, contract, fixture, instrument, sample, or test
  discrimination.
- Evidence-backed corrections and variants require provenance and silicon
  identity.

### Deliberately undecided

- trace schema and serialization;
- correspondence between model inputs and physical observations;
- clock alignment, tolerances, and observation resolution;
- fixture, instrument, sample, source, and software identity fields; and
- storage, retention, and review protocol.

### Reopening trigger

Reopen when a reviewed `ph-hil` workflow or another evidence process needs a
common replayable artifact for model-versus-silicon comparison.

## DMC-010: Execution-policy provenance

**Status:** Deferred

### Preserved findings

- Coordinator-selected values are execution provenance, not hidden device
  truth.
- A documented range does not imply a probability distribution.
- Behavioral baseline or silicon-variant selection is explicit and stable for
  an execution.

### Deliberately undecided

- representation of timing, coupling, resolution, and range-selection policy;
- fixed, swept, conservative, or typical parameter selection;
- configuration validation and defaults; and
- which policy fields enter trace identity or reproducibility claims.

### Reopening trigger

Reopen when two executions must be reproduced or compared and their supported
observations depend on coordinator-selected policy.

## Origin and maintenance

This record originated from the design and adversarial review discussion on
[photon-circus/.github pull request #13](https://github.com/photon-circus/.github/pull/13).
The PR discussion remains historical evidence for why these seams were
identified; this document is the maintained index.

Add a new entry only when a finding is outside the device boundary, materially
affects future interoperability, and is not already represented by an existing
entry. Prefer refining an existing entry over creating overlapping vocabulary.
