# Rust Peripheral-Driver Documentation Guide

Status: **Non-normative implementation guidance**

Scope: Rust peripheral-driver repositories, including workspaces that contain a
primary driver and an optional independent behavioral-model crate.

This guide adds no requirements. The adopted
[Repository Standards](../REPOSITORY_STANDARDS.md),
[Peripheral Driver Release and Evidence Profile](PERIPHERAL_DRIVER_PROFILE.md),
and, when applicable, the
[Device Behavioral Model Standard](DEVICE_BEHAVIORAL_MODEL_STANDARD.md) control
if this guide conflicts with them. Every recommendation, imperative, use of
"should," and template sentence in this guide is advisory. "Must" and
"required" appear only when this guide summarizes an existing linked
requirement; consult the normative source for the exact obligation.

## 1. Recommended organizing rule

Give each maintained fact one canonical owner. A documentary or device
proposition belongs in one evidence record. Downstream surfaces cite its stable
identifier and state only their local consequence; they do not copy the
proposition, vendor wording, source coordinates, or physical observation.
Repeat audience-specific status or API guidance only when necessary, and prefer
a link or generated projection over another maintained prose copy.

| Audience | Primary surface | It answers |
| --- | --- | --- |
| Repository visitor or contributor | Root `README.md` | What this repository owns, its state, packages, evidence, limits, and how to work on it |
| Crate evaluator or crates.io visitor | `crates/<driver>/README.md` | Whether this exact package fits their application and how to start using it |
| Rust API user | Crate-level rustdoc and item docs | How to use the API correctly, including errors, invariants, features, and examples |
| Human contributor | `CONTRIBUTING.md` | How to propose, implement, verify, and submit a change |
| Coding agent | `AGENTS.md` | What is expensive to infer, easy to get subtly wrong, or operationally protected |
| Maintainer reviewing device claims | Source catalog and stable-proposition evidence registry | Which source bytes or observations bear on each proposition and whether they support, refute, or leave it undefined |

The package boundary matters. When a package is published, Cargo uploads its
package README and crates.io renders it; repository-root contracts are not
automatically bundled with a nested crate. Consumer-critical caveats therefore
belong in the crate README or rustdoc, not only behind a repository link.

## 2. Recommended repository shapes

### 2.1 Small driver

```text
/
|-- README.md
|-- LICENSE
|-- CHANGELOG.md                 # when the lifecycle/publication rule applies
|-- CONTRIBUTING.md              # when the visibility/lifecycle rule applies
|-- SECURITY.md                  # when the visibility/lifecycle rule applies
|-- RELEASING.md                 # for a published/versioned deliverable
|-- AGENTS.md                    # when agent/non-obvious-invariant guidance adds value
|-- Cargo.toml
|-- crates/
|   `-- <part>/
|       |-- Cargo.toml
|       |-- README.md            # explicit package README
|       `-- src/lib.rs           # crate front page plus public item docs
|-- docs/
|   |-- SOURCES.toml             # when structured provenance adds value
|   |-- DEVICE_EVIDENCE.md       # only propositions consumed by current work
|   `-- DECISIONS.md             # only durable, non-obvious rationale
`-- <canonical verification>     # one documented local entry point
```

For a very small driver, source identity, device evidence, software invariants,
and durable decisions can be clearly separated sections of one
`docs/CONTRACT.md`. The evidence section remains the sole authority for each
stable proposition; the other sections cite it and own only their local
consequences. Creating a file per concern is not a quality signal.

### 2.2 Expanded driver with an independent model

```text
/
|-- README.md
|-- LICENSE
|-- CHANGELOG.md                 # when the lifecycle/publication rule applies
|-- CONTRIBUTING.md              # when the visibility/lifecycle rule applies
|-- SECURITY.md                  # when the visibility/lifecycle rule applies
|-- RELEASING.md                 # for a published/versioned deliverable
|-- AGENTS.md                    # when agent/non-obvious-invariant guidance adds value
|-- Cargo.toml
|-- crates/
|   |-- <part>/
|   |   |-- Cargo.toml
|   |   |-- README.md
|   |   `-- src/lib.rs
|   `-- <part>-model/
|       |-- Cargo.toml
|       |-- README.md            # one maintained model/fidelity declaration
|       `-- src/lib.rs
|-- docs/
|   |-- SOURCES.toml
|   |-- DEVICE_EVIDENCE.md       # stable propositions used by current consumers
|   |-- ARCHITECTURE.md          # when boundaries/dependency direction are non-obvious
|   |-- INVARIANTS.md            # when review-blocking truths need stable IDs
|   |-- TEST_PLAN.md             # when evidence layers are genuinely distinct
|   |-- DECISIONS.md
|   `-- vendor/README.md         # only for local, untracked vendor-file handling
`-- <canonical verification>
```

A `<canonical verification>` label represents one documented command, not a
literal filename. A Rust repository might expose `cargo xtask ci`; another
repository might keep `scripts/ci.sh`. Do not infer a second implementation
from these examples. The explicitly non-normative
[Rust xtask field guide](PERIPHERAL_DRIVER_XTASK_GUIDE.md) records observed
tradeoffs without making either form required.

A separate model crate, `docs/README.md`, API inventory, architecture file,
invariant file, test-plan file, and local documentation-style file are all
conditional. Start combined and split only when a document has a distinct
audience, authority, change cadence, or review purpose.

## 3. Existing required-file floor

This table is a convenience summary of the adopted organization standard. The
[documentation requirements](../REPOSITORY_STANDARDS.md#7-documentation-requirements)
remain authoritative.

| Artifact | Existing organization requirement |
| --- | --- |
| Root `README.md` | Every repository |
| Root `LICENSE` | Every repository |
| `CHANGELOG.md` | Every non-Experimental repository and every repository with a published package or versioned deliverable |
| `CONTRIBUTING.md` | Public Incubating, Active, and Maintenance repositories |
| `SECURITY.md` | Public Active and Maintenance repositories |
| `RELEASING.md` | Every repository with a published package or versioned deliverable |
| `AGENTS.md` | Active technical repositories using coding agents or carrying non-obvious invariants |
| `CODEOWNERS` | Multiple maintainers or sensitive ownership boundaries |
| `CODE_OF_CONDUCT.md` | Public repositories accepting community contributions |

Driver-specific content obligations are broader than this filename list. A
driver records exact provenance and stable identities for the device
propositions its behavior or public claims consume. The driver separately owns
its interpretations, assumptions, supported targets, tests, and limitations.
The standards do not require each concern to have a separate file.

Published Experimental work is the important override: publication still
triggers the repository's changelog and release-guidance requirements. Neither
root document has to be included in the distributed archive unless a
repository-specific release contract separately requires it. A private
Incubating repository does not acquire a `CONTRIBUTING.md` or `SECURITY.md`
requirement merely because a public repository would, though either file may
still be useful.

GitHub may display default community-health files from the public organization
`.github` repository when a repository has no local version. Those defaults are
fallback user-interface content: they are not cloned, packaged, or downloaded,
and they cannot carry repository-specific device, evidence, version, or
security guidance.

## 4. Conditional file-role guide

| Artifact | Recommended role | Create or retain when | Avoid |
| --- | --- | --- | --- |
| Root `README.md` | Repository/workspace front door | Always | Long API inventory, full installation tutorial, or duplicated contract text |
| Driver crate `README.md` | Standalone package evaluation and quick start | Any user-facing or potentially publishable nested crate | Repository layout, maintainer release mechanics, or dependence on private/unpackaged links for essential limits |
| Crate-level rustdoc | Compiled API front page | Every Rust library | A third, unchecked copy of the whole repository README |
| `docs/SOURCES.toml` | Exact source identity, integrity, applicability, and rights posture | Multiple or mutable specifications, behavioral models, source conflicts, or redistribution constraints | Acting as a global authority ranking or owning device propositions and their evidence state |
| Evidence registry, including a remediated hardware contract | Atomic documentary or device propositions with permanent identifiers, scoped evidence state, and exact provenance | A proposition is consumed by driver behavior, model behavior, conformance, physical evidence, or a bug disposition | Implementation policy, copied downstream prose, review owners, checkboxes, future-validation promises, or an exhaustive inventory of unconsumed source facts |
| Architecture/design | Ownership and dependency direction | Multiple crates/layers, non-obvious state authority, or important integration boundary | Restating directory names or code that is self-explanatory |
| API contract | Semantic compatibility contract or pre-implementation design | Contract-first incubation or unusually consequential semantic choices | Hand-maintained signatures already canonical in Rust code/rustdoc, or a second authority for device propositions |
| Invariants | Stable software truths and coupled tests | Stateful, timing-sensitive, recovery-sensitive, unsafe, concurrent, or evidence-sensitive work | General style advice, a second architecture summary, or copied device evidence |
| Test plan | Mapping from claims/failure modes to evidence | Distinct pure, transport, model, target, HIL, or qualification layers | A generic list of `cargo` commands already owned by CI |
| Decisions/ADRs | Why a non-obvious choice was made, its consequences, and supersession | The rationale would otherwise be rediscovered or relitigated | Describing current code without a decision or copying issue discussion verbatim |
| Documentation standards | Repository-specific claims and terminology delta | Device terminology is unusually easy to misstate | Generic prose style; prefer an organization guide or fold a short delta into invariants/CONTRIBUTING |
| Model README/declaration | One maintained fidelity, source, purpose, boundary, and nonclaim declaration | A behavioral model exists | Mirroring the declaration across model README, architecture, test plan, and policy files |
| `docs/vendor/README.md` | Local retrieval/storage instructions and redistribution guardrails | Maintainers keep untracked local vendor artifacts | A second source catalog with copied hashes and revisions |
| `docs/README.md` | Navigation only | The root documentation map is no longer usable | A second index that repeats scope or status claims |
| Tool shims such as `CLAUDE.md` | One-line redirect to `AGENTS.md` | A tool discovers only its own conventional filename | Duplicated agent instructions |

## 5. Root README structure

The root README is about the repository and its engineering claim, not just its
primary crate.

Recommended order:

1. Repository name and one factual sentence answering what it is and what it is
   for.
2. Small badge row, if every badge is currently truthful.
3. Four-field lifecycle, distribution, model, and physical-evidence disclosure.
4. `Packages in this workspace` table when more than one package exists.
5. Responsibility and explicit non-goals.
6. Quick-start link or very small example; avoid duplicating the full package
   tutorial.
7. Supported toolchain, targets, transport traits, and feature scope.
8. Evidence summary, limitations, and what passing CI does not prove.
9. Repository/document map.
10. Canonical local verification and the relationship of hosted CI to the full
    gate.
11. Contributing, security, changelog, and releasing links.
12. License.

Suggested skeleton:

````markdown
# ph-<part>-<class>

<One precise sentence: async/sync, no_std/allocation, device, and purpose.>

<badges, when applicable>

<status disclosure>

## Packages in this workspace

| Package | Role | Distribution |
| --- | --- | --- |
| `ph-<part>-<class>` | Primary driver | <exact state> |
| `ph-<part>-<class>-model` | <exact model role and audience> | <exact state> |

## Responsibility and boundaries

<What the repository owns, who it serves, and explicit non-goals.>

## Quick start

See the [driver package README](crates/<part>/README.md).

## Supported scope

<MSRV/toolchain, targets, traits, features, known incompatibilities.>

## Evidence and limitations

<Implementation/model/physical evidence, each scoped precisely.>

## Documentation

<Direct links with a one-clause role for each maintained document.>

## Verification

`<the repository's canonical command, such as cargo xtask ci or ./scripts/ci.sh>`

<Explain any bounded hosted subset.>

## Contributing and releases

<Links to CONTRIBUTING, SECURITY, CHANGELOG, RELEASING as applicable.>

## License
````

When repository and package names happen to match, their README roles still do
not. A root README can mention all workspace crates and maintainer workflow; a
package README needs enough packaged context to stand alone after Cargo packages
the nested crate.

## 6. Driver crate README structure

Recommended order:

1. Exact package name and a consumer-facing sentence.
2. Package badge row, once its targets exist.
3. The four-field disclosure required by the peripheral-driver profile. The
   fields report three independent dimensions, with evidence split into model
   and physical fields.
4. Availability/install instructions. For a prerelease, show the exact version;
   for an unpublished crate, say that it is not available from crates.io.
5. Minimal compiled example.
6. Important semantics and nonclaims that affect correct use.
7. Features and default-feature behavior.
8. `no_std`, allocation, unsafe-code, MSRV, and supported-target scope.
9. API documentation, source repository, issue/security route, and
   version-pinned contract links where those links are material to a released
   claim.
10. License.

Suggested skeleton:

````markdown
# ph-<part>-<class>

<One precise package sentence.>

<package badges, when applicable>

<status disclosure>

## Availability

<Unpublished statement or exact Cargo dependency.>

## Usage

```rust,no_run
// Small compile-checked happy path.
```

## Semantics and limitations

<Freshness, state, timing, error/recovery, units/calibration, and other
consumer-relevant distinctions.>

## Features

| Feature | Default | Effect |
| --- | --- | --- |

## Platform support

<MSRV, no_std/allocation claim, abstract HAL traits, tested target families.>

## Documentation and support

<docs.rs, repository, issues/security, and version-specific contracts.>

## License
````

Set `readme = "README.md"` explicitly in each publishable member's
`Cargo.toml`. Before release, inspect `cargo package --list` and the extracted
package to confirm that its README and license are present and that essential
links work without the repository checkout.

For crate README versus rustdoc synchronization, choose one of two patterns:

- Include the crate README as crate documentation with
  `#![doc = include_str!("../README.md")]` when it renders well in both places.
- Keep a curated rustdoc front page, but mark and check the shared status block
  and example so drift fails CI. The compiled rustdoc example is the better
  canonical owner because a doctest can verify it.

Do not maintain three unchecked copies of a usage example or status claim.

Rustdoc and the package README state the API or product consequence a user
needs. When that consequence depends on a device proposition, cite its stable
identifier and link to the canonical evidence record. Do not paste vendor
tables, source coordinates, or registry prose into user documentation merely to
show that research occurred.

### 6.1 Model crate README

When an independent behavioral-model crate exists, keep one maintained model
declaration in its README or crate front page. A useful order is:

1. Purpose, intended consumers, and whether the crate is a user dependency.
2. Source basis, stable proposition identifiers, and independence from the
   driver implementation. State model consequences without copying the
   proposition or its provenance.
3. Fidelity classification for relevant behavior as modeled, abstracted,
   injected, excluded, or unsupported, including the applied-stimulus boundary,
   assumptions, ambiguities, limitations, and explicit nonclaims.
4. Inputs, time/state semantics, validation behavior, and deterministic outputs.
5. Relationship to conformance tests and the exact claims those tests establish.
6. Distribution state, package metadata, documentation, and license.

The non-normative
[model declaration template](device-model-resources/MODEL_DECLARATION_TEMPLATE.md)
offers a starting set of prompts. Neither it nor the abbreviated order above is
a complete rendering of, or substitute for, the linked normative model
standard. The maintained declaration must satisfy every applicable requirement,
including recording assumptions, ambiguities, explicit nonclaims, deliberately
excluded behavior, and any corrections to the datasheet baseline or
evidence-backed silicon variants with their distinct provenance and supported
identities. Avoid copying the declaration across the model README, architecture,
test plan, and policy documents; choose one owner and link to it.

## 7. Badge policy

Badges are optional navigation and current-state indicators. They are never the
canonical lifecycle, compatibility, model-conformance, or hardware-evidence
record.

Recommended maximum sets:

| Surface/state | Badge row |
| --- | --- |
| Private or unpublished crate | Lifecycle, MSRV, license at most; no fake registry/docs badge |
| Public repository before publication | Lifecycle, representative hosted CI, MSRV, license |
| Published crate README | Lifecycle, crates.io version, docs.rs, MSRV, license |
| Root README after publication | Lifecycle, hosted CI, primary crate version/docs, license |

Use CI only after the public default-branch workflow has run successfully and
the badge describes that workflow. A private workflow badge is not externally
available. Avoid labeling a dispatch-only or deliberately partial workflow as
the release gate.

Use crates.io and docs.rs badges only after those destinations exist. Use the
manifest `rust-version` as the canonical MSRV; a badge is a checked projection.

Illustrative Markdown template for either surface (replace every placeholder and
verify every destination from that README's rendered and packaged context):

```markdown
[![Lifecycle: <lifecycle>](https://img.shields.io/badge/lifecycle-<lifecycle>-<color>.svg)](<lifecycle-definition-URL>)
[![CI](<workflow-badge-URL>)](<workflow-URL>)
[![crates.io](https://img.shields.io/crates/v/<crate>.svg)](https://crates.io/crates/<crate>)
[![docs.rs](https://img.shields.io/docsrs/<crate>)](https://docs.rs/<crate>)
[![MSRV](https://img.shields.io/badge/MSRV-<version>-blue.svg)](<manifest-URL>)
[![License: <SPDX>](<license-badge-URL>)](<license-URL>)
```

A README rendered only in the repository may use repository-relative links. For
any README published with a crate, treat archive membership and web resolution
as separate checks: `cargo package --list` only confirms that a file is in the
`.crate`. crates.io renders the packaged README but, for supported repository
hosts, rewrites ordinary relative links to the manifest `repository` URL under
`blob/HEAD` (`raw/HEAD` for media). Ordinary relative links in the docs.rs
README view, or in README text included in rustdoc, are browser-relative to
those generated pages, not to the packaged file tree. Use absolute URLs pinned
to the release tag or commit for release-critical documents, and validate every
destination in each rendered surface. Construct the license badge URL with the
badge provider's required escaping rather than placing a raw compound SPDX
expression in a URL path.

Recommended lifecycle colors, if lifecycle badges are adopted consistently:
Experimental red, Incubating orange, Active bright green, Maintenance yellow,
and Archived light grey. Always retain text in the alt label.

Avoid downloads, stars, generic "production ready," code coverage, "hardware
tested," or model-conformance badges. Implementation coverage is not physical
evidence, and operation-scoped model or silicon claims do not fit safely in a
badge.

Cargo's legacy manifest `[badges]` table is not the place for these; keep visual
badges in Markdown.

## 8. Status disclosure template

Distribution, lifecycle, model conformance, and physical evidence are
independent. Do not infer one from another. The four lines below present the
three dimensions defined by the profile while separating its two most commonly
confused evidence classes.

Base block for a README:

```markdown
> [!WARNING]
> **Lifecycle:** <current lifecycle and its practical consequence>.
> **Distribution:** <unpublished, exact crates.io prerelease, or exact ordinary release>.
> **Model conformance:** <none, or exact public driver operations that passed
> against an independent model, plus all uncovered operations or a packaged coverage link>.
> **Physical evidence:** <none, exact observed scope, or exact `ph-hil`-qualified
> operations or claims, silicon scope, and evidence contract>.
> Evidence and limitations apply only to the named operations; publication does
> not imply hardware qualification.
```

Use an ordinary `# Status` section with the same four facts in rustdoc if GitHub
admonition syntax does not render suitably.

### 8.1 Lifecycle sentence library

- **Experimental:** `Experimental - the supported contract is not yet
  established. Compatibility for any published artifact follows its documented
  version and release policy; evaluate the declared scope before use.`
- **Incubating:** `Incubating - the responsibility is bounded and intended to
  become supported. Compatibility follows the documented version and release
  policy, not lifecycle alone.`
- **Active:** `Active - usable, documented, verified, and actively developed
  within the declared scope; compatibility follows the documented release
  policy.`
- **Maintenance:** `Maintenance - supported within the documented release
  series for fixes and upkeep; major feature development is not expected.`
- **Archived:** `Archived - retained for historical or reference use; no further
  support is promised. <Replacement or "No replacement is designated.">`

Lifecycle never says whether a crate is published or hardware-qualified.

### 8.2 Distribution sentence library

- **Unpublished:** `Unpublished; the candidate version is <VERSION>.
  <For a crate not intended for registry distribution: The manifest sets
  publish = false. / For an intended future registry crate: No registry artifact
  exists yet.>`
- **Crates.io prerelease:** `Published to crates.io as prerelease <VERSION>;
  consumers need to name a prerelease requirement explicitly. Use an
  exact-version requirement only when deliberate pinning is intended.`
- **Ordinary crates.io release:** `Published to crates.io as ordinary release
  <VERSION>.`

Use the exact version. Major version zero by itself does not mean Experimental,
and an unpublished state does not by itself imply `publish = false`.

### 8.3 Model-conformance sentence library

- **None:** `None. No public driver operation is claimed as model-conformant.
  <NAME THE SOFTWARE-TEST LAYERS ACTUALLY PRESENT AND THEIR SCOPE>.`
- **Partial:** `The public driver operations <COVERED OPERATIONS> have passed
  against the independent <MODEL>, whose accepted domain covers those claims.
  <NAME EVERY UNCOVERED PUBLIC OPERATION, OR LINK TO A PACKAGED COVERAGE OR
  LIMITATIONS SECTION THAT NAMES THE COVERED AND UNCOVERED OPERATIONS>.`
- **Declared supported public surface:** `Every operation in the declared
  supported public surface identified in <PACKAGED COVERAGE LINK> has passed
  against the independent <MODEL>, whose accepted domain covers each claim.
  Exclusions and limitations remain <LIMITATIONS>.`

Use **None** only to report that no model-conformance claim is made. Any
model-conformance claim must state a passing driver-versus-model result through
the public driver surface; model implementation or model-test coverage alone is
insufficient. For partial coverage, name every covered and uncovered public
operation or link a packaged coverage or limitations section that does so. An
unpackaged issue or private record is insufficient.

### 8.4 Physical-evidence sentence library

- **None:** `None. No reviewed physical-device evidence supports a physically
  observed or ph-hil-qualified claim.`
- **Observed:** `Physically observed for <OPERATIONS> using driver revision
  <REVISION> on <DEVICE AND SILICON IDENTITY> with
  <FIXTURE, TOOLS, CONDITIONS, AND OBSERVATION SCOPE>, as recorded in
  <LINKED REVIEWED EVIDENCE RECORD>; this is not a qualification or calibration
  claim.`
- **`ph-hil`-qualified:** `ph-hil-qualified only for <OPERATIONS OR CLAIMS>
  using driver revision <REVISION> on <DEVICE AND SILICON IDENTITY> with
  <FIXTURE, TOOLS, CONDITIONS, AND OBSERVATION SCOPE>, under
  <LINKED REVIEWED PH-HIL EVIDENCE> satisfying
  <LINKED ADOPTED PH-HIL CONTRACT>. No broader device, board, condition, or
  calibration claim is made.`

A physically observed claim requires reviewed evidence identifying the exact
driver revision, device, conditions, fixture, tools, and observation scope. A
`ph-hil`-qualified claim additionally requires reviewed `ph-hil` evidence
satisfying the adopted contract. Both claims remain limited to their recorded
operation or claim, silicon identity, conditions, and observation capability.

The same factual block normally appears in the root README, packaged driver
README, and crate front-page docs. Either single-source it or compare the
copies in CI. Avoid repeating the exact candidate version in AGENTS, generic
issue placeholders, API inventories, and other mutable prose.

## 9. CONTRIBUTING versus AGENTS

They are different layers, not competing contribution guides.

Use an ownership map, not a blanket precedence order:

- Adopted organization standards and applicable profiles own organization
  obligations.
- Repository public contracts and recorded decisions own product semantics and
  durable repository decisions.
- `CONTRIBUTING.md` owns the shared human/agent contribution workflow.
- `AGENTS.md` adds agent-specific routing, execution constraints, and traps, and
  points to the canonical owners above.

A more specific file does not silently override the owner of another subject.
Resolve inconsistent instructions with a maintainer before changing the
affected behavior.

Recommended human path: `README.md` -> `CONTRIBUTING.md` -> the contract relevant
to the change.

Recommended agent path: `AGENTS.md` as a concise route map ->
`CONTRIBUTING.md` -> the linked contract and decision sources. The agent file
ideally tells an agent what else to read; the contribution guide need not make
every human read agent instructions.

### 9.1 CONTRIBUTING order

1. Scope of accepted contributions, conduct link, and private security route.
2. Toolchain and setup prerequisites.
3. How to open or discuss a change.
4. Change-coupling table: which contract, source, test, and changelog surface
   changes with each kind of behavior.
5. Evidence-source rules, especially hardware versus model/mock/code-reading.
6. Canonical local validation command and what result to include in the PR.
7. PR/review checklist.
8. Changelog, compatibility, and release-impact expectations.

CONTRIBUTING owns contributor-visible mechanics. Avoid hiding a necessary review
condition exclusively in AGENTS.

### 9.2 AGENTS order

1. Authority statement and link to CONTRIBUTING.
2. Product boundary, priorities, and non-goals.
3. Canonical-source map.
4. Load-bearing invariants and coupled edits the compiler cannot enforce.
5. Commands mapped to the claims they establish.
6. Operational traps, known deviations, and rejected approaches.
7. Protected release, publication, visibility, credential, and destructive
   actions.

Avoid duplicating installation instructions, public API inventories, generic
style rules, or literal versions available from a manifest in AGENTS.
Tool-specific files may redirect to AGENTS in one sentence.

## 10. Source and evidence capture

Capture should be proportionate and demand-driven. Survey a source to identify
the peripheral's externally visible features, then select a driver or model
consumer before promoting a source statement into a maintained proposition.
An unconsumed source section does not need a registry row, validation plan,
issue, test, or CI rule.

For repositories that retain device propositions, the
[peripheral-driver evidence resource pack](peripheral-driver-resources/README.md)
is the canonical non-normative implementation reference. It provides a small
[evidence-registry example](peripheral-driver-resources/EVIDENCE_REGISTRY.example.md),
source-catalog guidance, evidence semantics, physical-observation guidance, and
a remediation path. Existing `HARDWARE_CONTRACT.md` files may be remediated in
place; neither that filename nor a specific schema or identifier spelling is
required.

## 11. Existing-contract remediation

Remediate on demand or when a contract is already causing contradictory claims,
invented behavior, or speculative work. Preserve existing identifiers, turn
changed or compound meanings into tombstones plus new atomic propositions, move
driver and model consequences to their owning surfaces, and replace prose copies
with local consequence plus stable-ID citations. Convert unchecked boxes,
review-owner fields, and promises of future validation into the evidence state
actually supported—often `undefined`. An undefined or currently unconsumed row
creates no validation assignment, follow-up, or release block.

Do not require an organization-wide migration or completeness audit. The full
non-normative sequence and stopping conditions live in the
[resource pack](peripheral-driver-resources/README.md#remediate-an-existing-hardware-contract).

## 12. Manifest and package-documentation notes

- Set `readme = "README.md"` in each user-facing nested package.
- Keep `description`, `license`/`license-file`, `repository`, `rust-version`,
  keywords, and categories accurate.
- Omit `homepage` when it only duplicates `repository` or `documentation`.
- Use `[package.metadata.docs.rs]` only for the features, targets, or
  configuration actually needed to render useful documentation.
- Build rustdoc with warnings denied, run doctests, and check broken links.
- Document public items; use intra-doc links rather than a manually copied API
  signature inventory.
- State `no_std`, allocation, and unsafe-code claims narrowly and enforce them
  where possible. `#![forbid(unsafe_code)]` says something about that crate's
  source, not its entire transitive dependency graph.
- Inspect every publishable package, not only the workspace, for its README,
  license, normalized manifest, and intended file set.

Primary references:

- [Cargo manifest `readme`, metadata, MSRV, license, repository, and homepage](https://doc.rust-lang.org/cargo/reference/manifest.html)
- [Cargo packaging and publication inspection](https://doc.rust-lang.org/cargo/reference/publishing.html)
- [crates.io README relative-link rendering](https://github.com/rust-lang/crates.io/blob/main/crates/crates_io_markdown/src/lib.rs)
- [docs.rs build behavior](https://docs.rs/about/builds)
- [docs.rs build metadata](https://docs.rs/about/metadata)
- [docs.rs Markdown rendering](https://github.com/rust-lang/docs.rs/blob/main/crates/bin/docs_rs_web/src/utils/markdown.rs)
- [rustdoc front-page and public-item guidance](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html)
- [GitHub default community-health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [GitHub Actions status badges](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge)
