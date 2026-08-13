# Device behavioral model review checklist

Status: **Non-normative review aid**

Use the applicable prompts; this is not an additional acceptance standard.

## Claim and evidence

- [ ] The exact device, behavioral selection, source revision, and model purpose
      are visible.
- [ ] The change states what model agreement establishes and avoids physical or
      silicon-qualification claims.
- [ ] Source ambiguities are recorded; source-undeclared behavior is not
      silently invented.

## Boundary

- [ ] Every mutation is attributable to an explicit ordered input.
- [ ] Pure inspection is stable while the temporal frontier is unchanged.
- [ ] Relative duration is unit-bearing when time has a modeled consequence;
      the device does not own absolute harness time.
- [ ] Environmental truth, applied stimulus, and device measurement state are
      distinct.
- [ ] Documented transport side effects are visible in the behavioral claim.
- [ ] Unsupported model input remains distinguishable from a device refusal.

## Independence and proportionality

- [ ] Device behavior was derived independently of production constants,
      codecs, helpers, or transaction construction.
- [ ] Packaging is justified locally rather than treated as a shared semantic
      requirement.
- [ ] A future conformance consumer can use both implementations without either
      depending on the other.
- [ ] Supporting code, documents, scripts, adapters, and tests each address a
      current behavior or false-pass risk.
- [ ] No shared framework or coordinator contract was introduced from a single
      implementation without a current consumer or repeated semantic need.

## Handoff

- [ ] One maintained declaration covers modeled, abstracted, injected,
      excluded, and unsupported behavior.
- [ ] Verification commands and results are recorded.
- [ ] Remaining device-specific ambiguity and shared deferred questions are
      routed to their appropriate durable owner.
