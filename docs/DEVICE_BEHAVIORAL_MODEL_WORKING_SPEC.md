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
executable model of documented device behavior that is observable through the
operations supported by the driver.

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

### Device API as a sink

The model is a deterministic **sink** for explicitly timed triggers. It is not
a source of world time, environmental truth, or execution policy. Every
committed trigger carries a positive, unit-bearing relative duration from the
current temporal frontier to the next one.

1. **Timed transport boundaries** from the driver-facing abstract transport,
   such as a read, write, I2C STOP, or chip-select transition.
2. **Timed applied-stimulus changes** from the harness, such as supply
   availability, a sensing-element temperature, a completed raw sample, or a
   pending transport fault.
3. **Pure duration advancement** from the harness when elapsed time passes
   without another external operation.

For each trigger, the harness advances every participating model through the
same relative duration, applies the addressed operation at its declared
boundary, and publishes the resulting frontier only after its effects settle.
The addressed model deterministically transforms its prior state and returns
any transport response or externally visible device output. The harness owns
the trigger, duration, ordering, and commit boundary. The device model remains
quiescent between triggers.

A later organization-wide host harness should be able to orchestrate the same
transport, stimulus, and relative-step seam. Driver repositories should not
invent a private world coordinate, scheduler, environmental model, or stimulus
timeline that other peripherals would have to copy.

### Temporal frontier and explicit triggers

The harness maintains a strictly advancing **temporal frontier**: the greatest
point in the ordered trigger history through which every participating model
has been brought and all immediate consequences have settled. At a settled
frontier, each model's state and applied stimuli are valid at that frontier.

A harness may associate an elapsed-time coordinate called `now` with the
frontier, but its origin and absolute value have no device-level meaning. Only
relative duration and the resulting trigger order are semantic. Every
committed trigger advances that coordinate by its explicit duration; there are
no committed zero-duration triggers. Conditions that are simultaneous at the
declared resolution are grouped into one trigger.

Every state mutation must be attributable to an explicitly timed trigger
controlled by the harness:

- elapsed duration applies documented time-dependent effects to every
  participating device;
- the trigger's transport boundary may additionally apply documented
  transaction-dependent effects to the addressed device; and
- the trigger's stimulus boundary may additionally apply documented effects
  of the new stimulus to every affected device.

The model must not advance from wall time, poll external state, run background
evolution, introduce random variation, or lazily catch up during an unrelated
operation. Replaying the same initial state and ordered trigger trace must
produce the same transitions and outputs regardless of host speed, polling
frequency, test structure, or harness implementation.

Not every model changes observably at every frontier, but every participating
model consumes the trigger's relative duration. A targeted operation may add a
transition only to its addressed device; other models retain or evolve their
state according to elapsed time. The harness settles all immediate
consequences before publishing the frontier.

### Relative-duration contract

A time step is a non-negative, unit-bearing elapsed duration in the harness
reference-time domain. It is not an absolute timestamp or a device oscillator
tick count. An interface must make the unit explicit; an unqualified numeric
`delta` is insufficient. A duration type with nanosecond resolution, or an
explicitly named integer such as `delta_ns`, is suitable. This working
specification does not prescribe a shared Rust type.

The device does not choose the duration of a trigger. The harness derives it
from a declared deterministic timing policy, such as an abstract fixed
transaction cost, explicit test input, or a transport model. Changing that
policy changes the trigger trace and must be visible in test provenance.

Prefer a device method shaped like `step(delta)`:

- **Zero is inspection, not a trigger.** A zero duration cannot commit an
  operation or mutate state. It may be used only to describe pure evaluation
  of a frozen state.
- **No hidden elapsed time.** Every transport operation and stimulus change
  carries a harness-supplied duration. The device does not infer that duration
  from bus speed, host wall time, or the operation itself. If intermediate
  signal edges are in scope, the harness represents them as additional timed
  triggers.
- **Partitioning is consistent.** Under unchanged applied stimuli,
  `step(a)` followed by `step(b)` produces the same final state and ordered
  externally visible effects at the same relative offsets as `step(a + b)`.
- **Modeled events are preserved.** A large step applies every modeled
  rollover, match, conversion, flag change, and other event in the interval.
  It need not iterate through artificial fixed-size ticks.
- **Sub-resolution progress is retained.** The model preserves any fractional
  duration or oscillator phase needed to make valid partitions equivalent.

Advancing reference time is always a harness-wide operation, including when
the trigger is a transaction or stimulus change. Before the harness publishes
the next frontier, every participating model must have consumed the trigger's
duration. A driver wait of `n` means conceptually `harness.advance(n)`, not
`now += n` followed by `one_device.step(n)`.

The harness partitions a requested advance at scheduled stimulus changes and
at modeled device events whose externally visible consequences affect another
model. At each boundary it routes outputs, applies resulting stimulus changes,
and settles their immediate consequences before advancing again. This
specification preserves that seam without prescribing an event-discovery API.

`set_now(t)` on the device couples it to a world coordinate, including its
origin, units, rewind policy, and a stored `last_now`. That coordinate belongs
to the harness. A model may keep datasheet-required `busy_remaining`,
oscillator phase, conversion progress, and similar relative state. Those are
consequences of elapsed time, not a copy of harness `now`.

Harness reference time, device oscillator state, and device-visible time are
distinct. An RTC calendar may stop, drift, wrap, reset, or be written backward
while the harness frontier remains monotonic.

### Harness-owned environment and applied stimuli

The harness owns the **authoritative environmental state** for an execution:
shared physical conditions, their supplied history and changes, and
relationships among devices. This does not require a detailed physical world
model. A focused test may act as a minimal harness and supply deterministic
stimuli directly. A device model does not contain the authoritative environment
and does not receive a reference to harness environmental state.

The harness projects environmental truth into narrow, device-specific
**applied stimuli**. A model may retain the last applied value of a persistent
stimulus so it can evolve under that value during `step(delta)`. This retained
input is not authoritative environmental state: the model does not decide when
it changes, extrapolate its trajectory, or propagate it to another device.

For example, a temperature-sensor model may accept a sensing-element
temperature or a completed raw conversion. It owns its documented sampling,
conversion timing, quantization, filtering, register, and interrupt behavior.
It does not own ambient temperature, thermal coupling, airflow, self-heating,
or the future evolution of the physical quantity unless a deliberately
declared, source-backed fidelity decision places a specific effect in scope.

The device's measurement state may differ from current environmental truth. A
sensor may still report its previous conversion after the applied temperature
changes, and two sensors at the same frontier may report different values due
to their respective documented state. That is not temporal or environmental
inconsistency.

Persistent stimuli remain applied until a timed harness trigger changes them.
Unless a finer boundary is explicitly modeled, the prior stimulus is held over
that trigger's duration and the new value takes effect at its ending frontier.
Changes declared simultaneous at the harness resolution are applied as one
trigger. One-shot stimuli are delivered and consumed at their documented
boundary. Device outputs return to the harness; when an output affects another
device or a shared condition, the harness updates its world state and schedules
the resulting timed trigger. Devices do not mutate one another.

At every settled frontier, each model's applied stimuli must agree with the
harness projection for that device. If a condition changes during an elapsed
interval, the harness splits the interval at that change. The model does not
invent a trajectory between supplied values.

Initial device state and initial applied stimuli must be explicit or have
documented deterministic defaults. A model must not silently invent ambient
conditions merely because the harness has not supplied them.

### Transport transitions and visible effects

Transport operations are explicitly timed inputs to the state machine, not
necessarily pure observations. A transaction may return a response and apply
documented effects such as FIFO consumption, read-clear behavior, pointer
advancement, latching, or interrupt acknowledgement.

The harness advances every participating model through the transaction's
declared duration. Transaction-dependent effects then occur at their documented
linearization boundary. A second committed operation necessarily occurs at a
later temporal frontier and is evaluated against the resulting state.

The contract should identify the boundary at which the response and effects
linearize, such as command acceptance, byte transfer, STOP, or chip-select
release. If behavior depends on an intermediate point, the harness decomposes
the transaction into smaller timed triggers. A rejected operation may still
consume its declared duration; it leaves device state unchanged apart from
elapsed-time evolution unless documented behavior assigns an additional
effect to that failure.

The transition must be visible in the model contract and attributable to the
trigger; an interface presented as pure inspection must not hide device-state
mutation. A separate diagnostic inspection facility, if provided, observes a
frozen model state without committing device behavior. Repeated inspection of
the same frozen state produces the same result.

Semantically, each trigger has the form:

```text
(next state, response, outputs) =
    transition(current state, applied stimuli, delta, trigger)
```

The implementation may mutate storage in place, but the prior state, explicit
trigger, resulting state, and externally relevant effects must remain
deterministically reviewable and testable.

This specification does not prescribe a host-harness crate, shared duration
type, event scheduler API, or packaging. It preserves the responsibility seam:
the harness owns when and what is physically true; the device owns the
documented transition that follows.

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
define a stochastic process. Under the same initial state and ordered trigger
trace, the model must not add undocumented noise, jitter, drift, or
environmental change. Useful physical variation should normally be supplied as
an explicit, reproducible harness stimulus or separately configured device
characteristic.

Each model should state its purpose, applied-stimulus boundary, modeled and
abstracted behavior, injected inputs, exclusions, unsupported operations,
source basis, and explicit nonclaims. Unsupported behavior should fail clearly
or remain unavailable rather than return a plausible invented result.

Passing tests establish compatibility only with the behavior actually declared
and implemented. They do not establish correctness for excluded phenomena,
undocumented silicon behavior, analog performance, environmental physics, or
physical hardware.

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
- **Physical qualification:** Does reviewed `ph-hil` evidence show that the
  declared behavior reflects supported silicon?

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
- any source-backed correction learned during later physical qualification.

A material change to observable model behavior is a contract change and should
be reviewed as such. The model may live as a test-only module or workspace
crate; this specification does not prescribe packaging or make it a public API.

## 9. Peripheral examples

- A register peripheral can model reset values, access rules, field effects,
  and documented transaction boundaries without modeling its analog circuit.
- A sensor can accept an applied sensing-element value or injected raw sample
  and model documented conversion, status, and data-ready behavior without
  generating environmental truth or invented analog variation.
- An RTC can `step(delta)` under a harness-owned temporal frontier and model
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
- **Autonomous mutation:** changes state without an explicit harness trigger,
  including wall-time progress, background execution, lazy temporal catch-up
  on access, or invented stochastic variation.
- **Untimed trigger:** commits a transport, stimulus, or other external action
  without a harness-supplied relative duration and synchronized advancement of
  every participating model.
- **Hidden transport effect:** conceals FIFO consumption, read-clear behavior,
  pointer movement, or another documented transition inside an interface
  presented as pure inspection.
- **Unitless duration:** accepts a numeric time step whose unit and resolution
  are implicit.
- **Partition-dependent evolution:** discards fractional progress so that
  `step(a); step(b)` differs from `step(a + b)` under unchanged stimuli.
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
- Is every mutation attributable to an explicit, ordered harness trigger?
- Does the model remain quiescent between triggers?
- Does every committed trigger carry an explicit relative duration and advance
  every participating model to the same next frontier?
- Does the model consume unit-bearing relative duration without owning a
  harness `now`?
- Does harness advancement bring every participating model to the same
  temporal frontier before publishing it?
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
- Could a later harness drive the same transport/stimulus/step sink without
  rewriting the device?
- Does unsupported behavior fail honestly?
- Would a deliberate driver or model defect cause a test to fail?
- Are physical and board-level claims explicitly excluded?
- Can later silicon evidence correct the model without preserving a prior
  assumption for compatibility?

The desired result is a small, bounded, falsifiable device hypothesis, not a
complete virtual product and not an implementation that can only agree with
itself.
