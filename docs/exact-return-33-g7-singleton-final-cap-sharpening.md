# Order-25 singleton final-cap sharpening

This note records a theorem inside the FW303 singleton final-cap branch.  It
does not exclude that branch and does not imply global `b=27/J32` or Leech-tree
nonexistence.

## Hypotheses

Let `X` be an order-25 FW303 target.  Delete its globally heaviest edge of
weight `s`, and suppose the detached final cap is a singleton.  Let `K` be the
24-vertex component, rooted at the bridge endpoint `x`, and put

```text
F = Spec(K),       D = R_{K,x},
A = max D,         delta = max F = diam(K).
```

FW303.10 gives the disjoint exact partition

```text
F disjoint_union (s+D) = {1,...,300},
|F|=276, |D|=24, 0 in D.
```

All pair distances are distinct and all edge weights are positive integers.

## Elementary consequences

For every nonzero `d in D`, the pair from `x` to its vertex lies inside `K`,
so

```text
D minus {0} subset F,
s notin (D-D)^+.
```

The cap gives `s+A<=300`.  Every K-distance is at most `2A`, hence
`delta<=2A`.  Since F has 276 positive values, `delta>=276`; because `s<276`
and `s` is a missing value inside `[1,delta]`, in fact `delta>=277`.

The number of K-internal owners above the bridge is exactly

```text
|F intersect [s+1,300]| = 277-s.
```

## Exact parity equation

Let `E` and `O` be the numbers of even and odd elements of `D`.  For vertices
`u,v in K`, distance parity is the parity of
`d(x,u)+d(x,v)`, since the LCA term is even.  Thus K has exactly `EO` odd
pair distances.  The full interval `{1,...,300}` has 150 odd values.

If `s` is even, the cross set `s+D` has `O` odd values; if `s` is odd, it has
`E`.  Consequently

```text
s even: O(E+1)=150, so (E,O) is (14,10) or (9,15);
s odd:  E(O+1)=150, so (E,O) is (10,14) or (15,9).
```

## Top-block lemma

Assume `delta<300` and set `r=delta-276`.  Every integer above `delta` is
absent from F and therefore belongs to `s+D`.  Since exactly `r` cross values
lie in `[1,delta]`, the other `24-r=300-delta` cross values are precisely
`{delta+1,...,300}`.  It follows that

```text
A=300-s,
D = L disjoint_union {A-23+r,...,A},
|L|=r, 0 in L, L subset [0,A-24+r].
```

This is a coefficient identity; it does not assert any unproved LCA
projection.

For `delta=277`, the 23-term top block plus `0` has parity counts `(13,11)`
or `(12,12)`, incompatible with the exact parity equation.  For `delta=278`,
the 22-term block plus `0` and one low depth again gives only `(13,11)` or
`(12,12)`.  Hence both values are impossible.

## Singleton sharpening theorem

Every order-25 FW303 singleton-final-cap candidate satisfies

```text
delta >= 279,
A >= 140,
s <= 160,
277-s >= 117.
```

The last quantity is the exact number of K-internal pair owners above `s`.

If `delta=279`, then `r=3`.  The parity equation forces

```text
s even,
A=300-s,
D={0,d1,d2} disjoint_union {A-20,...,A},
d1,d2 even,
F={1,...,279} minus {s,s+d1,s+d2}.
```

Thus the first remaining diameter case is a three-hole spectrum with 21
consecutive deep root levels.

## Conditional frozen-packet corollary

The following tree-metric lemma is unconditional.  If a set of vertices has
rooted depths in an interval of width `W`, then every literal tree edge of
weight greater than `W` has at least one endpoint outside that set.  Hence a
matching of `q` such literal edges requires at least `q` distinct vertices
outside the interval.

A later `FW319 b=27/J32` finite-search interface freezes a 15-vertex packet
containing the pairwise disjoint literal edges of weights `22,27,32,34`, and
also a disjoint literal edge of weight `19`.  **Conditional on an independent
pre-cap packet-lift theorem** placing that full packet in the present
singleton branch, the lemma excludes `delta=279,280,281` and gives

```text
delta >= 282,
A >= 141,
s <= 159,
277-s >= 118.
```

No such pre-cap packet-lift is currently proved.  `FW303` itself fixes only
the connected six-vertex core with literal edge weights `1,2,6,7,10`.
Importing the later `R2,t=4`, `b=27`, or `J32` packet into this upstream
singleton branch would be circular.  Therefore the displayed strengthening
is `CONDITIONAL`, not part of the unconditional singleton theorem above.

## FW303-only core-gate reduction at `delta=279`

Let the genuine upstream core have literal edges

```text
z-b1=1, z-b2=2, c-d6=6, c-z=7, z-a=10.
```

The three low-depth vertices `{0,d1,d2}` form a connected rooted subtree.
The connected core has a unique rootward gate `g`; its six root depths are a
translate of the core-distance profile from `g`.  Writing
`q=A-d(x,g)`, the complete surviving classification is:

```text
all high (25 patterns):
  g=z:  q=13,...,20       g=b1: q=14,...,20
  g=b2: q=15,...,20       g=c:  q=17,...,20

mixed (13 patterns):
  g=b2: q=22
  g=c:  q in {22,24,26}
  g=a:  q in {24,26,28,30}
  g=d6: q in {24,26,28,30,32}.
```

There is no all-low placement, the root is not a core vertex, at most two
core vertices are low, and every mixed pattern satisfies `q<s`.  This is a
complete core-placement theorem, not an exclusion of the 38 patterns.

The core's complete internal spectrum is

```text
S_C={1,2,3,6,7,8,9,10,11,12,13,14,15,17,23}.
```

Global distance injectivity forbids every non-core edge from reusing a value
of `S_C`.  Hence every non-core edge whose endpoints both lie in the 21-term
high block has weight in

```text
{4,5,16,18,19,20}.
```

There are at most six such edges.  Counting the fixed high--high core edges
then shows that the high induced forest has at least ten components in every
all-high pattern, at least eleven in the mixed `b2`, `a`, and shallow `d6`
patterns, and at least twelve in the mixed `c` and two-low `d6` patterns.
Each component has exactly one attachment edge to the connected three-vertex
low subtree.

## High-component crowding reduction

Write `B=A-20=280-s`.  For every high component let its unique attachment
vertex have depth `B+y_i`, where `0<=y_i<=20`, and color it by its low parent.
If two such vertices have low-subtree LCA at depth `ell`, put

```text
rho=2*ell-B.
```

Their distance, the rooted high-depth exclusion, the diameter cap, and the
attachment-edge weight are respectively

```text
d(h_i,h_j)=B+y_i+y_j-rho,
y_i+y_j notin [rho,rho+20],
y_i+y_j <= rho+s-1,
a(rho,y_i)=(B-rho)/2+y_i < s.
```

Within each fixed-LCA class the sums `y_i+y_j` are all distinct, and all
attachment weights are globally distinct.  These are exact tree identities,
not a projection of arbitrary pair distances to rooted-depth differences.

For the low-`s` range `24<=s<=138`, no high component can attach directly to
the root: such an edge would have weight at least `B>s`.  The low subtree
cannot be a star, because then all at least ten component roots would have one
common non-root parent, producing at least `C(10,2)=45` distinct pair sums in
the 39-value range `{1,...,39}`.  Hence the only surviving low-`s` shape is

```text
x--u1--u2,
```

and in fact

```text
s even, 94<=s<=138,
c in {10,11,12},
c=10: (n1,n2) in {(1,9),(2,8),(3,7),(4,6),(5,5),(6,4)},
c=11: (n1,n2) in {(2,9),(3,8),(4,7)},
c=12: (n1,n2) in {(3,9),(4,8)}.
```

Here `n1,n2` count attachments to `u1,u2`.  The root `x` is a leaf, and
deleting it leaves the exact inherited rooted state

```text
R_{K-x,u1}={0,d2-d1} disjoint_union [B-d1,A-d1],
Spec(K-x)=[1,279]
  minus ({s,s+d1,s+d2,d1,d2} union [B,A]).
```

This state is not asserted to be a smaller Leech tree.

The remaining eleven low-`s` color-count rows admit a smaller exact finite
obstruction.  If `Y1,Y2` are the disjoint positions of component roots
attached to `u1,u2`, then all sums from

```text
C(Y1,2) union (Y1+Y2)
```

must be distinct because those root pairs have LCA `u1`; independently, all
sums from `C(Y2,2)` must be distinct because those pairs have LCA `u2`.
A deterministic enumeration of subsets of `{0,...,20}` returns zero for every
one of the eleven rows, and an independent checker re-enumerates all eleven
rows directly with the same result.  The checker was independently rerun by
the controller on the workstation.  Therefore

```text
94<=s<=138
```

is **CERTIFIED FINITE impossible**.  This enumeration is only the exact
colored component-root subsystem; it is not a weighted-tree enumeration.

For `s in {152,154,156,158,160}`, component-root capacity gives the star
upper bounds `11,12,12,12,13` and the chain upper bounds
`13,14,14,14,15`, in the same order.  In particular the `s=152` star
patterns with only three fixed high--high core edges, which require at least
twelve high components, are impossible.

If `f_C` is the number of high--high FW303 core edges, the number of non-core
high--high edges is exactly `21-c-f_C`.  Thus in the low-`s` chain the
`f_C=3` class has `c=12` and uses all six available weights
`{4,5,16,18,19,20}` exactly once.

## Trust boundary

The theorem and core-gate reduction do not show that the displayed
depth/spectrum data are realizable by a tree, nor that they are impossible.
The low-`s` adjusted-Sidon systems are now certified empty.  The five high-`s`
values remain, where root attachments may use all three low colors and the
root-LCA class has a value-dependent diameter cap.  The next load-bearing step
is:

> **S1-279-HIGH-S-FIVE-VALUE-ROOT-SIGNATURE.** Exclude or classify the
> three-color component-root signatures for
> `s in {152,154,156,158,160}`, for both low-tree shapes and every surviving
> FW303 component-count class, using the exact LCA table, diameter caps,
> attachment uniqueness, and within-class sum injectivity.

### First independently certified high-`s` shards

The finite chain shards

```text
s=152, chain, even 2<=d1<=36
```

are now **CERTIFIED FINITE impossible**.  For every even `2<=d1<=16`,
independent exact-10/full-21 scans are both empty.  For `d1=18`, independent scans agree
on the exhaustive 19 canonical root signatures; the proved 38-row FW303 gate
classification reduces those to four signature/row pairs, and two independent
complete 24-vertex forest searches return zero for every
`c in {10,11,12,13}`.  For `d1=20`, two exact scans agree on all 1353
canonical root signatures; independent 38-row reconstruction leaves the same
929 Class-A rows, and the two complete-tree implementations agree on all 3716
per-job counter records and return zero full spectra.  For `d1=22`, the two
exact scans agree on all 8711 signatures; independent row reconstruction leaves
6693 Class-A and six Class-B rows, and the two complete-tree implementations
agree on all 26790 per-job records and again return zero.  Exact scopes and hashes are in
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-16.md` and
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-18.md`, and
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-20.md`, and
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-22.md`.  For `d1=24`, the
two exact scans agree on all 10829 signatures; independent row reconstruction
leaves 8153 Class-A and 13 Class-B rows, and the two complete-tree
implementations agree on all 32651 per-job records and return zero.  Its exact
scope and hashes are in
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-24.md`.
For `d1=26`, the exact scans agree on the complete 19045-signature set but
emit it in different orders; independent row reconstruction leaves 13776
Class-A, ten Class-B, and two Class-C rows.  After keying jobs by canonical
signature content, the two complete-tree implementations agree on all 55138
per-job records and return zero.  Its exact scope, the preserved index-key
verifier failure, and the corrected certificate are in
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-26.md`.

For `d1=28`, the two exact searches agree on all 24220 canonical signatures
and on the new order-independent count of 26652 full-extension predicate
invocations.  Their raw recursive-node counts differ by 1649 because the two
implementations deliberately use different first-witness color orders and
short-circuit on success.  The failed counter certificate is preserved; an
order-only diagnostic replay and a v2 semantic verifier certify the exact
cause without hiding the difference.  Independent 38-row reconstruction
leaves 17410 Class-A, 34 Class-B, and one Class-C row on 11515 signatures.
The two complete-tree implementations agree on all 69744 canonical per-job
records and return zero full spectra.  Exact hashes and both the failed and
corrected certificates are in
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-28.md`.

For `d1=30`, the two exact searches agree on all 25952 canonical signatures
and on 28382 order-independent full-extension invocations.  Independent
38-row reconstruction leaves 19417 Class-A, 28 Class-B, and two Class-C rows
on 12684 signatures.  The two complete-tree implementations agree on all
77756 canonical per-job records and return zero full spectra.  Exact hashes
and certificates are in
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-30.md`.

For `d1=32`, the two exact searches agree on all 20921 canonical signatures
and 30714 order-independent full-extension invocations.  An order-only
diagnostic also explains the larger 17332334-node first-witness recursion
delta exactly.  Independent 38-row reconstruction leaves 14921 Class-A and
22 Class-B rows on 9816 signatures.  The complete-tree implementations agree
on all 59750 canonical per-job records and return zero full spectra.  Exact
hashes and certificates are in
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-32.md`.

For `d1=34`, the two exact searches agree on all 29538 canonical signatures
and 33715 order-independent full-extension invocations.  Their raw
first-witness recursion counters differ by 582091 and are retained as a
nonsemantic traversal-order diagnostic.  Independent reconstruction of all
38 rows leaves 20851 Class-A, 26 Class-B, and one Class-C row on 13757
signatures.  The 148 primary shards cover `[0,29538)` without gaps; the
independent C++ replay agrees on all 83484 canonical per-job records and all
seven counters.  Both implementations return zero full spectra.  Exact hashes
and certificates are in
`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-34.md`.

For `d1=36`, the two exact searches agree on all 18562 canonical signatures
and 21684 order-independent full-extension invocations. Independent 38-row
reconstruction leaves 12767 Class-A and 17 Class-B rows; the 93 primary shards
cover `[0,18562)` without gaps, and the independent C++ replay agrees on all
51119 canonical per-job records and all seven counters. Both implementations
return zero full spectra. Exact hashes and certificates are in
`docs/checkpoint-2026-09-01-s1-279-s152-chain-d1-36.md`.

This closes only the displayed `s=152`, chain, even `2<=d1<=36` shards.  It does
not close the `s=152` star case, chain `d1>=38`, the other four high values of
`s`, or S1-279 itself.

The full singleton branch, all other final-cap siblings, `R2-COVER`,
`T4-COVER`, and global nonexistence remain open.
