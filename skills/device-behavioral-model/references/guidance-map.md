# Guidance map

This map points to the maintained Photon Circus guidance. It does not summarize
or replace that guidance. Load current content from the target checkout when it
contains these files; otherwise load it from the canonical public repository.

## Always load

1. **Device Behavioral Model Standard** — read the complete document, including
   its status map, normative core, and non-normative review prompts.
   - Repository path: `docs/DEVICE_BEHAVIORAL_MODEL_STANDARD.md`
   - Canonical URL: <https://github.com/photon-circus/.github/blob/main/docs/DEVICE_BEHAVIORAL_MODEL_STANDARD.md>
2. **Device behavioral model implementation brief** — use as the procedural
   entry point after reading the standard.
   - Repository path: `docs/device-model-resources/IMPLEMENTATION_BRIEF.md`
   - Canonical URL: <https://github.com/photon-circus/.github/blob/main/docs/device-model-resources/IMPLEMENTATION_BRIEF.md>

## Load by task

- **Scoping or declaration work:** read the behavioral declaration template.
  - Repository path: `docs/device-model-resources/MODEL_DECLARATION_TEMPLATE.md`
  - Canonical URL: <https://github.com/photon-circus/.github/blob/main/docs/device-model-resources/MODEL_DECLARATION_TEMPLATE.md>
- **Considering a separate Rust workspace crate:** read the Rust integration
  note only after repository evidence makes that packaging a live option.
  - Repository path: `docs/device-model-resources/RUST_WORKSPACE_INTEGRATION.md`
  - Canonical URL: <https://github.com/photon-circus/.github/blob/main/docs/device-model-resources/RUST_WORKSPACE_INTEGRATION.md>
- **Encountering a coordination seam or proposing shared machinery:** read the
  deferred-decision register before making a local choice.
  - Repository path: `docs/DEVICE_MODEL_COORDINATION_DEFERRED_DECISIONS.md`
  - Canonical URL: <https://github.com/photon-circus/.github/blob/main/docs/DEVICE_MODEL_COORDINATION_DEFERRED_DECISIONS.md>

Also read the target repository's own accepted source registry and hardware
contract. Those device-specific records control the modeled part behavior; the
organization documents control shared responsibility and compatibility
boundaries.
