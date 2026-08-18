# Theory notes — necessary conditions on Leech trees (order n, N = C(n,2))

Owner: theory branch. Machine checks: `src/theory_checks.py test` (all lemmas, brute force n<=7 exhaustive
over all weightings, n<=10 all topologies for the relaxations, plus random weighted trees).
Filters on the frozen n=18 list: `src/theory_checks.py filter18 -j 9` -> `results/theory_survivors_18.txt`,
per-topology detail `results/theory_filters_18.jsonl`.

Notation. T tree on n vertices, weights w_e in Z_{>0}; d(x,y) = sum of w_e on the x–y path; Leech means the
multiset {d(x,y)} = {1,…,N}. Consequences used everywhere: (i) all N distances are distinct; (ii) every value
1..N is attained; (iii) w_e are distinct (edges are pairs). "hop(x,y)" = number of edges of the x–y path.
For an edge e let s_e = size of one side, c_e = s_e (n − s_e) = number of pairs
whose path uses e. For a pair (x,y) with hop>=1 let e_x (e_y) be the first (last) edge of the path and s_x (s_y)
the number of vertices on x's side of e_x (y's side of e_y); s_x s_y = number of pairs whose path contains the
x–y path (including (x,y) itself).
OGR(m) = length of an optimal Golomb ruler with m marks (2:1, 3:3, 4:6, 5:11, 6:17, 7:25, 8:34, 9:44, 10:55,
11:72, 12:85, 13:106, 14:127, 15:151, 16:177, 17:199). Values for m<=8 are re-derived by brute force in
`test_ogr`; m>=9 are the published table (Shearer; distributed.net OGR project) — LITERATURE, used only in
lemmas 3, 5 and the relaxation.

Status labels: PROVEN (proof below) / CHECKED (brute force in theory_checks.py) / LITERATURE.

## Lemma 1 (first moment / cut identity). PROVEN, CHECKED
For any weighted tree, sum_{x<y} d(x,y) = sum_e c_e w_e. For a Leech tree this equals N(N+1)/2.
Proof. Exchange sums: each pair contributes w_e for every edge on its path; edge e lies on exactly c_e paths.

## Lemma 2 (second moment identity). PROVEN, CHECKED
sum_{x<y} d(x,y)^2 = sum_e c_e w_e^2 + 2 sum_{e<f} c_{ef} w_e w_f, where c_{ef} = number of pairs whose path
contains both e and f. Deleting e and f leaves three components; if a and b are the sizes of the two components
not lying between e and f then c_{ef} = a b (a path uses both edges iff its endpoints are in those two outer
components). For a Leech tree the left side is N(N+1)(2N+1)/6; likewise sum d^3 = (N(N+1)/2)^2 with
c_{efg} = a b when e,f,g lie on a common path (0 otherwise).
Proof. Expand (sum_{e in P} w_e)^2 and count paths containing e, resp. {e,f}. The a b formula: the path
x–y contains both e and f iff x and y are separated by both edges, i.e. lie in the two outer components.
Checked exactly on the five known trees and 300 random weighted trees (`test_moments`).
Use: exact pruning identities for the search (last edge determined by Lemma 1; quadratic check by Lemma 2).
Remark: the star K_{1,17} gives 15·sum a_i^2 + 693^2 = M2, integral, so no divisibility contradiction there.

## Lemma 3 (Golomb / hop bounds). PROVEN, CHECKED
(a) In a Leech tree (indeed in any tree with all distances distinct) the vertices of any path with k edges,
placed at their cumulative distances, form a Golomb ruler with k+1 marks; hence for every pair,
d(x,y) >= OGR(hop(x,y)+1). (b) The weighted length of every path is <= N (it is a distance), so the hop
diameter D satisfies OGR(D+1) <= N. For n = 18 (N = 153): OGR(16) = 177 > 153, so **D <= 14**.
(c) The largest distance N is attained by a pair of leaves.
Proof. (a) Sub-path sums of the path are distances of distinct pairs, hence distinct. (b) immediate.
(c) If d(u,v) is maximal and u had another neighbour u' off the path, d(u',v) = d(u,v) + w > d(u,v).
Checked: `test_golomb_lemma` (all Leech weightings n<=7; 300 random distinct-distance trees).
Filter F1 (topology): OGR(D+1) <= N.

## Lemma 4 (top values; containment bound). PROVEN, CHECKED
Let (u,v) be the pair with d(u,v) = N (leaves by 3c).
(a) The pairs realising N−1 and N−2 both meet {u,v}. Consequently every pair disjoint from {u,v} has
distance <= N−3.
(b) If d(u,y) = N−1 then y is a leaf, or y is the neighbour of v with w(yv) = 1 (and deg y = 2).
(c) If d(x,y) = N−j then s_x s_y − 1 <= j; equivalently, for every pair,
    **d(x,y) <= N + 1 − s_x s_y**  (containment bound), in particular w_e <= N + 1 − c_e for every edge.
    Also, weaker: deg x + deg y − 2 <= j; and #{pairs with both degrees <= m} >= m for all m (filter F5).
Proof. (a) Four-point condition: among d(u,v)+d(x,y), d(u,x)+d(v,y), d(u,y)+d(v,x) the two largest are
equal. If {x,y} ∩ {u,v} = ∅ and d(x,y) = N−j, the four cross distances are distances of four distinct
pairs different from (u,v),(x,y), so they are distinct values in {1..N}\{N, N−j}; two of them sum to at
most (N−1)+(N−2) = 2N−3 when j>=3 and at most (N−1)+(N−3) = 2N−4 when j<=2. For j = 1,2 this is
< 2N−j, so 2N−j is the strict maximum of the three sums — contradiction. (b) If y is not a leaf, take a
neighbour y' of y off the u–y path: d(u,y') = N−1+w(yy') <= N forces w = 1 and y' = v (the only pair with
value N); a second off-path neighbour would give another value >= N. (c) Every pair (z,z') with z on x's
side of e_x and z' on y's side of e_y has path containing the x–y path, so d(z,z') > d(x,y) unless
(z,z') = (x,y); there are s_x s_y − 1 such pairs, all with distinct values in (N−j, N], so s_x s_y − 1 <= j.
Since s_x >= deg x and s_y >= deg y the degree form follows; the count form: the pairs realising
N, N−1, …, N−m+1 all have both endpoint degrees <= m.
Checked: `test_topvalues` (a,b,c) and `test_lp_and_projection` (ii) (rank of d(x,y) <= N+1−s_x s_y on 300
random distinct-distance trees; on Leech trees rank = value).
Use: per-pair upper bounds in the relaxation (F4) and in the searches (edge domains w_e <= N+1−c_e; e.g. an
edge with c_e = 81 has w_e <= 73).

## Lemma 5 (Sidon at a vertex; degree bound). PROVEN, CHECKED
Let v have degree d, neighbours u_1..u_d, incident weights a_1 < … < a_d, branch sizes b_1..b_d.
(a) For any choice of one vertex per branch, the distances from v to the chosen vertices form a Sidon set
(all pairwise sums distinct) whose pairwise sums avoid the set; the same holds for the pendant weights at v.
(b) A = {a_1..a_d} is Sidon and a_{d−1} + a_d = d(u_{d−1},u_d) is a distance, hence
    **OGR(d) + OGR(d−1) + 2 <= a_{d−1} + a_d <= N + 1 − b_(1) b_(2)**,
where b_(1) <= b_(2) are the two smallest branch sizes. For n = 18: OGR(12)+OGR(11)+2 = 159 > 153, so
**max degree <= 11** (the naive Sidon-in-[1,N] bound only gives <= 15).
Proof. (a) Cross-branch distances are d(v,x)+d(v,y), and they are distances of distinct pairs, distinct also
from d(v,x). (b) A Sidon set of size m has max−min >= OGR(m) (it is a Golomb ruler with m marks), so
a_d >= 1 + OGR(d) and, applying this to A \ {a_d}, a_{d−1} >= 1 + OGR(d−1); the sum is the distance
d(u_{d−1},u_d) whose containment bound (Lemma 4c) is N + 1 − b_i b_j <= N + 1 − b_(1) b_(2).
Checked: `test_sidon` (Leech weightings n<=7 and 300 random distinct-distance trees: Sidon-ness, top-two
sum, the OGR gaps). Filter F2 (topology). Small n: kills the star K_{1,4} at n=5 and 2 of 6 at n=6 (the
known L6 survives).

## Lemma 6 (residues mod 4; Taylor parity as corollary). PROVEN, CHECKED — weight-level only
Root T anywhere, phi(x) = d(root,x) mod 4, eps(x) = phi(x) mod 2. Then
d(x,y) ≡ phi(x) + phi(y) − 2 eps(lca(x,y)) (mod 4), and for a Leech tree the number of pairs with residue
r is |{k<=N : k ≡ r mod 4}| (n=18: 38,39,38,38 for r=0,1,2,3). Reducing mod 2 gives Taylor: the number
of odd-depth vertices a satisfies a(n−a) = ceil(N/2) (a ∈ {7,11} for n=18).
Proof. d(x,y) = d(r,x)+d(r,y)−2 d(r,lca), and 2 d(r,lca) mod 4 depends only on the parity of d(r,lca).
Not a topology filter: phi is an arbitrary map V→Z_4 with phi(root)=0 (weights are free mod 4). Usable as
a redundant constraint in the CP-SAT/SAT models (like Taylor, one level finer). Checked `test_mod4`.

## Lemma 7 (real relaxation; projection bound). PROVEN, CHECKED
Let A be the (pairs × edges) path-incidence matrix, d = A w. For a Leech tree d is a permutation of
v = (1,…,N), hence (i) d ≺ v (majorization; equivalently d = X v with X doubly stochastic), (ii) each
d_P ∈ [OGR(hop_P+1), N+1−s_x s_y] (Lemmas 3, 4), (iii) w_e ∈ [1,N], (iv) sum d = M1 := N(N+1)/2, and by
Karamata (v) sum d_P^2 <= M2 := N(N+1)(2N+1)/6 with equality. Necessary condition F4: the convex set
{w : (i)-(iv)} is non-empty. Weaker closed form F3: min{ w^T A^T A w : 1^T A w = M1 } = M1^2 / ||P_A 1||^2
<= M2, i.e. the constant vector must be well approximated by a real tree metric of the topology.
Proof. All constraints hold for the true weights; F3 drops all but (iv), so its minimum is <= sum d^2 = M2.
Implementation: HiGHS convex QP minimising sum d^2 subject to (ii)-(iv) plus cutting planes for (i)
("sum of the s largest d_P <= N+(N−1)+…+(N−s+1)", separated by sorting; preloaded for the sets
{hop >= k}, {hop <= k}); early exit if the minimum exceeds M2 (Karamata). Every kill is re-verified by an
independent scipy/HiGHS LP cutting-plane formulation (`filter_lp`); solver disagreement => kept.
Checked: exact Leech weights satisfy every row; LP and QP agree on all topologies n<=10; F4 ⇒ F3;
majorization oracle equals the subset definition on random vectors (`test_lp_and_projection`).
Caveat: floating point (tolerance 1e-6..1e-7); a fully rigorous version would extract Farkas certificates
in rationals. F6 = F4 plus the disjunction over the leaf pair (u,v) realising N with Lemma 4(a) bounds
(pairs disjoint from {u,v} <= N−3); it never killed anything beyond F4 in samples.

## Lemma 8 (small-value / edge-shift facts, for the search). PROVEN (trivial), noted for the search
(a) Values 1 and 2 are edge weights (a 2-edge path weighs >= 1+2 = 3); value 3 is an edge weight or the
edges of weights 1 and 2 are adjacent; value k is realised by a pair with hop h only if OGR(h+1) <= k.
(b) For every edge e = (a,b) and every vertex x ∉ e: |d(x,a) − d(x,b)| = w_e (the two paths differ by e).
    So the weight-1 edge yields n−2 disjoint pairs of consecutive values, etc. — a propagation rule.
(c) The hop-diameter path is a Golomb ruler with D+1 marks and length <= N; for D = 14 (n=18) only the
    15-mark rulers of length 151..153 are possible (OGR(15) = 151), i.e. a handful of candidates — a
    natural first branching point for the C++ search on the surviving D=13,14 topologies.

## What does NOT work (recorded to save others time)
- Rearrangement on Lemma 1 alone (weights 1..17 on the largest cuts) never exceeds M1 for n=18: even the
  path only reaches ~6330 of 11781; the sum identity has slack, it is the *distribution* that bites.
- Karamata makes "min sum d^2 <= M2" automatic once d ≺ v is imposed, so second-moment reasoning adds
  nothing to the majorization LP; higher moments likewise (they are Schur-convex tests). Integer/parity
  refinements of the moments (mod 2,3,4) reduce to residue counts, i.e. Lemma 6, weight-level.
- Hall/interval matching of pairs to values with the [OGR, containment] windows: killed 2 of 3000 sampled.
- The disjunction over the diameter leaf pair (F6): no additional kills in samples.
- Residue-count constraints (Lemma 6) are not topological because weights are free mod m.
Real relaxations are inherently weak on bushy trees (a star-like topology admits nearly constant real tree
metrics); the strong topology kills come from Golomb (long paths) and Sidon (high degree). The remaining
reduction must come from weight-level search with Lemmas 3–6, 8 as pruning.

## Results on the frozen n=18 list (123,867 topologies; 735 s on 9 cores)
| filter | lemma | individual survivors | cumulative |
|---|---|---|---|
| F1 hop-diameter <= 14 (OGR(D+1) <= N) | 3 | 123,796 | 123,796 |
| F2 degree: OGR(d)+OGR(d−1)+2 <= N+1−b_(1)b_(2) (=> max deg <= 11) | 5 | 123,789 | 123,718 |
| F5 low-degree pair count | 4c | 123,867 | 123,718 |
| F3 projection bound M1^2/‖P_A 1‖^2 <= M2 | 7 | 123,573 | 123,490 |
| F4 majorization + Golomb + containment relaxation (QP, LP-verified kills) | 3,4,7 | – | 122,347 |
| F6 F4 + diameter-pair disjunction | 4a | – | **122,344** |
Survivor list: `results/theory_survivors_18.txt` (122,344 ids); per-topology flags in
`results/theory_filters_18.jsonl` (2 topologies where QP said infeasible but the LP re-check disagreed were
kept, conservatively). Survivors by hop diameter: 3:3, 4:254, 5:1987, 6:10248, 7:21987, 8:30198, 9:26792,
10:17806, 11:8906, 12:3302, 13:780, 14:81; by max degree 3..11: 10358, 48906, 36735, 16294, 6336, 2369,
889, 330, 127. Strongest single filter: F4 (kills 1,143 beyond F1/F2/F3, mostly hop diameter 12–14);
strongest closed-form: F3 (projection). Overall the topology reduction is only 1.2 % — the useful output for
the search is the weight-level constraint pack: per-pair windows OGR(hop+1) <= d(x,y) <= N+1−s_x s_y
(edges: w_e <= N+1−c_e), Sidon at every vertex, top-value structure (Lemma 4a,b), the exact moment
identities (Lemmas 1–2), residues mod 4 (Lemma 6), and the diameter-path Golomb ruler (Lemma 8c).
