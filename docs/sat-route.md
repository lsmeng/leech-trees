# SAT route: certificate-producing decision of "topology T admits a Leech labeling"

Status labels as in README (OBSERVED = measured here on 2026-08-18, M-series Mac, 10 cores).
Code: `src/sat_encode.py` (encoder), `src/run_sat.py` (sharded/resumable driver),
`scripts/install_sat_tools.sh` (cadical 3.0.1, kissat 4.0.4, python-sat 1.9, drat-trim from
github.com/marijnheule/drat-trim built into `tools/`).  Results: `results/sat_order_{n}*.jsonl`.

## 1. Encoding (final = `--variant order`)

Let N = C(n,2) and let pairs p = {u,v}.  All variants share:

* **Domain pruning per pair** (sound, static).  A path with k edges strictly contains
  C(k+1,2)-1 sub-paths whose sums are distinct and smaller, so `d(p) >= C(k+1,2)`.  If removing
  the path's end-edges leaves side components of a and b vertices, the a*b-1 paths strictly
  containing it are all larger, so `d(p) <= N - (a*b-1)`.  (Consequences: value N is a
  leaf-leaf pair, values 1,2 are edges, ...)  Domain sizes at n=11 shrink the 55x55 matrix by
  ~30 %; at n=16/18 by less.
* **One-hot pair/value variables** `x[p][d]` (d in dom(p)) with exactly-one per pair (row) and
  exactly-one per value (column).  AMO = pairwise for <=6 literals, sequential counter otherwise
  (`pysat.card`; ladder/totalizer selectable via `--amo`).
* **Tree structure through a root r (a center).**  Pairs (u,r) are the root distances.  Every
  other pair (u,v) with lca l satisfies exactly one ternary relation `X = Y + Z` over pair
  variables: if l is neither endpoint, `(u,v) = (u,l) + (v,l)`; if l = v (ancestor),
  `(u,r) = (v,r) + (u,v)`.  So there are exactly C(n-1,2) relations (136 at n=18) and no adder
  networks: every path sum is a prefix-sum difference along the tree.
* **Symmetry breaking**: children of the same vertex whose rooted subtrees are isomorphic (AHU
  string) get strictly increasing weights on the edge to the parent (weights are distinct, so
  the strict lex-leader is sound).  Not broken: the bicentral half-swap (factor <= 2).
* **Optional Taylor parity** (`--parity`): the number of vertices at odd weighted root distance
  m must satisfy m(n-m) = ceil(N/2) (n=18: m in {7,11}); encoded with totalizers.  Empirically
  it *hurts* (see 3), so it is off by default.

Relation encodings compared:

| variant | clauses for X=Y+Z | idea |
|---|---|---|
| `onehot --dirs 1` | `Y=y & Z=z -> X=y+z` (or conflict if y+z out of dom) | support in one direction only |
| `onehot --dirs 3` | + `Y=y & X=x -> Z=x-y`, `Z=z & X=x -> Y=x-z` | forward checking all directions |
| `order` (**default**) | order literals `g[p][d]` = "value(p) >= d", channelled to `x[p][d]` (3 clauses/value); bounds clauses `Y>=a & Z>=b -> X>=a+b`, `Y<=a & Z<=b -> X<=a+b`, and the same for `Y = X - Z`, `Z = X - Y` (6 families, O(|dom|^2) each) | bounds consistency on every ternary sum, cheap unit propagation |
| `hybrid --dirs k` | order + onehot support | both |

Sizes (median over topologies): n=9 `order` ~1.0e5 clauses; n=11 ~3.9e5 clauses / 9.5e3 vars;
n=16 ~5.0e6 clauses (~90 MB DIMACS); n=18 estimated ~1.0e7 clauses (~200 MB).

Solver: `cadical -q -t T cnf proof` (binary DRAT).  Kissat also works (`--solver kissat`).
UNSAT proofs are checked with `drat-trim cnf proof` (result string recorded in the field
`drat`); SAT witnesses are decoded and passed through both `checker_a` and `checker_b`.

## 2. Validation (OBSERVED)

| n | topologies | result | check |
|---|---|---|---|
| 4 | 2 | both SAT | witnesses pass checker_a and checker_b (star 1,2,4; path 3,1,2 rooted differently, both Leech) |
| 6 | 6 | id 3 SAT (= known L6, `[(0,1,5),(0,4,1),(0,5,2),(1,2,4),(1,3,8)]`), 5 UNSAT | witness passes both checkers; all 5 DRAT proofs `VERIFIED` |
| 9 | 47 | all UNSAT | 47/47 `drat-trim: VERIFIED` (onehot-3, order, kissat, onehot-1 runs all agree) |
| 11 | 235 | all UNSAT | 235/235 `VERIFIED` (`results/sat_order_11.jsonl`) |

These agree with CP-SAT (`results/order_9.jsonl`, `order_11.jsonl` where the latter had 7 UNKNOWNs
which SAT now settles) and with the literature (SWZ 2005).

## 3. Benchmarks (OBSERVED, single-threaded solver processes, 8 in parallel)

Encoding ablation on a fixed random sample of 24 n=11 topologies (`--sample 24 --seed 1`),
cadical unless noted, cap 300 s, no proof checking during ablation:

| config | sum solve time (s) | max (s) | sum proof size |
|---|---|---|---|
| onehot dirs=1 | 1863 | 197 | 2.6 GB |
| onehot dirs=3 | 837 | 134 | 0.97 GB |
| hybrid dirs=3 | 934 | 156 | 0.30 GB |
| hybrid dirs=1 | 280 | 40 | 0.26 GB |
| **order** | **205** | **29** | **0.22 GB** |
| order + kissat | 241 | 38 | 0.26 GB |
| order, no symmetry breaking | 1260 | 191 | 0.84 GB |
| order + Taylor parity | 549 | 91 | 0.23 GB |

Take-aways: bounds propagation on the ternary sums (order encoding) is worth ~9x over one-hot
support clauses; symmetry breaking is worth ~6x; the Taylor parity constraint (as a totalizer)
slows cadical ~2.5x (it is implied and just adds noise); cadical slightly beats kissat.

Full runs with the default (`order`, cadical, sym on, parity off):

| n | # | solve time: sum / median / max (s) | proof size: sum / median / max | drat-trim: sum / median / max (s) |
|---|---|---|---|---|
| 9 | 47 | 83 / 1.5 / 6.0 (order run; onehot-3 run: 113 / 1.9 / 6.7) | 50 MB / 1.1 / 2.8 MB | 131 / 2.2 / 9.4 |
| 11 | 235 | 5131 / 16.9 / 101.7 | 2.7 GB / 9.0 MB / 47.9 MB | 10222 / 31.9 / 241.5 |
| 16 | 30 random (seed 0), cap 600 s | see table below | | |

drat-trim verification costs about 2x the solve time and proofs are ~0.5 MB per solver-second.

n=16 sample (30 topologies, cap 600 s each, `results/sat_order_16.jsonl`):
| item | value |
|---|---|
| topologies | 30 (ids [1326, 2416, 3107, 3236, 3299, 4563] ...), `--sample 30 --seed 0` |
| status | 30/30 TIMEOUT at 600 s (0 decided) |
| clauses / vars (median) | 4784236 / 48704 |
| DIMACS size (median) | 94 MB, encode+write 13 s |
| partial DRAT proof after 600 s (median / max) | 134 MB / 164 MB |
| C++ engine, its own random n=16 sample (200 topologies, `results/cpp_bench16_sample.jsonl`, other agent's run) | 170 UNSAT (median 12 s, max 198 s), 30 UNKNOWN at its cap |

For calibration, the purpose-built C++ engine (`src/leech_search.cpp`, other agent) decides most random
n=16 topologies in seconds to minutes (`results/cpp_bench16_sample.jsonl`), i.e. plain CDCL on this
encoding is 1-3 orders of magnitude slower than value-mode backtracking with bitset pruning.

Cube-and-conquer probe (n=16 topology 4943, which times out at 900 s): fixing the pair that
carries value N (28 leaf-leaf candidates) makes one cube UNSAT in 167 s (92 MB proof) with the
machine oversubscribed; a full level-1 split is therefore ~28 x 170 s ~ 1.3 CPU-hours per
topology, level-2 (values N and N-1, ~1200 cubes) is estimated similar or better.  Level-2 probe on the same topology (value N on the first leaf-leaf pair, value N-1 on each of 41 candidates): 11/16 cubes refuted in ~2 s (= CNF parse time; the pair carrying N-1 must share an endpoint with the pair carrying N and unit propagation finds that), the other 5 in 34-47 s with 63-74 MB proofs.  Summed over the 41 cubes this is ~270 s, i.e. no CPU gain over the level-1 cube (167 s) beyond parallelism, and ~1-2 CPU-hours per topology in total; the fixed ~90 MB CNF parse per cube dominates the easy cubes, so an incremental/assumption-based driver would be needed for anything larger.

## 4. Honest assessment for n=18 (123,867 topologies)

* Growth: median solve time per topology went 0.02 s (n=6) -> 1.9 s (n=9) -> 17 s (n=11) ->
  >600 s (n=16, 0/30 solved in the cap).  Roughly x10 per extra vertex.  Extrapolating, a
  single n=18 topology is 10^4-10^5 CPU-seconds with plain CDCL, and the proofs would be
  10-100 GB each; drat-trim would need comparable time and RAM.  All 123,867 topologies:
  ~10^9-10^10 CPU-seconds.  **Not feasible as the primary search**, even on Hoffman2.
* Proof size is the second wall: at n=11 the average proof is already 11 MB; at n=18 a
  certificate library for all topologies would be petabytes unless proofs are trimmed
  (drat-trim `-l` LRAT output after trimming is much smaller) and only proof hashes are kept.
* What the SAT route IS good for:
  1. **Independent, machine-checkable certificates for n <= 11** (done: 235 + 47 + 5 DRAT
     proofs verified) and, with cube-and-conquer, for individual n=16 topologies (order 1
     CPU-hour each, so a few hundred selected topologies are affordable, all 19,320 are ~2e4
     CPU-hours = borderline for a cluster).
  2. **Certifying the residual** of the real n=18 pipeline: theorem filters + C++ search leave a
     set of topologies that the C++ engine decides; a certificate for the whole claim only
     needs (a) trusted enumeration, (b) trusted filters, (c) per-topology certificates.  If the
     C++ engine can dump its top-k decision levels as cubes (value-mode: which unassigned edge
     receives the next missing value), each cube is a small SAT instance whose DRAT proof is
     checkable, and the cube set's completeness is itself a (tiny) DRAT-checkable tautology.
     This is the standard cube-and-conquer certificate and reuses the C++ engine's far better
     branching while keeping the proof independent of the C++ pruning code.
  3. Alternatively (not implemented): PB proof logging.  Encoding the moment identity
     `sum_e w_e s_e (n-s_e) = N(N+1)/2` and Hall counting natively as PB constraints and
     running RoundingSat with VeriPB logging would keep the C++ engine's strongest prunes inside
     a certified solver; the C++ engine's own value-mode branching cannot be forced onto
     RoundingSat either, so expect the same 10^2-10^3 gap unless the engine emits VeriPB
     itself (best long-term option: instrument `leech_search.cpp` with VeriPB "rup"/"pol"
     lines per pruned node).
* Bottom line: the SAT/DRAT route is validated and gives clean nonexistence certificates up to
  n=11 today; it is not a route to n=18 by itself.  For n=18 the certificate must come from
  cube-and-conquer driven by the C++ engine's decisions or from proof logging inside the C++
  engine.

## 5. Reproduce

```
bash scripts/install_sat_tools.sh
.venv/bin/python src/run_sat.py 9  --procs 8 --timeout 600            # 47 UNSAT + drat-trim
.venv/bin/python src/run_sat.py 11 --procs 8 --timeout 600            # 235 UNSAT + drat-trim (~35 min wall)
.venv/bin/python src/run_sat.py 16 --procs 8 --timeout 600 --sample 30 --seed 0
.venv/bin/python src/run_sat.py 11 --sample 24 --seed 1 --variant onehot --dirs 1 --tag _s24_d1 --no-check   # ablations
.venv/bin/python src/sat_encode.py 11 124 -o /tmp/t.cnf               # dump one DIMACS
```
`--keep-proofs` copies CNF+DRAT into `results/proofs/n{n}/` (git-ignored) for archival.
