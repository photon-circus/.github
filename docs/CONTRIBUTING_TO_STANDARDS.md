# Contributing to Photon Circus standards and organization defaults

Status: **Repository-specific contribution instructions; non-normative for
downstream repositories**

This guide applies specifically to changes in
[`photon-circus/.github`](https://github.com/photon-circus/.github). Start with
the organization-wide [contribution fallback](../CONTRIBUTING.md), then follow
the repository-specific instructions below. They govern contributions here;
they do not add requirements to the Repository Standards for downstream
repositories.

Changes to these standards and organization defaults should be proposed through
a pull request.

Explain:

- What requirement, guidance, template, or organization default changes.
- Which repository classes or lifecycle states are affected.
- Why the change creates value.
- Which existing practice or repository experience supports it.
- Whether adoption requires repository migrations or organization-setting
  changes.
- Whether an edited root community-health file will be inherited by
  repositories that do not provide a local replacement.

Identify whether the change is normative or non-normative. Do not make an
incidental normative change while editing explanatory guidance, templates, or
examples. Normative changes must update `CHANGELOG.md`. Material changes to
non-normative guidance or organization defaults should also be recorded under
`Unreleased` so their effect is reviewable.

Use UTC dates in `YYYY-MM-DD` form. Do not rename existing repositories or
packages as an incidental part of a standards change.

For documentation-only changes, inspect the rendered Markdown and validate all
changed relative links. Changes to the repository auditor or its policy should
also run:

```text
python -m unittest discover -s tests -v
```

Record checks that could not run and why. Approval of a pull request does not by
itself authorize publishing, organization-setting changes, repository
migrations, lifecycle promotion, or other irreversible actions.
