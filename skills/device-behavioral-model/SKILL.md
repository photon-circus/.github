---
name: device-behavioral-model
description: Scope, implement, or review a minimal device behavioral model for a peripheral driver using Photon Circus standards and pinned device evidence. Use when creating or refining a model issue, implementing a model and its conformance tests, reviewing a device-model pull request, or deciding whether proposed behavior belongs in the device, harness, environment, or a deferred coordination layer.
---

# Device Behavioral Model

Use this skill as a procedure for applying the current organization guidance.
Do not treat it as a policy source, device specification, code scaffold, or
replacement for repository instructions.

## Load authority before reasoning

1. Read repository-local contributor and agent instructions.
2. Read [references/guidance-map.md](references/guidance-map.md) completely.
3. Load the current normative device-model standard and the resources selected
   by that map. Do not rely on remembered or bundled summaries.
4. Inspect the target repository's accepted vendor-source registry, hardware
   contract, public driver surface, tests, package policy, and existing fakes.

If the current standard or the evidence required for the requested claim is
unavailable, report that limitation. Do not substitute an inferred contract.
When source-backed device behavior appears incompatible with a normative rule,
preserve the evidence and propose a standards change instead of establishing a
private convention in the model.

## Select the requested mode

- **Analyze:** examine a responsibility or compatibility seam and identify
  whether it belongs to device behavior, external execution, or a recorded
  deferred decision without creating or changing artifacts unless requested.
- **Scope:** produce or refine an implementation issue without writing the
  model unless explicitly requested. Draft or publish the issue only as the
  user authorizes.
- **Implement:** implement only the accepted claim, tests, adapters, and
  maintained declaration; do not broaden the task into a framework.
- **Review:** compare the proposal or implementation with its declared claim,
  pinned evidence, normative guidance, and repository policy. Report concrete
  seams and false-pass risks. Do not modify code unless explicitly requested.

Do not let a later workflow phase expand the user's requested authority.

## Establish the model boundary

1. Identify the exact device identity and behavioral selection. Do not infer
   family-wide support from a package or repository name.
2. Record the primary source URL, revision, date, and accepted digest. Separate
   datasheet baseline behavior from evidence-backed silicon variants.
3. Name the current consumer and write one minimum useful execution trace in
   terms of externally visible behavior. Do not encode the driver's current bus
   transcript as the model contract.
4. State what agreement with the model establishes, what it does not
   establish, and the concrete trigger that would justify more fidelity.
5. Define the accepted input domain: transport shapes and boundaries,
   addresses or commands, supported values and field combinations, applied
   stimuli, injected events, and unit-bearing relative duration where needed.
6. Define observable responses and outputs, retained device state, every
   observable initial value, and each input that can cause mutation.
7. Classify relevant behavior as modeled, abstracted, injected, excluded, or
   unsupported. Keep model limitations distinguishable from device responses.
8. Identify genuine source ambiguities and their observable consequences.
   Reject source-undeclared sequences rather than inventing plausible behavior.

Use the organization declaration template as intake content when scoping. At
handoff, prune it into one maintained declaration in an existing appropriate
location; leave the issue as history rather than a second maintained contract.

## Challenge the temporal and environmental seams

Verify that:

- every mutation follows an explicit, ordered external input;
- the model remains quiescent between inputs and never consults wall time;
- time-dependent behavior consumes relative duration without owning an
  absolute `now`, advancement policy, or scheduler;
- equivalent valid partitions of duration remain observationally equivalent
  under unchanged stimuli;
- driver delay intent reaches the same external advancement path used by model
  tests, and a no-op delay cannot create a passing timing claim;
- environmental truth and physical evolution remain harness concerns;
- the model accepts only its narrow applied stimulus and does not invent noise,
  jitter, drift, or realism;
- reads and writes apply only documented transport side effects;
- pure inspection does not mutate frozen state; and
- unsupported inputs are rejected before mutation when knowable at the
  accepted boundary, without erasing effects already committed in an earlier
  accepted phase.

Do not choose a shared duration type, coordinator API, event scheduler,
transport phase protocol, topology, rollback scheme, trace format, or other
recorded deferred decision merely to complete one model.

## Preserve independence and proportionality

Derive model behavior independently from pinned evidence. Do not reuse the
production driver's private register masks, codecs, transaction builders,
timing helpers, sequencing, or state machine when those are under test.

Keep adapters and harness glue outside the behavioral core. Allow a conformance
consumer to depend on both driver and model without creating an implementation
dependency in either direction. Choose a module, test helper, workspace crate,
or other package shape only from the repository's current needs. Do not inherit
another model's packaging as precedent, create a support crate for hypothetical
reuse, or add policy machinery disproportionate to the leakage risk.

## Require discriminating evidence

For an implementation or review, require evidence proportional to the claim:

- model-only tests of declared reset, transition, timing, and limitation
  behavior without the production driver;
- driver-versus-model tests through the driver's public boundary;
- stable repeated observation at an unchanged temporal frontier;
- timing boundaries and partition equivalence when duration matters;
- unsupported adjacent inputs that prove the fidelity boundary is executable;
- no-op-delay failure for timing-sensitive conformance;
- evidence that the suite discriminates a material false-pass risk; introduce
  a deliberate defect only when ordinary tests do not already demonstrate it;
  and
- the repository's existing canonical validation, packaging, and dependency
  checks rather than a second model-specific policy gate.

Do not describe model agreement as silicon, electrical, analog, performance,
or board-level evidence.

## Produce a bounded handoff

For scoping, produce an issue with these sections when applicable:

- purpose and minimum useful claim;
- evidence and behavioral-selection boundary;
- required inputs, state, observations, and transitions;
- acceptance traces and discrimination evidence;
- explicit exclusions and unsupported adjacent behavior;
- independence and proportionality constraints; and
- maintained declaration and validation requirements.

For implementation, report the exact claim delivered, validation performed,
known limitations, and any evidence requiring shared guidance to change.

For review, lead with actionable findings ordered by consequence. Distinguish
violations of normative requirements from non-normative refinements and open
coordination questions. Do not resolve or dismiss review discussion unless the
user requests it.
