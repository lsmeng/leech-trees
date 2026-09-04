# FW319 `b=27`: bundled residual two-branch frontier

This checkpoint is a single-entry replay of the already audited b=27 local
reductions.  It does not add a mathematical assumption; it prevents the
current frontier from depending on a prose-only chain of commands.

## Bundled result

The replay verifies, from the existing scripts and their load-bearing values:

```text
w >= 38,
r >= 16,
t >= 54,
32,34,35,36,37 are internal to L or J,
L-positive-arm overlap is closed,
J multi-edge 32 is impossible,
the J 32 path is a single edge,
the Pro deep-two-arm boundary is empty at b=27.
```

The L ancestor--descendant case has now been shape-reduced: under the
endpoint-edge floor, every distance-32 realization is a single new edge 32
attached at `P0` or `P1`; every longer fixed-core-plus-new-chain candidate
has an induced collision.  Therefore the exact residual cases are:

1. an L-internal single new edge of weight 32 attached at `P0` or `P1`; or
2. a J-internal single edge of weight 32.

For the L residual, adding the direct edge to the fixed core and checking all
cross translates to the three named J-side vertices `u,y0,y3` gives the
conditional floors `t>=77` when attached at `P0` and `t>=67` when attached at
`P1`.  This is a necessary finite floor only; it does not remove either
branch.

The same three-translate check, applied without the extra L edge, removes
seven isolated values from the low end of the J parameter: under `w>=38` and
`r>=16`, the only values below `67` that remain compatible with the complete
fixed-L spectrum are

```text
t in {54,59,61,62,63,64}.
```

Every `t>=67` still passes this necessary filter with `w=38`; this is a
parameter restriction, not an exclusion of the J single-edge-32 branch.

For the six isolated values, adding the two endpoints of the J edge `32` to
the translate test gives a further placement floor.  If `h` is the global
`d6`-depth of the shallower endpoint, then `h>=t+19` in every isolated row.
The edge is therefore forced beyond the named endpoint pair in precisely
these low-tail cases; this remains a necessary condition only.

One additional low-owner reduction is now verified.  The fixed-L rooted-depth
difference set forbids the corresponding edge weights in J, while every
interval of a J path must avoid the fixed-L spectrum and the punctured value
`4`.  Exhaustive path compositions show that J has no path of total `5` or
`21`.  Since both values lie below `w>=38`, their complete-spectrum owners
are forced to be L-internal.  Their LCA locations remain open.

For the six isolated rows below `t=67`, a row-conditioned refinement is also
verified.  Requiring the two J root distances `r` and `r+3` to avoid the
fixed-L spectrum leaves only `r=16` in each row (the relaxed `(64,38,26)`
row is removed by `r+3=29`).  The fixed-L spectrum and rooted-depth
difference set then leave only the one-edge J path `(16)`.  Global edge-weight
distinctness consequently rules out the L shapes `(5,16)` and `(16,5)` in
these rows, so the L owner of `21` is the direct edge `(21)`.  Replay:

```bash
.venv/bin/python theory-lab/scratch_pro_b27_isolated_j32_21_reduction.py
```

This refinement is row-conditioned and does not address `t>=67`, the remote
L attachment, or complete-spectrum closure.

## Pro low-support obligation (2026-08-28)

The persistent GPT Pro consultant identified the next finite obligation for
the J-single-edge-32 branch: enumerate the minimal owner-path forest for the
complete punctured prefix

```text
H37 = {5,16,18,19,20,21,24,25,26,32,34,35,36,37}.
```

This is stronger than selecting only convenient owners.  It must retain the
certified L shapes for 5 and 21, J-edge avoidance of `Delta(B0)`, all
low-distance injectivity and fixed-pair reuse rules, and the absence of 4.
The finite reduction is plausible because a path of total at most 37 cannot
use an edge heavier than 37; however, it is not yet a verified theorem until
the forest enumeration is independently implemented (preferably once as a
canonical weighted-tree enumeration and once as SAT/CP).

The first bounded replay is committed as
`theory-lab/topwindow/verify_pro_b27_j32_isolated_l521_minimal.py` (commit
`bf94a5a`).  It tests six isolated `t` rows, `h<=220`, a remote 5-edge from
`b2`, the shared `(5,16)` shape for 21, and the three J-32 gates.  It checks
edge-weight injectivity, all-pair injectivity, root-shift-4, and an explicit
order-25 cap after adding the punctured edge.  The run tested `473742`
candidates and found no survivor.  This is an `OBSERVED_CONTROL_SEARCH`
only: direct `(21)` placement, arbitrary remote L gates, other ownership of
34--37, `t>=67`, and the full low-support forest remain open.

The widened two-shape replay was then run on Hoffman2 as low-priority SLURM
job `98651` (one CPU, 2 GB, 20-minute limit, `nice=10000`).  It tested
`5,211,162` candidates and again found `survivors=[]`.  The machine-readable
output is
`theory-lab/topwindow/results/pro_b27_j32_isolated_l521_minimal_98651.json`.
This is still a bounded control result, not a complete-prefix theorem.

The follow-up Pro adversarial audit sharpened the finite-state requirement to
`(L0,F,pi,rho)`: the actual fixed core, the low-edge support forest, each
component's canonical attachment port, and its carrier/root orientation.
It confirmed that `>37` gateways cannot affect `<=37` distances, but warned
that an attachment-port completeness lemma is still required.  Without that
lemma, an abstract H37 forest may have trivial disconnected survivors and
cannot by itself be promoted to a J-32 exclusion.
The safe part of this audit is replayed by
`theory-lab/topwindow/verify_pro_b27_h37_support_bound.py` with status
`VERIFIED_LEMMA`; port completeness and H37 enumeration remain open.

The latest Pro refinement proposes a port-complete component state
`(T_C,p(C),sigma(C),H(C))`, where `T_C` is the actual low-support weighted
tree, `p(C)` is its rootward attachment port, `sigma(C)` is the `L/J` carrier,
and `H(C)` is the global `d6` depth of that port.  This is the minimum state
needed to recover LCA, cross-translate, and fixed-pair reuse information from
the actual topology.  Pro also suggested the conditional inequality
`H(C)+E_C+28<=N`, with `E_C=max_x d(p(C),x)`.  The fixed L depth set
`{0,6,13,14,15,23,27,28}` and its maximum `28` are confirmed by the existing
`VERIFIED` endpoint-floor replay, but the inequality itself is only
`CANDIDATE_BOUND`: the current frontier has not proved the required global
path decomposition or the meaning of `N` that would make the `+28` term valid.
The first safe test is therefore port-first enumeration of `R_p`, followed by
all `H` values whose `B0+(H+R_p)` translates avoid `S0` and the named J
translates.  A port can be removed only after this check has no feasible `H`.
The safe numerical audit is recorded by
`theory-lab/topwindow/verify_pro_b27_port_depth_candidate.py`; its status is
`CANDIDATE_BOUND`, because it does not prove the global `N` inequality or port
completeness.

A port-first prototype is now available at
`theory-lab/topwindow/scan_pro_b27_j32_port_profiles.py`.  It enumerates
rooted weighted component profiles and applies the necessary fixed-L and
named-J translate test.  Its two-edge smoke run is only
`OBSERVED_PORT_PROFILE_SCAN`; larger profile scans belong on Hoffman2 and do
not by themselves establish complete H37 coverage or J-32 nonexistence.
The reproducible low-priority Hoffman2 wrapper is
`scripts/hoffman2_port_profile_slurm.sh`; it was held until the login2 route
became responsive.

That wrapper has since run successfully as Hoffman2 job `98652` on `n1182`
(`COMPLETED`, exit `0`, about 6 seconds).  The `max_edges=3, h_max=220` scan
reported 993 admissible profiles, 1,090,314 tested `H` values, and 288,144
necessary-condition survivors (the first 1000 are retained).  The raw artifact
and an independent witness audit are
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98652.json` and
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98652_audit.json`.
This positive pressure result leaves the full H37/port/cap closure open; it is
not evidence for a complete Leech tree.

After excluding the already-used named-J values and edge weights `16,19,35`,
the same Hoffman2 scan was rerun as job `98653` (`n1182`, `COMPLETED`, about
3 seconds).  It reported 533 admissible profiles, 585,234 tested `H` values,
and 127,629 necessary-condition survivors.  The raw result and independent
audit are
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98653.json`
and
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98653_audit.json`.
This is a stricter but still positive pressure result, not a J-32 exclusion.

The strict scan was independently reimplemented without importing the primary
scanner, using an explicit list of the seven rooted one-to-three-edge shapes
and a separate weighted-distance routine.  Hoffman2 job `98657` was run with
the same `h_max=220` bound and matched job `98653` exactly:

```text
profiles by edges: 1 / 28 / 504
admissible profiles: 533
H candidates tested: 585234
survivors found: 127629
```

The artifact is
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_independent_98657.json`
(SHA-256
`f0b235e75f07b2294a62a0f4fb600ddafb60cd7e8fa271bc0eadef7c707993c1`).
The artifact-level comparison is replayed by
`theory-lab/topwindow/verify_pro_b27_port_profile_independent_result.py`,
which returns `VERIFIED_INDEPENDENT_REPLAY_ARTIFACT`.  This upgrades confidence
in the bounded enumeration contract only: the positive survivors still do not
provide a complete H37 forest, port-completeness lemma, global cap, or
Leech-tree embedding.

As a further remote pressure test, the primary scanner was extended to four
edges on Hoffman2 job `98658` (`n1182`, one CPU, 2 GB, low priority).  It found
`1 / 28 / 504 / 7410` admissible profiles by edge count, tested `8,721,414`
`H` candidates, and retained `1,019,466` necessary-condition survivors (the
first 1000 are recorded).  The raw artifact is
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e4_h220_98658.json`
(SHA-256
`1487912627be1b0b6ff2b5a49ab0b9c75ae47b1f9531b8e377c237e431cfccf8`); the
independent witness audit is
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e4_h220_98658_audit.json`
and returns `VERIFIED_REMOTE_ARTIFACT`.  The survivor count remains strongly
positive, so increasing profile depth alone is not closing the J32 branch; the
next useful step is a port-complete multi-component state, not an unbounded
extension of this pressure scan.

The proposed port-depth inequality was then audited with its missing geometric
assumption made explicit.  The replay
`theory-lab/topwindow/verify_pro_b27_port_depth_conditional.py` returns
`VERIFIED_CONDITIONAL_LEMMA`: if a low component is genuinely on the J side
and every path from it to the fixed L core passes through `d6`, then its
deepest cross pair with the fixed depth-28 vertex is exactly
`H+E_C+28`, hence at most `N`.  The same replay gives a small non-separated
attachment showing why that inequality must not be used unconditionally.
Thus the cap interval is now a sound conditional filter, while proving
`d6`-separation and port completeness for every actual component remains open.

The graph-level state interface is now explicit in
`theory-lab/topwindow/verify_pro_b27_port_state_extractor.py`.  After deleting
all edges above 37 from a positive rooted tree, each non-root component has a
unique shallowest vertex `p(C)` and exactly one rootward boundary edge; the
remaining boundary edges point outward.  The extractor records
`(T_C,p(C),sigma,H,E_C)` and flags whether the component is actually
`d6`-separated from the fixed L core.  It returns
`VERIFIED_GRAPH_LEMMA` on the b=27 control tree and an explicit non-separated
attachment.  This supplies the canonical state machinery, but it does not
prove that every FW319 component is J-separated or that the finite port set is
complete.

The extractor is paired with
`theory-lab/topwindow/verify_pro_b27_port_state_combiner.py`, which checks a
restricted multi-component state: each component carries its actual rooted
profile and port depth; all edge weights and internal pair values are unique;
all fixed-L translates are disjoint; component-to-component cross-sums are
distinct and below `N=300`; and the conditional cap is applied.  It returns
`VERIFIED_PORT_STATE_COMBINER` on a positive one-component J-side control,
rejects the named-packet J32 collision, and rejects a deliberately colliding
second port depth.  This is the first executable multi-component interface,
but the positive control omits the forced L owners 5 and 21 and does not model
arbitrary LCAs or gateway orientations.

That conditional filter was applied remotely in Hoffman2 job `98661` with
`max_edges=4`, `h_max=240`, and `N=300`.  The profile partition remained
`1 / 28 / 504 / 7410`, but the cap-aware scan tested `7,613,094` candidates
instead of `8,721,414` and retained `573,864` survivors.  The artifact is
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e4_cap300_98661.json`
(SHA-256
`37bc3ae77b9a9825aa8f6cd750e95d6dd1a2e5f9e49ca0d0d5be4c2e0159367a`), and
`theory-lab/topwindow/verify_pro_b27_port_profile_remote_result.py --job 98661`
returns `VERIFIED_REMOTE_ARTIFACT`.  The cap removes many impossible depths
but leaves a large positive set; it is therefore a validated conditional
filter, not a branch exclusion.

## Restricted two-component replay (Hoffman2 98663 / 98720)

The explicit two-component checker was run on Hoffman2 with the strict J32
profile paired with one generic low-support component.  Job `98663` tested
`29` J32 profiles against `108` generic profiles, for `112,491,139` pairs,
and found zero survivors.  Its raw artifact is
`theory-lab/topwindow/results/pro_b27_two_component_port_states_e2_98663.json`;
the artifact verifier returns `VERIFIED_RESTRICTED_ZERO_ARTIFACT` and reports
SHA-256
`ef92da15265bf4f456698dfc7292241b7892d78ec5b1742c3688a277f24d14c0`.

An optimized pre-screen replay, job `98720`, preserved the exact predicate
but reduced the Cartesian product to `1,951` J32 states times `9,745` generic
states, i.e. `19,012,495` pair tests, again with zero survivors.  The replay
artifact is
`theory-lab/topwindow/results/pro_b27_two_component_port_states_e2_replay_98720.json`
with SHA-256
`c0ee87fbeb400756782ab3f9054ed4c23744cd433dc701f3ac8d849c85b55cf4`.
This is an optimization replay of the same logical checker, not a clean-room
independent proof.  Both zeros are only for the d6-separated two-component
necessary-condition model: they omit the forced L owners 5 and 21, additional
H37 components, shared high Steiner skeletons, arbitrary LCAs/gateways, and
complete-spectrum closure.

## Pro structural correction: shared high skeleton

The latest GPT Pro audit rejects the stronger “each H37 component has an
independent gateway directly to the carrier” picture.  Several low components
may share a high-only Steiner skeleton before reaching the carrier.  The safe
global statement is instead the **Port--Skeleton Compression** observation:
every new edge of weight at most 37 lies in the union of the fourteen unique
owner paths for `H37`, so the low support has at most fourteen new edges; the
remaining high-only part must be represented by a compressed terminal tree.
The minimum falsification extension is to relax exactly one hypothesis in the
current checker: let the J32 component and one generic component share one
high Steiner node, and recompute their cross distances using the two gateway
lengths.  A zero there would support an induction target; a survivor would
identify the missing terminal-metric state.  Neither outcome alone is a
global theorem.

The first falsification run of that relaxation was Hoffman2 job `98722`: one
J32 component and one generic component, each with at most one low edge,
`h<=120`, and one shared high-only Steiner depth `s>=38`.  It tested `221,824`
Steiner placements and found zero survivors.  The artifact
`theory-lab/topwindow/results/pro_b27_shared_steiner_e1_h120_s38_98722.json`
has SHA-256
`3d9d2e8787ea534609878944855d7873aa96734687a23faeb4f1d47fce2e457d`, and
`theory-lab/topwindow/verify_pro_b27_shared_steiner_result.py` returns
`VERIFIED_SHARED_STEINER_ZERO_ARTIFACT`.  This is only a bounded pressure
test; it does not justify an induction step or cover larger components,
multiple Steiner nodes, the forced L owners, or complete-spectrum closure.

## Pro decomposition audit: lossless compressed state (2026-08-28)

The second GPT Pro pass supplied a sharper theorem candidate and corrected the
earlier terminal-only sketch.  Under the exact-return hypotheses that the
fixed core `K` owns every low value in
`[1,37]\\setminus(H37\\cup{4})`, that each `H37` value has a unique owner, and
that every pair distance is at most `N`, let `F` be the union of the fourteen
`H37` owner paths.  Every edge outside `K\\cup F` has weight `>37`: a low edge
would either collide with a fixed owner, equal the forbidden puncture `4`, or
be the unique owner edge for an `H37` value and hence lie in `F`.  This gives at
most fourteen new low edges and at most twenty-eight incident new vertices.

The remaining high-only part can be compressed by retaining all vertices
outside `K\\cup F` of degree other than two, suppressing maximal degree-two
paths, and recording each suppressed path as the **ordered tuple** of its
original edge weights, together with its exact incidences in `K\\cup F` and
the rooted orientation.  High edges inject into `{38,...,N}`, so there are at
most `N-37` of them and each compressed arc has at most `floor(N/38)` entries.
The resulting state is finite and reconstructs all intermediate vertices,
edge distances, LCAs, gateway orientations, and fixed-core cross distances.

The machine replay
`theory-lab/topwindow/verify_pro_b27_port_skeleton_compression.py` returns
`VERIFIED_CONDITIONAL_DECOMPOSITION_LEMMA`.  It explicitly distinguishes the
same terminal length represented by `(101)` and `(48,53)`: storing only the
sum would lose the realized pair values `48` and `53` and can change collision
and owner data.  This converts the Pro proposal into a sound conditional
state lemma, but not into a global exclusion.

The remaining `GAP` is the enumeration/closure step: the project still has no
complete implementation over all incidence-level ports, all compressed high
skeleton topologies and ordered edge tuples, the forced L owners `5` and `21`,
and the complete-spectrum, least-remote, and inherited-descent obligations.
The current two-component and one-Steiner zeros remain strict bounded models.

The representation itself has also been checked by a round-trip audit in
`theory-lab/topwindow/verify_pro_b27_port_skeleton_roundtrip.py`, returning
`VERIFIED_CONDITIONAL_COMPRESSION_ROUNDTRIP`.  On a supplied tree containing
two high-only branches, it preserves endpoint incidences and ordered edge
tuples, reconstructs all suppressed vertices, and reproduces the complete
sorted pair-distance table exactly.  This closes a representation bug-risk
but does not establish completeness of the FW319 attachment-state catalogue.

The incidence interface has now been audited separately by
`theory-lab/topwindow/verify_pro_b27_multi_port_interface.py`, returning
`VERIFIED_MULTI_PORT_INTERFACE`.  A low component with internal edge `32`
was given one rootward gateway and two outward high gateways from a different
internal vertex.  The extracted state records all three incidences, not just
the rootward port.  High-only singleton pieces are correctly left to the
compressed skeleton rather than misclassified as low components.  This closes
another state-representation ambiguity; it does not enumerate the possible
incidence patterns.

## Ordered high-arc control (Hoffman2 98771)

To test the newly identified lossless state variable, a narrow exact-distance
pressure scan was implemented with one shared high Steiner vertex, one-edge
J32 and generic low components, and exactly one gateway represented by an
ordered pair of high edge weights.  All contiguous sums on the stem and
gateway paths, all fixed-core/named translations to retained path vertices,
low-component-to-gateway distances, and shared-Steiner cross distances were
included in the collision table.  The other gateway remained a one-edge
control branch.

Hoffman2 job `98771` (`h_max=150`, one CPU, 2 GB, low priority) tested
`9,287,808` candidates and found zero survivors.  The artifact is
`theory-lab/topwindow/results/pro_b27_ordered_arc_h150_98771.json` with
SHA-256
`4dca8012cf37f099f1dccedb7257d6eb7c34df837553d1e4517450961f96ec85`;
`theory-lab/topwindow/verify_pro_b27_ordered_arc_result.py` returns
`VERIFIED_ORDERED_ARC_ZERO_ARTIFACT`.

This result is a useful bounded pressure check, not a theorem: the model has
only one shared Steiner, one-edge low components, a simplified fixed/named
attachment, and one split gateway.  It does not enumerate all incidence-level
ports, arbitrary high skeletons, forced L owners `5,21`, or complete-spectrum,
least-remote, and inherited-descent closure.

## Multi-port outward-gateway control (Hoffman2 98772)

The incidence-level interface was next exercised on a J32 component with one
direct rootward gateway and two outward high gateways attached at the internal
32-edge endpoint.  For every candidate `(H,a,b)`, the checker includes the
root-to-component distances, the two outward-edge distances, their sums, all
component-to-fixed and component-to-named translations, and the outward-leaf
cross distance.  Hoffman2 job `98772` (`h_max=150`, outward edge bound `180`)
tested `1,147,289` candidates and found zero survivors.

The artifact is
`theory-lab/topwindow/results/pro_b27_multi_port_h150_e180_98772.json` with
SHA-256
`c8b49c76adc4399cedff7fceb350177e57eaf649b67724e848e93ebb7125f10f`;
`theory-lab/topwindow/verify_pro_b27_multi_port_result.py` returns
`VERIFIED_MULTI_PORT_ZERO_ARTIFACT`.

This is a bounded necessary-condition control only.  It does not cover
multiple low components, shared multi-Steiner skeletons, arbitrary port
incidences, forced L owners `5,21`, or complete-spectrum closure.

## Shared multi-port two-component control (Hoffman2 98773)

The next finite relaxation combined both structural features: a J32 component
and one generic H37 component share a high Steiner node, and each low
component has one outward high leaf attached to its internal low-edge
endpoint.  The fragment checker constructs the full pair-distance table of
the seven-vertex skeleton, then checks fixed-core and named translations.
Using the explicit high-edge pool
`{43,44,45,46,47,48,49,51,52,53}`, Hoffman2 job `98773` tested `241,920`
assignments and found zero survivors.

The artifact is
`theory-lab/topwindow/results/pro_b27_shared_multiport_pool10_98773.json` with
SHA-256
`8a9f434e8c4c1f0fa2ede5c997cca5f01bbf370bccc36a118ea91be40ed4e1c1`;
`theory-lab/topwindow/verify_pro_b27_shared_multiport_result.py` returns
`VERIFIED_SHARED_MULTIPORT_ZERO_ARTIFACT`.

This is stronger pressure than the one-Steiner or one-component controls, but
still a finite fragment only: arbitrary high weights, larger low forests,
multiple Steiner nodes, all incidence patterns, forced L owners `5,21`, and
complete-spectrum/least-remote/descent closure remain open.

### Audit correction

The first run (`98773`) had a checker bug: it re-added root-to-vertex depths
that were already present in its full fragment pair table, so its zero could
have been a trivial duplicate rejection.  It is superseded and must not be
used as evidence.  The corrected code was rerun as Hoffman2 job `98774`; it
again tested `241,920` assignments and found zero survivors.  The corrected
artifact is
`theory-lab/topwindow/results/pro_b27_shared_multiport_pool10_fix1_98774.json`
with SHA-256
`8a9f434e8c4c1f0fa2ede5c997cca5f01bbf370bccc36a118ea91be40ed4e1c1`, and
`theory-lab/topwindow/verify_pro_b27_shared_multiport_result.py` now returns
`VERIFIED_SHARED_MULTIPORT_ZERO_REPLAY_ARTIFACT` for this corrected run.

The state layer is also composable in
`theory-lab/topwindow/verify_pro_b27_composed_skeleton_state.py`, returning
`VERIFIED_COMPOSABLE_SKELETON_STATE`.  A two-component state with three
outward incidences and three shared-skeleton arcs expands to a 36-entry pair
table with no duplicate distances; replacing an ordered arc `(48,53)` by the
same-sum single edge `(101)` produces a distinct canonical state.  This is an
interface/round-trip result, not a completeness or nonexistence theorem.

The rooted incidence fact behind that state has an independent finite replay
in `theory-lab/topwindow/verify_pro_b27_port_incidence_exhaustive.py`, returning
`VERIFIED_PORT_INCIDENCE_EXHAUSTIVE_REPLAY`.  It checks all `18,248` labelled
tree topologies on two through seven vertices, across seven low/high
thresholds (`61,463` nontrivial low components).  In every case the unique
shallowest vertex has the sole rootward boundary edge and every other boundary
edge is outward.  This is consistent with the direct general rooted-tree
argument, but it does not by itself enumerate the FW319 skeleton states.

The general argument is short and is now part of the proof state.  Let `C` be
a connected component after deleting all edges above `37`, and root the full
tree at the carrier.  The exact-return condition makes all root distances
distinct, so `C` has a unique shallowest vertex `p`.  The unique path from the
root to any vertex of `C` enters `C` first at `p`; once inside, it cannot leave
and later re-enter `C`, since that would give a second route between two
vertices of the tree.  Hence the boundary edge at `p` is the only edge directed
toward the root.  Every other boundary edge leads to a component not
containing the root and is therefore directed outward.  Thus the incidence
fields recorded by the state interface are necessary for every genuine tree,
not an artefact of the small replay.

## Remaining-vertex budget

The canonical J-single-edge-32 branch already contains 15 distinct vertices:
eight in the fixed L factor, one for the realized 34-owner, and six in the
named J packet plus the single 32-edge.  Since the first open order is
`n=25`, every completion of this branch has at most ten additional vertices
available for all remaining H37 support and the compressed high skeleton.
This count is independently replayed by
`theory-lab/topwindow/verify_pro_b27_vertex_budget.py`, returning
`VERIFIED_VERTEX_BUDGET`.  It is now a hard input bound for any complete-state
topology generator, although it does not determine the attachments or close
the full spectrum.

## Pure-high Steiner-chain falsification control (Hoffman2 98775)

The external Pro audit identified a precise remaining finiteness gap: the ten
new-vertex budget does not by itself exclude a chain of high-only Steiner
vertices that is not incident to a low-component boundary.  Its proposed
canonical state is `(F,K,Pi,T_H,omega)`, where `F` is the H37 support forest,
`K` the fixed core, `Pi` the rootward incidence of each low component, `T_H`
the compressed high skeleton, and `omega` the ordered edge tuple on every
compressed arc.  The first falsification check is therefore the smallest such
relaxation: two consecutive degree-three pure-high vertices.

That control is implemented in
`theory-lab/topwindow/enumerate_pro_b27_pure_high_chain_control.py`.  Its
fragment is `r--S2--S1`, with one high carrier leaf at `S2` and two high
gateway edges from `S1` to a J32 component and one generic H37 component.
Thus both `S1` and `S2` are degree three and neither is a low-edge boundary.
The complete fragment pair table and all fixed-core/named translations are
checked without re-adding root depths.  The finite Hoffman2 job `98775` uses
the explicit twelve-value high pool
`{43,44,45,46,47,48,49,51,52,53,56,58}` and all eight generic low values.

Hoffman2 job `98775` completed normally in 22 seconds and tested the expected
`8 * 12P5 = 760,320` candidate assignments; it found zero survivors.  The
artifact is
`theory-lab/topwindow/results/pro_b27_pure_high_chain_pool12_98775.json` with
SHA-256
`637114a90630e5dfef13fee4edfd760743fd84e507745aa53ac4a1ace7a3cbde`, and
`theory-lab/topwindow/verify_pro_b27_pure_high_chain_result.py` returns
`VERIFIED_PURE_HIGH_CHAIN_ZERO_ARTIFACT`.  This is **OBSERVED bounded
pressure**, not a theorem: arbitrary high weights, other skeleton topologies,
larger low forests, forced L owners `5,21`, and complete-spectrum,
least-remote, and inherited-descent closure remain open.  A survivor in a
broader pool or topology would still redirect the structural lemma.

The Pro follow-up proposes the theorem-level target **Pure-High Chain
Contraction Lemma**: in a least-remote minimal counterexample, a maximal path
whose internal vertices are degree-three, all incident edges are `>37`, and
which has no low-support attachment should have at most one internal Steiner
vertex.  The intended move is to contract an outermost vertex while replacing
the ordered pair `(a,b)` by `(a+b)`, preserving the low incidences.  The
unproved implication is whether side-branch distances and exact-return
ownership survive that contraction; this is a structural **GAP**, not settled
by the bounded zero above.

## Three-pure-high-Steiner-chain control (Hoffman2 98776)

The smallest next topology for testing that contraction target is
`r--S3--S2--S1`, with a high carrier leaf at `S3`, a high gateway to a generic
H37 component at `S2`, and a high J32 gateway plus a high side leaf at `S1`.
All three `S_i` have degree three and every chain, side, and gateway edge is
`>37`; the only low edges are the J32 edge `32` and one generic H37 value.
This uses nine non-root fragment vertices, within the ten-vertex residual
budget.

The control is implemented in
`theory-lab/topwindow/enumerate_pro_b27_three_pure_high_chain_control.py`, with
an exact full fragment distance table and fixed-core/named translation checks.
Hoffman2 job `98776` completed normally in 2 minutes 43 seconds and tested the
expected `8 * 10P7 = 4,838,400` candidate assignments; it found zero survivors.
The artifact is
`theory-lab/topwindow/results/pro_b27_three_pure_high_chain_pool10_98776.json`
with SHA-256
`612447396040b227bb7140ca3167db1e041683d2817b00ebc53a44f89c2a743c`, and
`theory-lab/topwindow/verify_pro_b27_three_pure_high_chain_result.py` returns
`VERIFIED_THREE_PURE_HIGH_CHAIN_ARTIFACT`.  This is still only bounded
pressure: it does not prove the contraction lemma or cover other skeletons,
high weights, the forced L owners, or complete-spectrum closure.

## Contraction-scope audit

The proposed contraction must be kept at the level of the compressed-state
interface.  The exact replay
`theory-lab/topwindow/verify_pro_b27_terminal_metric_contraction.py` returns
`VERIFIED_TERMINAL_METRIC_CONTRACTION_CONDITIONED`: replacing a terminal-free
ordered high interval by its total weight preserves every distance between
explicitly marked attachment terminals, provided no low-support path traverses
that interval.  It does **not** preserve the full pair-distance multiset, since
the suppressed vertices remain genuine vertices and realize their own pair
distances.  The replay also gives an endpoint-only counterexample: the same
endpoint total `144` can place a side attachment at distances `103` or `151`
from the root endpoint.  Therefore every attachment incidence must be marked
as a terminal before any state contraction, while the ordered arc tuple must
still be retained for spectrum/ownership checks.  The missing owner-transfer
or minimality theorem remains **GAP**; no contraction-based global exclusion
is claimed.

## Rooted residual-skeleton topology catalogue

To make the finite-state route concrete, the light-weight audit
`theory-lab/topwindow/verify_pro_b27_residual_skeleton_catalogue.py` enumerates
all non-isomorphic free trees of orders `1,...,10`, roots each at every vertex,
and deduplicates them by a canonical rooted code.  It returns
`VERIFIED_ROOTED_SKELETON_CATALOGUE`, with free-tree counts
`1,1,1,2,3,6,11,23,47,106` and rooted counts
`1,1,2,4,9,20,48,115,286,719` (1,205 rooted codes in total).  Thus the
unmarked topology layer is genuinely finite under the current ten-vertex
budget.  Incidence markings, ordered high-edge tuples, admissible weights, and
the complete fixed-core/spectrum checks are still separate layers and remain
open; this catalogue is not itself an exhaustive Leech-tree enumeration.

The first marked layer is also frozen by
`theory-lab/topwindow/verify_pro_b27_marked_skeleton_catalogue.py`.  Assigning
two labelled incidences (`rootward`, `outward`) to arbitrary skeleton vertices
and quotienting by rooted automorphisms gives
`VERIFIED_MARKED_SKELETON_CATALOGUE`: 71,259 canonical marked states through
ten vertices, including 48,426 at order ten.  This confirms that incidence
marking is finite once the residual vertex budget is fixed.  It is deliberately
only a two-token layer; arbitrary multi-port low components, ordered arc
tuples, and the full spectrum still require the next enumerator.

## Full high-edge-domain CP-SAT control (Hoffman2 98777)

To remove the finite-pool limitation for the first pure-high chain, the
two-Steiner fragment was encoded as an exact CP-SAT feasibility model.  Each
of its five high edges ranges over the complete integer domain `38..300`, all
fragment pair distances are constrained to be distinct and outside the fixed
occupied set, and every fixed-core/named translation of a non-root fragment
vertex is included in the same all-different table.  The expression layer was
independently replayed against a direct weighted-tree distance calculation.

Hoffman2 job `98777` completed normally in four seconds.  For all eight
generic low values `{18,20,24,25,26,34,36,37}`, CP-SAT returned
`INFEASIBLE` (no time-limit `UNKNOWN` rows).  The artifact is
`theory-lab/topwindow/results/pro_b27_pure_high_chain_cpsat_98777.json` with
SHA-256
`fe9b32e62e101893f423f5bd91392079c90bb4e0299cbd70b3683de78e0b68f9`, and
`theory-lab/topwindow/verify_pro_b27_pure_high_chain_cpsat_result.py` returns
`VERIFIED_PURE_HIGH_CHAIN_CPSAT_INFEASIBLE`.  This is a complete zero only
for that finite two-Steiner necessary-condition fragment; it does not close
other skeletons, low forests, forced L owners, or the global spectrum.

## Full high-edge-domain three-Steiner CP-SAT control (Hoffman2 98778)

Following the Pro recommendation, the three-Steiner topology was then encoded
over the full high-edge domain rather than the ten-value pool.  The model has
seven high variables in `38..300`, one generic low value in each of the eight
allowed cases, and explicitly covers all 45 unordered pairs of the ten
fragment vertices.  It also models all 90 translations of the nine non-root
vertices by the seven fixed-core depths and three named offsets, for 135
distance variables in one `AllDifferent` table.  A direct weighted-tree replay
checked the generated linear path expressions before submission.

Hoffman2 job `98778` completed normally in ten seconds.  Every generic-low row
returned `INFEASIBLE`, with no time-limit `UNKNOWN`.  The artifact is
`theory-lab/topwindow/results/pro_b27_three_pure_high_chain_cpsat_98778.json`
with SHA-256
`9ea7837698d41476c5400760e439f57775e3cb562e871ae6d5a0f405a448c088`, and
`theory-lab/topwindow/verify_pro_b27_three_pure_high_chain_cpsat_result.py`
returns `VERIFIED_THREE_PURE_HIGH_CHAIN_CPSAT_INFEASIBLE`.  This is a complete
zero for the specified three-Steiner necessary-condition fragment, not a
global b=27 closure; other rooted skeletons, multi-port low forests, forced L
owners, and complete-spectrum/descent obligations remain open.

## Incidence-partition route and subdivision correction

With both short pure-high-chain families excluded over the full edge domain,
the Pro consultant recommends switching from chain length to an
**Incidence-Partition Finite Model**: a rooted skeleton type `tau` (among the
1,205 audited types), a port map `pi` from each low component to a skeleton
vertex, outward-incidence multiplicities, and one ordered high-edge variable
per skeleton arc.  The sound pair-coverage set must include skeleton--skeleton,
skeleton--low-endpoint, skeleton--fixed-core, low-endpoint--fixed-core,
low-endpoint--low-endpoint, and named-carrier pairs.  Whether `(tau,pi)` is
complete without retaining unmarked high-branch internals is still **GAP**.

The suggested first check was audited by
`theory-lab/topwindow/verify_pro_b27_outward_subdivision.py`, returning
`VERIFIED_SUBDIVISION_COUNTEREXAMPLE`.  A high edge of total `100` and its
split `(48,52)` have the same endpoint metric but different realized pair
values; the even smaller `(38,38)` split introduces the named value `38`.
Thus an unmarked outward branch is not subdivision-invariant at full-spectrum
level.  Any incidence-partition model must retain the ordered tuple (or an
equivalent internal pair-state); the next implementation target is therefore
an incidence-marked, ordered-arc CP-SAT model with an explicit all-pair
coverage audit, not a total-length-only compression.

## Full-domain shared multi-port CP-SAT control (Hoffman2 98779)

The first multi-component incidence test was then encoded as a full-domain
shared-Steiner fragment.  A single high Steiner vertex carries both a J32
component and a generic one-edge H37 component, with one rootward and one
outward gateway per component.  All five high-edge variables range over every
integer in `38..300`; the eight generic-low cases are the same allowed set as
the preceding controls.  The model contains all 28 unordered pairs of its
eight fragment vertices and all 70 fixed-core/named translations of the seven
non-root vertices, for 98 variables in one `AllDifferent` table.  The linear
distance expressions were independently replayed against a direct weighted
tree calculation before submission.

Hoffman2 job `98779` completed normally in three seconds.  Every generic-low
row returned `INFEASIBLE`, with no time-limit `UNKNOWN`.  The artifact is
`theory-lab/topwindow/results/pro_b27_shared_multiport_cpsat_98779.json` with
SHA-256
`cef6ffd1672693263757b45ea29aa6b17aa78c5cabb73d1c73d156108cf91e7d`, and
`theory-lab/topwindow/verify_pro_b27_shared_multiport_cpsat_result.py` returns
`VERIFIED_SHARED_MULTIPORT_CPSAT_INFEASIBLE`.  This is a complete zero only
for the specified shared-Steiner necessary-condition fragment; it does not
cover arbitrary rooted skeletons, larger low forests, forced L owners, or the
global spectrum/descent closure.

## Port-minimal route (candidate, not yet certified)

The next Pro-guided route is to stratify the 1,205 rooted skeletons by the
number of independent low ports, beginning with exactly two low components and
arbitrary port placements.  A sound state must retain `(tau, Pi, E)` together
with every ordered high-arc tuple: `tau` is the rooted skeleton, `Pi` assigns
each low component's rootward port, and `E` records the ordered high weights.
For each concrete state, the coverage invariant is the complete set of
unordered pairs on
`V* = V(fixed core) union V(all low components) union V(skeleton)`, including
skeleton--skeleton, skeleton--low, skeleton--fixed, cross-component low--low,
and low--fixed pairs.  Any reduced state that omits one of these pairs is not a
valid exclusion model.

The first unsupported implication is that unmarked outward high branches can
be deleted or normalized without changing this full pair spectrum; the
subdivision counterexample above shows that total-length compression is not
sound.  Therefore the first falsification experiment must be a two-port,
full-domain CP-SAT model with an independent pair-list audit, run on Hoffman2.
Until that model or a structural replacement is verified, the port-minimal
reduction remains **CANDIDATE** and the global closure remains **GAP**.

## Shared `L(5,21)` / `J(32)` label-state control (Hoffman2 98793/98794)

The first Hoffman2 run (`98793`) covered the full 16,420-row order-five family
and was independently replayed as all-infeasible, but its shared `FWD/REV`
rows lack the current explicit `EXPLICIT_NAMED_16_RESERVATION` route.  It is
kept as a legacy comparison only, not as a current-version reproduction.
The current-hash rerun is job `98794`; its completed artifact below supersedes
`98793` for current-version evidence.

For reference, the legacy artifact is
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_98793.json` with
SHA-256
`73783a6c576004ac01b440f1268e6426a5a425f39c2df5bcab4d3f013d8a1881`.
Both runs concern only the finite one-gateway/shared-path/one-outward-leaf
family and cannot prove attachment/LCA completeness, arbitrary outward high
subtrees, or global `b=27` nonexistence; any `UNKNOWN` row is uncovered rather
than `INFEASIBLE`.

The current source was independently executed on the Geo workstation (PID
`2195208`).  Its artifact
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_geo.json` has
SHA-256
`2ebe11ba5e6166c6c2d9320a7b0221e6b658017f67682c92c71d439ad4efe9cb` and the
independent verifier returns both
`VERIFIED_L521_J32_LABEL_STATE_CPSAT_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY` for all 16,420 rows.  Hoffman2 job `98794`
completed with the same current source and verifier.  Its artifact
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_98794.json` has
SHA-256
`0975222739cc8bebe57ebdb0345735c34f7baf2156e088f56aa5209979545492`.
After dropping wall-time fields, the two current-source artifacts have exactly
the same 16,420 row semantics (canonical row SHA-256
`3a266f03916f9f73e5117350013eca1ee8430b6910ed37ae43c28af463091c7f`).
Neither result changes the finite claim boundary above.

The first attachment/LCA falsification model was then run on Hoffman2 job
`98802`.  For the order-one rooted skeleton it enumerated both endpoints as
the rootward attachment for each of the three low components, one optional
outward high leaf at each exposed endpoint, all shared-path attachments and
side masks, and both J32 endpoint attachments.  It tested 896 rows: 512
`EDGE`, 192 `FWD`, and 192 `REV`; every row was `INFEASIBLE` with no
`UNKNOWN`.  The artifact
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_98802.json`
has SHA-256
`26cfb6651e95480f225a52fa2c4aa4f77e266ce041cc272f6355862172aece6d`.
Its independent verifier returns
`VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  This is a finite order-one state-class
exclusion only; arbitrary high Steiner subtrees, richer incidences, higher
skeletons, and the Label-State Completeness Lemma remain `GAP`.

The first order-two run (`98803`) was rejected by the independent verifier:
an indentation error duplicated the FWD/REV loop under the EDGE port loop,
producing 17,280 rather than 6,528 intended rows.  Its raw artifact is kept
only as a superseded provenance record (SHA-256
`eccbfab442bdb2fe7408b227a670e9400e327747b51d7b34334fd4c742702c3c`).  The
enumerator was corrected in commit `f1c408a`, and job `98804` is the current
replacement.

The corrected order-two artifact from job `98804` contains the intended 6,528
rows (4,608 `EDGE`, 960 `FWD`, 960 `REV`).  Independent replay verifies its
graph/owner layer; solver statuses are `6,072 INFEASIBLE` and `456 UNKNOWN`,
with no `FEASIBLE` row.  Every unknown is the order-two path skeleton with
all three EDGE ports at the internal vertex, so this is a mixed finite result,
not a zero.  The artifact
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order2_98804.json`
has SHA-256
`94db8144a54dd4ea82dec5d3d4ac22d2311739f83623a98e960cf848c2b62f7f` and the
verifier returns `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` plus
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  Targeted rerun job `98805` is resolving
only those 456 unknown rows; they must remain uncovered until a definitive
solver status is obtained.

Hoffman2 job `98805` resolved all 456 rows at the five-second per-row limit:
the rerun artifact
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order2_unknown_rerun_98805.json`
has SHA-256
`7ad697156ffd4afecb07389ebf80662c3184e55397c477bc5b8a59058da31d0c` and
contains 6,528/6,528 `INFEASIBLE` rows with no `UNKNOWN` or `FEASIBLE` rows.
The independent verifier returns
`VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` plus
`VERIFIED_INDEPENDENT_BFS_REPLAY`; only solver-status/time/statistic fields
differ from the mixed input artifact.  This verifies the order-two finite
state-class exclusion, not the global Label-State Completeness Lemma.

The Pro-directed J32 outward-depth extension was run on Hoffman2 job `98806`.
Each J32 endpoint independently chose `NONE`, a two-edge high path (`PATH2`),
or a two-leaf high fork (`FORK2`), while all previous attachment variables and
complete pair coverage were retained.  The order-one run covered 2,016 rows
(`1,152` `EDGE`, `432` `FWD`, `432` `REV`); all were `INFEASIBLE` with no
`UNKNOWN`.  The artifact
`theory-lab/topwindow/results/pro_b27_j32_outward_deeper_98806.json` has
SHA-256
`7849c9b68cfb9b7cd08bb792c3089dbe9360110a3fc4943c96bd4f27f401f754`, and its
independent verifier returns `VERIFIED_J32_OUTWARD_DEEPER_ARTIFACT` plus
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  This remains a finite order-one control;
longer high paths, larger forks, arbitrary Steiner skeletons, and the global
completeness bridge are still `GAP`.

Following that zero, the order-two extension was submitted to Hoffman2 as
job `98807` via `scripts/hoffman2_j32_outward_deeper_order2_slurm.sh` with
`--max-order 2 --time-limit 0.20`.  It is a single `campus24` CPU job; the
first queue check showed `RUNNING` on `n1183`.  The intended family has 14,688
rows (`10,368` `EDGE`, `2,160` `FWD`, `2,160` `REV`, from the current loop
bounds).  This is an active
computation, not yet evidence: the output must be retrieved, checked for
complete row coverage and `UNKNOWN`, and independently replayed before any
status is promoted.

The retrieved initial artifact has SHA-256
`06cab8427ec5ac85c7377f6a1702f29cb2ca161b0d96e1c8c1653c7bb675bd9e` and
passes the independent graph/BFS replay.  Its exact solver status is 13,608
`INFEASIBLE` and 1,080 `UNKNOWN`, with no `FEASIBLE`; all UNKNOWN rows are the
order-two path skeleton `(())` with all three low ports at its internal
vertex.  Job `98808` reran precisely those rows at five seconds per row.  The
final artifact has SHA-256
`5a11a3ac5fbe95d2d176057257bbb320b904513e20a641e2a3b4f6b03d3aee01`, passes
the same independent verifier, and has 14,688/14,688 `INFEASIBLE` with zero
`UNKNOWN` or `FEASIBLE`.  Non-UNKNOWN rows are unchanged; replaced rows only
change status and wall-time fields.  This is a finite nine-mode order-two
closure, not a global completeness theorem.

## Two-port rooted-skeleton falsification control (Hoffman2 98782)

The first concrete port-minimal experiment covers every rooted skeleton type
through order four: `1+1+2+4 = 8` rooted types, with both low ports allowed at
every ordered pair of skeleton vertices (87 states total).  Each component is
represented conservatively by a rootward high gateway, one low edge (J32 uses
32; the second uses a generic value from `{18,20,24,25,26,34,36,37}`), and an
outward high leaf.  In every state all high edges range over the full integer
domain `38..300`; the generic low edge is a domain variable and edge labels are
kept distinct.

For each state, the model places every unordered pair of every concrete
fragment vertex in one `AllDifferent` table, together with every non-root
vertex translated by the seven nonzero `B0` depths and the three named
offsets.  The largest states have ten fragment vertices, 45 fragment pairs,
90 translation variables, and hence 135 all-different distance variables.
The symbolic path expressions were independently replayed by a weighted-tree BFS in
`theory-lab/topwindow/verify_pro_b27_two_port_skeleton_cpsat_result.py`.

Hoffman2 job `98782` completed normally in five seconds.  All 87 states were
`INFEASIBLE` with no `UNKNOWN` rows.  The artifact is
`theory-lab/topwindow/results/pro_b27_two_port_skeleton_cpsat_98782.json` with
SHA-256
`93297df7014146a22861fb80fc52c3fe32ed037d4898a81ee5cddbc2456f02cc`, and the
verifier returns `VERIFIED_TWO_PORT_SKELETON_CPSAT_ARTIFACT` together with
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  This is a finite falsification result for
the stated order-four, one-low-edge-per-component model only; it is not a
global two-port theorem.  Larger skeletons, richer low-component interiors,
forced L owners, arbitrary outward branch states, and least-remote/descent
closure remain **GAP**.

## Two-port rooted-skeleton order-five extension (Hoffman2 98783)

The same complete model was extended one order further without changing its
state semantics.  It covers all 17 rooted skeleton types through order five
(`1+1+2+4+9`), every ordered pair of ports, and 312 states.  In the largest
states there are 11 fragment vertices, 55 fragment pairs, 100 translations,
and 155 all-different variables; high edges still range over the full domain
`38..300`, with one J32 low edge and one generic low edge per state.

Hoffman2 job `98783` completed normally in nine seconds.  All 312 states were
`INFEASIBLE`, with no `UNKNOWN`.  The artifact is
`theory-lab/topwindow/results/pro_b27_two_port_skeleton_order5_98783.json`
with SHA-256
`be600d741416766200fd6c936e0bc7ed77f35d5183957a2500d78246afee490e`, and the
same verifier returns `VERIFIED_TWO_PORT_SKELETON_CPSAT_ARTIFACT` plus an
independent BFS expression replay.  This closes only the stated simplified
one-low-edge-per-component model through skeleton order five; richer low
components, higher skeletons, forced L owners, and global closure remain
**GAP**.

## Ordered-arc spectrum falsification (Hoffman2 98784)

The Pro-revised canonical state retains each high arc's real internal vertices
and its ordered edge-weight tuple.  To test the first possible ambiguity, the
light-weight control
`theory-lab/topwindow/verify_pro_b27_ordered_arc_spectrum.py` used all 17
rooted skeleton types through order five, every ordered pair of low ports, and
each skeleton arc.  It inserted one actual internal high vertex on the chosen
arc and tested all 624 ordered pairs from the admissible finite pool
`{43,...,70}` after removing occupied/named values (24 values, 624 ordered
tuples per arc-state group).

For every state it computed, by an independent weighted-tree BFS, the complete
multiset of all fragment unordered-pair distances—including the inserted
vertex—and every non-root depth translated by the seven nonzero `B0` depths and
three named offsets.  Across 1,132 arc-state groups and 624,864 ordered
tuples, no two distinct tuples on the same arc produced the same spectrum.
The artifact is
`theory-lab/topwindow/results/pro_b27_ordered_arc_spectrum_98784.json` with
SHA-256
`78e80da58e93cd3cbaaa9fd9bcb6386feccdca87e451194e6cbb0103105bd1cd`, and
`theory-lab/topwindow/verify_pro_b27_ordered_arc_spectrum_result.py` returns
`VERIFIED_ORDERED_ARC_SPECTRUM_ARTIFACT` with raw status
`OBSERVED_ORDERED_ARC_NO_DUPLICATE_IN_POOL`.

This supports, but does not prove, uniqueness of the ordered-arc state: it
uses one subdivision, a finite weight pool, and the simplified two-component
fragment.  Multiple subdivisions, richer low components, the full high domain,
and global least-remote/descent closure remain **GAP**.

## Marked high-branch skeleton partition audit

The Pro completeness discussion isolates one purely graph-theoretic point:
after deleting low edges, mark the root, every vertex whose high-subgraph
degree is not two, and every degree-two vertex carrying a low/fixed incidence.
Each remaining maximal path has unmarked degree-two interior and is an ordered
arc.  The independent audit
`theory-lab/topwindow/verify_pro_b27_high_branch_skeleton_partition.py` checks
the path construction, edge partition, and pairwise disjointness of arc
interiors for all rooted instances of all free trees through order ten
(1,809 rooted instances), with every subset of degree-two vertices promoted to
an incidence mark (22,515 marked instances; 143,654 arcs checked).

The artifact is
`theory-lab/topwindow/results/pro_b27_high_branch_skeleton_partition_20260828.json`
with SHA-256
`f1e9b168fbfa518d4b8edf2f1b6f200ab27723b5389bd238cc5541856a76784a`, and
`theory-lab/topwindow/verify_pro_b27_high_branch_skeleton_partition_result.py`
returns `VERIFIED_HIGH_BRANCH_SKELETON_PARTITION_ARTIFACT`.  Thus two ordered
arcs cannot secretly share an internal high vertex: such a vertex is a
branching terminal and belongs in the skeleton.  This removes one specific
topological ambiguity in the proposed
`(tau, Pi, Gamma, Omega)` state, but it is not a labeling proof; bounds on the
number of skeleton vertices, completeness of low/fixed incidence marks, and
the global least-remote/descent argument remain **GAP**.

## Port-complete state lemma

The remaining port interface has now been isolated as a general tree theorem,
not merely an order-ten computation. For a rooted tree whose edges are
partitioned into low and high, contract each connected low component. The
quotient is a tree, so every non-root low component has exactly one rootward
high boundary edge and hence one canonical port `p(C)`. Recording the rooted
internal low tree, `p(C)`, the carrier tag, the rooted high quotient, and both
endpoint incidences of every high edge reconstructs the original rooted
edge-coloured tree edge-for-edge. Consequently every LCA and weighted pair
distance is recovered from the reconstructed tree; no abstract LCA field is
needed.

The exact depth identity is `d_T(r,x)=H(C)+d_C(p(C),x)` for `x` in a low
component `C`. For cross-component pairs, the path may exit through a
child-side boundary vertex rather than `p(C)`; all high-edge endpoint
incidences are therefore essential. This distinction is independently
replayed by
`theory-lab/topwindow/verify_pro_b27_port_depth_decomposition.py`, which
returns `VERIFIED_PORT_DEPTH_DECOMPOSITION` through labelled order five.

The proof and exact scope are recorded in
`docs/pro-b27-port-complete-state-lemma.md` as
`VERIFIED_PORT_DECOMPOSITION_LEMMA`. The finite order-ten round-trip
(`98813`) and the independent labelled Prüfer replay through order six remain
implementation evidence for this interface. This theorem closes only the pure
port/reconstruction implication. It does **not** prove that the represented
states cover every allowed low-support or fixed-incidence decomposition, nor
does it close complete-spectrum reception, least-remote/minimality, inherited
descent, or the residual `L32`/`J32` branches.

The same note records an unrestricted ordered-high-arc corollary: after the
root, high-degree vertices, and low/fixed-incidence degree-two vertices are
marked, maximal paths through the remaining degree-two vertices are a
pairwise interior-disjoint partition of the high edges. The finite high-branch
audit is therefore an implementation check of a general path-compression
fact, while bounds on the compressed skeleton and all spectral constraints
remain separate obligations.

## Three-port marked skeleton catalogue (Hoffman2 98812)

The topology-only completeness input was extended from two incidence marks to
three labelled locations, `L5`, `L21`, and `J32`, on every rooted residual tree
of orders one through ten.  Hoffman2 job `98812` returned
`VERIFIED_MARKED_SKELETON_CATALOGUE_3PORT`.  The artifact is
`theory-lab/topwindow/results/pro_b27_marked_skeleton_3port_98812.json` with
SHA-256
`d80feac9332a3732037d1607f0904fd70bec06a3180a8e3ea5e7499141e2f834`.
It contains `601832` canonical marked rooted states; the per-order counts are
`1,8,41,179,718,2731,10009,35692,124616,427837`.

This freezes only the finite three-port topology layer.  Low-component shapes,
ordered high-edge tuples, admissible weights, complete pair distances, and
complete-spectrum closure are not enumerated, so the Label-State Completeness
bridge and global nonexistence claim remain open.

The companion structural audit `98813` then combined low-component port
extraction with high-skeleton endpoint retention.  Across every rooted free
tree through order ten and every low/high edge partition it checked one
rootward port per non-root low component, retained every high boundary
incidence, and reconstructed the identical rooted edge-coloured tree.  The
artifact
`theory-lab/topwindow/results/pro_b27_low_component_port_skeleton_roundtrip_98813.json`
has SHA-256
`485640a1b630e95c05187c04fd85b66a46f22d9981824b939f23a8310cfc4d57` and reports
`VERIFIED_LOW_COMPONENT_PORT_SKELETON_ROUNDTRIP` for `680961` partitions,
`3657039` component records, and `2976078` high-edge incidences.  This is a
finite structural bridge only; weights, complete pair spectra, label
assignments, and least-remote/descent completeness remain open.

An independent Prüfer-tree replay (no NetworkX and no shared primary tree
generator) checked the same unique-port and reconstruction invariants through
order six: `1,441` labelled topologies, `8,476` rooted instances, and
`259,384` low/high partitions, all passing.  This strengthens the structural
interface evidence but remains finite and unweighted.

The exact CP-SAT label-state expansion to order seven (`98814`) timed out at
30:13 with a zero-byte output and is not evidence.  The order-six replacement
(`98820`) covered 55,300 rows and passed the independent graph/BFS verifier,
but returned 53,137 `INFEASIBLE` and 2,163 `UNKNOWN` rows.  A one-second
targeted rerun (`98823`) resolved 365 of those, leaving 1,798 UNKNOWN; job
`98826` then reran exactly that remainder at five seconds per row.  Its final
artifact has SHA-256
`b9d7e3dcc9f0401a3d2eb7c832e02b881d8c41b0c8668c1021647470807c382d`, passes
the independent verifier, and is `55,300/55,300 INFEASIBLE` with zero UNKNOWN
or FEASIBLE rows.  A semantic comparison across both reruns found no changes
outside solver status/time fields.  This closes the exact order-six finite
model only; no global completeness claim follows.

The order-seven replacement was sharded over all 48 rooted skeletons.  The
recovered original shards covered `129,360` rows (`2,695` per shard):
`124,368 INFEASIBLE` and `4,992 UNKNOWN`, with every UNKNOWN row an `EDGE`
state.  Array `98895` reran exactly those UNKNOWN rows at five seconds each;
all 48 shards were retrieved and merged.  The merged artifact
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order7_merged.json`
has SHA-256
`100e6db398ceda441f872968b277e66f685983946fbaf05221e636839474524a`.
The independent verifier returns `VERIFIED_L521_J32_LABEL_STATE_CPSAT_ARTIFACT`
with `129,360/129,360 INFEASIBLE`, so this exact order-seven label-state model
is now a verified finite exclusion.  It still does not close attachment/LCA
completeness, arbitrary low forests, or the global nonexistence theorem.

The next bounded extension was Hoffman2 array `98972`, covering all 115 rooted
order-eight skeletons under the same forced `L(5,21)/J(32)` full-domain
label-state model (`3,584` rows per shard). Its 412,160 original rows contain
`398,094 INFEASIBLE` and `14,066 UNKNOWN` (all UNKNOWN are `EDGE`).  Targeted
five-second rerun array `99091` completed all 115 shards.  The merge replaced
exactly `14,066` UNKNOWN rows, and the independent verifier returns
`VERIFIED_L521_J32_LABEL_STATE_CPSAT_ARTIFACT` plus
`VERIFIED_INDEPENDENT_BFS_REPLAY` for all `412,160` rows: `58,880 EDGE`,
`176,640 FWD`, and `176,640 REV`, all `INFEASIBLE`.  The merged artifact is
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order8_merged.json`
with SHA-256
`d490f3b40a75b34d59fd43458cfd0907031233a45f74df9adf0f8764797a632f`.
This closes the exact finite order-eight label-state model, but not
attachment/LCA completeness, arbitrary low forests, or global nonexistence.

The next direct attachment/LCA falsification was submitted as Hoffman2 job
`99416` (`scripts/hoffman2_attachment_lca_order3_slurm.sh`) and completed with
an initial artifact.  Its
`--max-order 3` setting actually covers rooted skeleton orders 1, 2, and 3,
for `41,088` rows in total.  The order-three slice is both rooted order-three
skeletons and `34,560` rows (`27,648 EDGE`, `3,456 FWD`, `3,456 REV`); orders 1
and 2 add `6,528` rows.  All rows use the corrected full-domain attachment
model.  The artifact has `41,088/41,088` rows, with `35,244 INFEASIBLE` and
`5,844 UNKNOWN` (all `EDGE`); it passes the independent graph/BFS replay layer
but is not yet an exclusion because `UNKNOWN` is not zero.  Its SHA-256 is
`7871ad8696819ba9cfd81e03a331db9b79a900ebc18d4979e63cbd50d794bfd5`.
A targeted five-second rerun of exactly those `5,844` rows completed as
Hoffman2 job `99604` via
`scripts/hoffman2_attachment_lca_order3_unknown_rerun_slurm.sh`.  The full
rerun artifact
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order3_unknown_rerun_99604.json`
has `41,088/41,088 INFEASIBLE`, zero `UNKNOWN` and zero `FEASIBLE`; the
independent verifier returns `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT`
and `VERIFIED_INDEPENDENT_BFS_REPLAY`.  Its SHA-256 is
`12f9941bf7747e15867ba405dff9486705221ddfa8aee35fe6df7ff68dfbbbc`.  A
semantic comparison against the initial artifact found no changes outside
solver status/time fields.  This closes the stated finite order-three
attachment/LCA model only; richer high subtrees, arbitrary low forests,
attachment-state completeness, and global nonexistence remain **GAP**.

## Deeper J32 outward order-three run (99744 complete; geoworkstation chained rerun complete)

The next bounded relaxation keeps the complete order-three attachment/LCA
state and replaces the one-outward-leaf assumption at each J32 endpoint by
three explicit modes: `NONE`, a two-edge high path (`PATH2`), or a two-leaf
high fork (`FORK2`).  It covers rooted skeleton orders 1--3 and all existing
endpoint, side, port, and owner choices, for `92,448` rows.  Hoffman2 job
`99744` completed the initial pass at `0.20` seconds per row via
`scripts/hoffman2_j32_outward_deeper_order3_slurm.sh`; its complete artifact
already passes the independent graph/BFS verifier.  The finite relaxation is
not closed until every `UNKNOWN` row is rerun separately.  The targeted rerun
wrapper is already prepared at
`scripts/hoffman2_j32_outward_deeper_order3_unknown_rerun_slurm.sh`.

The initial artifact is
`theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_99744.json`,
with SHA-256
`c8ff7915eb5f6e4a9fc46fa0706fa2bdfe7c5c124ee8667203e1642b660f05df`.  The
independent verifier returns `VERIFIED_J32_OUTWARD_DEEPER_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY` for all `92,448` rows, but the initial
statuses are `82,831 INFEASIBLE` and `9,617 UNKNOWN` (no `FEASIBLE`), all
UNKNOWN rows in the `EDGE` shape: `1,080` at order two and `8,537` at order
three.  The queued Hoffman2 job `100025` was a ghost allocation (no batch
process, zero CPU time, and zero-byte output), so it was not used as evidence.
The exact `9,617` UNKNOWN rows were instead rerun on geoworkstation in two
deterministic 64-shard passes: first at five seconds per row, then the
remaining rows at thirty seconds per row.  The chained final artifact is
`theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_rerun_final.json`
with SHA-256
`0f1a3ebd40e18e755f5d5287aa68cf3d31feba335d5cebb5ef4403415703f238`.
The targeted audit returns `VERIFIED_J32_OUTWARD_DEEPER_TARGETED_RERUN`; the
full artifact audit returns `VERIFIED_J32_OUTWARD_DEEPER_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`, with `92,448/92,448 INFEASIBLE` and zero
`UNKNOWN` or `FEASIBLE`.  The chain-finalization tool is
`theory-lab/topwindow/finalize_pro_b27_j32_outward_deeper_chained_rerun.py`.
The targeted audit command is:

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_j32_outward_deeper_rerun.py \
  theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_99744.json \
  theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_rerun_final.json
```

This closes the stated finite J32 outward order-three relaxation only.  It
does not prove arbitrary high subtrees, arbitrary low forests, Label-State
Completeness, or the global `b=27` nonexistence theorem.

## Pro-guided isolated low-support control (Hoffman2 100060)

While `100025` is running, a separate bounded control implemented the Pro
advisor's complete low-support obligation, including both `L(21)` shapes.
Hoffman2 job `100060` completed normally in 17 seconds with `stem<=80` and
`h<=120`, testing `377,982` candidates across the six isolated rows and the
three J-32 gates.  It found zero survivors.  The artifact is
`theory-lab/topwindow/results/pro_b27_j32_isolated_l521_minimal_stem80_h120_100060.json`
with SHA-256
`14fc9ec1c4ba3c787559d098f39780a8d5065893d6738a124eead61c65e040cc`.
The independent artifact audit is:

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_j32_isolated_l521_minimal_result.py \
  theory-lab/topwindow/results/pro_b27_j32_isolated_l521_minimal_stem80_h120_100060.json
```

It returns `VERIFIED_J32_ISOLATED_CONTROL_ARTIFACT`.  This is a bounded
pressure control only: remote attachment gates, other `34--37` ownership
patterns, arbitrary high subtrees, and global Label-State Completeness remain
outside its scope.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_residual_two_branch.py
```

The replay returns `status: VERIFIED_FRONTIER` and embeds SHA-256 digests of
all twelve dependency verifiers.  It is a proof-state bundle, not a global
nonexistence theorem: complete-spectrum reception, least-remote minimality,
and strict inherited descent remain open.

## Order-four attachment/LCA extension (geoworkstation; mixed finite status)

To enlarge the direct attachment/LCA falsification without changing the
state semantics, the corrected enumerator was run through rooted skeleton
order four using 64 deterministic shards.  The merged artifact contains
`196,736` rows and passed the independent graph/BFS replay.  Its SHA-256 is
`c78cd41f019aa5e2977a41a3a20b14abde1f689e8f4073f18cbd4b38b01c4a70`; solver
statuses are `158,421 INFEASIBLE` and `38,315 UNKNOWN`, with no FEASIBLE row.

The exact UNKNOWN set was rerun once at one second per row, preserving all
non-status fields and the initial input hash.  The merged rerun has SHA-256
`af52aaab15f29c52ad50f9e4c4086774fe3fc3928521ab14451b006319ca9be5` and
statuses `161,864 INFEASIBLE`, `34,872 UNKNOWN`, no FEASIBLE row.  A second
five-second rerun of exactly those remaining rows used 96 deterministic
shards.  Its merged artifact has SHA-256
`a7c8fb1d7cf6c5f6127b89ac435b08de193c1978616d4746984ed49cf9797492` and
passes both the remote and local independent verifiers.  The final statuses
are `164,688 INFEASIBLE`, `32,048 UNKNOWN`, no FEASIBLE row.  A third rerun
targeted exactly those `32,048` rows at thirty seconds per row with 96
deterministic shards.  Strict merging produced
`results/pro_b27_attachment_lca_falsification_order4_geo_rerun_30s.json`
with SHA-256
`08addbaf987ac18217e3a3fb65a93096b6dea7a8331deb560932e32328f85239`.
The remote and local independent verifiers both pass, with
`196,736/196,736 INFEASIBLE`, zero `UNKNOWN` and zero `FEASIBLE`.  This closes
the declared rooted order-four attachment/LCA finite model only; it does not
close arbitrary high subtrees, larger low forests, or global Label-State
Completeness.
