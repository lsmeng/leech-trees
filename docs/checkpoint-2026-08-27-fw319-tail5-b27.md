# Exact-return-33 FW319 Tail-5 checkpoint (`b=27`)

Date: 2026-08-27; local frontier update: 2026-08-28

This checkpoint records the current Luna-controlled frontier.  It is a
proof-state record, not a global nonexistence claim.

## Committed upstream refinements

The preceding FW315--FW319 reductions were independently replayed and
committed in `82227d0` (`Record FW315-FW319 exact-return refinements`).  The
chain is:

```text
FW315 reflected-owner pressure
FW316 six-distance rectangle classification
FW317 coreward-incidence reduction
FW318 fixed-core attachment-cell classification
FW319 five-block reception window
```

Each verifier and its certificate returns `PASS`.  These are finite or
conditional reductions with the trust boundaries recorded in their own
documents; they do not close the b=27 Tail-5 branch below.

## Verified chain

For the FW319 pre-`z` reverse cell at `b=27`, the replayed chain is:

```text
w >= 38,
r >= 16,
t=w+r >= 54,
32,34,35,36,37 are internal to L or J.
```

The fixed-L factor has spectrum

```text
{1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
 27,28,29,30,31,33,39,40,41,42,50,55}.
```

The L-positive-arm overlap alternative for the 32-owner is closed by the
finite multi-edge audit.  The L ancestor--descendant alternative is further
shape-reduced: with endpoint edges at least 6, only a single new edge 32
attached at `P0` or `P1` survives the induced-distance audit.  The remaining
cases are:

1. an L single new edge of weight 32 attached at `P0` or `P1`; or
2. a J ancestor--descendant owner, which is a single J edge of weight 32.

## New local evidence

The J path-composition catalogue is exhaustive for paths of lengths
`32,34,35,36,37` whose intervals avoid the fixed-L spectrum and reserved
value `4`:

```text
32: (32)
34: (34), (16,18), (18,16)
35: (35), (16,19), (19,16)
36: (36), (16,20), (20,16)
37: (37), (5,32), (32,5), (16,21), (21,16), (18,19), (19,18).
```

The J-branch control has fixed L, `w=56`, named J depths `16,19`, a J edge
`32`, and an L leaf `34` at `b_2`.  It realizes unique internal owners

```text
32=(p,q), 34=(b_2,v), 35=(y_0,y_3), 36=(z,v), 37=(b_1,v)
```

with all `91` local pair distances distinct.  Its maximum is `198`, above
the order-14 cap `91`, so this is `OBSERVED_CONTROL` only.

The symmetric L-branch control has `w=98`, named J depths `34,37`, an L
ancestor edge `32` at `P_0`, and additional L edges `35,36`.  It realizes

```text
32=(P_0,x), 34=(u,y_0), 35=(x,v), 36=(P_0,v'), 37=(u,y_3)
```

with all `91` local pair distances distinct and maximum `229>91`.  It is
also `OBSERVED_CONTROL` only.

An additional J-branch control uses a branched endpoint pair with
`w=45`, `r=54`, `r+3=57`, and a single J edge `32` below parent depth `86`.
Together with an L leaf owning `34`, it realizes actual owners for all five
values `32,34,35,36,37`.  Its 15-vertex induced tree has 105 distinct pair
distances and maximum `212`, which is below the order-25 cap
`binom(25,2)=300`.  This is an `OBSERVED_CONTROL`: it shows that the global
order-25 cap alone does not eliminate the J branch, while making no claim
about completion to the full spectrum.

The L-ancestor control also lies below the order-25 cap: its maximum is
`229`, giving margin `71` below `binom(25,2)=300`.  Thus both residual
branches have explicit local controls compatible with the first open-order
cap; the cap cannot be used alone as the missing exclusion.

The finite L path-shape audit now verifies that the first residual case has no
longer-chain form: the only surviving induced-distance-injective shapes are a
single new edge `32` attached at `P0` or `P1`, each with local maximum `87`.
Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_rootdiff32_shape.py
```

Conditioned on either direct L shape, the enlarged-L joint cross-translate
audit (including `u,y0,y3`) further gives `t>=77` for attachment at `P0` and
`t>=67` for attachment at `P1`; every admissible `(w,r)` pair below the
respective finite threshold collides with an induced L distance or a
cross-cross pair.  Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_direct32_cross_floor.py
```

Without assuming the extra L edge, the complete fixed-L spectrum gives one
additional necessary filter for the J branch.  The three translates from
`u,y0,y3` allow only

```text
t in {54,59,61,62,63,64} union [67,infinity).
```

The verifier exhausts `54<=t<=66` and proves the upper-tail statement from
`max(S0)=55` and `max((B0-B0)_+)=28`; it does not claim that any upper-tail
row extends to a full J tree.  Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_three_translate_floor.py
```

For the unresolved J single-edge-32 branch, root J at `u` and let `h` be
the global `d6`-depth of the shallower endpoint of the 32 edge.  Including
both edge endpoints in the same fixed-L translate test gives
`h>=t+19` for each of the six isolated rows.  This is a placement floor only;
the edge may still lie farther out and its J-side LCA geometry is not fixed.
Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_edge32_depth_floor.py
```

The fixed-L rooted-depth difference set gives one further owner-color
reduction.  Every J edge weight must avoid

```text
{1,2,4,5,6,7,8,9,10,12,13,14,15,17,21,22,23,27,28},
```

and every interval on a J path must avoid the fixed-L spectrum and the
punctured value `4`.  Exhaustive ordered path compositions show that neither
`5` nor `21` has an admissible J realization.  They are both below `w>=38`,
so in a complete spectrum their owners are forced into L.  This is an owner
location reduction only; the L owners and their LCAs remain unknown.
Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_forced_l_values.py
```

The two forced L owners admit one further finite shape reduction.  Because
every edge and contiguous subpath is an actual pair distance, the fixed-L
spectrum and punctured value `4` leave only

```text
5:  (5)
21: (21), (5,16), (16,5).
```

Thus the 5-owner is a single 5-edge, and a two-edge 21-owner must reuse that
same edge and add a 16-edge.  This still does not locate either attachment or
LCA, and it does not exclude the J single-edge-32 branch.  Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_forced_5_21_shapes.py
```

The advisor-guided fixed-cell check adds one location reduction: attaching
the forced single 5-edge directly to any of the eight named fixed-core
vertices produces a duplicate distance.  Therefore its attachment is outside
those eight cells; this is not a claim that the remote attachment is
impossible.  Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l5_fixed_attachment.py
```

A separate bounded pressure control was replayed for the sharp `t=54` cell.
The fixed core was augmented by the marked J-side 32-edge, a symmetric pair
of candidate remote J arms, and the final cap edge.  The check enforced
distinct edge weights, complete pair-distance injectivity on the displayed
tree, the root-shift-4 prohibition, the least-remote test on the displayed
J values, and direct carrier-sum injectivity.  The exhaustive bounded scan
returned `NONE`:

```bash
.venv/bin/python theory-lab/scratch_b27_j32_remote_control.py
```

This is `OBSERVED_CONTROL` only: it covers one sharp cell and a restricted
marked topology/parameter range.  It neither excludes the J single-edge-32
branch globally nor locates the remote L attachment of the forced 5-edge.

A complementary one-stem L-side scan records the first surviving stem
weights when the 5-edge is attached beyond the fixed core, still imposing
distinct edge weights, induced pair-distance injectivity, and the strict
order-25 cap.  For stems `H<=300`, the first survivors are

```text
P1:  H=51 (maximum 121)
b2:  H=54 (maximum 101)
v34: H=20 (maximum 101)
```

All other named core bases have no survivor in this bounded model.  Replay:

```bash
.venv/bin/python theory-lab/topwindow/scratch_b27_l5_one_stem_floor.py
```

This is another `OBSERVED_CONTROL`, not a theorem: it omits the J branch,
the L 32-edge, the 21-owner, complete cross-distances, root-shift-4, and
least-remote minimality.

The isolated-row J32 reduction gives a sharper row-conditioned lemma.  After
requiring the two J root distances `r` and `r+3` to avoid the fixed-L
spectrum, the actual rows below `t=67` are exactly

```text
(t,w,r) = (54,38,16), (59,43,16), (61,45,16),
          (62,46,16), (63,47,16), (64,48,16).
```

The relaxed `(64,38,26)` row is removed because `r+3=29` is already in the
fixed-L spectrum.  Independently enumerating all ordered edge compositions
of the remaining J path of total `16`, while forbidding the fixed-L spectrum,
the punctured value `4`, and the fixed-root depth-difference set, leaves only
the one-edge composition `(16)`.  Since edge weights are globally distinct,
the L owner shapes `(5,16)` and `(16,5)` are therefore unavailable on these
six rows; the L owner of `21` is forced to the single edge `(21)`.

Replay:

```bash
.venv/bin/python theory-lab/scratch_pro_b27_isolated_j32_21_reduction.py
```

This is `VERIFIED` only after conditioning on the six isolated J32 rows and
the existing fixed-L/J path model.  It does not remove those rows, address
the `t>=67` tail, or locate the remote attachment/LCA of the L 5-edge.

Two additional Pro-generated pressure controls were independently replayed.
For a fixed `t=59`, `w=43`, `r=16` final-cap control, scanning one-stem
attachments of either a 5-edge or a 21-edge to each of the eight named gates
returned no individual candidate and hence no combined candidate:

```bash
.venv/bin/python theory-lab/scratch_pro_b27_j32_remote521_finalcap_only.py
# individual 0 0
# NONE
```

A second displayed control with a remote L `(5,21)` tail and a J single-edge
32 was subjected to root-shift-4 and distinct-distance checks while trying to
place the owner 34.  It returned zero states at the first added owner:

```bash
.venv/bin/python theory-lab/scratch_pro_b27_j32_remote521_root4_cap.py
# after 34 states 0
```

Both are `OBSERVED_CONTROL` only.  They use one fixed J geometry and bounded
gate/stem ranges, omit complete spectrum reception, and do not exclude the
residual branch globally.

The least-remote pressure search was then run remotely on `geo-ws-vpn` as a
single `nice 19` process.  Its first deterministic sample already produced a
displayed control with remote J arms `(4617,4269)`, least remote pair
`8886`, final bridge `s=8884`, 24 vertices before the cap, and 26 after it.
The maximum displayed distance is `13640`, below the ambient order-166 cap
`13695`; owners `5,21,32,34,35,36,37` are all present and the b1-root depth
set has no difference four.  An independent fixed-edge checker reproduces
all 325 pair distances and the least-remote condition:

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_full_low_least_remote_control.py
```

The generator and replay are both preserved in the repository.  This is a
stronger `OBSERVED_CONTROL`, not a nonexistence result: it omits the complete
punctured spectrum and the isolated `t`-row constraints, so it actually shows
that cap/least-remote/root-shift conditions alone do not eliminate the local
geometry.

The first Hoffman2 attempt for the Pro-generated L32 random route was not a
mathematical run: job `98649` used node-local `/tmp` and exited before finding
the script; after moving the script to shared home, job `98650` correctly
started but failed its base assertion.  An independent base diagnostic finds
four pre-existing distance collisions, at values `65,66,67,76`:

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_l32_remote521_base.py
```

This route is therefore marked `MODEL_INVALID`; no `NONE`, `FOUND`, or
nonexistence conclusion is inferred from jobs `98649` or `98650`.

The right-side Pro consultant's Tail-5 root-provenance proposal was audited
independently.  Its endpoint-trim arithmetic and the empty deep-two-arm
boundary at `b=27` (also `b=28`) are valid.  The proposed four-way split is
not exhaustive as written because it omits the L-positive-arm overlap class;
that class is now independently closed, and the L ancestor shape audit then
reduces the current non-cross residual exactly to the two single-edge shapes
listed above.  The cross-owner packet is bookkeeping, not an exclusion.  The
response used the weaker pre-b27 bound `t>=24`; its `t=21` discussion is
superseded by the current `w>=38,r>=16,t>=54` chain.  No new global exclusion
was promoted.
Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_consultant_root_provenance_audit.py
```

## Earliest unclosed implication

The local fixed factor, carrier/endpoint floors, path-shape catalogue, and
complete ownership of `34,...,37` do not yet exclude either remaining case.
The missing theorem must use the complete exact-return spectrum, the final
no-outlier cap, least-remote minimality, or a strict inherited descent.

## Replays

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_prez_b27_carrier_floor.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_endpoint_depth_floor.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_low_owner_separation.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_tail5_owner_funnel.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_tail5_no_simple_fork.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_tail5_multiedge_overlap.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_rootdiff32_endpoint_floor.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_rootdiff32_shape.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_low_path_compositions.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_rootdiff32_full_low_control.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_rootdiff32_full_low_control.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_n25_cap_control.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_consultant_root_provenance_audit.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_forced_5_21_shapes.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_rootdiff32_shape.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_direct32_cross_floor.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_residual_two_branch.py
```

All nineteen listed checks pass.  The two cap controls are intentionally labelled
`OBSERVED_CONTROL`, the consultant check is labelled `VERIFIED_AUDIT`, and
the final command is the bundled `VERIFIED_FRONTIER` replay.

## Trust boundary

No full Leech tree has been constructed or excluded.  No claim is made for
other `b` values, the other FW319 cells, or the global conjecture.
