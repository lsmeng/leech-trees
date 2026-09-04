# Handoff — Leech tree project

> **SUPERSEDED OPERATIONAL SNAPSHOT (2026-08-24).**  This file preserves the
> 2026-08-20 handoff history, but its running-job list and §5 execution order
> must not be followed without a fresh cluster check.  In particular,
> `docs/nonexistence-roadmap.md` now exists and the order-25 hop-diameter-at-
> most-four campaign is already complete: 322,189,234,739 reported nodes and
> 3,403,240 CPU-s (about 945 CPU-h), not the obsolete future estimate below.
> Do **not** relaunch it.  Current mathematical and operational authority is
> `README.md`; the active post-review route is
> `docs/post-max-review-q1-plan.md`, with FW218--FW262 in
> `docs/edge-handoff-orientation.md`.  Re-query Hoffman2 before making any
> statement about jobs that this historical file says are running.

You are taking over a computer-assisted mathematics project from another AI agent. The human owner is **Lingsen Meng**, a seismologist at UCLA — competent technically, not a combinatorialist. Everything below is the true state as of **2026-08-20 16:10 PDT**. Read this whole file before touching anything.

Repository: `/Users/geoclaw/Documents/claude/projects/leech-trees` (git, clean working tree at commit `4a6e86c`+). Python venv at `.venv` (ortools, networkx). Build: `scripts/build.sh` → `bin/forest_search`, `bin/leech_search`.

**Constraints that carry over:** do not use `bl` / `bailian-cli` tools. The Mac is shared with other projects — keep to ≤4 processes at `nice 10`. Hoffman2 (`ssh hoffman2`) runs **SLURM, not SGE** — `qsub` hangs silently, use `sbatch`; QOS `campus24` caps you at 100 jobs / 500 submitted / 768 CPUs / 16 nodes **across all your jobs**, and other projects are already using that quota.

---

## 1. The problem

A **Leech tree** of order *n*: a tree on *n* vertices with positive integer edge weights whose C(n,2) pairwise path sums are exactly {1, …, N}, N = n(n−1)/2. Leech (1975) found five; none has been found since. Taylor (1977): *n* or *n*−2 must be a perfect square, so admissible orders are 2, 3, 4, 6, 9, 11, 16, 18, **25**, 27, 36, 38, 49, 51, …. Orders 9, 11 (Székely–Wang–Zhang 2005) and 16 (Calhoun et al. 2007) were excluded by computer. Székely–Wang–Zhang conjectured there are finitely many; **no general nonexistence theorem exists.**

---

## 2. What is finished — do not redo any of this

### 2.1 Main theorem (solid, four-way replicated)

**There is no Leech tree on 18 vertices.** Hence, with Taylor excluding 19–24, **the five known Leech trees are the only ones of order ≤ 24**, and the smallest open order is 25.

Method: the forced-forest search — **Calhoun et al. 2007 Algorithm 2.7, not ours** (`src/forest_search.cpp`). 59,779,854,336 forced forests, level-17 count 0, ~5.5 CPU-hours.

Evidence chain, all in the repo:
- Two independent witness checkers (`src/checker_a.py`, `src/checker_b.py`), two independent topology enumerations (networkx vs nauty).
- Two adversarial referee passes: `docs/referee-report.md` (per-topology engine), `docs/referee-forest.md` (forest engine). No unsound prune found. They caught a real error in our own theory notes.
- A **clean-room re-implementation** by an agent forbidden to read the original (`cleanroom/cr_forest.c`): all eighteen per-level counts identical.
- Four runs — two Hoffman2 shard layouts (gcc/x86), local (clang/arm64), clean-room — with bit-identical unique-node totals. Verify with `python src/verify_forest_run.py 18 results/hoffman2 210 8`.
- Independent *method* cross-check with the per-topology engine: n=16 complete (19,320/19,320 UNSAT, reproducing Calhoun); n=18 at **91.5% coverage** (111,951 of 122,344 survivor topologies UNSAT, 1,170 still undecided at a 1 h cap, **0 SAT**) — still running on the cluster, see §4.
- SAT/DRAT certificates for n ≤ 11 (`docs/sat-route.md`).

### 2.2 Neighbouring results (`variants/RESULTS.md`)

M(11) = 60 with exactly two minimal trees; 77 ≤ M(12) ≤ 78; no modular Leech tree of order 9 or 11; order 5 **does** exist (contradicting a claim relayed in Leach 2014 — hedged carefully in the paper); exactly six 6-leaf leaf-Leech trees, five with an irreducible vertex, answering Question 3.1 of Ozen–Wang–Yalman affirmatively.

### 2.3 The paper

`paper/main.tex` → `paper/main.pdf`, 17 pp, compiled with `tectonic` (not pdflatex). Single author, Lingsen Meng, UCLA EPSS. Latest PDF also at `paper/Meng-Leech18-draft-v3-2026-08-20.pdf`.

Seven visible `\todo` markers remain: confirm the email address; obtain Luo–Yu 2024 and compare with the star-Sidon lemma; report the final per-topology cross-check numbers; AI-statement wording; repository URL and Zenodo DOI; acknowledgements and funding; exact M(12) once the queued D=77 run finishes.

Section 3 now carries an explicit attribution paragraph: the algorithm is Calhoun's, we claim no algorithmic novelty. **Keep it.** A referee will ask why nobody did n=18 in the 19 years since; the honest answer — the field is tiny, not that it was hard — should stay in the discussion.

`AUDIT-PROMPT.md` is a prepared brief for an *independent* AI audit before submission. The owner wants that audit done before he submits. A packaged bundle sits on his Google Drive.

---

## 3. What happened today (2026-08-20) — new, and partly unwritten

A 12-agent workflow attacked the general nonexistence question from six angles with four adversarial referees. **11 of 12 agents returned; the final synthesis agent was stopped mid-run for this handoff, so `docs/nonexistence-roadmap.md` was never written.** Every raw result is preserved in **`theory-lab/WORKFLOW-RESULTS-RAW.json`** (11 reports, 78 claims with per-claim status, plus all referee verdicts). **Writing that roadmap is your first job — see §5.**

### 3.1 The big new result

**No path or spider Leech tree exists for any order 5 ≤ n ≤ 63.**

A top-down "zero-slack" prover closed every admissible order through 51 (25, 27, 36, 38, 49, 51), each with a from-scratch paranoid recheck at every node, in **236,957 search nodes total** — against 6×10¹⁰ for the single bottom-up n=18 exhaustion. Combined with Taylor and the known exhaustions for n ≤ 18, that covers all orders up to 63. Code and outputs in `theory-lab/catspider/` and `theory-lab/exp-families/`.

This is the project's first result covering an unbounded-looking family rather than one order. The reports argue it is **one bounded case analysis in disguise** (per-anchor case trees of ~110–130 nodes, value windows never deeper than ~22 below N, both independent of n from 12 through 51) and that symbolising it — treat T and N−T as symbols, branch on the finitely many bounded comparisons — would turn it into a genuine **infinite-family theorem**: *no spider Leech tree for any n*. That would be the first general nonexistence theorem in the subject's 50-year history. **This is the highest-value open task.**

Also closed: **bi-spiders at 25 and 27** (all trees with at most two vertices of degree ≥ 3, covering double stars and double brooms) — 29.2M nodes at n=25 replicated three times, 45.9M at n=27 in three exactly-partitioning shards, 0 solutions; the C prover was differentially validated against a Python reference for n=4..13.

**Hop-diameter ≤ 4 completely classified for n ≤ 24**: only the five known trees. A diameter-restricted engine (scratch copy of the refereed `forest_search.cpp` plus a proved subforest invariant and four new proved prunes) exhausted 2 ≤ n ≤ 18; Taylor covers 19–24. n=25 needs ~2×10¹¹ nodes ≈ 150–200 CPU-hours, engine ready and 512-way sharded, cluster-feasible.

### 3.2 A route that is now dead — do not retry it

The **difference-set crowding** idea (the interval [1,N] being crowded out by A−A, forcing the pendant-weight set to have nowhere to sit) **does not close, and the experiment says so quantitatively**: occupation stalls near 0.5 and *decreases* with n — centroid mean 0.60 / 0.52 / 0.49 for n = 11 / 16 / 18, occupancy of [−N,N] 0.33 / 0.26 / 0.25, and the exact positive L6 sits at 0.41. Data in `theory-lab/exp-occupation/`. The underlying structural fact is fine; the quantitative contradiction is not available. Do not spend time re-deriving it.

**Correction the owner has been told, and which must not be lost:** the lemma as originally stated — for a vertex *v* with pendant weights *B* and depth set *A*, (A−A) ∩ (B−B) = {0} — is **WRONG as literally stated**, because that *A* includes *v*'s own pendant leaves, which makes B−B automatically a subset of A−A. It fails on the known trees L3, L4_star and L6 themselves, and at 23,058 vertex instances across 49,435 exhaustively enumerated distance-injective trees, failing exactly at vertices with ≥ 2 pendant leaves. The **correct hardened form** (referee verdict CORRECT, zero failures over the same exhaustive check) is claim **L-C** in the raw results: *A* = {0} ∪ {d(v,x) : x ≠ v, x **not a pendant leaf at v**}. Use only the hardened form.

### 3.3 Where the obstruction actually bites

Experiment E2: for near-miss states that die, the unplaceable forced value t\*/N concentrates in **[0.13, 0.38]** — the search dies at the **small end**, not near the top. Any future analytic attack should aim there. The covering lens produced matching small-end machinery: a Kruskal merge-profile refinement of the forcing bound (w\_{k+1} ≤ 1 + Σ\_{j≤k} a\_j b\_j, sharper than Calhoun's by the component count of the light forest) and an exact waste identity with a new inequality forcing ~n⁴/32 waste for a balanced heaviest cut.

### 3.4 Literature verdict on the PSDS route

The perfect-systems-of-difference-sets literature (Bermond–Kotzig–Turgeon 1978; Abrham–Kotzig 1984) is the closest proven analogue — a threshold-1 PSDS is exactly a perfect distance forest whose components are paths, and there the field *did* prove the program we want (BKT: no perfect system whose components all have ≥ 6 elements, any number of components, any threshold). **But it does not import wholesale**, for a precise reason: a spider Leech tree is a threshold-1 PSDS only after deleting the cross-leg *sum* values, so its m difference triangles must tile [1,N] minus a (1−Θ(1/m))-dense set of cross-sums, and every interval-tiling theorem fails to apply for m ≥ 3 legs. For m ≤ 2 the reduction is literal and only reproves "no Leech path for n ≥ 5". Details and citations are in the raw results.

### 3.5 Other proved-and-refereed material in the raw results

Power-sum nondegeneracy: for the star K\_{1,n−1} the determinant of the first-(n−1) power-sum Jacobian equals (n−1)!·∏\_{j=0}^{n−2}(n−2^j)·Vandermonde(w), identically singular iff *n* is a power of 2 (verified exactly for n = 3..9); all 43 non-star topologies with 4 ≤ n ≤ 8 are generically nonsingular; all five known Leech trees are isolated (rigid) solutions. Plus caterpillar ghost-coordinate reformulation, global coordinate distinctness, two-sided window tiling with excess, window/anti-concentration lemmas W1–W3 with explicit constants for diameter ≤ 4, and a master generating-function identity. Referee verdicts are attached to each; several are FIXABLE with the fix stated (typically a missing `n ≥ 3` or a quantifier restriction).

### 3.6 Caterpillars are open and known to be hard

Bottom-up forced-forest search restricted to caterpillar shape is validated three ways and exhausts n ≤ 16, but at n = 25 level 13 already costs 3.3×10⁹ nodes and grows ×9.5–10 per level with 11 levels to go — ≥10¹⁶ nodes, infeasible. The obstruction is identified precisely: a pendant leaf carries two coordinates (ρ, λ) with a free radius, so top-down window forcing pins only one coordinate per end-cluster leaf. **Caterpillars at 25 and 27 remain open.** Do not restart a bottom-up caterpillar run without a new idea.

---

## 4. What is still running, and what was stopped

**On Hoffman2 (untouched, no budget cost, let them finish):**
- `redo18` — the per-topology cross-check of the n=18 UNKNOWNs, currently 91.5% coverage, 0 SAT. Results accumulate in `$SCRATCH/leech-trees/results/redo/`. Pull with rsync and re-run `src/verify_forest_run.py`-style aggregation when done; the paper's §4.2 and §7 numbers should be updated then.
- Also queued/running from other sub-projects and sharing the same QOS quota: `thrackle`, `oddgraceful25`, `sem27`, `vlpspec`, plus two unrelated `wan22-*` jobs. Do not cancel them; do budget around them.

**Stopped for this handoff:** the 12-agent workflow (synthesis never ran) and three local `forced_family` processes plus one `fs_d4_ablate` that were running capped 5-second probes for caterpillar/diameter-4 at order 27. Their partial outputs are committed in `theory-lab/exp-families/`. **Watch out:** lines in those `.out` files carry `capped=1`, meaning the shape hit the time cap and was *not* exhausted — `found=0` with `capped=1` is **not** a nonexistence result. Only `capped=0` lines are conclusive. Any claim built from those files must filter on that.

---

## 5. What to do next, in order

1. **Write `docs/nonexistence-roadmap.md`** from `theory-lab/WORKFLOW-RESULTS-RAW.json`, in the house style of `README.md`: proved-and-refereed lemmas with statements and proofs; FIXABLE ones with the exact fix; refuted ideas with their counterexamples (so nobody re-derives them — especially §3.2); the importable literature with citations; the experiments' decision outputs; and a ranked route list. Every item gets a status label. Cross-check each claim's referee verdict before promoting it — several claims were marked WRONG or FIXABLE by referees and the raw file contains both the claim and its verdict.
2. **Symbolise the spider closure into an infinite-family theorem** (§3.1). Highest value in the project. The evidence that it is a bounded case analysis is measured, not guessed.
3. **Run the diameter-4 engine at n = 25** on Hoffman2 (~150–200 CPU-h, 512-way sharded, engine ready) once quota frees, then n = 27 (~2000–3000 CPU-h). Yields "the only hop-diameter ≤ 4 Leech trees of order ≤ 35 are the five known ones" — the first exclusions at the smallest open order for a natural family.
4. **Finish `redo18`** and update the paper's cross-check numbers.
5. **Clear the seven `\todo`s** in the paper. The Luo–Yu 2024 one matters most: it is a possible priority overlap on the degree bound and we could never obtain the text.
6. Only then: submission. Target `arXiv math.CO` → **Experimental Mathematics** (first choice) → Integers / Discrete Mathematics note. The independent audit in `AUDIT-PROMPT.md` should happen first — the owner has said he will not submit until it passes.

---

## 6. House rules this project runs on

They are the reason the n=18 result is trustworthy, and they are not optional.

- **Never state "we did not find one" as "there is none."** Every nonexistence claim needs an exhaustion argument with the search's own invariants published (per-level counts, node totals), not just a verdict.
- **Two independent checkers for every witness**, sharing no code.
- **Label every claim** OBSERVED / LITERATURE / PROVED / SPECULATIVE, and keep the running ledger in `README.md` chronological and honest, including corrections.
- **When a claim is load-bearing, re-implement it clean-room** and compare invariants, not just answers.
- **Report what was skipped or capped.** The `capped=1` trap in §4 is exactly the kind of thing that turns a good result into a retraction.
- Prior-art check before claiming novelty. Two things this project has already found the hard way: an Earth–Moon result was superseded by a Zenodo preprint from two weeks earlier, and a slow-slip "global census" idea was pre-empted by a 2024 Science Advances paper. Both were caught by the agents themselves and dropped.

---

## 7. Fast orientation

```bash
cd ~/Documents/claude/projects/leech-trees
cat README.md                       # chronological status ledger — read first
scripts/build.sh                    # builds both engines
source .venv/bin/activate
python tests/test_checkers.py       # 5 known trees + 1000 perturbations
./bin/forest_search 16 --shard 0 1 --shard-level 0   # ~5 min, must report nsol 0
python src/verify_forest_run.py 18 results/hoffman2 210 8   # replays the archived n=18 verdict
python -c "import json;d=json.load(open('theory-lab/WORKFLOW-RESULTS-RAW.json'));print(len(d),'reports',sum(len(v.get('claims') or []) for v in d),'claims')"
```
