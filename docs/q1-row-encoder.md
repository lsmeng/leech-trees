# Universal q=1 row-conditioned realization encoder

Status, 2026-08-25:

- **OBSERVED:** the tree/model correspondence, exact `Q` coverage, triangular
  distance recurrence, optional propagation constraints, fail-closed output
  semantics, and the implementation-level small-order oracle have been
  independently audited.
- **OBSERVED negative performance result:** the propagation sprint fails its
  predeclared small-order gate at `n=11`; the order-conditioned CP-SAT route is
  stopped before `n=16` and before any `n=25` search.
- **UNVERIFIED:** CP-SAT `INFEASIBLE` has no independently checkable proof log,
  and this work proves no new order exclusion and does not prove G18.

## Purpose and stop rule

The generic forest search has no usable order-25 scale.  FW218--FW219 give a
canonical coordinate system for every hypothetical Leech tree of order at
least five.  This pilot tested whether encoding that exact system eliminates
enough topology freedom to make a finite order-25 branch measurable.

The pilot passes only if:

1. both directions of the model/tree correspondence are proved;
2. every permitted `Q` branch is represented;
3. known positive and negative small orders behave correctly;
4. every SAT result passes `src/checker_a.py` and `src/checker_b.py`;
5. the row encoder beats the topology-free forest engine by orders of
   magnitude at a predeclared `n=16` gate before any order-25 sentinel is run;
6. only after that gate, capped `n=25`, `Q=2,10,19` sentinels may be run on Geo
   Workstation.

`UNKNOWN`, timeout, memory cap, unfinished coverage or `found=0` at a cap are
not exclusions.  The small-order curve did not reverse, so conditions 5--6
were not reached.  No `n=16` or `n=25` row was run.

## Canonical variables

Let `N=binomial(n,2)`, `m=n-1`, and orient the unique q=1 diameter endpoints
as in FW218.  Remove endpoint `x`, root at its neighbour, and write `y(v)` for
the FW219 reflected coordinate.  For a fixed first hole `Q`, relabel the
vertices of `T-x` by increasing coordinate.  Global distance uniqueness
makes this ordering canonical:

```text
y_i=i                              for 0<=i<Q,
Q<y_Q<...<y_(m-1)<N,
root=m-1,
parent(i) in {i+1,...,m-1}.
```

The missing coordinate is exactly `Q`.  FW219g gives

```text
Q<=4(n-2-Q)+7,
Q<=floor((4n-1)/5).
```

Thus order 25 has the complete branch list `Q=2,...,19`.

Every edge of `T-x` is forced by its parent:

```text
w(i,parent(i))=y_parent(i)-y_i.
```

The final endpoint edge is

```text
w(x,root)=N-y_root.
```

## Triangular distance recurrence

For `i<j`, the path from `i` to `j` begins with the parent edge of `i`, since
a larger-coordinate vertex cannot be a descendant of `i`.  Conditional on
`parent(i)=k`,

```text
d(i,j)=y_k-y_i                         if k=j,
d(i,j)=y_k-y_i+d(min(k,j),max(k,j))    otherwise.
```

Every distance on the right has minimum index greater than `i`; the system is
therefore triangular rather than a cyclic LCA encoding.  All internal
distances lie in `[1,M]`, `M=N-Q`, and

```text
d(x,i)=N-y_i.
```

There are exactly

```text
binomial(m,2)+m=N
```

distance variables.  Requiring them all distinct in `[1,N]` forces them to
be exactly `{1,...,N}`.  The explicit global distance-sum identity
`sum d=N(N+1)/2` is redundant but kept for propagation and audit visibility.

## Audited completeness map

Tree to model:

1. apply FW218 and FW219;
2. sort `T-x` vertices by their distinct reflected coordinates;
3. record the rooted parent of each nonroot vertex;
4. use the displayed path recurrence;
5. choose the branch indexed by the actual `Q`.

Model to tree:

1. connect every `i<m-1` to its selected larger parent with the positive
   coordinate difference;
2. connect `x=m` to root `m-1` with weight `N-y_(m-1)`;
3. the increasing-parent rule makes a connected acyclic tree;
4. AllDifferent plus the bounds makes its pair spectrum exactly `I_N`.

For `n>=5` the root-hit exception has already been excluded in FW219.  The
audit also checked that the displayed `Q` bound has the stated universal
quantifiers.  There is no additional topology or sibling symmetry breaker:
the ordered endpoints and injective `y` coordinates canonically name every
remaining vertex, so an uncoloured-tree canonicalisation here would risk
deleting a genuine role embedding.

The implementation is:

```text
theory-lab/topwindow/q1_row_cpsat.py
```

The independent oracle does not reuse the CP-SAT recurrence.  It reconstructs
the weighted tree and computes distances by BFS, checks the recurrence and hop
recurrence on deterministic increasing-parent trees, canonicalises all five
known witnesses from raw edges, exercises fail-closed summary semantics, and
compares complete free row sweeps at orders 5--8 with the topology-free forest
engine:

```text
theory-lab/topwindow/verify_q1_row_encoder.py
```

The oracle covers 2,944 deterministic rooted states, 294,400 independent
pair-distance checks, 294,400 hop checks, 81,880 distinct-edge hop-bound
checks, 38,272 independently reconstructed subtree-size checks, and all 19,894
ordered cut rows for `5<=n<=200`.  It also pins `L6` through every optional
propagation mode, including the full edge-cap/value-first combination; every
SAT control passes both `src/checker_a.py` and `src/checker_b.py`.

This is an audited research encoder, not an independently checkable UNSAT
certificate, an order-25 exclusion, or G18.

## Optional exact propagation

All switches are redundant consequences of the exact Leech model; none is a
new assumption or symmetry cut.

- `--inverse` adds the inverse permutation between the values `1,...,N` and
  their canonical actual-pair owners.
- `--value-first` uses that inverse to branch on the owner of values
  `1,2,...`; it is available only with `--inverse`.
- `--parity` adds Taylor parity
  `a(n-a)=ceil(N/2)`.  This is powerful only at arithmetically impossible
  orders and can make allowed rows slower.
- `--structural` applies the correct FW218 bound to the edge incident with
  coordinate-zero endpoint `z`, applies the independent radius bound to the
  edge incident with `x`, and forces values 1 and 2 to be edge weights.  The
  `z` edge must not be confused with the `x` edge: in `L6` they are 2 and 8.
- `--hop-bound` mirrors the triangular recurrence in unweighted hop counts
  and imposes `d>=binomial(h+1,2)` because a path contains distinct positive
  edge weights.
- `--edge-cap` computes every rooted subtree order exactly from the
  increasing-parent variables and applies the audited cut-product/rooted-span
  edge cap below.  It is retained for reproducibility, not enabled by default.

For an edge whose deletion has side orders `s,n-s`, put

```text
c=s(n-s),  C_s=binomial(s,2),  C_t=binomial(n-s,2),
L(s)=ceil((C_s+C_t)/2)+min(ceil(C_s/2),ceil(C_t/2)).
```

The joint rooted-span bound gives `w<=N-L(s)`.  The independently proved
finite edge-excess ladder gives

```text
f(c)>=1,2,3,4,5,6,7,8,9
at c>=11,19,21,29,31,33,35,42,44,
w<=N+1-c-f(c).
```

Thus `--edge-cap` uses

```text
U_n(s)=min(N-L(s), N+1-s(n-s)-f(s(n-s))).
```

At `n=25`, the exact caps for `s=1,...,12` are

```text
s       1   2   3   4   5   6   7   8   9  10  11  12
U(s)  162 172 181 189 192 178 166 156 148 142 138 136
```

The exact first cut moment

```text
sum_e w_e s_e(n-s_e) = N(N+1)/2
```

was also encoded in a temporary ablation.  It is mathematically redundant and
made the solver slower, so it is deliberately not a released switch.  A
second-moment encoding would add still more nonlinear/ancestor machinery to a
model that already has the exact distance permutation and was not pursued.

## Frozen implementation boundary

The encoder emits one JSON document, uses exclusive-create output rather than
append, and records source/model/checker/host/parameter hashes.  A complete
summary requires the exact default `Q` list in order and every row to be
`INFEASIBLE`.  Missing, repeated, reordered or out-of-range rows fail closed.
Every SAT witness is reconstructed and checked by both independent checkers.

CP-SAT's memory parameter and a 50 ms RSS watchdog are both active.  On the
current macOS/Python 3.14 runtime, lowering `RLIMIT_RSS` is rejected by the OS;
the output records that fact and does not pretend that the in-process watchdog
is a kernel hard limit.  Geo Workstation's OR-Tools 9.11 and the local
OR-Tools 9.15 use different Python/protobuf APIs; compatibility fixes were
independently replayed in both versions, including the positive `L6` row.

Final frozen hashes after the last replay are:

```text
q1_row_cpsat.py                 475d18350b75475eb36a7403ad90772f72b1b0e17b2811cd9a06daf14888a93f
verify_q1_row_encoder.py        ea298e9bfb4151377aaf6c8baade81cbe10e646f6bb2d570b92cb2ca3f087f56
verifier deterministic stdout  8cab3d3b4ed5c6d91ca386f1572797c283c19585927b8b8186cde0f3a9fecd42
```

The independent verifier freezes the expected encoder hash; two complete
replays produced byte-identical stdout.

## Small-order calibration

The topology-free forest baseline, recomputed locally in one unsharded run per
order, is:

| order | forest nodes | result | wall time |
|---:|---:|---:|---:|
| 5 | 11 | 0 solutions | <0.001 s |
| 6 | 47 | 1 solution | <0.001 s |
| 7 | 215 | 0 solutions | <0.001 s |
| 8 | 961 | 0 solutions | <0.001 s |
| 9 | 4,750 | 0 solutions | 0.002 s |
| 10 | 23,451 | 0 solutions | 0.005 s |
| 11 | 123,309 | 0 solutions | 0.036 s |
| 12 | 704,494 | 0 solutions | 0.208 s |

The principal one-worker CP-SAT ablation used seed 1, 2 seconds per `Q`, and a
2 GiB cap:

| order | propagation | completed rows | total row time |
|---:|---|---:|---:|
| 8 | baseline | 5 UNSAT | 2.098 s |
| 8 | inverse | 5 UNSAT | 1.961 s |
| 8 | parity | 5 UNSAT | 0.020 s |
| 8 | inverse + parity | 5 UNSAT | 0.019 s |
| 9 | baseline | 4 UNSAT, 2 UNKNOWN | 6.530 s |
| 9 | inverse | 4 UNSAT, 2 UNKNOWN | 6.967 s |
| 9 | parity | 3 UNSAT, 3 UNKNOWN | 6.835 s |
| 9 | inverse + parity | 3 UNSAT, 3 UNKNOWN | 6.949 s |

Parity closes `n=8` in presolve only because Taylor's equation has no integer
root there.  At `n=9` it makes one previously completed row time out, so it is
not a uniform speedup.  For `Q=2`, inverse plus value-first reduces the
2-second branch counts from 96,160 to 93,266 at `n=8` and from 126,943 to
71,087 at `n=9`, but the latter remains `UNKNOWN`.  Exact edge-cap propagation
changes the longer `n=9,Q=2` baseline only from 20.13 s / 583,351 branches to
19.96 s / 555,449 branches; the first moment reaches `UNKNOWN` at 30 seconds.
The released exact-cap + inverse + value-first pack closes that row in 24.736
seconds / 231,631 branches on the final local runtime: fewer branches do not
translate into a wall-time improvement over baseline.

The last workstation pre-gate used one worker, a 2 GiB cap, and the strongest
useful owner/value/cut-cap pack on `n=11,Q=2`.  It remained `UNKNOWN` after 60
seconds (436,999 branches, 313,074 conflicts, 139.223 MiB peak RSS), while
the recorded local generic forest search over *all* `n=11` states takes about
0.04 seconds.  Across these recorded runs, the row model is over three orders
of magnitude slower in wall time before it even covers the other `Q` rows;
the wall figures are a stop-gate diagnostic, not a hardware-normalised
publication benchmark.

## Stop verdict and successor

The mathematical encoder and its engineering boundary pass.  The proposed
computational route does not: safe redundancies change constants but do not
restore the forest engine's low-distance forcing.  Under the predeclared gate,
the sprint stops at `n=11`; `n=16` and the `n=25` sentinels `Q=2,10,19` were
not authorised or run.  Hoffman2 was not used.  No local or workstation heavy
row process remains.

The next useful mathematical milestone is a **low-owner localisation theorem**:
prove that the owners of an initial interval `1,...,k` lie in a bounded
visible/core interface, or equivalently give a bounded rooted-ball/attachment
catalogue that preserves actual-pair provenance.  Such a theorem could feed a
custom forced-prefix engine and recover the forest search's decisive
propagation.  Adding more global moments, span constants or generic CP-SAT
redundancies without that localisation is not counted as progress.

## FW269 successor verdict

The requested low-owner audit has now been carried out.  Its **OBSERVED**
positive theorem is exact but weaker than the engine milestone.  Every owner
of `1,...,Q-1` lies in one of four explicit LCA cones.  The unique weight-1
edge also has cross-Sidon cut-side rooted depths, and each side contains no
two rooted depths differing by one.  Hence the visible coordinates below the
unit edge form an independent set and number at most `ceil(Q/2)`.

This does not bound the attachment depth: a unit edge in a pure threshold-core
tail can have no visible descendant at all.  FW269c shows that this is a real
limitation of the weakened interface.  For every fixed `I_kappa`, a globally
distance-distinct q=1-top-geometric pressure family places the low edge owners
at separated `Theta(n)`-deep core anchors.  The family is not Leech and fails
FW219c/FW261 exact tight-spectrum coverage, so it is a pressure diagnostic,
not a counterexample to a Leech theorem.

The **OBSERVED exact** fifteen local owner signatures through `I_6` do not
repair the missing attachment information.  The deliberately stronger
**OBSERVED external/non-replayed engine diagnostic** in which the unit edge
has a permanent true-leaf endpoint gives 1,351 constructed candidates by
insertion depth six,
already above the 1,233 charged-node 100-fold gate derived from the 123,309
node order-11 forest baseline.  That external count is not part of the frozen
FW269 arithmetic replay.

Therefore the encoder remains stopped: there is no new custom engine, n=16
gate, or n=25 sentinel.  Reopening requires an **UNVERIFIED** pure-core-tail
elimination theorem or a full tight-spectrum owner-provenance bridge from
FW219c/FW261.  Full proof, construction and trust boundary:
`docs/q1-low-owner-localization.md`.  Frozen deterministic replay:
`theory-lab/topwindow/verify_q1_low_owner_localization.py`, with certificate
`theory-lab/topwindow/results/q1_low_owner_localization_certificate.json`.
G18 is unchanged.

## FW270 final successor audit

Both FW269 reopening conditions have now been tested.  The full
tight-spectrum option is circular at the exact level: after the proved q=1
top-owner class is added, FW219c is coefficientwise equivalent to `F_T=I_N`,
and FW261 only refines that same actual-pair partition.  At every finite
level, an **OBSERVED negative metric pressure family** realizes formal
diameter-`D` owner suppliers matching the `I_P`-projections of FW219c/FW261
for every `P>=Q>=2`, while retaining a nonpendant pure-`H` unit edge and
missing `P+1`.  It is not an FW219c/FW261 state.

The unit-edge domino identity and pure-tail parity packing do give the
**OBSERVED** bounds

```text
d(x,b)>=2Q+1,
2|A|-1<=M-1-d(x,b)<=M-2Q-2,
```

but not a contradiction.  The possible replacement, a near-perfect
nonpendant-unit diameter theorem, remains **UNVERIFIED**; its evidence through
order 12 is only an **OBSERVED external/non-replayed finite diagnostic**.  It
would reduce only to `Q<=4` and would leave the singleton tail untreated.

Therefore the row encoder remains stopped.  It can reopen only after a rooted
near-perfect realization theorem and a separate singleton-tail theorem.
There is no new engine, gate, or sentinel, and G18 remains **UNVERIFIED**.
Full FW270 proof and trust boundary: `docs/q1-pure-tail-stop.md`.
