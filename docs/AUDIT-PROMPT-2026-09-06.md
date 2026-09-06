# Audit prompt: re-check the work of 2026-09-05/06 on the Leech-tree project

You are auditing two days of work, not the whole project. The repository is at

    /Users/geoclaw/Documents/claude/projects/leech-trees

(local working tree; the public branch `deposit-2026-09-04` on
https://github.com/LSMENG/leech-trees predates this work). The earlier
referee round is in `paper/REVIEW-PROMPT.md` and
`docs/fable-second-referee-takeover-2026-09-04.md`; do not repeat it.

## What was done (claimed), with the files to check

| item | file | sha256 (first 16) |
|---|---|---|
| route review: three new lemmas, ladder-cost negative, verdicts on the five "what would help" items, Astra assessment (§1.5), Lemma 5 (§1.6), theory WP outcomes (§C), measured updates | `docs/fable-route-review-2026-09-05.md` | e193ec47ae78fd41 |
| plan with gates G1/G2 and the token protocol | `docs/plan-2026-09-05.md` | bf818543528207b7 |
| positive controls for the lemmas (five known Leech trees) | `theory-lab/double_end/check_new_lemmas.py` | 2d9ffdcff61aed66 |
| signed-moment / derivative / charge identity checks | `theory-lab/double_end/check_signed_moment_family.py` | 58005886e2d2d260 |
| external idea being assessed (OpenAI Astra 6, 2026-09-04) | `~/Documents/Codex/leech-ideas-2026-09-04/数学思路审查.md`, `check_signed_moment.py` | — |
| WP-A1: Wiener + signed moment wired into the depth phase, four levels, differential | `theory-lab/s1_crowding/abstract_class_search_moment.cpp`, `docs/briefs/WP-A1-result.md` | cbf2bc661f4aaaec |
| WP-B1/B1b: forest engine n=19 and n=20 on Hoffman2, n=17 control under the MAXV=21 binary | `docs/briefs/WP-B1-result.md`, `WP-B1b-result.md`, `results/hoffman2_forest19_20/`, `src/forest_search.cpp` (one-line MAXV change) | tgz n=20: 9274bd989138e612 |
| WP-A3: delta=285 residual wave submitted then cancelled by the author's decision | `docs/briefs/WP-A3-result.md`, research_state 2026-09-06 | — |
| paper edits: Corollary `cor:secondend` + proof, Remark `rem:moments`, §9 cost sentence, §11 DOI | `paper/main.tex` (search for those labels; backup `main.tex.bak-secondend-*`) | 674791c9dcb48e7b |
| append-only log entries dated 2026-09-05 and 2026-09-06 | `research_state.md` (tail ~150 lines) | — |

## What to verify, in order of value

1. **Corollary cor:secondend (paper §8).** Re-derive (a), (b), (c) from the
   identity $d(u,v)=N-f(u)-e(v)-2h_c$ of Theorem thm:endpoint. Check the
   quantifiers, the case in which the last common ancestor $x_0$ of the high
   block lies in $W$, the claim that no other vertex of the $a$–$x_0$ path
   can lie in $W$, and the depth bound arithmetic
   $\binom{m}{2}\le 2N-1-2d(a,x_0)$ (and $\binom{m+1}{2}$ when $x_0\notin W$).
   Test (a)–(c) on the five known Leech trees (edge lists in
   `theory-lab/double_end/ground_truth_small.json`) with your own code.
2. **Remark rem:moments.** Check the identity
   $\sum_{u<v}(-1)^{d}d=\sum_e w_e q_e(S-q_e)$, its value $N/2$ ($N$ even) or
   $-(N+1)/2$ ($N$ odd), and the more general
   $P'(\zeta)=-N/(1-\zeta)$ with the cut form stated in the route review §1.5.
   Confirm the wording does not overclaim novelty (the literature check is in
   research_state 2026-09-06, WP-C4) and is consistent with the AI-use
   statement in §12.
3. **§9 cost sentence and the n=19/20 numbers.** From the shard records:
   raw sums 474,060,441,097 (n=19) and 3,883,156,913,714 (n=20); unique
   counts subtract $(K-1)\times 73{,}408$ prefix copies with $K=1680$;
   growth factors 7.928 and 8.193; CPU-hours 60.74 and 510.3 from
   Elapsed×AllocCPUS; 0.46–0.47 µs per node; extrapolations
   1.4e17–2.2e17 nodes and 2e7–3e7 CPU-h. Also check the n=17 control
   accounting: raw 7,890,649,165 = 7,875,306,893 + 209×73,408. Say whether
   the $73{,}408$ prefix is the same for every $n\ge17$ (see
   `src/verify_forest_run.py`, PREFIX) and whether the n=18 total used as
   the denominator (59,795,196,608 raw) was treated consistently.
4. **WP-A1 soundness.** Read `abstract_class_search_moment.cpp` against the
   frozen `abstract_class_search.cpp`. The claim is: levels 1–3 never reject
   an assignment that level 0 accepts (necessity only), the record format is
   unchanged, and the measured effect at delta=284 is a 1.01× speed-up with
   level 3 8.7× slower. Spot-check the (W) and (M) coefficient construction
   (edge weights affine in $s, l_1..l_{r-1}$; cut sizes; signed cut sums per
   parity pattern), the gcd/lattice test, and the 2×2 solve. You may run the
   order-6 positive control and the `--moment-selftest` (seconds). Do not
   rerun the delta=284 records.
5. **The negatives in the route review.** (i) The ladder cost table (§2.1): is
   the 60× step and the 18× per-tree inference used correctly, and is the
   conclusion "delta=287 alone exceeds the whole-problem direct search" fair
   given the direct-search figure has since risen to 2e7–3e7 CPU-h? (ii) The
   two-sided crowding arithmetic (§2.2). (iii) The Sidon counterexample
   (§3 item 2): three pendant paths of heights $h,h+1,h+2$ at one foot — do
   their mutual and crossing distances really stay distinct? (iv) The mod-4
   star/path example (§C, WP-C3): recompute both count vectors.
6. **Lemmas 2–4 of the route review** (chordal near-graphs; roots-of-unity
   subtree identity; $g_2\le46$). Try to refute each; if you cannot, say
   which step is weakest.
7. **Provenance and process.** (i) research_state entries of 09-05/06 versus
   the files: hashes, job ids (214065, 214066, 217848, 217897, 218157), the
   statement that the cancelled wave produced no ABSTRACT lines. (ii) The
   paper cites DOI 10.5281/zenodo.22334399, which is *reserved on a saved
   draft and not yet published* (the author decided to publish only after the
   paper is final): decide whether the availability text needs a
   "reserved, to be activated" qualifier. (iii) `src/forest_search.cpp` in the
   working tree carries the MAXV=21 patch that produced the n=19/20 runs while
   the frozen n=18 certificate was made with MAXV=20; check that the paper's
   provenance table does not silently mix the two.

## Ground rules

Label every finding CONFIRMED / REFUTED / CANNOT VERIFY, with file and line.
Keep PROVED / FINITE VERIFIED / OBSERVED / CANDIDATE / OPEN / NEGATIVE apart,
as the documents do. A finite computation over a fixed range never proves the
general statement; nothing here claims order 25 is settled — flag any sentence
that reads otherwise. Do not launch or modify any cluster job; small local
checks (under a minute, one process, `nice -n 15`) are fine. Order findings
by severity; a precise replacement sentence is worth more than a paragraph of
commentary. If everything holds, say so plainly and name the single weakest
point.
