# Rust workspace integration note

Status: **Non-normative implementation aid**

This note records one proportional way to integrate an unpublished Rust device
behavioral model with a driver repository. It applies only when the repository
has already chosen a separate workspace crate because that packaging makes the
current independence boundary easy to inspect. It does not require a separate
crate, standardize a model API, or create a precedent for another repository.

The normative
[Device Behavioral Model Standard](../DEVICE_BEHAVIORAL_MODEL_STANDARD.md)
controls whenever this note is used.

## Dependency direction

Keep the implementation dependencies one-way:

```text
production driver       device model
       ^                      ^
       |                      |
       +-- conformance test --+
```

- Production driver code does not depend on model implementation code.
- Model implementation code does not depend on production-driver encodings,
  transactions, timing helpers, or state machines.
- A conformance integration test may depend on both and exercise the driver
  through its public transport and delay boundaries.

A path-only development dependency is sufficient when the model is an
unpublished workspace package:

```toml
[dev-dependencies]
device-model = { path = "../device-model" }
```

Cargo includes only development dependencies that specify a registry version
when it prepares a package for publication. It can therefore omit this
path-only dependency from the normalized package manifest while still including
an integration-test source file that imports the model. Ordinary `cargo
package` verification can remain green because it verifies the package's normal
build, while `cargo test` against the unpacked package fails to compile that
test. See the Cargo Book's
[development-dependency publication rule](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#development-dependencies).

Keep conformance-only test source out of the distributable driver package when
its model dependency is intentionally unpublished, or place the conformance
consumer in another non-distributable workspace package. Add a registry version
only when that exact package and version genuinely exist; do not create a
fictional published dependency to retain a packaged test or satisfy a
dependency-policy check.

If the repository denies wildcard dependency versions with `cargo-deny`, its
[documented path exception](https://embarkstudios.github.io/cargo-deny/checks/bans/cfg.html#the-allow-wildcard-paths-field-optional)
can retain the general policy while allowing local development dependencies:

```toml
[bans]
wildcards = "deny"
allow-wildcard-paths = true
```

This is a repository tooling choice, not a device-model requirement. Confirm
the installed `cargo-deny` version supports the option before adopting it.

## Test-side adapters

Keep transport and driver-delay adapters with the conformance test or another
external support layer, not in the behavioral core. The current adapter should
do only what its consumer needs:

- translate the driver's supported abstract transport operations into model
  inputs;
- route driver-requested delay to the model's explicit relative-duration
  input; and
- preserve the difference between a device response and a model limitation.

When a required Rust trait contains methods outside the current model claim,
return a concrete test error that retains the model limitation. Do not panic for
an ordinary unsupported method merely because the current driver does not call
it. A panic remains appropriate for a genuine test invariant or programming
defect, not for declared unsupported fidelity.

## Bounded verification

Extend the repository's existing local gate rather than adding a second policy
script. Useful checks for this packaging include:

```text
model-only tests without the production driver
driver-versus-model integration tests
normal formatting, lint, documentation, and target checks for both packages
dependency-policy checks
driver package listing and package verification
```

Package listing should confirm that the model implementation is not included
in the distributable driver package. It should also confirm that conformance
test sources depending on an omitted path-only development dependency are not
included. Package verification should continue to work while the model remains
unpublished. When such test sources intentionally remain in the package, test
the unpacked package rather than treating normal package verification as proof
that every packaged test target compiles.

## Documentation

Maintain the model claim in one existing crate README, module document, or
other durable location. Update other repository documents only when the new
model makes an existing statement false or when one index link is needed. Do
not mirror the behavioral declaration across several policy surfaces.

This integration shape should be replaced or omitted whenever a smaller local
arrangement preserves the same independence and current consumer value.
