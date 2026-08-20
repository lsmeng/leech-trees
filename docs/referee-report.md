# Adversarial referee report: soundness of `src/leech_search.cpp` (pruning + symmetry breaking)

Referee pass 2026-08-18. Object of the audit: the exact C++ engine that will carry the claim
"no Leech tree of order 18 exists (or witness)". Two engine versions exist and both were audited:

| label | source | binary | role |
|---|---|---|---|
| **v1** | commit `78d940c` (= `8955bf1` for this file) | `bin/leech_search` (md5 `02eec864…`), built 13:33 | **the cluster/production run depends on this one** |
| **v2** | commit `4785a43` (`git show 4785a43:src/leech_search.cpp`, sha256[:16] `b5e80adf…`) | `bin/leech_search_v2` (not touched; I built my own copy) | fast path: component groups, 64-bit window domains, `--wcover 50`, `--look`, `--hallw 40` on by default |

Nothing under `src/` or `bin/` was modified. Referee code: `tests/referee_enum.py` (independent
enumerators), `tests/referee_diff.py` (differential harness; builds its own binaries into a scratch dir
from frozen source copies and also runs `bin/leech_search` read-only). Scratch helpers (star-Sidon and
Golomb brute forces) are quoted inline below.

Verdict legend: **VERIFIED** (proof re-derived AND exercised by SAT planted instances where possible) /
**BUG** (with counterexample) / **UNCLEAR** (cannot be validated empirically here; rests on a proof or on
literature values). Summary table at the end.

---

## 1. Forcing-lemma branching (`recV`) — VERIFIED

Claim implemented: at level `t` (all target values `< t` realised, `t` not realised), some **unassigned**
edge has weight exactly `t`.

Re-proof, including the edge cases asked about:
* Values realised so far are values of *completed* pairs (`rem[p]==0`); in any extension they stay
  the values of those pairs. Hence no unassigned edge can carry a weight `v < t` (it would duplicate the
  completed pair realising `v`). So all edges of weight `< t` are assigned.
* If `t` were realised by a path with >= 2 edges, every edge on it has weight `< t`, so all are assigned,
  the pair is complete and `t ∈ R` — contradiction. Hence `t` is the weight of an unassigned edge.
* Custom targets: values not in `fullM` are skipped by the `while` loop; an unassigned edge cannot take a
  non-target value (its own pair value), so the skip is safe.
* Termination: `t > N` means every target value is realised by a distinct completed pair; `|target| = P`
  forces all `P` pairs complete, i.e. all edges assigned — `nsol++` is a genuine labeling.
  `nAssigned == E` with `t <= N` is correctly dead.
* Completeness of the branch set: any solution's weight-`t` edge is unassigned and is tried unless a
  (sound) prune or `symOK` removes it; `allowed` is captured before recursion (scratch arrays are per node).

**grp rules (identical / superset unassigned-edge sets), exactly as implemented:**
* legacy `prunes()`: (a) `useGrp && !useFC`: hash of `(um<<8)|s` — two incomplete pairs with the same
  unassigned set and the same partial sum would get identical final values -> dead. Sound. *(Nit: the key
  packs `s[p]` into 8 bits; fine for NW=3 (`N<=190`), but in the `-DNW=8` test build `s` can exceed 255 and
  keys can collide -> spurious prune possible in `--no-fc` runs of the test binary only. Not production.)*
  (b) `useFC`: pairs with `rem==1` per edge (`sBits[e]`, duplicates -> dead), pairs with `rem>=2` bucketed by
  exact `um` (probing until `hkey>>8 == um`; duplicates of `s` -> dead). Sound. (c) 2-crossing forbid: pair
  `p` with set `{e,f}`, `q` with set `{e}`: `w_f != s_q - s_p` (`forb[f] |= sBits[e] >> s_p`) — correct
  direction. (d) `--grp2`: `p` with set `W`, `q` with `W\{f}` -> `w_f != s_q - s_p`, using `mbits` (partial
  sums per exact `um`, filled for all `rem>=2` pairs) — `list3` holds `rem>=3`, so `W\{f}` has `>=2` edges
  and lives in `mbits`; `rem==2` is handled by (c). Consistent.
* fast path (`assign2` merge + `prunesFast`): `G[a][b]` = partial sums of the group of pairs between
  components `a`,`b` (all share the unassigned set = quotient-tree path). On assigning `e=(a,b,wt)`: groups
  across `e` shift by `wt` (side test via `sideV[e]` and component ids being vertices — valid because a
  component never straddles an unassigned edge), then `(a,c)` and `(b,c)` merge, and an overlap of their
  partial sums is a duplicate final value -> dead. `unassign2` restores in reverse. The one-edge-difference
  forbid `w_e != s_near - s_far` (near = `(A, same side)`, far = `(A, other side)`) is the general
  superset rule; both bit-tricks (`ne >> f` and `reflectN(fa) >> (N-b)`, v2: `.win()` variants) compute
  `{b - f}` correctly, group bitsets only carry bits `<= N` (guaranteed by the `s[p] > N` rollback).
  All these are necessary conditions.

Empirical: every flag subset (including all-off legacy) reproduces the independent DFS counts on all
planted SAT instances (Section 7).

## 2. Bounds — VERIFIED (with two literature dependencies flagged)

* **Containment UB** `pairUB[q] = (s_x s_y)-th largest target value` (`N+1-s_x s_y` for the standard
  target): the `s_x s_y - 1` pairs strictly containing the path have strictly larger, distinct values.
  `ex/ey/sideOf` extraction checked on all cases (ancestor pair, equal depth, single edge -> `c_e`).
  Applied to completed pairs (`assign2`), edge domains (`epair`), Hall `u`. Correct for any distinct target.
* **`w_i + w_j <= N`** (`cap = N - max(wmax, k>=2 ? t : 0)`): any two edges lie on a common path; the
  other unassigned edge (exists iff `k>=2`) will get weight `>= t` (Section 1). Sound.
* **Calhoun `m1 <= floor((4n-1)^2/48)`** (`m1Bound`, standard target only): re-derived (heaviest edge `ab`,
  components of `k`, `n-k` vertices; `N >= m1 + (d1+d2)/2`, `d1 >= C(k,2)`, `max(d1,d2) >= C(k,2)+C(n-k,2)`)
  giving `m1 <= max_k floor(N - C(k,2) - C(n-k,2)/2)`; computed for `n=4..18`, equals the engine's closed
  form at every `n` (n=18: 105; n=4: 4 = tight on the known star). Applied to all edges (valid: `m1` is the
  max). **Cannot be exercised by planted instances** (`m1Bound = N` there); n=4,6 standard SAT instances
  pass through it. Status: proof-only.
* **Golomb LB** `pairLB = OGR(hop+1)`: sub-path sums are distinct -> vertices of the path are a Golomb
  ruler. Values `OGR(2..11) = 1,3,6,11,17,25,34,44,55,72` re-verified here by an independent brute force
  (`ogr.c`, seconds); the repo verified `<= 13` (`docs/sources/golomb.c`); **`OGR(14..17) = 127,151,177,199`
  are LITERATURE (Shearer / distributed.net)** and are used at n=18 for hop >= 13 pairs and for the
  diameter <= 14 filter (via `rootDead`). Also: `hop+1 > 17 -> pairLB = 2^20` (kills `P_18`, sound only for
  the standard target where `P_18` is known non-Leech; a hop-17 planted instance would be wrongly killed —
  test-only concern).
* **Degree filter** `OGR(d)+OGR(d-1)+2 <= (b_(1) b_(2))-th largest value` (`rootDead`, theory-notes
  Lemma 5b): see **BUG (theory)** below. As applied by the engine for `n<=18` it never kills wrongly.
* **Sum identity** (`useSum`, legacy path only): rearrangement bounds `minRem/maxRem` (largest `c_e` with
  smallest/largest missing values) and per-edge UB `(B - others)/c_e` with `others` = rearrangement minimum
  over the other `k-1` edges (prefix/suffix of `ms`). Correct. Edge weights are missing values (they are
  their own pair's value) — the premise holds.
* **Hall prefix/suffix counting**: legacy: `lb = max(s + pms[rem], pairLB, s + Σ lo_e)`, `u = min(s + Σ hi_e,
  pairUB)`; prefix (`#pairs with lb <= v >= #missing <= v`) and suffix; `#incomplete pairs = #missing`.
  Sound. Fast path: per component-group, `base = max(pms[r], distinctness-adjusted Σ sorted lo_e)`,
  `lb = s + base`; `ghi + base > N` dead; prefix only. v2 windowed Hall (`--hallw 40`): counts only
  `lb ∈ [t, t+HW]`; valid because every `lb >= t` and no missing value `< t`, so the window prefix is a
  restriction of the full prefix test (weaker, still sound); `cntLB[80]` with `HW <= 78` fits.
* **`--match` (Glover)** and **`--cover`**, **`--wcover`** (window-cover DFS: every missing value below the
  smallest multi-edge-pair LB must be an edge weight or a singleton value `w_e + s`, translates pairwise
  disjoint, `w_e` in the window domain; budget exhaustion returns *alive*; partial sums `> 63` cannot cover a
  window value because `w_e >= t`), **`--look`** (child's forced value `t'` must be placeable on some other
  edge with `t' ∈ dom_f` and disjoint translates; the child's domain is a subset of the parent's, argued
  in-line): all re-derived as necessary conditions. VERIFIED (and exercised: on planted instances v2 fires
  `cover` ~2.3k and `look` ~200 times per 22 instances with exact counts preserved).
* **Top-value structure** (`topOK`, Lemma 4a): four-point condition, redone for an arbitrary distinct
  target (`t1+t2 > t3+t4`, `t1+t3 > t2+t4`), so it is valid on planted instances too, where it is
  exercised. Ties impossible (distinct values). *(Nit: for `n=2`, `topv[1..2] = -1` and `R.test(-1)` reads
  out of bounds — irrelevant for n>=3.)*

## 3. Symmetry breaking — VERIFIED (complete and non-redundant)

Value mode: for each vertex, children with equal AHU canonical strings form groups; edge `e` in sibling
subtree `i` may be assigned only if some edge of sibling subtree `i-1` (including its top edge) is
already assigned; since weights are assigned in increasing order this is exactly `min w(subtree_{i-1}) <
min w(subtree_i)`. Bicentral case: `min w(half_1) < min w(half_2 \ central edge)` when the two halves are
isomorphic (`h1 == canon[c2]`, correct comparison of "c1 with its other children" vs "c2 with its
children"). Existence of a representative in every orbit: apply the permutations top-down (root first),
inner reorderings never change outer subtree minima. Uniqueness: automorphisms act freely on labelings
(distinct weights), so `count(sym) * |Aut| = count(nosym)` iff exactly one representative per orbit — this
identity holds on **every** planted instance in Section 7 (including the top-|Aut| trees of each order
8..12: spiders, brooms, symmetric bicentral trees, `|Aut|` up to 20000), for v1, v2 and `bin/leech_search`,
and for the standard target (`n=4`: 2/2 and 6/6 -> 1; `n=6` L6: 8/8 -> 1). Centers by leaf stripping
checked on the corner cases (P2, stars, P4). Edge/ff modes (`ltEdge`, `halfOK`) use the top-edge-weight
rule instead; also exact on all instances.

## 4. Taylor parity DP and top-value rule — VERIFIED

Parity: `#odd distances = a(n-a)` with `a` = number of odd-depth vertices from any root; per component of
the assigned forest the odd count is `odd` or `m-odd` depending on the (free) parity of the unassigned
path from the root — free bits because the quotient graph is a tree, so root parities of components are
independent. `reach` DP correct; `par_a<0` -> immediate UNSAT is correct (`a(n-a)` must equal the odd
count of the target). Ties: none. Note the rule almost never fires on planted SAT instances with the full
prune stack (domain rules subsume it); it does fire (thousands of times) with `--no-fc` / `--legacy --no-fc`
and on the standard target (`n=11`: 5354 kills in v1). The differential harness therefore includes
parity-skewed planted families (`par0/1/2`: 0/1/2 odd edge weights, so `a ∈ {0,1,2}`) and flag sets in
which parity is the only remaining rule; counts stay exact -> VERIFIED empirically as well.

## 5. BUG (theory, no engine consequence for n <= 18): Lemma 5(b) "incident weights form a Golomb ruler"

`docs/theory-notes.md` Lemma 5 (status PROVEN) says the incident weights `a_1<…<a_d` are a Sidon set and
"a Sidon set of size m has max−min >= OGR(m)". The Leech condition only gives a *weak* Sidon set (sums of
**distinct** pairs `i<j` distinct, and distinct from the elements); `2a_i = a_j + a_k` is **not**
excluded, and weak Sidon sets are not Golomb rulers. **Counterexample:** star `K_{1,7}` with weights
`{1,2,4,8,14,19,24}`: all 28 distances distinct (checked), `a_6 + a_7 = 43 < 44 = OGR(7)+OGR(6)+2`.
Exact minima of `a_{d-1}+a_d` over "star-Sidon" sets (brute force, `starsidon.c`, and independently in
Python for d<=9):

| d | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| true min | 3 | 6 | 11 | 19 | 31 | **43** | 63 | 80 | 110 | 138 | 169 |
| OGR(d)+OGR(d-1)+2 | 3 | 6 | 11 | 19 | 30 | **44** | 61 | 80 | 101 | 129 | 159 |

Consequences: (i) The lemma statement is false for `d=7` (and the "Sidon" claim in Lemma 5a needs the
qualifier *weak*). (ii) In the engine (`rootDead`) the rule fires only with `b_(1)b_(2)=1` for every
`n<=18` (enumerated), i.e. it is a pure "`OGR(d)+OGR(d-1)+2 > N`" max-degree kill; each such kill is
independently justified by the true minima above (`43 > 36` at n=9; `110 > 91`; `138 > 120`;
`169 > 153` for `d=12` at n=18, matching ledger L11). So **no unsound kill happens**, but the justification
must be changed to the exact star-Sidon minima (or L11), not Lemma 5b. Recommend fixing theory-notes and
filters F2 wording.

## 6. Cluster/production observations (v1 = `bin/leech_search`)

* Records without a JSON output line (parse failure `bad record`, `n > MAXV`) go to stderr, which the
  drivers discard; the shard runner would just leave the id undone. Any final claim needs an explicit
  coverage check (every id of the frozen `data/trees_18.jsonl` has exactly one non-UNKNOWN record; record
  the engine version/hash and the edge-list hash in each line — currently neither is recorded).
* `--no-top` disables both the top-value rule and the root filters, but the Golomb/containment checks in
  `assign2` and `m1Bound` are unconditional; there is no flag that yields a "pure forcing" search.
* v2 changes defaults (`--wcover 50 --look --hallw 40`); the cluster binary is v1, so v2's new code is
  not what the running campaign uses. Both audited; both exact on all instances.

## 7. Differential test results (`tests/referee_diff.py`)

Harness: `.venv/bin/python tests/referee_diff.py --src <frozen v2 src> --src <frozen v1 src> --nmax 10 --symn 12 --per 3 --cpsat 40`
(seed 11; ~10 min). Ground truth = `tests/referee_enum.py::count_dfs` (plain edge-by-edge backtracking over
target values, no forcing lemma, no engine rules), cross-checked on 40 random instances by an independent
CP-SAT enumeration model (`count_cpsat`, single worker) — always equal; also equal to the known-tree
counts at n=4,5,6 (P4: 2, K_{1,3}: 6, L6: 8 labelings).

Instance set (574): **all** topologies n=7..10 with planted distinct-distance targets (weights from
1..59 / 1..29 / 1..19, max value <= 190 so the NW=3 production build applies), the standard Leech target
for all topologies n=7..9 (81, all UNSAT — checked, not assumed), parity-skewed planted families with
0/1/2 odd edge weights (152), and a symmetry stress set: for each n=8..12 the 8 trees with the largest
|Aut| (<= 20000: spiders, brooms, symmetric bicentral trees) plus 6 random ones (55). 493 SAT instances.

Checks per binary (v2 `4785a43`, v1 `78d940c` rebuilt, and the production `bin/leech_search` md5
`02eec864…`): (1) `--count --no-sym` == DFS count; (2) `--count` x |Aut| (GraphMatcher enumeration) == DFS
count; (3) default run status SAT/UNSAT == (count>0) and every witness re-checked to realise the target;
(4) the same for 32 flag sets on v2 (every single `--no-*`, `--legacy` with every subset, all-off legacy,
`--cover`, `--match`, `--wcover 0/200/500`, `--no-look`, `--hallw 0/3/78`, edge/ff modes, parity-only
sets) and 17 flag sets on v1/production (incl. `--no-fc` sets where parity/sum/grp fire alone).

**Result: 0 discrepancies** across 574 instances x 3 binaries x (2 + 2 x #flagsets) runs. Prune categories
verified to fire on these instances (`-v` counters): fc/domain, hall (L and U), sum, grp, top, cover, look,
and parity (thousands of kills under `--no-fc` / legacy sets, 5354 kills on the standard n=11 target).

Standard target: v1 and v2 give UNSAT on all 47 (n=9) and 235 (n=11) topologies (v1 3.19M nodes / 5.0 s,
v2 2.44M nodes / 3.3 s), id-by-id equal to CP-SAT `results/order_9.jsonl` (47 INFEASIBLE), `order_11.jsonl`
(92 recorded, 85 INFEASIBLE + 7 UNKNOWN), and the drat-trim-VERIFIED SAT route `results/sat_order_9.jsonl`
(47/47) and `sat_order_11.jsonl` (235/235 UNSAT, all `VERIFIED`). n=4/6 standard: exactly the known trees
SAT with `count(sym)=1`, `count(nosym)=|Aut|` (2, 6, 8). (No `results/cpp_order_11_shard1.jsonl` exists.)

Caveat on what this does NOT test: the standard-target-only paths (`m1Bound`, `OGR(>=14)` values, the
`hop+1>17`/`d>=17` sentinels) are proof-only (Section 2); UNSAT-vs-UNSAT agreement cannot detect an
unsound prune, only SAT (planted) instances can, which is why the harness is planted-heavy.
A second seed (`--seed 23`, 560 instances, 479 SAT, v2 + production binary): again **0 discrepancies**.

## 8. Certificate story / what an auditor needs

An auditor cannot accept "UNSAT for 122k topologies" from node counts. Minimal scheme, in increasing
strength:

1. **Reproducibility envelope**: freeze `data/trees_18.jsonl` (hash), the engine source hash and build
   flags, the exact command line per shard; make the engine print `{"src_sha": …, "flags": …,
   "edges_sha": …}` on every line; a coverage script that proves each id has exactly one `UNSAT` record.
   Deterministic node logs are worthless as *proof* (they are only useful for re-running spot checks — do
   record `nodes` and re-run a random 1 % sample bit-for-bit).
2. **Two engines / two rule sets**: re-run every topology (or the hard ones) with `--legacy` (v1 rules)
   *and* the v2 fast path — different code for the same lemmas — plus `--no-parity`, `--no-top` variants on a
   sample; disagreements are bugs. Cheap.
3. **Remove the proof-only dependencies from the production run**: `m1Bound` and `OGR(14..17)`
   (literature) cost `<1 %` nodes; a build with `m1Bound = N` and `pairLB` limited to `OGR(<=13)` (or
   `<=11` re-verified here) removes them from the trust base entirely. Likewise run the 71 diameter>=15 and
   78 degree>=12 topologies with the engine instead of dropping them by filter (they are trivial).
4. **Independent DRAT certificates by cube-and-conquer** for an audit sample: use `--dump D K` (or a
   deterministic replay of the forcing-lemma tree to depth `D`, i.e. the assignment of the `D` smallest
   weights) as cubes; each cube = unit assumptions in `src/sat_encode.py`'s CNF, solved with cadical +
   DRAT and checked with drat-trim; the cube set is exhaustive by the forcing lemma (a one-paragraph
   proof) — the *engine's pruning is not trusted at all* in this route, only its branching order. Sample
   size: a few hundred topologies stratified by leaf count (all of the hardest few-leaf class if affordable),
   plus every topology that any variant run flagged UNKNOWN before its final rerun.
5. For a **SAT** outcome, the certificate is trivial (witness re-checked by two checkers) — already done.

## Summary table

| rule / component | verdict |
|---|---|
| forcing-lemma branching, termination, custom targets | VERIFIED |
| grp identical-set (legacy hash + fast merge), 2-crossing forbid, grp2 superset forbid, one-edge-difference forbid | VERIFIED (nit: 8-bit `s` in NW=8 test build) |
| containment UB, `w_i+w_j<=N`, per-edge sum UB, min/max sum | VERIFIED |
| Calhoun `m1` bound | VERIFIED by proof (closed form == derived max for n=4..18); not empirically testable |
| Golomb `pairLB` | VERIFIED for `OGR(<=11)` here (`<=13` in repo); `OGR(14..17)` LITERATURE (used at n=18) |
| degree root filter | engine kills sound for n<=18; **theory Lemma 5b BUG** (counterexample `K_{1,7}` weights 1,2,4,8,14,19,24) |
| Hall prefix/suffix (legacy, fast, windowed) | VERIFIED |
| Taylor parity DP | VERIFIED |
| top-value structure | VERIFIED (nit: n=2 OOB read) |
| symmetry breaking (siblings + bicentral, all modes) | VERIFIED (complete, exactly one rep per orbit) |
| `--wcover`, `--look`, `--cover`, `--match` | VERIFIED |
| certificate for an UNSAT verdict | UNCLEAR today — see Section 8 |
