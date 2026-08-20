# Independent audit request — "There is no Leech tree on 18 vertices"

You are being asked to **audit a computer-assisted mathematical result before it is submitted for publication**. Your job is *not* to be encouraging. Your job is to find the mistake, or to state clearly that you looked for it in the specific places where it would hide and did not find it. A wrong pruning rule, a mis-stated lemma, an incomplete search, or a mis-attributed prior result would each make the paper wrong or unpublishable. Assume the authors are competent and that any error is subtle.

Please work from the actual repository and re-run what you can. Do not accept any claim in the documentation as evidence for itself.

---

## 1. The claim under audit

**Theorem.** There is no tree on 18 vertices with positive integer edge weights whose 153 pairwise path sums are exactly the integers 1, 2, …, 153. (Such a tree is a *Leech tree*, Leech 1975.) Combined with prior work and Taylor's condition, the five known Leech trees are the only ones of order ≤ 24, and the smallest open order is 25.

Secondary claims (Section 6 of the paper): M(11) = 60 with exactly two minimal trees; 77 ≤ M(12) ≤ 78; no modular Leech tree of order 9 or 11; modular Leech trees of order 5 do exist; exactly six 6-leaf leaf-Leech trees, five with an irreducible vertex, answering Question 3.1 of Ozen–Wang–Yalman (2016) affirmatively.

**Explicitly not claimed:** algorithmic novelty. The search is a re-implementation of Algorithm 2.7 of Calhoun, Ferland, Lister and Polhill (2007). Please check that the paper's attribution is accurate and sufficient.

---

## 2. Where everything is

Repository root: `~/Documents/claude/projects/leech-trees` (git, 40 commits). Python environment: `.venv` (ortools, networkx). Build: `scripts/build.sh` (clang++ -O3 -std=c++17).

**Read first, in this order:**
| File | What it is |
|---|---|
| `README.md` | Working status ledger, chronological. Every claim is labelled OBSERVED / LITERATURE / CORRECTION. |
| `paper/main.tex`, `paper/main.pdf` | The manuscript under audit (17 pp). |
| `docs/literature-ledger.md` | 20 items (L1–L20): every result taken from the literature, with the source, the proof re-derived by the authors, and a VERIFIED-BY-ME / LITERATURE-ONLY / UNCLEAR label. |
| `docs/theory-notes.md` | The authors' own lemmas, with machine checks. |
| `docs/referee-report.md` | A prior adversarial review of the per-topology engine. |
| `docs/referee-forest.md` | A prior adversarial review of the forest engine (the decisive one). |
| `docs/cleanroom-forest.md` | The independent re-implementation. |
| `docs/engine-optimization.md` | Engine variants and benchmarks. |
| `docs/sat-route.md` | The SAT/DRAT route used for n ≤ 11. |

**Code.** `src/forest_search.cpp` is the engine that produced the theorem. `src/leech_search.cpp` is the independent per-topology engine. `src/checker_a.py` and `src/checker_b.py` are two deliberately dissimilar witness checkers. `src/enumerate_trees.py` builds the topology lists two ways. `src/verify_forest_run.py` is the run-integrity script. `cleanroom/cr_forest.c` is the clean-room implementation, written by an agent forbidden from reading `forest_search.cpp`. `tests/` holds regression, differential and referee tests. `src/theory_checks.py` and `src/filters.py` hold the lemma checks.

**Data and results.** `data/known_leech_trees.json` (the five known trees), `data/trees_{n}.jsonl` (frozen topology lists). `results/hoffman2/` and `results/hoffman2_rep2/` are the two cluster runs at n=18 (per-shard JSON plus stderr with per-level histograms); `results/forest_order_18.jsonl` is the local run; `results/cleanroom_forest_18_shard*.jsonl` is the clean-room run; `results/cpp_order_16.jsonl` and the Hoffman2 per-topology outputs are the independent-method cross-check.

---

## 3. What to check, hardest first

### 3.1 Is the search complete? (the load-bearing question)

A nonexistence result is only as good as the claim that nothing was skipped. Four things must all hold.

**(a) The forcing lemma.** Paper Lemma 2.1 / Calhoun Lemma 2.6: with edge weights w₁ < … < w_{n−1}, w_k is the least positive integer not realised as a distance in the subforest of edges of weight < w_k. Re-derive the proof yourself. Check especially the boundary cases: what if the least missing value is already realised by a path all of whose edges are assigned; can a Leech tree's weight sequence ever *skip* the least missing value; is the "start a disjoint new edge" move genuinely necessary (construct or find an example where a Leech tree's construction requires it — the order-6 tree does; verify that).

**(b) Isomorph rejection.** Paper Lemma 3.2 (`lem:aut`): in a forest whose edge weights are pairwise distinct, every automorphism fixes every edge, so Aut is Z₂ raised to the number of single-edge components. Prove or refute this exactly as stated. Then check that the canonical-parent rule (remove the maximum-weight edge) plus the orbit-representative rule together generate every abstract forced forest **exactly once** — not at least once, and not more than once. `tests/referee_forest_enum.py` contains an independent Python oracle; run it, and if you can, write your own oracle rather than trusting theirs.

**(c) The prunes are necessary conditions, not heuristics.** Each rule in `forest_search.cpp` that discards a node must be justified: distance repetition, distance > N, vertex count > n, the `w_i + w_j ≤ N` rule, the attachment prefilter, the per-translate early exit. For each, either prove it or find a counterexample. A prune that is *usually* right is fatal here.

**(d) Sharding.** The run was split by level-8 subtree index. Verify that the shards partition the search: no subtree counted twice, none dropped, including when the shard count does not divide the number of level-8 nodes. `cleanroom/check_sharding.py` and `src/verify_forest_run.py` are relevant; test with your own K and L values.

### 3.2 Do the numbers hold up?

The run reports 59,779,854,336 forced forests at n = 18 and these per-level counts:

```
level  0..8 :  1, 1, 2, 8, 41, 229, 1384, 8899, 62843
level  9..12:  480085, 3984162, 35540837, 332597341
level 13..17:  2896330052, 17017193146, 37669242243, 1824413062, 0
```

- Verify levels 0–5 **by hand**. (Level 2 = 2 should be checkable in a minute; if it is not 2, everything downstream is suspect.)
- Re-derive levels ≤ 9 or ≤ 10 with your own independent program.
- Run `python3 cleanroom/verify_18.py 18` and `python src/verify_forest_run.py 18 results/hoffman2 210 8`; confirm the shard-integrity identities actually test what they claim to.
- Check that the four runs (two Hoffman2 shard layouts, local, clean-room) genuinely used different code paths / architectures and are not silently the same binary or the same shard layout.
- Rebuild the engine from source and reproduce at least one shard byte-for-byte.

### 3.3 Is the terminal test right?

The search declares a leaf a Leech tree when the forest is connected, has n vertices and n−1 edges. Verify that this implies the distance multiset is exactly {1,…,N} given the invariants maintained (all distances distinct, all ≤ N, count = C(n,2)) — and that those invariants really are maintained. Check the off-by-one at N and at n.

### 3.4 Positive controls

The engine must **find** what exists, or its silence at n = 18 means nothing.
- n = 4 → 2 Leech trees; n = 6 → exactly 1; n = 5, 7, 8 → 0.
- Every witness must pass **both** `checker_a.py` and `checker_b.py`. Read both checkers and confirm they are genuinely independent (different algorithm, no shared helper) — if they share a bug they are one checker.
- `tests/referee_forest_planted_big.py` plants random distinct-distance trees up to n = 18 and requires the engine to recover them. Run it; check that the planting procedure cannot accidentally produce instances the engine is tuned for.
- Confirm the five known trees in `data/known_leech_trees.json` are the five in the literature (Leech 1975; the figure is reproduced in Ozen–Wang–Yalman, Integers 16 (2016) #A21, which is open access), and that the count "five" uses the same convention (isomorphism classes; does it include the trivial n = 2 tree?).

### 3.5 The literature

- **Is n = 18 really open?** Search independently for any prior determination of order 18 (arXiv, MathSciNet/zbMATH if you have access, Google Scholar, the Epoch AI FrontierMath open-problems page, Gallian's dynamic survey DS6, ResearchGate, theses). The authors note that Calhoun et al. (2007) say "n ≤ 24" in a summary paragraph while their abstract and Table 1 say n < 18, and treat the former as a misprint — **check this yourself**, because if it is not a misprint the main theorem is not new.
- Verify Taylor's condition (n or n−2 a perfect square) and hence that orders 19–24 and 26 are excluded, which is what upgrades the result to "n ≤ 24".
- Check the attribution of the algorithm to Calhoun et al. Alg. 2.7 and of the forcing lemma to their Lemma 2.6 / Székely–Wang–Zhang's "Find-Next-Weight", and whether the paper's added attribution paragraph in Section 3 is adequate or still overclaims.
- Check every citation in `paper/refs.bib` resolves to a real paper with the stated authors, year, venue and page numbers. Two known trouble spots the authors flagged: Luo–Yu (2024) could not be obtained, so a possible priority overlap on the degree bound is unresolved; and the modular-Leech order-5 claim contradicts a statement Leach (2014) attributes to Leach–Walsh (2011), which the authors also could not obtain. Both need an outside opinion on whether the paper's hedging is honest enough.

### 3.6 The lemmas in Section 2

Re-derive each and check it is used only where its hypotheses hold: the cut identity; the Golomb-ruler and containment bounds; the star-Sidon degree bound (Δ ≤ 11 at n = 18, using exact minima S(2..12) = 3, 6, 11, 19, 31, 43, 63, 80, 110, 138, 169 — recompute at least S(2..8) yourself); Taylor's parity condition and the claim that it constrains weights rather than the unweighted bipartition. Note the authors already corrected one error here after a prior review (incident weights at a vertex form a *weak Sidon set*, not a Golomb ruler; counterexample K₁,₇ with weights {1,2,4,8,14,19,24}) — confirm the corrected statement is right and that nothing else depends on the old one.

### 3.7 Section 6 (the neighbouring problems)

These are stated more briefly and have thinner verification than the main theorem. For each — M(11) = 60, 77 ≤ M(12) ≤ 78, modular Leech orders 5, 9, 11, leaf-Leech with six leaves — check the definitions against the cited sources (Calhoun et al. 2007; Leach, *Int. J. Combin.* 2014:218086; Ozen–Wang–Yalman 2016), verify every witness by hand or with your own script, and judge whether the confidence labels in Section 6.4 are honest. The paper states that the order-11 modular result rests on a single implementation; decide whether that is adequately flagged.

### 3.8 Reproducibility as a referee would test it

Clone the repo fresh, build, and try to reproduce: the n ≤ 6 results, the n = 16 forest run (about 5 minutes), and one n = 18 shard. Note anything that does not build, does not run, or produces different numbers. Check that `README-GITHUB.md` is sufficient for a stranger.

---

## 4. Specific things that would sink the paper

Look for these by name:

1. A prune that is not a necessary condition (would make the search incomplete).
2. Isomorph rejection that drops a genuine orbit (same effect).
3. Sharding that loses a subtree.
4. The two "independent" checkers sharing logic; or the clean-room implementation having in fact seen the original source (check the git history and the agent transcript claims sceptically).
5. Order 18 already settled in the literature.
6. The "n ≤ 24" line in Calhoun et al. not being a misprint.
7. A wrong constant in a bound (e.g. S(12) = 169, OGR(15) = 151, OGR(16) = 177, N = 153) silently excluding a live case.
8. The n = 25 cost estimate or the first-moment heuristic in the Discussion being wrong by enough to mislead.
9. Anything in the AI-assisted research statement (Section 7) that misdescribes how the work was actually done, given what the repository shows.

---

## 5. Context you should know

This work was carried out by AI agents (Claude) under the direction of a human author who is a seismologist, not a mathematician, over roughly 24 hours. The verification chain — two checkers, an adversarial referee pass, a clean-room re-implementation, cross-architecture replication — was built precisely because of that. Two errors were already caught internally by that chain and are documented (`docs/referee-forest.md`, the Lemma 5(b) correction in `docs/theory-notes.md`). Treat this history as a reason for *more* scrutiny of the mathematical statements and the literature claims, not less: the code has been attacked hard, the scholarship less so.

---

## 6. What to give back

1. **Verdict**: would you sign your name to this being correct and new? Yes / yes with fixes / no.
2. **Findings**, each labelled FATAL / MAJOR / MINOR / NIT, with the file and line, what is wrong, and a concrete counterexample or a reproduction command.
3. **What you re-ran**, with the commands and the numbers you got, and what you could not check and why.
4. **Novelty judgement**: is order 18 genuinely open; is the attribution to Calhoun et al. adequate; what would a referee at *Experimental Mathematics* or *Discrete Mathematics* most likely object to.
5. **Anything you think is over-claimed** in the abstract or the discussion, quoted.

If you conclude the result is correct, say so plainly and say what you checked — a bare endorsement is worth nothing here.
