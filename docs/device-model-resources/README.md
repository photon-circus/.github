# Device behavioral model resources

Status: **Non-normative implementation aids**

These resources help contributors apply the
[Device Behavioral Model Standard](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md)
without rediscovering settled organization-wide decisions. They do not add
requirements, prescribe Rust structure, or define a shared harness API.

The resource pack intentionally has two aids:

- [Implementation brief](IMPLEMENTATION_BRIEF.md): a procedural entry point for
  a contributor or AI agent after it reads the normative core.
- [Behavioral declaration template](MODEL_DECLARATION_TEMPLATE.md): one intake
  record that graduates into the model's maintained declaration.

The declaration template is content, not a required file or a parallel policy
surface. It may begin as the body of the implementation issue. At handoff,
prune it and move the durable answers into an existing crate README, module
document, or other maintained model description. The issue remains discussion
history; it is not a second maintained declaration.

Use the organization's ordinary feature issue and pull-request templates for
workflow metadata. This pack does not install a device-model issue form across
unrelated repositories or create a second pull-request acceptance checklist.
The standard's
[working review prompts](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md#11-working-review-prompts-non-normative)
remain the single non-normative review surface.

When a device exposes a seam the standard does not settle, preserve the source
evidence and propose a standards change or deferred decision. Do not resolve a
shared coordination concern privately inside the model.
