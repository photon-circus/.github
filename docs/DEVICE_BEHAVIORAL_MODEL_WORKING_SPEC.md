# Device Behavioral Model Working Specification

Status: **Non-normative working specification**

Recorded: **2026-08-12 UTC**

Last revised: **2026-08-13 UTC**

This document supplies vocabulary and design guidance for the executable model
commonly called a *driver mock*. It is not an organization standard, audit
input, publication gate, or claim of hardware qualification. It does not
override a repository contract, the normative organization standards, or a
pinned vendor source. It is expected to change as the organization gains
experience building and qualifying drivers.

## 1. Preferred term and working definition

The preferred durable term is **device behavioral model**. *Driver mock* is
acceptable shorthand, but can misleadingly suggest that the driver itself is
being mocked. The driver is the system under test; the model represents the
device side of its abstract transport boundary.

The organization standards' terms **behavioral mock** and **behavioral model**
refer to this same artifact; **device behavioral model** is the preferred
durable name used by this working specification.

A device behavioral model is an independently derived, deterministic,
executable predictor of source-declared device behavior observable through the
operations supported by the driver. Given an explicitly selected behavioral
claim, transport operations, applied stimuli, and elapsed duration, it produces
device state, responses, and outputs without inventing physics, environmental
reality, or autonomous variation.

It is intentionally a cheap peripheral predictor for CI, not a complete
simulator. Its boundary should remain usable by a focused test helper and by
future external temporal coordination without requiring the device's
behavioral logic to be redesigned.

It exists to make a datasheet interpretation executable and reviewable before
physical evidence is available. Passing driver-versus-model tests establishes
compatibility with that model only. It does not establish correctness on
silicon.

## 2. What the model is for

The model can challenge whether the driver correctly handles:

- protocol framing, addresses, commands, and transaction boundaries;
- encoding and decoding of documented fields;
- reset values, register or memory state, and access restrictions;
- documented state transitions and operation sequencing;
- read-clear, write-one-to-clear, latching, and similar semantics;
- documented status, fault, busy, and error behavior; and
- deterministic time-dependent behavior when time is part of the digital
  contract.

The useful question is not whether the model resembles the implementation. It
is whether an independently implemented driver can interact truthfully with the
documented device contract represented by the model.

## 3. What the model is not

A device behavioral model is not:

- a second implementation of the driver;
- a queue of expected bus calls tailored to the current driver;
- a stub that returns canned success values;
- a complete simulator, emulator, digital twin, or model of device physics;
- an MCU, board-support package, firmware example, or integration harness;
- a host-side world clock, scheduler, or virtual-time kernel;
- hardware-in-the-loop evidence or a substitute for `ph-hil`;
- an assertion about undocumented silicon behavior;
- proof of electrical, analog, timing, performance, safety, or board-level
  correctness; or
- an infallible oracle. It remains a testable hypothesis derived from sources.

A scripted transport fake can still be useful for a focused unit test, and
reference vectors can still be useful for validating codecs. Neither artifact
becomes a device behavioral model merely because the driver passes against it.

## 4. Observation boundary

The model accepts operations at the same abstract transport boundary used by
the driver and returns only behavior that the driver could observe there. It
may also accept explicit, deterministic injections for events originating
outside that boundary.

Examples include:

- injecting a raw conversion result rather than simulating temperature,
  luminance, pressure, or electrode physics;
- stepping logical time by a duration rather than sleeping on wall time;
- injecting a documented fault rather than reproducing an electrical cause;
  and
- exposing an interrupt state as device behavior without owning a GPIO driver,
  executor, or application response.

Transaction boundaries that alter documented behavior, such as an I2C STOP or
chip-select transition, belong in the model. Concrete buses, pins, DMA,
scheduling, retries, and product policy do not.

### Minimal compatible sink

A device behavioral model is a deterministic state machine driven by explicit
inputs from outside the model. Its useful input categories are:

1. **Transport operations** at the same abstract boundary used by the driver.
2. **Applied stimuli** at the device boundary, such as supply availability,
   sensing-element temperature, an available raw sample, or a pending fault.
3. **Relative elapsed duration** under the currently applied stimuli.
4. **Behavioral selection**, identifying the datasheet-derived baseline or an
   evidence-backed silicon variant whose claim this execution evaluates.

Behavioral selection is explicit execution provenance. It may be fixed when a
model is constructed rather than delivered as a temporal input, but CI must not
change it implicitly.

For the same initial state and the same ordered inputs, the model produces the
same state transitions, transport responses, and device outputs. It remains
quiescent between inputs: it does not consult wall time, poll shared state, run
background evolution, introduce random variation, or lazily catch up during an
unrelated operation.

Conceptually:

```text
(next state, response, outputs) =
    transition(behavioral selection, current state, ordered execution inputs)
```

This notation does not prescribe a Rust trait, mutation style, trigger type, or
whether a future coordinator supplies transport, stimulus, and duration
separately or together. Those are API and harness decisions. The compatibility
requirement is that the device does not originate or hide them.

### Relative time and temporal validity

A model accepts non-negative, unit-bearing **relative duration** when documented
device behavior depends on elapsed time. It does not accept or store a
harness-owned absolute `now`, infer elapsed time from host execution, or decide
how long a transport operation or external action costs.

The model may retain device state required by the datasheet, such as
`busy_remaining`, oscillator phase, conversion progress, countdowns, or
fractional remainder. Those values describe the device's progress; they are not
a copy of a world-time coordinate.

Under unchanged applied stimuli, different valid partitions of the same elapsed
duration should be observationally equivalent at the model's declared
boundary. This does not require reporting or individually iterating internal
events that have no distinct modeled observation. The model must retain enough
relative progress to honor its declared timing abstraction.

The concrete duration representation, resolution, rounding policy, overflow
behavior, and event-discovery surface remain future shared-API decisions. A
model may use arithmetic, retained phase, bounded iteration, or another honest
implementation appropriate to its purpose. A future event-discovery API may
reduce coordination cost, but is not required for temporal correctness within
the model.

A focused test may advance one model directly. A future coordinated simulator
may advance several participating models against a shared temporal frontier.
The device boundary must support both without alteration. In particular:

- the model does not own advancement policy, event ordering, or a scheduler;
- it does not assume it is the only time-aware device in an execution;
- driver-requested delays must be capable of reaching the same external
  advancement mechanism as other elapsed duration; and
- the model does not implement `DelayNs`, timers, or pin waits on behalf of the
  harness.

A no-op driver delay provider invalidates timing-sensitive driver-versus-model
tests. It can make conversions appear to complete only after unrelated
transport activity, or make insufficient-wait defects pass for reasons that do
not reflect the driver's requested delay. A focused test must therefore route
driver delay intent into its explicit duration input; a future shared harness
must preserve that same semantic path.

This specification does not decide whether every external action has a modeled
cost, how simultaneous actions are represented, how a transaction is divided
into phases, or how a shared frontier is committed. It requires only that those
decisions remain outside device-specific behavioral logic.

Harness reference time, device oscillator state, and device-visible time remain
distinct. An RTC calendar may stop, drift, wrap, reset, or be written backward
while an external coordinator's temporal progression remains monotonic.

### Harness-owned environment and applied stimuli

The external test or harness owns the **authoritative environmental state** for
an execution. That may be a sophisticated shared-world model or merely a test
supplying deterministic values. The device model receives only the narrow
**applied stimuli** relevant at its boundary.

A model may retain the last applied value of a persistent stimulus so it can
evolve under that value. It does not decide when the stimulus changes,
extrapolate its physical trajectory, derive a global environment, or propagate
conditions directly to another device.

For example, a temperature-sensor model may accept a sensing-element
temperature or a completed raw conversion. It owns its documented sampling,
conversion timing, quantization, filtering, register, and interrupt behavior.
It does not own ambient temperature, airflow, thermal coupling, self-heating,
or future physical evolution unless a specific source-backed effect is
deliberately included in its declared fidelity.

The device's measurement state may differ from current environmental truth. A
sensor can continue to report its previous completed conversion after an
applied temperature changes. Two sensors driven from the same environmental
execution may report different values because their documented state,
configuration, and conversion history differ.

A held stimulus remains stable until an external input changes it. Elapsed time
may produce documented transitions, but it must not cause the model to invent
noise, jitter, drift, or environmental variation. If a future coordinator
routes one device's output into another device's stimulus, topology, latency,
ordering, and settlement remain coordinator concerns; devices do not reference
or mutate one another.

Initial state and initial applied stimuli must be explicit or have documented
deterministic defaults. A model must not silently invent ambient conditions
because no stimulus was supplied.

### Transport transitions and visible effects

Transport operations are inputs to the device state machine, not necessarily
pure observations. A read or transaction may cause documented effects such as
FIFO consumption, read-clear behavior, pointer advancement, latching, or
interrupt acknowledgement.

Such effects must be attributable to the documented transport boundary and
visible in the model's behavioral contract. An interface presented as
diagnostic inspection must not conceal device mutation. Repeated pure
inspection of the same frozen state produces the same result.

Transport duration, protocol-phase decomposition, response linearization, and
rejection timing depend on the declared abstraction used by a future harness or
focused test. A device model should represent documented effects at the
boundary it accepts, but it must not invent hidden bus timing or require a
particular global transaction protocol.

A modeled device refusal is documented device behavior. An operation outside
the model's supported fidelity is instead an explicit model limitation and
must fail clearly or remain unavailable rather than fabricate a plausible
device response, duration, or state transition.

Unsupported behavior may become knowable only after part of the transport
abstraction has already been accepted. In that case the model or test must not
invent subsequent behavior or erase effects already committed at its declared
boundary. How partial transport phases, elapsed duration, and abort semantics
are represented remains part of the deferred transport and failure contract.

### Compatibility boundary and deferred coordination

The purpose of this working specification is to prevent independently authored
peripheral models from capturing responsibilities that would make later
coordination require rewriting them. It does not define that coordinator.

These shared semantic decisions are useful before a shared coordinator exists.
A focused repository test can supply transport operations, stimuli, and elapsed
duration directly and use the model immediately in CI. A future coordinator can
supply those same categories of input across RTC, sensor, GPIO, flash, and
other models without changing their device-specific transition logic.

Interoperability therefore comes from shared meanings and responsibility
boundaries, not from prematurely standardizing one framework. Each model should
avoid inventing a private answer for a concern that belongs to external
coordination, while remaining no more complex than its declared purpose
requires.

A device model owns:

- datasheet-derived device state and deterministic transitions;
- its documented response to transport, applied stimuli, and elapsed duration;
- transport responses and device-observable outputs;
- declared abstractions, exclusions, limitations, and silicon variants.

It does not own:

- an absolute world clock or advancement policy;
- driver delay, timer, executor, or scheduling policy;
- authoritative environmental state or physical-world evolution;
- topology, other device models, cross-device routing, or coupling policy;
- event queues, simultaneity, settlement, or global failure atomicity;
- trace serialization, HIL orchestration, or a future harness API.

The following choices are intentionally deferred until a coordinated simulator
has concrete requirements:

- the shared duration type and exact arithmetic;
- whether duration and actions are supplied together or separately;
- transport timing and phase granularity;
- event-discovery and next-boundary APIs;
- batching, simultaneity, and cross-device settlement;
- topology and transport delegation;
- mutable versus value transition APIs;
- trace, snapshot, rollback, and failure semantics.

The durable context, reopening triggers, and expected ownership for these
questions are maintained in
[`DEVICE_MODEL_COORDINATION_DEFERRED_DECISIONS.md`](DEVICE_MODEL_COORDINATION_DEFERRED_DECISIONS.md).
That record preserves design seams without making them requirements of this
device-model specification.

A simple model should not implement speculative machinery for any deferred
choice. It should preserve the semantic inputs and outputs needed for a later
coordinator to supply that machinery externally.

The following questions are review prompts, not a complete partition of
responsibility. A concern may have both a device-owned rule and an
externally-owned execution choice. Ask:

1. Is it a deterministic, source-backed consequence of device state,
   transport, applied stimulus, or elapsed duration?
2. Is it needed to challenge behavior observable through the supported driver
   contract?
3. Or does it decide when an input occurs, what the shared world contains, how
   devices are connected, or how several models are coordinated?

Use the answers to separate source-backed device consequences from choices
about occurrence, parameter selection, topology, and coordination. When a
concern spans both, record each responsibility separately rather than assigning
the whole concern to one actor.

## 5. Purpose-driven fidelity and honest incompleteness

Model fidelity is purpose-driven and multidimensional. A model is not improved
merely by containing more simulated detail. It should implement the least
complexity needed to challenge the documented, driver-observable behavior in
its declared scope.

Each relevant behavior or phenomenon should be classified as:

1. **Modeled:** implemented from documented behavior and included in the
   model's claims.
2. **Abstracted:** simplified while preserving the declared observable
   behavior.
3. **Injected:** supplied externally rather than generated by the model.
4. **Excluded:** deliberately outside scope and not implied by passing tests.
5. **Unsupported:** detected and rejected or left unavailable rather than
   approximated.

Additional fidelity should be included only when it adds reviewable value by
exercising a documented distinction, revealing a meaningful driver defect, or
preventing a known false confidence. Physical behavior must not be invented
merely to make the model appear realistic.

In particular, accuracy limits and physical uncertainty do not by themselves
define a stochastic process. Under the same initial state and ordered input
trace, the model must not add undocumented noise, jitter, drift, or
environmental change. Useful physical variation should normally be supplied as
an explicit, reproducible harness stimulus or separately configured device
characteristic.

A documented range must not silently collapse into one universal physical
truth. A model may select a fixed, conservative, typical, or swept point when
that choice is useful and explicitly declared as modeled, abstracted, or
externally selected. The declaration should also state whether the choice is
fixed per model instance, per execution, or per test case. The model need not
invent a probability distribution or parameterization unsupported by its
purpose and sources.

Each model should state its purpose, applied-stimulus boundary, modeled and
abstracted behavior, injected inputs, exclusions, unsupported operations,
source basis, and explicit nonclaims. Unsupported behavior should fail clearly
or remain unavailable rather than return a plausible invented result.

Passing tests establish compatibility only with the behavior actually declared
and implemented. They do not establish correctness for excluded phenomena,
undocumented silicon behavior, analog performance, environmental physics, or
physical hardware.

### Datasheet baseline and silicon variants

The default model should remain an independently derived interpretation of its
pinned sources. Later physical evidence may correct that interpretation or
demonstrate behavior specific to a silicon family member, revision, lot, or
other recorded identity.

A silicon-specific observation must not silently replace the datasheet
baseline or behavior supported by another observed variant. CI should be able
to select the baseline or a supported variant explicitly and preserve the
claim under test. This specification does not prescribe whether variants use
parameters, profiles, constructors, tables, shared implementation, or separate
implementations with common conformance tests.

Each departure from the baseline should record:

- the affected silicon identity and tested conditions;
- whether the change corrects a source interpretation or introduces a variant;
- the physical evidence and review decision supporting it;
- the precise behavior that differs; and
- the variants and baseline behavior that remain preserved.

Physical evidence does not automatically identify which artifact is wrong. A
disagreement may implicate the driver, model, source interpretation, contract,
fixture, instrument, sample, or test discrimination. Corrections should remain
independently derived and reviewed rather than editing driver and model merely
until they agree.

## 6. Independence from the driver

Driver and model may use the same pinned source material, but their
interpretations and implementations must remain independently reviewable. The
model should not reuse the driver's private:

- register masks and command encoders;
- response decoders;
- transaction builders;
- operation sequencing; or
- state-machine implementation.

Sharing an abstract transport trait or public API domain types does not by itself
destroy independence. Sharing the logic whose correctness is being tested
does. Separate contributors, agents, branches, or work packets can support
independence, but separation of authorship is not a substitute for separation
of derivation.

When driver and model disagree, the resolution should return to pinned source
evidence and record an explicit contract decision. Editing either side merely
to make the test green creates a self-confirming system.

## 7. Validation layers

These layers answer different questions and should not be collapsed:

- **Codec and reference-vector tests:** Is a local transformation correct for
  known inputs and outputs?
- **Scripted transport tests:** Did a focused path issue the expected calls?
- **Driver-versus-model tests:** Can the public driver operate against the
  modeled device behavior without knowing model internals?
- **Model tests:** Does the model itself implement its declared reset,
  transition, access, and fault semantics?
- **Physical qualification:** Does reviewed `ph-hil` evidence support the
  driver claim for the identified silicon, conditions, fixture, and
  observation capability, and does it reveal a baseline correction or variant
  that the model should preserve explicitly?

Model tests should not require the production driver. Driver-versus-model tests
should assert through the driver's public surface and device-observable effects,
not privileged model state. Deliberately perturbing either implementation is a
useful check that the suite can detect disagreement.

## 8. Source and change discipline

Each model should identify:

- the vendor documents and revisions from which it was derived;
- source URLs and recorded digests without redistributing unlicensed vendor
  documents;
- its purpose and applied-stimulus boundary;
- behavior classified as modeled, abstracted, injected, excluded, or
  unsupported;
- assumptions, ambiguities, explicit nonclaims, and deliberately excluded
  behavior; and
- corrections to the datasheet baseline and evidence-backed silicon variants,
  with their distinct provenance and supported identities.

A material change to observable model behavior is a contract change and should
be reviewed as such. The model may live as a test-only module or workspace
crate; this specification does not prescribe packaging or make it a public API.

## 9. Peripheral examples

- A register peripheral can model reset values, access rules, field effects,
  and documented transaction boundaries without modeling its analog circuit.
- A sensor can accept an applied sensing-element value or injected raw sample
  and model documented conversion, status, and data-ready behavior without
  generating environmental truth or invented analog variation.
- An RTC can consume relative duration supplied by a test or harness and model
  calendar rollover without owning world time or claiming crystal accuracy,
  drift, or analog backup-supply behavior.
- A flash device can model command state, write enable, busy state, and address
  rules without claiming endurance or signal integrity.
- A bus switch can model channel-selection semantics and reset behavior without
  modeling capacitance, voltage levels, or downstream board topology.
- A touch controller can accept injected electrode observations without
  simulating capacitance or enclosure mechanics.

## 10. Common anti-patterns

- **Echo model:** imports the driver's codecs and confirms their own output.
- **Transcript overfit:** rejects any valid transaction sequence that differs
  from the one currently emitted by the driver.
- **Omniscient assertion:** tests private model state that the device could not
  expose to the driver.
- **Silent completeness:** returns invented behavior for unsupported commands.
- **Integration capture:** absorbs HAL, board, executor, DMA, retry, or product
  policy into the device model.
- **World clock in the device:** stores harness `now`, exposes `set_now(t)`, or
  implements `DelayNs` / pin waits on the model. Logical time is a harness
  coordinate; the device consumes only explicit relative-duration steps.
- **Environmental capture:** owns ambient or shared physical truth, predicts
  its future evolution, or directly propagates conditions to another device
  instead of accepting a harness-projected applied stimulus.
- **Autonomous mutation:** changes state without an explicit external input,
  including wall-time progress, background execution, lazy temporal catch-up
  on access, or invented stochastic variation.
- **Hidden transport effect:** conceals FIFO consumption, read-clear behavior,
  pointer movement, or another documented transition inside an interface
  presented as pure inspection.
- **Unitless duration:** accepts a numeric time step whose unit and resolution
  are implicit.
- **Partition-dependent evolution:** discards fractional progress so that
  valid partitions of the same elapsed duration are observably different under
  unchanged stimuli merely because the caller divided the interval.
- **Invented realism:** adds noise, jitter, drift, thermal behavior, or random
  variation without a documented requirement and explicit fidelity claim.
- **Harness capture:** puts a scheduler, stimulus timeline, subscriber bus, or
  multi-device kernel inside the device model. A 20-line test helper that
  calls `inject` / `step` is disposable glue. A private world object is a
  product other peripherals will have to replace.
- **Hidden physical claim:** describes host-model success as hardware support.
- **Speculative scaffolding:** adds future `ph-hil` layouts or evidence machinery
  before a reviewed protocol requires them.

## 11. Working review prompts

These are prompts for design review, not normative acceptance criteria:

- Can the observation boundary be explained in one paragraph?
- Is every modeled behavior traceable to a pinned source or recorded decision?
- Can the model be tested without the production driver?
- Does it avoid production logic whose correctness it is meant to challenge?
- Is every mutation attributable to an explicit, ordered external input?
- Does the model remain quiescent between inputs?
- Does the model consume unit-bearing relative duration without owning a
  harness `now`?
- Is duration evolution partition-consistent under unchanged applied stimuli?
- Does the model retain fractional progress rather than round each step
  independently?
- Are environmental truth, applied stimulus, and device measurement state kept
  distinct?
- Does the device avoid generating or evolving physical conditions that belong
  to the harness?
- Are transport side effects explicit and tied to documented boundaries?
- Does pure diagnostic inspection leave frozen model state unchanged?
- Is each relevant phenomenon declared as modeled, abstracted, injected,
  excluded, or unsupported?
- Could a later harness supply the same semantic transport, stimulus, and
  duration inputs without rewriting the device?
- Does the model avoid choosing a deferred coordinator API or scheduling
  policy merely because no shared harness exists yet?
- Does unsupported behavior fail honestly?
- Would a deliberate driver or model defect cause a test to fail?
- Are physical and board-level claims explicitly excluded?
- Can later silicon evidence correct the baseline or add a selected variant
  without erasing behavior supported by another silicon identity?

The desired result is a small, bounded, falsifiable device hypothesis, not a
complete virtual product and not an implementation that can only agree with
itself.
