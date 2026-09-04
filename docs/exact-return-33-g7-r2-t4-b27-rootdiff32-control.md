# FW319 `b=27`: rooted-difference-32 local metric control

The remaining ancestor--descendant rooted-difference-32 branches cannot be
eliminated using only the fixed L factor, carrier/endpoint floors, rooted
directness, and global distance injectivity.  The following finite controls
are deliberately **not** Leech trees and identify the missing global inputs
precisely.

## Controls

Keep the exact `b=27` L factor and attach a carrier of weight `w=43`.  On the
J side use rooted depths

```text
d(u,y0)=16,  d(u,y3)=19,  d(u,p)=100,  d(u,q)=132,
```

where `q` is a child of `p` by an edge of weight 32.  Thus

```text
t=w+16=59,          d(p,q)=32=b+5.
```

The resulting 13-vertex weighted tree has all `binom(13,2)=78` pair
distances distinct.  It realizes the exact fixed L data and satisfies the
local floors `w>=38`, `r>=16`, and `t>=54`.

There is also an L-internal control: keep the same fixed L factor, take
`w=51`, `r=16`, and attach a new leaf `x` to `P1` by an edge of weight `32`.
The resulting 12-vertex tree has all 66 pair distances distinct, with the
unique 32-owner `(P1,x)`, `t=67`, and maximum distance `130>66`.

## Meaning

Both controls are **OBSERVED_CONTROL**, not counterexamples to Leech
nonexistence.  They fail the indispensable global hypotheses:

```text
first missing low values: 4,5,18,20,21,24,25,26,...
maximum distance: 203 > binom(13,2)=78.
```

Hence they cannot be used to extend a Leech tree.  Their legitimate
consequence is narrower: a proof eliminating either rooted-difference-32
branch must use the complete punctured low spectrum, the final no-outlier cap,
or a genuine least-remote descent—not merely the current local metric
constraints.

The separate endpoint-shape audit now proves that a multi-edge J
ancestor--descendant 32 owner is impossible; only a single J edge of weight
32 remains on that side.  The L rooted branch is not similarly reduced by
this observation.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_rootdiff32_control.py
```

The replay prints both controls with status `OBSERVED_CONTROL`; no global
existence or nonexistence conclusion follows.
