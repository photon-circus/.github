# Peripheral Driver Bootstrap Intent

Status: **Design intent — machinery not yet implemented**

Recorded: **2026-08-12 UTC**

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
must not independently authorize:

- source interpretations that affect supported behavior;
- lifecycle promotion;
- hardware or silicon claims;
- removal of a publication lock;
- crates.io publication or a release;
- repository visibility or organization-setting changes.

Those remain explicit maintainer decisions supported by reviewed evidence.

## Source-first intake

Every run begins with identified source material, not an inferred API or an old
driver implementation. Intake records, where available:

- the official source URL and issuing authority;
- document identity, revision, and publication date;
- retrieval date, exact byte length, and cryptographic digest;
- redistribution rights or the absence of them;
- supersession and conflict precedence;
- known ambiguities and claims that require physical evidence.

Vendor material is not copied into a public repository without explicit
redistribution permission. The resulting driver repository receives a
machine-readable metadata registry, not unlicensed source documents.

## Bounded work packets

The supervisor decomposes the source into small packets with one reviewable
outcome. A packet records:

- a stable identifier and narrow question;
- exact source sections or pages;
- prerequisites and lane ownership;
- the artifact or decision expected;
- acceptance checks and evidence produced;
- forbidden dependencies and explicit non-goals;
- status, unresolved ambiguity, and review outcome.

Packets normally follow observable behavior domains such as transport,
addressing, register access, data conversion, state transitions, interrupts,
timing bounds, reset behavior, error recovery, and public operations. The
decomposition must not assume that every source section becomes a feature.

## Independent work lanes

The temporary workspace keeps three derivation lanes distinct:

1. **Driver lane** — implements the transport-facing driver from the pinned
   vendor sources and verifies exact operations with scripted transports.
2. **Mock lane** — independently implements an observable device model from the
   same pinned sources, without using driver behavioral logic.
3. **Validation lane** — independently derives black-box scenarios and expected
   observations from the sources.

The mock must not reuse driver register codecs, sequencing helpers, private
types, or scripted expectations for the behavior it is intended to challenge.
Public value types may be shared when they express the API rather than its
implementation. Agreement between driver and mock is evidence only when their
derivation remains meaningfully independent.

The validation lane compares public behavior. A disagreement becomes a bounded
source-interpretation task; it is not resolved merely by changing one side until
the test passes.

## Temporary workspace

Bootstrap coordination belongs outside the product repository, preferably in a
disposable sibling workspace. The future machinery should assemble a versioned
template containing concepts equivalent to:

```text
bootstrap.toml
sources/
tasks/
lanes/driver/
lanes/mock/
lanes/validation/
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
product evidence or guidance. Expected graduated artifacts include:

- a source registry;
- a bounded README contract and lifecycle warning;
- driver and independently implemented mock code;
- public black-box and transport tests;
- a reconciled behavioral-model contract;
- durable design decisions and unresolved limitations;
- canonical local CI and supported-target checks;
- changelog entries describing observable value and constraints.

Agent roles, work assignments, scratch interpretations, duplicated source
extracts, orchestration state, and temporary task prompts do not graduate.
Unresolved work that needs durable coordination may become a bounded GitHub
issue.

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
explicit datasheet-model warning and publication lock. The later physical
evidence process validates whether the independent model reflects supported
silicon; it does not retroactively justify speculative HIL scaffolding during
bootstrap.

## Non-goals of the first machinery

The first implementation should not attempt to:

- generate a complete driver without maintainer review;
- infer electrical or board behavior from host tests;
- create MCU examples or speculative fixture code;
- enforce organization policy or remediate repositories;
- manage releases, publishing credentials, or GitHub settings;
- preserve every exploratory artifact indefinitely;
- generalize beyond peripheral drivers before real repetition establishes a
  stable wider boundary.

The intended result is modest: a local supervisor can repeatedly turn pinned
source material into small, reviewable, independently derived work while the
maintainer retains every consequential decision.
