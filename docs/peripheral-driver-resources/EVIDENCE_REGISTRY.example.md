# Device evidence registry example

Status: **Non-normative representation example with synthetic propositions**

This example demonstrates linkable stable propositions without defining a file
name, identifier spelling, field vocabulary, or machine-readable schema. Replace
or remove every placeholder when adapting it, including `EXAMPLE-*` values,
dates, locators, and digest text. Do not copy propositions that lack a current
consumer.

States report evidence, not approval or future work. `Undefined` is not an
unchecked task and does not assign validation to anyone.

## Source baseline

For a small repository this inline entry can be the canonical source record. If
a separate source catalog exists, replace this metadata with a link to its
stable source ID; do not maintain both copies.

- `EXAMPLE-DS-R1`: Example Semiconductor, EX1234 datasheet, revision 1.0,
  retrieved `YYYY-MM-DD`, SHA-256
  `REPLACE_WITH_64_LOWERCASE_HEX_DIGITS`.

### S-01

**Kind:** documentary. **State:** supported.

**Proposition:** The pinned `EXAMPLE-DS-R1` source states that the output word
is 16 bits.

**Evidence:** Relation: supports. Affirmative documentary observation:
`EXAMPLE-DS-R1`, page `REPLACE_WITH_PAGE`, table `REPLACE_WITH_TABLE`.

### S-02

**Kind:** documentary. **State:** supported.

**Proposition:** Within `EXAMPLE-DS-R1` sections
`REPLACE_WITH_SEARCH_SCOPE`, no statement was located that specifies whether a
read of status register `EXAMPLE-STATUS` clears flag `EXAMPLE-FLAG`.

**Evidence:** Relation: supports. Located-negative documentary review of the
named source and search scope found no clearing statement. This proposition says
only that the scoped search found silence.

### S-03

**Kind:** device. **State:** undefined.

**Proposition:** Reading status register `EXAMPLE-STATUS` leaves
`EXAMPLE-FLAG` unchanged on scoped EX1234 silicon.

**Evidence:** Relation: does not resolve. [S-02](#s-02) establishes documentary
silence, not device behavior. Physical evidence: none.

**Relevance:** Current only if a driver guarantee, model behavior, conformance
expectation, physical observation, or reported bug cites this proposition. This
field may change without changing the proposition.

### S-04

**Kind:** device. **State:** supported.

**Scope:** The identified EX1234 samples and recorded power-on conditions.

**Proposition:** After the recorded power-on procedure, flag `EXAMPLE-FLAG`
reads zero on the identified EX1234 samples.

**Evidence:** Relation: supports. Affirmative physical observation:
`EXAMPLE-ARTIFACT`, identifying sample and silicon revisions, reset history,
voltage, temperature, fixture, tools, software commit, procedure, raw
observations, and digest. The evidence does not establish behavior outside that
scope.

### S-05

**Kind:** registry tombstone. **Disposition:** superseded.

**Former proposition:** The pinned source does not specify status-read clearing,
and reading status leaves `EXAMPLE-FLAG` unchanged on EX1234 silicon.

This compound referent was split into [S-02](#s-02) and [S-03](#s-03). It
remains resolvable and must never be reused.

## Downstream citation examples

These are component consequences, not registry prose:

- Driver: `read_threshold_status` makes no clearing guarantee ([S-03](#s-03)).
- Model: status-read clearing is unsupported ([S-03](#s-03)).
- Conformance: no successful clearing behavior is claimed ([S-03](#s-03)).

The downstream surfaces do not copy the proposition, source passage, source
coordinates, or physical observation.
