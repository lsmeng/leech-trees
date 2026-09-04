# Exact-return `(3,3)` `g=7` first-activation countercontrol and last-cut stop (FW302)

FW301 leaves a connected pressure tree that forces fresh edges 19 and 26 and
then two weight-27 branches, both with next missing value 29.  FW302 tests the
proposed first-root-activation obstruction against that chain.  It is false.
The repair is to move from the first root activation to the globally last one.

## 1. Exact packing at any root activation

Immediately before an edge `e=xy` of weight `s` joins a floating component
`H` to a root-connected component `K`, put

```text
x in K,  y in H,
D=R_{K,x}={d_K(x,u):u in K},
R=R_{H,y}={d_H(y,v):v in H}.
```

The new actual pair distances are exactly

```text
s+(D+R).                                                (FW302.1)
```

In any distance-injective continuation the sum is direct:

```text
(D-D) intersect (R-R) = {0}.                            (FW302.2)
```

Indeed, a common nonzero difference gives two distinct pairs with the same
cross distance.  The new block must also be disjoint from the old spectrum.
In a Leech tree of order `n`, with `N=binom(n,2)`, it must satisfy

```text
s+max(D)+max(R) <= N.                                   (FW302.3)
```

If `H` is coloured `A`, the block (FW302.1) decomposes by actual owner as

```text
X^s R_{A,x}R_{H,y},
X^(s+alpha+10) Lambda R_{H,y},
X^(s+alpha+17) W R_{H,y},        alpha=d_A(a,x).         (FW302.4A)
```

For a `B`-activation it decomposes as

```text
X^s R_{B,x}R_{H,y},
X^(s+beta+10) U R_{H,y},
X^(s+beta+7) W R_{H,y},          beta=d_B(z,x).          (FW302.4B)
```

For a `C`-activation it decomposes as

```text
X^s R_{C,x}R_{H,y},
X^(s+gamma+7) Lambda R_{H,y},
X^(s+gamma+17) U R_{H,y},        gamma=d_C(c,x).         (FW302.4C)
```

These are exact necessary identities.  They are not an obstruction.

## 2. The explicit weight-29 countercontrol

Start with the FW301 connected order-ten component

```text
(0,1,1), (0,2,2), (6,7,4), (8,9,5), (3,4,6),
(0,3,7), (0,5,10), (6,8,16), (4,7,18),
```

then add

```text
(10,11,19), (12,13,26), (10,14,27).
```

The component orders are `10,3,2`, all current distances are distinct, and
29 is missing.  Colour the edge-26 component `C`.  The edge

```text
(9,12,29)                                               (FW302.5)
```

is a valid first activation into the rooted `C` component.  At its two
attachment vertices,

```text
D={0,5,21,25,43,49,56,57,58,66},
R={0,26}.
```

The sum is direct because `26` is not in `D-D`.  Its twenty new distances are

```text
29,34,50,54,55,60,72,76,78,80,
85,86,87,95,98,104,111,112,113,121.                    (FW302.6)
```

Every one was absent.  Their owner split is

```text
I_C : 29,34,50,54,55,60,72,76,78,80,98,104
BC  : 85,86,87,111,112,113
AC  : 95,121.                                           (FW302.7)
```

The largest is only `121<153=N_18`.  Before activation, at least 104
coefficients of `[29,153]` were available, while the activation uses twenty.  The other
FW301 weight-27 branch, the new isolated edge `(14,15,27)`, admits exactly the
same activation and owner block.  Thus first activation can be coherent,
direct, disjoint from the old spectrum, and below the global cap.

After (FW302.5), 30 is missing.  On both weight-27 branches, exhausting its
placements leaves only a fresh isolated edge 30; the next missing value then
jumps to 39.  No known monotone descent accompanies the activation.

## 3. Connected geometric pressure control

Starting from the first weight-27 branch and its activation (FW302.5), join
the remaining order-three component by

```text
(13,14,47).                                              (FW302.8)
```

This gives a connected order-15 weighted tree with all 105 pair distances
distinct, the same exact `(3,3,0)` return, and a nontrivial nine-vertex sink.
The rooted depth sets at edge 47 are

```text
D={0,26,55,60,76,80,98,104,111,112,113,121},
R={0,27,46};
```

all `12*3=36` cross sums are distinct.  This tree is not Leech: its first
missing value is 30 and its largest distance is `214>N_15=105`.  It proves
only that coherent parent/LCA realization does not by itself obstruct the
activation.  Full interval coverage and the no-outlier cap are indispensable.

## 4. Correct all-order reduction: the last activation

Suppose a complete Leech tree extends an FW301 coloured state.  List its
edges in increasing weight.  Let `e=xy` be the globally heaviest edge, of
weight `s`.  Deleting it leaves exactly two components `K,H`.  Since the
standing edges `q=10,r=7` share `z` and precede `e`, they and all three roots
`a,z,c` lie in one component, called `K`; `H` is rootless.  Consequently `e`
is exactly the final root activation and no future edge remains.

Writing `F_K,F_H` for the two internal distance polynomials gives the exact
full-range identity

```text
I_N = F_K + F_H + X^s R_{K,x}R_{H,y}.                   (FW302.9)
```

The product is direct, is disjoint from both internal spectra, and is
contained in `[s,N]`.  If `k=|K|` and `h=|H|`, it uses exactly `kh`
coefficients.  Hence

The elementary containment count first gives

```text
sigma := N+1-kh-s >= 0.
```

Equality would force the two rooted factors to directly tile the complete
cross interval and the internal spectra to tile `[1,s-1]`.  The independently
verified edge-cut equality rigidity theorem in `docs/heaviest-edge-rigidity.md`
excludes that case for every Leech tree of order at least five.  Hence in the
standing `n>=18` regime the strict conclusion is

```text
sigma := N+1-kh-s >= 1.                                 (FW302.10)
```

Unlike first activation, (FW302.9) has no residual component or future
connector that could repair a hole.  It automatically absorbs any finite
fresh-component cascade such as `19,26,27,29,30,...`.

## 5. The exact remaining lemma

> **COLOURED LAST-ACTIVATION NO-GRAZING LEMMA.**  Under (FW302.9), with `K`
> containing the exact FW301 `q/r` owner structure, prove at least one of:
>
> 1. `(R_{K,x}-R_{K,x})` and `(R_{H,y}-R_{H,y})` share a nonzero value, so
>    the cross sum is not direct;
> 2. `s+max R_{K,x}+max R_{H,y}>N`, so there is an outlier;
> 3. one proper side carries a well-founded, strictly smaller inherited
>    exact-return state.

For non-singleton `H`, every edge weight in `H` belongs to its rooted-depth
difference set.  A sharp subproblem is therefore to force one of those same
differences in `R_{K,x}-R_{K,x}` from reflected top support and the standing
`q/r` geometry.  Singleton `H` has trivial difference set and must be handled
by the outlier/descent clause.  Zero slack is already excluded by edge-cut
equality rigidity.

No present theorem proves this trichotomy.

## 6. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_g7_last_activation_stop.py
theory-lab/topwindow/results/exact_return_33_g7_last_activation_stop_certificate.json
```

**Proved analytically:** the exact activation sum, directness criterion,
owner decompositions, cap condition, last-edge/final-activation reduction,
full-range identity (FW302.9), and the strict positive capacity slack after
invoking the independently verified edge-cut equality rigidity theorem.

**Exact finite pressure evidence:** both weight-27 branches admit the
weight-29 `C` activation; its twenty owner coefficients; forced fresh edge 30;
and the connected order-15 edge-47 control.

**Not proved:** the last-activation no-grazing lemma, a strict descent,
exclusion of `g=7`, ERTC, NSSC, or global Leech-tree nonexistence.

**Verdict: FALSE FIRST-ACTIVATION OBSTRUCTION + EXACT LAST-CUT STRICT STOP.**
