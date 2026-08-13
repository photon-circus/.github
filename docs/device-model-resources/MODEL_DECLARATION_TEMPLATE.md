# Device behavioral model declaration template

Status: **Non-normative content template**

Copy the useful sections into the model's existing README or module
documentation. Replace prompts, remove inapplicable entries, and keep one
maintained declaration rather than preserving this template as a second file.

## Claim

- Device identity and behavioral selection:
- Purpose and current consumer:
- What agreement with this model establishes:
- What agreement with this model does not establish:

## Sources

- Primary source, revision, and date:
- Provenance or integrity record:
- Additional evidence, if any:

## Behavioral boundary

### Inputs

- Transport operations:
- Applied stimuli:
- Relative-duration input and unit, or why elapsed duration has no modeled
  consequence:
- Injected events:

### Outputs and observations

- Device responses:
- Device outputs visible outside the transport:
- Pure inspection, if exposed:

### State and mutation

- State retained by the device:
- Inputs that permit mutation:
- Documented transport side effects:
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
  - Evidence:
  - Interpretation:
  - Observable consequence:

## Independence and proportionality

- How derivation remains independent of the production implementation:
- Why the chosen packaging fits this repository:
- Any supporting artifact beyond the model and tests, and the current value
  that justifies it:

## Known limitations and change discipline

- Model limitations distinguishable from device responses:
- Evidence that could revise the baseline or introduce a silicon variant:
- Deferred harness or coordination concerns intentionally left unresolved:
