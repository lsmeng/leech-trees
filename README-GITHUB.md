# leech-trees — there is no Leech tree on 18 vertices

A *Leech tree* of order *n* is a tree on *n* vertices with positive-integer edge
weights whose C(n,2) pairwise path-weights are exactly {1, 2, …, C(n,2)}
(Leech, *Amer. Math. Monthly* 1975). Five are known (orders 2, 3, 4, 4, 6).
Taylor (1977) showed the order must be k² or k²+2; orders 9, 11 (Székely–Wang–Zhang 2005)
and 16 (Calhoun–Ferland–Lister–Polhill 2007) were excluded by computer, leaving
**n = 18 as the smallest open order** (FrontierMath open-problem list, EJGTA 2020, Integers 2016).

**Claim (this repository).** There is no Leech tree on 18 vertices.
The proof is an exhaustive search over *forced forests* (Calhoun et al., Alg. 2.7)
with complete isomorph rejection, so that every weighted forest that can be the set of
lightest edges of a Leech tree is generated exactly once up to isomorphism.
The search tree for (n, N) = (18, 153) has **59,779,854,336 nodes** and **no node at level 17**.
Its per-level node counts

```
level:   0  1  2  3   4    5     6      7       8        9          10          11
count:   1  1  2  8  41  229  1384   8899   62843   480085     3984162    35540837
level:          12            13              14              15             16   17
count:   332597341    2896330052    17017193146    37669242243    1824413062    0
```

are a mathematical invariant (number of non-isomorphic forced forests with k edges) and
were reproduced bit-for-bit by three runs of the reference engine (x86_64/gcc on a cluster
with two shard layouts, arm64/clang on a laptop) and by an independent clean-room
implementation written from the algorithm description alone.

The write-up is `paper/main.pdf` (draft). Status: computer-assisted theorem, human review
ongoing; see the "AI-assisted research statement" in the paper and `docs/`.

## Layout

| path | what |
|---|---|
| `src/forest_search.cpp` | **reference forest engine** (C++17, no deps): forced-forest DFS + isomorph rejection + sharding |
| `src/run_forest.py`, `src/verify_forest_run.py` | sharded local driver; verdict script for a sharded run |
| `cleanroom/cr_forest.c`, `cleanroom/verify_18.py`, `cleanroom/oracle_brute.py` | **clean-room re-implementation** (C), its verdict script and its own brute-force oracle |
| `src/leech_search.cpp`, `src/run_cpp.py` | **per-topology engine** (independent method; cross-check) |
| `src/checker_a.py`, `src/checker_b.py` | two independent Leech-tree checkers (BFS; depth+LCA) |
| `src/enumerate_trees.py`, `data/trees_{n}.jsonl` | unlabelled trees, two generators (networkx WROM, nauty `gentreeg`); `trees_18.jsonl` = 123,867 trees, frozen |
| `src/sat_encode.py`, `src/run_sat.py` | SAT route (CNF per topology, CaDiCaL/Kissat + DRAT proofs checked by drat-trim), n ≤ 11 |
| `src/solve_v*.py`, `src/run_order.py` | OR-Tools CP-SAT route (small n; oracle for the differential tests) |
| `src/filters.py`, `src/theory_checks.py` | one function per proven lemma (topology filters), self-tests |
| `tests/` | pytest suite + referee harnesses (`referee_forest_enum.py` = Python oracle for the forest search) |
| `results/` | per-shard records and depth histograms of every run (`hoffman2/`, `hoffman2_rep2/`, `forest_order_*.jsonl`, `cleanroom_forest_18_shard*.jsonl`, SAT/CP-SAT outcomes) |
| `docs/` | literature ledger, theory notes, engine notes, adversarial referee reports, clean-room report, paper draft |
| `paper/` | LaTeX source and PDF of the note (CC BY 4.0) |
| `scripts/` | build script, benchmark scripts, SLURM array scripts used on the cluster |

## Requirements

* C/C++ compiler (clang or gcc; `-O3 -march=native -std=c++17`), Python ≥ 3.10.
* Python packages: `networkx`, `numpy`, `pytest`; optionally `ortools` (CP-SAT route) and `python-sat` (SAT encoder).
* Optional external tools: nauty (`gentreeg`) for the second tree generator; `cadical`/`kissat` and
  `drat-trim` for the SAT route (`scripts/install_sat_tools.sh` builds drat-trim into `tools/`).

```
python3 -m venv .venv && .venv/bin/pip install networkx numpy pytest ortools python-sat
scripts/build.sh                       # -> bin/leech_search, bin/leech_search_nw8, bin/forest_search
clang -O3 -march=native -o cleanroom/cr_forest cleanroom/cr_forest.c
```

## Reproducing each layer

Numbers in **bold** are what you should get.

### 0. Checkers and known trees (seconds)
```
.venv/bin/pytest tests/test_checkers.py -q
```
Both checkers accept the five known trees in `data/known_leech_trees.json` and agree on 1000 perturbations.

### 1. Tree enumeration (minutes)
```
.venv/bin/python src/enumerate_trees.py 18      # needs gentreeg on PATH for the nauty route
```
**123,867** unlabelled trees on 18 vertices from both generators (n = 5, 9, 11, 16: 3, 47, 235, 19,320);
`data/trees_18.jsonl` is the frozen list used everywhere.

### 2. Forest engine, small orders (seconds to minutes; single core)
```
bin/forest_search 4      # 2 trees (star, path)     bin/forest_search 6   # 1 tree (double star)
bin/forest_search 12     # 0 trees, 704,494 nodes; depth: ... 8:58933 9:278539 10:356479
bin/forest_search 16     # 0 trees, 1,096,039,152 nodes, ~5 min
```
Expected: n = 4 → **2**, n = 6 → **1**, n = 5, 7…17 → **0** Leech trees. Per-level histograms are printed to stderr;
n = 16: `1 1 2 8 41 229 1384 8899 62843 480048 3968025 33269745 220001476 683511193 154735257 0`.
Regression tests (planted instances, symmetry completeness, sharding identities, agreement with the per-topology engine summed over topologies):
```
.venv/bin/pytest tests/test_forest_search.py tests/test_cpp_search.py -q
```

### 3. Forest engine, n = 18 (≈ 5–11 CPU-hours; sharded)
```
.venv/bin/python src/run_forest.py 18 --shards 512 --procs 8 --level 8      # local, resumable
# or one shard by hand:
bin/forest_search 18 --shard 0 210 --shard-level 8 2> shard0.err            # ~1.5 min; nodes=260865163
```
Verdict on a directory of shard records + stderr histograms (as archived in `results/hoffman2/`):
```
.venv/bin/python src/verify_forest_run.py 18 results/hoffman2 210 8
.venv/bin/python src/verify_forest_run.py 18 results/hoffman2_rep2 175 9
```
Expected: all K shards `DONE`, indices 0..K−1 once, every shard's levels ≤ L equal the prefix
`1 1 2 8 41 229 1384 8899 62843`, per-level sums equal the table above, **unique nodes = 59,779,854,336, nsol = 0**.
Σnodes over shards = unique + (K−1)·73,408 (K = 210: 59,795,196,608; K = 175, L = 9: 59,876,162,118; K = 512: 59,817,365,824).

### 4. Clean-room engine, n = 18 (≈ 9.5 CPU-hours)
```
cleanroom/run_shards.sh 18 100 8 5          # K=100 shards, L=8, 5 workers, resumable
python3 cleanroom/verify_18.py 18           # -> REFERENCE PER-LEVEL MATCH: True, unique nodes == 59,779,854,336: True, nsol 0
```
Small-order agreement with its own oracle: `python3 cleanroom/oracle_brute.py 12` vs `cleanroom/cr_forest 12 --no-sumrule`
(704,495 nodes; with the sum rule 704,494 — the rule fires exactly once at n = 12 and never at n = 18).
The n = 18 prefix through level 9 (480,085 forests) was checked with the Python oracle of `tests/referee_forest_enum.py`
(see `docs/referee-forest.md` §1 for the exact invocation).

### 5. Python oracle for the forest search (isomorph rejection is exact)
```
.venv/bin/python tests/referee_forest_enum.py 12          # n=4..12 (23 min at n=12): per-level counts == engine, 0 canonical-form collisions
python3 cleanroom/oracle_brute.py 12 --sumrule            # independent second oracle (clean-room side)
```

### 6. Per-topology engine (independent method)
```
.venv/bin/python src/run_cpp.py 9            # 47 topologies, all UNSAT (~5 s)      -> results/cpp_order_9.jsonl
.venv/bin/python src/run_cpp.py 11           # 235 topologies, all UNSAT (~5 s)
.venv/bin/python src/run_cpp.py 16 --procs 10 --time 3600   # 19,320 topologies, ~500–700 CPU-h; 19,308 UNSAT + 12 UNKNOWN at 1800 s cap
```
n = 18 over all 123,867 topologies is a cluster job (10⁴–10⁵ CPU-h, `scripts/hoffman2_cpp_array.sh`); partial at the time of writing.
Differential audit vs rule-free DFS and CP-SAT: `tests/referee_diff.py` (574 + 560 instances × 3 binaries × 32 flag subsets, 0 discrepancies).

### 7. SAT certificates, n ≤ 11 (minutes)
```
scripts/install_sat_tools.sh
.venv/bin/python src/run_sat.py 9  --procs 8       # 47/47 UNSAT, drat-trim VERIFIED
.venv/bin/python src/run_sat.py 11 --procs 8       # 235/235 UNSAT, drat-trim VERIFIED
```

### 8. Paper
```
tectonic paper/main.tex        # -> paper/main.pdf
```

## CPU costs (Apple M4 laptop unless noted)

| computation | cost |
|---|---|
| forest engine n = 16 | 321 s single core |
| forest engine n = 17 | 1.7 CPU-h (32 shards) |
| forest engine n = 18 | 5–11 CPU-h (cluster: 210 shards × ~1.5 min; laptop: 39,708 CPU-s at nice 10) |
| clean-room engine n = 18 | 34,207 CPU-s (100 shards, nice 15) |
| Python oracle to level 9 at n = 18 | 2.5 min; full n = 12: 23 min |
| per-topology engine n = 16 (all 19,320 trees) | ~500–700 CPU-h (cluster) |
| per-topology engine n = 18 (projected) | 10⁴–10⁵ CPU-h |
| SAT + DRAT n = 11 (235 trees) | minutes; does not scale to n = 16 |

## Status labels

Every claim in `README.md` and `docs/` is labelled OBSERVED / LITERATURE / UNCLEAR. The n = 18 verdict is
**OBSERVED, replicated four ways** (three reference-engine runs + clean-room). The per-topology cross-check on
n = 18 is still running; the paper marks it as pending. Referee reports: `docs/referee-forest.md`
(forest engine: no BUG found), `docs/referee-report.md` (per-topology engine; produced the correction to the
star-Sidon lemma).

## Citing

See `CITATION.cff`. Code and data: MIT; paper: CC BY 4.0 (`LICENSE`).

## Provenance

Search code, harnesses and drafts were produced by Claude (Anthropic) agents under the direction of the
author; all mathematical claims were checked by independent implementations (see paper §4); human review is
ongoing.
