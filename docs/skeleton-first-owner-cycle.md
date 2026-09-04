# Skeleton first-owner transition and cycle reduction (FW284)

FW283 strictly stopped a single leaf-port prefix from following an unnamed
owner gate.  FW284 replaces that gate by a canonical transition on the
linear full-window skeleton.  Every first colored owner either lies inside a
named first-level thin cap or crosses a named core/boundary edge.  Repeating
the transition therefore produces an actual directed cycle.

This is an **OBSERVED all-order exact reduction**, not an exclusion.  The
remaining cycle theorem, NSSC, is still **UNVERIFIED**.

## 1. The guaranteed second cut

Let `C` be a nontrivial full-window sink core.  Two different graph leaves of
`C` do not always give two different core cuts: if `|C|=2`, both leaves share
the same core edge.  Thus the uniformly guaranteed configuration is:

1. a core-leaf edge `e=vv_0` of weight `p`; and
2. a first-level cap boundary `f=bc` of weight `g` at another core leaf.

The second boundary exists because every graph leaf of `C` has an attached
cap; otherwise it would be a global leaf and could not belong to a
full-bidirectional component.  This remains valid when `C` is a single edge.

Let `S` be the `v`-side of `e`, let `B` be the strict thin cap outside `f`,
and put

```text
M=T-(S union B).
```

Then `M` is connected.  Write `ell=d_C(v_0,c)` and define actual rooted
depths

```text
u_x=d_S(v,x),              x in S,
w_z=d_B(b,z),              z in B,
lambda_m=d_M(v_0,m),       m in M,
rho_m=d_M(c,m),            m in M.
```

If the projection of `m` to the `v_0--c` connector is at distance `t_m` from
`v_0` and has off-connector height `h_m`, then

```text
lambda_m=t_m+h_m,
rho_m=ell-t_m+h_m,
lambda_m+rho_m=ell+2h_m.                         (FW284.1)
```

The two rooted depth sets on `M` are therefore vertexwise matched; they are
not independently permutable factors.

## 2. Exact three-block owner identity

Let `U,W,L,R` be the rooted polynomials of the four depth lists above.  The
six actual pair classes `SS,MM,BB,SM,MB,SB` give

```text
I_N
 = F_S + F_M + F_B
 + X^p U L
 + X^g W R
 + X^(p+ell+g) U W.                              (FW284.2)
```

Every coefficient retains its actual unordered-pair owner.  The cross
polynomials at the two cuts are

```text
C_e=X^p U(L+X^(ell+g)W),
C_f=X^g W(R+X^(ell+p)U).                         (FW284.3)
```

The shared `S--B` class is identical in both ledgers, and hence

```text
C_e-C_f=X^p U L-X^g W R.                         (FW284.4)
```

This subtraction alone is a tautological reclassification, not a
contradiction.  Its useful content is the actual pair-class switch:

```text
pair class   e-cut            f-cut
SS           same S           same complement
MM           same complement  same complement
BB           same complement  same thin cap
SM           cross            same complement
MB           same complement  cross
SB           cross            cross
```

For a pair that is cross in both cuts, its two offsets differ by `p-g`.
Equation (FW284.1) supplies the required common-vertex matching inside `M`.

## 3. The full-window skeleton

Delete every first-level cap boundary from `C` and retain

```text
E_skel=E(C) union {all first-level boundary edges}.
```

If the first-level caps have total order `n-|C|`, then their count is at most
that number, so

```text
|E_skel|=(|C|-1)+d <= n-1.                       (FW284.5)
```

For every skeleton edge `q`, write its weight as `w_q`.  In a Leech tree of
order `n>=18`, its cut product is at least `n-1`, the strict edge bound leaves
at least ten coefficients above `w_q`, and the rooted-prefix theorem applies.
Thus the exact cut ledger has a compensated first cross hole

```text
eta_q in {1,2,3,4,5,6,8,9,10}.                  (FW284.6)
```

Let `P_q` be the unique same-side owner path of distance

```text
d(P_q)=w_q+eta_q.                                (FW284.7)
```

For a core edge both same-side colors are nonempty.  For a first-level
boundary, the strict thin cap contributes no distance above its boundary, so
the owner is on the inward side.  Complete Leech coverage is load-bearing:
without it the first missing cross coefficient need not have a same-side
owner and the transition below need not be total.

## 4. Skeleton first-hole transition theorem

Define `tau(q)` from the actual endpoints and path of `P_q`.

### Case I: cap lift

If both endpoints lie in one first-level cap `A_j`, put `tau(q)=f_j`, its
boundary.  Thinness gives

```text
w_(tau(q)) >= w_q+eta_q+1.                       (FW284.8)
```

Writing

```text
sigma_q=w_(tau(q))-w_q-eta_q,
```

we have `sigma_q>=1`.  If `q=f_j`, its first owner is on the inward side, so
this case cannot return to the same boundary.

### Case II: actual owner return

After all skeleton edges are deleted, the components are the first-level cap
interiors and single core vertices.  If the endpoints are not in one cap,
their path crosses a skeleton edge.  Since `P_q` is same-side at the `q` cut,
it does not cross `q`.  Choose the unique maximum-weight skeleton edge `r` on
the path and put `tau(q)=r`.  The owner becomes cross at `r`:

```text
w_q+eta_q=w_r+alpha_q+beta_q,                    (FW284.9)
rho_q:=alpha_q+beta_q=w_q+eta_q-w_r >= 0.         (FW284.10)
```

The old edge `q` lies wholly on one side of `r`, so its owner changes in the
opposite direction: cross at its own cut and same-side at the target cut.

These cases are exhaustive and `tau(q) != q`.  Therefore

```text
tau:E_skel -> E_skel
```

is a fixed-point-free total map.  Since the skeleton is finite, every orbit
enters a directed cycle.  The formerly arbitrary gate is now named by a cap
boundary or a skeleton edge.  This is a state compression, not a metric bound
on the gate distance.

## 5. Lift/drop trichotomy

The FW283 path dichotomy makes every transition exactly one of the following.

1. **Cap lift:**
   `w_tau-w_q=eta_q+sigma_q` with `sigma_q>=1`.
2. **Edge lift:** `P_q` is the single target skeleton edge, so
   `w_tau-w_q=eta_q`.
3. **Path drop:** `P_q` has at least two edges, all below `w_q`, hence
   `w_tau<w_q`.  Put `delta_q=w_q-w_tau>=1`.  At the target cut,

```text
delta_q           is owned same-side by the old edge q,
delta_q+eta_q     is cross-owned by P_q,
rho_q=delta_q+eta_q.                              (FW284.11)
```

The two owners in (FW284.11) are actual named pairs whose distances differ by
at most ten.

## 6. Cycle balance

On a directed cycle, let `C_lift` be its cap lifts and `D` its path drops.
Summing the edge-weight changes around the cycle gives the exact identity

```text
sum_(q in D) rho_q
 = sum_(q on cycle) eta_q + sum_(q in C_lift) sigma_q.  (FW284.12)
```

Consequences:

1. every cycle contains a path drop;
2. the outgoing transition from a maximum-weight cycle edge is a path drop;
3. without cap lifts, the sum of returned residuals is at most ten times the
   cycle length.

This is an actual-owner ledger, but it does not exclude a cycle.  A scalar
balance loses the endpoint projections around successive connectors.

## 7. Pressure controls

### Known L6

The full-window sink is a singleton, so L6 is outside the remaining
nontrivial-core branch.  Its skeleton nevertheless gives an exact Leech
cycle:

```text
5 --edge lift, eta=3--> 8
8 --path drop, eta=1, rho=4--> 5,
4=3+1.
```

Thus local prefix states, one translated owner swap and cycle balance cannot
exclude cycles.  The nontrivial core connector is essential.

### FW282 one-defect tree

The actual transitions include

```text
1 -> 2 -> 3 -> 7,
11 --path drop--> 7.
```

At the weight-seven cut, offset two would require global distance nine, the
tree's unique missing in-range coefficient.  It has no compensating same-side
owner, so the Leech transition stops exactly there.  The outlier is 21.  This
confirms that complete coefficient coverage, rather than the local sink
geometry, makes `tau` total.

### FW283 remote-gate family

For `T_t`, the weight-20 first owner is the weight-30 edge inside the remote
cap.  FW284 turns it into the cap lift

```text
20 -> 2t-18,
sigma=2t-48.
```

At order eleven the target boundary already exceeds `N=55`, so its capped
Leech ledger does not exist.  The family therefore confirms both sides of the
trust boundary: one port cannot bound the gate, while the second named cap
detects precisely where no-outlier coverage fails.

## 8. Remaining theorem and trust boundary

> **UNVERIFIED NSSC (Nontrivial-Sink Skeleton-Cycle Exclusion).**  In an
> order-`n>=18` Leech tree with nontrivial full-window sink core, the FW284
> first-owner transition map has no directed cycle.

FW284 proves that such a tree must produce a cycle.  Consequently NSSC would
exclude the entire nontrivial-sink branch.  It is a substantially smaller
**state obligation** than the full LPCT coefficient ledger—one owner record
per skeleton edge—but, after the transition theorem, it is logically
equivalent to excluding this remaining branch.  It should not be advertised
as an already easier theorem or as an order exclusion.

L6 shows that the next proof must use the nontrivial core connector.  The
specific missing invariant is endpoint monodromy: compose the actual endpoint
and projection correspondences around a complete lift/drop cycle and prove
that a nontrivial core forces a repeated endpoint, reversed projection order,
or repeated distance.  Reopening with only a scalar cycle sum, independent
rooted prefixes or one translated window would discard the information FW284
was built to retain.

FW285 audits this proposed continuation and finds a sharper information
boundary: FW284 composes target edges, but it does not define a correspondence
between the incoming owner `P_q` and the next first owner `P_(tau(q))`.
Actual non-Leech pressure trees with nontrivial sinks have total FW284 cycles
whose consecutive owners are vertex-disjoint, and cap lift has the same
discontinuity.  Thus endpoint composition from the compressed records is now
a strict-stop mechanism.  NSSC remains open; the live successor is a
full-spectrum connector-crossing owner-overlap theorem.  See
`docs/skeleton-endpoint-monodromy-stop.md`.

FW286 then proves an exact path-drop reduction inside that full-spectrum
successor.  If removing `q` and its target `r` gives `A--q--B--r--C`, the
translated owner band is forced to be `AB` at offsets
`0,...,eta_q-1` and `BC` at `eta_q`; the `AC` class starts no earlier than
`eta_q+1`.  Thus the remaining path-drop theorem concerns only the terminal
adjacent `AB -> BC` owners.  Cap-lift transport and compatibility around the
cycle are still unproved.  See `docs/two-cut-terminal-owner-switch.md`.

FW287 turns the terminal pair into exact crossed-swap and four-point
identities.  Injectivity yields four projection/height cones; the critical
endpoint-edge bound excludes the complete left-projection cone.  The three
surviving modes `R,D,U` are locally realizable and remain unverified as
cycle-composable transports.  See `docs/terminal-four-cone-reduction.md`.

FW288 completes that local path-drop classification by retaining a named
bridge in `D/U`, an oriented marked connector interval in `R`, or the direct
shared endpoint.  The live NSSC bottleneck is now compatibility between these
typed records and the next FW284 arc, together with independent cap-lift
transport.  See `docs/terminal-local-transport.md`.

FW289 reduces cap lifts to direct shallow-endpoint transport or an unverified
remote-cap rectangle record.  The target first prefix alone cannot eliminate
the remote state, even when all four named rectangle cross distances stay
inside the pair cap.  See `docs/cap-endpoint-depth-stop.md`.

FW290 adds the target-first-owner fork for each path drop: exact return gives
a path-drop/edge-lift two-cycle, while strict return gives a sub-source owner.
The latter is not a skeleton potential because cap promotion can jump above
the source.  See `docs/pathdrop-target-owner-fork.md`.

FW291 reduces the exact-return branch to the target-cut owner strip
`BC^delta AB^eta BC` with matched two-root convolutions.  The local strip is
strictly insufficient; ERTC must use its global extension and nontrivial
connector together.  See `docs/exact-return-switchback-stop.md`.

The replay

```text
theory-lab/topwindow/verify_skeleton_first_owner_cycle.py
theory-lab/topwindow/results/skeleton_first_owner_cycle_certificate.json
```

checks support-defined skeletons, compensated/uncompensated first ledger
events, actual owner paths, all three transition types, the six pair classes,
connector projection identities and the stated controls.  It does not prove
NSSC, exclude a nontrivial sink, exclude an order, prove G18 or prove global
nonexistence.
