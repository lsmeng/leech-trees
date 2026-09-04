# Exact-return `(3,3)` pre-target internal-gap stop (FW296)

FW295 proves that the exact local strip and a nontrivial sink do not exclude
`(delta,eta)=(3,3),ell=0`.  FW296 adds the first global numerical bound,
`g>=7`, and stronger controls that already cover the complete low spectrum
through seven.  The remaining target is an internal gap somewhere before the
edge weight `g`.

This is a **PROVED TARGET-WEIGHT BOUND plus a VERIFIED SHARPENED MECHANISM
STOP**.  The proposed pre-target gap lemma remains unverified.

## 1. The forced internal owner at six

The common-root shallow factor is the unique injective star

```text
z--b_1=1,   z--b_2=2,   d(b_1,b_2)=3.
```

At the `r` cut the exact-return coefficients are

```text
[X^j](Rho*W)=1,1,1,0,0,0,1,   j=0,...,6.
```

Because neither factor has rooted depth `3,4,5`, the return at six is exactly
one root-to-depth-six pair in `B` or `C`.  Thus global distance six already
has an internal owner.

If `g` were `1,2,3`, the target edge itself would repeat one of the three
known `B` distances.  If `g=4` or `5`, the `BC` prefix at global distances
`g,g+1,g+2` would already include another owner of distance six.  If `g=6`,
the target edge would repeat the internal return owner.  Therefore

```text
g>=7,   p=g+3>=10.                                  (FW296.1)
```

Every global distance below `g` is consequently internal to one of the
disjoint parts `A,B,C`; a pair crossing `r` has distance at least `g`, and a
pair crossing `q` has distance at least `p`.

## 2. Completing four and five is still insufficient

Distance four must be a single edge: a multi-edge path of total four would
use another edge of weight one, two, or three, but the unique weights one and
two are already the two star edges and there is no weight-three edge.

Distance five is either a single edge or the path formed by the weight-one
and weight-four edges.  The path alternative would attach the weight-four
edge to `z--b_1` and create forbidden `B` rooted depth four or five.  Hence a
complete extension contains distinct edges of weights four and five.

These deductions do not give a contradiction.  Put the weight-four edge
after `z--b_2=2`, and the weight-five edge after it:

```text
z--b_2 : 2,
b_2--u : 4,
u--v   : 5.                                        (FW296.2)
```

The resulting `B` subtree owns all distances `1,...,7` and also `9,11,12`;
the root-to-`u` path is the exact return of length six.

## 3. Strong pressure controls

For `g=13,14,15`, add the source and target leaves

```text
z--a : p=g+3,
z--c : g
```

to the tree (FW296.2) and the edge `z--b_1=1`.  All 21 pair distances are
distinct, the sink is the three-vertex path `{z,b_2,u}`, and FW291 reconstructs
the exact `(3,3),ell=0` return cycle.  Each control covers the complete global
prefix `1,...,7`; its first gap is eight.

A topologically independent order-eleven control has edges

```text
z--b_1=1, z--b_2=2, z--a=13,
a--x=27, x--y=4, a--u=48, u--v=5,
z--c=10, c--d=6, c--e=24.                          (FW296.3)
```

It has 55 distinct distances, sink `{a,z,c}`, the same exact return state,
and complete global prefix `1,...,6`.  It first misses `7,8,9`.

Thus neither completion of distances four and five nor complete coverage
through the return value six closes `(3,3)`.  Even complete coverage through
seven coexists with the full local mechanism.

## 4. Strict stop and precise successor

> **STRICT STOP (FW296).**  Do not attack `(3,3)` using only a fixed bounded
> list of owners through the return, even when the list is combined with
> distance injectivity and a nontrivial sink.  Actual controls cover farther
> than that information and still survive.

The smallest remaining global obligation is the **Pre-Target Internal-Gap
Lemma**:

> In a globally distance-injective exact-return state with
> `(delta,eta)=(3,3)`, `ell=0`, and a nontrivial full-window sink, the three
> parts `A,B,C` cannot internally own every distance `1,...,g-1`.

Equivalently, some pre-target value must be absent.  This is **UNVERIFIED**,
strictly weaker than ERTC, and directly falsifiable.  A complete Leech
spectrum would contradict it automatically because (FW296.1) puts the whole
interval below both cut weights.

## 5. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_pretarget_gap_stop.py
theory-lab/topwindow/results/exact_return_33_pretarget_gap_stop_certificate.json
```

It checks all pair distances independently and replays the FW291 transition,
owner, convolution, connector, and sink audit on the four stronger controls.

**Proved:** the internal return owner at six, `g>=7`, and internal ownership
of every value below `g` in a complete extension.

**Verified pressure evidence:** three order-seven controls covering
`[1,7]` and one order-eleven control covering `[1,6]`.

**Not proved:** the Pre-Target Internal-Gap Lemma, exclusion of `(3,3)`, any
other FW294 row, ERTC, NSSC, G18, an order exclusion, or global nonexistence.

**Verdict: PROOF + SHARPENED STRICT STOP.**
