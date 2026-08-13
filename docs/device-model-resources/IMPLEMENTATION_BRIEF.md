# Device behavioral model implementation brief

Status: **Non-normative agent and contributor aid**

Apply the normative decisions in the
[Device Behavioral Model Standard](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md).
Reason locally only about behavior specific to the selected device and pinned
sources.

## Task

Implement the smallest deterministic device behavioral model that predicts the
declared source behavior needed by its current tests or consumer.

Before implementation:

1. Identify the exact device identity, behavioral selection, source revision,
   and source provenance.
2. Define observable outputs and explicit ordered inputs: transport operations,
   applied stimuli, relative duration where behavior depends on it, and any
   injected events.
3. Classify relevant behavior as modeled, abstracted, injected, excluded, or
   unsupported.
4. Record genuine source ambiguity and the selected interpretation. Do not
   invent behavior for a source-undeclared sequence.

During implementation:

- Keep the model quiescent between explicit inputs.
- Keep harness time, environmental truth, topology, and orchestration outside
  the device.
- Distinguish a device response from an unsupported model input.
- Derive device behavior independently of the production implementation.
- Add only complexity attributable to source-backed behavior or a current
  consumer.
- Do not introduce a support crate, generic framework, coordinator trait,
  adapter family, policy script, or new document set for hypothetical reuse.

At handoff:

- Complete one behavioral declaration in an existing maintained location.
- Provide tests proportional to the model's claim and false-pass risks.
- State exactly what passing tests establish and what they do not establish.
- Escalate an insufficient shared rule with evidence rather than establishing a
  conflicting local convention.

Packaging is a repository choice. No crate, module, trait, or method layout is
implied by this brief.
