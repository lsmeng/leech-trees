# Exact-return `(3,3)` `g=7` coloured freeze and adversarial chain (FW301)

FW300 leaves 75 globally distinct first successors of the ten forced
weight-sixteen forests.  FW301 restores every part colour that is already
meaningful, proves that later connectors cannot change the low owner ledger,
and isolates a smallest connected adversarial survivor.  The result is a
strict stop, not an exclusion of `g=7`.

## 1. The exact necessary coloured state

Delete the two cross edges

```text
q=az=10,       r=zc=7.
```

The remaining internal forest has three distinguished rooted components,
containing `a`, `z`, and `c`; label them `A`, `B`, and `C`.  Every other
component is rootless at the current threshold.  A full completion assigns
each such component to exactly one of `A,B,C`, and its first connection to the
corresponding root component occurs through a later internal edge.

Thus a successor with `k` rootless components has `3^k` necessary colourings.
The components remain distinguishable by their incident edge-weight profiles,
so there is no additional permutation quotient.  This construction is
complete in the necessary direction: every full exact-return completion
induces one of these colourings.  It does not assert that every colouring
extends.

The exact count is

```text
75 uncoloured first successors  -->  829 necessary coloured states.   (FW301.1)
```

The complete parent-wise compression is:

| weight-16 parent | uncoloured children | children by rootless count `k` | coloured states | coloured states by next missing |
| --- | ---: | --- | ---: | --- |
| attach at `a` | 4 | `k=1:1, k=2:2, k=3:1` | 48 | `19:48` |
| attach at `d_6` | 3 | `k=2:2, k=3:1` | 45 | `19:45` |
| attach at `E_4` | 17 | `k=1:9, k=2:7, k=3:1` | 117 | `19:105, 22:12` |
| attach at `E_5` | 13 | `k=1:6, k=2:6, k=3:1` | 99 | `19:90, 22:9` |
| join `a` to `E_4` | 3 | `k=1:2, k=2:1` | 15 | `19:15` |
| join `d_6` to `E_4` | 1 | `k=2:1` | 9 | `19:9` |
| join `d_6` to `E_5` | 1 | `k=2:1` | 9 | `19:9` |
| join `E_4` to `E_5` | 6 | `k=0:1, k=1:4, k=2:1` | 22 | `19:22` |
| new edge 16 | 20 | `k=2:11, k=3:8, k=4:1` | 396 | `19:324, 20:36, 21:36` |
| attach at `b_2` | 7 | `k=1:2, k=2:4, k=3:1` | 69 | `21:60, 24:9` |

Consequently

```text
next missing 19 : 667,     20 : 36,     21 : 96,
             22 : 21,      24 : 9.                         (FW301.2)
```

## 2. Frozen low owners

Let `m` be the least missing distance of one of the 75 successors.  Any
rootless component needs a future internal connector.  The forcing lemma puts
every future edge at weight at least `m`; hence every rooted depth newly
created by that connector is at least `m`.  No future connection can change an
owner coefficient below `m`.

Therefore the actual pairs already present give the final owner-class ledger
on `1,...,m-1`.  Write `I` for an internal owner.  All 829 colourings collapse
to only five frozen signatures, one for each possible `m`:

```text
1..6       : I
7..9       : BC
10..12     : AB
13..15     : BC
16         : I
17         : AC
18..m-1    : I, except that m=24 has owner AC at 23.        (FW301.3)
```

The multiplicity of each signature is exactly the corresponding row of
(FW301.2).  In particular, colour labels add no new low-coefficient
contradiction.  Any successful successor theorem must use coefficients at or
above `m`, where the future root connector becomes visible.

## 3. A connected adversarial survivor

The strongest small obstruction is already connected.  Starting from the
FW299 base, take

```text
E_4--E_5:16,       d_6--(other E_4 endpoint):18.
```

In verifier labels its edges are

```text
(0,1,1), (0,2,2), (6,7,4), (8,9,5), (3,4,6),
(0,3,7), (0,5,10), (6,8,16), (4,7,18).
```

This is an actual connected distance-injective tree of order ten.  It has

```text
(|A|,|B|,|C|)=(1,3,6),
W={0,6,24,28,44,49},
five sink vertices,
first missing distance 19.
```

It has the exact `(3,3),ell=0` return and a nontrivial sink, but it is not
Leech.

Exhausting the forced edge 19 gives one survivor only:

```text
a new isolated edge 19.                                  (FW301.4)
```

The next missing value is then 26.  Exhausting edge 26 again gives one
survivor only:

```text
a new isolated edge 26.                                  (FW301.5)
```

The next edge is 27.  Exactly two canonical placements survive: attach 27 to
an endpoint of edge 19, or form a new isolated edge 27.  Both have next missing
value 29.  Thus even a connected owner-aware pressure tree can force two new
components without contradiction.

## 4. Strict stop and Pro successor

> **COLOURED-FREEZE STOP (FW301).**  Part colouring, the exact owner ledger
> below the next missing value, and nontrivial-sink compatibility do not close
> the `g=7` branch.  The 75 successors induce 829 necessary colourings but only
> five frozen low-owner signatures, and the connected adversarial survivor
> forces isolated edges 19 and 26 before branching at 27.

The weakest live successor is a **First Root-Activation Packing Lemma**
(equivalently, the connector-crossing owner-overlap lemma).
It must use coefficients at or above the current missing value and prove that
the future connector of a floating component either collides with an existing
`AB/BC/AC` owner or yields a strictly smaller inherited exact-return state.
Any valid lemma must in particular defeat the explicit `19,26,27` adversarial
chain above.

## 5. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_g7_coloured_freeze.py
theory-lab/topwindow/results/exact_return_33_g7_coloured_freeze_certificate.json
```

**Proved:** the complete necessary 829-colouring count, its parent-wise and
next-missing distributions, the five frozen low-owner signatures, and the
forced `19,26` new-edge chain with two weight-27 successors.

**Verified pressure evidence:** the order-ten connected adversarial tree is
distance-injective, has the exact return and a nontrivial five-vertex sink.

**Not proved:** extension of any colouring to a complete Leech tree,
exclusion of `g=7`, any order exclusion, G18, NSSC, ERTC, or global
nonexistence.

**Verdict: EXACT COLOURED FREEZE + ADVERSARIAL-CHAIN STRICT STOP.**
