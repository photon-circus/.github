# Device Behavioral Model Standard

Status: **Normative core with non-normative guidance**

Recorded: **2026-08-12 UTC**

Last revised: **2026-08-14 UTC**

This document contains the organization-wide responsibility boundary and
implementation guardrails for the executable model commonly called a *driver
mock*, together with non-normative rationale and review aids. It supplements
the repository standards and pre-`ph-hil` peripheral driver profile. It is not
by itself a publication gate, audit finding, or claim of hardware
qualification, and it does not override a pinned vendor source.

The terms **must**, **must not**, **required**, **should**, **should not**, and
**may** express the strength of a rule. Statements that explicitly defer a
choice do not authorize each model to choose a private coordinator contract.

### Authority and agent use

The normative core is the inherited decision set for independently acting
contributors, including AI agents. Its purpose is to prevent each model effort
from re-deriving shared semantics and making locally plausible choices that are
incompatible with other models or the direction of the organization standards.

An implementation must apply the normative core as an input constraint, not as
an open design prompt. It may choose among alternatives only where the standard
explicitly permits a local choice. It must not override a settled boundary for
local convenience, infer a required code structure from another model, or
privately resolve a choice recorded as deferred.

If current work demonstrates that a normative rule is insufficient or
incompatible with source-backed device behavior, the implementation must
preserve that evidence and propose a standards change. It must not silently
establish a conflicting local convention. If a deferred question becomes
concrete, the work must identify its reopening trigger and route the decision
to the expected shared owner recorded in the deferred-decision register.

A provision belongs in the normative core only when all of the following are
true:

1. it resolves a recurring seam that independently authored models could
   otherwise resolve incompatibly;
2. it is supported by concrete design or implementation evidence;
3. it expresses a stable semantic, responsibility, evidence, or independence
   boundary that applies across device families;
4. recording it prevents rediscovery or incompatible local decisions; and
5. it can be stated without prescribing incidental code structure or resolving
   a coordinator concern whose requirements remain deferred.

Material that does not meet this admission test remains non-normative guidance
or a deferred decision. One implementation, agent preference, code-size target,
or convenient API shape is not by itself sufficient to create an
organization-wide requirement.

### Status map

The following sections are **normative**:

- Section 1, preferred term and definition;
- Section 3, exclusions and responsibility boundary;
- Section 4, observation, input, time, environment, transport, and coordination
  boundaries;
- Section 5, fidelity and silicon-variant discipline;
- Section 6, independence and packaging;
- Section 7, separation of validation claims; and
- Section 8, source and change discipline.

The following sections are **non-normative guidance**:

- Section 2, intended uses;
- Section 9, peripheral examples;
- Section 10, common anti-patterns; and
- Section 11, working review prompts.

Non-normative sections explain and help review the normative core. They do not
create additional acceptance criteria. If guidance appears to conflict with a
normative requirement, the normative requirement controls.

## 1. Preferred term and definition (normative)

The preferred durable term is **device behavioral model**. *Driver mock* is
acceptable shorthand, but can misleadingly suggest that the driver itself is
being mocked. The driver is the system under test; the model represents the
device side of its abstract transport boundary.

The organization standards' terms **behavioral mock** and **behavioral model**
refer to this same artifact; **device behavioral model** is the preferred
durable name used by this standard.

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

## 2. What the model is for (non-normative)

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

## 3. What the model is not (normative)

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

## 4. Observation boundary (normative)

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

Determinism does not authorize a convenient value for source-undeclared
observable initial state. Each such value must be source-backed, supplied as an
explicit initial input, selected as a declared purpose-driven abstraction, or
left unavailable until an explicit input establishes it. In particular, the
absence of a documented reset value does not authorize returning zero, `false`,
an empty value, or another plausible device result without declaring the
abstraction and its observable consequence.

### Transport transitions and visible effects

Transport operations are inputs to the device state machine, not necessarily
pure observations. A read or transaction may cause documented effects such as
FIFO consumption, read-clear behavior, pointer advancement, latching, or
interrupt acknowledgement.

Such effects must be attributable to the documented transport boundary and
visible in the model's behavioral contract. An interface presented as
diagnostic inspection must not conceal device mutation. Repeated pure
inspection of the same frozen state produces the same result.

An externally applied level and an edge-triggered event are different inputs.
If an API accepts the current level of RESET, power-good, enable, an interrupt,
or another persistent stimulus, applying the same unchanged level again must
not repeat an edge effect. Resetting on assertion and resetting on every call
that happens to carry an asserted or released level are not equivalent. A model
may instead accept explicit assertion and release events, but its naming and
contract must make that event semantics unambiguous.

Transport duration, protocol-phase decomposition, response linearization, and
rejection timing depend on the declared abstraction used by a future harness or
focused test. A device model should represent documented effects at the
boundary it accepts, but it must not invent hidden bus timing or require a
particular global transaction protocol.

A modeled device refusal is documented device behavior. An operation outside
the model's supported fidelity is instead an explicit model limitation and
must fail clearly or remain unavailable rather than fabricate a plausible
device response, duration, or state transition.

The public result surface must preserve this distinction. A model-input error,
unsupported-sequence result, or unavailable operation must not be translated
into a protocol NACK, timeout, fault bit, or other response that claims the
device produced it. Convenience helpers and transport adapters must preserve
the same distinction rather than collapsing it for a simpler return type.

When an external interface requires callable operations outside the model's
declared fidelity, its adapter must return or preserve a distinguishable model
limitation rather than treat an ordinary unsupported input as a process panic
or fabricated device response. This does not prohibit treating a violated
programmer invariant as a defect; unsupported fidelity is an expected boundary
outcome, not such an invariant violation.

A model must not choose behavior for a source-undeclared transport sequence
merely because its state machine can continue. It must reject the sequence as
unsupported or leave it unavailable unless the model's declared purpose and
evidence establish the behavior. Rejection must not commit pending effects or
perform cleanup that would itself mutate device state, except where the
declared boundary explicitly models that cleanup input.

The declared input domain includes supported operation shapes, addresses or
commands, values, and field combinations, not only method or register names.
The model must validate all information available at its accepted boundary
before committing effects that depend on that input. This does not require
rolling back effects already committed at an earlier declared transport phase.

Unsupported behavior may become knowable only after part of the transport
abstraction has already been accepted. In that case the model or test must not
invent subsequent behavior or erase effects already committed at its declared
boundary. How partial transport phases, elapsed duration, and abort semantics
are represented remains part of the deferred transport and failure contract.

### Compatibility boundary and deferred coordination

The purpose of this standard is to prevent independently authored
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

Implementation structure must remain proportional to device behavior and the
model's declared purpose. A simple model must not be required to expose a
generic framework, implement speculative coordinator traits, duplicate a
production transport API, or add model-specific policy enforcement merely to
demonstrate future compatibility. Reusable machinery must not be introduced as
a model requirement until at least two concrete models demonstrate the same
semantic need, unless a current consumer or source-backed behavior already
requires it.

Convenience transaction builders, driver adapters, schedulers, trace encoders,
and orchestration error hierarchies are external support concerns unless they
encode source-backed device behavior. They must remain outside the
device-specific behavioral core—in focused tests, a support module, or another
external support layer—and must not enlarge the model's public behavioral
surface without a current consumer and documented need.

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
device-model standard.

A simple model should not implement speculative machinery for any deferred
choice. It should preserve the semantic inputs and outputs needed for a later
coordinator to supply that machinery externally.

## 5. Purpose-driven fidelity and honest incompleteness (normative)

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

Each model must state its purpose, applied-stimulus boundary, modeled and
abstracted behavior, injected inputs, exclusions, unsupported operations,
source basis, and explicit nonclaims. Unsupported behavior should fail clearly
or remain unavailable rather than return a plausible invented result.

Passing tests establish compatibility only with the behavior actually declared
and implemented. They do not establish correctness for excluded phenomena,
undocumented silicon behavior, analog performance, environmental physics, or
physical hardware.

The fidelity declaration is a semantic requirement, not a required document
set. A model may satisfy it in one concise crate README, module document,
repository contract section, or other durable location appropriate to its
size. Repositories must link to one maintained declaration rather than repeat
the same source, ownership, exclusion, and nonclaim prose across several files.

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

## 6. Independence from the driver (normative)

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

Packaging and independence are separate decisions. A model may be a test
module, a private repository crate, a workspace crate, or another bounded
artifact. A separate crate can make dependencies and `no_std` properties easy
to inspect, but this standard does not require one merely because another model
used that structure.

Production driver code must not depend on model implementation code, and model
implementation code must not depend on private production encodings,
transactions, or transition logic. This does not prohibit a conformance-test
crate, integration-test target, or external harness from depending on both. A
guard intended to preserve independence must enforce the two implementation
boundaries without preventing the common consumer required to compare them.

Mechanical checks must be proportional to the actual leakage risk. Package
boundaries and dependency graphs may be checked where useful; repository-local
scripts must not attempt to prove independent derivation by banning legitimate
conformance topology or scanning for superficial textual similarity. A
repository is not required to add a dedicated independence script when its
existing package boundary, dependency graph, and review make the prohibited
dependencies directly inspectable.

When driver and model disagree, the resolution should return to pinned source
evidence and record an explicit contract decision. Editing either side merely
to make the test green creates a self-confirming system.

## 7. Validation layers (normative)

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

This standard does not require a synthetic wrong-oracle function or mutation
test for every directly asserted behavior. Such tests are required only when
they demonstrate that a material independence, discrimination, or false-pass
risk is not already exercised by ordinary model and conformance tests.

## 8. Source and change discipline (normative)

Each model must identify:

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
be reviewed as such. Packaging is selected for the repository's current
boundary and consumers; it must not silently become a behavioral requirement or
an organization-wide precedent.

## 9. Peripheral examples (non-normative)

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

## 10. Common anti-patterns (non-normative)

- **Echo model:** imports the driver's codecs and confirms their own output.
- **Transcript overfit:** rejects any valid transaction sequence that differs
  from the one currently emitted by the driver.
- **Omniscient assertion:** tests private model state that the device could not
  expose to the driver.
- **Silent completeness:** returns invented behavior for unsupported commands.
- **Convenient initialization:** assigns zero, `false`, empty, or another
  plausible value to source-undeclared observable initial state merely to make
  the model deterministic.
- **Fabricated refusal:** reports an unsupported model input as a device NACK,
  timeout, or fault response.
- **Value-domain leakage:** claims a narrow register or operation slice but
  accepts undeclared values, reserved fields, or feature combinations because
  the storage or transition logic can represent them.
- **Adapter panic:** crashes on an ordinary unsupported operation required by a
  callable adapter interface instead of preserving a model limitation.
- **Level retrigger:** reapplies reset, conversion start, or another edge effect
  whenever an unchanged persistent input level is supplied.
- **Speculative continuation:** defines behavior for a source-undeclared
  transport sequence because the implementation can conveniently continue.
- **Independence blockade:** prevents a conformance consumer from depending on
  both implementations in an attempt to keep driver and model independent.
- **Packaging precedent:** treats a separate crate, module, or repository used
  by one model as a universal behavioral-model requirement.
- **Adapter capture:** makes transaction builders, driver-facing adapters, or
  orchestration errors part of the model API before a current consumer needs
  them.
- **Policy scaffolding:** adds model-specific scripts or framework machinery
  whose size and complexity are not justified by the leakage risk or modeled
  device behavior.
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

## 11. Working review prompts (non-normative)

These are prompts for design review, not normative acceptance criteria:

When a concern may span both device behavior and external execution, ask:

- Is it a deterministic, source-backed consequence of device state,
  transport, applied stimulus, or elapsed duration?
- Is it needed to challenge behavior observable through the supported driver
  contract?
- Or does it decide when an input occurs, what the shared world contains, how
  devices are connected, or how several models are coordinated?

Use those answers to separate source-backed device consequences from choices
about occurrence, parameter selection, topology, and coordination. When a
concern spans both, record each responsibility separately rather than assigning
the whole concern to one actor.

- Can the observation boundary be explained in one paragraph?
- Can the current claim be demonstrated by one minimum useful execution trace?
- Is every modeled behavior traceable to a pinned source or recorded decision?
- For every observable initial zero, `false`, empty, or sentinel value, is its
  source or declared abstraction explicit?
- If an observable initial value is source-undeclared, is it injected,
  explicitly abstracted, or unavailable until an establishing input?
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
- Does the accepted input domain identify operation shapes, values, and field
  combinations rather than only method or register names?
- Are unsupported inputs rejected before state mutation when all required
  information is available at the accepted boundary?
- Are model limitations distinguishable from responses produced by the
  modeled device?
- Do adapters preserve model limitations for callable but unsupported
  operations rather than panic or fabricate a device response?
- Do persistent stimulus levels remain idempotent unless their value changes?
- Are source-undeclared sequences rejected without committing hidden cleanup
  effects?
- Is packaging justified locally rather than inherited as precedent?
- Can an external conformance consumer depend on both driver and model while
  the implementations remain independent?
- Is most implementation complexity attributable to source-backed device
  behavior rather than adapters, policy scripts, or speculative reuse?
- Is there one maintained declaration, with other documents changed only when
  an existing statement became stale?
- Would a deliberate driver or model defect cause a test to fail?
- Are physical and board-level claims explicitly excluded?
- Can later silicon evidence correct the baseline or add a selected variant
  without erasing behavior supported by another silicon identity?

The desired result is a small, bounded, falsifiable device hypothesis, not a
complete virtual product and not an implementation that can only agree with
itself.
