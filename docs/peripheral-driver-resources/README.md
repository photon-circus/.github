# Peripheral-driver evidence resources

Status: **Non-normative implementation and remediation guidance**

These resources help repositories apply the normative
[stable-device-proposition rule](../../REPOSITORY_STANDARDS.md#102-stable-device-propositions)
without prescribing a file name, identifier spelling, schema, workflow, or CI
implementation. Every recommendation and template in this directory is
advisory.

The user-facing result is a driver whose behavior can be trusted. The evidence
record, driver, model, conformance suite, and physical observations are distinct
projections of that claim. Shared proposition identity gives those projections a
common referent while preserving independent interpretation; a model that fills
an evidence gap with plausible behavior does not add trustworthy coverage.

The stable identity belongs to the proposition, not to this representation. A
small repository may use a Markdown section; another may have a machine-readable
consumer that justifies a structured registry. Do not adopt a format merely
because another driver uses it.

## Start with demand, not an evidence inventory

The non-normative
[bootstrap intent](../PERIPHERAL_DRIVER_BOOTSTRAP_INTENT.md#feature-survey-then-consumer-demand)
owns the recommended disposable feature survey and product-scope selection.
Once a current consumer is selected:

1. Add the smallest truth-apt proposition only when current driver behavior,
   model behavior, conformance, scoped physical work, or a reported bug needs
   the shared referent.
2. Let driver and model derive their own consequences while citing the same
   proposition identifier.
3. Test only the honestly supported intersection. Unsupported or incomplete
   coverage is a valid result.
4. Add physical work only for a named proposition with a current consumer and a
   feasible discriminating observation.
5. When evidence changes, update the evidence record, inspect direct citations,
   and edit only local consequences that became stale. Keep that propagation in
   one bounded transaction, then stop.

A source section with no current consumer does not create a maintained fact,
feature, test, issue, decision record, hardware task, or CI rule. Electrical or
board-integration data is not automatically a driver or model proposition merely
because a source lists it; capture it only when a current component claim or
scoped physical activity consumes it. A retained legacy proposition may be
marked not currently relevant; that is metadata, not a backlog.

## Keep source identity and proposition identity separate

A **source record** identifies exact input bytes: publisher, title, document,
revision, retrieval, digest, and rights posture. A **proposition record** says
what one documentary or device proposition is and what evidence addresses it.

Use [the optional source example](SOURCES.toml.example) when multiple or mutable
documents, source conflicts, exact-byte integrity, or redistribution constraints
make a separate registry valuable. Add a source only when a current proposition
cites it or another actual integrity or rights consumer needs it. A digest
identifies bytes; it does not verify an interpretation or establish silicon
behavior.

Source IDs and proposition IDs are different namespaces. A global source
ranking must not silently decide a proposition when sources conflict. Record
each relevant source as evidence on that proposition and preserve the conflict.

## Evidence-registry semantics

The [Markdown example](EVIDENCE_REGISTRY.example.md) demonstrates one small
representation. Its field names and `S-nn` spelling are not organization
requirements.

Useful distinctions are:

- **Documentary proposition:** what a pinned source states, omits within a named
  search scope, or contradicts.
- **Device proposition:** behavior attributed to scoped silicon.
- **Evidence relation:** an item supports, refutes, or does not resolve the
  proposition.
- **Knowledge state:** a concise summary may say supported, refuted, or
  undefined. When retained same-scope evidence conflicts, preserve every item;
  a three-state representation remains undefined until the proposition is
  narrowed or the conflict is resolved.
- **Relevance:** optional mutable metadata saying whether a current driver,
  model, conformance, physical, or reported-bug consumer exists.

Keep observation type separate from its relation to the proposition. An
affirmative observation or a negative result may support or refute a proposition
depending on what that proposition says. A located-negative review supports the
documentary proposition that a bounded search found no statement; it does not
resolve the corresponding device behavior. Mere absence of evidence leaves the
proposition undefined. Undefined is a knowledge state, not evidence polarity and
not the opposite behavior.

Hardware cannot refute that a document contains particular wording. When
silicon appears to contradict vendor guidance, preserve the documentary
proposition and record a separate device proposition linked to it. Likewise, a
located negative establishes source silence only within its search scope; it
does not establish the inverse silicon behavior.

Keep one identifier attached to one atomic proposition. If a proposition changes
meaning or splits, retain the old identifier as a tombstone and allocate new
identifiers. Never reuse an identifier. Conflicting evidence remains visible;
do not overwrite an earlier observation merely because a later one differs.

## Downstream projections

The evidence registry records no driver policy, model policy, test expectation,
or judgment that evidence is sufficient for a downstream guarantee. Downstream
code and documentation cite the proposition identifier and state only their
local consequence, for example:

- the driver promises, rejects, masks, waits, or exposes uncertainty;
- the model implements, abstracts, injects, excludes, or reports unsupported;
- conformance covers only the overlap between those declared boundaries; and
- physical work records a scoped observation without deciding which component
  must change.

Do not copy the proposition, vendor passage, source coordinates, or physical
observation into those downstream surfaces. A citation shares evidence identity,
not interpretation or implementation logic.

## Admit physical work narrowly

A useful physical-observation request names:

- one stable device proposition;
- the current driver, model, conformance, qualification claim, or bug disposition
  that will consume the result, or one explicitly selected bounded confirmation
  question;
- an observation that could discriminate support from refutation;
- device and silicon identity, reset history, voltage, temperature, fixture,
  tools, and software revision as applicable; and
- the durable raw artifact or digest that will receive the result.

If those fields cannot be stated from the current information, do not create the
physical request or claim confirmation. Preserve the existing evidence record;
an already-undefined proposition remains undefined. Do not write `owner will
validate`, `maintainer blocked`, `hardware validation required`, an unchecked
box, or a due date as a substitute for evidence. Confirmation of one selected
proposition is different from broad validation of a document or repository.

## Remediate an existing hardware contract

Existing hardware-contract files, including `HARDWARE_CONTRACT.md` and
`HARDWARE_CONTRACT.toml`, may be repaired in place so links and history remain
useful. No rename or schema migration is required, regardless of the existing
filename or representation.

1. Stop new issue, decision, HIL, and CI fan-out while the contract is being
   classified.
2. Preserve every existing stable identifier. If rows lack identifiers, assign
   them only to propositions with a current consumer or a retained external
   reference.
3. Classify each row as a documentary proposition, device proposition,
   component policy, task, duplicate, or non-truth-apt note.
4. Keep atomic propositions. Tombstone and replace compound or changed meanings;
   never silently redefine an identifier.
5. Replace checkbox, `provisional`, owner-review, and future-validation states
   with the evidence actually present. Often the honest state is undefined.
6. Move driver and model reactions into their owning component documentation and
   cite the proposition identifier from each.
7. Mark retained propositions with no current consumer as not currently
   relevant. This creates no coverage gap, issue, hardware task, or release
   blocker.
8. Replace duplicated proposition and provenance prose elsewhere with the local
   consequence plus the stable citation.
9. Remove validators, checklists, and work items that exist only to protect or
   complete speculative records.
10. Re-run existing technical tests and disclose unsupported coverage honestly.

Move a current component policy to its owning component. Remove obsolete tasks,
duplicate prose, and non-truth-apt scaffolding; retain a tombstone only when an
existing identifier or external reference must continue to resolve.

One evidence correction remains one bounded change even when it requires a
registry update and local consequence changes in the driver, model, or
conformance. Do not edit an unaffected layer or split the propagation into an
issue graph merely because several layers cite the proposition.

Remediation is complete when retained identifiers resolve, evidence is honestly
represented, current citations have been inspected, stale duplicate authorities
are gone, existing technical checks pass, and no unrelated source section has
been promoted into new work.

## Proportionate automation

Automation is useful for closed structural invariants such as:

- proposition identifiers are unique;
- retired identifiers still resolve;
- downstream citations resolve; and
- tracked or packaged vendor artifacts follow the recorded rights posture.

Avoid using CI to classify prose, decide whether a statement needs a
proposition, judge evidence sufficiency, infer source meaning, demand a hardware
run, or generate issues and follow-ups. Keep semantic review bounded to the
current change and its consumers.

## Source revisions and local artifacts

Do not silently replace the revision, byte count, or digest of a source record.
Add a new source identity for changed bytes and retain an older identity while a
proposition still cites it. Conflicting revisions become proposition-scoped
evidence rather than a global winner chosen in advance.

Use `not-established`, `permitted`, or `prohibited` for redistribution posture
when that distinction is useful. A public URL is not permission to redistribute.
Keep unlicensed local vendor files untracked and outside published packages. A
`docs/vendor/README.md`, when needed, contains only retrieval, local storage,
hashing, ignore, and packaging instructions; it links to the source record
instead of becoming a second metadata catalog.
