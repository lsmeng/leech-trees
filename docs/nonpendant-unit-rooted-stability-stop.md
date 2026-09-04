# The nonpendant-unit rooted-stability stop (FW275)

FW275 audits the first actual-LCA attack on the near-perfect
nonpendant-unit diameter conjecture left open by FW270.

* **OBSERVED exact:** a counterexample in the hard `2|b` branch must satisfy
  the rooted wrapper and hole partition in Section 2.
* **OBSERVED analytic:** scalable formal states survive the audited
  first-pivot, reflection and `2p`-chain conditions, although the displayed
  family dies at its second actual rooted pivot.
* **OBSERVED hand-checkable:** equality trees at orders nine and eleven lie
  one unit above the counterexample cap and show that local LCA laminarity
  alone permits multi-gate transfer and long-chain/whole-row telescoping.
* **UNVERIFIED:** the near-perfect conjecture, a global owner potential and
  the terminal-suffix descent in Section 8 remain open.

The resulting **OBSERVED STOP** applies only to the cap-blind first-pivot /
`2p`-chain / single-virtual-row mechanism.  It is not a counterexample to the
conjecture, does not refute a theorem that essentially uses `D<=D_0`, and is
not an all-LCA impossibility theorem, order exclusion, or G18.

## 1. Conjecture and conditional q=1 payoff

> **UNVERIFIED near-perfect conjecture.**  If `S` is a
> positive-integer-weighted, globally distance-distinct tree of order `m>=5`
> and deleting its unit edge leaves two sides of order at least two, then
>
> ```text
> diam(S)>=binom(m,2)+m-4.                          (FW275.1)
> ```

The nonpendant hypothesis is essential: the known order-six Leech tree has a
pendant unit edge.  In the q=1 application, `S=T-x`, `m=n-1`, and
`diam(T-x)=N-Q`, where `N=binom(n,2)`.  If (FW275.1) applied, then

```text
N-Q>=binom(n-1,2)+(n-1)-4=N-4,
```

so `Q<=4`.  This would still leave `Q=2,3,4` and the singleton unit-tail
branch.  FW275 does not prove (FW275.1).

## 2. Exact hard `2|b` rooted wrapper

Consider the smallest nonpendant branch

```text
c --x-- a --1-- r -- B,            x>=2,
```

where `(B,r)` has order `b`, so the whole tree has order `m=b+2`.  Put

```text
Y={d_B(r,v):v in B},     Y_+=Y-{0},
F_B={d_B(u,v):{u,v} subset B}.
```

All pairs not internal to `B` have the **OBSERVED exact** spectrum

```text
O={x} dot-union (1+Y) dot-union (x+1+Y),           (FW275.2)
|O|=2b+1,
C*=binom(b,2)+2b+1=binom(b+2,2).                  (FW275.3)
```

A counterexample to (FW275.1) has diameter at most

```text
D_0=C*+b-3=binom(b,2)+3b-2.                        (FW275.4)
```

Padding to that cap gives a hole set `H`, `|H|=b-3`, and the exact owner
partition

```text
F_B dot-union O dot-union H=I_[1,D_0].             (FW275.5)
```

The root pairs own `Y_+`.  Thus

```text
J=I_[1,D_0]-(O union H union Y_+),
|J|=binom(b-1,2),                                  (FW275.6)
```

and the nonroot pairs of `B` must own `J` bijectively through their actual
LCA distances.  This provenance is part of the hard rooted state; a set
partition of the right cardinality is only a relaxation.  Uniqueness also
forces

```text
(Y-Y) intersect {+/-1,+/-x,+/-(x+1)}=empty,
x-1,x,x+1 notin Y_+.                              (FW275.7)
```

## 3. First pivot and `2p` chains

Let `p=min Y_+`.  Its vertex is a direct child of `r`.  For each other
depth `y`, its LCA with that vertex is `r` or the depth-`p` vertex, so the
actual distance is

```text
y+p       outside the p-subtree,
y-p       inside the p-subtree.                   (FW275.8)
```

If `y,y+2p in Y`, an outside vertex at `y` cannot precede a descendant at
`y+2p`: both selected distances would be `y+p`.  Every step-`2p` depth
chain therefore has the monotone form

```text
descendant, ..., descendant, outside, ..., outside. (FW275.9)
```

But consecutive unused/selected reflections telescope:
`y+p=(y+2p)-p`.  Hence a long chain may leave only endpoint values, rather
than one hole per vertex.

## 4. Scalable first-pivot formal survivors

For every `b>=5`, set

```text
x=2,
Y={0,4} union {8+5i:0<=i<=b-3},
p=4,
P_4={12+5i:0<=i<=b-3}.                            (FW275.10)
```

Formally make the depth-four vertex a root leaf.  The wrapper, root row and
required first-pivot row are

```text
O={2} union ({1,5} union {9+5i})
      union ({3,7} union {11+5i}),
Y_+={4} union {8+5i},
P_4={12+5i}.                                      (FW275.11)
```

The tail families occupy distinct residue classes modulo five.  They obey
(FW275.7)--(FW275.9), and

```text
max P_4=5b-3<=D_0,
D_0-(5b-3)=(b^2-5b+2)/2>=1.                       (FW275.12)
```

After reserving `O,Y_+,P_4`, there are

```text
D_0-(2b+1)-(b-1)-(b-2)=b(b-3)/2                  (FW275.13)
```

free cap positions.  Choose `b-3` as `H`; the remaining positions plus
`P_4` have exactly `binom(b-1,2)` slots for `J`.  At `b=7`, for example,
`H={6,10,15,20}` works.  This is an **OBSERVED analytic formal partial
state**, not a tree.

The next pivot kills the whole family.  Since depth four is a leaf, depth
eight is a direct root child.  Its distance to depth thirteen must be

```text
13-8=5       or       13+8=21,                    (FW275.14)
```

but `5=1+4` and `21=3+18` are already wrapper owners.  Thus fixed one-pivot
audits can survive at every `b`, while actual second-pivot geometry does not.
This does not show that arbitrarily many actual pivot layers survive.

## 5. Order-nine multi-gate equality control

Take

```text
b=7, m=9, x=2, D=41,
Y=(0,4,12,20,26,31,37),
positive-depth parent indices=(0,0,2,2,3,3),
edge increments=(4,12,8,14,11,17).                (FW275.15)
```

Add `r--1--a--2--c`.  Direct path calculation gives the **OBSERVED
hand-checkable** actual-tree spectrum

```text
Spec(S_9)=I_[1,41]-{6,9,10,18,36}.                (FW275.16)
```

Its 36 distances are distinct and its five holes equal `m-4`; it is an
equality control, not a Leech/SAT witness.  Crucially, here `D_0=40`, so the
control lies one unit above the strict hard-counterexample cap.  It can
red-team consequences of local LCA geometry, but not a consequence that
essentially assumes `D<=D_0`.  For the missing middle translate `Z=2+Y_+`,
the actual owners are

| target | source depth | owner depths | LCA depth |
|---:|---:|---:|---:|
| 6 | 4 | hole | -- |
| 14 | 12 | 12,26 | 12 |
| 22 | 20 | 20,26 | 12 |
| 28 | 26 | 31,37 | 20 |
| 33 | 31 | 26,31 | 12 |
| 39 | 37 | 26,37 | 12 |

The last three owner pairs form a triangle on depths `26,31,37`, using gate
depths twenty and twelve.  Actual laminarity therefore neither makes the
owner-transfer graph acyclic nor selects a unique next row.

The depth-four root leaf selects the row `{16,24,30,35,41}`.  Its unused
reflections are `{8,16,22,27,33}`; all are internal or wrapper owners and
none is a hole.  Thus direct per-vertex reflection charging already fails in
an actual equality tree.

## 6. Order-eleven telescoping equality control

Take instead

```text
b=9, m=11, x=2, D=62,
Y=(0,4,10,18,27,35,43,51,59),
positive-depth parent indices=(0,1,1,3,3,4,4,7),
edge increments=(4,6,14,9,17,16,24,8).            (FW275.17)
```

With the same handle, direct calculation gives

```text
Spec(S_11)=I_[1,62]-{12,15,22,34,49,56,57}.       (FW275.18)
```

This **OBSERVED hand-checkable** actual tree has 55 distinct distances and
seven holes, again equality in (FW275.1), not a Leech witness.  Its
counterexample cap is `D_0=61`, so it too lies exactly one unit above the
hard state and tests only cap-blind local implications.  Here `p=4` is
ancestor of every other positive-depth vertex.  Its chains and rows are

```text
10 -> 18,                  27 -> 35 -> 43 -> 51 -> 59,
selected lower={6,14,23,31,39,47,55},
unused upper={14,22,31,39,47,55,63}.              (FW275.19)
```

Every internal upper reflection equals the next selected lower reflection;
only `22` is a hole and `63` is beyond the cap.  The virtual row is

```text
2+Y_+={6,12,20,29,37,45,53,61}.                  (FW275.20)
```

The depth-ten vertex, through LCA gate four, owns every entry except its
diagonal `12`, which is a hole.  A whole laminar row can therefore replicate
the virtual translate for one diagonal hole.

## 7. Mechanism verdict and strict-cap boundary

The two actual controls do **not** refute any implication whose hypothesis
essentially uses `D<=D_0`: each has `D=D_0+1`.  They show instead that the
following statements cannot be deduced from actual rooted LCA laminarity and
the local rows alone:

1. every unused reflection is a hole;
2. every `2p` chain produces linearly many boundary values;
3. every virtual row produces linearly many holes; or
4. owner handoff is acyclic.

Conversely, the scalable family in Section 4 obeys the strict hard-cap
arithmetic and every audited first-pivot condition, but is not a tree and
dies at its second pivot.  Together these controls expose the exact gap:
cap arithmetic at one pivot does not enforce rooted realizability, while
local rooted realizability without the one-unit strict cap does not enforce
the required extra hole.  A successful proof must couple both inputs and use
the missing top coefficient or an equivalent global terminal constraint.

For general `x`, even the virtual row is less isolated: `x+Y` can meet
`1+Y` through a depth difference `x-1`, not forbidden by (FW275.7).

Naive peeling also does not close.  Deleting a shallow root leaf removes
`b+1` scattered full-tree values, whereas

```text
D_0(b)-D_0(b-1)=b+2.                              (FW275.21)
```

No terminal suffix or inherited hard `2|(b-1)` cap follows.  If `p` is a
universal ancestor, rerooting leaves three handle offsets
`{p,p+1,p+x+1}`; in the mixed case the row splits into `y-p` and `y+p` on
different laminar regions.  Either operation regenerates a multi-handle or
two-root problem rather than (FW275.5).

This is the precise **OBSERVED STOP**: the audited cap-blind local mechanism
has no proved strictly decreasing potential on actual labelled owners.  It
says nothing against a cap-aware rooted-LCA argument; in particular it does
not rule out deriving a contradiction from the single missing top value at
`D_0+1`.

## 8. Exact reopening gate

Either of the following new **UNVERIFIED** lemmas would reopen the route.

### 8.1 Global multi-gate owner potential

Prove, using the strict cap `D<=D_0`, that following every filled
reflection/virtual-row coefficient through all later actual LCA owners
produces at least `b-2` distinct holes.  The potential must retain each
unordered owner pair and gate, charge mergers and cycles, handle the
order-nine multi-gate triangle, and explain why deleting the top coefficient
prevents the order-eleven replicated row from paying only one reusable
diagonal.  A scalar depth, first-hole position, row index, or chain count
cannot suffice.

### 8.2 Exact terminal-suffix descent

Prove that every padded hard state with `|H|=b-3` and `b` outside a fixed
finite base has a nonempty terminal rooted set `W subset B-{r}`, `|W|=s`,
with `1<=s<=b-5`, such that `B-W` is connected and

```text
I_[D_0(b-s)+1,D_0(b)]                             (FW275.22)
```

is exactly the disjoint union of all full-tree pair distances incident to
`W` and exactly `s` holes.  The removed-pair and suffix counts are

```text
K=s(2b-s+3)/2,
D_0(b)-D_0(b-s)=s(2b-s+5)/2=K+s.                 (FW275.23)
```

The lemma would preserve the hard wrapper after deleting `W` and give
`h_b=h_(b-s)+s`, hence a finite-base descent.  The count identity alone is
not enough: the order-nine shallow row is scattered across the cap.

More first-pivot inequalities, finitely many owner rows, or a larger finite
topology search does not meet either reopening gate.

## 9. Evidence and trust boundary

* (FW275.2)--(FW275.14) are **OBSERVED analytic** consequences of actual
  rooted distances or the explicitly marked formal relaxation.
* The two controls are **OBSERVED hand-checkable actual weighted trees**;
  their displayed edge data determine every path.  Both have `D=D_0+1`,
  support sharpness, and do not test any conclusion that essentially uses
  the strict counterexample cap.
* Complete nonpendant-unit checks through order twelve are only **OBSERVED
  external/non-replayed finite diagnostic** evidence inherited from FW270.
  Two order-thirteen fixed-topology attempts returned `UNKNOWN`.
* The conjecture and both reopening lemmas remain **UNVERIFIED**.

No complete deterministic all-order kernel exists for FW275, so there is no
new verifier or certificate.  The equality controls have holes and are not
SAT witnesses; the repository's two-checker witness rule is not invoked.
FW275 authorises no larger search, excludes no order, leaves nonpendant and
singleton q=1 tails open, and leaves G18 **UNVERIFIED**.

Antecedents: `docs/q1-pure-tail-stop.md`,
`docs/q1-full-spectrum-mechanism-audit.md`,
`docs/q1-two-root-closure-sprint.md`, and `variants/RESULTS.md`.
