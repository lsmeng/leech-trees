# Exact-return-33 checkpoint after FW319

Date: 2026-08-27

This checkpoint continues the frozen FW314 frontier.  It records five
separately replayable refinements.  It does not claim ERTC, NSSC, or global
Leech-tree nonexistence.

## Verified advances

1. **FW315: reflected-owner pressure.**  For an X-owner
   `c=w+b+r=s-delta`, with `eta=s-w`, both reflected values
   `b+delta=eta-r` and `r+delta=eta-b` are positive and below `s`.
   Complete low ownership must receive them, but FW314 forbids them as the
   corresponding rooted depths.  This adds a genuine ownership layer but
   does not exclude an X mode.

2. **FW316: exact six-distance rectangle.**  The four cross distances and
   the internal L/J distances leave exactly the lower, middle, and upper
   regimes stated in
   `docs/exact-return-33-g7-r2-t4-six-distance-rectangle.md`.  The middle J
   pair owns `q+2`; the upper regime has a rigid seven-term order.  No full
   regime is excluded.

3. **FW317: coreward incidence.**  The consecutive fixed-core depths at
   gates `a` and `d_6` force at least one monotone L endpoint into the
   fixed-core component.  Exactly one is coreward iff `kappa=0`; both are
   coreward iff `kappa>0`.

4. **FW318: attachment-cell exclusion.**  The actual fixed-core topology
   gives fourteen one-coreward cell/orientation rows.  The
   `d_6/(6,6,6)/O0` row is impossible because two distinct named pairs both
   have distance `b+1`.  This is the first genuine subfamily exclusion after
   FW314.  The reverse row forces named owners of `b,b+1,b+2,b+3,b+4`.

5. **FW319: pre-z five-block window.**  In that reverse row, the fixed-core
   spectrum and the carrier rooted difference-three condition give the exact
   current window

   ```text
   b=24 or b>=27.
   ```

   The excluded values are: `b=5` by endpoint coincidence plus the fixed
   distance eleven; `b=18` by `18-15=3`; and `b=25,26` by the fixed depth 23.
   No surviving value is asserted to extend to a full carrier.

## Corrections caught during the audit

- The FW311 complementary quantities are subpath differences in `R`; they
  are not automatically depths rooted at `u`.  No argument here uses that
  false basepoint strengthening.
- A preliminary scalar test tuple failed the existing FW309 global cap and
  was discarded.  It is not evidence against the theorem.
- Abstract weighted-tree controls and finite parameter scans remain
  diagnostic only; none is promoted to a Leech-tree realization or an
  asymptotic proof.

## Earliest live gap and next exact task

The global gap remains rooted reception for the complementary low owners.
The smallest new branch is now **Isolated-24 Reception** in the surviving
pre-`z` reverse cell.  At `b=24` the named block is `24,...,28` and the L-pair
distance is 49.  The next proof obligation is to show that complete low
ownership forces an additional carrier depth at 21, 22, 26, or otherwise at
difference three from 24 or 25.  Success would remove the isolated value and
push this cell to `b>=27`; it would still not by itself prove the global
conjecture.

The bounded 41-row FW313 top-strip problem remains a separate open branch.

## Replays completed

The five scripts

```text
verify_exact_return_33_g7_r2_t4_reflected_owner_pressure.py
verify_exact_return_33_g7_r2_t4_six_distance_rectangle.py
verify_exact_return_33_g7_r2_t4_coreward_incidence.py
verify_exact_return_33_g7_r2_t4_attachment_cells.py
verify_exact_return_33_g7_r2_t4_five_block.py
```

were replayed against their JSON certificates.  The repository test suite
reported `5 passed`, and `git diff --check` was clean.

## Trust boundary

The results above are exact symbolic/finite checks of the stated local
lemmas.  They do not verify complete low-spectrum ownership for an actual
survivor, construct a Leech tree, exclude all L/J/X/4 owner modes, close the
41 bounded rows, or establish an inherited descent.  The full conjecture is
still open in this project.
