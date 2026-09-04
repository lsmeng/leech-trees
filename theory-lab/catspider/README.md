# theory-lab/catspider — structured-family (caterpillar / spider / bi-spider) searches

Reproduction commands only; findings are reported in the session log / paper notes.

## Files
| file | what |
|---|---|
| `cs_forest.c` | bottom-up forced-forest DFS (clean-room engine `cleanroom/cr_forest.c` + `--shape all\|cat\|spider` pruning, MAXV=28, 16-bit dists). Build: `clang -O3 -DNW=3 -o bin/cs_nw3 cs_forest.c` (n<=20), `-DNW=5` (n=25), `-DNW=6` (n=27). |
| `oracle_shape.py` | independent brute-force oracle for the shape-restricted per-level counts (n<=10): `python oracle_shape.py n {all\|cat\|spider} --sumrule` |
| `spider_topdown.py` | top-down exact prover/enumerator for Leech spiders (incl. paths), `python spider_topdown.py n [Tlo Thi] [--paranoid]` |
| `spider_window_probe.py` | cap-aware exact numeric companion; reports the first missing high-value offset and optional window frontier |
| `spider_offset_prover.py` | finite relaxed offset search for the uniform regular region `U>W`, `T-U>W` |
| `spider_affine_prover.py` | affine symbolic search for the boundary strips `U<=10` and `T-U<=10` |
| `spider_affine_cleanroom.py` | independent immutable-state, full-recomputation checker for the affine strips |
| `verify_spider_uniform.py` | complete reproduction of the computer-assisted all-orders spider theorem |
| `bispider_topdown.py` | Python reference of the bi-spider (<=2 branch vertices) prover: `python bispider_topdown.py n {LR\|LL\|both} [--paranoid]` |
| `bispider.c` | C port of the bi-spider prover (paranoid recheck on by default). Build: `clang -O3 -o bin/bispider bispider.c`. Usage: `bispider n [LR\|LL\|both] [lo hi] [--r-lo R --r-hi R] [--fast]` (lo/hi shard the anchor loops; LR-only r filters use `r=N-2*T_R`; `--fast` is a non-certificate window probe that disables only the diagnostic full recomputation). |
| `bispider_cleanroom.py`, `verify_bispider_cleanroom.py` | independent immutable geometric enumeration and C cross-check, separately for LR/LL through n=10; every positive witness passes both repository checkers |
| `bispider_offset_prover.py`, `bispider_offset_cleanroom.py` | paired finite relaxation for the balanced-centre uniform LR region |
| `bispider_dominant_prover.py`, `bispider_dominant_cleanroom.py` | paired finite relaxation for the right-tip-dominant uniform LR region |
| `verify_bispider_regular.py` | one-command verification of both partial all-orders LR theorems |
| `bispider_strip_prover.py`, `bispider_strip_cleanroom.py` | paired finite relaxation for the bounded-imbalance LR strip |
| `verify_bispider_strip.py` | full primary and sampled/full clean-room verification of the 1,956-regime strip certificate |
| `bispider_smalla_positive_prover.py`, `bispider_smalla_positive_cleanroom.py` | paired finite relaxation for the small-A, positive-imbalance LR region |
| `verify_bispider_smalla_positive.py` | full per-A verification of the 50-regime small-A positive certificate |
| `bispider_smallb_positive_prover.py`, `bispider_smallb_positive_cleanroom.py` | paired finite relaxation for the small-B positive LR tail, including its long-spine stable regime |
| `verify_bispider_smallb_positive.py` | full per-regime verification of the 10,260-regime small-B positive certificate |
| `bispider_smalla_negative_prover.py`, `bispider_smalla_negative_cleanroom.py` | paired collision-class relaxation for the small-A negative LR tail |
| `verify_bispider_smalla_negative.py` | full per-regime verification of the 570-regime small-A negative certificate |
| `bispider_middle_tail_prover.py`, `bispider_middle_tail_cleanroom.py` | paired large-h relaxation for the small-A bounded-imbalance LR tail |
| `verify_bispider_middle_tail.py` | full per-regime verification of all 1,800 `(A,r)` middle-tail regimes |
| `bispider_ll_prover.py` | canonical-state prover for the three uniform LL regions at `n>=18` |
| `bispider_ll_near_cleanroom.py`, `bispider_ll_far_cleanroom.py`, `bispider_ll_small_cleanroom.py` | independent immutable LL searches for the near-centre, remote-centre and small-second-tip regions |
| `verify_bispider_ll.py` | full paired verification of all 2,305 LL regimes, including a finite partition audit |
| `bispider_region_coverage.py` | exact initially-legal LR anchor coverage of the six uniform regions |
| `theory_checks_catspider.py` | machine checks of the caterpillar lemmas L-A..L-D (reformulation, coordinate distinctness, pendant disjointness, window tiling) on the known trees + random distinct-distance trees |
| `results/` | run outputs (JSON lines as printed by the engines) |

## Validation chain (updated 2026-08-21)
1. `cs_forest --shape all` == `cleanroom/cr_forest` per-level node counts, n=4..13 (exact).
2. `cs_forest --shape cat|spider` == `oracle_shape.py` per-level counts, n=6..10 (exact).
3. Restricted bottom-up finds exactly the known trees: cat n=2,3,4(2),6; spider n=2 n/a(k>=2 needs n>=3), 3,4(2); 0 for all other n<=16.
4. `spider_topdown` n=3,4 finds exactly the known path/star/path trees; closes (0 sols) for n=5..18
   in agreement with bottom-up; `--paranoid` (full recomputation each node) clean for all n<=18, 25, 27.
5. `bispider_topdown.py` finds exactly the two n=4 trees and the n=6 double star L6; closes n=5,7..12.
6. `bispider.c` == Python reference branches/nodes/nsol exactly for n=4..13; paranoid recheck always on.
7. Uniform spider theorem: the relaxed regular search closes in 111 states at `W=10`; both affine implementations close
   all 20 boundary regimes in 1,123 states and agree on six invariants; exact numeric orders 5..15 and 60 tail instances
   agree.  Run `nice -n 10 python3 verify_spider_uniform.py`; proof: `../../docs/spider-uniform-theorem.md`; independent
   adversarial audit: `../../docs/referee-spider-uniform.md`.  The verifier deliberately rejects `python -O` because no
   proof-critical check may depend on optimization-sensitive assertions.
8. Clean-room bi-spider enumeration: a slot-based immutable search with full distance recomputation agrees exactly with the
   production C engine on anchors/nodes/solutions in each LR and LL regime for n=4..10 (27,046 nodes per implementation).
9. Uniform LR partial theorem: two implementations close the balanced-centre region at W=20 in 2,871 states and the
   right-tip-dominant region at W=15 in 1,881 states, both with zero frontier.  Run
   `nice -n 10 python3 verify_bispider_regular.py`; proof: `../../docs/bispider-progress.md`.
10. Bounded-imbalance LR theorem: two implementations agree on all 1,956 `(r,h)` regimes at W=50 and close 2,402,716
    states with zero frontier.  Together with item 9 this excludes every LR anchor whose smaller tip depth is `A>50`.
    Run `nice -n 10 python3 verify_bispider_strip.py --full-cleanroom`; proof: `../../docs/bispider-progress.md`.
11. Small-A positive LR theorem: two implementations agree for every `A=1,...,50` at W=20 and close 87,885 states
    with zero frontier.  Together with item 9, every surviving `r>20` anchor has `B<=20`.
    Run `nice -n 10 python3 verify_bispider_smalla_positive.py`; proof: `../../docs/bispider-progress.md`.
12. Small-B positive LR theorem: two implementations agree on all 10,260 finite `(A,B,Q)` regimes at W=20 and
    close 564,478 states with zero frontier.  The Q=81 regime represents the proved Q>80 stable tail; together with
    items 9 and 11 this excludes every `r>20` LR anchor.
    Run `nice -n 10 python3 verify_bispider_smallb_positive.py`; proof: `../../docs/bispider-progress.md`.
13. Small-A negative LR theorem: two implementations agree on all 570 finite `(A,C)` regimes at W=15 and close
    78,835 states with zero frontier.  B=C+16 represents every dominance gap and C=46 the proved C>45 stable tail;
    together with item 9 this excludes every `r<-15` LR anchor.
    Run `nice -n 10 python3 verify_bispider_smalla_negative.py`; proof: `../../docs/bispider-progress.md`.
14. Middle LR tail: two implementations agree per regime for every `1<=A<=50`, `-15<=r<=20` at W=35 and close
    1,386,587 states with zero frontier.  The proved threshold is
    `h=N-2A>max(35,2(35-A)+abs(r))`; it is automatic for `n>=18` because `N>=153`.  Together with items 9--13,
    this excludes every LR anchor at every order `n>=18`.
    Run `nice -n 10 python3 verify_bispider_middle_tail.py --jobs 4`; proof: `../../docs/bispider-progress.md`.
15. Complete LL theorem: a canonical-state prover and three separately written immutable searches agree per regime on
    all 2,305 W=36 regimes (740,594 states, zero frontier).  The three disjoint regions are `U>36,L<=36`,
    `U>36,L>36`, and `2<=U<=36`; the verifier also maps all 624,389 actual LL anchors at orders 18--40 into exactly
    one table entry.  The paranoid C engine independently closes all 2,825 order-18 LL anchors in 723,912 states.
    Together with item 14, this proves that no Leech tree of order `n>=18` has at most two branch vertices.
    Run `nice -n 10 python3 verify_bispider_ll.py --jobs 4`; proof: `../../docs/bispider-progress.md`; adversarial audit:
    `../../docs/referee-bispider-n18.md`.

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

## Next structural target

- OBSERVED: the independent geometric implementation matches every LR/LL regime through n=10; seven paired LR relaxations
  and three paired LL regions now exclude every bi-spider at every order `n>=18`.  The fixed-order order-27 run itself has
  not been independently reproduced in full, but it is no longer load-bearing for this all-orders conclusion.
- UNVERIFIED: the next structural target is at least three branch vertices, beginning with the exact three-branch and
  hop-diameter-at-most-four cases.  A separate project may test the stronger conjecture that the order-six double star is the
  only Leech bi-spider (no bi-spider for `n>=7`); it is not implied by the present `N>=153` bridge.
