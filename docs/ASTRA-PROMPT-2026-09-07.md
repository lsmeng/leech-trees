# Second inspection prompt: a global obstruction for order 25?

You looked at this project on 2026-09-04 and proposed the signed first moment
`sum_{u<v} (-1)^{d(u,v)} d(u,v) = 150`, with its cut form
`sum_e w_e q_e (S - q_e)`. That was correct, it was new to this project, and it
is now cited in the paper as a remark with your contribution acknowledged.
We also measured it, which is the reason for this second prompt.

This time the question is narrower and, we think, sharper.

## What happened to the last idea, measured

We wired the signed moment together with the Wiener equation into the depth
phase of the order-25 class search (`abstract_class_search_moment.cpp`, four
levels, exact differential against the frozen delta = 284 certificates and
against an independent Python check on 4040 complete assignments at n <= 10).
The result was a **1.01x speed-up**. With seven or more free depths the two
integer linear equations are almost always solvable: structure-level kills were
8 of 1811, 4 of 2170 and 0 of 2736 on the three frozen records we ran. Pinning
the last two depths inside the DFS was 8.7x *slower*, because the distance
collision check kills branches before those depths are reached while the
memoisation is invalidated. Your own parity-pattern tables said the same thing
more cheaply (0 of 48 extra kills at r = 9, 1 of 88 at r = 10).

This is not a complaint. The identity is true and worth recording. But it tells
us something about the shape of the problem, and that is what we want you to
attack.

## The precise state of order 25

`N = 300`. Let `T` be a Leech tree of order 25 and `{a,b}` the unique pair at
distance 300, named so that `d(a,w) = N-1` for some `w`.

* **PROVED, no computation.** `diam(T - l) >= 281` for every leaf `l`. The
  argument is a crowding count: deleting a leaf leaves a block of
  `m = 300 - diam(T-l)` consecutive rooted depths, the `C(m,2)` distances inside
  the block fall into `r+1 = 25-m` classes, and inside a class a distance is a
  constant plus `y_i + y_j` with `y` in `[0, m-1]`, so a class holds at most
  `2m-3` of them. Hence `C(m,2) <= (r+1)(2m-3)`, which at `k = 24` fails for
  `m >= 20`.
* **PROVED.** The pair attaining `delta = diam(T-a)` contains `b`, so
  `delta = N - min f`, where `f(u) = N - d(b,u)`. The pendant weight at `a`
  satisfies `s >= N - delta`. On the path from `a` to the last common ancestor
  of the high block, consecutive vertices are at least `N - delta` apart in
  depth.
* **PROVED (Taylor, in two-anchor form).** With `e(u) = N - d(a,u)` and
  `f(u) = N - d(b,u)`, calling a vertex even when both are even, the parity
  count forces `beta(25 - beta) = 150`, so the number of odd vertices is
  exactly 10 or 15.
* **FINITE VERIFIED.** `delta = 281, 282, 283, 284` are excluded by exhaustive
  search of an explicit normal form, 1.64e9 structures at 284 alone, reproduced
  from frozen source.
* **OPEN.** Therefore: no Leech tree of order 25 exists **iff** the normal form
  is empty for each of the fourteen values `delta = 285, ..., 298`.

## The exact reason we are stuck, stated as sharply as we can

**Every constraint anyone has found is local, and the object has enough
freedom to satisfy all of them at once.**

Concretely, the crowding inequality is the only tool that ever excluded a value
of `delta`, and it needs a long top block: it bites at `m >= 20`, while the open
range is `m = 300 - delta <= 15` by definition. As `delta` grows the structural
pre-filter stops filtering. Measured survival of the depth-free phase:

| delta | r | low trees carrying structures | survival |
|---|---|---|---|
| 285 | 9 | 95 of 286 | 33% |
| 286 | 10 | 317 of 719 | 44% |
| 287 | 11 | 1523 of 1842 | 83% |

At `delta = 298` the normal form is a rooted tree on 24 vertices with 22 free
low depths and two pinned high vertices: it simply *contains* the generic
24-vertex problem. So the ladder cannot be finished, and this is not an
implementation weakness. Costs, all measured or extrapolated from measurements:
`delta = 285` about 1e4 CPU-h; `delta = 286` about 60 times that;
`delta = 287` about 5e7 CPU-h, which alone exceeds the whole-problem direct
search. Direct search at `n = 25` we measured by running `n = 19` and `n = 20`
to completion (4.74e11 and 3.88e12 nodes, growth factors 7.93 and 8.19, still
rising): 1.4e17 to 2.2e17 nodes, 2e7 to 3e7 CPU-hours.

What is missing is a **global** obstruction: something that looks at the whole
distance multiset `{1, ..., 300}` at once and derives a contradiction, the way
Taylor's parity argument does for inadmissible orders. Every invariant we have
tried instead constrains a bounded number of distances at a time, and with
7 to 22 free depths the system has room to satisfy them simultaneously.

## What we have already tried, so you do not repeat it

Each of these is either proved and unhelpful, or measured and unhelpful.

1. **Moment and generating-function identities.** `P(z) = sum_{u<v} z^{d(u,v)}`
   equals `z + z^2 + ... + z^N` identically. Taylor is `P(-1)`; `P(zeta) = 0` at
   every nontrivial 300th root of unity; Wiener is `P'(1)`; your signed moment
   is `P'(-1)`; and `P'(zeta) = -N/(1-zeta)` in general, with a cut
   decomposition that we verified numerically. As a residue pre-filter this is
   hopeless (the residue space is `60^24`) and inside an exact engine the tiling
   already implies it. We also checked that `P(i) = 0` yields no Taylor-type
   condition on `n` or on the depth-residue class sizes: the star with weights
   1,2,3,4 and the path with weights 1,1,1,1 have the same depth-residue
   multiset but mod-4 distance counts (2,3,2,3) and (1,4,3,2).
2. **Sidon-type bounds on the deficit sets `E = {e(u)}`, `F = {f(u)}`.** Not
   available: three pendant paths of heights `h, h+1, h+2` hanging in different
   branches at one foot put a 3-term arithmetic progression in each of `E` and
   `F` while all mutual distances stay distinct. Distance injectivity bounds
   neither additive energy. The spine is a Golomb ruler and that is already
   used.
3. **Hall / capacity refinements.** Joint interval Hall over unions of classes,
   demand-span, colored moment-Hall with parity resolution, partial-domain
   propagation, a global distance-slot flow. All implemented; on a complete
   candidate they are implied by the exact class sets, and the recorded minimal
   counterprofile at `r = 5` shows total capacity cannot improve the bound.
4. **Two-sided crowding** using `diam(T - {a,b})`: we proved
   `g_2 = 300 - diam(T-{a,b}) <= 46` (else `T - {a,b}` is a Leech tree of order
   23, against Taylor), and the far graph above that threshold is a double star.
   The resulting inequality degenerates to the one-sided one and needs
   `m_a >= 21`, which the open range never reaches.
5. **A charge identity.** With charges `+2` on the 15-vertex parity class and
   `-3` on the 10-vertex class, `5M + sum_e w_e (2a_e - 3b_e)^2 = 44400`, where
   `M` is the sum of the 45 minority-class distances. Correct, and its content
   is `sum_e w_e (2a_e - 3b_e)^2 <= 34050`. Under a random class placement the
   expectation of the left side is `45150/4`, about 11,290, three times below
   the bound, so we expect it to bite rarely.
6. **The chordal filtration.** For every `t`, the graph on the vertices whose
   edges are the pairs at distance `<= t` is chordal (balls in a tree are
   subtrees; subtree intersection graphs are chordal). This is a weight-free
   condition on which pair gets which rank. We found no case where it excludes
   anything.
7. **Alternative search orders.** A parameter-free two-anchor search (worse: a
   floor of 1.96e13 nodes for the part already known); a rooted-depth global
   search (over 1e12 CPU-h, pruning under 1%); top-window sumset tiling alone
   (patterns roughly double per level).

## What would actually help

In rough order of value to us.

1. **A global counting obstruction.** Something summing over all 300 distances
   or all 25 vertices that cannot be satisfied, for `n = 25` specifically or for
   `n = k^2` and `k^2+2` in general beyond Taylor. If you find one, we want the
   hypotheses, a proof, and the smallest `n` where it is not vacuous.
2. **A different reduction of the whole problem.** We have only ever reduced by
   deleting a leaf. Is there a reformulation as an exact cover, a perfect
   difference family, a question about Sidon sets in a group, a flow or a
   design, in which the order-25 instance becomes small rather than large? A
   reduction that makes the instance *different* rather than smaller is of
   interest even if it is not obviously cheaper.
3. **A theorem that the fourteen values collapse.** Anything showing that
   `delta` near 298 forces structure that `delta` near 285 does not, so that the
   expensive end becomes the easy end. At present the cost runs the wrong way.
4. **An argument that no search of this shape can decide order 25**, if that is
   your honest conclusion. We would rather have a well-supported negative than a
   vague positive; we have written several of the former ourselves.

## Ground rules

Label every claim **PROVED** (with a proof), **FINITE VERIFIED** (a computation,
with its exact scope), **OBSERVED**, **CANDIDATE**, **OPEN** or **NEGATIVE**. A
finite computation over a fixed range is never a proof of the general statement.
For any new lemma give exact hypotheses and quantifiers, a proof, the first
`(delta, r, m)` it improves, and either a small independent positive control or
a minimal counterexample. For any proposed computation give its size in nodes or
CPU-hours and say how you arrived at the figure: the routes above were killed by
measurement, not by taste. Nothing here claims order 25 is settled, and we would
rather you tell us the honest state than produce an idea that sounds new.

## Where the material is

Public: `https://github.com/LSMENG/leech-trees`, tag `v1.3-deposit-2026-09-07`;
Zenodo `doi:10.5281/zenodo.22654236` (code, certificates, data) and
`doi:10.5281/zenodo.22653637` (the paper). Locally, if you are on this machine,
the working tree is `/Users/geoclaw/Documents/claude/projects/leech-trees`;
`research_state.md` is the append-only log and records every route that failed
and why, `docs/fable-route-review-2026-09-05.md` is our own assessment of the
routes, and `theory-lab/double_end/THEORY.md` section 10 has the constraint
system for the closed case.
