# Peripheral-driver source-registry resources

Status: **Non-normative implementation aids**

These resources offer an optional, machine-readable way to record the exact
source material used to derive a peripheral driver. They help apply the source
and evidence expectations in the
[Peripheral Driver Release and Evidence Profile](../PERIPHERAL_DRIVER_PROFILE.md)
and preserve the source-first intake described by the
[Peripheral Driver Bootstrap Intent](../PERIPHERAL_DRIVER_BOOTSTRAP_INTENT.md).

This pack adds no requirement, defines no organization-wide schema, and does
not make a source registry part of every driver repository. It also does not
replace reviewed interpretation, establish redistribution permission, or make
a model or hardware-qualification claim. Every recommendation, imperative, and
lower-case modal term in this pack is advisory; the linked normative documents
remain the source of obligations.

## Use only when it reduces a real risk

A registry is useful when a driver depends on multiple or mutable documents,
exact source bytes matter to an independently derived model, sources conflict,
or redistribution constraints need an explicit record. A small driver may keep
a concise source table in its hardware contract or another maintained document
when that is sufficient.

Do not add an empty registry merely to resemble another repository. Once a
registry is useful, copy [the example](SOURCES.toml.example), replace its sample
records, and maintain it at exactly `docs/SOURCES.toml`. The uppercase
`SOURCES` spelling matters on case-sensitive systems and in packaged links.

The example evolves an earlier driver source-registry pattern and uses synthetic
source records so it does not disclose or accidentally canonize a current
driver's provenance. It is a starting point, not a requirement to migrate an
adequate local registry or retain fields that have no current consumer.

## What the registry owns

| Concern | Registry record | What the record establishes |
| --- | --- | --- |
| Identity | Publisher, title, document number, revision, publication date, applicability, and URLs | Which named source was reviewed |
| Integrity | Retrieval date, media type, exact byte count, and SHA-256 digest | Which exact artifact bytes the record describes |
| Authority | Stable ID, role, kind, status, and explicit precedence | Which source is primary when claims overlap or conflict |
| Rights posture | Per-source tri-state value and repository redistribution policy | What has been established about copying the artifact and what the repository chooses to track |

A digest identifies bytes. It does not prove that the artifact is authoritative,
that a claim was interpreted correctly, that redistribution is permitted, or
that physical silicon behaves as described. Likewise, a precedence number
orders overlapping sources; it does not turn a supplemental source into a
universal device claim.

Keep interpreted register, protocol, timing, state, and error claims out of
free-form registry notes. Those claims need source locations, review context,
and explicit nonclaims in a maintained hardware contract or equivalent.

## Ownership chain

```text
vendor artifact
  -> docs/SOURCES.toml
       identity, exact bytes, authority, retrieval, and rights posture
  -> hardware contract or equivalent maintained contract
       interpreted claim, source ID, page or section, assumption, and nonclaim
  -> decisions
       ambiguity, conflict, inference, deviation, and supersession rationale
  -> driver, independent model, and tests
       executable behavior and claim-scoped evidence
```

Use the stable registry ID when another document cites a source. The hardware
contract owns what the source means for supported behavior. A decision record
owns durable reasoning where the sources are ambiguous, conflict, or leave a
gap needing an explicit boundary. Prefer deriving driver and model
implementations from the accepted sources and decisions rather than from one
another; their tests establish only the named software or conformance claims.
Physical evidence remains separate.

Not every repository needs a document named `HARDWARE_CONTRACT.md`, a decision
log, or an independent model. The ownership boundaries still apply when those
concerns are combined into fewer maintained artifacts.

## Revisions and supersession

Treat one entry as the identity of one exact document revision and artifact.
Do not silently replace its revision, byte count, or digest when a vendor
publishes new bytes.

- Add a new entry with a new stable ID for a later revision.
- Use `supersedes` on the new entry and, when useful, `superseded_by` plus a
  `superseded` status on the retained old entry.
- Retain an older entry while a maintained claim still depends on it. A newer
  source does not retroactively change that claim.
- If bytes change without a visible revision change, preserve both identities,
  distinguish the replacement in the IDs, and record the reconciliation in the
  decision owner.
- Update `reviewed_utc` when the registry as a whole is reviewed. It is not the
  source publication date, artifact retrieval date, or hardware-test date.

Supersession describes the document relationship. Conflict precedence remains
explicit: in the example, the lower positive `authority` number wins for an
overlapping claim unless a reviewed decision records a narrower exception.

The example uses a small, local `status` vocabulary: `active` means the entry is
current for claim review, while `superseded` means it is retained for history or
for claims that still depend on it but a newer entry is preferred. A repository
that does not need that distinction may omit `status`; a repository that adds
values documents their meanings locally in this recommended pattern.

## Redistribution and local source copies

Use a string rather than a Boolean for each source's redistribution posture:

- `not-established`: no applicable redistribution grant has been confirmed;
- `permitted`: an applicable grant or license has been reviewed and recorded;
- `prohibited`: reviewed terms prohibit redistribution.

Unknown is not the same as prohibited, and a public download URL is not a grant
to redistribute. The example sets `redistribution_policy = "metadata-only"`:
the repository records metadata and does not redistribute vendor PDFs. Keep
local review copies untracked and outside published packages. Even a
`permitted` entry does not override that repository policy; changing it would
require a separate, explicit review for the exact artifact and terms.
For `permitted` or `prohibited`, identify the reviewed grant, license, or terms
in the entry notes or a referenced decision rather than recording a bare
conclusion.

When a repository has `docs/vendor/README.md`, use it only for local retrieval,
storage, hashing, ignore, and packaging instructions. Link back to
`docs/SOURCES.toml` instead of copying URLs, revisions, sizes, and digests into a
second catalog.

## Proportionate validation

At minimum, parse the registry as TOML during review. Add small automated checks
when the number of sources, references, or releases makes drift plausible:

- source IDs are unique and downstream source IDs resolve;
- byte counts are positive and SHA-256 values contain 64 hexadecimal digits;
- redistribution values use the three states defined here, and any local
  `status` vocabulary is documented and applied consistently;
- authority precedence is unambiguous where sources overlap;
- optional supersession links resolve and do not form cycles; and
- vendor artifacts are excluded from tracking and packaging unless both the
  reviewed rights posture and repository policy explicitly permit them.

An authorized maintainer may separately compare a local artifact's byte count
and digest with the registry. A clean CI path need not download or possess a
vendor document that the repository does not redistribute. A single-source
repository does not need a custom schema validator or source-management
framework merely because it adopted this example.
