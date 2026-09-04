# `depth_search` — a rooted-depth exact search engine for Leech trees

Pilot built 2026-09-01/02 in `theory-lab/depth_search/`.  Nothing outside this directory was
modified.  **No nonexistence result for `n = 25` is claimed anywhere below.**

| file | what it is |
|---|---|
| `depth_search.cpp` | the engine (C++17, single file, no dependencies) |
| `validate.py` | validation driver: runs `n = 2..11`, canonicalises witnesses up to isomorphism, compares with `data/known_leech_trees.json` |
| `validation_results.txt` | its output (all checks pass) |
| `nf_sweep.sh` | runs the complete normal-form sweep (all `r`, all `s`) for one order |
| `pilot_configs.txt`, `hoffman2_depth_search_array_slurm.sh` | Hoffman2 pilot array (22 tasks) |
| `pilot_n25_levels.txt` | raw `n = 25` level histograms quoted below |

Build: `g++ -O3 -march=native -std=c++17 -o depth_search depth_search.cpp`

---

## 1. Algorithm

A Leech tree of order `n` has all `C(n,2)` pairwise distances equal to `[1,N]`, `N = C(n,2)`.
Root it at any vertex `ρ`.  Then

```
d(u,v) = dep(u) + dep(v) - 2·dep(lca(u,v)).
```

The `n-1` numbers `dep(v)`, `v ≠ ρ`, *are* the distances from `ρ`, hence pairwise distinct and
in `[1,N]`.  So a rooted Leech tree has `n` distinct depths, and can be built by placing the
vertices in **strictly increasing depth order**: every ancestor is strictly shallower, hence
already placed, so the parent of a new vertex is always among the placed ones.  Conversely a
rooted weighted tree with distinct depths gives exactly one such sequence (sort by depth).
The enumeration is therefore a bijection — nothing is produced twice, nothing is missed.

Placing vertex `v` means choosing a depth `δ > dep(v-1)` and a parent `p < v`; then
`lcad[v][u] = (u==p ? dep(p) : lcad[p][u])` and the `v` new distances are `δ + off(u)` with
`off(u) = dep(u) - 2·lcad[v][u]`.  A *node* of the search tree is a consistent partial
placement; level `L` means "`L+1` vertices placed", so level `nv-1` nodes are exactly the
complete solutions and `LEVELS` prints the per-level counts.

State: `dep[]`, `par[]`, the `lcad` table, a `used` bitset over `[1,Vmax]`, and a `free`
bitset (`allowed & ~used`) for fast rank/select.

---

## 2. Symmetry breaking — why each choice loses nothing

**`--sym none`.** Root anywhere.  Complete, but each tree is found once per vertex orbit.

**`--sym w1` (default).**  `1` is a distance; in a positively weighted tree a path of length 1
is a single edge, and edge weights are themselves distances, hence pairwise distinct — so
there is exactly one edge `{a,b}` of weight 1.  Rooting at `a` gives `dep(b) = 1`, the smallest
possible positive depth, so `b` is placed first with parent `a`.  Every Leech tree is therefore
enumerated, exactly twice (once per endpoint of its weight-1 edge).  **Vertex 1 is pinned:
depth 1, parent 0** — this removes the entire level-1 branching (a factor `N` at `n = 25`) for free.

**`--sym diam`.**  The largest distance is `N`, realised by a unique pair `{a,b}`.  Then
`ecc(a) = N`, so `a` is an endpoint of a diametral path, hence a leaf.  Rooting at `a`:
`dep(b) = N` is the maximum depth, so `b` is the **last** vertex placed and its depth is pinned
to `N`; and since `a` is a leaf the root has exactly one child (vertex 1), so no `v ≥ 2` may
take parent 0.  Complete, twice per tree.

**`--sub-diam K` (only with `--sym diam`).**  Because `a` is a leaf, `[1,N]` is the *disjoint*
union of the depths (= distances from `a`) and `Spec(T-a)`.  Hence
`diam(T-a) = max([1,N] \ Depths)` and

```
diam(T-a) ≥ K  ⟺  [K,N] ⊄ Depths  ⟺  |Depths ∩ [1,K-1]| ≥ (n-1) - (N-K)
              ⟺  dep(v) ≤ K-1  for all  v ≤ (n-1) - (N-K).
```

At `n = 25, K = 284` this is exactly "`dep(v) ≤ 283` for `v = 1..8`".  *The hypothesis
`diam(T-a) ≥ 284` itself is taken from the project (`docs/checkpoint-2026-09-01-s1-top-block-crowding.md`,
`docs/fable-audit-report-2026-09-01.md`); it is **not** re-derived here, and every number
reported under `--sub-diam` is conditional on it.*

---

## 3. Prunes and their soundness

Throughout, `Vmax` is the largest admissible distance (`N`, or `δ` in normal-form mode) and
"allowed" is the target value set.

**[P0] Distance validity.**  Every new distance must be allowed and not yet used.
*Sound:* in a Leech tree all distances are distinct and inside the target set.  Since
`#pairs = |target|`, a complete placement realises the target exactly, so this test is both
necessary at every step and sufficient at the leaf.

**[P1] Offset distinctness (per candidate parent, before the depth loop).**  For a fixed parent
`p` the new distances are `δ + off(u)` with `off(u)` independent of `δ`.  If `off(u₁) = off(u₂)`
for `u₁ ≠ u₂` then `d(v,u₁) = d(v,u₂)` for **every** `δ`, so `p` is discarded in `O(v)` without
entering the depth loop.  *Sound:* two equal distances are forbidden.

**[P2] Ceiling cap `δ ≤ Vmax - G(p)`, `G(p) = max_u off(u)`.**  This is P0's upper test hoisted
out of the depth loop: the largest new distance is `δ + G(p)`.  `G(p) ≥ 0` because `u = root`
gives `off = 0`, so the cap never exceeds `Vmax`.

**[P3] Two-edge cap `δ ≤ dep(p) + Vmax - w_max`.**  *Sound:* for any two distinct edges `e, f`
of a tree there is a path containing both (take the endpoint of `e` farther from `f` and the
endpoint of `f` farther from `e`), so `w(e) + w(f) ≤ diam ≤ Vmax`.  The new edge weighs
`δ - dep(p)` and `w_max` is the largest weight already placed.

**[P4] Depth headroom.**  Depths are strictly increasing and bounded by `Vmax` (by `B-2` for
low vertices in normal-form mode), so at least one unit of room must be left per later vertex.

**[P5] Forcing / gap cap `δ ≤ dep(v-1) + q`.**  Let `D = dep(v-1)`, `k = nv - v` the number of
vertices not yet placed, and `q` the `(C(k,2)+1)`-st smallest value that is allowed and unused.
*Soundness.*  Because vertices are placed in increasing depth order, the placed set is exactly
`{vertices of depth ≤ D}`, and every unplaced vertex has depth `≥ δ`.  For a placed `u` and an
unplaced `w`, `lca(u,w)` is an ancestor of `u`, hence placed, hence of depth `≤ dep(u)`, so
`d(u,w) = dep(w) + dep(u) - 2·dep(lca) ≥ dep(w) - dep(u) ≥ δ - D`.  Therefore every target
value strictly below `δ - D` must be realised by a pair of two *unplaced* vertices, and there
are only `C(k,2)` such pairs, with distinct distances.  Hence
`#{unrealised target values ≤ δ-D-1} ≤ C(k,2)`, i.e. `δ ≤ D + q`.  This is the depth-order
analogue of the forcing lemma: at `k = 1` it says the last vertex must sit within `t_min` of
the deepest placed vertex, `t_min` the smallest missing value.
*Caveat handled in code:* in normal-form mode the holes `s+l` of the **not yet chosen** low
depths are still counted as free, so the free set over-counts what really must be realised;
`C(k,2)` is therefore replaced by `C(k,2) + #(low depths still to choose)`.  Without that
slack the prune is too strong and can lose solutions (this was a real bug, found and fixed
before any pilot number below was produced).

**[P6] Hall / capacity condition (`--hall`).**  Let the unplaced vertices have sorted depth
lower bounds `fut[1..k]` (`fut[i] = δ + i - 1` when unknown; in normal-form mode the whole top
block is known *exactly*).  A target value `≤ t` can be realised by `(u, w_i)` only if
`dep(u) ≥ fut[i] - t`, and by `(w_i, w_j)` only if `fut[j] - fut[i] ≤ t` when both depths are
known (counted conservatively otherwise).  Each unrealised target value `≤ t` needs its own
pair, giving `#{unrealised ≤ t} ≤ cap(t)` (plus the same hole slack as P5).  Sound by the same
lca argument as P5, of which this is a refinement.  Checked at the `--hall-max` smallest
unrealised values.

**[P7] Forced smallest edge weights (`--force-edges`, normal-form mode, `s ≥ 3`).**  *Forcing
lemma:* sort the (distinct) edge weights `w₁ < w₂ < …`; let `F` be the target set and `F_i` the
forest of the `i` lightest edges.  Then `w_{i+1} = min(F \ Spec(F_i))`: "`≤`" because `w_{i+1}`
is a target value that cannot be realised inside `F_i` (a path in `F_i` of that length would
duplicate the distance `w_{i+1}`), and "`≥`" because a path realising `min(F \ Spec(F_i))` must
leave `F_i`, hence contains an edge of weight `≥ w_{i+1}`.  For `i = 0,1` this gives
`w₁ = f₁ = min F` and `w₂ = f₂`.  In normal-form mode the holes of `F` are `s + L`, all `≥ s`,
so `s ≥ 3` forces `f₁ = 1, f₂ = 2` whatever `L` is.  The engine then demands an edge of weight 1
and one of weight 2 and prunes as soon as no remaining vertex could carry the missing weight
(exact once every remaining depth is known, i.e. in the top-block phase; conservative before).

**[P8] `δ` is attained: no low depth equals `B-1`.**  `δ` is *defined* as `diam(K) = max F`, and
the holes `s+l` are `≤ s+(B-1) = δ`, so `max F = δ` iff `B-1 ∉ L`.  Dropping this would only
make the sweep redundant across different `r`, never incomplete.

---

## 4. Normal-form mode (`--nf --r R --s S`)

Structure supplied by the project.  With `{a,b}` the unique pair at distance `N`, `x` the
neighbour of `a`, `s = w(a,x)`, `K = T - a` on `k = n-1` vertices rooted at `x`, `D` its depth
set and `δ = diam(K)`:

```
Spec(K) = [1,δ] \ (s + D)   exactly,     δ = C(k,2) + r,   m = k - r,
A = N - s,  B = A - m + 1,  D = L ⊔ [B,A],  |L| = r,  0 ∈ L,  L ⊆ [0, B-2].
```

So the search object is a rooted tree on `k` vertices whose `r` shallowest depths are free and
whose deepest `m` depths are the **forced consecutive block** `B, …, A`, with target
`F = [1,δ] \ (s+L)`.  The holes `s+l` are removed from `allowed` as each low depth is chosen
(and must not already be used).  For `n = 25` the project's results give `r ∈ [8,22]`,
`δ = 276 + r ∈ [284,298]`, `m = 24 - r ∈ [2,16]`.

**End-to-end correctness of this mode.**  If a normal-form run finds a complete `K`, then
`Spec(K) = F` (the `C(k,2)` distinct distances fill the `C(k,2)`-element set `F`), and attaching
a pendant vertex of weight `s` at `x` adds the `k` distances `s+D`.  Since
`F ⊔ (s+D) = ([1,δ] \ (s+L)) ⊔ (s+L) ⊔ [δ+1,N] = [1,N]`, **every normal-form solution is a
genuine Leech tree of order `n`.**  That makes the mode falsifiable at small orders, and it is
used as a test below.

---

## 5. Validation

`python3 validate.py` → `validation_results.txt`.  Witnesses are canonicalised up to
isomorphism of weighted trees and compared with `data/known_leech_trees.json`.

| n | `--sym none` | `--sym w1` | `--sym diam` | up to iso | expected |
|---|---|---|---|---|---|
| 2 | 1 | 1 | 1 | 1 | 1 (`L2`) |
| 3 | 3 | 2 | 2 | 1 | 1 (`L3`) |
| 4 | 8 | 4 | 4 | 2 | 2 (`L4_star`, `L4_path`) |
| 5 | 0 | 0 | 0 | 0 | 0 |
| 6 | 6 | 2 | 2 | 1 | 1 (`L6`) |
| 7–11 | 0 | 0 | 0 | 0 | 0 |

**ALL VALIDATION PASSED.**  The raw multiplicities are exactly as predicted by the symmetry
arguments of §2 (one rooted copy per vertex orbit for `none`; exactly two for `w1` and `diam`).
Every witness is additionally re-checked by an independent ancestor-walk recomputation of all
`C(n,2)` distances (`--verify`).

**Normal-form mode, independent checks.**

* `n = 6, r = 1, s = 8` returns exactly the `K` of `L6` rooted at `x`
  (`0-1:4 0-2:5 2-3:1 2-4:2`, depths `0 4 5 6 7`) — the hand-derived normal form.
* The full sweep over all `(r,s)` at `n = 6` returns exactly two solutions, both of which are
  `L6` minus one of its two admissible leaves.
* The full sweeps at `n = 9` and `n = 11` (all `r`, all `s`; 168 and 360 instances, run to
  completion) return **nothing** — as they must, since by §4 any solution would *be* a Leech
  tree of those orders.  This exercises the top-block bookkeeping, the hole logic and the
  target-set arithmetic end to end.

---

## 6. Scaling, and comparison with the forest engine

General mode, `--sym w1`, single core, Apple M4 under load:

| n | N | nodes | CPU | level counts (levels 0…n-1) |
|---:|---:|---:|---:|---|
| 7 | 21 | 3,811 | <0.01 s | 1 1 23 363 2239 1184 0 |
| 8 | 28 | 35,132 | 0.01 s | 1 1 33 758 8558 23191 2590 0 |
| 9 | 36 | 336,616 | 0.05 s | 1 1 45 1408 24585 161863 145824 2889 0 |
| 10 | 45 | 3,394,521 | 1.7 s | 1 1 59 2407 58985 693835 2094056 543205 1972 0 |
| 11 | 55 | 35,461,384 | 23–37 s | 1 1 75 3853 124992 2250485 14804764 17150528 1125953 732 0 |

`n = 12` was **not** run locally (projected ≈ 3.7·10⁸ nodes, ≈ 5 min > the 2-minute local
budget); it is queued on Hoffman2 (tasks `gen_n12`, `gen_n13`).  Growth per unit of `n`:
**9.2, 9.6, 10.1, 10.5** — still rising.

Forest engine, from `paper/main.tex` Table `tab:small`, same target `[1,C(n,2)]`:

| n | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|
| nodes | 123,309 | 704,494 | 4,178,290 | 25,486,327 | 162,497,458 | 1,096,039,152 | 7.88·10⁹ | 5.98·10¹⁰ |
| CPU | 0.05 s | 0.14 s | 0.9 s | 6.4 s | 44 s | 321 s | 1.7 h | 5–11 h |

Growth 6.5–7 per unit of `n`.  **At `n = 11` the depth engine visits 288× more nodes than the
forest engine, and the gap widens by a further ≈ 1.5× per unit of `n`.**  The reason is
structural, not an implementation detail: the forest engine's forcing lemma makes the *next
edge weight deterministic*, so it branches only over placements; the depth engine must branch
over a depth **and** a parent, and its P5 is only the weak "gap" shadow of the forcing lemma,
because depth order and weight order are different orders.

Normal-form sweep (all `r`, all `s`, every instance run to completion):

| n | instances | nodes | wall | factor |
|---:|---:|---:|---:|---:|
| 6 | 30 | 564 | 0.04 s | |
| 7 | 60 | 6,436 | 0.05 s | 11.4 |
| 8 | 105 | 80,734 | 0.06 s | 12.5 |
| 9 | 168 | 1,081,845 | 0.17 s | 13.4 |
| 10 | 252 | 14,727,658 | 6.1 s | 13.6 |
| 11 | 360 | 202,347,577 | 111 s | 13.7 |

≈ 0.55 µs/node.  The sweep is *more* total work than the undecomposed search at the same
order (the number of `(r,s)` instances grows like `O(n³)`), but it is embarrassingly parallel.

---

## 7. `n = 25` pilot

### 7a. Do the extra prunes help?  (measured on complete sweeps)

| variant | `n = 9` nodes | `n = 10` nodes | `n = 10` wall |
|---|---:|---:|---:|
| plain (P0–P5, P8) | 1,081,845 | 14,727,658 | 6.4 s |
| `--force-edges` (P7) | 1,077,594 (−0.4 %) | 14,719,769 (−0.05 %) | 6.9 s |
| `--hall` (P6) | 1,059,520 (−2.1 %) | 14,627,143 (−0.7 %) | 12.5 s (**1.9×**) |
| both | 1,055,273 (−2.5 %) | 14,619,161 (−0.7 %) | 14.4 s (**2.2×**) |

**The forcing-lemma anchor buys ≈ 0.05–0.4 % of the nodes and the Hall/capacity look-ahead
≈ 0.7 %, at roughly twice the wall time — i.e. net negative.  The benefit *shrinks* with `n`.**
Explanation: P0 (distinct + inside target) already subsumes almost all of what P6/P7 can say,
because in the depth-order enumeration the small target values are consumed by the shallow
levels long before the capacity bound becomes tight.  P7 cannot be turned into the forest
engine's real forcing lemma here, because that lemma prescribes the *next edge weight*, which
the depth order does not expose.

### 7b. Normal-form growth for `r = 10, 12, 16, 22` (`n = 25`, 10⁷-node cap)

Level counts are **DFS prefixes**, not full level counts — the run is aborted mid-tree, so
deep levels are undercounted and the trailing zeros mean "not reached yet", *not* "empty".

```
r=10 s=50   1 1 1 1 1 1 1 171 77225 8696354 1226244 0 …        (deepest level touched: 10/23)
r=10 s=150  1 1 1 1 1 1 1 227 62940 6990912 2945915 0 …        (10/23)
r=12 s=50   1 1 1 1 1 1 1 1 7 6769 619625 9178803 194789 0 …   (12/23)
r=12 s=150  1 1 1 1 1 1 1 1 81 13995 726006 8581766 678145 0 … (12/23)
r=16 s=50   1 1 1 1 1 1 1 1 1 755 89091 1680373 5137033 2783438 305393 3909 0 …  (15/23)
r=16 s=150  1 1 1 1 1 1 1 1 5 1887 155614 2459267 5957801 1408355 17054 10 0 …   (15/23)
r=22 s=50   1 1 1 1 1 1 1 1 1 530 67588 1414552 4935474 3134999 438544 8298 7 0 … (16/23)
r=22 s=150  1 1 1 1 1 1 1 1 5 1887 155614 2459267 5957801 1408355 17054 10 0 …    (15/23)
```

Observations.

* **All of the visible work is in the low (free-depth) half.**  For every `r` the budget is
  exhausted before the top block is reached: `r = 10` stalls at level 10 (the first top-block
  level), `r = 22` at level 16 of 21 free low levels.  The top-block structure removes the
  depth branching for the deepest `m` vertices, but those are the *cheap* vertices; the cost
  lives in the `r` low depths, and it grows with `r`.
* A single level-9 subtree of `(r = 10, s = 50)` — shard `0` of `20000` at split level 9,
  i.e. one subtree — exceeds **4·10⁸ nodes** without terminating.
* The low-phase depth cap is `B - 2 - (r-1-v) = 276 - s + v`, **independent of `r`**.  That is
  why large-`s` instances have identical histograms across `r` (e.g. `s = 250` gives
  `1 1 9 539 18574 348455 …` for `r = 10, 12, 16, 22` alike): for large `s` the low phase dies
  for reasons that do not see `r` at all.
* Only the extreme `s` complete inside 3·10⁶ nodes: `s = 260` (1,297,847 nodes) and `s = 270`
  (1,651 nodes), again identically for all `r`.  Everything in `s ∈ [1,255]` is open.

### 7c. Diametral-endpoint structure in general mode (2·10⁷-node cap)

```
--sym w1                     20,000,001 nodes  36.6 s   1 1 1 1 1 1 1 1 1 1 130 38569 1446004 8562387 8308565 1598442 45841 53 0 …
--sym diam                   20,000,001 nodes  34.2 s   1 1 1 1 1 1 1 1 1 1 243 56136 1661725 8621314 8177589 1451503 31432 49 0 …
--sym diam --sub-diam 284    20,000,001 nodes  36.2 s   (byte-identical to --sym diam)
```

* Rooting at a diametral endpoint instead of the weight-1 edge changes the prefix only
  marginally (level 10: 130 → 243; level 16: 45,841 → 31,432); both stall at level 17 of 24.
* **`--sub-diam 284` changes nothing at all.**  This is not a bug and is explained by §2: the
  constraint reduces to `dep(v) ≤ 283` for `v = 1..8`, and a depth-first search that takes the
  smallest admissible depth first reaches such branches essentially last, so the constraint is
  inert on any prefix of the size we can afford.  Stated as a constraint on the depth sequence
  alone it is extremely weak — it forbids only the single pattern `Depths ⊇ [284,300]`.
  It would have to be combined with something that acts on the *first* choices to matter.

---

## 8. Feasibility assessment for `n = 25`

**Method.**  All the extrapolations below are fitted on searches that were run *to completion*
(§6), and are stated with deliberately wide bars because the measured growth factor is itself
still rising at the largest order that fits in the budget.

**General mode.**  From `n = 11` (3.55·10⁷ nodes) with a per-unit factor `g ∈ [10.5, 13]`:

```
nodes(25) ≈ 3.55·10⁷ · g¹⁴  =  7·10²¹ … 1.4·10²³
CPU       ≈ 2–4 µs/node     →  4·10¹² … 2·10¹⁴ CPU-hours
```

**Normal-form sweep.**  From `n = 11` (2.02·10⁸ nodes over all `(r,s)`) with `g ∈ [13.7, 16]`,
scaled by ≈ 0.65 for the restriction to `r ∈ [8,22]`:

```
nodes(25) ≈ 1.1·10²⁴ … 1·10²⁵
CPU       ≈ 1–5 µs/node  →  3·10¹⁴ … 1·10¹⁶ CPU-hours
```

**Reference point.**  Extrapolating the *forest* engine from `n = 18` (5.98·10¹⁰ nodes) at its
own 6.5–7 per unit gives ≈ 3–5·10¹⁶ nodes, ≈ 2·10⁶–10⁷ CPU-hours — itself far out of reach,
and still **7 to 10 orders of magnitude cheaper than this design.**

### Verdict

**Infeasible with this design, by a very large margin — and, on the evidence here, structurally
rather than incidentally so.**  Concretely:

1. The depth-order enumeration is *strictly worse than the engine the project already has*, at
   every order where both were measured (288× at `n = 11`, widening ≈ 1.5× per unit of `n`).
   Its one real advantage — that depths are distinct and can be enumerated monotonically — is
   paid for by branching on a depth *and* a parent instead of on placements alone.
2. The forcing lemma, which is what makes the forest engine work, **does not survive the change
   of order**.  Its depth-order shadow (P5) only caps the depth *gap*, and the two look-aheads
   that do encode genuine forcing content (P6, P7) are worth `< 1 %` of the nodes at `n = 10`
   and less as `n` grows, while costing about 2× in wall time.
3. The top-block structure is real but is applied to the wrong half: it eliminates depth
   branching for the `m = 24 - r` deepest vertices, whereas every measured instance exhausts
   its budget inside the `r` free low depths.  Larger `r` — which is exactly the open regime,
   `r ∈ [8,22]` — makes this worse, not better.
4. The `diam(T-a) ≥ 284` hypothesis, in the only form it can take as a constraint on the depth
   sequence, is *inert* for this search.

**Where this design could still be useful.**  (a) As an independent cross-check on small and
medium orders — it reproduces the known trees at `n ≤ 6` and emptiness at `7 ≤ n ≤ 11` from a
completely different enumeration order than the forest engine, which is worth something for a
paper that rests on one engine.  (b) The normal-form mode is a cheap, *falsifiable* oracle:
by §4 any solution it reports is a genuine Leech tree, so it can be used to sanity-check
normal-form derivations at small orders (it already did, at `n = 9` and `n = 11`).
(c) The `(r,s)` decomposition is embarrassingly parallel and each instance is independent, so
if a future structural result cuts the *low* half — pinning several of the `r` low depths, in
the spirit of `theory-lab/s1_crowding`'s class-injectivity capacity bounds — this engine would
be a reasonable place to plug it in.  Nothing here suggests that raw search over the low half
can be made to work.

**No claim is made about the existence or nonexistence of a Leech tree of order 25.**

---

## 9. Cluster runs

Hoffman2 array `118739` (22 tasks) was submitted with `--nice=10000`, `--partition=campus`,
`--qos=campus24`, `--time=23:50:00`, `1 cpu`, `2G`, writing to
`$SCRATCH/leech-trees/theory-lab/depth_search/out/`.  Tasks: `r ∈ {10,12,16,22}` × `{plain,
force, hall, both}` each sweeping **all** `s` with a 2·10⁷-node cap, plus complete `n = 12`,
`n = 13` general-mode runs, an `n = 14` capped run, and capped `n = 25` general-mode runs for
`w1 / diam / diam+subdiam284`.  At the time of writing all 22 tasks were still `PENDING`
behind the ~100 running `s1dv7` jobs of the same user (QOS `MaxJobsPU=100`), so no cluster
results are included above; every number in this README is from complete local runs.  No job
submitted by anyone else was touched.

Reproduce locally:

```
g++ -O3 -march=native -std=c++17 -o depth_search depth_search.cpp
python3 validate.py                       # §5
./nf_sweep.sh 10                          # §6 normal-form sweep
./depth_search --order 25 --nf --r 16 --s 50 --no-witness --levels --nodes-limit 10000000
./depth_search --order 25 --sym diam --sub-diam 284 --no-witness --levels --nodes-limit 20000000
```
