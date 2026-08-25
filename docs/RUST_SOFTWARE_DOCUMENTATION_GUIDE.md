# Rust Software Documentation Guide

Status: **Non-normative guidance**

Scope: User-facing Rust software in Photon Circus repositories, including
libraries, command-line tools, services, procedural macros, FFI packages,
firmware, embedded applications, and `no_std` crates. The guidance applies to
published packages and to repository-local Rust products whose intended users
need to evaluate, build, run, integrate, operate, diagnose, or change them.

Audience: Maintainers, contributors, reviewers, release owners, and coding
agents designing or reviewing user-facing documentation.

This guide adds no organization requirements or release gates. The adopted
[Repository Standards](../REPOSITORY_STANDARDS.md) control if this guide
conflicts with them. The explicitly non-normative
[Repository Contract Guide](REPOSITORY_CONTRACT_GUIDE.md) owns general guidance
about responsibility, claims, evidence, and document placement. Specialized
normative profiles and standards continue to control where they apply. The
[Rust Peripheral-Driver Documentation Guide](PERIPHERAL_DRIVER_DOCUMENTATION_GUIDE.md)
adds driver-specific package, status, evidence, and model guidance.

Every recommendation, imperative, use of "should," and template sentence in
this guide is advisory. When it summarizes an existing requirement, it links
the controlling source for the exact obligation. References to required user
setup or to an external language or tool contract do not create organization
requirements.

## 1. Organize documentation around user outcomes

Documentation is part of a software product's public interface. Types and
signatures expose only part of the contract. Users may still need units,
ranges, ordering, side effects, allocation, blocking, cancellation, retries,
failure state, runtime assumptions, supported features, target differences,
hazards, and migration consequences.

A proportionate documentation set lets an intended user answer six questions:

1. **Fit:** Is this software appropriate for the problem and its constraints?
2. **Adoption:** What is the shortest complete path to a meaningful result?
3. **Contract:** What behavior, failure modes, side effects, and resource costs
   can a caller rely on?
4. **Operation:** How is the software configured, observed, diagnosed, secured,
   and recovered?
5. **Compatibility:** Which versions, features, targets, runtimes, protocols,
   or hardware are supported, and with what evidence?
6. **Change:** What changed, who is affected, and what must an upgrader modify?

Not every repository needs a book, an external site, or a file for each
question. A small library can answer them through a package README, crate-level
rustdoc, item documentation, examples, and a changelog. A service or complex
tool may need separate operational and migration guides. Add a surface when it
serves a distinct audience, authority, task, or change cadence—not because a
template contains another heading.

Experimental work can be incomplete without being misleading. State which
user path exists, what has been checked, which interfaces are provisional, and
what remains unsupported. Do not make a hypothetical future user path read as
current behavior.

## 2. Give each surface one audience and role

Do not write for one abstract "user." Route readers from a concise front door
to the detail needed for their current decision.

| Reader state | Primary question | Recommended starting surface |
| --- | --- | --- |
| Evaluator | Does this fit my constraints? | Package metadata, repository or package README, crate root |
| New adopter | How do I get one meaningful result? | Quick start or linear tutorial |
| Working user | How do I complete a task? | Runnable example or how-to guide |
| Integrator | What is the exact contract? | Crate, module, type, trait, and item rustdoc |
| Operator | How do I configure, observe, secure, and recover it? | Operations, configuration, and troubleshooting guidance |
| Upgrader | What changed and what must I modify? | Changelog, release notes, deprecation notes, and migration guide |
| Contributor | How do I change it safely? | `CONTRIBUTING.md` and linked repository contracts |
| Coding agent | What is expensive to infer or easy to get wrong? | `AGENTS.md` and its canonical-source map |

The root README is the repository front door. A nested package README is a
standalone package-evaluation surface. Crate rustdoc explains API use and
semantics. Contributor and agent files do not replace user documentation, and
user documentation should not contain release mechanics or agent-only traps.

### 2.1 Assign canonical owners

Give each maintained fact one canonical owner. Other surfaces should state only
the consequence their reader needs and link to the owner. Intentional
audience-specific projections, such as a short status statement in both a
package README and crate front page, should be generated, included, or compared
where practical.

| Fact | Useful canonical owner |
| --- | --- |
| Package identity, version, edition, and declared MSRV value | `Cargo.toml` |
| MSRV verification and change policy | One repository toolchain policy selected by the repository |
| Public API semantics | Rustdoc beside the implementation |
| Feature names, defaults, and dependency wiring | `Cargo.toml` |
| Feature behavior, interactions, and user consequences | One maintained feature reference selected by the repository |
| CLI flags and defaults | CLI definition, checked against rendered `--help` |
| Configuration fields | Typed or machine-readable schema plus rendered reference |
| Supported targets or hardware and evidence level | One explicit support matrix selected by the repository |
| Runnable examples | Doctests or named programs under `examples/` |
| Released behavior changes | `CHANGELOG.md` |
| Repository responsibility and evidence boundaries | One repository contract: the root README for a small repository or one linked detailed contract |

Do not maintain API signature inventories in Markdown when rustdoc can own and
check the interface. Do not copy complete feature tables, status blocks, or
examples into several unchecked pages.

### 2.2 Keep version scope visible

User-facing reference material should say which release, branch, or version
range it describes. A site generated from `main` should not look like the stable
reference for an older published package. Prefer versioned API URLs and
release-pinned links for contract material that must remain stable for a
published package.

When a package README is rendered on crates.io, docs.rs, and GitHub, validate
links in every intended context. Archive membership, repository-relative
resolution, and generated-site resolution are different checks.

## 3. Make the README an adoption and routing surface

The adopted standards define the answers required near the top of every root
README. For a user-facing Rust product, a useful order is:

1. Name and one factual positioning sentence.
2. Current lifecycle, distribution, stability, and important non-fit.
3. A complete quick start or a direct route to one.
4. Purpose, responsibility, and explicit non-goals.
5. Compatibility: MSRV, targets, runtime, `std`/`alloc`, native dependencies,
   and important feature constraints.
6. Core concepts or component map when orientation is needed.
7. Documentation map: API reference, examples, how-to material, changelog,
   migration, support, and security.
8. Verification scope, contribution route, and license.

The first screen should establish identity, state, and the next action. Badges,
logos, history, and sponsor material should not delay those answers. Prefer
specific claims such as "fixed-capacity, `no_std`, no heap allocation" to
unbounded adjectives such as "fast," "safe," or "production ready."

### 3.1 State fit and non-fit early

When choosing the software has consequential trade-offs, add compact "Use this
when" and "Do not choose this when" guidance. Name the alternative or owning
layer when known. Examples include blocking versus asynchronous execution,
lossy versus lossless conversion, allocation versus fixed capacity, a stable
machine-output format versus unstable human output, or a driver versus board
integration policy.

Negative information is part of correct adoption. Do not hide unsupported
targets, changed defaults, required native libraries, destructive behavior, or
unverified hardware behind an issue tracker or a late limitations section.

### 3.2 Provide a reproducible first success

A quick start should contain every fact needed to reproduce one meaningful
result:

- prerequisites, including toolchain, target, runtime, service, permissions,
  native library, or hardware;
- dependency addition and every required non-default feature;
- complete imports, construction, and entry point;
- the command to build or run it from a stated working directory;
- an assertion, output, state change, or other observable success condition;
- normal error propagation or bounded error handling; and
- a link to the next realistic task.

One adaptable shape is:

````markdown
## Quick start

Prerequisites: <toolchain, target, runtime, native library, or hardware>.

```text
cargo add <package-name> --features <required-feature>
```

```rust
use <crate_name>::<EntryPoint>;

fn main() -> Result<(), <crate_name>::Error> {
    let result = <complete meaningful operation>?;
    assert_eq!(result.<observable>(), <expected>);
    Ok(())
}
```

Run from `<working-directory>`:

```text
cargo run
```

Expected result: `<observable output or state>`.

Next: [<real task>](<link>).
````

Validate the path in a clean temporary project or equivalent isolated
environment using only the stated prerequisites. An invocation fragment is not
a quick start when the dependency, input, setup, runtime, or expected result is
implicit.

### 3.3 Keep package READMEs standalone

A published nested package does not carry the repository root README by
implication. Give each user-facing package a package-specific README and set its
manifest `readme` field explicitly. The packaged surface should retain the
status, fit, setup, compatibility, material limitations, documentation links,
support route, and license facts required to evaluate that package.

A workspace overview is not a substitute for leaf-package use. Conversely, a
package README should not reproduce repository layout, maintainer release
mechanics, or internal architecture that does not affect package users.

### 3.4 Treat manifest metadata as user documentation

For a publishable package, keep the manifest's `description`, `readme`,
`repository`, `documentation`, `license` or `license-file`, `rust-version`,
keywords, categories, edition, and package identity accurate. The description
should name a concrete capability and material differentiator rather than use a
generic phrase such as "Rust utilities."

Repository and documentation links should lead a package evaluator to the
matching package and version. Omit `homepage` when it only duplicates the
repository or API reference. License metadata should match the distributed
files and the repository's dependency and provenance posture.

Inspect the normalized manifest and exact files Cargo will package. Values
that work in a workspace checkout can still fail after path dependencies,
workspace inheritance, ignored files, generated files, or repository-relative
links cross the package boundary.

## 4. Document semantic contracts in rustdoc

The signature already states names and types. Documentation should explain the
meaning that remains invisible in the type system.

### 4.1 Use each rustdoc layer deliberately

- **Crate root:** capability, problem boundary, mental model, primary entry
  points, feature and target posture, resource or execution model, error
  strategy, important caveats, and a complete example.
- **Module:** domain boundary, relationships among public items, and the
  recommended place to begin.
- **Type or trait:** abstraction, invariants, ownership and lifecycle, state
  transitions, implementor obligations, and non-obvious equality, ordering,
  serialization, pinning, or concurrency semantics.
- **Function or method:** exact operation, units, ranges, state effects,
  failures, resource effects, and applicable platform or feature differences.
- **Constant or static:** meaning, units, source or protocol, valid context,
  stability, and whether the value is a limit, sentinel, address, mask, or
  approximation.
- **Macro:** accepted syntax, generated public effects, required imports and
  features, diagnostics, hygiene limits, and representative invalid use.

Start each item with a concise sentence that distinguishes it from nearby
alternatives. Use intra-doc links and the public paths users are expected to
write.

### 4.2 Review the caller-visible concerns

Consider each concern below and document it when it affects a caller's
decision, correctness, or risk. Do not add empty headings for inapplicable
concerns.

| Concern | Useful questions |
| --- | --- |
| Inputs and outputs | What units, ranges, encodings, freshness, precision, normalization, or ownership apply? |
| Errors and recovery | Which conditions map to which errors? Is retry valid? What state or partial output remains? |
| Panics and aborts | Can ordinary inputs, capacity, state, overflow, or sequencing trigger them? |
| Safety | Which validity, alignment, aliasing, lifetime, synchronization, and ownership obligations protect safe code? |
| Side effects and atomicity | What I/O or mutation occurs? Can observers see partial state? What survives interruption? |
| Ordering and determinism | Is order stable, unspecified, backend-dependent, scheduled, randomized, or locale-sensitive? |
| Resources | Does the operation allocate, copy, block, sleep, spin, hold a lock, enter a critical section, or have a material worst case? |
| Async and cancellation | Which runtime, executor, timer, or wake source applies? Is cancellation safe, and what work may already have committed? |
| Concurrency | What thread, interrupt, signal, core, reentrancy, or synchronization assumptions apply? |
| Lifecycle | Who owns resources, when are they released, and what does `Drop` do? |
| Compatibility | Which features, targets, platforms, upstream versions, protocols, or hardware variants apply? |
| Security | Does it process secrets or untrusted input, cross a trust boundary, or expose denial-of-service risk? |

Use conventional `# Errors`, `# Panics`, and `# Safety` headings when they
apply. An unsafe item needs a complete caller obligation rather than a circular
statement such as "the pointer must be valid." A trait intended for third-party
implementation needs the implementor contract, not only an example that calls
one method.

For error types, explain categories, recovery, transient versus permanent
conditions, sources, matching stability, and partial state. For deprecated
items, link the replacement and name material semantic differences.

## 5. Treat examples as maintained user paths

A useful example establishes a problem, complete setup, intended control flow,
error path, and observable result. Hide only boilerplate that does not affect
understanding. Do not hide a runtime, feature, safety precondition, resource
lifecycle, or hardware assumption.

Prefer doctests for focused API use and named programs under `examples/` for
tasks that combine APIs, require arguments or external resources, demonstrate
alternative backends, or need substantial explanation. Name examples after
the user task, such as `read_temperature`, `convert_fixture`, or
`custom_executor`, rather than `example3`.

For code blocks collected by rustdoc as doctests, choose behavior deliberately:

- ordinary Rust doctest blocks compile and run;
- `no_run` compiles code that requires hardware, credentials, a service, a
  destructive effect, or a long-lived process;
- `compile_fail` demonstrates a rejected use or type-state boundary;
- `should_panic` demonstrates an intentional, unambiguous panic contract;
- `text` marks output, pseudocode, or intentionally incomplete Rust; and
- `ignore` is a last resort, not a permanent way to hide drift.

These attributes do not make arbitrary README or guide blocks compile or run.
Route non-rustdoc blocks through a repository check that extracts, builds,
executes, or otherwise validates them at the level the documentation claims.

Declare required features for Cargo example targets when appropriate. State
target, runner, fixture, service, file, environment, and hardware prerequisites
before the example. If the path cannot run in routine CI, document whether it
is compiled, manually exercised, or retained only as illustrative material and
record the acceptance condition used at its declared evidence level.

`unwrap()` can be defensible for a hard-coded invariant in a minimal example,
but it should not make panic-driven integration look like the normal error
model. Examples that accept user, I/O, service, or hardware input should show
propagation, validation, or recovery as appropriate.

## 6. Make configuration and compatibility explicit

Every user-selectable feature changes the public configuration surface.
Document whether it is enabled by default, what capability or API it changes,
which dependencies or platforms it introduces, how it interacts with other
features, and its material effect on `std`, allocation, size, build time, MSRV,
runtime, or stability.

| Feature | Default | Public effect | Dependencies | Constraints |
| --- | --- | --- | --- | --- |
| `<feature>` | yes/no | `<capability or API change>` | `<dependency or none>` | `<interaction, target, runtime, or MSRV>` |

Show common supported dependency configurations. When disabling default
features removes behavior, integration, security hardening, or error support,
say what is lost as well as what remains.

An MSRV statement should identify:

- the minimum compiler version;
- the feature and target scope to which it applies;
- how the repository verifies it;
- the policy for raising it; and
- where an increase is announced.

For platform-sensitive software, define support tiers by evidence rather than
using "cross-platform" as a blanket claim. Distinguish at least the relevant
states: routinely tested, release-tested, compile-only, physically exercised,
community-reported, or expected but unsupported. State behavioral platform
differences, not only `cfg` names.

Configure docs.rs for a deliberate, buildable, representative feature and
target set. Use `all-features = true` only when all features are compatible and
the resulting page represents a useful configuration. When docs.rs cannot
build the package, provide a clearly versioned alternative API reference and
explain the supported configuration.

## 7. Add product-specific material only when it applies

The common outcomes remain the same, but different Rust products expose
different user risks.

| Product | Material user-facing questions |
| --- | --- |
| Library crate | What abstraction does it own? How are values constructed, composed, extended, failed, retried, and released? Does it block, allocate, require a runtime, or integrate with ecosystem traits? |
| Command-line tool | What is the command hierarchy? What are defaults, formats, precedence, stdin/stdout/stderr, exit statuses, machine-output stability, prompts, destructive effects, and platform shell differences? |
| Service or daemon | How is it installed, configured, authenticated, observed, drained, backed up, restored, upgraded, rolled back, rate-limited, and recovered? Where is data stored and what are the trust boundaries? |
| Procedural macro | Which syntax and attributes are accepted? What public code, bounds, names, visibility, imports, and diagnostics are generated? Which invalid uses deserve `compile_fail` examples? |
| FFI or `-sys` crate | Which upstream version, target, ABI, link mode, generation provenance, native prerequisite, license, ownership, allocation, nullability, thread, callback, encoding, and unwind rules apply? |
| Embedded or `no_std` crate | What are the `std`/`alloc`, target, HAL/PAC, execution, timer, interrupt, DMA, memory, panic, reset, power, electrical, bus, timing, units, recovery, and hardware-evidence boundaries? |
| Firmware or embedded application | Which board, image, memory map, boot path, configuration, flashing procedure, observable output, safe power state, rollback, and operator-owned integration decisions apply? |
| Generator or automation tool | Which inputs, outputs, filesystem or network effects, determinism, schema, credentials, overwrite rules, dry-run behavior, and recovery guarantees apply? |

The specialized driver guide controls the recommended projections of driver
lifecycle, distribution, model-conformance, and physical-evidence status. Do
not apply its four-field status block to unrelated Rust products.

## 8. Document operation, troubleshooting, support, and security

Operational documentation should expose configuration types, defaults,
validation, precedence, reload behavior, observability, persistent state,
limits, startup and shutdown, backup, restore, and recovery when those concerns
exist. Keep exhaustive fields in a reference and safe procedures in how-to
guides.

Place prerequisites, scope, hazards, backup, and rollback before a destructive,
irreversible, privileged, electrical, or security-sensitive action. A warning
after the command is too late.

A useful troubleshooting entry follows an evidence-to-recovery path:

1. **Applies to:** versions, features, targets, platforms, or hardware.
2. **Symptom:** exact error, state, log event, or failed outcome.
3. **Likely causes:** ordered possibilities with discriminating evidence.
4. **Diagnostic:** command, status, trace, metric, register, or observation.
5. **Correction:** bounded action with prerequisites and risk stated first.
6. **Verification:** observable evidence that the fault is resolved.
7. **Escalation data:** version, configuration, complete error chain, minimal
   reproduction, redacted logs, and hardware details as applicable.

Do not collect unverified forum answers into a troubleshooting page. State the
conditions under which a correction was validated.

Give users stable diagnostic vocabulary where useful: error codes, exit
statuses, log events, metrics and units, trace relationships, debug commands,
status flags, data locations, and redaction rules. State where usage questions,
reproducible defects, and private security reports belong and which release
lines are supported.

## 9. Communicate change from the user's perspective

Keep three jobs distinct even when one file performs all of them:

- a changelog records user-visible changes;
- release notes interpret the value, impact, and compatibility of a release;
  and
- a migration guide gives an ordered, verifiable procedure.

For a breaking change or consequential changed default, explain:

1. previous behavior or API;
2. new behavior or API;
3. affected users and configurations;
4. the mechanical edits available;
5. semantic decisions the user must make;
6. validation and rollback constraints; and
7. any deprecation or compatibility window.

Record user-visible changes to behavior, defaults, errors, MSRV, features,
targets, dependencies, data, protocols, security, resource use, or operation.
Raw commit messages, filenames, and internal refactors are not release guidance
unless they have a user consequence.

A deprecation should identify its replacement, the version in which it began,
the removal policy if known, and every material semantic difference. A
migration guide should name supported source and destination versions,
prerequisites, before-and-after configuration or code, ordered data or protocol
steps, validation, and rollback limits.

## 10. Write direct, accessible, stable documentation

- Address the reader directly and use imperative steps where appropriate.
- Put conditions before actions and the normal path before optional variants.
- Replace "just," "simply," "obviously," and "easy" with the actual
  prerequisite or remove them.
- Give one concept one stable name and match code, CLI, UI, protocol, and
  documentation terminology.
- Distinguish package, crate, workspace, module, binary, and repository;
  asynchronous, concurrent, and non-blocking; and supported, tested,
  compatible, observed, and expected to work.
- State units, encodings, time zones, and unambiguous ISO 8601 dates where they
  affect interpretation.
- Use goal-oriented headings, numbered procedures, copyable commands, expected
  checkpoints, and cleanup or rollback where relevant.
- Give links descriptive text and images useful alt text. Do not encode meaning
  only by color, screenshot, hover state, animation, or viewport position.
- Keep code and output selectable. Provide textual explanations for diagrams
  and videos.
- Use diagrams only when they make ownership, flow, state, timing, topology, or
  layering materially clearer; retain an editable source and identify version
  scope.

Review the rendered documentation, not only its source. Heading hierarchy,
tables, callouts, code languages, link labels, line wrapping, and relative
paths can fail while the Markdown remains syntactically valid.

## 11. Maintain documentation with the implementation

When a change alters user-visible behavior, review the documentation in the
same change. Ask:

- Which user-facing contract changed?
- Which README, rustdoc item, guide, example, configuration reference, or CLI
  help owns that contract?
- Did errors, panics, safety, side effects, performance, allocation, blocking,
  cancellation, or recovery change?
- Did features, defaults, targets, MSRV, dependencies, protocol, hardware, or
  evidence scope change?
- Does the quick start still show the recommended supported path?
- Is a changelog, deprecation, release-note, or migration entry needed?

The implementation author should provide the first accurate contract update.
Other reviewers can improve navigation, task success, accessibility, and
language, but they should not be expected to infer semantics after the change
has shipped.

### 11.1 Add proportionate automated checks

Integrate documentation checks into the repository's one canonical
verification entry point when they establish supported claims. Common library
checks include:

```text
cargo test --doc
cargo rustdoc -- -D warnings
cargo package --list
```

Add named supported feature and target configurations rather than assuming the
default build represents every user. Run `--all-features` only when that
combination is valid.

Useful additional checks include:

- rustdoc lints for broken intra-doc links, invalid code blocks and HTML, bare
  URLs, and missing documentation according to repository policy;
- README and guide code blocks not exercised as doctests;
- internal and external links in every intended rendered context;
- package-relative images, licenses, and attachments;
- generated CLI help, configuration examples, schemas, feature lists, and
  machine-readable output;
- representative docs.rs feature and target configuration;
- clean-project quick starts and promoted examples; and
- heading order, alt text, descriptive links, and table headers.

Automation detects drift; it does not prove that explanations are accurate,
risks are visible, navigation works for a new reader, or the selected example
solves a meaningful task. Keep a rendered and user-path review in release or
change review where the risk warrants it.

### 11.2 Review the packaged and published surfaces

Before a release, review the exact package or artifact rather than only the
working tree. Proportionate documentation review considers:

- packaged README and license presence;
- manifest metadata and version-scoped links;
- declared MSRV and supported feature/target configurations;
- doctests and promoted examples at their declared evidence level;
- rustdoc output and selected lint results;
- quick start from a clean consumer project;
- docs.rs metadata or an equivalent versioned reference;
- new public APIs' semantic, error, panic, and safety documentation;
- changed defaults, features, targets, MSRV, data, protocols, and migrations;
  and
- deprecation replacements, security guidance, and support routes.

The adopted release standard and any applicable profile remain the authority
for actual publication gates. This list neither authorizes publication nor
makes every check applicable to every product.

## 12. Adopt the smallest useful improvement first

For an existing Rust product with weak user documentation, a useful sequence
is:

1. Repair identity, status, metadata, package-specific routing, license, and
   support links.
2. Make one clean-environment quick start produce an observable result.
3. Explain the crate or product mental model, primary entry points, boundaries,
   and major caveats.
4. Close high-risk semantic gaps: safety, failure, destructive effects,
   blocking, allocation, concurrency, hardware, and recovery.
5. Document common public entry points and implementor contracts.
6. Promote tested examples for real tasks and supported configurations.
7. Add troubleshooting, diagnostics, deprecations, and migration paths.
8. Automate the checks that catch likely drift.
9. Review the rendered and packaged user path from a clean environment.

Stop when the intended user can evaluate, start, use, diagnose, and change the
software within its declared scope. Do not manufacture a large documentation
set, numeric quality score, or speculative release gate when a smaller complete
account serves the current product honestly.

## 13. Compact review prompts

- Can an evaluator identify purpose, status, fit, non-fit, compatibility, and
  evidence limits before adopting the product?
- Can a new user reproduce one meaningful result using only stated
  prerequisites?
- Does rustdoc explain semantic behavior not encoded by types, including
  failure, safety, resource, execution, and platform behavior where relevant?
- Are features, defaults, MSRV, targets, runtimes, native dependencies, and
  version scope explicit at the surfaces where users encounter them?
- Are examples compiled or otherwise assigned an honest validation level, with
  required setup and an observable result?
- Can an operator diagnose and verify recovery from a representative failure?
- Are hazards and destructive effects disclosed before the action?
- Can an upgrader identify changed behavior, affected users, required edits,
  semantic decisions, and validation?
- Does each maintained fact have one canonical owner, with intentional
  projections kept consistent?
- Do rendered, packaged, and published documentation describe the same
  supported release and configuration?

## Primary references

- [The rustdoc book: how to write documentation](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html)
- [The rustdoc book: documentation tests](https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html)
- [The rustdoc book: rustdoc-specific lints](https://doc.rust-lang.org/rustdoc/lints.html)
- [Rust API Guidelines: documentation](https://rust-lang.github.io/api-guidelines/documentation.html)
- [RFC 1574: API documentation conventions](https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html)
- [The Cargo Book: manifest format](https://doc.rust-lang.org/cargo/reference/manifest.html)
- [The Cargo Book: features](https://doc.rust-lang.org/cargo/reference/features.html)
- [The Cargo Book: publishing](https://doc.rust-lang.org/cargo/reference/publishing.html)
- [The Cargo Book: `cargo rustdoc`](https://doc.rust-lang.org/cargo/commands/cargo-rustdoc.html)
- [docs.rs build metadata](https://docs.rs/about/metadata)
- [Diataxis documentation framework](https://diataxis.fr/)
- [Embedded Rust Book](https://docs.rust-embedded.org/book/)
- [Google developer documentation style guide](https://developers.google.com/style)
