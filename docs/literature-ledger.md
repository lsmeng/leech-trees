# Literature ledger: proven structural results on Leech trees usable as search pruning (target n = 18)

Compiled 2026-08-18. Every item carries one of three labels:

* **VERIFIED-BY-ME** - I read the source (or a faithful reprint) AND re-derived the proof, or re-proved it by an exhaustive computation in this repo.
* **LITERATURE-ONLY** - statement taken from a source I could read (or from an abstract), proof not re-derived / not checkable here.
* **UNCLEAR** - I could not read the primary text, or the printed argument has a step I could not reproduce.

Notation: n = order, S = C(n,2) (= 153 at n = 18), "diameter t" = number of **edges** on a longest path,
B_{r,s} = double star (centres u,v adjacent; r pendants at u, s at v), Delta = maximum degree.
Filter code: `src/filters.py` (one function per lemma, self-test `--selftest`, counts `--count data/trees_18.jsonl`).
Retrieved sources are archived in `docs/sources/`.

## 0. Sources: what was obtained and how

| # | Source | Obtained? | How / where |
|---|--------|-----------|-------------|
| 1 | Leech 1975, "Another tree labelling problem", Amer. Math. Monthly 82, 923-925 | **No** (JSTOR paywall) | Contents known only through SWZ 2005 p.3, Calhoun 2007 Prop 1.2, EJGTA 2020, cut-the-knot summary. Statements attributed to it below are labelled accordingly. |
| 2 | Taylor 1977, "Odd path sums in an edge-labeled tree", Math. Mag. 50(5) 258-259 | **No** (JSTOR) | Proof reprinted verbatim-in-spirit in SWZ 2005 Thm 1 and Calhoun 2007 Thm 1.3/1.6; also cut-the-knot page. Re-derived (L2). |
| 3 | Szekely, Wang, Zhang 2005, "Some non-existence results on Leech trees", Bull. ICA 44, 37-45 | **Yes** (author preprint) | `people.math.sc.edu/laszlo/leech7.pdf` is now 404; recovered from the Wayback Machine (2010 capture) -> `docs/sources/SWZ2005_leech7_preprint.pdf/.txt`. The C programs referenced in the paper (`www.math.sc.edu/~szekely/leechtree/`) also recovered from Wayback (2006) -> `docs/sources/SWZ_ninenode.c`, `SWZ_elevennode.c`. |
| 4 | Calhoun, Ferland, Lister, Polhill 2007, "Minimal distinct distance trees", JCMCC 61, 33-57 | **Yes** (Combinatorial Press open PDF, scanned; OCR'd with tesseract) | `docs/sources/JCMCC2007_Calhoun_*.pdf/_OCR.txt`. Key pages (Table 1, Thm 2.8, Summary) also read from page images. |
| 5 | Varghese, Lakshmanan, Arumugam 2020, "Two classes of non-Leech trees", EJGTA 8(1) 205-210 | **Yes** (open access PDF) | `docs/sources/EJGTA2020_*.pdf/.txt` |
| 6 | Luo, Yu 2024, "A graph labeling problem", Involve 17(2) 327-335 | **Abstract only** (MSP paywall; no arXiv version found via arXiv API / web search) | Abstract: "no diameter-3 Leech tree of order n >= 7, at most finitely many diameter-4 Leech trees; a result of SWZ on maximum degree is improved" (keywords: Sidon sets). Exact statements/bounds NOT available -> LITERATURE-ONLY. |
| 7 | Ozen, Wang, Yalman 2016, Integers 16 #A21 | **Yes** | `docs/sources/Integers2016_*.pdf/.txt` |
| 8 | Eldho (Merlin Mariya) & Lakshmanan 2024, Discrete Math 347(4) 113837, "On Leech labelings of graphs and some related concepts" | **Abstract only** (Elsevier paywall; no arXiv) | Extends Leech labelling to general graphs (Leech index, path number of wheels/unicyclic graphs). Nothing in the abstract about tree non-existence -> not a pruning source (L18). |
| 9 | Epoch AI FrontierMath page (leech-trees) | **Yes** | `docs/sources/EpochAI_FrontierMath_leech_trees_2026-08-18.txt` - problem statement only, "smallest open n = 18", asks for a construction; no mathematics. |
| 10 | P. Mark Kayll 2005, "A note on weak Sidon sequences", Discrete Math. 299, 141-144, DOI 10.1016/j.disc.2004.05.019 | **Yes** | Full text read through an ordinary open web copy; no subscription or workstation fallback used. Gives the Ruzsa bound `f(H)<=sqrt(H)+O(H^(1/4))` for weak Sidon sets. |
| - | Golomb ruler table (OEIS A003022; Shearer; distributed.net OGR) | used for L6 | m <= 13 re-verified here by `docs/sources/golomb.c`, `golomb2.c` (the m=14 search was stopped unfinished after ~40 min); m >= 14 literature. |

## 1. The ledger

### L1. Basic facts about the weights (VERIFIED-BY-ME)
*Statement.* In a Leech tree all n-1 edge weights are distinct positive integers (each edge is a path). For n >= 3 the weights 1 and 2 are both edge weights; 3 is either an edge weight or the sum of two adjacent edges of weights 1 and 2.
*Source.* EJGTA 2020 intro (p.206), SWZ 2005 p.3, Calhoun 2007 Lemma 2.6.
*Proof.* Any path with >= 2 edges has weight >= 1+2 = 3, so the distances 1 and 2 must be single edges. Distance 3 is a single edge unless the edges 1 and 2 are adjacent.
*Type.* WEIGHT constraint (also a symmetry-breaking anchor for a search: "where do edges 1 and 2 sit" is a 2-way case split: adjacent or not - exactly the split used in SWZ's code, `p2 = 1 or 15`).

### L2. Taylor's condition and the parity classes (VERIFIED-BY-ME)
*Statement.* If a Leech tree of order n exists then n = k^2 or n = k^2 + 2. More precisely n = k^2 when S is even and n = k^2+2 when S is odd; and if A, B are the vertex classes at even / odd weighted distance from a fixed vertex, then {|A|,|B|} = {k(k+1)/2 + p, k(k-1)/2 + p} where p = S mod 2 (Calhoun Prop 1.8, equivalent to Gibbs-Slater 1991).
*Source.* Taylor 1977 (not read); reprinted SWZ 2005 Thm 1 (p.2-3), Calhoun 2007 Thm 1.3, Thm 1.6 (generalisation to forests/graphs with a "Taylor colouring"), Prop 1.8.
*Proof (re-derived).* d(x,y) = d(x,z)+d(y,z) mod 2 in a tree. Fix v; A = even class, B = odd class; a distance is odd iff its ends are in different classes, so #odd = |A||B|. The set {1..S} has ceil(S/2) odd members: 2|A||B| = S (S even) or S+1 (S odd). Then (|A|-|B|)^2 = n^2 - 4|A||B| = n - 2p, i.e. n = k^2 + 2p with k = |A|-|B|. Solving |A|+|B| = n, |A|-|B| = k gives Prop 1.8. The remark in SWZ that "n = k^2 iff S even" adds nothing: for n = k^2, S = k^2(k^2-1)/2 is always even, for n = k^2+2, S = (k^2+2)(k^2+1)/2 is always odd (checked k = 1..4).
*At n = 18.* 18 = 4^2 + 2, S = 153 odd, so |A| = 11, |B| = 7 (77 odd distances, 76 even). This is the constraint already implemented in `solve_v2` (README "CORRECTION" line: it constrains the parity pattern of the WEIGHTS, not the unweighted bipartition).
*Type.* Order filter (passes at 18) + WEIGHT parity constraint. Not a topology filter.
*Calhoun Thm 2.2* (Taylor for distinct-distance trees with maxdist d: a^2 + 2(u-v+p) = n where u,v = # even/odd missing values below d) - read, proof checked (it is Thm 1.6 applied to the tree plus isolated edges carrying the missing values). Not needed for the exact Leech question at n=18. VERIFIED-BY-ME, unused.

### L3. Paths: P_n is a Leech tree iff n <= 4 (VERIFIED-BY-ME)
*Source.* Leech 1975 (noted without proof, per SWZ); proof in SWZ 2005 p.3; Calhoun 2007 Prop 1.2 (via Golomb rulers: a perfect Golomb ruler exists only for <= 4 marks).
*Proof (re-derived).* The whole path must be the unique path of weight S = C(n,2); its n-1 distinct positive weights sum to S = 1+2+...+(n-1), so the weights are exactly {1,...,n-1}. Edge 1 can be adjacent only to edge n-1 (else 1 + w < n repeats an edge weight); edge 2 likewise can be adjacent only to n-1 (1+(n-1) = n already used, and 2 + w <= n for any other w). So n-1 has neighbours 1 and 2 and nothing can be attached beyond 1 or 2 without repeating: n-1 <= 3.
*Type.* TOPOLOGY filter (`passes_not_long_path`). Kills 1 topology at n = 18. Also killed by L5/L6.

### L4. The weight-forcing lemma (VERIFIED-BY-ME) - the central search principle
*Statement (Calhoun Lemma 2.6; SWZ "Find-Next-Weight").* Let w_1 < w_2 < ... < w_{n-1} be the edge weights of a Leech tree (or perfect distance forest). For each k, w_k equals the least positive integer that is NOT a distance in the sub-forest formed by the edges of weights w_1..w_{k-1}.
*Proof (re-derived).* Let m_k be that least missing integer. If w_k < m_k then w_k is already a distance in the sub-forest, repeated. If w_k > m_k then every path containing an edge of weight >= w_k has weight > m_k, and m_k is not realised in the sub-forest, so m_k is never a distance. Hence w_k = m_k.
*Consequences.* w_1 = 1, w_2 = 2, w_3 = 4 if edges 1,2 are adjacent else 3. A labelling is completely determined by the ORDER in which the edges receive weights (a permutation of the edges) - this is what SWZ 2005 Sec.3 and Calhoun Alg 2.7 exploit, and what `leech_labelings_of_topology` in `src/filters.py` implements. Note (Calhoun): the lemma is false for graphs with cycles.
*Type.* WEIGHT / search-order constraint. Not a topology filter, but the strongest known pruning device (it turns the labelling search of a fixed topology into a search over edge orderings with forced values).

### L5. SWZ Theorem 2: no very long paths (VERIFIED-BY-ME, exact finite form derived)
*Printed statement.* "If there is a Leech tree on n vertices, then it has no paths longer than n/sqrt2 (1+o(1))" (SWZ 2005 Thm 2, p.4; quoted as Thm 1.1 in EJGTA 2020, and as "a Leech tree cannot contain a long path" in Ozen-Wang-Yalman 2016 p.3 with [5] = SWZ).
*Exact form (re-derived).* Let a path have t edges a_1..a_t inside a Leech tree of order n. For 1 <= k <= t, the N_k = tk - C(k,2) sub-paths consisting of 1..k consecutive edges have pairwise distinct positive weights, so their total is >= N_k(N_k+1)/2. On the other hand each a_i lies in at most j+1 windows of j+1 edges, so sum_i (a_i+...+a_{i+j}) <= (j+1) sum_i a_i <= (j+1) S (the whole path is itself a distance), and summing over j = 0..k-1 the total is <= C(k+1,2) S. Hence
  N_k (N_k + 1) / 2 <= C(k+1,2) * C(n,2)   for every k <= t.
Choosing k ~ sqrt n gives SWZ's asymptotic; for a fixed n one just tests all k (`swz_path_ok`).
*At n = 18.* t = 16: k = 2 gives N = 31, 496 > 3*153 = 459 - violated. t = 15 satisfies all k (k = 3: 903 <= 918, tight). So diameter <= 15. The full path P_n violates the inequality iff n >= 7 (k = 2: n^2 - 7n + 6 <= 0), so at n = 5, 6 the path is killed only by L3.
*Type.* TOPOLOGY filter (`passes_swz_long_path`). Kills 9 topologies at n = 18 (diameter 16: 8, diameter 17: 1). Subsumed by L6.

### L6. Golomb-ruler diameter bound (argument VERIFIED-BY-ME; ruler values LITERATURE for >= 14 marks)
*Statement (this project, folklore).* The t+1 vertices of a longest path (or of any path) in a Leech tree have pairwise distinct distances, all <= S, so they are the marks of a Golomb ruler of length <= S. Hence t + 1 <= max{m : G(m) <= S} where G(m) is the optimal Golomb ruler length.
*Values.* G(1..19) = 0,1,3,6,11,17,25,34,44,55,72,85,106,127,151,177,199,216,246 (OEIS A003022). I re-verified G(m) for m <= 13 by exhaustive search (`docs/sources/golomb.c`, `golomb2.c`: G(13) = 106 confirmed with 1.9e9 nodes / 147 s); the m = 14 run (L <= 126) was stopped unfinished after ~40 min; G(15) = 151, G(16) = 177 are literature (Shearer's exhaustive tables 1990s; distributed.net OGR confirmations).
*At n = 18.* S = 153: G(15) = 151 <= 153 < 177 = G(16), so t + 1 <= 15, i.e. **diameter <= 14**.
*Type.* TOPOLOGY filter (`passes_golomb_diameter`). Kills 71 topologies (diameters 15, 16, 17: 62 + 8 + 1). Strictly stronger than L5.
*Note.* Calhoun 2007 Prop 1.2 uses the same Golomb link for the path case only.

### L7. Diameter <= 3: only the five known trees (VERIFIED-BY-ME by independent exhaustive search)
*Statement.* The star K_{1,n-1} is Leech only for n <= 4 (edge weights forced 1,2,4, then 7, then 10 collides: 1+10 = 4+7). The double star B_{r,s} (r,s >= 1) is Leech iff it is B_{1,1} (n=4) or B_{2,2} (n=6). Hence for n >= 7 every Leech tree has diameter >= 4.
*Sources.* Stars: SWZ 2005 p.4 (weights 1,2,4,7 fail: 10 missing; 1,2,4,7,10: 11 twice), Calhoun 2007 Prop 2.10, cited by Ozen-Wang-Yalman Prop 2 proof. Double stars: Calhoun 2007 Prop 2.11 (finite forced-weight search tree, Fig. 10), Varghese-Lakshmanan-Arumugam 2020 Thm 2.1 (hand case analysis, pp.207-208), Luo-Yu 2024 (abstract: "no diameter-3 Leech tree of order n >= 7").
*My verification.* `no_leech_double_star(n)` runs the forced-weight DFS (L4) over the star and all B_{r,s} for 7 <= n <= 18, with symmetry breaking between pendant edges at the same centre. None admits a Leech labelling; the same engine finds B_{1,1}, B_{2,2}, K_{1,3} at n = 4, 6. I also read the EJGTA case analysis (Cases 1, 2a-c) - it is the same forced-weight tree, done by hand.
*Type.* TOPOLOGY filter (`passes_diameter_ge_4`). Kills 9 topologies at n = 18 (1 star + 8 double stars).

### L8. EJGTA 2020 Thm 3.1: path plus a pendant at v_{m-1} (VERIFIED-BY-ME)
*Statement.* Let G_m be P_m = (v_1..v_m) with one extra pendant vertex attached at v_{m-1} (order m+1, diameter m-1). Then G_m is not a Leech tree for m >= 4. Together with L3, K_{1,3} is the only Leech tree of diameter n-2.
*Source.* EJGTA 2020, Lemma 3.1 (the 2-edge path at the fork has weight < S - 85 for m >= 17; Observation 3.1: only < S - 6 is needed, valid for m >= 9), Thm 3.1 (pp.208-209): the maximal paths P_m, P_m', and the fork; one of P_m, P_m' has weight S; then S-1, S-2, ... are forced onto specific sub-paths and each case ends in a repeated distance.
*My verification.* Read the case analysis (consistent). Exhaustive forced-weight search confirms no Leech labelling of G_m for orders 5..11 (`_selftest` item 4).
*Type.* TOPOLOGY filter (`passes_ejgta_broom`), kills exactly 1 topology; at n = 18 already killed by L5/L6 (diameter 16).

### L9. SWZ Theorem 3: max degree <= (sqrt(3/8) + o(1)) n  (UNCLEAR)
*Printed statement (SWZ 2005 p.4-5).* In a Leech tree the maximum degree d satisfies d <= (sqrt(3/8) + o(1)) n.
*Printed proof (as I read the preprint).* Vertex v of degree d, W = incident weights, D = neighbours; intervals I_1 = [1, S/3), I_2, I_3 = (2S/3, S]; i_l = |W cap I_l|; Z = distances not between two neighbours, j_l = |Z cap I_l|. (6) C(i_1,2) + j_1 >= S/3; (7) C(i_2,2) + j_3 >= S/3; (8) j_1+j_2+j_3 <= S - C(d,2); then (9) i_l^2/2 >= d^2/2 - n^2/3 + O(n) for l = 1,2, (10) d >= i_1 + i_2 >= 2 sqrt2 sqrt(d^2/2 - n^2/3), "solving gives d <= (sqrt(3/8)+o(1)) n".
*Problems.* (a) I cannot justify (7): a distance in I_3 = (2S/3, S] can be the sum of a small and a large incident weight (e.g. 1 + 150), so C(i_2,2) does not obviously bound the number of neighbour-neighbour distances landing in I_3, whatever I_2 is. (b) Solving (10) as printed gives d^2 <= 8n^2/9, i.e. d <= 0.943 n, not sqrt(3/8) = 0.612. Either the interval definitions were garbled in the preprint or a step is missing. (c) The o(1) is not quantified, so even the printed bound is unusable at n = 18 (sqrt(3/8)*18 = 11.02).
*Status.* UNCLEAR. Not used. Replaced by L11 (exact search), which happens to give Delta <= 11 at n = 18.
*Luo-Yu 2024* claim to improve this theorem (abstract, "Sidon sets") - LITERATURE-ONLY, text not accessible.

### L10. Luo-Yu 2024 (Involve 17(2)): LITERATURE-ONLY
Abstract only: (i) no diameter-3 Leech tree of order n >= 7 (independent proof of L7); (ii) at most finitely many diameter-4 Leech trees; (iii) improved max-degree bound. No explicit finite bound is available to me for (ii) or (iii); Calhoun 2007 Sec 2.6 shows why the forced-weight search tree is INFINITE for diameter 4 (Fig. 11: for every a >= 2 a distinct-distance diameter-4 tree on 2a+1 vertices lies in the search tree), so (ii) needs a genuinely different argument. Diameter-4 topologies at n = 18: 280 - all still survive here.

### L11. Star-Sidon max degree bound: Delta <= 11 at n = 18 (VERIFIED-BY-ME, exhaustive search)
*Statement (this project; the natural finite version of the idea behind L9/L10).* Let v have degree d with incident weights w_1 < ... < w_d. The d edge weights and the C(d,2) neighbour-neighbour distances w_i + w_j are d + C(d,2) pairwise distinct integers in [1, S]. Define D_max(S) = the largest d for which such a set exists (distinct elements, all pairwise sums (i<j) distinct, no sum equal to an element, everything <= S). Then Delta <= D_max(S).
*Computation.* Exhaustive DFS in increasing order (`docs/sources/stardeg.c`; Python re-implementation `star_sidon_feasible` re-verifies n <= 12). Results, n : D_max = 3:2, 4:3, 5:3, 6:4, 7:5, 8:5, 9:6, 10:7, 11:7, 12:8, 13:8, 14:9, 15:9, 16:10, 17:10, **18:11** (d = 12 at S = 153 exhausted after 8.6e8 nodes; d = 11 witness {1,2,4,7,12,23,32,41,56,70,83}). Sanity: L4_star (weights 1,2,4, S=6) and L6 (centre weights 1,2,5, S=15) satisfy it.
*Type.* TOPOLOGY filter (`passes_max_degree`). Kills 78 topologies at n = 18 (max degree 12..17: 47+19+7+3+1+1).
*Possible strengthening (not done).* The same "sub-shape must be a distinct-distance tree with maxdist <= S" test can be run for double stars B_{a,b} (adjacent degree pairs), spiders, etc. A first attempt (`dstar.c`) for B_{8,4} at S = 153 did not finish in 10 min; needs a smarter search (assign large values first / counting bounds). Calhoun's M(m) values (M(10) = 50, M(16) >= 121, M(17) >= 139) are all < 153, so the generic "any m-vertex subtree" version gives nothing at n = 18.

### L12. Calhoun Thm 2.8: largest weight m_1 <= floor((4n-1)^2/48) (VERIFIED-BY-ME)
*Proof (re-derived).* Remove the heaviest edge e = ab (weight m_1): components T_1 (k vertices, containing a) and T_2. Let d_1, d_2 be their maximum internal distances; by the triangle inequality some x in T_1 has d(x,a) >= d_1/2 and some y in T_2 has d(y,b) >= d_2/2, so S >= d(x,y) >= m_1 + (d_1+d_2)/2. Distances inside T_1 are C(k,2) distinct positive integers so d_1 >= C(k,2); the C(k,2)+C(n-k,2) distances inside T_1 u T_2 are distinct so their maximum, WLOG in T_2, is >= C(k,2)+C(n-k,2). Hence m_1 <= S - C(k,2) - C(n-k,2)/2 for the actual k, so m_1 <= max_k [S - C(k,2) - C(n-k,2)/2] = (4n-1)^2/48 (real maximum at k = (2n+1)/6).
*At n = 18.* m_1 <= 105 (integer k = 6 attains 105 exactly). Tight check: n = 4 gives 4 (L4_star has weight 4).
*Type.* WEIGHT constraint (upper bound on every edge weight; also each edge weight <= 105 can be fed to a solver as domain bound).

### L13. Calhoun Thm 2.9: second-largest weight m_2 <= floor((S-1)/2) (VERIFIED-BY-ME) + generalisation
*Proof.* Any two edges of a tree lie on a common path, so m_1 + m_2 <= S; with m_2 < m_1, 2 m_2 + 1 <= S. At n = 18: m_2 <= 76. General form (same proof): for ANY two edges w_i + w_j <= S, and the weights of any set of edges lying on a common path sum to <= S.
*Type.* WEIGHT constraint.

### L14. Non-existence at n = 9, 11, 16 and how it was computed (LITERATURE, computer; n = 9 also OBSERVED here)
* n = 9: Shen Lin's computer search reported by Taylor 1991 (Discrete Math 93, 167-168; not read; cited by Calhoun p.35); SWZ 2005 Thm 4 (their own program); this repo's CP-SAT over all 47 topologies (README).
* n = 11: SWZ 2005 Thm 4; Calhoun 2007 Sec 2.2.
* n = 16: Calhoun 2007 Sec 2.2/Table 1 ("Computer Search", lower bound M(16) >= 121 > 120).
*SWZ's method (paper p.6-7 + recovered source `SWZ_ninenode.c`, dated 2004-01-27, author Yong Zhang).* Backtracking over a 9x9 (11x11) adjacency matrix indexed by the 36 (55) upper-triangular positions. Edge weights handled in increasing order and FORCED by `nextvalue_matrix` (= L4). Edge 1 fixed at position (0,1); edge 2 either adjacent (`p2 = 1`, then v3 = 4) or disjoint (`p2 = 15`, then v3 = 3) - both blocks present in the code; small hand-derived position restrictions for the third edge (`p3 in {2,9,15,21}`); nested loops p4..p8 over all remaining positions with cycle check (`Check-Validity`), then all-pairs distance matrix (matrix powers) and duplicate check (`Is-Valid`). No isomorph rejection beyond those anchors, no runtime stated. "Wayne Goddard independently arrived at the same computational results" (p.7).
*Calhoun's method (Alg 2.7, p.42-43).* DFS whose nodes are weighted FORESTS: the next edge gets the forced weight (Lemma 2.6) and is added either (1) joining two components, (2) attaching a new vertex, or (3) as a disjoint new edge; prune when a distance repeats, exceeds S, or the vertex count exceeds n. "No node of the search tree is equivalent to any other node." Same algorithm with gaps allowed computed M(n) for n <= 10 and lower bounds for 11 <= n <= 17 (Table 1). No runtimes given. Their summary item 1 says "the only perfect distance trees with n <= 24 vertices are those in Figure 1" but the abstract, Table 1 (n = 18: lower bound 153 justified only by Prop 1.1) and every later paper say n < 18; I treat "24" as a misprint - **n = 18 is open**.
*Type.* Not a filter at n = 18; establishes that 18 is the smallest open order (with L2).

### L15. Calhoun Table 1 lower bounds M(n) (LITERATURE-ONLY, computer). Not usable at n = 18 (all < 153).

### L16. Ozen-Wang-Yalman 2016 (VERIFIED-BY-ME, no pruning value)
Thm 1: a Leech tree T yields a leaf-Leech tree T^e (subdivide edges by weight, add a pendant to every original vertex) - trivial from d(v_i,v_j) = 2 + d_T(u_i,u_j). Thm 2: converse for trees without "irreducible" vertices. Prop 2/3 (no starlike / caterpillar leaf-Leech trees with > 4 leaves) rest on "[5]": "no Leech star other than Figure 1" and "no Leech paths [beyond n <= 4]" - consistent with SWZ p.3-4 (L3, L7). Nothing about degrees/leaves of Leech trees themselves.

**LITERATURE terminology note.** Section 4, Fig. 5 calls the order-5 tree with
edge weights `1,2,3,7` an “almost Leech tree”: 6 is the only value missing from
`{1,...,10}`. The paper presents this example and says the general packing
optimization is not explored there; it gives no classification or constant-
defect theorem. This repo therefore uses the more precise term *prefix defect*
for `binom(i,2)+1-p`, rather than identifying the corridor core with the
literature's informal “almost Leech” example.

### L17. SWZ Sec 4, Buneman 4-point condition (VERIFIED-BY-ME reading; not a filter)
Any tree metric satisfies the 4-point condition; SWZ's Conjecture 2 (no metric on n > n_0 points with distance set {1..S} satisfies it) is refuted by their own half-integer-weight example (Fig. 3, p.8-9). So metric-space arguments alone cannot settle Leech's problem; integrality is essential.

### L18. Eldho-Lakshmanan 2024 (Discrete Math): LITERATURE-ONLY / not relevant
Abstract: Leech labelling of general graphs, Leech index, path number of wheels and unicyclic graphs. Not a source of tree non-existence results.

### L19. FrontierMath page: statement only; confirms "smallest open n = 18"; no structural results.

### L20. What is NOT in the literature (as far as I could read)
* No proven bound on the NUMBER OF LEAVES.
* No proven finite max-degree bound at n = 18 other than the star exclusion (L11 above is new here, though probably close to what Luo-Yu did).
* No result on which edge carries weight 1 or 2 beyond L1/L4 (in the five known trees weight 1 is always pendant, but I see no proof that this must hold).
* No diameter-4 or diameter-5 exclusion with an explicit bound available.
* No published runtimes / node counts for the n = 11, 16 searches.

### L21. Weak Sidon asymptotic and the root-arm application

*Literature theorem.* For a weak Sidon set
`0<=a_1<...<a_d<=H`, meaning that the sums `a_i+a_j` with `i<j` are all
different, Kayll gives an alternate proof of Ruzsa's bound

```text
d<=sqrt(H)+O(H^(1/4)).
```

Source: P. Mark Kayll, “A note on weak Sidon sequences,” *Discrete
Mathematics* 299 (2005), 141--144,
[DOI 10.1016/j.disc.2004.05.019](https://doi.org/10.1016/j.disc.2004.05.019).
The asymptotic theorem is labelled **LITERATURE** in this project.

*Project application.* In the current endpoint terminal, choose one farthest
vertex in every component of the lower core `C_0-v`.  Their distinct
`v`-depths have pairwise sums equal to cross-arm distances, hence form a weak
Sidon set after translation into `[0,h-1]`.  Therefore the number `d_v` of
root-incident lower-core arms is at most `n/2+O(sqrt(n))`, and at least
`n/2-O(sqrt(n))` lower-core edges are not incident with `v`.  This application
and the exact finite difference inequality in (FW178b) are
**VERIFIED-BY-ME / OBSERVED conditional all-order**, not literature claims.
They do not bound the total number of leaves of an arbitrary tree and do not
exclude the remaining terminal by themselves.

## 2. Survivor counts at n = 18 (123,867 topologies, `data/trees_18.jsonl`)

`.venv/bin/python src/filters.py --count data/trees_18.jsonl` (self-test passes: 5 known trees accepted; exhaustive n <= 8 search reproduces exactly the five known trees and no filter kills a Leech-admitting topology).

| Filter | Lemma | killed | survivors |
|---|---|---|---|
| F1 not_long_path | L3 | 1 | 123,866 |
| F2 diameter >= 4 | L7 | 9 | 123,858 |
| F3 SWZ long path (exact) | L5 | 9 | 123,858 |
| F4 Golomb diameter <= 14 | L6 | 71 | 123,796 |
| F5 EJGTA broom | L8 | 1 | 123,866 |
| F6 max degree <= 11 | L11 | 78 | 123,789 |
| **combined** | | **152** | **123,715** |

Diameter histogram at n = 18: 2:1, 3:8, 4:280, 5:2015, 6:10263, 7:21990, 8:30198, 9:26793, 10:17843, 11:9124, 12:3745, 13:1223, 14:313, 15:62, 16:8, 17:1.
Max-degree histogram: 2:1, 3:11019, 4:49503, 5:36893, 6:16322, 7:6336, 8:2369, 9:889, 10:330, 11:127, 12:47, 13:19, 14:7, 15:3, 16:1, 17:1.

**Conclusion.** The published structural theory prunes essentially nothing at the topology level (0.12 %). All real pruning power is in the WEIGHT constraints: the forcing lemma L4 (search over edge orderings), Taylor's 11/7 parity split (L2), the weight bounds m_1 <= 105, m_2 <= 76, w_i + w_j <= S (L12, L13), plus the position anchors for weights 1, 2 (L1). The purpose-built search should be organised around L4, exactly as SWZ and Calhoun did, with modern incremental distinctness checking and isomorph rejection.

## 2b. Cross-check against the parallel theory branch (`docs/theory-notes.md`, `src/theory_checks.py`, commit 666509c)

The theory branch (written independently, same day) proves its own lemmas rather than sourcing the literature; the two agree wherever they overlap:
* its F1 (hop-diameter <= 14 via OGR(D+1) <= N) leaves 123,796 = my F4 (same 71 kills);
* its F2 (Sidon at a vertex + containment: OGR(d)+OGR(d-1)+2 <= N+1-b_(1)b_(2), giving max degree <= 11) leaves 123,789 = my F6 (same 78 kills) - two different proofs of Delta <= 11 at n = 18 (theirs analytic via Golomb tables, mine by exhaustive star-Sidon search);
* its Lemma 8a = my L1/L4 fragments; its Lemma 6 refines Taylor (L2) mod 4; its Lemma 4c (w_e <= N+1-c_e, containment) and Lemmas 1-2 (moment identities) are WEIGHT-side tools not present in the published literature.
* Its extra topology kills come from the real relaxations (F3 projection, F4 majorization QP): 122,344 survivors. My literature filters additionally kill the 3 remaining diameter-3 double stars (ids 123606, 123621, 123643: B_{10,6}, B_{9,7}, B_{8,8}), which the relaxations do not see. **Intersection of both survivor sets: 122,341 topologies.** Neither list contains anything the other proves impossible except those 3.

## 3. Verification status summary

| Item | Status |
|---|---|
| L1, L2, L3, L4, L5, L7, L8, L12, L13, L16, L17 | VERIFIED-BY-ME |
| L6 | argument VERIFIED-BY-ME; G(m) for m >= 14 LITERATURE (m <= 13 re-verified) |
| L11 | VERIFIED-BY-ME (new here, exhaustive search) |
| L9 (SWZ Thm 3) | UNCLEAR |
| L10 (Luo-Yu), L14 (n=11,16 computations), L15, L18 | LITERATURE-ONLY |
| Leech 1975, Taylor 1977 primary texts | not read; content taken from reprints and re-derived |
