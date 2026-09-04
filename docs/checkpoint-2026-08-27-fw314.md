# Exact-return-33 checkpoint after FW314

Date: 2026-08-27

Repository head at checkpoint: `e96fc85` (`Certify all complementary owner
modes`), followed by this checkpoint-only update.

## Latest verified and observed conclusions

1. **FW313 VERIFIED / OBSERVED conditional reduction.**  Below order 36,
   Taylor's necessary order condition and the repository order-18 theorem
   reduce the FW312 exception to orders 25 and 27.  Exactly 41 union rows
   remain.  Their gate, least remote offset, bridge weight, paired receiver,
   and named top-strip owner are frozen in the FW313 certificate.  No one of
   the 41 rows is excluded.

2. **FW314 VERIFIED finite pressure audit.**  The two complementary low
   owners have the elementary cut trichotomy L-internal/J-internal/cross,
   with cap-owned four treated separately.  The ordinary modes are
   `LL,LJ,LX,JL,JJ,JX,XL,XJ,XX`; the exceptional modes are `4L,4J,4X`.
   Twelve actual weighted-tree controls independently realize every listed
   mode.  Every control has distinct edge weights and all pair distances
   distinct, exact return `(3,3,0)`, the four FW311 `B` holes, root-factor
   directness, `D intersect (D+4)=empty`, the claimed least remote owner, and
   the canonical sink.  Every control first misses distance five and violates
   its own order cap, so none is a Leech tree.

3. **Independent worker audit: VERIFIED within the stated boundary.**  The
   FW311, FW313, and FW314 replays passed and live FW314 output matched the
   committed certificate.  No prose/executable mismatch was found.  The
   certificate serializes `D_intersect_D_plus_4` as an empty list after an
   actual executable check; the analytic trichotomy itself is not a
   machine-generated theorem.

4. **Gemini evidence: PARTIALLY_USEFUL.**  Its broad X-mode exclusions were
   false because it confused arbitrary `g`-rooted `B` depths with fixed-core
   depths and confused `B` with the global `b_1`-root factor `D`.  The only
   accepted observation is conditional: when two J endpoints in a
   cross--cross rectangle are ancestor/descendant from `u`, their mutual
   distance is `|x|`, so fixed-core distance injectivity forces a branched
   LCA whenever `|x|` lies in the fixed-core spectrum.  This does not exclude
   a mode.

5. **ChatGPT Pro current X-mode round: no result.**  The round was explicitly
   asked to exclude an X-containing subfamily or return a smaller certified
   state, but the browser ended with `Thinking failed`.  No claim from that
   round entered the proof state, and the round was not restarted at this
   checkpoint.

## Earliest unclosed logical gap on the current exact-return-33 route

The earliest live gap in the remote `R2,t=4` branch is **root provenance for
the complementary low owners**.

FW311 proves that the least remote owner produces four missing rooted depths

```text
a+c_alpha, a+c_alpha+4, a+c_beta, a+c_beta+4 not in B.
```

The punctured low spectrum supplies actual pair owners of `c_alpha,c_beta`
(apart from cap-owned four), but an arbitrary pair owner does not become a
vertex rooted from the carrier gate `g`.  FW314 classifies those owners into
L/J/X/4 modes and derives class-specific LCA and hole constraints, but it
does not force any of the four receiving depths into `B`, a root-depth
difference four, an outlier, or a well-founded inherited exact-return state.

This gap is the **Evasive Complementary-Owner Exclusion** obligation.  Until
it is closed, Remote Complementary-Root Reception, remote-packet exclusion,
`R2,t=4`, the two-point cap, `g=7`, ERTC, NSSC, and global Leech-tree
nonexistence remain unproved.  The bounded 41-row Top-Strip Reception
Exclusion is a separate live obligation.

## Checks completed for the atomic FW314 step

Controller replay:

```text
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_all_owner_modes.py > /tmp/fw314-replay.json
.venv/bin/pytest -q
git diff --check
```

Result: FW314 replay passed; repository tests reported `5 passed`; the diff
check was clean.

Independent bounded worker replay:

```text
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_complementary_root_holes.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_small_order_top_strip.py
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_all_owner_modes.py
```

All passed and the live FW314 JSON matched the committed certificate.  The
worker also noted that `tests/test_checkers.py` collected zero tests; this
does not affect the five-test repository run above but should not be cited as
an additional test pass.

## Unfinished or finite-evidence-only items

- No L/J/X/4 owner mode is excluded under the full Leech hypotheses.
- No one of the 41 FW313 rows is excluded.
- The twelve FW314 controls are finite pressure evidence only and deliberately
  fail the low spectrum and global cap.
- The corrected Gemini collinear-J observation is conditional and not a mode
  exclusion.
- The attempted Pro X-mode round produced no answer.
- No inherited exact-return descent has been established inside a remote
  carrier.

## One minimal question for the external mathematical collaborator

> In the full `R2,t=4` punctured-tiling state, consider the surviving
> cross--cross monotone rectangle `(x,y)=(3,1)` at gate `g in {a,d_6}`.
> Prove or refute the following narrowly stated claim: after the collinear J
> endpoints are excluded by fixed-core distance injectivity, the required
> branched J-LCA arms `l,l+3` cannot simultaneously satisfy carrier
> directness, complete ownership of all distances below `s` except four, and
> the global no-outlier cap.  Do not restrict arbitrary `B` depths to the
> fixed-core depth table, do not identify `B` with the global `b_1`-root
> factor, and do not invoke FW286--FW288 without proving path-drop hypotheses.
> If the claim is false, give an actual distance-injective pressure control
> satisfying a strictly longer initial low interval than FW314.

This is a checkpoint, not the start of the next research epoch.
