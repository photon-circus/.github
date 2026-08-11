# Photon Circus

**Deterministic, bare-metal software for embedded systems, instruments, and strange machines.**

Photon Circus is an open engineering workshop for embedded Rust, narrowly scoped peripheral drivers, reusable MCU primitives, and the tooling needed to make their behavior measurable.

We favor predictable execution, explicit memory and timing costs, honest hardware evidence, and APIs that expose important failure modes instead of hiding them. Experiments are welcome, but supported components have bounded responsibilities and documented proof for the claims they make.

## Featured projects

- [ph-eventing](https://github.com/photon-circus/ph-eventing) — stack-allocated `no_std` ring buffers with explicit overwrite and backpressure semantics, verified with Miri and Loom.
- [ph-curves](https://github.com/photon-circus/ph-curves) — deterministic embedded curves, calibrated transfer functions, temporal filters, and tickless scheduling without allocation.
- [ph-esp32-mac](https://github.com/photon-circus/ph-esp32-mac) — bare-metal ESP32 Ethernet MAC support with LAN8720A, `smoltcp`, Embassy, and `esp-hal` integration.
- [ph-qmi8658-imu](https://github.com/photon-circus/ph-qmi8658-imu) — an async `no_std` driver for the QMI8658 six-axis IMU.

## How we work

- A repository owns one bounded responsibility and the invariants needed to make it truthful.
- Device behavior stays in drivers; board resources, scheduling, and application policy stay in integration.
- Determinism, memory use, code size, concurrency, and physical behavior are measured when claimed.
- Private development relies on authoritative local verification; released public software adds bounded contributor-facing CI.
- New organization-owned repositories and packages use the `ph-` prefix. Existing names remain stable.

Read the adopted [Photon Circus Repository Standards v0.1](https://github.com/photon-circus/.github/blob/main/REPOSITORY_STANDARDS.md) for lifecycle, naming, documentation, licensing, contribution, CI, branch, and release policy.

## Contributing

Public projects carry repository-specific contribution and security guidance. Bug reports with exact hardware, target, toolchain, configuration, and evidence are especially valuable.

MIT is the default license. Some projects use Apache-2.0 when upstream provenance or compatibility calls for it.
