# theory-lab/catspider — structured-family (caterpillar / spider / bi-spider) searches

Reproduction commands only; findings are reported in the session log / paper notes.

## Files
| file | what |
|---|---|
| `cs_forest.c` | bottom-up forced-forest DFS (clean-room engine `cleanroom/cr_forest.c` + `--shape all\|cat\|spider` pruning, MAXV=28, 16-bit dists). Build: `clang -O3 -DNW=3 -o bin/cs_nw3 cs_forest.c` (n<=20), `-DNW=5` (n=25), `-DNW=6` (n=27). |
| `oracle_shape.py` | independent brute-force oracle for the shape-restricted per-level counts (n<=10): `python oracle_shape.py n {all\|cat\|spider} --sumrule` |
| `spider_topdown.py` | top-down exact prover/enumerator for Leech spiders (incl. paths), `python spider_topdown.py n [Tlo Thi] [--paranoid]` |
| `bispider_topdown.py` | Python reference of the bi-spider (<=2 branch vertices) prover: `python bispider_topdown.py n {LR\|LL\|both} [--paranoid]` |
| `bispider.c` | C port of the bi-spider prover (paranoid recheck always on). Build: `clang -O3 -o bin/bispider bispider.c`. Usage: `bispider n [LR\|LL\|both] [lo hi]` (lo/hi shard the anchor loops; LR shards on T_L in [1,N/2], LL on T_1 in [N/2+1,N-1], ranges disjoint so one split shards both). |
| `theory_checks_catspider.py` | machine checks of the caterpillar lemmas L-A..L-D (reformulation, coordinate distinctness, pendant disjointness, window tiling) on the known trees + random distinct-distance trees |
| `results/` | run outputs (JSON lines as printed by the engines) |

## Validation chain (all reproduced 2026-08-20)
1. `cs_forest --shape all` == `cleanroom/cr_forest` per-level node counts, n=4..13 (exact).
2. `cs_forest --shape cat|spider` == `oracle_shape.py` per-level counts, n=6..10 (exact).
3. Restricted bottom-up finds exactly the known trees: cat n=2,3,4(2),6; spider n=2 n/a(k>=2 needs n>=3), 3,4(2); 0 for all other n<=16.
4. `spider_topdown` n=3,4 finds exactly the known path/star/path trees; closes (0 sols) for n=5..18
   in agreement with bottom-up; `--paranoid` (full recomputation each node) clean for all n<=18, 25, 27.
5. `bispider_topdown.py` finds exactly the two n=4 trees and the n=6 double star L6; closes n=5,7..12.
6. `bispider.c` == Python reference branches/nodes/nsol exactly for n=4..13; paranoid recheck always on.

## Main runs
- spider_topdown: n=25 (15058 nodes, 0 sols), 27 (18020, 0), 36 (33373, 0), 38 (37528, 0),
  49 (63676, 0), 51 (69302, 0); each rerun with --paranoid for 25/27 (identical).
- bispider: n=16 (1.19e6 nodes, 0), 18 (3.19e6, 0);
  n=25 FULL run x3 (identical replicas; a zsh quoting slip ran each "shard" over the full range):
  branches 32,882 / nodes 29,155,730 / nsol 0 / ~701 s each -> no Leech tree of order 25
  with at most two vertices of degree >= 3.  Shard-partition identity of `[lo hi]`
  verified exactly at n=12 (830+131+486=1447 branches, 53758+8826+28695=91279 nodes).
  n=27: 3 shards (1-80 / 81-175 / 176-350): branches 21400+8876+15167=45443,
  nodes 25731175+11836641+8294568=45862384, nsol 0 -> no Leech tree of order 27
  with at most two vertices of degree >= 3.
  (n=25 replicas renamed to results/bispider_25_full_run{1,2,3}.out.)
- bottom-up full: cat n=16: 999,661,866 nodes, 0; spider n=16: 436,856,251 nodes, 0.
- bottom-up cat n=25 prefix (`--maxlevel 13`): levels 0..13 =
  1,1,2,8,41,229,1379,8819,61966,471680,3899688,34661660,328609581,3304675701 (infeasible to finish).
