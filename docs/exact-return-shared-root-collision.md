# Exact-return shared-root outer collision (FW293)

FW292 leaves 50 parameter types with separated-root local witnesses and two
additional types that can survive only on the zero-connector face.  The latter
are impossible for a reason already visible inside the two outer components:
both contain a distinct owner of distance two.  Some of the remaining 50
types may also admit optional coincident-root signatures; FW293 does not
classify those alternatives.

This is a **PROVED exclusion of the FW292 shared-root branch**.  It does not
exclude any of the 50 separated-root types and does not prove ERTC.

## 1. Setup inherited from FW291--FW292

Removing the two exact-return edges gives the disjoint vertex partition

```text
A -- q -- B -- r -- C.
```

Write `a_0` for the endpoint of `q` in `A` and `c_0` for the endpoint of `r`
in `C`.  The rooted outer factors are

```text
U={d(a_0,a):a in A},
W={d(c_0,c):c in C}.
```

FW292 proves that the only locally surviving rows with coincident inner roots
are

```text
(delta,eta)=(8,8), (8,10).                         (FW293.1)
```

The earlier row `(8,9)` is already impossible because coincident roots would
make the depth-8 inner vertex simultaneously present and absent.

## 2. The two forced outer factors

FW283's thin-bouquet orientation is not symmetric in the extremal rows.  It
forces the outer factor to be

```text
O_8 ={0,2},
O_10={0,2,8}.                                      (FW293.2)
```

At the `r` cut, `delta=8`, so `W` contains a vertex `c_2` with

```text
d(c_0,c_2)=2.                                      (FW293.3)
```

At the `q` cut, `eta` is either 8 or 10.  In both cases (FW293.2) says that
`U` contains a vertex `a_2` with

```text
d(a_0,a_2)=2.                                      (FW293.4)
```

## 3. Actual-owner collision

The two unordered pairs in (FW293.3)--(FW293.4) are distinct.  The first is
contained in `C`, the second in `A`, and `A` and `C` are disjoint components
after the two distinct edges `q,r` are removed.  Thus the hypothetical global
tree has two different owners of distance two:

```text
{c_0,c_2} != {a_0,a_2},
d(c_0,c_2)=d(a_0,a_2)=2.                            (FW293.5)
```

This contradicts distance injectivity.  Complete `[1,N]` coverage, the exact
return coefficient at `D`, and coefficients beyond `D` are not needed.
Consequently

> **FORCED-SHARED-ROOT EXCLUSION (FW293).**  Neither `(8,8)` nor `(8,10)` can
> occur in an exact-return state.  Thus no FW292 parameter type survives only
> by forcing the two inner roots to coincide.

The `L6` control is unaffected: it has `(delta,eta)=(3,1)`, so FW283 does not
force two outer depth-2 owners.

## 4. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_shared_root_collision.py
theory-lab/topwindow/results/exact_return_shared_root_collision_certificate.json
```

It rebuilds the FW283 table and thin-bouquet orientations, replays the FW292
matched classification, and records the two distinct symbolic owner pairs for
both remaining zero-connector rows.

**Proved:** both FW292 types forced onto the zero-connector face are
impossible, leaving the 50 parameter types that have separated-root local
witnesses.

**Not proved:** exclusion of optional coincident-root signatures within those
50 types, extension or exclusion of any of the 50 parameter types,
coefficients beyond `D`, ERTC, SBCC, RCRT, PRCC, NSSC, G18, any new order
exclusion, or global Leech-tree nonexistence.

**Verdict: PROOF + EXACT FORCED-SHARED-ROOT EXCLUSION.**
