# Device behavioral model declaration template

Status: **Non-normative content template**

Use the useful sections as the implementation issue body. At handoff, replace
the prompts, remove inapplicable entries, and graduate the durable answers into
the model's existing README or module documentation. Keep that location as the
one maintained declaration; the issue remains discussion history.

This template elicits device-specific answers only. Reading and applying the
normative core of the
[Device Behavioral Model Standard](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md) is
still required; completing these prompts is not a substitute.

## Claim

- Device identity and behavioral selection:
- Purpose and current consumer:
- Minimum useful behavioral execution trace, not an expected-call transcript:
- What agreement with this model establishes:
- What agreement with this model does not establish:
- Concrete expansion trigger:

## Sources

- Primary source URL, revision, and date:
- Recorded digest and provenance or integrity record:
- Additional evidence, if any:
- Source-backed preconditions and expected result for each transition in the
  minimum trace:

## Behavioral boundary

### Inputs

- Transport operations:
- Accepted operation shapes, values, and field combinations:
- Supported sequencing, repetition or cardinality, and terminal-state behavior:
- Adjacent unsupported inputs and rejection behavior:
- Applied stimuli:
- Relative-duration input and unit, or why elapsed duration has no modeled
  consequence:
- Injected events:

### Outputs and observations

- Device responses:
- Device outputs visible outside the transport:
- Outputs unavailable until an establishing input:
- Pure inspection, if exposed:

### State and mutation

- State retained by the device:
- Observable status derived from the authoritative lifecycle, plus any
  deliberately redundant state and its invariant:
- For each observable initial value, its source, explicit input, declared
  abstraction, or first establishing transition:
- Inputs that permit mutation:
- Documented transport side effects:
- Inputs rejected before mutation, and earlier-phase effects preserved when a
  limitation becomes knowable only later:
- Stable behavior at an unchanged temporal frontier:

## Fidelity

| Classification | Included behavior |
| --- | --- |
| Modeled | |
| Abstracted | |
| Injected | |
| Excluded | |
| Unsupported | |

## Source decisions

Record only decisions needed to interpret genuine ambiguity or bound
source-undeclared behavior. Include source locations and issue links where
available.

- Decision:
  - Source section or evidence:
  - Interpretation:
  - Observable consequence:

## Independence and proportionality

- How derivation remains independent of the production implementation:
- Why the chosen packaging fits this repository:
- Any supporting artifact beyond the model and tests, and the current value
  that justifies it:
- How adapters preserve model limitations for callable but unsupported
  operations:

## Discrimination evidence

- Model-only evidence for the minimum useful trace:
- Unsupported-input evidence, distinguishing pre-commit rejection from
  preservation of earlier accepted transport-phase effects:
- Sequence, repetition, and terminal-state boundary evidence:
- Timing-sensitive evidence that would fail with no advancement, if applicable:
- Temporal frontier checkpoints and unit-bearing partition arithmetic, if
  applicable:
- Why broader behavior is not needed by the current consumer:

## Known limitations and change discipline

- Model limitations distinguishable from device responses:
- Evidence that could revise the baseline or introduce a silicon variant:
- Deferred harness or coordination concerns intentionally left unresolved:
