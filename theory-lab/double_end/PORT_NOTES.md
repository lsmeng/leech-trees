# C++ port of the double-end search — notes and validation

Port of `double_end_search.py` to `double_end_search.cpp` (C++17, single file, no
dependencies).  Written 2026-09-02.

## Reference version

The port targets the **frozen** reference:

    theory-lab/double_end/frozen/double_end_search_frozen.py
    SHA-256 934b24162db8c0c2b2d88e10d4b0b7d0adc78eb70da42556bb563ceea1884eb3

Every Python-vs-C++ number below was produced against that file.

The live `double_end_search.py` drifted several times during the port.  After the
freeze it gained one further option, `force_e_upto` (default `0`, inert).  That
option is also ported (`--force-e-upto K`) and cross-checked against the live
Python — see the last table.  At the default the C++ is behaviourally identical
to both the frozen and the live Python.

## Compile command

    c++ -O2 -std=c++17 -o double_end_search double_end_search.cpp

Clean under `-Wall -Wextra`.

## CLI

    double_end_search <n> [options]
      --nodes-limit K        stop after K nodes (0 = unlimited)
      --max-solutions K      stop after K solutions (default 200)
      --split LEVEL K M      explore only shard K of M at recursion depth LEVEL
      --verify               rebuild each solution and BFS-check it
      --progress             progress lines on stderr every 20M nodes
      --quiet                suppress the per-solution lines
      --trace                one line per rec() call (state + depth), for diffing
      --debug                counters + a per-depth node histogram on stderr
      --no-hall --no-lb --no-attach --no-hc --no-deferred-check
      --no-ultra --no-cover --no-ub --no-parity --no-sym
      --stable-deferred / --unstable-deferred   (see "Sharding" below)
      --force-e-upto K       beyond the frozen reference; inert at K=0

Summary line:

    DOUBLE_END n=<n> N=<N> V=<V> split=<lvl>:<k>/<m> nodes=<nodes> solutions=<count> status=<...>

`split=-1:0/1` means "not sharded".  `status` is `EXHAUSTED`, `BAILED` (node
limit *or* solution limit reached) or `PARITY_IMPOSSIBLE`.  As in the Python, a
run with `--nodes-limit L` that bails reports `nodes = L+1`.

## Task 3a — exact agreement with the Python

Node counts *and* the set of `(e,f)` vectors, compared as sorted sets of
`(e_i, f_i)` pairs.

| n | symmetry break | python nodes | cpp nodes | python sols | cpp sols | solution sets | match |
|---|---|---|---|---|---|---|---|
| 3 | on  | 3     | 3     | 1 | 1 | identical | yes |
| 3 | off | 5     | 5     | 2 | 2 | identical | yes |
| 4 | on  | 8     | 8     | 2 | 2 | identical | yes |
| 4 | off | 15    | 15    | 4 | 4 | identical | yes |
| 6 | on  | 44    | 44    | 1 | 1 | identical | yes |
| 6 | off | 87    | 87    | 2 | 2 | identical | yes |
| 9 | on  | 24335 | 24335 | 0 | 0 | identical | yes |
| 9 | off | 48669 | 48669 | 0 | 0 | identical | yes |

Stronger than node counts: with `--trace` the C++ emits one line per `rec()`
call carrying `(g, nv, e[], f[], |deferred|)`, and the same trace is produced
from the Python by monkey-patching `Search.rec`.  The two traces are
**byte-identical** in all eight cases, i.e. the C++ visits the same 24335 (resp.
48669) nodes in the same order in the same state.

Regression against the independent ground truth
(`ground_truth_small.json`, counts 1,1,2,0,1,0,0,0 for n=2..9), with symmetry
breaking on:

| n | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|
| C++ solutions | 1 | 2 | 0 (parity) | 1 | 0 (parity) | 0 (parity) | 0 |
| ground truth  | 1 | 2 | 0 | 1 | 0 | 0 | 0 |

Differential against the independent vertex-order enumerator
`brute_double_end.py`, with **all** optional prunes off
(`--no-hc --no-attach --no-hall --no-lb --no-ultra --no-parity --no-cover
--no-ub --no-sym`):

| n | C++ relaxation solutions | brute_double_end distinct (E,F) | verdict |
|---|---|---|---|
| 3 | 2  | 2  | agree |
| 4 | 4  | 4  | agree |
| 6 | 12 | 12 | agree |

## Task 3b — prune soundness

Each prune disabled individually, `--max-solutions` effectively unlimited,
`--nodes-limit 40000000` (no run bailed).

n = 6 (baseline: 44 nodes, 1 solution, EXHAUSTED; the solution verifies):

| prune disabled | nodes | solutions | status | keeps all baseline solutions | extra solutions that verify as real trees |
|---|---|---|---|---|---|
| (none)                | 44  | 1 | EXHAUSTED | — | — |
| `--no-hall`           | 44  | 1 | EXHAUSTED | yes | — |
| `--no-lb`             | 44  | 1 | EXHAUSTED | yes | — |
| `--no-attach`         | 114 | 6 | EXHAUSTED | yes | **0** (5 extra, all REJECT) |
| `--no-hc`             | 45  | 1 | EXHAUSTED | yes | — |
| `--no-deferred-check` | 44  | 1 | EXHAUSTED | yes | — |
| `--no-ultra`          | 44  | 1 | EXHAUSTED | yes | — |
| `--no-cover`          | 44  | 1 | EXHAUSTED | yes | — |
| `--no-ub`             | 51  | 1 | EXHAUSTED | yes | — |
| `--no-parity`         | 47  | 1 | EXHAUSTED | yes | — |

n = 9 (baseline: 24335 nodes, 0 solutions, EXHAUSTED):

| prune disabled | nodes | solutions | status | keeps all baseline solutions | extra solutions that verify as real trees |
|---|---|---|---|---|---|
| (none)                | 24335    | 0  | EXHAUSTED | — | — |
| `--no-hall`           | 24335    | 0  | EXHAUSTED | yes | — |
| `--no-lb`             | 24335    | 0  | EXHAUSTED | yes | — |
| `--no-attach`         | 105230   | 18 | EXHAUSTED | yes | **0** (18 extra, all REJECT) |
| `--no-hc`             | 11942021 | 0  | EXHAUSTED | yes | — |
| `--no-deferred-check` | 25997    | 0  | EXHAUSTED | yes | — |
| `--no-ultra`          | 1462492  | 0  | EXHAUSTED | yes | — |
| `--no-cover`          | 24335    | 0  | EXHAUSTED | yes | — |
| `--no-ub`             | 28338    | 0  | EXHAUSTED | yes | — |
| `--no-parity`         | 24450    | 0  | EXHAUSTED | yes | — |

**Reading the `--no-attach` rows.**  Eight of the nine prunes leave the solution
set literally unchanged.  `attach_ok` does not: disabling it *adds* solutions (5
at n=6, 18 at n=9).  That is the expected direction and is **not** unsoundness —
`attach_ok` is a tree-realisability condition, not merely a search-order filter,
so switching it off enlarges the solution set of the relaxation.  The soundness
test that actually matters holds in both directions:

* no baseline solution is ever lost (the "keeps all" column is `yes` everywhere);
* every one of the extra solutions is rejected by `--verify`, each with the
  message `no on-path attachment vertex at p=...` — i.e. exactly the condition
  `attach_ok` encodes.  At n=9, 0 VERIFIED / 18 REJECT; at n=6, 1 VERIFIED (the
  baseline solution) / 5 REJECT.

So no prune drops a genuine Leech tree, and `attach_ok` removes only non-trees.

## Task 3c — `--verify`

`--verify` rebuilds the explicit tree exactly as `verify_solution()` does
(on-path chain by `p`, branches grouped by `p` and attached by the recorded
`h_c`), then BFSes all pairs and checks the distance multiset is `{1..N}`.  With
`--no-sym` (so both mirror images appear):

    n=3: e=1     f=2       VERIFIED  edges=[(0,2,2),(1,2,1)]
         e=2     f=1       VERIFIED  edges=[(0,2,1),(1,2,2)]
    n=4: e=1,2   f=3,4     VERIFIED  edges=[(0,3,4),(1,3,2),(2,3,1)]
         e=1,4   f=5,2     VERIFIED  edges=[(0,3,2),(1,2,1),(2,3,3)]
         e=5,2   f=1,4     VERIFIED  edges=[(0,2,1),(1,3,2),(2,3,3)]
         e=3,4   f=1,2     VERIFIED  edges=[(0,3,2),(1,3,4),(2,3,1)]
    n=6: e=1,2,3,7  f=12,13,4,8  VERIFIED edges=[(0,5,8),(1,3,2),(2,3,1),(3,5,5),(4,5,4)]
         e=12,13,4,8 f=1,2,3,7   VERIFIED edges=[(0,3,2),(1,5,8),(2,3,1),(3,5,5),(4,5,4)]

These are the known Leech trees: order 3 the path with weights 1,2; order 4 the
star 1,2,4 and the path 1,3,2 (2 trees up to isomorphism); order 6 the single
known tree.  Each appears twice, once per orientation of the anchor pair, and
symmetry breaking keeps exactly one of each pair — matching the ground-truth
counts 1, 2, 1.  n=9 yields no solutions, hence nothing to verify.

## Task 2 — sharding, and one correctness fix it needed

`--split LEVEL K M` keeps a global counter that increments once for every branch
the unsharded search would recurse into from a node at recursion depth exactly
`LEVEL` (depth = branch decisions already taken, root = 0), in DFS order, and
explores that branch only when `counter % M == K`.  The counter is incremented
immediately before the recursive call in all three options, so it numbers
exactly the children at depth `LEVEL+1`.

### The problem `--split` uncovered

The Python `undo()` restores a resolved deferred pair by **appending** it to the
end of `self.deferred`, not at the index it was removed from.  `rec()` is
therefore not state-neutral: it can return with `self.deferred` permuted.  Node
counts and solution sets are invariant under that permutation (the same set of
option-1 branches is tried either way, and each subtree is explored from
identical state), but the DFS *order* is not — and `--split` numbers branches in
DFS order.  A shard that skips a subtree skips the resolves inside it, so a later
node can see a different `deferred` order than the unsharded run did, and the
branch-to-shard assignment drifts.

This is not hypothetical.  With the Python's append-on-restore behaviour forced
on (`--unstable-deferred`), for n = 9:

| LEVEL | M | sum of shard nodes | required M·A + B | |
|---|---|---|---|---|
| 3  | 8 | 67502 | 67502 | ok |
| 5  | 7 | 67900 | 67900 | ok |
| 8  | 5 | 69712 | 69712 | ok |
| 10 | 4 | **69733** | **70201** | **shards lose 468 nodes** |

(measured on the pre-`ub_prune` build, where the unsharded run was 67432 nodes.)

### The fix

`--stable-deferred` restores the entry at the index it was removed from, making
`rec()` completely state-neutral and the shard numbering path-determined.
`--split` turns it on automatically.  `--unstable-deferred` forces the Python
behaviour back on, for diagnosis only.

`--stable-deferred` changes neither node counts nor solution sets — verified
directly for n = 3, 4, 6, 9 (3/8/44/24335 nodes and the same solutions either
way).  The default (no `--split`) is the faithful append-on-restore behaviour,
which is why the traces above match the Python byte for byte.

### Proof by exhaustion that the shards partition the run

Every node at depth ≤ LEVEL is visited by every shard; every deeper node is
visited by exactly one.  So with `A` = nodes at depth ≤ LEVEL and `B` = deeper
nodes, the shards must sum to `M·A + B`, and the multiset of visited nodes must
be `M` copies of the shallow part plus one copy of each deep node.  Both were
checked by dumping the full `--trace` of every shard and of the unsharded run and
comparing multisets of `(g, nv, e[], f[], |deferred|, depth)`:

| n | LEVEL | M | unsharded nodes | depth ≤ L | deeper | union of shards | predicted | node multisets |
|---|---|---|---|---|---|---|---|---|
| 9 | 3  | 8 | 24335 | 10  | 24325 | 24405 | 24405 | identical |
| 6 | 2  | 4 | 44    | 5   | 39    | 59    | 59    | identical |
| 6 (`--no-sym`) | 2 | 4 | 87 | 9 | 78 | 114 | 114 | identical |
| 9 | 10 | 4 | 24335 | 832 | 23503 | 26831 | 26831 | identical |
| 9 | 5  | 7 | 24335 | 78  | 24257 | 24803 | 24803 | identical |
| 9 | 0  | 3 | 24335 | 1   | 24334 | 24337 | 24337 | identical |

Solutions: for n=6, LEVEL=2, M=4 the shard solution counts are 0,0,0,1 summing
to the unsharded 1; with `--no-sym` they are 0,0,0,2 summing to 2; for n=9 all
shards report 0, summing to 0.  In every case the union of the shards' SOLUTION
lines is identical to the unsharded run's, with no solution appearing in two
shards.

## Task 4 — throughput probe on n=11

**The 200,000,000-node probe was not run.**  At the throughput measured on this
machine it would have taken roughly 15 minutes of wall time, far past the hard
4-minute cap.  What was actually measured, with `--nodes-limit 25000000`:

    ./double_end_search 11 --nodes-limit 25000000 --quiet --progress --debug
    DOUBLE_END n=11 N=55 V=9 split=-1:0/1 nodes=25000001 solutions=0 status=BAILED
    21.42s user, 111.56s wall (19% CPU)

| metric | value |
|---|---|
| nodes/s, CPU time | ≈ 1.17 × 10⁶ |
| nodes/s, wall clock | ≈ 2.24 × 10⁵ |
| did n=11 finish? | **no** — BAILED at 25M nodes |

The two rates differ by ~5× because the machine was heavily contended
throughout (load average ≈ 115 on 10 cores), so the process got about a fifth of
one core.  The CPU-time figure is the fair measure of the program; the wall
figure is what this machine actually delivered.  Extrapolating the CPU rate,
200M nodes is about 171 s of CPU — comfortably inside 4 minutes on an idle
machine, but ~15 minutes at the contention observed here.

**Not established:** whether n=11 terminates within 200M nodes.  All that is
shown is that it needs more than 25M.  n=9 needs 24335 nodes, so n=11 is at
least ~10³ times larger; it is a good candidate for `--split`.

## Discrepancies found and how they were resolved

1. **Candidate-list aliasing (my bug).**  The option-2 candidate list was first
   implemented as a `Search` member vector to avoid per-node allocation.  A
   recursive call rebuilt it and clobbered the parent's iteration, so n=6 gave
   160 nodes / 0 solutions against the Python's 101 / 2.  Found by diffing the
   `--trace` output against a monkey-patched Python trace: the first divergent
   node had `nv=3` with `f[3]` set, an impossible state.  Fixed by moving
   candidates to a flat stack-disciplined pool (`candStack`), as was already
   done for the option-1 snapshot of `deferred`.  All other scratch buffers
   (`LBs`, `UBs`, `hbuf`, matching arrays) are only used inside non-recursive
   helpers and are safe as members.

2. **Deferred-list ordering vs sharding** — see Task 2 above.  Not a port bug;
   a property of the reference that only sharding exposes.

3. **Python floor division.**  `pair_hc`, `_h_ub` and the `hc` helper inside
   `verify_solution` can take a negative numerator, where Python's `//` floors
   and C++ `/` truncates.  A `floordiv()` helper is used at those three sites.

4. **Reference churn.**  The Python changed five times mid-port (the `rescan`
   loop, `lo = g` in `lb_prune`, the rewritten `hc_heights`,
   `ultrametric_ok`/`class_ok`, `cover_ok` + `exempt`, `ub_prune`, symmetry
   breaking).  Everything above is against the frozen SHA-256.

5. **`force_e_upto` is not solution-preserving.**  Ported for
   forward-compatibility and cross-checked against the live Python; it agrees at
   every setting tried.  But note it *loses solutions* when nonzero — n=4 drops
   from 2 solutions to 0 at K=3, n=6 from 1 to 0 at K=5 — so it is a search
   restriction, not a sound prune.  Default `0` is inert.

   | n | K=0 | K=1 | K=2 | K=3 | K=5 |
   |---|---|---|---|---|---|
   | 4 | 8/2 | 8/2 | 5/1 | 3/0 | 3/0 |
   | 6 | 44/1 | 44/1 | 24/1 | 16/1 | 5/0 |
   | 9 | 24335/0 | 24335/0 | 24041/0 | 5646/0 | 1652/0 |

   (nodes/solutions; C++ and Python agree in all 15 cells.)

## Implementation notes

* State mirrors the Python one-for-one: `e[]`, `f[]`, `nv`, `alpha`, `beta`,
  `taken[]` (byte array), `pv[]` (flat V×V, `0` undetermined / `-1` deferred),
  `deferred` (a vector with the same `erase`/`push_back` semantics), `cov[]`,
  `exempt[]`.
* One global trail vector replaces the Python's per-frame `trail0` + `trail`.
  That is equivalent: `trail0` is filled entirely by `rescan` before any branch
  pushes onto `trail`, and undo is LIFO throughout, so the two stacks are
  disjoint in time.  `rec()` records `mark0 = trail.size()` and undoes to it on
  exit, reproducing the Python's `try/finally`.
* `hall_partners` uses Kuhn's algorithm with timestamped visit arrays instead of
  Python sets.  Set iteration order affects which matching is found but not
  whether one exists, so the boolean result is order-independent.
* `deferred_ok` carries a `v < N` guard on the scan.  It is unreachable:
  `base + 2·hmax = N − |e_i − e_j|` for a tied pair, and coordinate values are
  distinct, so the top of the window is at most `N−1`.
