# Device behavioral model resources

Status: **Non-normative implementation aids**

These resources help contributors apply the
[Device Behavioral Model Standard](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md)
without rediscovering settled organization-wide decisions. They do not add
requirements, prescribe Rust structure, or define a shared harness API.

The resource pack intentionally has three aids:

- [Implementation brief](IMPLEMENTATION_BRIEF.md): a procedural entry point for
  a contributor or AI agent after it reads the normative core.
- [Behavioral declaration template](MODEL_DECLARATION_TEMPLATE.md): one intake
  record that graduates into the model's maintained declaration.
- [Rust workspace integration note](RUST_WORKSPACE_INTEGRATION.md): an optional
  packaging and validation recipe for repositories that have already chosen an
  unpublished workspace model crate.

The declaration template is content, not a required file or a parallel policy
surface. It may begin in the current work record when one exists. At handoff,
prune it and move the durable answers into an existing crate README, module
document, or other maintained model description. Any issue remains discussion
history; it is not a second maintained declaration.

Use the organization's ordinary feature issue and pull-request templates for
workflow metadata. This pack does not install a device-model issue form across
unrelated repositories or create a second pull-request acceptance checklist.
The standard's
[working review prompts](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md#11-working-review-prompts-non-normative)
remain the single non-normative review surface.

When evidence does not settle a device behavior, return to the shared stable
proposition and record the model's local consequence, including unsupported.
Propose a standards change only when repeated repository experience identifies
a genuinely shared coordination gap; a local disagreement does not create one.
