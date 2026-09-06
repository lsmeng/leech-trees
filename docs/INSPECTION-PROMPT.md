# Inspection prompt: is there a better route to order 25?

You are being asked to look at a research programme and say whether there is a
better idea in it than the ones already tried. Not to referee a paper, not to
check arithmetic — to find a route the people working on it have missed.

Read the repository at https://github.com/LSMENG/leech-trees, branch
`deposit-2026-09-04`. If you are running on this machine, the working tree is at

    /Users/geoclaw/Documents/claude/projects/leech-trees

and contains more than the public branch does (in particular the 2.3 GB of
superseded top-window artefacts, which you can ignore).

Where things are:

| path | what is in it |
|---|---|
| `paper/main.tex` | the paper; Section 8 is the order-25 material |
| `paper/section-double-end.tex` | the two-anchor reformulation, not yet merged into main.tex |
| `theory-lab/double_end/THEORY.md` | the two-anchor normal form, its lemmas, and section 10 on why the restricted case is rigid |
| `theory-lab/s1_crowding/` | the order-25 engines: `verify_s1_top_block_crowding.py` (arithmetic verifier for the crowding table), `s1_direct_search.cpp` (direct normal-form search, no inherited assumptions), `abstract_class_search.cpp` (depth-free class search plus the (s,L) depth phase), `hh_capacity.cpp` (exact per-class capacity), `brute_abstract_check.py` (independent brute force) |
| `theory-lab/s1_crowding/frozen/` | hash-tagged frozen sources; the file name carries its own SHA-256 prefix |
| `theory-lab/s1_crowding/certificates/` | the split certificates: `depthv7_r8/` and `depthfrozen_r8frozen/` for delta = 284 (448 (split, shape) records each, identical), and `depthv7_r9_partial_20260902/` with the partial delta = 285 harvest and its per-file hash manifest |
| `theory-lab/double_end/` | the two-anchor engine (`double_end_search.py` and the trace-identical `double_end_search.cpp`), the independent enumerator, the brute-force oracle `brute_leech_small.py` with `ground_truth_small.json`, the differential harness, and `frozen/` |
| `theory-lab/depth_search/` | the rooted-depth pilot and its negative result |
| `src/`, `cleanroom/` | the order-18 forest engine, the per-topology engine, the clean-room re-implementation |
| `results/` | per-shard outputs and depth histograms for n = 18 and n <= 17, the SAT run records |
| `variants/` | the minimal-distinct-distance, modular and leaf-Leech engines, `RESULTS.md`, and `witnesses/` |
| `research_state.md` | the append-only log, including every route that failed and why |
| `docs/checkpoint-*.md` | dated technical records |

`research_state.md` is the most useful single file if you want to know what has
already been tried; it is long, and the entries from 2026-09-01 onwards cover
the order-25 work.

## The problem

A *Leech tree* of order n is a tree on n vertices with positive integer edge
weights whose C(n,2) pairwise path-weights are exactly 1, 2, ..., C(n,2). Five
are known, of orders 2, 3, 4, 4, 6. Taylor: the order must be k^2 or k^2 + 2.
Orders 9, 11, 16 and now 18 are excluded. **The smallest open order is 25**,
where N = C(25,2) = 300.

## What is settled, and what the open question now is

Let T be a Leech tree of order 25 and {a,b} the unique pair at distance 300.

- **Diametral-endpoint reduction (proved).** Every pair avoiding a and b has
  distance at most N-2, so the value N-1 is realised by a pair containing a
  or b; naming them so that d(a,w) = N-1, we get diam(T-b) = 299 and
  diam(T-a) <= 298.
- **Top-block crowding (proved, no computation).** Deleting a leaf leaves a
  block of m consecutive rooted depths and r low ones. The C(m,2) high-high
  distances split into r+1 classes by the depth of the nearest common ancestor,
  and inside a class the distance is a constant plus y_i + y_j with
  y in [0, m-1], so a class holds at most 2m-3 of them. Hence
  C(m,2) <= (r+1)(2m-3), i.e. 5m^2 - (4k+11)m + 6k+6 <= 0 with k = n-1. At
  n = 25 this gives diam(T-l) >= 281 for every leaf.
- **Finite certificates.** delta = 281, 282, 283, 284 are excluded by exhaustive
  search of an explicit normal form (1.64e9 structures at delta = 284 alone),
  reproduced from a frozen source.
- **Therefore: no Leech tree of order 25 exists if and only if the normal form
  is empty for every delta in [285, 298].** Fourteen values. That is the open
  question. Nothing here claims the conjecture is proved.

## The measured cost of the obvious continuations — do not propose these

Every number below is measured, not estimated.

1. **More delta values by the same search.** delta = 285 was costed at about
   1e4 CPU-hours and stopped after 3,196 of 24,320 (split, shape) pairs, all
   empty. The cost grows steeply in r: the depth-free phase leaves 95 of 286
   rooted low trees with structures at delta = 285, 317 of 719 at delta = 286,
   1523 of 1842 at delta = 287. **The crowding inequality stops biting once the
   top block is short**, which is exactly the regime the open range lives in.
2. **The direct forced-forest engine at n = 25.** Extrapolates to 1e16-1e17
   nodes from a measured growth of 5.71, 5.93, 6.10, 6.38, 6.74, 7.19, 7.59 per
   vertex over n = 12..18. Four to five orders of magnitude out of reach.
3. **A parameter-free two-anchor search.** Reformulating without delta gives a
   clean tiling problem (below) and independently re-derives non-existence for
   n <= 11 (n = 11 exhausted in 3.34e9 nodes). At n = 25 it is **worse**, not
   better: a sampling experiment (200 shards of a 20,000-way split, two hours
   each) had none finish, putting the restricted search — only the part
   equivalent to diam(T-a) <= 284, already known — above 1.96e13 nodes, about
   4e4 CPU-hours, and that is a floor. Fixing delta fixes the top block and lets
   crowding prune it; the parameter-free form explores every admissible delta at
   once and pays for it.
4. **A rooted-depth-order global search.** Piloted and abandoned: >1e12 CPU-h,
   with the forcing lemma pruning under 1% in depth order.
5. **Top-window sumset tiling alone.** The window patterns roughly double per
   level (4, 8, 14, 24, 42 for W = 3..7); the window by itself is weak.

## The structure you have to work with

Coordinates at the two anchors. For u outside {a,b} put e(u) = N - d(a,u) and
f(u) = N - d(b,u). Then for u != v, with p the foot on the a-b path,

    d(u,v) = N - f(u) - e(v) - 2 h_c,     h_c >= 0,

where u is the one whose foot comes first and h_c is the height of the last
common vertex when both hang off the same foot in the same branch. So the whole
problem is: choose two disjoint V-sets E and F in [1, N-1] with
e + f = N (mod 2) and e + f <= N, plus a branch structure, such that

    {0} ⊔ E ⊔ F ⊔ {all d(u,v)}  =  [0, N-1] exactly.

Consequences already extracted, all proved: an exact parity split
((alpha+2)beta = N/2 for N even) which recovers Taylor as a corollary; the
spine is a Golomb ruler, so at most 20 of the 25 vertices lie on the a-b path;
an attachment lemma; a ball-counting bound.

**And the one that looks most promising and is not yet exploited.** If
diam(T-a) <= N-16 = 284 then the sixteen largest distances 285..300 are all
realised by pairs containing a, so the sixteen vertices W with d(a,·) >= 285
carry labels i_u = d(a,u) - 284 that are *exactly the interval [1,16]*. Then
d(u,v) = 568 + i_u + i_v - 2 mu_uv with mu the depth of the median. Grouping by
median, distances in a class are a constant plus i_u + i_v, and [1,16] admits
only 29 distinct pairwise sums, so each median carries at most 29 pairs and a
split of m members into parts n_1..n_t needs sum_{i<j} n_i n_j <= 29. That
forces the top of the hierarchy to be a caterpillar (m = 16..13 may peel at
most 2, m = 12 at most 3, m = 11 at most 4, m <= 10 unconstrained). Two further
necessary conditions: sum over pairs of mu >= 21630 (from
sum d = 70200 - 2 sum mu and the 120 distances being distinct and <= 284), and
for any vertex x at depth mu with m members of W strictly below it,
C(m+1,2) <= 599 - 2mu, so the first branch point sits at depth <= 231.
**These are compatible — 21630 <= sum mu <= about 32500 — so they do not yet
contradict. Closing that gap, or showing it cannot be closed, is the concrete
target.**

## What would actually help

In rough order of value:

1. A **sound inequality stronger than C(m,2) <= (r+1)(2m-3)** that still bites
   when the top block is short. The obvious direction is Hall applied to unions
   of classes with their actual attainable intervals, rather than a per-class
   capacity. Either prove one that kills a new delta, or produce the smallest
   explicit normal-form configuration showing why this route cannot improve the
   bound.
2. Additive-combinatorial structure on the **deficit sets** E and F. Starting
   from d(u,v) = N - f(u) - e(v) - 2h_c, is there a set of pairs on which h_c is
   forced or controlled, and does distance injectivity then impose a Sidon-type
   or additive-energy bound on E and F? A failed attempt should end in a minimal
   counterexample, not a remark that the variables are dependent.
3. **Parity coupled to crowding.** The high block has a fixed number of odd and
   even targets. Refine the class capacities by the parities of the two depths
   and of the low median. Does the parity-resolved system exclude any case with
   r >= 9 before any depth search?
4. Anything that makes the fourteen open values collapse to finitely many
   *small* cases, or that replaces the delta ladder entirely.
5. An argument that order 25 is not decidable by any search of this shape, if
   that is what you conclude. A well-supported negative is worth more than a
   vague positive.

## Ground rules

Keep these apart and label every claim: **PROVED** (with a proof), **FINITE
VERIFIED** (a computation, with its exact scope), **OBSERVED** (a pattern, no
proof), **CANDIDATE**, **OPEN**. A finite computation over a fixed range is
never a proof of the general statement; the project has been careful about this
and expects the same.

For any new lemma, give the exact hypotheses and quantifiers, a proof, the
first (delta, r, m) it improves, and either a small independent positive control
or a minimal counterexample. If you propose a computation, state its size in
nodes or CPU-hours and how you arrived at that figure — the five routes above
were all killed by measurement, not by taste.

Do not re-derive what is already in the paper, and do not restate the problem
back. If your honest answer is that you see no better route than the fourteen
finite cases, say that plainly and say which of the fourteen you would attack
first and why.
