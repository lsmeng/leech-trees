# FW319 b=27: frozen-v3 m=2,e=2 shard plan and schema audit

Date: 2026-08-29

## Purpose

This note freezes a theorem-supporting remote interface for the next universal
literal-low layer `m=2,e=2`.  It is a bounded design audit only: no large local
enumeration is run here, and no previously verified `m=3` artifact is modified.

## Current generator support boundary

The current script
`theory-lab/topwindow/enumerate_pro_b27_universal_low_smoke.py` is genuinely
implemented only for `e<=1`, despite accepting arbitrary integers through the
`--e-values` CLI.  The load-bearing reason is structural:

- `endpoint_candidates(m,e,...)` returns one endpoint pair, not a two-edge set;
- `base_blocks(...)` assigns one scalar `lambda_value` and constructs at most
  one `extra` edge;
- therefore passing `e=2` today does **not** create two literal new low edges.

Hence `--e-values 2` on that generator would be an under-model, not a valid
`m=2,e=2` coverage run.  A dedicated two-edge generator (or a generalized
base-domain implementation) is required before any Geo `e=2` result can be
used theoremically.

## Complete literal endpoint base domain

For `m=2`, the vertices are fixed `K` plus `x0,x1`.  A new literal edge must
touch at least one anonymous vertex.  There are exactly

- one anonymous-anonymous edge `x0-x1`;
- fifteen `x0-named` edges;
- fifteen `x1-named` edges;

for 31 admissible new-edge endpoint pairs.

The universal `e=2` endpoint domain is every unordered pair of distinct such
edges, hence

`C(31,2)=465`

endpoint sets.  They split into the following S2-stable partition, used only
for sharding and never for pruning:

1. `aa_plus_named`: `x0-x1` plus one anonymous-named edge — 30 sets;
2. `same_anon_two_named`: two distinct named neighbors of the same anonymous
   vertex — 210 sets;
3. `cross_anon_same_named`: `x0-v` and `x1-v` — 15 sets;
4. `cross_anon_distinct_named`: `x0-v` and `x1-w`, `v!=w` — 210 sets.

The counts sum to 465 and the four classes are invariant under the anonymous
swap `x0<->x1`.

## Ordered distinct low weights

Let

`H37_L={5,16,18,19,20,21,24,25,26,34,35,36,37}`.

For each unordered two-edge endpoint set, first sort its two literal edges by
one deterministic named-preserving endpoint order and call them slots 0 and 1.
Then enumerate **all ordered injective assignments**

`(lambda0,lambda1) in H37_L^2`, `lambda0 != lambda1`.

There are `13*12=156` assignments per endpoint set, for

`465*156 = 72,540`

base descriptors before any forest-validity or owner filtering.

Under `x0<->x1`, weights travel with literal edges; only after transport are
edge slots re-sorted.  A transport certificate must therefore act on weighted
literal edges, not merely on the two-position weight tuple.

## Required remote materialization semantics

For each base descriptor `(E_new,lambda)`:

1. materialize `FIXED_EDGES union E_new` literally;
2. perform acyclicity, distinct edge-weight, puncture-4, fixed-owner reuse and
   duplicate low-pair checks;
3. invalid bases occupy exactly one explicit sentinel raw slot;
4. for each valid base, recompute the actual low-component partition;
5. enumerate every rootward-port choice for every non-root component;
6. enumerate every outward-incidence subset for every component;
7. recompute all component pair distances from the materialized forest;
8. derive total `owner_status` for every `h in H37_L`, with
   `L_ACTUAL(actual endpoints/path)` or `NOT_L`, and force `status[32]=NOT_L`;
9. verify the theorem-level `5/21` path condition from the actual path; do not
   generate only preselected `(21)/(5,16)/(16,5)` topology templates;
10. retain actual owner endpoints and literal path-edge identities so shared
    owner paths and forks are preserved automatically;
11. do not impose any unproved `34--37` endpoint/LCA/attachment geometry.

This is the minimum semantics needed for the existing Fixed-L/H37 exhaustion
theorem to imply low-side coverage.

## Raw index / shard contract

The remote generator should use a hierarchical key

`(endpoint_type, endpoint_set_rank, weight_assignment_rank, port_rank, mask_rank)`

within the frozen global `m=2,e=2` domain.  A base descriptor that fails before
port/mask expansion contributes one sentinel slot.  A valid base contributes
`port_total * mask_total` slots determined only after actual component
materialization.

Therefore the flattened index must be constructed from base-block prefix sums;
it must not assume a constant port/mask radix across endpoint types.

Each shard artifact must bind at least:

- frozen schema version and ordering version;
- common semantic-base hash and scope-specific semantic-input hash;
- exact endpoint-type / endpoint-rank / weight-rank scope;
- fixed-K / H37 / owner-status semantics;
- global raw count for its declared domain, processed/accepted/sentinel counts;
- sentinel reason counts;
- raw-stream and canonical-stream SHA-256 commitments;
- generator SHA-256;
- canonical multiplicity information sufficient for exact merge.

A provenance certificate must additionally bind the source artifact SHA and
full-stream replay certificate/script SHA.

## Independent replay obligations

The replay implementation must not consume generator owner hints.  From each
raw base and port/mask rank it must independently rebuild:

- literal weighted edges;
- tree/forest validity and rejection reason;
- component partition;
- rootward/outward incidence;
- complete low pair table;
- all `H37_L` owner statuses and forced `32=NOT_L`;
- actual 5/21 path condition;
- canonical marked serialization.

It then must reproduce raw/canonical stream digests and all aggregate counts.

## S2 orbit certificate

For the complete marked state, `sigma=(x0 x1)` acts simultaneously on:

- literal weighted edges (with weights carried by edges);
- component vertices;
- rootward ports;
- outward masks;
- actual owner endpoints/path identities;
- anonymous aliases.

The certificate must prove:

`canon(sigma(s)) = canon(s)`

for the defined state representation and account for non-free stabilizers.
No universal `accepted = 2*canonical` rule may be assumed for `e=2`; stabilizer
sizes depend on the weighted two-edge geometry and incidence marks.

The final merge must verify canonical multiplicity conservation

`sum_k multiplicity(k) = accepted_raw`.

## Lightweight planner

`theory-lab/topwindow/plan_pro_b27_m2_e2_shards.py` freezes and checks only the
endpoint/weight base domain.  It verifies:

- 31 admissible literal edges;
- 465 unordered two-edge sets;
- exact endpoint-type counts `30/210/15/210`;
- S2 stability of this partition;
- 156 ordered distinct weight assignments;
- 72,540 pre-validity base descriptors;
- weighted-edge S2 transport round-trip on a tiny fixture.

It does not enumerate ports, masks, owner tables, or canonical rows.

## Implemented first bounded two-edge pilot

The separate generator
`theory-lab/topwindow/enumerate_pro_b27_m2_e2_two_edge_pilot.py` now implements
the requested exact pilot without changing any verified one-edge or m3 file:

`m=2,e=2, endpoint_type=cross_anon_same_named`

with endpoint set `{x0-d6, x1-d6}` and ordered assignments `(5,16)` and
`(16,5)`.  Both literal weighted edges are inserted before any validity test.
For a valid base the implementation derives the actual component partition,
all rootward-port radices, all outward-mask radices, H37 owner pairs, total
owner status, and S2-canonical marked payload from that actual forest.

There is an important branch-specific outcome: both requested bases are
necessarily explicit sentinels, because the fixed packet already contains the
literal edge `v-y0` of weight `16`.  Hence the edge-weight injectivity check
rejects either ordered assignment with reason `edge_weight_duplicate`.  The
bounded pilot therefore has exactly two raw slots, both sentinels, and zero
accepted rows.  This is a valid test of true two-edge materialization and
sentinel accounting, but it does not exercise accepted-row port/mask expansion.

The same file supplies `--fixture-only`, a codec-only test with two synthetic
weights above 37.  It checks that both literal extras survive materialization,
that components/ports/masks are derived from the resulting edge list, and that
weighted edges transport correctly under `x0<->x1`.  Those synthetic weights
are explicitly not branch-valid low states and contribute no search evidence.

### Still unimplemented for the universal m2,e2 layer

The pilot does not yet provide:

1. ranking/enumeration of all 465 unordered two-edge endpoint sets;
2. ranking/enumeration of all 156 ordered distinct H37 assignments per set;
3. the 72,540-base hierarchical flatten/unflatten/shard index;
4. a full-stream independent two-edge replay implementation;
5. provenance hardening for arbitrary m2,e2 shard scopes;
6. an independent S2 orbit/stabilizer certificate for arbitrary accepted
   two-edge marked states;
7. cross-shard canonical multiplicity merge.

The pilot generator now also supports `--weights W0 W1 --base-only` and
`--find-valid-candidates`.  These paths perform only base materialization and
validity checks; they do not enumerate port/mask rows.  For the fixed endpoint
set `{d6-x0,d6-x1}`, all 90 ordered distinct tuples drawn from the 10 H37_L
values not already used as fixed literal edge weights are invalid: 49 fail
`fixed_owner_reuse` and 41 fail `pair_distance_duplicate`.  For example,
`(5,18)` creates a new pair of value 11 and `(20,24)` creates a new pair of
value 30, both reusing fixed S0 owners.  Hence this endpoint topology has no
accepted candidate under the current low-side validity predicate.

The bounded selector was then extended to four explicit endpoint sets without
port/mask expansion.  Two sets involving `a` remained fully invalid over the 90
eligible ordered tuples.  The first accepted candidates appeared when only the
smaller fixed components were touched:

- `same_anon_two_named_u_p = {u-x0, p-x0}` with ordered weights `(5,20)` is
  base-valid after only two ordered tuples are checked.  Its actual low
  components have port radices `[1,4,3,1]`, `port_total=12`,
  `mask_total=131072`, hence `1,572,864` incidence raw rows.
- `cross_anon_distinct_named_u_p = {u-x0, p-x1}` with ordered weights `(5,20)`
  is also base-valid, with port radices `[1,2,3,3]`, `port_total=18`, and
  `2,359,296` incidence raw rows.

The first Geo accepted-row stress pilot should therefore use the smaller
`same_anon_two_named_u_p` base `(5,20)`.  This selection is an engineering pilot
choice only and must not be promoted to a pruning theorem for the 72,540-base
universal domain.

## Theorem boundary

Passing the planner fixture proves only that the intended base-domain partition
is finite, complete by definition, and S2-stable.  Passing the proposed Geo
pilot would certify only that tiny declared pilot scope.

A theorem-supporting frozen `m=2,e=2` claim requires the complete endpoint and
weight domain, full port/mask expansion, independent owner/canonical replay,
S2 orbit accounting, provenance hardening and exact merge.  Even that would not
prove `m>3`, `e>2`, complete L-surjectivity, high-completion surjectivity, the
FW319 `b=27` residual nonexistence theorem, or global Leech-tree nonexistence.
