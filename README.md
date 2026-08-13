# Photon Circus organization standards

This repository contains the shared repository, contribution, release, and engineering standards for the Photon Circus GitHub organization.

Start with [Photon Circus Repository Standards v0.1](REPOSITORY_STANDARDS.md).

Unpublished peripheral drivers also follow the
[Pre-`ph-hil` Peripheral Driver Profile](docs/PERIPHERAL_DRIVER_PROFILE.md).
The
[Device Behavioral Model Standard](docs/DEVICE_BEHAVIORAL_MODEL_STANDARD.md)
defines a normative responsibility and implementation core for driver-test
models, surrounded by explicitly non-normative rationale and review guidance,
without making model success a hardware-qualification claim.

The standards favor deterministic, bare-metal engineering; narrowly bounded responsibilities; honest evidence; and lifecycle-appropriate process. Existing repository and package names are grandfathered under v0.1.

## Status

Version 0.1.0 was adopted on 2026-08-11 UTC.

Changes to normative requirements are documented in [CHANGELOG.md](CHANGELOG.md).

## Standards audit

The [read-only repository auditor](docs/STANDARDS_AUDIT.md) collects Markdown and JSON evidence against machine-observable parts of the standard. It has no remediation mode or authority to change anything it flags.

## Future driver-bootstrap machinery

The [Peripheral Driver Bootstrap Intent](docs/PERIPHERAL_DRIVER_BOOTSTRAP_INTENT.md)
records the authority boundary, independent derivation lanes, temporary-workspace
model, and durable handoff expected from future local tooling. It records design
intent only; the machinery and reusable templates do not yet exist.

## License

MIT. See [LICENSE](LICENSE).
