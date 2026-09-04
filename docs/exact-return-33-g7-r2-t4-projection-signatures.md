# Exact-return `(3,3)` `g=7` `R2,t=4` projection signatures (FW308)

FW307 forces 55 actual internal owners into the first 82 offsets of the
`R2,t=4` final-cap row.  FW308 retains the endpoints of the uniquely forced
first seven paths from FW305 and projects them to the complete six-vertex
core.  Six of the eight possible small endpoint trims are impossible.  The
two survivors are rigid fixed-core fans and cannot coexist, so at least 13 of
the 14 first-seven endpoint incidences are heavy.

The remaining obstruction is global: later owner paths can hide in remote
full-bidirectional sink-core carriers without meeting the marked core.

## 1. Fixed-core projection stencil

Label the fixed core

```text
0=z,  1=b_1,  2=b_2,  3=c,  4=d_6,  5=a
```

with edges

```text
b_1--z:1,   z--b_2:2,   z--c:7,   c--d_6:6,   z--a:10.
```

Let `C_0` denote this subtree.  Every component of `K-E(C_0)` meets `C_0`
at a unique projection vertex; otherwise the tree would contain a cycle.
For `v` outside `C_0`, write `pi(v)` for this vertex,
`r_v=d(v,pi(v))`, and `q_v=r_v-s`.  Then for every core vertex `c_0`,

```text
d(v,c_0)=s+q_v+d_C(pi(v),c_0).                         (FW308.1)
```

An offset zero in (FW308.1) repeats the final bridge distance `s`.  A positive
offset at most 18 lies inside the certified deficit span and must be one of

```text
H_7={2,6,9,10,13,16,17}.                              (FW308.2)
```

This is the projection stencil used below.  Negative offsets remain low
internal distances and are not discarded.

## 2. Outward `b_1` annulus

If `v` lies in a component attached at `b_1`, its six core distances have
offsets

```text
q+{0,1,3,8,11,14},       q=d(b_1,v)-s.                (FW308.3)
```

Applying (FW308.2) to every positive entry at most 18, while forbidding zero,
gives the exact elementary classification

```text
q<=-15,       q=-12,       q=16,       or q>=19.       (FW308.4)
```

The exceptional values force named fans:

```text
q=-12:  d(v,d_6)=s+2, so P_2={v,d_6};
q=16:   offsets {16,17,19,24,27,30}.                  (FW308.5)
```

No claim that such an outward vertex must exist is needed in FW308.

## 3. Complete trim enumeration

Suppose an endpoint edge of `P_h` has weight `h-j` and trimming it exposes
the earlier owner `P_j`.  The edge is one of the fixed core edges from
FW305.  Orient it `o--i`, where `o` is the discarded endpoint of `P_h` and
`i` is retained by `P_j`; let `v` be the shared other endpoint.  Its core
projection lies on the `i`-side of the cut edge.  From
`d(v,i)=s+j`, every core offset is

```text
theta(c_0)=j-d_C(pi(v),i)+d_C(pi(v),c_0).              (FW308.6)
```

The verifier exhausts both orientations and every projection on the retained
side.  Requiring no zero and applying (FW308.2) leaves exactly:

| FW305 trim | result |
| --- | --- |
| `P_9 --7--> P_2` | impossible |
| `P_10 --1--> P_9` | impossible |
| `P_13 --7--> P_6` | impossible |
| `P_16 --6--> P_10` | one rigid `d_6` fan |
| `P_16 --7--> P_9` | impossible |
| `P_16 --10--> P_6` | impossible |
| `P_17 --1--> P_16` | one rigid `b_1` fan |
| `P_17 --7--> P_10` | impossible |

There is no sampling or LCA relaxation in this six-vertex enumeration.

## 4. The two rigid fans

### `D`: the `d_6` fan

The surviving weight-six trim is

```text
P_16 --(c,d_6;6)--> P_10,
pi(v_D)=d_6,       d(v_D,d_6)=s+10.                   (FW308.7)
```

Its complete fixed-core offsets are

```text
d_6:10,  c:16,  z:23,  b_1:24,  b_2:25,  a:33.       (FW308.8)
```

In particular `d(b_1,v_D)=s+24` is a root depth.  The cap gives

```text
2s+28<=N,
sigma>=ceil((P-2k+31)/2)>=60.                         (FW308.9)
```

Root-capacity counting then gives at least 60 actual owners by offset 98.

### `B`: the `b_1` fan

The surviving unit-edge trim is

```text
P_17 --(z,b_1;1)--> P_16,
pi(v_B)=b_1,       d(v_B,b_1)=s+16.                   (FW308.10)
```

Its complete offsets are

```text
b_1:16,  z:17,  b_2:19,  c:24,  a:27,  d_6:30.       (FW308.11)
```

The cap gives

```text
2s+20<=N,
sigma>=ceil((P-2k+23)/2)>=56,                         (FW308.12)
```

and at least 56 actual owners by offset 93.

### Mutual exclusion

The `D` fan owns `s+24` with `{b_1,v_D}`.  The `B` fan owns the same value
with `{c,v_B}`.  Equality of the two unique unordered owner pairs would
either identify `b_1=c`, or identify both positive-distance external fan
vertices with the opposite fixed core vertices.  Both are impossible.  Thus
the fans cannot coexist.

The first-seven path signatures are now exactly

```text
N: no small trim;
D: the single d_6 fan (FW308.7--9);
B: the single b_1 fan (FW308.10--12).                 (FW308.13)
```

At most one of the 14 endpoint incidences is small.  All 14 are heavy in
signature `N`; at least 13 are heavy in `D` or `B`.

## 5. Remote owners enter the sink core

Let `J` be a component outside `C_0`, attached through edge `f`.  If both
endpoints of some high owner path `P_h` lie in `J` and the path avoids the
core, then

```text
diam(J)>=s+h>s>w(f).                                   (FW308.14)
```

The opposite component of `K-f` contains the final bridge edge of weight
`s`, so its diameter is also greater than `w(f)`.  Therefore `f` is
full-bidirectional and belongs to the sink core.

This is the exact remaining obstruction: the projection stencil controls an
owner meeting `C_0`, but it does not prevent many owners from being carried
inside a remote thick sink-core branch.

## 6. Actual pressure controls

All controls below are independently replayed as distance-injective weighted
trees with exact `(3,3,0)` return and a nontrivial sink.  They first miss
global distance five, so none satisfies the punctured low spectrum.

The first owner `P_2` can have every unit-cut colour:

| colour | extra edges beyond the fixed core | `P_2` | max distance |
| --- | --- | --- | ---: |
| inward `ZZ` | cap/final edges from FW305, `s=21` | `{d_6,a}` | 39 |
| crossing `BZ` | `(b_1,6,19),(b_1,7,31),(7,8,4)` | `{d_6,6}` | 54 |
| outward `BB` | `(b_1,6,19),(b_1,7,28),(b_1,8,45),(8,9,4)` | `{6,7}` | 77 |

Both surviving fans are also locally realizable:

```text
D fan:
(4,6,16),(6,7,27),(1,8,33),(8,9,4),   max=94;

B fan:
(1,6,21),(6,7,28),(1,8,33),(8,9,4),   max=86.
```

Each order-ten tree has all 45 pair distances distinct and lies below the
ambient order-18 cap 153.

Finally, a star at `b_1` with leaf weights

```text
4367,5635,  5469,4537,  2190,7819,  6989,3021,
8345,1668,  3039,6977,  1976,8041
```

has paired sums `10002,10006,10009,10010,10013,10016,10017`.  Adding the
fixed core, final bridge `s=10000`, and cap edge four gives an actual
distance-injective order-22 tree with all seven `P_h`, every endpoint edge
greater than `h`, and `D intersect (D+4)=empty`.  It first misses five and
has maximum distance 18,349, far above its own Leech cap 231.  Thus endpoint
heaviness plus coherent tree geometry is not enough; the low spectrum and
global cap are genuinely load-bearing.

## 7. Rejected consultant transfer

The consultant additionally claimed that `b_1` must have an extra edge in
`K`, citing the historical all-order boundary-thin-cap theorem.  That theorem
is formulated inside a specific reflected boundary corridor with variables
`q,lambda,U,V` and earlier hypotheses (FW17), (FW19), (FW36)--(FW40).  No
map from those hypotheses to the present last-cap cut was supplied, and the
current `b_1--z` unit cut being full-bidirectional is not by itself such a
map.

FW308 therefore does **not** certify or use the extra-`b_1`-edge claim.  This
does not affect the projection stencil or trim collapse above.

## 8. Remaining three-signature lemma

> **THREE-SIGNATURE 82-WINDOW INTERSECTION LEMMA.**  No full `R2,t=4`
> punctured-tiling state with 55 actual owner paths in `[s+1,s+82]` can
> realize any of the signatures `N,D,B` in (FW308.13), including the complete
> forced fans in `D` and `B`.

A proof must show that the remaining paths cannot all hide in remote thick
sink-core carriers, or that one such carrier yields a proper inherited exact-
return descent.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_projection_signatures.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_projection_signatures_certificate.json
```

**Proved analytically:** the projection stencil, the two rigid fans and their
mutual exclusion, the 13/14 endpoint-heavy consequence, and remote-carrier
absorption into the sink core.

**Exact finite audit:** all core projections, both fan bounds, three unit-cut
colour controls, two fan controls, and the endpoint-heavy star.

**Not proved:** the historical boundary-thin theorem transfers to this cut;
the three-signature lemma; exclusion of `R2,t=4`, the two-point cap, `g=7`,
ERTC, NSSC, or global Leech-tree nonexistence.

**Verdict: THREE RIGID SIGNATURES + REMOTE-CARRIER STRICT STOP.**
