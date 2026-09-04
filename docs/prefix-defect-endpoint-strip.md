# Endpoint stripping for a prefix-defect-one tree

This note records an **OBSERVED** structural theorem for the only new core
left by the large-rank singleton-corridor reduction.  It is an analytic
reduction, not yet the all-order contradiction.

Let `K` be an integer-weighted distinct-distance tree of order `i`, put

```text
C=binom(i,2),
dist(K)={1,...,C-1,D},
D=C+g.
```

The corridor application has `g>=21` and has a vertex `u` incident with the
weight-1 and weight-2 edges.

## The endpoint-strip theorem

Let `A,B` be the unique pair at distance `D`, let `A',B'` be their neighbours,
and let the two pendant weights be

```text
alpha=d(A,A'),  beta=d(B,B').
```

Then:

1. `A` and `B` are leaves and

   ```text
   alpha>=g+1,  beta>=g+1.                         (1)
   ```

2. The inner tree `K0=K-{A,B}` contains every distance `1,...,g`.  If
   `g>=2` and the weight-1 and weight-2 edges meet at `u`, all three vertices
   of that rooted `1--2` fork belong to `K0`.

3. Writing

   ```text
   R_A={d_K0(A',z): z in V(K0)},
   R_B={d_K0(B',z): z in V(K0)},
   ```

   the following is an exact disjoint partition:

   ```text
   {1,...,C-1}
      = dist(K0) disjoint_union (alpha+R_A) disjoint_union (beta+R_B),   (2)
   D=alpha+d_K0(A',B')+beta.                                            (3)
   ```

4. Deleting just `A` leaves a distinct-distance tree whose least missing
   positive distance is exactly `alpha`; the analogous statement holds for
   `B` and `beta`.  Thus both diameter leaves are forced leaf extensions of
   proper trees having prefix lengths at least `g`.

5. There is an empty metric strip at both ends of the diameter.  For any
   `z in K0`, let `c` be its projection to the `A--B` path and put

   ```text
   s=d(A,c),  t=d(c,z).
   ```

   Then

   ```text
   g+1+t <= s <= D-g-1-t.                         (4)
   ```

6. The inner tree has the sharp collar diameter cap

   ```text
   diam(K0) <= D-2g-2 = C-g-2.                    (5)
   ```

   Consequently the entire high ordinary tail

   ```text
   {C-g-1,...,C-1}
   ```

   is supplied by the two endpoint translates in (2), never by an inner
   pair.

7. Let `P=[A',B']` be the diameter backbone inside `K0`, and put

   ```text
   H={C-g-1,...,C-1},  |H|=g+1.
   ```

   The `A`-translate restricted to `P` and the `B`-translate restricted to
   `P` each supply at most `ceil((g+1)/4)` values of `H`.  Hence at least

   ```text
   g+1-2 ceil((g+1)/4)                              (6)
   ```

   high-tail values have an endpoint in `V(K0)\P`.  Since one off-backbone
   vertex can supply at most one `A`-cross and one `B`-cross value, at least

   ```text
   floor((g+1)/4)                                  (7)
   ```

   distinct off-backbone vertices occur in high-tail owner pairs.

8. In the separated geometry `u in P`, consider distinct off-backbone
   vertices other than the two fork leaves which each own two high-tail
   values.  On either fixed side of `u`, their tail indices are three
   separated.  More precisely, on the `B` side write

   ```text
   d(A,z)=C-1-i(z),  0<=i(z)<=g.
   ```

   If two such vertices project to the `B` side of `u`, then

   ```text
   |i(z_1)-i(z_2)| >= 3.                          (8)
   ```

   The analogous assertion on the `A` side uses the `B`-tail index.  Thus a
   fixed side has at most `floor(g/3)+1` non-fork two-sided tail owners.

8a. Still in the separated geometry, relabel the endpoints so that
    `p=d(A,u)<=q=d(B,u)`.  Let `z` be an `A`-tail owner and let `c` be its
    diameter projection, with `r=d(A,c)`.  If `r<=p` (the *short-side cis*
    case), then `z` necessarily also owns a `B`-tail value.  In particular,
    writing

    ```text
    d(A,z)=C-1-a,   d(B,z)=C-1-b,   0<=a,b<=g,
    ```

    gives the exact identities

    ```text
    2r=C+g+b-a,       2d(c,z)=C-g-2-a-b,       b<=a.       (8a)
    ```

    This localises the only one-sided `A`-tail escape, under `p<=q`, to the
    trans side `r>p`.  It does not bound that trans side, the long-side cis
    owners, or close the tail quota.

8b. Under the same labelling, consider a `B`-tail owner whose projection has
    `B`-coordinate `s<=q` and whose `A`-distance is *not* in `H` (a
    long-side, one-sided cis owner).  Then

    ```text
    ceil((D+1)/2) <= s <= q.                       (8b)
    ```

    If `q-p<=8`, this interval has integral diameter at most three.  The
    backbone four-gap therefore forces all such owners to the same gate.
    After deleting the three fork exceptions `u,v_1,v_2`, their `B`-tail
    indices are three-separated, so there are at most `ceil((g+1)/3)`
    nonexceptional owners and at most `ceil((g+1)/3)+3` owners in total.
    The `+3` is necessary: the exceptional depths zero, one and two are not
    mutually three-separated.

8c. Let `delta=q-p`, and let `z_L,z_R` be distinct two-sided high-tail
    owners outside `{u,v_1,v_2}`.  If their projection coordinates satisfy
    `r(z_L)<=p<=r(z_R)`, and their endpoint-tail indices are respectively
    `(a_L,b_L)` and `(a_R,b_R)`, then

    ```text
    |a_R-b_L-delta| >= 3.                         (8c)
    ```

    Thus the two-sided matching cannot use any of the three cross-side
    diagonals `a_R=b_L+delta, b_L+delta+1, b_L+delta+2`.  This is a genuine
    cross-channel constraint, but it does not yet control one-sided owners
    or the internal distances between different gates.

8d. Let `L` and `R` be two-sided high-tail owners with strictly left and
    strictly right projection coordinates, respectively (`r(L)<p<r(R)`).
    If `b(L)` is the `B`-tail index of `L` and `a(R)` the `A`-tail index of
    `R`, then

    ```text
    d(L,R)=C-g-2-b(L)-a(R).                        (8d)
    ```

    Consequently the map `(L,R) -> b(L)+a(R)` is injective on the Cartesian
    product of any such left/right owner sets.  In particular, if there are
    `ell` strict-left and `rho` strict-right owners, then

    ```text
    ell*rho <= 2g+1.
    ```

    This is a cross-gate sumset constraint, not yet a contradiction: the
    present tail counts do not force both factors large enough.

9. The exceptional gap is linearly bounded in the core order:

   ```text
   g <= 4i-14.                                    (9)
   ```

   Hence the only possible outlier values for an order-`i` prefix-defect
   core lie in the finite interval

   ```text
   C+21 <= D <= C+4i-14.
   ```

10. In the separated geometry `u in P`, write `p=d(A,u)` and
    `q=d(B,u)`.  If `p<C/2+4`, the `A`-translate values in the high tail are
    three separated, and hence

    ```text
    (g+1)-ceil((g+1)/3) <= i-2.                   (10)
    ```

    The symmetric assertion holds if `q<C/2+4`.  Thus any core violating
    (10) is forced into the balanced geometric case

    ```text
    p,q >= C/2+4.
    ```

In particular, at corridor gap `g>=21`, the two exceptional leaves can be
removed without touching the complete distance prefix `1,...,21` or the
rooted `1--2` fork.  Equation (2), rather than the parity square condition
alone, is the exact interface that an induction or finite prefix catalogue
must exploit.

## Proof

Endpoints of a maximum-weight path in a positive-weight tree are leaves: an
extra edge at an endpoint would extend the path and exceed `D`.  The pairs
`(A',B)` and `(A,B')` have distances `D-alpha` and `D-beta`.  They are not the
unique diameter pair, so both values are at most `C-1`.  This gives (1).

Every path involving `A`, except `AB`, has weight at least `alpha>=g+1`; the
same holds for `B`.  Hence the pairs realising `1,...,g` avoid both endpoints
and survive in `K0`.  A diameter endpoint is a leaf whose incident edge has
weight at least `g+1`; when `g>=2` it can therefore be neither endpoint of a
weight-1 or weight-2 edge.  Their common endpoint has degree at least two as
well, proving the rooted-fork assertion.

The unordered vertex pairs of `K` split into the pairs internal to `K0`, the
pairs `Az` with `z in K0`, the pairs `Bz` with `z in K0`, and `AB`.  Their
distances are respectively

```text
dist(K0),  alpha+R_A,  beta+R_B,  D.
```

Global distance injectivity makes these sets disjoint.  They have together
`C` elements, and `D` is the only distance outside `1,...,C-1`; this proves
(2)--(3).

No value below `alpha` can involve `A`, so `K-A` contains
`1,...,alpha-1`.  It cannot contain `alpha`, because the different pair
`AA'` already has that distance in `K`.  This proves the one-leaf statement.

Finally,

```text
d(A,z)=s+t,       d(B,z)=D-s+t.
```

Neither pair is `AB`, hence both distances are at most `C-1=D-g-1`.
Rearranging the two inequalities gives (4).  `QED`

For (5), take `x,y in K0`, denote their diameter projections by `c_x,c_y`,
and write `r_x=d(A,c_x)`, `r_y=d(A,c_y)` and
`h_x=d(c_x,x)`, `h_y=d(c_y,y)`.  Suppose without loss of generality that
`r_x<=r_y`.  Going from `x` to `c_x`, along the diameter to `c_y`, and then
to `y` gives the valid path upper bound

```text
d_K0(x,y) <= h_x + (r_y-r_x) + h_y.
```

Apply the left inequality of (4) to `x` and the right inequality to `y`:

```text
h_x-r_x <= -g-1,
h_y+r_y <= D-g-1.
```

Their sum is at most `D-2g-2=C-g-2`, proving (5).  The tail assertion then
follows from the exact disjoint tiling (2).  `QED`

For (6)--(7), the two fork leaves cannot lie on `P`: they remain pendant in
`K0`, while neither can equal `A'` or `B'` (each of those is adjacent to a
diameter leaf in `K`).  Thus no two distinct vertices of `P` can be at
distance `1`, `2`, or `3`, since those three distances are already uniquely
realised by the fork pairs.  Along the path `P`, the rooted distances from
either endpoint therefore have gaps at least four.  An interval of `g+1`
integers contains at most `ceil((g+1)/4)` such values.  Apply this separately
to the two translates covering `H`, using (5), to obtain (6).  Each remaining
tail value is endpoint-cross and each off-backbone vertex participates in at
most two such pairs (one with `A`, one with `B`); taking a ceiling after
dividing (6) by two gives (7).  `QED`

For (8), put `p=d(A,u)`.  If the projection of `z` lies on the `B` side,
then the path from `A` to `z` goes through `u`, so

```text
d(u,z)=d(A,z)-p=C-1-i(z)-p.
```

Equal indices repeat the two pairs with `u`.  An index difference one gives
two `u`-depths differing by one and hence repeats a distance between the
two distinct pairs obtained by appending the weight-one and weight-two fork
leaves.  An index difference two gives the corresponding collision between a
root pair and a pair using the weight-two leaf.  These are exactly the
fork-root separation identities proved above, so (8) follows.  The two fork
leaves are excluded because their `u`-depths are the exceptional values one
and two.  `QED`

For (9), `K0` has `i-2` vertices and its backbone `P` has at least the two
distinct vertices `A',B'`.  Thus `|V(K0)\P|<=i-4`.  Combine this with (7):

```text
floor((g+1)/4) <= i-4.
```

The integral rearrangement is `g<=4i-14`.  `QED`

For (10), take an `A`-tail owner `z`, let `r` be its projection coordinate
and `h=d(c,z)`.  If `r>=p`, its path to `A` passes through `u`, giving
`d(u,z)=d(A,z)-p`.  If `r<=p`, the collar gives

```text
r >= (d(A,z)+g+1)/2 >= C/2.
```

The backbone coordinates have gaps at least four.  When `p<C/2+4`, the
window `[C/2,p]` therefore contains only its already present endpoint `u`;
thus the second case also has `r=p` and again

```text
d(u,z)=d(A,z)-p.
```

For `i>=18`, the earlier linear cap (9) strengthens to `g<=C/2-7`; hence the
exceptional fork depths `0,1,2` give `A`-distances below the high tail in the
present window.  All `A`-tail owners are subject to fork-root
three-separation, so at most `ceil((g+1)/3)` of the `g+1` tail values are
`A`-owned.  The remaining values are distinct `B`-cross pairs and the `B`
root profile has only `i-2` vertices, giving (10).  `QED`

For (8a), put `m=d(A,z)` and `h=d(c,z)`, so `m=r+h`.  The complementary
endpoint distance is exactly

```text
d(B,z)=D-r+h=D+m-2r.                              (11)
```

If this distance were not in `H`, it would be at most `C-g-2`, since it is
an endpoint-cross distance below the diameter.  As `m>=C-g-1`, (11) would
then give

```text
2r >= m+2g+2 >= C+g+1=D+1.
```

But `r<=p<=q` implies `r<=D/2`, a contradiction.  Thus
`d(B,z)=C-1-b` lies in `H`.  Substituting `m=C-1-a` into (11) yields the
first two identities in (8a); the inequality `r<=p` becomes
`b-a<=2p-D=p-q<=0`.  `QED`

For (8b), write `m=d(B,w)=C-1-k` and let `h` be the height above the
projection.  The complementary distance is

```text
d(A,w)=D-s+h=D+m-2s.
```

If it is not in `H`, it is at most `C-g-2`; hence

```text
2s >= C+2g+1-k >= C+g+1=D+1,
```

which proves (8b).  The width of the resulting interval is at most
`(q-p-1)/2`; for `q-p<=8` it is strictly less than four.  Distinct backbone
gates have distance at least four, so the gate is unique.  At that gate the
nonexceptional root depths differ exactly as their `B`-tail indices, and the
fork-root separation proves the stated nonexceptional capacity.  The three
exceptional vertices `u,v_1,v_2` may occupy the same gate with depths zero,
one and two, so they must be counted separately.  `QED`

For (8c), the two-sided identities give the root depths directly.  On the
left of `u`,

```text
d(u,z_L)=d(B,z_L)-q=C-1-b_L-q,
```

whereas on the right,

```text
d(u,z_R)=d(A,z_R)-p=C-1-a_R-p.
```

Their difference is `a_R-b_L-(q-p)`.  The fork-root profile has no
repeated depth or depth difference one or two between two nonexceptional
vertices, which proves (8c).  `QED`

For (8d), write the two endpoint-index identities at the two projection
gates.  Since the gates are distinct, the path from `L` to `R` traverses the
backbone segment between them, so

```text
d(L,R)=h(L)+(r(R)-r(L))+h(R)=C-g-2-b(L)-a(R).
```

Different ordered choices `(L,R)` are different unordered vertex pairs, and
all tree distances are globally distinct.  Thus their displayed index sums
are distinct.  They lie in `{0,...,2g}`, giving `ell*rho<=2g+1`.  `QED`

## Trust boundary and next use

Nothing above excludes an arbitrary inner tree containing a fixed prefix;
claiming that it does would be circular.  The remaining all-order step is to
combine the forced high-tail ownership from (5), the exact tiling (2), and
the rooted `1--2` fork, or to prove that repeated endpoint stripping creates
a proper prefix-defect core with a strictly smaller parameter.  Until that
decreasing parameter is proved, the singleton-corridor branch remains
**UNVERIFIED**.
