# `b=27`: forced `L(5,21)` / `J(32)` label-state control

## Purpose

The current verified frontier forces the owners of `5` and `21` into `L`,
with the `5` owner a single edge and the `21` owner one of
`(21)`, `(5,16)`, or `(16,5)`.  The remaining `32` branch is the J-internal
single edge.  This document records the next finite control suggested by the
persistent GPT Pro audit.  It is deliberately a finite fragment and is not a
claim of global nonexistence.

## Exact finite graph family

For each rooted high skeleton through the selected order bound, every ordered
port assignment is enumerated.

* `EDGE`: three independent one-edge low components of weights `5`, `21`, and
  `32`, each joined to the skeleton by one high gateway.
* `FWD`: one path `a--5--b--16--c`, so `d(a,c)=21`, and one J edge `32`.
* `REV`: one path `d--16--a--5--b`, so `d(d,b)=21`, and one J edge `32`.

In `FWD` and `REV` the `5` edge is literally shared by the `21` path; it is
never copied.  The shared component has one rootward gateway, whose endpoint
is enumerated over all three path vertices.  The external `21` port is
coupled to this same gateway, since a second connection to a connected rooted
skeleton would make a cycle.  To expose the first under-approximation found
by Pro, each shared-path vertex independently receives zero or one optional
outward high leaf; all eight masks are enumerated.  These outward edges are
悬挂 leaves, so every row remains a tree.

## Spectrum constraints

High edges range over the full integer interval `38..300` and are pairwise
distinct.  For each row, every unordered pair on the concrete skeleton and
low-component vertices is included, together with every non-root root-profile
translation by

```text
B0_nonzero = {6,13,14,15,23,27,28},   named offsets = {38,54,57}.
```

All such values share one `AllDifferent` table and avoid the fixed packet,
the punctured value `4`, and named internal values `{16,19,35}`.  In
particular, the shared states explicitly expose the canonical-packet
reservation of `16` instead of silently dropping the `(5,16)/(16,5)`
candidates.  This reservation is a hypothesis of the finite control: it is
not, by itself, a new theorem that one globally fixed unordered pair owns
`16` in every residual realization.

Consequently the implementation records every shared `FWD/REV` row as an
explicit `INFEASIBLE` logical contradiction (`new 16-edge` versus the
reserved `16`) rather than repeatedly invoking CP-SAT on identical
constraints.  The independent verifier checks the graph and owner distances
for those rows as well as for the solver-backed `EDGE` rows.

The primary model is
`theory-lab/topwindow/enumerate_pro_b27_l521_j32_label_state_cpsat.py`; its
independent weighted-tree replay is
`theory-lab/topwindow/verify_pro_b27_l521_j32_label_state_cpsat_result.py`.
The Hoffman2 wrapper is
`scripts/hoffman2_l521_j32_label_state_slurm.sh`.

## Hoffman2 legacy run (98793; provenance-limited)

The first Hoffman2 run covered the full 16,420-row order-five family and
returned `INFEASIBLE` for every row.  Independent replay verified the graph
and distance tables, but the artifact shows that the shared `FWD/REV` rows
were generated before the explicit `EXPLICIT_NAMED_16_RESERVATION`
short-circuit was present (14,976 rows have no reservation route field).  It is
therefore retained only as a legacy all-zero comparison and must not be cited
as a current-version reproduction.

The legacy artifact is
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_98793.json`
(SHA-256
`73783a6c576004ac01b440f1268e6426a5a425f39c2df5bcab4d3f013d8a1881`).
The current-hash rerun is Hoffman2 job `98794`.  Its artifact is
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_98794.json`
(SHA-256
`0975222739cc8bebe57ebdb0345735c34f7baf2156e088f56aa5209979545492`).
The same verifier returns `VERIFIED_L521_J32_LABEL_STATE_CPSAT_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  After removing nondeterministic wall-time
fields, its 16,420 row records match the Geo current-hash run exactly (row
semantics SHA-256
`3a266f03916f9f73e5117350013eca1ee8430b6910ed37ae43c28af463091c7f`).

## Geo workstation current-hash run (PID 2195208)

The same current source was also run independently on the Geo workstation at
low priority.  It covered the same 16,420 rows and returned `INFEASIBLE` for
every row, including the explicit reservation route on all 14,976 shared
`FWD/REV` rows.  The artifact
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_geo.json` has
SHA-256
`2ebe11ba5e6166c6c2d9320a7b0221e6b658017f67682c92c71d439ad4efe9cb`.
The independent verifier returns
`VERIFIED_L521_J32_LABEL_STATE_CPSAT_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  Ignoring nondeterministic wall-time
fields, the two current-source runs should be compared by row semantics;
the legacy `98793` run is not suitable for that comparison.

## Evidence boundary

If all rows for a fixed skeleton/port/shape/side-mask family are `INFEASIBLE`,
the exact conclusion is only that this displayed finite graph family has no
label assignment satisfying the listed constraints.  It does not establish
attachment/LCA completeness, arbitrary outward high subtrees, a high-side
forest, or global `b=27` closure.  A `UNKNOWN` row is not a zero.  The first
remaining structural gap is a completeness theorem for the omitted outward
topologies (and, separately, for how low-support components attach to the
fixed core).

The Pro audit specifically rejected promoting the one-gateway shared model to
a theorem: a real tree may share the low `5` edge while carrying an internal
high side branch.  The eight optional-leaf masks are therefore an explicit
stronger finite control, not a silent claim that all side structure has been
enumerated.

## Attachment/LCA first falsification (Hoffman2 98802)

To address the next completeness gap, a separate experiment fixed the same
three owner states but exposed additional attachment variables.  For the
order-one rooted skeleton it enumerated both endpoints as the rootward
attachment for each of the three low components, and independently allowed
one outward high leaf at either endpoint of each low edge.  The shared states
also varied all three shared-path attachment vertices, all eight shared-path
leaf masks, both J32 endpoint attachments, and all four J32 leaf masks.  Every
fragment pair and every non-root translation remained in one `AllDifferent`
table.

Hoffman2 job `98802` tested 896 rows (`512` `EDGE`, `192` `FWD`, `192`
`REV`); all 896 were `INFEASIBLE`, with no `UNKNOWN`.  The artifact is
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_98802.json`
(SHA-256
`26cfb6651e95480f225a52fa2c4aa4f77e266ce041cc272f6355862172aece6d`).
The independent replay is:

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_attachment_lca_falsification_result.py \
  theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_98802.json
```

It returns `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  This is only a local order-one state-class
exclusion: arbitrary high Steiner subtrees, richer outward incidences, larger
skeletons, and the global completeness lemma remain open.  The next safe
extension is order two (or a proof that higher skeletons normalize), not a
global theorem upgrade.

### Superseded order-two attempt (98803)

The first order-two submission (`98803`) exposed an enumerator-scope bug: the
FWD/REV loop was nested under the three-port EDGE loop, so the artifact has
17,280 rows instead of the intended 6,528.  The independent verifier rejected
it on this row-count mismatch.  The raw file is retained for provenance
(`SHA-256 eccbfab442bdb2fe7408b227a670e9400e327747b51d7b34334fd4c742702c3c`)
but is not evidence.  The loop was corrected in commit `f1c408a`; current
order-two job `98804` is the replacement.

## Order-two attachment/LCA run (Hoffman2 98804)

The corrected order-two run covers 6,528 intended rows: 4,608 `EDGE`, 960
`FWD`, and 960 `REV`.  Independent structural/BFS replay verified all row
graphs and owner distances.  Solver results were `6,072 INFEASIBLE` and
`456 UNKNOWN`, with no `FEASIBLE` row; all 456 unknowns are the order-two path
skeleton with the three EDGE ports at its internal vertex.  Thus this run is
not an all-zero result and the unknown rows remain uncovered.

The artifact is
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order2_98804.json`
(SHA-256
`94db8144a54dd4ea82dec5d3d4ac22d2311739f83623a98e960cf848c2b62f7f`).
The verifier command is:

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_attachment_lca_falsification_result.py \
  theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order2_98804.json
```

It returns `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`, but the logical status is only a mixed
finite control (`UNKNOWN` is not `INFEASIBLE`).  Job `98805` is a targeted
five-second rerun of precisely those 456 rows.

The targeted rerun (`98805`) resolved all 456 rows: the final artifact has
6,528/6,528 `INFEASIBLE` and no `UNKNOWN` or `FEASIBLE` rows.  Its SHA-256 is
`7ad697156ffd4afecb07389ebf80662c3184e55397c477bc5b8a59058da31d0c`.
The same independent verifier passes; comparison with the mixed artifact
shows that only solver-status/time/statistic fields changed.  Therefore the
specified order-two attachment/LCA family is a verified finite exclusion,
while the larger topology and completeness gaps remain exactly as stated.

## Deeper J32 outward control (Hoffman2 98806)

Following the Pro adversarial audit, the J32 endpoint leaf assumption was
relaxed without changing the owner states or attachment variables.  Each J32
endpoint independently chooses one of `NONE`, a two-edge high path (`PATH2`),
or a two-leaf high fork (`FORK2`).  The order-one run covered all 2,016 rows
(`1,152` `EDGE`, `432` `FWD`, `432` `REV`); every row was `INFEASIBLE` with no
`UNKNOWN`.

The artifact is
`theory-lab/topwindow/results/pro_b27_j32_outward_deeper_98806.json`
(SHA-256
`7849c9b68cfb9b7cd08bb792c3089dbe9360110a3fc4943c96bd4f27f401f754`).
The independent verifier returns `VERIFIED_J32_OUTWARD_DEEPER_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  This is a finite order-one exclusion for
the nine two-endpoint modes only; longer paths, larger forks, arbitrary high
Steiner skeletons, and the global completeness lemma remain open.

## Order-two J32 outward run (Hoffman2 98807/98808; completed)

After the order-one zero, the same enumerator was submitted as job `98807`
using `scripts/hoffman2_j32_outward_deeper_order2_slurm.sh` with
`--max-order 2 --time-limit 0.20`.  It is a single low-priority CPU job on
Hoffman2 (`campus24`); at submission the queue reported it `RUNNING` on
`n1183`.  The expected finite family is 14,688 rows (10,368 `EDGE`, 2,160
`FWD`, and 2,160 `REV`, from the current loop bounds).  No result, coverage claim, or theorem is recorded
until the artifact is retrieved and passes the independent verifier; any
`UNKNOWN` rows will be rerun separately rather than counted as zero.

The initial artifact was retrieved after the job left the queue and has SHA-256
`06cab8427ec5ac85c7377f6a1702f29cb2ca161b0d96e1c8c1653c7bb675bd9e`.  Its
independent graph/BFS verifier passed for all 14,688 row graphs, with the
exact breakdown `10,368 EDGE + 2,160 FWD + 2,160 REV`; the solver status was
`13,608 INFEASIBLE + 1,080 UNKNOWN`, with no `FEASIBLE` row.  Every UNKNOWN
was the order-two path skeleton `(())`, with all three low ports at its
internal vertex; the endpoint/mode choices varied.

Hoffman2 job `98808` reran exactly those 1,080 rows at five seconds per row.
The final artifact
`theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order2_unknown_rerun_98808.json`
has SHA-256
`5a11a3ac5fbe95d2d176057257bbb320b904513e20a641e2a3b4f6b03d3aee01` and
passes the same independent verifier.  It has 14,688/14,688 `INFEASIBLE`,
zero `UNKNOWN` and zero `FEASIBLE`; the rerun records `1080` replacements,
`5.0` seconds per row, and the exact input SHA above.  A semantic comparison
found no change in any non-UNKNOWN row and only `status`/wall-time changes in
the replaced rows.

This closes the displayed order-two nine-mode finite family, not the global
problem: arbitrary longer paths, larger forks, high Steiner skeletons, and
the label-state completeness bridge remain open.

## Three-port marked skeleton catalogue (Hoffman2 98812)

To make the next completeness bridge explicit, job `98812` enumerated every
rooted residual tree of orders one through ten with three labelled incidence
locations, `L5`, `L21`, and `J32`, quotienting only rooted automorphisms.  The
artifact is
`theory-lab/topwindow/results/pro_b27_marked_skeleton_3port_98812.json`
(SHA-256
`d80feac9332a3732037d1607f0904fd70bec06a3180a8e3ea5e7499141e2f834`) and
reports `VERIFIED_MARKED_SKELETON_CATALOGUE_3PORT`.

The raw assignment rows by order are
`1,16,81,512,1875,7776,26411,94208,308367,1060000`; canonical marked rooted
counts are
`1,8,41,179,718,2731,10009,35692,124616,427837`, totaling `601832`.
This is a topology-only finite catalogue: it does not enumerate
low-component shapes, ordered high-edge tuples, admissible weights, complete
pair distances, or complete-spectrum closure.  It therefore supplies a
three-port input layer for the Label-State Completeness bridge but does not
close that bridge or imply global nonexistence.

## Low-component port/skeleton round-trip (Hoffman2 98813)

The next structural audit combined the port extractor with the high-skeleton
incidence layer.  For every free tree of order at most ten, every root, and
every subset of edges designated low (the complement being high), it recorded
each low component's rootward port, every high boundary edge with both endpoint
incidences, and the component-local rooted low tree.  It then reconstructed the
rooted edge-coloured tree and compared its canonical code with the input.

Hoffman2 job `98813` returned
`VERIFIED_LOW_COMPONENT_PORT_SKELETON_ROUNDTRIP`.  It covered `1,809` rooted
instances and `680,961` low/high partitions (the exact expected count), with
`3,657,039` component records and `2,976,078` high-edge incidences processed.
The maximum number of components was ten and the maximum boundary incidence
count was nine.  The artifact is
`theory-lab/topwindow/results/pro_b27_low_component_port_skeleton_roundtrip_98813.json`
(SHA-256
`485640a1b630e95c05187c04fd85b66a46f22d9981824b939f23a8310cfc4d57`).

This closes only the finite structural round-trip: it does not enumerate
positive edge weights, complete pair distances, three-port label assignments,
or complete-spectrum/least-remote descent.  Thus it supports the state
interface but does not prove Label-State Completeness or global nonexistence.

An independent implementation, without NetworkX or the primary
non-isomorphic-tree generator, replayed the same port invariant on all labelled
Prüfer trees through order six.  It covered `1,441` labelled topologies,
`8,476` rooted instances, and `259,384` low/high partitions, with every
round-trip passing.  The local command is:

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_low_component_port_skeleton_independent.py \
  --max-order 6
```

It returns `VERIFIED_INDEPENDENT_LABELLED_PORT_REPLAY`.  This is an independent
finite replay of the structural layer, not a weighted-spectrum or global
completeness proof.

The unrestricted combinatorial implication behind this interface is now
written as `VERIFIED_PORT_DECOMPOSITION_LEMMA` in
`docs/pro-b27-port-complete-state-lemma.md`: contracting low components gives
a rooted quotient tree, hence one and only one rootward port for each non-root
component; restoring the recorded internal low trees and both high-edge
incidences is lossless, so LCAs and pair distances are recovered from the
actual reconstructed tree. This removes a purely tree-theoretic ambiguity,
but it does not establish completeness of the represented attachment states
or any weighted-spectrum/nonexistence conclusion.

## Expanded exact label-state control (Hoffman2 98820/98823/98826)

An attempted order-seven expansion (`98814`) reached the 30-minute SLURM
limit and wrote a zero-byte output; it is recorded as `TIMEOUT`, not evidence.
The controlled order-six replacement (`98820`) covered the exact 55,300 rows
(`5,764 EDGE`, `24,768 FWD`, `24,768 REV`) and passed independent graph/BFS
replay.  Its initial statuses were `53,137 INFEASIBLE` and `2,163 UNKNOWN`,
with no `FEASIBLE` rows; all UNKNOWN rows were `EDGE` order 4--6.

The artifact is
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order6_98820.json`
(SHA-256
`40259ede7c5995ff52b2d2c4d9eb52861f9f481d2fd81b6eb4aeafe21aece53b`).
The first targeted rerun (`98823`) gave those 2,163 rows a one-second limit:
`365` became `INFEASIBLE`, leaving `53,502 INFEASIBLE + 1,798 UNKNOWN`.
The five-second rerun (`98826`) then targeted precisely those remaining 1,798
rows.  Its final artifact
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order6_unknown_rerun5_98826.json`
has SHA-256
`b9d7e3dcc9f0401a3d2eb7c832e02b881d8c41b0c8668c1021647470807c382d` and
passes the independent verifier with `55,300/55,300 INFEASIBLE`, zero UNKNOWN
and zero FEASIBLE.  Semantic comparison shows that across both reruns only
solver status/time fields changed; all structural row fields and all previously
non-UNKNOWN rows are unchanged.  Thus the exact order-six family is a verified
finite exclusion for this model, while the broader attachment/LCA and global
completeness gaps remain open.

## Order-seven sharded label-state control (98831/98879/98895)

The whole order-seven expansion is split over the 48 rooted skeletons (`2,695`
rows per skeleton).  The first array (`98831`) produced valid non-empty output
for skeletons 16--47; a corrected resubmission (`98879`) produced skeletons
0--15.  The local audit therefore has all `48 * 2,695 = 129,360` original
rows, with `124,368 INFEASIBLE` and `4,992 UNKNOWN`; every UNKNOWN is an
`EDGE` row.  Sixteen zero-byte files from the failed first-array tasks are
ignored and are not evidence.

The five-second targeted UNKNOWN rerun was submitted as array `98895` using
`scripts/hoffman2_l521_j32_label_state_order7_unknown_rerun_array_slurm.sh`.
All 48 non-empty rerun shards were retrieved after the array completed.  The
merge script
`theory-lab/topwindow/merge_pro_b27_l521_j32_label_state_order7_shards.py`
replaced exactly the `4,992` original UNKNOWN rows and verified that every
non-status structural field is unchanged.  The merged artifact is
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order7_merged.json`
with SHA-256
`100e6db398ceda441f872968b277e66f685983946fbaf05221e636839474524a`.

The independent verifier returns
`VERIFIED_L521_J32_LABEL_STATE_CPSAT_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY` for all `129,360` rows, broken down as
`16,464 EDGE + 56,448 FWD + 56,448 REV`; every row is `INFEASIBLE`, with no
`UNKNOWN` or `FEASIBLE` result.  This closes the exact forced
`L(5,21)/J(32)` model through rooted skeleton order seven.  It remains a
finite model exclusion only: attachment/LCA completeness, arbitrary low
forests, and global `b=27` nonexistence are still open.

An order-eight extension ran as Hoffman2 array `98972` using
`scripts/hoffman2_l521_j32_label_state_order8_array_slurm.sh`. It covers the
115 rooted order-eight skeletons (`3,584` rows per shard) under the same
full-domain `38..300` model. The 412,160 original rows contain `398,094
INFEASIBLE` and `14,066 UNKNOWN`, all UNKNOWN rows being `EDGE`.  The targeted
five-second rerun is array `99091`; all 115 rerun shards completed.  The merge
replaced exactly `14,066` UNKNOWN rows with no change to non-status fields.  The
merged artifact is
`theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order8_merged.json`
with SHA-256
`d490f3b40a75b34d59fd43458cfd0907031233a45f74df9adf0f8764797a632f`.

The independent verifier returns
`VERIFIED_L521_J32_LABEL_STATE_CPSAT_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY` for all `412,160` rows, broken down as
`58,880 EDGE + 176,640 FWD + 176,640 REV`; every row is `INFEASIBLE`, with no
`UNKNOWN` or `FEASIBLE` result.  This closes the exact forced
`L(5,21)/J(32)` model through rooted skeleton order eight.  It remains a finite
model exclusion only: attachment/LCA completeness, arbitrary low forests, and
global `b=27` nonexistence are still open.

## Order-three attachment/LCA extension (Hoffman2 99416; initial artifact)

To attack the remaining attachment/LCA gap directly, the corrected attachment
enumerator was submitted once as low-priority Hoffman2 job `99416` using
`scripts/hoffman2_attachment_lca_order3_slurm.sh`.  The script's
`--max-order 3` setting includes rooted skeleton orders 1, 2, and 3: `41,088`
rows in total.  The order-three slice is the two rooted order-three skeletons
and contributes `34,560` rows (`27,648 EDGE + 3,456 FWD + 3,456 REV`); orders 1
and 2 contribute the remaining `6,528` rows.  Every row uses the same
endpoint, side-leaf, shared-path, and J32 attachment choices, the full
`38..300` high-edge domain, and one complete fragment/translation
AllDifferent table.  The initial artifact
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order3_99416.json`
has `41,088/41,088` rows and passes the independent graph/BFS replay layer:
`35,244 INFEASIBLE` and `5,844 UNKNOWN`, all of the latter in the `EDGE`
shape.  Its SHA-256 is
`7871ad8696819ba9cfd81e03a331db9b79a900ebc18d4979e63cbd50d794bfd5`.
Because `UNKNOWN` is not a zero, Hoffman2 job `99604` reran exactly those
`5,844` rows with a five-second limit using
`scripts/hoffman2_attachment_lca_order3_unknown_rerun_slurm.sh`.  The full
rerun artifact
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order3_unknown_rerun_99604.json`
has `41,088/41,088 INFEASIBLE`, zero `UNKNOWN` and zero `FEASIBLE`, and its
independent verifier returns `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT`
with `VERIFIED_INDEPENDENT_BFS_REPLAY`.  Its SHA-256 is
`12f9941bf7747e15867ba405dff9486705221ddfa8aee35fe6df7ff68dfbbbc`.  A
semantic comparison against the initial artifact found no changes outside
solver status/time fields.  This closes the stated finite order-three
attachment/LCA model only; attachment-state completeness, richer high
subtrees, arbitrary low forests, and global nonexistence remain open.

## Deeper J32 outward order-three run (99744 plus geoworkstation rerun; complete finite model)

The next bounded relaxation keeps the complete order-three attachment/LCA
state and replaces the one-outward-leaf assumption at each J32 endpoint by
three explicit modes: `NONE`, a two-edge high path (`PATH2`), or a two-leaf
high fork (`FORK2`).  The model covers rooted skeleton orders 1--3, all
endpoint/side/port choices, the full `38..300` high-edge domain, and the same
single AllDifferent table over all fragment pairs and fixed/named translates.
The loop contains `92,448` rows.  Hoffman2 job `99744` supplied the initial
pass at `0.20` seconds per row via
`scripts/hoffman2_j32_outward_deeper_order3_slurm.sh` (wrapper SHA-256
`f31ec80db197f41020077531ba01469a3978e9ca2d7bef3051c821a70bb58126`).
The exact `9,617` UNKNOWN rows were rerun on geoworkstation in two deterministic
64-shard passes (5 seconds per row, then 30 seconds for the remainder).  The
chain-final artifact is
`theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_rerun_final.json`
with SHA-256
`0f1a3ebd40e18e755f5d5287aa68cf3d31feba335d5cebb5ef4403415703f238`.
The targeted rerun verifier and full artifact verifier both pass, including
the independent BFS replay; all `92,448` rows are `INFEASIBLE`, with no
`UNKNOWN` or `FEASIBLE`.  This is a verified finite exclusion for this exact
relaxation only; arbitrary high subtrees, arbitrary low forests, Label-State
Completeness, and global nonexistence remain open.

## Order-four attachment/LCA expansion (geoworkstation; mixed finite status)

The corrected attachment/LCA shard runner was extended to rooted skeleton
order four.  Its deterministic 64-shard initial pass covered all orders one
through four, `196,736` rows in total.  The merged artifact on the
geoworkstation is
`results/pro_b27_attachment_lca_falsification_order4_geo_initial.json`
(SHA-256
`c78cd41f019aa5e2977a41a3a20b14abde1f689e8f4073f18cbd4b38b01c4a70`).
The independent verifier returned
`VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`; solver statuses were `158,421
INFEASIBLE` and `38,315 UNKNOWN`, with no `FEASIBLE` row.

The exact `38,315` UNKNOWN rows were then rerun in 64 deterministic shards
with a one-second per-row limit.  Strict merging checked the initial input
hash and preserved every non-solver field.  The resulting artifact is
`results/pro_b27_attachment_lca_falsification_order4_geo_rerun_1s.json`
(SHA-256
`af52aaab15f29c52ad50f9e4c4086774fe3fc3928521ab14451b006319ca9be5`),
with `161,864 INFEASIBLE` and `34,872 UNKNOWN`, no `FEASIBLE`.  A second
rerun of exactly those rows at five seconds per row used 96 deterministic
shards.  Strict merging replaced all `34,872` target rows; the final artifact
is
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order4_geo_rerun_5s.json`
(SHA-256
`a7c8fb1d7cf6c5f6127b89ac435b08de193c1978616d4746984ed49cf9797492`).
The remote and local independent verifiers both return
`VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`.  Solver statuses are `164,688
INFEASIBLE` and `32,048 UNKNOWN`, with no `FEASIBLE` row.  A third rerun then
targeted exactly those `32,048` rows at thirty seconds per row using 96
deterministic shards.  The merged artifact is
`theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order4_geo_rerun_30s.json`
(SHA-256
`08addbaf987ac18217e3a3fb65a93096b6dea7a8331deb560932e32328f85239`).
The remote and local independent verifiers both return
`VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` and
`VERIFIED_INDEPENDENT_BFS_REPLAY`; all `196,736` rows are `INFEASIBLE`, with
zero `UNKNOWN` or `FEASIBLE`.  This closes the declared rooted order-four
attachment/LCA finite model only; arbitrary high subtrees, larger low forests,
and global Label-State Completeness remain open.
