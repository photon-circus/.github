# Photon Circus organization standards

This repository contains the shared repository, contribution, release, and engineering standards for the Photon Circus GitHub organization.

Start with the [Photon Circus Repository Standards](REPOSITORY_STANDARDS.md).

The explicitly non-normative
[Repository Contract Guide](docs/REPOSITORY_CONTRACT_GUIDE.md) offers
category-neutral guidance for expressing repository-local responsibility,
consumer handoffs, evidence boundaries, component roles, and controlled
contract evolution across all repository and material component types. It
includes a provisional initial development contract and a concrete,
evidence-triggered re-examination once the first usable surface exists.

Peripheral drivers also follow the
[Peripheral Driver Release and Evidence Profile](docs/PERIPHERAL_DRIVER_PROFILE.md).
The
[Device Behavioral Model Standard](docs/DEVICE_BEHAVIORAL_MODEL_STANDARD.md)
defines a normative responsibility and implementation core for driver-test
models, surrounded by explicitly non-normative rationale and review guidance,
so independently acting contributors and AI agents inherit settled decisions
without making model success a hardware-qualification claim.
The explicitly non-normative
[Rust Peripheral-Driver Documentation Guide](docs/PERIPHERAL_DRIVER_DOCUMENTATION_GUIDE.md)
offers proportional structures for repository, package, source, contribution,
and agent documentation without adding requirements.
The explicitly non-normative
[Rust xtask field guide for Photon Circus technical repositories](docs/PERIPHERAL_DRIVER_XTASK_GUIDE.md)
records what several native cross-platform verification gates made better,
what failed during adoption, and which design choices remain local.
The
[device model resource pack](docs/device-model-resources/README.md) provides
non-normative procedural, declaration, and optional Rust workspace integration
aids that apply those decisions without prescribing code structure.
The
[peripheral-driver evidence resource pack](docs/peripheral-driver-resources/README.md)
provides optional, non-normative guidance for demand-driven proposition capture,
evidence state, physical observations, downstream citations, and remediation of
legacy hardware contracts without requiring a particular registry schema or an
organization-wide migration.

The standards favor deterministic, bare-metal engineering; narrowly bounded responsibilities; honest evidence; and lifecycle-appropriate process. Existing repository and package names are grandfathered under v0.1.

## Status

The numbered `0.1.0` baseline was adopted on 2026-08-11 UTC. The live `main`
branch is the current adopted authority; the
[normative-language section](REPOSITORY_STANDARDS.md#1-normative-language)
defines effectivity and reproducible pinning.

Changes to normative requirements are documented in [CHANGELOG.md](CHANGELOG.md).

## Organization-wide community-health fallbacks

The root [contribution](CONTRIBUTING.md) and [security](SECURITY.md) files are
intentionally general because GitHub may display them in Photon Circus
repositories that do not provide local replacements. They defer to guidance
committed in the target repository and do not replace the repository-specific
files required by the standards.

Changes to this standards repository also follow
[Contributing to Photon Circus standards and organization defaults](docs/CONTRIBUTING_TO_STANDARDS.md).

## Standards audit

The [read-only repository auditor](docs/STANDARDS_AUDIT.md) collects Markdown and JSON evidence against machine-observable parts of the standard. It has no remediation mode or authority to change anything it flags.

## Future driver-bootstrap machinery

The [Peripheral Driver Bootstrap Intent](docs/PERIPHERAL_DRIVER_BOOTSTRAP_INTENT.md)
records the authority boundary, independent derivation lanes, temporary-workspace
model, and durable handoff expected from future local tooling. It records design
intent only, including a disposable feature survey followed by consumer-driven
promotion of the smallest needed propositions; executable bootstrap machinery
and workspace-generation templates do not yet exist. The non-executable
device-model aids above do not implement that deferred tooling.

## License

MIT. See [LICENSE](LICENSE).
