# Device behavioral model implementation brief

Status: **Non-normative agent and contributor aid**

## Required input

Read the normative core of the
[Device Behavioral Model Standard](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md)
before using this brief. Sections 1 and 3 through 8 remain mandatory input to
the work.

This brief deliberately does not summarize or replace those requirements. Its
omission of a rule does not waive that rule, and its procedural ordering does
not create another acceptance standard. If a task packet, repository document,
or this brief conflicts with the normative core, the normative core controls.

## Task

Implement the smallest deterministic device behavioral model that predicts the
declared source behavior needed by its current tests or consumer.

Use the
[behavioral declaration template](MODEL_DECLARATION_TEMPLATE.md) as the issue
intake when useful. Before implementation:

1. Identify the exact device identity, behavioral selection, source revision,
   source URL, and recorded digest.
2. Define observable outputs and explicit ordered inputs: transport operations,
   applied stimuli, relative duration where behavior depends on it, and any
   injected events.
3. Classify relevant behavior as modeled, abstracted, injected, excluded, or
   unsupported.
4. Record genuine source ambiguity and the selected interpretation. Do not
   invent behavior for a source-undeclared sequence.

During implementation, apply the normative core and reason locally only about
behavior specific to the selected device and pinned sources. Keep additional
artifacts proportional to a current behavior, consumer, or false-pass risk.

Do not use this brief to introduce a support crate, generic framework,
coordinator trait, adapter family, policy script, or new document set for
hypothetical reuse.

At handoff:

- Prune the intake and graduate its durable answers into one behavioral
  declaration in an existing maintained location.
- Provide tests proportional to the model's claim and false-pass risks.
- State exactly what passing tests establish and what they do not establish.
- Escalate an insufficient shared rule with evidence rather than establishing a
  conflicting local convention.

No crate, module, trait, method, adapter, test, or packaging layout is implied
by this brief.
