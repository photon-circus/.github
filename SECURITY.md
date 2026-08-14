# Security policy

This file is an organization-wide fallback. GitHub may display it for a Photon
Circus repository that does not commit its own `SECURITY.md`.

## Reporting a vulnerability

Follow the security policy committed in the affected repository when it has
one; that local policy controls over this fallback. Otherwise, report the issue
privately through the affected repository's **Security** tab and **Report a
vulnerability** option when available. If private reporting is not available,
use a nonpublic maintainer channel already named by that repository. If it names
none, open a
[minimal contact-request issue](https://github.com/photon-circus/.github/issues/new?title=Private%20security%20contact%20requested&body=Private%20security%20contact%20requested.)
containing only the sentence "Private security contact requested." Do not name
a private repository or describe the vulnerability. Maintainers should arrange
a private channel before accepting any sensitive details.

Once a private reporting channel is established, include enough context to
reproduce and assess the report:

- Affected repository, package, version, release, or commit.
- Impact, prerequisites, and the smallest safe reproduction.
- Toolchain, target, enabled features, and relevant configuration.
- For hardware-sensitive reports, the device, silicon, board, and MCU revisions
  and the bus or interface mode.
- Whether the evidence came from physical hardware, a model or simulation, a
  mock, source documents, or code analysis.
- Known mitigations and whether disclosure is already public.

Do not disclose credentials, access tokens, private repository contents,
confidential or redistribution-restricted vendor material, unpublished
vulnerability details, or hardware secrets in a public issue, pull request,
discussion, log, or test artifact. Redact unrelated sensitive data from private
reports as well.

## This standards repository

[`photon-circus/.github`](https://github.com/photon-circus/.github) contains
documentation and organization defaults rather than executable production
software. Report a security risk in its standards, templates, or workflows
through its
[private GitHub security-advisory interface](https://github.com/photon-circus/.github/security/advisories/new)
when available. If that option is unavailable, use the minimal contact-request
issue described above.

Ordinary corrections and hardening proposals may be submitted through public
issues or pull requests only when they contain no sensitive information.
