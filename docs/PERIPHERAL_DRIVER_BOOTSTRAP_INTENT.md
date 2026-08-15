# Peripheral Driver Bootstrap Intent

Status: **Non-normative design intent — machinery not yet implemented**

Recorded: **2026-08-12 UTC**

This document adds no repository requirement. Its imperatives and uses of
"must" describe advisory constraints for any future machinery; the normative
standards control if this design intent conflicts with them.

This document preserves the constraints for future local machinery that helps a
maintainer bootstrap a narrow peripheral-driver repository from vendor source
material. It is not a task plan, an agent prompt, a generated workspace, or a
claim that the machinery currently exists.

Non-executable
[device behavioral model resources](device-model-resources/README.md) help
apply the current model standard. They are not the workspace templates,
supervisor tooling, or generated bootstrap machinery deferred by this document.

The purpose of the workflow is to make the expensive initial reasoning
repeatable without committing temporary coordination scaffolding to the driver
repository or allowing one implementation to validate itself.

## Authority boundary

The workflow is supervised assistance. It may decompose work, assemble temporary
workspaces, track bounded tasks, run checks, and prepare evidence for review. It
may record what cited evidence supports, refutes, or leaves undefined. It must
not turn that evidence state into driver or model policy, invent unsupported
behavior, or create a validation assignment merely because information is
missing. It also must not independently authorize:

- a new product scope or public guarantee;
- lifecycle promotion;
- hardware or silicon claims;
- removal of a publication lock;
- crates.io publication or a release;
- repository visibility or organization-setting changes.

Those remain explicit maintainer decisions supported by evidence appropriate to
the decision. Evidence state itself is not an approval state: an undefined
proposition may remain undefined without being assigned to a maintainer.

## Feature survey, then consumer demand

Every run begins with identified source material, not an inferred API or an old
driver implementation. Its first result is a disposable feature survey: what
externally observable capabilities the peripheral appears to provide and where
the sources discuss them. The survey does not propose a Rust API, driver
sequence, model state machine, test inventory, or stable proposition registry.
It exists to support product-scope selection and is discarded after handoff.

Only after selecting the current driver and model product slice should the
workflow promote evidence into maintained propositions. Add the smallest atomic
proposition only when current driver behavior, model behavior, conformance,
scoped physical work, or a reported bug needs the referent. A source section
with no consumer creates no repository fact, feature, test, issue, or validation
obligation.

For sources that a selected proposition actually cites, intake records where
available:

- the official source URL and issuing authority;
- document identity, revision, and publication date;
- retrieval date, exact byte length, and cryptographic digest;
- redistribution rights or the absence of them;
- supersession relationships and conflicts relevant to the proposition;
- the exact locations used by the proposition; and
- applicable ambiguity, conflict, and located-negative scope.

Vendor material is not copied into a public repository without explicit
redistribution permission. The resulting driver repository retains only the
source identity and provenance its propositions need, in a representation
selected for actual consumers, not unlicensed source documents.

## Bounded work packets

The supervisor decomposes selected consumer work into small packets with one
reviewable outcome. A packet records:

- a temporary work identifier and narrow consumer question;
- applicable stable proposition identifiers;
- exact source sections or pages;
- prerequisites and lane ownership;
- the artifact or decision expected;
- acceptance checks and evidence produced;
- forbidden dependencies and explicit non-goals;
- status, unresolved ambiguity, and review outcome.

Work identifiers are coordination labels, not evidence propositions, and do not
graduate into the repository merely because a packet existed. Packets normally
follow observable behavior domains such as transport,
addressing, register access, data conversion, state transitions, interrupts,
timing bounds, reset behavior, error recovery, and public operations. The
decomposition must not assume that every source section becomes a fact or
feature.

## Independent work lanes

The temporary workspace keeps three derivation lanes distinct:

1. **Driver lane** — independently derives the transport-facing driver from the
   shared propositions and verifies exact operations with scripted transports.
2. **Model lane** — independently implements an observable device model from the
   same shared propositions, without using driver behavioral logic.
3. **Conformance lane** — independently derives black-box scenarios and expected
   observations from the shared propositions selected for both components.

The model must not reuse driver register codecs, sequencing helpers, private
types, or scripted expectations for the behavior it is intended to challenge.
Public value types may be shared when they express the API rather than its
implementation. Agreement between driver and model is evidence only when their
derivation remains meaningfully independent.

The conformance lane compares public behavior. A disagreement returns to the
shared proposition and becomes two local questions: what the driver can promise
and what the model can support. Either may remain unsupported. It is not
resolved merely by changing one side until the test passes or by inventing a
repository-wide interpretation rule.

## Temporary workspace

Bootstrap coordination belongs outside the product repository, preferably in a
disposable sibling workspace. The future machinery should assemble a versioned
template containing concepts equivalent to:

```text
bootstrap.toml
sources/
tasks/
lanes/driver/
lanes/model/
lanes/conformance/
decisions/
evidence/
handoff/
```

The manifest tracks template version, source identity, task dependencies, lane
ownership, status, outputs, evidence, and maintainer decisions. Separate
branches or worktrees should be used where they materially preserve lane
independence.

The workspace is disposable coordination state. It must not become a second
architecture or an undocumented source of product requirements.

## Graduation into the driver repository

Temporary artifacts enter the driver repository only when they become durable
product evidence or guidance. Possible base driver artifacts, admitted only
when currently consumed, include:

- a source and stable-proposition evidence record;
- a bounded README contract and lifecycle warning;
- driver code and implementation-focused tests;
- durable rationale whose recurrence justifies preserving it and limitations of
  current public claims;
- canonical local CI and supported-target checks;
- changelog entries describing observable value and constraints.

When the independent model and conformance lanes complete, additive graduated
artifacts include:

- independently implemented model code and model tests;
- public driver-versus-model conformance tests; and
- one model fidelity declaration and explicit coverage limitations.

Agent roles, work assignments, scratch interpretations, duplicated source
extracts, orchestration state, temporary task prompts, and unconsumed source
facts do not graduate. Uncertainty becomes a bounded GitHub issue only when it
blocks a current acceptance criterion and a feasible completion condition can
be named.

## Template and machinery home

Reusable workspace templates and supervisor tooling belong in a dedicated
Photon Circus Tooling repository, separate from both organization standards and
product drivers. The recommended future repository name is
`ph-peripheral-bootstrap`. It should begin private and `Incubating`, use tagged
template versions, and be created only when an initial implementation bound is
approved.

The organization `.github` repository records the governing intent. It must not
accumulate executable bootstrap machinery or generated workspaces.

`ph-driver-standards` is not a policy authority, template source, or dependency
for this workflow. Historical analysis in that repository must not be imported
wholesale. Any surviving principle must be re-evaluated and adopted explicitly
through the organization standards before use. Retirement, archival, visibility
change, or deletion of that repository remains a separate maintainer decision.

## Relationship to driver qualification

Bootstrap completion does not qualify hardware. Before `ph-hil` is available,
the result may be public as an Experimental or Incubating driver with an
explicit warning describing its actual validation. It may retain a publication
lock or, through a separate maintainer decision, use an explicit SemVer
prerelease for registry distribution. A later ordinary software release follows
the release gate independently of model completeness or hardware qualification.
Physical evidence addresses only the stable propositions and supported claims
named by its scope and, where a model exists, may test whether the independent
model reflects supported silicon. Admit physical work only when a current
driver, model, conformance, qualification, or bug consumer—or one explicitly
selected bounded confirmation question—names the proposition, a feasible
discriminating observation, the silicon and setup scope, and a durable evidence
destination. Otherwise do not schedule or claim physical confirmation. Preserve
the existing evidence record;
an already-undefined proposition remains undefined. Missing physical work does
not retroactively justify speculative HIL scaffolding during bootstrap.

## Non-goals of the first machinery

The first implementation should not attempt to:

- generate a complete driver without maintainer review;
- inventory every data-sheet fact or promote the disposable feature survey into
  a maintained contract;
- create a proposition, issue, hardware task, decision record, or CI rule merely
  because a source is silent or a future consumer might exist;
- encode "maintainer will validate," an unchecked box, or a review owner as a
  substitute for evidence;
- infer electrical or board behavior from host tests;
- create MCU examples or speculative fixture code;
- enforce organization policy or remediate repositories;
- manage releases, publishing credentials, or GitHub settings;
- preserve every exploratory artifact indefinitely;
- generalize beyond peripheral drivers before real repetition establishes a
  stable wider boundary.

The intended result is modest: a local supervisor can repeatedly turn selected
capabilities and pinned source material into small, reviewable, independently
derived work while evidence remains honest and product, visibility, lifecycle,
and release decisions remain explicit.
