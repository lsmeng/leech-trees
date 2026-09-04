# Kruskal covering schedule and merge waste

**OBSERVED theorem.** These shape-independent identities control the light-edge
end of every Leech tree and quantify the distance mass forced by balanced
merges. They are a proved ingredient for the proposed thick-tip contradiction,
but no global nonexistence conclusion follows from them alone.

## Covering schedule

Let the edge weights of a Leech tree be

```text
w_1 < w_2 < ... < w_{n-1}.
```

Process them in increasing order. When edge `k` joins components of sizes
`a_k,b_k`, put

```text
Delta_k = a_k b_k,
Pi_k = Delta_1+...+Delta_k,       Pi_0=0.
```

Then

```text
sum_k Delta_k = N,
w_{k+1} <= 1+Pi_k                 (0<=k<=n-2).
```

More exactly,

```text
sigma_k = Pi_k-(w_{k+1}-1)
```

is the number of pairs already connected by the `k` lightest edges whose
distance is greater than `w_{k+1}`.

Proof: the light forest spans exactly `Pi_k` vertex pairs. Every value below
`w_{k+1}` is realised by a path using only lighter edges, so all
`1,...,w_{k+1}-1` occur inside that forest; the value `w_{k+1}` itself does
not. Counting the remaining spanned pairs gives the inequality and `sigma_k`.
The merge products sum to `N` because every vertex pair first becomes connected
at exactly one merge. `QED`

For the final merge, let the heaviest edge split component orders `a,b`. Then
`Pi_{n-2}=N-ab`, and the rigidity theorem in
`docs/heaviest-edge-rigidity.md` proves

```text
sigma_{n-2}=N-ab-w_{n-1}+1 >= 1                 (n>=5).
```

Thus the final covering inequality is never tight beyond the three known
orders `2,3,4`. A lower bound on this excess that grows with `a,b` is still
**UNVERIFIED**.

There is also a bounded-location refinement. For `n>=12`, among the ten
values `w_{n-1}+1,...,w_{n-1}+10` at least one is already realised inside a
component of the forest before the final merge. This follows from the rooted
cross-prefix theorem in `docs/heaviest-edge-rigidity.md`. It locates one unit
of final covering waste in a fixed window, but does not yet lower-bound the
total number of such units.

More precisely, the first missing cross deficit `h<=10` forces the final
cross-sum set above its minimum by at least `ab-h`. Hence the global quadratic
bound strengthens to

```text
TW >= (sum_k Delta_k^2-N)/2 + ab-10              (n>=12),
```

where `ab=Delta_{n-1}` is the final merge product.

The finite-hole extension does lower-bound that count at the first open
orders. Writing `E=sigma_{n-2}`, exact enumeration through `E=8` proves

```text
n=25,27: E>=3;     n=36,38: E>=7;     n=49,51: E>=9.
```

The holes occur by offsets `(10,19,22)`, through 40 for the first seven, and
through 51 for the first nine. Comparing the cross-deficit set with
`{0,...,ab-1}` therefore strengthens the final-merge waste term
`binom(ab,2)` by at least 24, 69 and 164 at those three target pairs,
respectively. The calculation is recorded in
`docs/heaviest-edge-rigidity.md`.

See `theory-lab/topwindow/verify_heaviest_excess_ladder.py`. These are rigorous
finite-order merge-waste inputs; a uniform asymptotic continuation is still
**UNVERIFIED**.

If the light forest has `m` nontrivial components after `k` edges, convexity of
`sum binom(v_i,2)` gives the component-concentration corollary

```text
w_{k+1} <= binom(k-m+2,2)+m.
```

Thus near-maximal early weight growth forces the light edges to concentrate in
few components.

## Exact waste identity

For integer `t`, let `Pi(t)` be the number of vertex pairs connected by edges
of weight at most `t`, and define

```text
TW = sum_{t=1}^N (Pi(t)-t).
```

Every summand is nonnegative by the covering argument. For a vertex pair `P`,
let `M_P` be the largest edge weight on its path. Double counting the thresholds
from `M_P` through `d(P)-1` gives

```text
TW = sum_P (d(P)-M_P)
   = N(N+1)/2 - sum_k w_k Delta_k.
```

The covering schedule also yields

```text
TW >= (sum_k Delta_k^2-N)/2.
```

There is an exact surplus refinement.  Put

```text
sigma_{k-1}=Pi_{k-1}-(w_k-1).
```

Then `w_k=1+Pi_{k-1}-sigma_{k-1}`, and therefore

```text
TW = (sum_k Delta_k^2-N)/2
     +sum_k Delta_k sigma_{k-1}.                  (4)
```

Indeed, while

```text
sum_k Pi_{k-1} Delta_k = (N^2-sum_k Delta_k^2)/2.
```

substitution into `TW=N(N+1)/2-sum_k w_k Delta_k` gives (4) exactly.
The usual quadratic lower bound is the result of dropping its nonnegative
weighted covering-surplus term.  Thus an early forest that already realises
several values above its next edge weight contributes in proportion to that
edge's merge product, not merely once.

As a topology-free corollary, Cauchy gives

```text
TW >= n(n-1)(n-2)/8.
```

A single balanced merge product strengthens this substantially. The missing
endgame is an upper bound on the waste that thick, bushy terminal profiles can
actually supply.

## Connected-subtree merge mass

There is a useful lower bound that keeps the merge products instead of
replacing them individually by one.  Let `Q` be any connected induced
subtree, and use the merge products from the Kruskal process on the full tree.
Then

```text
sum_{e in E(Q)} Delta_e >= binom(|Q|,2).           (5)
```

Indeed, for every pair of vertices of `Q`, the unique maximum-weight edge on
their path also lies in `Q`.  That pair is first connected when this edge is
inserted and is one of the `Delta_e` pairs counted at that merge.  Products
can be larger because their light components may already contain vertices
outside `Q`, which only strengthens (5).

For a bare pendant path, index edges from the free end so that the first `r`
edges span `r+1` vertices.  Equation (5) gives the simultaneous prefix bounds

```text
D_r:=sum_{s=1}^r Delta_s >= binom(r+1,2).
```

If `kappa(1)>=...>=kappa(S)>=0`, Abel summation therefore gives

```text
sum_{s=1}^S Delta_s kappa(s)
 = kappa(S)D_S+sum_{r=1}^{S-1}(kappa(r)-kappa(r+1))D_r
 >=sum_{s=1}^S s kappa(s).                         (6)
```

Equations (5)--(6) are **OBSERVED** shape-independent merge-mass statements.
Their terminal use, including the conditional handoff multiplicities, is
recorded as (FW176) in `docs/edge-handoff-orientation.md`.

## Computational audit

`theory-lab/smallend/verify_kruskal_waste.py` checks the path-maximum/merge
identity on 28,200 pairs in 900 deterministic random distinct-distance trees.
It then requires all five known Leech witnesses to pass both independent
checkers and verifies every one of their 14 schedule steps, all threshold
cover inequalities, both waste formulas, the exact weighted-surplus
decomposition (4), and the quadratic lower bound.

Run:

```text
python3 theory-lab/smallend/verify_kruskal_waste.py
```

The frozen summary is
`theory-lab/smallend/results/kruskal_waste_certificate.json`.
