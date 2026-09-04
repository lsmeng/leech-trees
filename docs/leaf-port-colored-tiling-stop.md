# Bounded leaf-port prefix stop and two-port successor (FW283)

FW282 reduces every non-singleton full-window sink to an exact leaf-port
colored tiling.  This note audits the strongest bounded-prefix consequences of
that state and records a **STRICT STOP for one specific mechanism**:

```text
one leaf-port cut + a bounded rooted prefix + successive owner gates.
```

The stop is not a counterexample to LPCT.  Complete Leech coefficient coverage
may still force a contradiction.  What fails is the proposed attempt to reach
that contradiction by keeping only one cut and extending its bounded prefix
one owner at a time.  The next live obligation must compare at least two sink
ports simultaneously.

## 1. Exact first-cross-hole table

Use the FW282 notation for a core-leaf edge of weight `p`:

```text
[0,N-p]=(U direct-sum V) dotunion H_S dotunion H_R,
eta=min(H_S union H_R)<=10.
```

Since `eta` is the first colored owner, `U+V` represents every offset below
`eta` exactly once and does not represent `eta`.  Rebuilding the rooted-parent
search from scratch gives the following complete necessary table, up to
swapping the two rooted factors:

```text
eta   U below eta          V below eta
 1    {0}                  {0}
 2    {0}                  {0,1}
 3    {0}                  {0,1,2}
 4    {0,1}                {0,2}
 5    {0,1,4}              {0,2}
 6    {0,1}                {0,2,4}
 7    impossible
 8    {0,1,4,5}            {0,2}
 9    {0,1,4,5,8}          {0,2}
10    {0,1,4,5}            {0,2,8}
```

The unfiltered survivor counts while forcing cross coefficients `1,...,10`
are

```text
2,4,2,4,6,2,2,4,2,0.
```

The separate thin-bouquet geometry fixes the orientation of the last three
rows.  For `eta=8,9`, the bouquet factor must be `{0,2}`.  For `eta=10`, it
must be `{0,2,8}` with the star parent map `root--2`, `root--8`; the chain
parent map is not thin.  The opposite factor `{0,1,4,5}` has its unique rooted
map `root--1--4`, `root--5`.

These are necessary prefix states.  They do not say how coefficients after
`eta` are owned.

## 2. The first colored owner path

Let `P_eta` be the actual within-side path of length `p+eta` owning the first
colored coefficient.  Every proper subpath of `P_eta` has length at most
`p-1`.  Indeed, a proper subpath strictly between `p` and `p+eta` would be an
earlier colored owner, while equality with `p` would repeat the core-edge
distance.

Consequently exactly one of the following holds.

1. `P_eta` is the single edge of weight `p+eta`.  No global edge weight lies
   strictly between `p` and `p+eta`, so this is the next edge weight after
   `p`.
2. `P_eta` has at least two edges.  Every edge on it is below `p`, and each of
   its two endpoint edges has weight at least `eta+1`: deleting an endpoint
   edge leaves a proper suffix of length at most `p-1`.

This is an actual-path dichotomy, not just a set-theoretic observation.  It
still gives no bound on the projection gate of `P_eta` relative to the cut
root.

## 3. Two exact controls

The known order-six Leech tree, cut at its central weight-five edge, has

```text
U={0,1,2},   V={0,4,8},   H_S=empty,   H_R={3,7},
```

and these classes tile `[0,10]` exactly.  This small control is outside the
`n>=18` two-nonempty-color conclusion, but it shows that a first cross hole
can be repaired by an actual same-side owner without destroying complete
capped coverage.

The order-six one-defect tree in FW282 has both colors, a non-singleton sink,
and spectrum `[1,15]-{9}+{21}`.  Its colored owners at offsets `4,5` are
followed by a gap at offset `6`, after which offsets `7,...,12` recover.  Thus
a first colored owner does not begin a monotone colored block.

## 4. An arbitrarily remote eta=10 owner

For every integer `t>=70`, let `T_t` have cut edge `uv` of weight `20`.  Attach
four singleton leaves to `u` with weights

```text
2, 8, t, t+26.
```

On the `v` side attach

```text
v --1-- a --3-- b,
v --5-- leaf,
v --(2t-18)-- r --30-- x.
```

The full-window sink core is the path

```text
u --20-- v --1-- a.
```

The vertex `u` is a core leaf and its side of the weight-20 cut is a bouquet
of four singleton strict thin caps.  At this cut,

```text
U below 10 = {0,2,8},
V below 10 = {0,1,4,5},
U+V         = {0,1,...,9,12,13}.
```

There is no within-side distance `21,...,29`; the edge `rx` owns distance
`30=p+10`.  Hence `eta=10`, but its gate has depth

```text
d(v,r)=2t-18,
```

which is unbounded.  The first colored owner is also the single next edge
after `p`, so the strongest branch of the path dichotomy does not localize it.

All 55 pair distances are distinct.  Writing each as an affine function of
`t`, their constants are

```text
A0 = {1,2,3,4,5,6,8,9,10,20,21,22,23,24,25,26,27,28,29,30,32,33},
A1 = {0,2,8,20,21,24,25,26,28,34,46,47,50,51},
A2 = {-18,-17,-14,-13,2,4,10,12,13,16,17,26,32,34,40},
A3 = {2,28,32,58},
```

in the four bands `A0`, `t+A1`, `2t+A2`, `3t+A3`.  At `t=70`, and therefore
for every larger `t`, the bands are strictly separated:

```text
33 < 70,
70+51 < 140-18,
140+40 < 210+2.
```

The family is deliberately not Leech: distance `7` and cut offset `11` are
missing, while its maximum distance is `3t+58`.  It is an actual-tree
countermodel only to the proposed inference that the bounded one-port state,
thinness, injectivity, full support, a unique sink and a next-edge first owner
force a bounded gate.

## 5. Precise strict stop

The bounded prefix fixes only `U below eta` and `V below eta`.  After the
first colored owner, the next coefficient may be supplied by a new root
depth, a new cross pair, or a same-side path behind a new projection gate.
Colors may switch and cross ownership may resume.  The controls above show
that neither a monotone owner block nor a bounded gate recursion follows from
the single-cut state.

Therefore continuing this mechanism would require recording each new owner
path and gate individually.  That recreates an unbounded owner/LCA ledger and
is not a finite successor to FW282.  The following route is now frozen:

> **STRICT STOP (FW283).**  Do not continue LPCT by extending one leaf-port
> bounded rooted prefix one coefficient at a time.  Reopening this subroute
> requires a new theorem that couples complete capped coverage to another
> actual sink port.

LPCT itself remains **UNVERIFIED**, not false.  FW283 excludes no order and
proves neither G18 nor global nonexistence.

## 6. Next live theorem: simultaneous two-port owner return

Let `e=vv'` be the leaf-core edge used by FW282, and choose a distinct
first-level sink port whose connector reaches the same bidirectional core.
The required successor must compare the exact pair-owner ledgers across both
cuts.  A useful theorem must show that complete caps at the two ports prevent
the first unforced owner from appearing behind a fresh unrelated projection
gate—by forcing either an owner return under the second cut, a repeated
distance, or a cross sum beyond the relevant cap.

This obligation must use all four pieces simultaneously:

1. no-outlier capped coverage at both cuts;
2. actual pair owners, not just coefficient counts;
3. the projections/LCA positions of their paths;
4. the common core connector between two distinct ports.

Merely saying that complete coverage should localize an owner restates LPCT
and is not a proof.  The new target is a bounded **two-port owner-return
invariant**, distinct from FW281 transformed convolution and from FW283's
stopped single-port ledger.

FW284 now supplies the exact successor.  It promotes an owner hidden inside
a first-level cap to that cap's strictly heavier boundary; otherwise it
returns the same actual pair across a named skeleton edge.  The resulting
fixed-point-free transition map must contain a lift/drop cycle.  The remaining
problem is NSSC endpoint monodromy, not another bounded first-prefix search.
See `docs/skeleton-first-owner-cycle.md`.

## 7. Replay and trust boundary

The clean-room replay is

```text
theory-lab/topwindow/verify_leaf_port_colored_tiling_stop.py
theory-lab/topwindow/results/leaf_port_colored_tiling_stop_certificate.json
```

It independently enumerates all rooted parent maps needed for the table,
checks the extremal bouquet orientations, replays the exact order-six Leech
cut, proves the affine separation of `T_t` for every integer `t>=70`, and
checks numerical instances at `t=70,71,100,1000`.  The critical-path lemma and
the mechanism stop are analytic arguments above.  The replay does not prove
LPCT or the proposed two-port invariant.
