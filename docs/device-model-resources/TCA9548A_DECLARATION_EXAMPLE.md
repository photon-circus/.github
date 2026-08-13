# Minimal behavioral declaration example: TCA9548A

Status: **Non-normative illustrative example**

This example demonstrates the information density expected from a simple
model. It does not prescribe packaging, API shape, Rust structure, or tests.

The model is a deterministic CI predictor for the Texas Instruments TCA9548A
using SCPS207H, Rev. H, September 2024. Agreement establishes compatibility
with the declared digital interpretation only; it is not silicon, electrical,
timing, or driver qualification.

Inputs are ordered I2C events at a START/address/data/STOP abstraction,
injected power-on reset, and injected RESET assertion or release. Outputs are
transport ACK/NACK/data, explicit unsupported-input results, and committed
channel selection. The model remains unchanged between inputs. Elapsed duration
has no modeled consequence at this fidelity.

| Classification | Included behavior |
| --- | --- |
| Modeled | Strap-derived address matching; control-byte receipt; last-byte retention; STOP-committed selection; committed readback; empty, single, and multiple channel selection; POR; RESET; non-matching address NACK. |
| Abstracted | I2C events rather than SCL/SDA waveforms; transaction helpers as event sequences rather than another state machine. |
| Injected | POR and RESET. RESET pulse width is not timed; assertion takes effect when injected. |
| Excluded | Electrical switching, voltage translation, pull-ups, capacitance, propagation delay, board topology, downstream devices, bus ownership, retries, and routing. |
| Unsupported | 10-bit addressing, Hs-mode, SMBus address resolution, general-call decoding, wire-level failures, repeated START after an acknowledged control byte, and invalid event sequences. |

Source decisions are limited to behavior needed by the model: readback reflects
the last STOP-committed byte; an address-only write leaves selection unchanged;
repeated START does not invent write completion; and an unsupported event is a
model limitation rather than a fabricated device NACK.

The model is derived without production masks, codecs, helpers, or transaction
builders. Its repository chooses its packaging locally. A future conformance
consumer may depend on both driver and model without coupling their
implementations.
