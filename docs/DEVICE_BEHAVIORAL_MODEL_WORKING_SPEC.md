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

The model is a **sink** for three kinds of input. It is not a source of world
time and not a test harness.

1. **Transport operations** from the driver (the abstract bus the driver
   already uses).
2. **Environment injections** from the harness: held physical conditions such
   as power availability, a completed sensor sample, or a pending transport
   fault.
3. **Time steps** from the harness: `step(Δt)` meaning “this much simulated
   time passed under the environment you currently hold.”

The harness answers *what time is it, and what is physically true?* The model
answers *given that, what does the datasheet do to this device?* The driver
answers *which transport operations do I issue?*

A later organization-wide host harness, and later `ph-hil` physical execution,
should be able to drive the same sink. Driver repositories should not invent a
private world, scheduler, or `now` object that other peripherals would have to
copy.

### Logical time is `step(Δt)`, not `set_now(t)`

Distinguish two clocks:

- **Harness `now`:** a monotonic simulated elapsed-time coordinate. The
  harness owns it. Jumping `now` is a harness operation.
- **Device state:** registers, flags, pin modes, and any datasheet timers
  (busy remaining, conversion period, countdown chain). Those are device
  state. They are not a copy of harness `now`. An RTC’s civil calendar is an
  *output* of stepping while the modeled oscillator is running, not the
  definition of time.

Prefer a device method shaped like `step(Δt)` with `Δt ≥ 0`:

- **Inject is instantaneous.** Changing power or a sample does not consume
  simulated time. Datasheet effects that occur on the condition change (for
  example an oscillator-stop flag on loss of supply) happen on inject.
- **`step(Δt)` is the only way simulated time passes.** Transport operations
  do not implicitly advance `now`. Driver `DelayNs` or pin waits belong to
  the harness: a wait of `n` is `now += n` followed by `device.step(n)`.
- **A zero step is a no-op** for time. A negative step is a contract error.
- **A large step must apply every modeled event in the interval**, not skip
  to the end as if intermediate matches, conversions, or rollovers did not
  occur. Variable-sized steps are still discrete-event evolution, not a
  busy 1 ms loop.
- **If environment changes at an intermediate time,** the harness splits the
  interval (`step` under `E0`, inject, `step` under `E1`). The model does
  not own a stimulus timeline.

`set_now(t)` on the **device** couples the chip to a world coordinate:
rewind policy, epoch, units, and a stored `last_now`. That coordinate
belongs to the harness. A harness may offer `set_now` as sugar
(`Δt = t − now`; `device.step(Δt)`; `now = t`). The device should not.

The model may keep remaining-time counters that the datasheet requires. Those
counters are updated by `step(Δt)`. They are not harness `now`.

### Held environment

The harness owns the story of physical conditions. The model holds only the
last told condition, the way a pin holds a level until it changes. Injected
power, samples, and similar levels remain in force until the next inject.
Pending one-shot faults are consumed at the transport boundary.

This specification does not prescribe a host-harness crate, a shared clock
type, or packaging. It only preserves a seam: environment in, datasheet
state out, so a future shared `now` does not require rewriting each device
model.

## 5. Fidelity and honest incompleteness

The model should classify its behavior rather than imply completeness:

1. **Modeled:** behavior required by the repository's supported driver
   contract.
2. **Optional:** additional documented behavior useful for exercising that
   contract.
3. **Excluded:** analog and electrical behavior, board topology, physical
   tolerances, undocumented quirks, and functionality outside the declared
   scope.

Unsupported behavior should fail explicitly or remain unavailable. The model
must not invent a plausible response and quietly broaden the support claim.

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
- the operations and state it models;
- assumptions, ambiguities, and deliberately excluded behavior; and
- any source-backed correction learned during later physical qualification.

A material change to observable model behavior is a contract change and should
be reviewed as such. The model may live as a test-only module or workspace
crate; this specification does not prescribe packaging or make it a public API.

## 9. Peripheral examples

- A register peripheral can model reset values, access rules, field effects,
  and documented transaction boundaries without modeling its analog circuit.
- A sensor can accept injected raw samples and model status or data-ready
  behavior without generating real-world environmental values.
- An RTC can `step(Δt)` under a harness-owned `now` and model calendar
  rollover without owning world time or claiming crystal accuracy, drift, or
  analog backup-supply behavior.
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
  coordinate; the device only `step(Δt)` under a held environment.
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
- Are time and external events explicit and deterministic?
- Does the model `step(Δt)` under a held environment, or does it own a `now`?
- Could a later harness drive the same inject/step sink without rewriting the
  device?
- Does unsupported behavior fail honestly?
- Would a deliberate driver or model defect cause a test to fail?
- Are physical and board-level claims explicitly excluded?
- Can later silicon evidence correct the model without preserving a prior
  assumption for compatibility?

The desired result is a small, bounded, falsifiable device hypothesis, not a
complete virtual product and not an implementation that can only agree with
itself.
