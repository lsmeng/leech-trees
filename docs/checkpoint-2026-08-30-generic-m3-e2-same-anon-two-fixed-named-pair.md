# Checkpoint: generic `(m,e)=(3,2)` same-anon / two-fixed-named pilot

Date: 2026-08-30

## Scope

Frozen named pair is `(u,p)`, which occurs at fixed-vertex indices `(9,13)` in

```text
(d6,c,z,b1,b2,a,P0,P1,v34,u,v,y0,y3,p,q).
```

For each `x_i in {x0,x1,x2}`, the two literal new low edges are

```text
u--x_i, p--x_i.
```

Every ordered injective pair of values from

```text
H37_L={5,16,18,19,20,21,24,25,26,34,35,36,37}
```

is assigned to those two fixed edge slots.  Therefore the raw weighted-base
domain is exactly

```text
3 * P(13,2) = 3 * 156 = 468.
```

No incidence row is enumerated.

## Result

Pilot status:

```text
VERIFIED_GENERIC_M3_E2_SAME_ANON_TWO_FIXED_NAMED_PAIR_PILOT
```

Independent checker status:

```text
VERIFIED_INDEPENDENT_GENERIC_M3_E2_SAME_ANON_TWO_FIXED_NAMED_PAIR_PILOT
```

Exact counts:

- raw bases: `468`
- accepted: `33`
- rejected: `435`
- `edge_weight_duplicate`: `198`
- `pair_distance_duplicate`: `237`
- canonical weighted-base orbits under full `S3`: `11`
- orbit sum: `33`
- stabilizer histogram: `{2: 11}`
- orbit-size histogram: `{3: 11}`
- incidence rows enumerated: `0`

The independent checker reconstructed all 468 ranks without importing the pilot
or generic indexer and matched rejection reasons, canonical-key commitment,
orbit multiplicities, stabilizers, and incidence metadata exactly.

## Trust boundary

This closes only the complete S3-invariant endpoint subdomain with one shared
anonymous endpoint and the fixed named pair `(u,p)`.  It is not the complete
`(m,e)=(3,2)` domain, not a proof of compression for all `S_cover`, and does not
establish high-completion coverage or FW319/Leech-tree nonexistence.
