# Fork-root depth separation

This is a small **PROVED** local lemma recovered while auditing the
endpoint-strip route.  It is useful only when a diameter-leaf neighbour is
the already forced fork root (or when a specified endpoint translate is
known to be rooted at that vertex).  It does **not** prove endpoint-strip
descent in general.

Let `T` be an integer-weighted tree with all unordered vertex-pair distances
distinct.  Suppose that `u` is incident with pendant edges `uv_1` and
`uv_2` of weights `1` and `2`, respectively.  Write

```text
R_u = { d_T(u,z) : z in V(T) }.
```

Then `R_u` is injective as a vertex-depth profile and, after the forced
depths `0,1,2`, every pair of distinct depths differs by at least `3`:

```text
R_u cap {1,2,3} = {1,2},
|r-r'| >= 3
  for distinct r,r' in R_u \ {0,1,2}.
```

## Proof

For a vertex `z` different from `u,v_1,v_2`, the pendant-fork geometry gives

```text
d(z,v_1) = d(z,u)+1,
d(z,v_2) = d(z,u)+2.                              (1)
```

If two distinct vertices have the same `u`-depth, the two pairs with `u`
already repeat a distance.  Thus the depth profile is injective.  If
`d(u,z)-d(u,z')=1`, then by (1)

```text
d(z,v_1) = d(z',v_2),
```

which repeats a pair distance.  If `d(u,z)-d(u,z')=2`, then

```text
d(u,z) = d(z',v_2),
```

which again repeats a pair distance.  Finally a vertex at depth `3` would
give `d(u,z)=d(v_1,v_2)=3`.  All three possibilities are forbidden by global
distance injectivity.  `QED`

## Endpoint-strip consequence and boundary

In the prefix-defect endpoint strip, if `A'=u`, then

```text
alpha + R_A
```

contains `alpha, alpha+1, alpha+2`, omits `alpha+3`, and all of its later
members are mutually at least three apart.  The analogous conclusion holds
for `B'=u`.

This does not yet apply to a general endpoint neighbour `A'`: the path from
`A'` to a vertex can branch before reaching `u`, so its `A'`-depth is not a
uniform translate of its `u`-depth.  Nor does the spacing alone prevent
`dist(K0)` or the other endpoint translate from filling the omitted values.
Thus the first unresolved interface remains an actual LCA/ownership lemma
connecting an endpoint neighbour to the inherited fork.

This limitation already occurs in the smallest useful exact tree.  Take the
five-vertex path-with-fork

```text
v_1 --1-- u --4-- x --7-- z,
             |
             2
             v_2.
```

All ten pair distances are distinct:

```text
{1,2,3,4,5,6,7,11,12,13}.
```

The fork-root profile is `R_u={0,1,2,4,11}`, which has the proved
three-separation after `0,1,2`.  But the profile at the unrelated root is

```text
R_x={0,4,5,6,7}.
```

In particular it contains the full block `d(x,u),...,d(x,u)+3`.  This is a
literal countermodel to the tempting claim that the inherited fork makes an
arbitrary endpoint-neighbour profile three-separated.  It is not a
prefix-defect core; it only isolates the missing LCA hypothesis.

There is nevertheless one exact LCA localization which survives for every
non-fork root.  Let `x != u`, put `t=d_T(x,u)`, and let `C_x` be the component
containing `x` after deleting `u`.  For every positive integer
`h not-in R_u`,

```text
d_T(x,z)=t+h  implies  z in C_x.                 (2)
```

Indeed, if `z` were outside `C_x`, its `x--z` path would pass through `u`,
so `d_T(x,z)=t+d_T(u,z)` and (2)'s antecedent would put `h` in `R_u`.
The fork makes `3 not-in R_u`, so its first universal instance is

```text
d_T(x,z)=d_T(x,u)+3  implies  z in C_x.          (3)
```

For endpoint stripping, take `x=A'` (or `B'`).  Thus any actual `A`-cross
owner of `alpha+d(A',u)+3` must end on the endpoint-side component of the
`u` cut.  This is a genuine owner/LCA localization, but not a closure result:
the tiling permits that value to be owned internally or from the other
endpoint translate, and (3) does not exclude a vertex in `C_{A'}`.

Even if both endpoint translates contain their respective first localized
value, there is no automatic collision.  Suppose `A'` and `B'` lie in
different components of `T-u`, and witnesses `z_A in C_{A'}` and
`z_B in C_{B'}` satisfy

```text
d(A',z_A)=d(A',u)+3,
d(B',z_B)=d(B',u)+3.
```

Let `w_A` and `w_B` be the branch points of the two witness paths on
`[u,A']` and `[u,B']`, and put `s_X=d(u,w_X)`.  The two equations give

```text
d(u,z_A)=2s_A+3,
d(u,z_B)=2s_B+3.
```

Since the witnesses are distinct, fork-root three-separation only forces

```text
|s_A-s_B| >= 2.                                  (4)
```

It does not force a contradiction.  The seven-vertex tree

```text
v_1 --1-- u --10-- A' --13-- z_A
             |
             2
             v_2
             |
            30
             B' --33-- z_B
```

has all 21 pair distances distinct.  Here both localizations occur, with
`s_A=10` and `s_B=30`; (4) is satisfied.  Therefore a future proof must
make a *quantitative upper bound* on these two LCA gates from the endpoint
strip, or force the two values to have specified owners.  Mere simultaneous
existence of the two localized witnesses is insufficient.

One such bound is available in the geometrically separated case.  Assume the
same two witnesses exist and `A'` and `B'` are in different components of
`K0-u`.  Then the diameter has order

```text
A, A', ..., w_A, ..., u, ..., w_B, ..., B', B,
```

and the witness projections onto the diameter are exactly `w_A,w_B`.  Put

```text
t_A=d(u,A'),  t_B=d(u,B'),
s_A=d(u,w_A), s_B=d(u,w_B).
```

The local `+3` equations say that the off-diameter lengths are
`d(w_A,z_A)=s_A+3` and `d(w_B,z_B)=s_B+3`.  Applying the left and right
endpoint-strip collar inequalities gives the **PROVED conditional bounds**

```text
2s_A <= alpha+t_A-g-4,
2s_B <= beta+t_B-g-4.                            (5)
```

Because `d(A',B')=t_A+t_B` in this case, their sum and the witness cross
distance obey

```text
s_A+s_B <= (D-2g-8)/2,
d(z_A,z_B)=2(s_A+s_B)+6 <= D-2g-2.               (6)
```

The factor `1/2` in (5)--(6) is essential.  These are real quantitative
restrictions, but they do not close the case: the last bound is merely
stronger than the ordinary non-diameter ceiling and need not duplicate a
named pair distance.  To use it, one still needs either forced ownership of
both localized values or a separate lower bound on the two gate depths.

There is also a basic endpoint-depth separation that precedes any owner
classification.  Put

```text
p=d(A,u),  q=d(B,u).
```

The six pairs

```text
Au, Av_1, Av_2, Bu, Bv_1, Bv_2
```

have distances `p,p+1,p+2,q,q+1,q+2`, respectively.  Global injectivity gives

```text
|p-q| >= 3.                                      (7)
```

Indeed `q=p,p+1,p+2` would repeat one of `Au,Av_1,Av_2`, and the symmetric
possibilities are identical.  Hence, when `p+3<=C-1`, the next value after
the `A`-fork triple has this exact preliminary classification:

* if `q=p+3`, it is already uniquely owned by `Bu`;
* otherwise it is uniquely owned by either an internal pair, an `A`-cross
  pair, or a nontrivial `B`-cross pair.

The first bullet is important: the `+3` value is **not** automatically an
`A`-translate value even in the separated-diameter geometry.  The second
bullet is only a partition, not an elimination.  In particular, the fork
alone rules out internal pairs incident with `v_1` or `v_2` at that value,
but does not yet rule out an arbitrary internal pair or a branch-local
`B`-cross owner.  The missing implication is precisely a global owner
localization for this third value.

## Check

The proof is a direct identity check on the three explicitly named pairs;
it does not rely on a finite enumeration.  The relevant endpoint-strip
hypotheses are recorded in `prefix-defect-endpoint-strip.md`.

The concrete non-root countermodel is replayed by:

```bash
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_fork_root_countermodel.py
```
