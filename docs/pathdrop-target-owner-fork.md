# Path-drop target first-owner fork (FW290)

FW288 gives a complete local record joining the terminal owners of one path
drop.  PRCC must also compare the incoming path with the target edge's own
first owner.  FW290 records the exact order of those two target-cut events.

This is a **PROVED all-order fork**.  It also gives a **STRICT STOP** for
treating the next owner distance as a decreasing skeleton-weight potential.

## 1. Target-cut order

Let `q -> r` be a path drop with

```text
p=w_q,             g=w_r,             delta=p-g>=1.
```

At the `r` cut, the old edge `q` is a same-side owner at offset `delta`.
Let

```text
theta=eta_r
```

be the first compensated same-side offset at `r`, with unique owner `P_r`.
By minimality,

```text
theta<=delta.                                           (FW290.1)
```

The full-window capped ledger hypotheses used by FW284 guarantee that
`theta` exists and is in the usual Leech range.  This order statement is not
available in a non-covered target ledger that stops at an uncompensated gap.

## 2. Equality: exact edge-lift return

If `theta=delta`, then

```text
d(P_r)=g+theta=g+delta=p=d(q).
```

Distance injectivity forces

```text
P_r=q.                                                  (FW290.2)
```

The pair `q` is a single skeleton edge and cannot lie wholly inside a
first-level cap.  Hence the FW284 transition from `r` is exactly

```text
r --edge lift--> q.                                     (FW290.3)
```

Together with the incoming path drop, this is the directed two-cycle

```text
q --path drop--> r --edge lift--> q.                    (FW290.4)
```

Known `L6` realizes this at weights `8 -> 5 -> 8`.  An order-five
distance-injective tree with nontrivial sink realizes `9 -> 8 -> 9`.  The
second tree is not Leech, so complete nontrivial-sink coverage is still
available as a possible two-cycle exclusion mechanism.

## 3. Strict inequality: sub-source next owner

If `theta<delta`, integrality gives

```text
d(P_r)=g+theta<=g+delta-1=p-1.                          (FW290.5)
```

Thus the target's next owner lies strictly below the dropped source weight.
This is a useful owner-level record, but it is not a skeleton-weight descent.

An actual order-eight distance-injective control has

```text
22 --path drop--> 16,
theta=1,             d(P_16)=17<22,
16 --cap lift--> 39.
```

The cap promotion can therefore send the next skeleton edge above the old
source even though the owner path itself is below it.  This freezes the
following inference:

> **STRICT STOP (FW290).**  Do not use `d(P_r)<w_q` as a decreasing potential
> on skeleton-edge weights without also controlling cap promotion.

On an actual directed cycle whose chosen `q` has maximum weight, the same cap
promotion cannot exceed `w_q`; nevertheless it can return to `q` or erase the
strict owner decrease.  FW289's cap rectangle data are needed to analyse that
case.

## 4. Remaining cycle fork

Every path drop now has two exact target-compatibility outputs:

```text
E: theta=delta    exact path-drop/edge-lift two-cycle;
S: theta<delta    target first owner has distance at most w_q-1.
```

The smallest live cycle obligations are therefore:

1. **UNVERIFIED Exact-Return Two-Cycle Exclusion (ERTC):** exclude (FW290.4)
   in a Leech tree with nontrivial full-window sink using complete coverage
   and the FW288 local record.
2. **UNVERIFIED Strict-Branch Cap Compatibility (SBCC):** if the strict
   target owner is promoted by a cap lift, combine its retained endpoints
   with the FW289 direct/remote rectangle record instead of discarding the
   decrease.

PRCC reduces to ERTC/SBCC plus compatibility for strict branches whose next
arc is an edge lift or another path drop.  Neither item is proved here.

## 5. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_pathdrop_target_owner_fork.py
theory-lab/topwindow/results/pathdrop_target_owner_fork_certificate.json
```

It checks the known `L6` equality, a nontrivial-sink equality control, both
forks in one skeleton, and the strict-owner/cap-escape counterexample.

**Proved:** (FW290.1)--(FW290.5), including exact return classification and
the strict sub-source owner bound.

**Not proved:** ERTC, SBCC, full PRCC, RCRT, cap-to-boundary transport, cycle
compatibility, NSSC, nontrivial-sink exclusion, G18, any order exclusion, or
global Leech-tree nonexistence.

**Verdict: PROOF + STRICT SCALAR-POTENTIAL STOP.**

## 6. FW291 exact-return boundary

FW291 rewrites the equality branch as the forced target-cut color strip
`BC^delta AB^eta BC`, or equivalently two correlated rooted convolutions with
a complementary prefix, gap and return.  Known `L6` realizes full coverage
with a singleton sink, while non-Leech controls realize nontrivial connectors
and the complete local strip.  Thus the strip alone is a strict-stop
mechanism; ERTC must use global coefficients outside it together with the
nontrivial connector.  See `docs/exact-return-switchback-stop.md`.
