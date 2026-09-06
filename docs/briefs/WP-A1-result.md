# WP-A1 result — (W) and (M) in the abstract_class_search depth stage

status: **done** (2026-09-06).  The unverified leftover was renamed to
`abstract_class_search_moment.cpp.stale-20260905` and never read; work restarted from the
483-line `abstract_class_search.cpp` (sha256 d833238707… = the frozen copy).
## Change summary — new `theory-lab/s1_crowding/abstract_class_search_moment.cpp`, 875 lines
* Rebuilds the complete order-n tree (R low, M high, anchor) with edge weights affine in
  `[1, s, l_1..l_{R-1}]`, cut sizes `|A_e|`, and per parity pattern the signed cut sums
  `q_e` and `S`.  Targets come from `N = n(n-1)/2`; nothing is pinned to n=25.
* Parity patterns are pre-filtered by `o(n-o) = ceil(N/2)` (|S|=5 at n=25): only 22 remain
  for even s, 14 for odd s, at r=8.
* `--moment-level 0..3` (`--no-moment` = 0, default 2); debug `--moment-selftest`, `--emit-rho`, `--no-memo`.
  - **1** exact (W),(M) test on every complete (s,L)  [brief item 3].
  - **2** + per-structure screen [item 1]: dead when no (s, parity pattern) passes the (W)
    interval bound, gcd divisibility of both residuals (`l = b + 2u` makes the step lattice
    `gcd(2c_i)`, subsuming a mod-8 test whenever 8 | gcd) and the 2-column lattice minor
    test of the joint system.  The DFS is untouched, so the hroot rho memo stays sound.
  - **3** + in-DFS pruning [item 2]: per-s solvability skip, `l_{R-1}` pinned by (W) alone,
    `l_{R-2}` pinned by the 2x2 (W),(M) solve per surviving pattern, falling back to
    enumeration when the two rows are dependent.
* Memo: the coarse rho key is hroot only, so an in-DFS moment prune invalidates it.  `dead_rho`
  is now written only when the run was not narrowed by the moment layer; at level >= 2 an
  exact second memo keyed by (hroot, per-high subtree size / even-index count / parent gap)
  — which determines W and every J — backs it up.
* Record format unchanged (counters appended after `leaf_checks`); `verify_depth_splits.py`'s
  LINE regex still matches.
## Validation
* order-6 genuine positive control `--m 3 --lowpar 0 --order 6`: every level returns the same
  single survivor `s=8 L=0,4 hpar=-1,0,0`, the known L6 Leech tree; csp_nodes 126/126/82/7.
* `--moment-selftest` recomputes both moments from the explicit tree at every complete (s,L):
  5470 assignments, n=5..12, r=2..6, 0 failures.
* Independent differential: of 4040 complete (s,L) from the level-0 engine (n=5..10, every low
  shape with r=2..5), a standalone Python check written from the tree definition says exactly
  9 satisfy (W),(M); levels 1, 2, 3 each return exactly those 9, 0 mismatches.
* DEPTH_SURVIVOR differential, memos on, n=5..11, r=2..6, all shapes: 1/2/3 == level 0.
## Differential table — frozen delta=284 r8 records
`ssh geo-ws` (100.111.22.15:22) timed out twice, so this is the authorised reduced laptop run:
3 of the 10 records, one at a time, `nice -n 15`, alarm 600 s.  Every level-0 run reproduces
its recorded certificate line exactly.

| shape | split | leaves old=new | nodes | csp_nodes old=new | surv | L0 s | L2 s | screen kills |
|---|---|---|---|---|---|---|---|---|
| 0,1,1,2,4,5,6 | 5:51/64 | 22527 | 24458525 | 5910945 | 0=0 | 37.74 | 37.46 | 8 / 1811 |
| 0,1,2,2,3,5,6 | 5:11/64 | 24450 | 26635592 | 7319857 | 0=0 | 47.60 | 50.94 | 4 / 2170 |
| 0,1,2,3,3,4,6 | 5:23/64 | 30620 | 27354187 | 10074403 | 0=0 | 61.34 | 55.19 | 0 / 2736 |

Level 3 on a 1e6-node prefix of 0,0,1,3,4,5,6 5:0/64: 364.7 s vs 41.8 s (8.7x slower) — the
pins are never reached (`mom_pins=0`; the CSP dies above level R-2) while the hroot memo
collapses (rho_csp_runs 595 -> 9774, csp_nodes 6.8M -> 73.3M); hence default 2.  Finding: at
r=8, delta=284 the equations alone almost never exclude a structure (8/1811, 4/2170, 0/2736)
— with 7 free depths the system is nearly always solvable; they bite when few depths are
free (order 6: 14 of 22 structures killed with no depth DFS at all).
## Binaries (g++ -O2)
old `abstract_class_search_base`  `0474e4372021b85fe09974acb086d4f08ea32d7a1c1450426b7d23997498182f`
new `abstract_class_search_moment` `6d0027e6c412de90b0efd6f6b5660f5c2077fdade076a69aca9bad6a8317047e`
new source `cbf2bc661f4aaaec3a865ea3c4971d57e2c65a99dfbaca97a647313ffcbccea1`

```json
{"status": "done", "speedup_smoke": 1.01, "blocking": "geo-ws unreachable (ssh timed out twice) so the r8 differential used the authorised laptop fallback: 3 of 10 records, all exact matches; level 2 is neutral at delta=284 because the moment system is nearly always solvable there, and level 3 is 8.7x slower because in-DFS pruning voids the hroot rho memo"}
```
