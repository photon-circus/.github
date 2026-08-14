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

1. Write one **minimum useful execution trace** for the current consumer. State
   the observable agreement it can establish and the concrete future need that
   would justify expanding it. Use the trace to bound semantic behavior, not as
   a queue of expected driver calls; source-equivalent operation sequences
   remain valid unless ordering itself is part of the declared device behavior.
2. Identify the exact device identity, behavioral selection, source revision,
   source URL, and recorded digest.
3. Audit the proposed trace against those sources and the explicit behavioral
   selection. For every selected value and transition, identify the pinned
   source, recorded interpretation, or reviewed evidence-backed silicon variant
   that establishes its precondition and expected observable result. A vector
   is not authorized merely because it distinguishes two plausible
   implementations; if no accepted source, decision, or variant evidence
   establishes its result, choose an established trace or declare the behavior
   unsupported.
4. Define observable outputs and explicit ordered inputs: transport operations,
   applied stimuli, relative duration where behavior depends on it, and any
   injected events.
5. Audit every observable initial value. Record its source-backed default,
   explicit initial input, declared abstraction, or the input that first makes
   it available. Do not fill an undeclared value with zero, `false`, empty, or
   another convenient result merely to make the implementation deterministic.
   Check whether the establishing input covers the whole observable; if it
   covers only part, keep the rest unavailable, report it distinguishably, or
   declare an abstraction for it.
6. Define the accepted input domain narrowly enough to implement that trace:
   operation and transaction shapes, addresses or commands, values, and field
   combinations, together with supported sequencing, repetition or cardinality,
   and terminal-state behavior. State which adjacent unsupported inputs can be
   rejected before mutation and which earlier-phase effects remain committed
   when a limitation becomes knowable only later. Avoid a transcript tailored
   only to the current driver. An operation needed once by the minimum trace
   does not become repeatable merely because the state machine can accept it
   again.
7. Classify relevant behavior as modeled, abstracted, injected, excluded, or
   unsupported.
8. Record genuine source ambiguity and the selected interpretation. Do not
   invent behavior for a source-undeclared sequence.

During implementation, apply the normative core and reason locally only about
behavior specific to the selected device and pinned sources. Keep additional
artifacts proportional to a current behavior, consumer, or false-pass risk.
Implement only the retained state and transitions required by the minimum
useful trace. An operation is not supported merely because the model can store
its value or continue its state machine.

Prefer one authoritative representation for the current lifecycle and derive
observable status from it when that keeps the model clear. If behavior requires
redundant retained state, document and test the invariant that relates the
representations. This is an auditability aid, not a required enum, transition
table, mutation style, or Rust architecture.

Keep driver or framework adapters outside the behavioral core. If a required
interface exposes an operation outside the model's claim, preserve a typed or
otherwise distinguishable model limitation rather than panic or fabricate a
device response. For timing-sensitive conformance, route driver delay intent to
the same explicit relative-duration input used by focused model tests.

Do not use this brief to introduce a support crate, generic framework,
coordinator trait, adapter family, policy script, or new document set for
hypothetical reuse.

At handoff:

- Prune the intake and graduate its durable answers into one behavioral
  declaration in an existing maintained location.
- Provide tests proportional to the model's claim and false-pass risks.
- For a declared temporal frontier, include an observation immediately before
  it, verify the transition at the frontier, and make the unit-bearing
  partition arithmetic visibly total the intended duration. Equivalent final
  states alone do not demonstrate that a partition avoided overshooting the
  boundary.
- Include focused checks that source-undeclared initial outputs are not
  invented; unsupported inputs do not mutate state when complete validation
  information is available before commitment; effects from an earlier accepted
  transport phase remain when a limitation becomes knowable only later;
  sequencing, repetition, and terminal-state behavior match the declared input
  domain; repeated observation at an unchanged temporal frontier is stable;
  and a no-op delay cannot make a timing-sensitive conformance test pass.
- State exactly what passing tests establish and what they do not establish.
- Escalate an insufficient shared rule with evidence rather than establishing a
  conflicting local convention.

No crate, module, trait, method, adapter, test, or packaging layout is implied
by this brief.
