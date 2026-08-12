# Changelog

All notable changes to the Photon Circus organization standards are documented in this file.

## Unreleased

### Added

- Public organization profile introducing Photon Circus, its engineering principles, featured projects, and adopted repository standards.
- Shared bug-report, feature-proposal, and pull-request templates that preserve bounded scope, evidence provenance, compatibility decisions, and explicit handoffs across repositories without local overrides.
- Read-only repository standards auditor producing Markdown and JSON evidence without remediation authority or GitHub write operations.
- Peripheral-driver bootstrap design intent (2026-08-12 UTC) defining
  source-first intake, bounded task packets, independent driver/mock/validation
  lanes, temporary workspace boundaries, durable artifact graduation, and the
  future home for reusable local tooling. This preserves a repeatable path from
  data sheet to reviewable driver without making temporary agent coordination or
  self-validating implementations part of the product repository.

## 0.1.0 - 2026-08-11

**What this release delivers.** This first standards release gives Photon Circus repositories a shared language for bounded scope, lifecycle, naming, documentation, licensing, contributions, feature development, verification, CI, branch protection, and releases. It was created so strong local engineering can remain maintainable as the organization grows, while allowing experiments to stay honest experiments and requiring supported work to carry reproducible evidence.

### Added

- Repository Lifecycle and Domain classifications.
- Bounded-scope and invariant-ownership principles.
- Prospective `ph-` naming and peripheral-driver class tokens.
- README, documentation, changelog, and licensing requirements.
- MIT as the default license with justified Apache-2.0 exceptions.
- Contribution and hardware-evidence guidance.
- Feature proposal, independent-PR, and first-class rejection practices.
- Local-first CI for private repositories and bounded hosted CI for public releases.
- `main` as the default for future repositories, with existing branch names grandfathered.
- Lifecycle-sensitive branch protection, release, and adoption rules.

### Known issues

- Organization-wide templates, property assignment, repository audits, and ruleset rollout remain follow-up adoption work.
