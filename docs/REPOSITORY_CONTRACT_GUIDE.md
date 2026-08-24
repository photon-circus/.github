# Photon Circus Repository Contract Guide

Status: **Non-normative guidance**

Scope: All Photon Circus repositories and all material components they contain,
including crates, libraries, executables, firmware, tools, behavioral models,
schemas, hardware sources, documentation, generated artifacts, examples, and
repositories that contain no Rust crates.

Audience: Maintainers, contributors, reviewers, and coding agents drafting or
evaluating a repository-local contract.

This guide adds no requirements. The adopted
[Photon Circus Repository Standards](../REPOSITORY_STANDARDS.md)
control if this guide conflicts with them. Specialized normative material also
controls where it applies, including the
[Peripheral Driver Release and Evidence Profile](PERIPHERAL_DRIVER_PROFILE.md)
and Sections 1 and 3 through 8 of the
[Device Behavioral Model Standard](DEVICE_BEHAVIORAL_MODEL_STANDARD.md).
Sections 2 and 9 through 11 of the model standard are explanatory guidance.
Every recommendation, imperative, use of "should," and template sentence in
this guide is advisory. "Must" and "required" appear only when this guide
summarizes an existing linked requirement; consult the normative source for the
exact obligation.

A maintained contract can be authoritative for repository-local product
semantics when it is consistent with adopted organization standards. It cannot
create organization policy or authorize lifecycle, release, deployment, or
physical-operation decisions. Link the decision that made the contract current
when its authority would otherwise be ambiguous.

## 1. Recommended organizing rule

A useful repository contract gives durable answers to ten questions:

1. What is this repository, and what state is it in now?
2. Who or what does it serve?
3. What responsibility and invariants does it own?
4. What does it deliberately leave elsewhere?
5. Which artifacts and observable behavior does it expose?
6. Under which conditions, constraints, and trade-offs do its claims hold?
7. What evidence supports those claims?
8. What condition makes the current responsibility complete or stable?
9. Which changes affect compatibility or the contract?
10. How are contract changes reviewed and authorized?

The contract is the maintained repository-level account of responsibility,
limits, and reliance. It lets a reader determine whether support is claimed
and, if so, whether a use falls inside it. It also lets a contributor decide
whether a change belongs and a reviewer decide whether the change widens a
promise.

"Repository contract" names that responsibility surface, not a mandatory
filename. The adopted standards already require every repository to define a
[bounded responsibility](../REPOSITORY_STANDARDS.md#4-bounded-scope-and-invariant-ownership)
and to answer the
[README-contract questions](../REPOSITORY_STANDARDS.md#6-readme-contract)
near the top of its root `README.md`. A small repository can keep the complete
contract there. A larger repository can keep the concise repository contract
in the README and link to a detailed `CONTRACT.md`, `docs/CONTRACT.md`,
architecture document, component contract, schema, or evidence record. A
linked specialist document does not replace the seven answers required near the
top of the root README.

Use the repository contract to classify any crate or component whose role
affects consumer reliance, compatibility, evidence, release, safety, or
repository cohesion. That does not mean every helper needs an inventory row,
every crate needs a separate contract document, or every component inherits
every repository-wide claim. The repository contract explains material
aggregation, inheritance, and component-specific applicability.

For a newly created repository, this guide calls the first version the
**initial development contract**. Writing it does not by itself make proposed
work implementation-ready; a separate recorded decision authorizes applicable
implementation. When the adopted
[feature-state process](../REPOSITORY_STANDARDS.md#121-feature-states)
applies, an implementation decision moves the proposal to `Committed` only when
it also establishes the expectation that the feature will enter a release.
Permission to prototype or gather evidence alone does not create that release
commitment. The contract can guide authorized implementation while remaining
explicitly provisional rather than fixed in stone. Its trigger identifies when
the initial operations or artifacts, consumer path, and evidence entry point
are available to challenge the boundary. Reaching that trigger starts a
deliberate contract review; it does not silently make the draft current,
promote lifecycle, create compatibility, or authorize release.

## 2. Keep authority levels distinct

Several useful documents can contain contract-like language without owning the
same subject.

| Surface | Recommended role | It does not become merely by existing |
| --- | --- | --- |
| Organization standard | Common organization-wide floor | A repository-specific design |
| Repository contract | Local responsibility, boundaries, claims, completion, and evidence posture | An organization-wide rule |
| Component or crate contract | Semantics of one independently meaningful component | The contract of every workspace member |
| API, schema, hardware, or protocol specification | Detailed meaning of one interface or artifact | A complete repository boundary |
| Architecture or decision record | Ownership, dependency direction, or retained rationale | A current support or evidence claim |
| Roadmap, proposal, or issue | Intended or possible future work | A present commitment or authorization to implement |
| Test plan or evidence record | How claims are tested, or what was observed | The claim itself or a broader qualification |
| Release guide | Mechanics and approval path for a release | Authorization to publish, tag, promote, or change visibility |

Prefer one canonical owner for each maintained fact. Other surfaces can state
their local consequence and link to that owner. Copying the same promise into
the README, contract, rustdoc, test plan, and agent instructions makes drift
more likely, not the promise stronger.

A repository contract also does not grant external authority. Completing it
does not by itself authorize publication, a tag, a GitHub Release, a visibility
change, a lifecycle transition, deployment, physical operation, or hardware
qualification. Record those decisions through their own maintained process.

## 3. Begin with a bounded promise

Draft one sentence before drafting sections. One workable form is:

> `<repository>` provides `<artifact or capability>` for `<named consumer or
> context>` and owns `<observable outcome or invariant>`; `<adjacent
> responsibility>` remains with `<other layer, repository, or operator>`.

A strong sentence usually:

- names one coherent problem rather than listing features;
- identifies a real consumer, use context, or engineering outcome;
- states an observable responsibility rather than an aspiration;
- survives an internal directory or implementation change; and
- implies a useful reason to reject or relocate an adjacent feature.

If the sentence needs several unrelated conjunctions, the repository may need
a cohesion review. A workspace can contain many components while still owning
one responsibility; one-crate purity is not the goal.

## 4. Draft from consumers and handoffs

Repository boundaries become clearer when written from both sides. For each
material consumer or neighboring system, consider recording:

- what it receives from this repository;
- what it is permitted to rely on;
- what conditions it supplies;
- which failures or uncertainties remain for it to handle; and
- which responsibility resumes on its side of the handoff.

"Owns" is otherwise easy to overread. Useful distinctions include:

| This repository may own | Without thereby owning |
| --- | --- |
| An implementation | Every system behavior involving that implementation |
| An API or integration point | Correct composition, scheduling, deployment, or operator policy |
| A generated artifact | The truth, safety, or suitability of its source inputs |
| A behavioral model | The physical device or every unmodeled behavior |
| A conformance harness | Qualification beyond the propositions and cases exercised |
| Hardware design sources | Fabrication quality, assembly correctness, safe energization, or product certification |
| Documentation wording | The external specification, device fact, or implementation behavior it describes |
| A test command | Claims outside the checks that command actually performs |

Stable repository, component, integrator, and operator boundaries are usually
more durable than ownership assigned to a named individual.

Where a handoff is consequential, a small table can expose it:

| Responsibility | Owned here | Source or input authority | Downstream owner | Handoff artifact |
| --- | --- | --- | --- | --- |
| `<bounded responsibility>` | `<repository or component>` | `<specification, source, or input>` | `<consumer or operator>` | `<API, file, image, board, report, or command>` |

## 5. Suggested contract anatomy

The following sections are prompts, not a mandatory document shape. Combine,
rename, or omit them when the repository remains unambiguous.

### 5.1 Identity and current state

State what the repository is in one factual sentence, then separate status
dimensions that readers might otherwise collapse:

| Dimension | Useful question |
| --- | --- |
| Repository lifecycle | Which adopted Photon Circus lifecycle describes the repository? |
| Repository domain | Which adopted Photon Circus domain or domains describe the work? |
| Visibility | Is the GitHub repository public or private? |
| Distribution | Which packages, binaries, images, documents, or fabrication outputs are published or unpublished? |
| Implementation state | Which declared surfaces exist, and which remain incomplete? |
| Compatibility | Which interfaces or artifacts, if any, carry a compatibility promise? |
| Evidence | What has been built, inspected, modeled, observed, or qualified, and at what scope? |
| Operational status | Is anything deployed, supported in use, or approved for a physical operation? |

Only show dimensions that resolve a likely ambiguity. Do not make every
repository display irrelevant model, hardware, registry, or deployment fields.
When a repository uses a local status, describe its meaning in plain terms—for
example, proposed, governing implementation target, current for named versions
or surfaces, historical, or superseded. Keep it distinct from organization
lifecycle and feature-state terms, and link its approving or superseding
decision when relevant.

### 5.2 Purpose, consumers, and use contexts

Name the problem, the current consumers, and the context in which the
repository is valuable. A consumer can be another crate, a firmware image, a
maintainer workflow, a physical build, a contributor, an operator, or a person
using an installation.

Named consumers are especially useful when they govern feature admission.
Avoid inventing hypothetical consumers merely to justify a broad abstraction.

### 5.3 Responsibility and invariants

Describe outcomes the repository is responsible for preserving. Record
load-bearing invariants only when violating them would make the repository's
promise untrue, unsafe, incompatible, or misleading.

Depending on the repository, these may concern:

- value meaning, units, ranges, rounding, overflow, or determinism;
- state authority, transitions, failure, retry, cancellation, and recovery;
- dependency direction and resource ownership;
- input, output, serialization, identity, provenance, or mutability;
- concurrency, memory, timing, allocation, or target constraints;
- electrical, mechanical, fabrication, or assembly boundaries;
- model fidelity, conformance scope, observation, or evidence retention; or
- canonical documentation ownership and normative versus explanatory text.

Do not turn ordinary implementation details into permanent commitments. A
directory tree, private type name, or current dependency belongs only when a
consumer or invariant genuinely relies on it.

### 5.4 Non-goals, deferred work, unknowns, and exclusions

Keep four ideas separate:

| Category | Meaning |
| --- | --- |
| Non-goal | Deliberately outside the repository responsibility |
| Deferred | Plausibly in scope later, but not part of the current promise |
| Unknown | The answer or evidence is not currently established |
| Unsupported | A context or configuration for which no support claim is made |

Name where an adjacent responsibility belongs when known. "Not here" is more
useful when paired with "owned by integration," "retained in the source
specification," "decided by the operator," or another explicit handoff.

A non-goal is not necessarily permanent. A later reviewed contract change can
move a responsibility. A useful change process updates the contract before
implementation crosses the existing boundary.

### 5.5 Components and artifacts

Account for each component whose role could change how a reader interprets
consumption, compatibility, evidence, release, safety, or repository cohesion.
This includes non-crate artifacts when they are material.

| Component or artifact | Role and consumer | Supported surface or internal aid | Distribution and compatibility | Release relationship | Canonical local detail |
| --- | --- | --- | --- | --- | --- |
| `<name/path>` | `<bounded role>` | `<supported/internal/example/generated>` | `<exact posture>` | `<lockstep/independent/not released>` | `<README, rustdoc, schema, or design link>` |

The table need not inventory incidental test helpers or every source directory.
Its purpose is to prevent a primary crate's claims from silently attaching to
generators, CLIs, models, examples, fixtures, experiments, or other workspace
members.

### 5.6 Observable commitments

State what a consumer can rely on and under which conditions. Prefer precise
sentences such as:

> Crate A is the published compatibility surface. Crate B is an internal
> generator and is neither independently versioned nor supported as a library.

> Given a valid format-X document and the pinned toolchain, the command emits
> byte-identical output on the documented platforms. It does not canonicalize
> or validate the truth of user assertions.

> The behavior has been observed on device revision R under configuration C.
> Other revisions remain unqualified.

Record failure, partial mutation, overload, cancellation, resource, or recovery
semantics when they are part of truthful use. A feature list without these
conditions is usually an inventory, not a contract.

### 5.7 Constraints and accepted trade-offs

Record constraints that materially shape correct use or future design. Common
examples include platform and toolchain bounds, no-network or offline behavior,
fixed capacity, allocation, latency, code size, determinism, licensing,
redistribution, privacy, destructive side effects, operator involvement, and
known formal or physical limitations.

Explain the engineering consequence of a trade-off. "Uses fixed capacity" is
more useful when the contract also states the overload behavior and who chooses
the capacity.

### 5.8 Evidence posture and verification

Map important claims to evidence of matching strength. The contract can name
stable evidence classes and canonical entry points without copying volatile
test counts or complete logs.

| Claim | Scope and conditions | Current evidence or result | Reproduction method | What the evidence does not establish |
| --- | --- | --- | --- | --- |
| `<specific claim>` | `<target, version, feature, device, setup, or input class>` | `<obtained result or retained artifact>` | `<test, review, command, model, or observation method>` | `<important limit>` |

The adopted standards require verification to follow the repository's actual
failure modes. Evidence establishes only the property actually exercised. For
example:

- a build or behavioral test establishes only its stated environment, inputs,
  cases, and properties;
- deterministic tool or generator output does not establish the truth, rights,
  safety, or authorized use of its inputs;
- schema validation establishes structural meaning, not the truth of the data;
- a discriminating comparison through a public operation can establish that
  operation's conformance to an independent model within the model's accepted
  domain, not independent silicon truth;
- a hardware observation applies to the identified device, setup, operation,
  and run unless broader evidence justifies a broader claim; and
- a skipped, unavailable, or planned check is not passing evidence.

Use current tense for current evidence. Put planned evidence and promotion work
in a proposal, issue, or roadmap. A repository can remain honest with partial
evidence when it narrows its claims accordingly.

The adopted default for a technical repository is one canonical routine
verification entry point. Identify it and explain the claims covered by any
hosted subset. If the repository deviates, link the documented reason and state
which checks are available. Do not imply that a command establishes every
contract statement. For nontechnical work, name the corresponding inspection,
rendering, or validation path.

When several components, tests, evidence records, or downstream repositories
need to cite the same consequential proposition, a stable clause or claim
identifier can prevent wording drift. A simple repository does not need a
registry or an identifier for every sentence. Applicable retained
peripheral-driver and device-model propositions remain subject to the adopted
[stable device-proposition requirements](../REPOSITORY_STANDARDS.md#102-stable-device-propositions),
which do not prescribe one registry, filename, schema, or identifier at every
code site.

### 5.9 Feature admission, compatibility, change, and completion

Use the contract to apply the adopted
[feature-admission test](../REPOSITORY_STANDARDS.md#41-feature-admission-test)
to the repository's actual responsibility, invariants, evidence, release model,
and non-goals. Link to that live test rather than maintaining a local rewrite.

Describe the compatibility unit and the events that require explicit contract
review. These might include changes to observable semantics, accepted inputs,
generated bytes, public interfaces, supported targets, evidence strength,
artifact identity, release coupling, or ownership across a repository boundary.

Also state the condition under which the current responsibility is complete or
stable. "Done" need not mean that no feature can ever be added. It can mean the
declared surface and evidence bar are satisfied, the experiment answered its
question, the hardware sources produce the retained outputs, or the
documentation covers its named audience and canonical subjects.

Keep these separate:

- implementation completion;
- repository lifecycle;
- interface stability;
- distribution or release;
- deployment or operational adoption; and
- model, physical, safety, or qualification evidence.

A contract can govern an implementation that is still incomplete. Completing
that implementation can leave distribution disabled. Publication can exist
without broad physical evidence. State the actual combination rather than
relying on one label to imply the others.

### 5.10 Exceptions and local deltas

When the contract records a standards deviation, follow and link to the live
[exceptions section](../REPOSITORY_STANDARDS.md#19-exceptions)
instead of reproducing its required fields here. Merely calling something a
contract does not legitimize an otherwise unexplained deviation.

Keep an exception distinct from ordinary local design. Choosing one optional
verification entry point, omitting an irrelevant advisory section, or adopting
a stricter local invariant is not automatically a standards exception. A local
contract cannot weaken the organization standard through silence or
contradictory wording.

## 6. Multi-crate and multi-component repositories

Treat the repository contract as the aggregation and relationship layer. Use
the component map to show repository-wide applicability, local contracts or
deltas, supported versus internal roles, version and release coupling,
dependency direction, evidence posture, and edit authority for generated or
frozen artifacts.

Repository lifecycle describes the repository. It does not automatically make
every workspace member a supported or published surface. Likewise, evidence
for one crate or artifact does not cover its siblings unless the evidence and
claim explicitly say so.

An independently consumed or released crate often benefits from a local README
or component contract. Keep shared facts at repository level and local
semantics at component level. Consumer-critical limitations need to travel with
a distributed package rather than existing only in an unpackaged private
document.

A multi-component repository remains cohesive when the components serve one
responsibility boundary, share contracts and release intent, and need
coordinated development. If a component solves a distinct problem with its own
invariants, consumers, evidence, and release cadence, consider a separate
repository or an explicit experimental arrangement rather than silently
expanding the parent contract.

## 7. Proportional prompts by repository profile

These prompts supplement the common structure; they are not additional
requirements.

| Profile | Contract questions worth answering | Common overclaim to avoid |
| --- | --- | --- |
| Shared library or published crate | Which semantics, resource bounds, features, targets, and compatibility surfaces can consumers rely on? Which policies stay downstream? | Treating "reusable" as permission to absorb every adjacent capability |
| Peripheral driver | Which supported device operations, state, timing, failure, and recovery semantics are owned? Which concrete resources and workflow policy stay in integration? | Treating model, mock, or one hardware observation as universal device qualification; use the specialized normative profile |
| Firmware, application, or experience | Which hardware, site, runtime, operator, and workflow assumptions define the system? Which safety and recovery decisions exist at this layer? | Presenting one successful installation or board bring-up as a reusable component guarantee |
| Host tool, CLI, service, or automation | What inputs, outputs, side effects, platforms, permissions, failure behavior, and reproducibility properties apply? What requires network, process, credential, or filesystem access? | Describing validation of input shape as truth, safety, or authorization to act |
| Hardware design repository | Which design boundary, revisions, source files, generated outputs, interfaces, and constraints are owned? What fabrication, assembly, inspection, and test evidence exists? | Equating ERC/DRC, simulation, or reproducible outputs with safe and qualified hardware |
| Art, media, enclosure, CAD, or reusable design assets | Which editable sources are authoritative, which exports are derived, and which format, scale, color, licensing, and provenance constraints apply? | Treating a rendered preview or visual inspection as proof that source files, dimensions, fabrication outputs, or rights are correct |
| Device behavioral model | Which observables are modeled from which independent sources? What is modeled, abstracted, injected, excluded, or unsupported? | Treating model tests as driver conformance, or model behavior as independent silicon truth; use the model standard's normative sections |
| Broader simulator or emulator | Which world, timing, topology, physics, or system abstractions are represented, and for which questions? | Calling it a device behavioral model when its responsibility or fidelity is materially broader or different |
| Conformance harness | Which systems and independent oracles are compared, through which public boundary, for which cases and accepted domains? | Letting a passing comparison cover unexercised operations, model internals, physical fidelity, or qualification |
| HIL, bench, or retained-evidence repository | Which propositions, setups, identities, operations, raw artifacts, seals, and comparison rules are owned? Which operator and safety authority remains external? | Widening one scoped run into device-family, system, or product qualification |
| Schema, data, generator, or artifact repository | Which representation is canonical, what identity and compatibility rules apply, what is generated, and which transformation is deterministic? | Treating structural validity or byte identity as semantic or physical truth |
| Documentation or standards repository | Which audience and subjects are canonical here? Which text is normative, explanatory, generated, inherited, or externally authoritative? How are links and rendering checked? | Turning examples, rationale, or inherited defaults into unstated policy |
| Example or reference repository | Which contexts and versions does the example illustrate? Which parts are copy-ready, intentionally simplified, unsupported, or noncanonical? | Making an example layout, dependency choice, or successful demo a supported organization architecture by implication |
| Experimental or meta repository | Which question, coordination function, or retained context gives the repository value? What is intentionally unsupported, mutable, or unsafe to depend on? What triggers extraction, promotion, or retirement? | Making prototype code or coordination aids a supported product surface by implication |

## 8. Recommended document placement

Choose the smallest structure that preserves a clear authority boundary.

### README-only contract

Useful when the repository has one simple responsibility and few load-bearing
semantics. Keep the adopted README questions near the top, then add only the
detail needed for truthful evaluation and verification.

### README plus one detailed contract

Useful for contract-first incubation, consequential numeric or behavioral
semantics, multiple internal components, or a definition of done that would
overwhelm the front door. Keep the README summary independently useful and link
to the detailed authority.

### README plus specialized canonical documents

Useful when architecture, schema, evidence, API, hardware, or release material
has a genuinely different audience, authority, or change cadence. Add a short
contract map so readers know which document owns which subject.

A `CONTRACT.md` filename is optional. More files are not evidence of a better
contract. Split a document because authority, audience, change cadence, or
review purpose differs, not because a template offers another heading.

## 9. Drafting workflow

One practical sequence is:

1. Inventory current artifacts, consumers, distributions, external authorities,
   evidence, unsupported assumptions, and intended future state.
2. Write the bounded promise and name responsibilities owned here and elsewhere.
3. Map material components, handoffs, dependency direction, and release units.
4. Extract the few observable commitments and invariants that make the promise
   truthful.
5. Map each important claim to current evidence, a reproduction method, and an
   explicit limit.
6. State compatibility posture, change authority, and the finite completion or
   stability condition. For an initial development contract, also name the
   re-examination trigger.
7. Choose canonical document owners and replace duplicate prose with links.
8. Review the draft from the perspectives of a consumer, contributor, reviewer,
   coding agent, integrator, and evidence owner as applicable.

Start from evidence and existing consumers rather than filling every template
slot. An honest short contract with explicit unknowns is stronger than a large
specification built from unverified assumptions.

## 10. Initial development contract and re-examination

```text
initial development contract
    -> separate recorded implementation decision
    -> implementation, evidence, and reviewed mutations
    -> named re-examination trigger
    -> revised current contract | revised initial contract | reject or supersede target
```

### 10.1 Write the initial contract before the first implementation expands

The initial development contract is a bounded design hypothesis. After a
separate recorded decision authorizes implementation, it can become the current
development target. It gives the work a responsibility, non-goals, invariants,
component relationships, intended evidence, and a finite initial surface. It
distinguishes:

- what is already known or source-backed;
- what the first implementation intends to establish;
- which assumptions remain open;
- which present-tense claims are not yet earned; and
- what event will trigger re-examination.

Label it plainly as an initial development contract. Do not describe intended
features or deliverables as current behavior merely because they appear in the
contract. A reviewed initial target can govern implementation while remaining
changeable through the recorded mutation process.

### 10.2 Let implementation and evidence challenge it

The initial contract can mutate when implementation, source material, a real
consumer, or discriminating evidence shows that an assumption, boundary, or
acceptance criterion is wrong or incomplete. Mutation is not failure; silent
drift is.

A useful contract change records:

- what changed and whether it corrects an error, narrows a claim, or expands
  scope;
- the implementation, source, consumer, or evidence that prompted the change;
- the effect on invariants, non-goals, components, compatibility, and the
  definition of complete; and
- the repository-local review path or decision that makes the revision the
  current development target.

Update the contract before or with the implementation that crosses its current
boundary. Do not relax a criterion or rewrite expected evidence solely to make
an implementation appear conformant. Preserve an earlier version through Git
history or mark a retained document historical or superseded when it remains
useful.

### 10.3 Re-examine it when the initial surface can be evaluated

The initial contract names a repository-specific re-examination trigger. A
useful trigger names the exact initial operations or artifacts, the consumer
path that exercises them end-to-end, and the evidence entry point. Re-examine
the contract when that evidence is available whether it passes, fails, or
remains partial—and earlier if implementation or evidence shows that the
initial boundary cannot be achieved. Avoid a calendar date or an undefined
phrase such as "when mostly done."

At the trigger, review the contract as a whole:

| Review surface | Question |
| --- | --- |
| Responsibility | Does the implemented repository still own one coherent problem? |
| Consumers and handoffs | Are the real consumers, inputs, outputs, effects, and downstream responsibilities accurately named? |
| Invariants and semantics | Which intended commitments survived implementation, and which need correction or narrower conditions? |
| Components | Do all material crates and artifacts still belong together, with accurate supported and internal roles? |
| Evidence and nonclaims | Which claims are now established, which remain partial or unknown, and what does the evidence still not prove? |
| Compatibility and distribution | Which facts are ready to hand to a separate authorized compatibility or distribution decision, and which surfaces remain provisional? |
| Completion | Is the initial definition of working met, or does evidence justify revising it? |

Record one of three honest outcomes:

1. Through the repository-local decision path, designate a revised contract as
   current for the named implemented surface.
2. Keep a revised initial development contract because important boundaries or
   evidence remain unsettled, and record its next concrete re-examination
   trigger.
3. Narrow, split, extract, reject, or supersede the development target when the
   implemented repository does not support the original boundary. Continue
   under the currently recorded lifecycle unless a separate authorized process
   changes it.

The re-examination does not make the contract permanently immutable. Nor does
it authorize publication, lifecycle promotion, deployment, physical operation,
or qualification. Those remain separate decisions.

## 11. Ongoing contract evolution

Consider a contract update when a change alters:

- repository or component responsibility;
- a supported consumer, environment, target, input, output, or artifact;
- an observable guarantee, non-goal, limitation, or evidence basis;
- compatibility, versioning, publication, or release coupling;
- a component's supported, internal, generated, experimental, or retired role;
- an ownership handoff across components or repositories; or
- the condition used to call the current responsibility stable or complete.

An internal refactor need not churn the contract when none of those answers
changes. Use Git history alone for non-consequential contract-document
evolution. A change to current supported scope, compatibility, limitations, or
evidence claims is an engineering consequence and follows the repository's
applicable changelog policy even when no code changes. A separately versioned
contract is useful only when consumers truly select or depend on that version.

State the repository-local decision path for contract changes: which canonical
document changes, what review or approving role makes it current, and whether a
proposal or decision record comes first. Prefer a durable role or process over
a named individual. Contract-change approval remains separate from release,
deployment, lifecycle, visibility, and physical-operation authority.

When a contract is the pre-implementation authority, mark future surfaces and
acceptance criteria clearly. When it describes a shipped surface, keep roadmap
items out of present-tense commitments. Retain rejected directions when their
rationale prevents likely repetition, but do not turn every abandoned idea
into permanent contract text.

If a contract no longer governs, label it historical or superseded and point
to the current authority. Do not leave an obsolete design target looking like
an alternative live contract.

## 12. Compact review checklist

- Can a reader state the one owned problem, current state, constraints, and
  verification path without reading specialist documents first?
- Can a maintainer decide whether an adjacent feature belongs here, and where a
  rejected responsibility belongs instead?
- Can each real consumer tell what it may rely on and what remains its
  responsibility?
- Are material crates and non-crate artifacts classified without making
  internal aids, examples, or generated outputs supported by accident?
- Are lifecycle, implementation, compatibility, distribution, and evidence
  reported as separate facts?
- Does an initial development contract distinguish intended behavior from
  current behavior and name a concrete re-examination trigger?
- Does each important claim identify its scope, current evidence, reproduction
  method, and nonclaim without inflating model, mock, inspection, or physical
  evidence?
- Is the definition of complete or stable finite and evidence-bound, without
  turning an unmet condition into an implicit assignment?
- Are contract-change triggers and the approving role clear, with old contracts
  marked historical or superseded when retained?
- Would the contract survive an internal layout refactor, or is it merely a
  feature and directory catalogue?
- Does each maintained fact have one canonical owner rather than several
  drifting prose copies?
- Does any sentence weaken a live standard or accidentally authorize release,
  publication, lifecycle promotion, deployment, visibility change, physical
  operation, or qualification?

## Appendix A: Adaptable repository-contract skeleton

This skeleton is deliberately longer than many repositories need. Delete
sections that do not clarify the boundary; do not fill them with boilerplate.

````markdown
# `<repository>` repository contract

**Repository lifecycle:** `<organization Lifecycle value>`
**Contract status and authority:** `<proposed/current/historical/superseded;
governing scope and approving decision>`
**Contract phase:** `<initial development or current for a named surface>`
**Re-examination trigger:** `<initial operations/artifacts, consumer path, and
evidence entry point; "not applicable" only for a current contract>`
**Visibility and distribution:** `<what is public/private and published/unpublished>`
**Compatibility posture:** `<exact promise or none>`
**Evidence summary:** `<current, bounded summary>`

This contract governs `<repository-local implementation or supported surface>`.
It does not by itself authorize publication, release, deployment, visibility or
lifecycle changes, physical operation, or qualification.

## 1. Purpose and current state

`<One-sentence bounded promise.>`

`<What exists now; keep planned state separate.>`

## 2. Consumers and use contexts

| Consumer or context | Uses | May rely on | Remains responsible for |
| --- | --- | --- | --- |
| `<name>` | `<artifact or behavior>` | `<bounded commitment>` | `<integration or policy>` |

## 3. Responsibility and boundaries

### Owned here

- `<outcome or invariant>`

### Outside this repository

- `<adjacent responsibility>` — owned by `<layer or repository>`, or explicitly
  unowned/deferred because `<reason>`.

### Deferred, unknown, and unsupported

- **Deferred:** `<not part of the current promise>`
- **Unknown:** `<fact or evidence not established>`
- **Unsupported:** `<configuration or use for which no claim is made>`

## 4. Components and artifacts

| Component or artifact | Role | Status/distribution | Release relationship | Local authority |
| --- | --- | --- | --- | --- |
| `<name/path>` | `<bounded role and consumer>` | `<supported/internal/generated/example/etc.>` | `<lockstep/independent/none>` | `<link>` |

Repository-wide statements apply to `<enumerated components>` except where a
component row or linked local contract says otherwise.

## 5. Observable commitments and invariants

1. `<Behavior, conditions, and failure or recovery semantics where relevant.>`
2. `<Resource, timing, identity, provenance, or determinism constraint.>`

## 6. Interfaces and ownership handoffs

| Handoff | This repository provides | Consumer supplies/owns | Failure or uncertainty boundary |
| --- | --- | --- | --- |
| `<name>` | `<API/artifact/interface>` | `<resource/context/policy>` | `<behavior>` |

## 7. Constraints and accepted trade-offs

- `<constraint>` — `<consequence and why it is accepted>`

## 8. Evidence and verification

| Claim | Scope and conditions | Current evidence or result | Reproduction method | Does not establish |
| --- | --- | --- | --- | --- |
| `<claim>` | `<exact scope>` | `<obtained result or retained artifact>` | `<command or method>` | `<limit>` |

Canonical routine verification: `<one documented entry point, or the documented
reason for deviation and available checks>`.

`<Explain skipped/unavailable checks and any hosted subset.>`

## 9. Compatibility and change control

- Compatibility unit: `<API/schema/artifact/workspace/none>`
- Contract review triggers: `<observable changes>`
- Contract change authority: `<durable role/process and governing decision>`
- Initial-development re-examination: `<trigger and defined review outcome>`
- Version/release relationship: `<exact posture>`

## 10. Definition of complete or stable

| Condition | Current assessment | Evidence |
| --- | --- | --- |
| `<finite condition>` | `<met, unmet, unknown, or other precise state>` | `<result or artifact>` |

An unmet condition records the current posture; it does not by itself create an
assignment or prove the opposite claim.

Meeting this bar does not by itself authorize `<separate decisions>`.

## 11. Canonical material

| Subject | Canonical owner |
| --- | --- |
| `<API/schema/architecture/evidence/contribution/release/etc.>` | `<link>` |
````

## Appendix B: Public contract-shape illustrations

These public repositories illustrate different document shapes. They are
examples, not organization policy, templates, or authority for another
repository's semantics.

| Shape | Public illustration | Useful lesson |
| --- | --- | --- |
| Compact explicit contract | [`ph-haptics`](https://github.com/photon-circus/ph-haptics/blob/main/docs/contract.md) | A non-driver contract can organize definition, guarantees, non-guarantees, and a finite definition of working. |
| Contract distributed across front door and API docs | [`ph-curves`](https://github.com/photon-circus/ph-curves/blob/main/README.md#guarantees-and-limits) | A repository can keep guarantees and caller-owned policy in the README without adding `CONTRACT.md`. |
| Consequential component contracts plus evidence records | [`ph-eventing`](https://github.com/photon-circus/ph-eventing/blob/master/docs/README.md) | Stable clauses and claim-to-evidence records can help when several components need to cite precise semantics. |
| Status-first Experimental contract | [`ph-agent-toolkit`](https://github.com/photon-circus/ph-agent-toolkit/blob/main/STATUS.md) | Trust limits, inappropriate use, allowed effects, and extraction or retirement conditions can matter more than API stability. |
| Specialized driver, model, and conformance authorities | [`ph-sht4x-hts`](https://github.com/photon-circus/ph-sht4x-hts/blob/main/README.md#documentation) | Evidence-sensitive work can split documents by authority and audience without making that structure universal. |
