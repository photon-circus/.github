# Device behavioral model resources

Status: **Non-normative implementation aids**

These resources help contributors apply the
[Device Behavioral Model Standard](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md)
without rediscovering settled organization-wide decisions. They do not add
requirements, prescribe Rust structure, or define a shared harness API.

Use only the aids that reduce current work:

- [Implementation brief](IMPLEMENTATION_BRIEF.md): a compact task packet for a
  contributor or AI agent.
- [Behavioral declaration template](MODEL_DECLARATION_TEMPLATE.md): prompts for
  the model-specific claim, boundary, fidelity, and source decisions.
- [Review checklist](REVIEW_CHECKLIST.md): a proportional review aid for a
  device-model pull request.
- [Minimal bus-switch example](TCA9548A_DECLARATION_EXAMPLE.md): an example of
  a completed declaration without implementation or repository scaffolding.

The declaration template is content, not a required file. Prefer completing it
inside an existing crate README, module document, or other maintained model
description. Delete prompts that do not apply. Do not create parallel documents
that restate the same claim.

The issue form at
[`device-behavioral-model.yml`](../../.github/ISSUE_TEMPLATE/device-behavioral-model.yml)
can capture source and boundary work before implementation. The pull-request
template at
[`device-behavioral-model.md`](../../.github/PULL_REQUEST_TEMPLATE/device-behavioral-model.md)
can be selected for model changes.

When a device exposes a seam the standard does not settle, preserve the source
evidence and propose a standards change or deferred decision. Do not resolve a
shared coordination concern privately inside the model.
