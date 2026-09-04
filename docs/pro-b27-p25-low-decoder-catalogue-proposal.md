# Proposed remote task: `P25 Low-Decoder Catalogue`

Date: 2026-08-29

This is a task specification, not a proof result.  Its purpose is to address
the first uncovered quantifier in the `b=27` FW319 branch: whether every real
low-forest/port-incidence state is represented by a canonical finite state.

## Finite state domain

Keep the literal fixed core

```text
d6-c=6, c-z=7, z-b1=1, z-b2=2, z-a=10,
d6-P0=27, c-P1=22.
```

For each `m=0,...,10`, enumerate every acyclic low-edge forest on at most `m`
new vertices.  New edge weights come from

```text
H37 = {5,16,18,19,20,21,24,25,26,32,34,35,36,37}.
```

The state must retain each component's literal weighted edge list, its unique
rootward port, every allowed outward incidence vertex, the component
partition, and the low pair-owner map.  The forced `5` and `21` shapes are
enforced; `34--37` owners are not preassigned and are recorded only when
realized by an actual low pair.  The current J32 state records 32 as
non-L-owned.

## Required checks and output

Each canonical row must include a fixed-core hash, component records,
rootward/outward port data, all low distances, owner status for `H37`, a
pair-table hash, and a canonical state hash.  An aggregate must include raw
and canonical counts by `m`, component count, `21` shape, and `34--37` owner
mask, plus the semantic input hash.

An independent implementation must reproduce the literal forest, acyclicity,
unique rootward port, all low distances, puncture `4`, fixed-owner reuse,
`H37` uniqueness, the `5/21` shape rule, canonical hashes, and the exact
raw-to-canonical key set (not merely equal totals).

## Acceptance and boundary

The run is accepted only if all `m=0,...,10` partitions finish with replayable
non-empty output, or if a concrete encoding counterexample is reported.  A
partial or timed-out partition is `PARTIAL`, never coverage.  A successful
run would close only low-catalogue surjectivity/port-complete low-forest
coverage.  It would not close high-quotient completion, `34--37` J geometry,
the `t>=86` tail, inherited descent, or global nonexistence.

Status: `PROPOSED_REMOTE_TASK`; no computation has been started from this
specification.
