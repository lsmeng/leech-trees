# Exact-return `(3,3)` `g=7` owner lift and first-successor stop (FW300)

FW299 leaves ten canonical uncoloured forests after the forced edge sixteen.
FW300 restores exactly the part and root data visible at that moment, then
exhausts one further forced edge.  It does not continue the rapidly growing
generic forest search.

This is an **exact owner lift and a finite first-successor classification**,
not an exclusion of `g=7`.

## 1. Six rooted states and four floating states

Use the FW299 vertices

```text
A root a;       B root z with depths b_1=1,b_2=2;
C root c with c--d_6=6;       q=az=10;       r=zc=7.
```

Every edge other than `q,r` is internal to exactly one of `A,B,C`.  Therefore
the ten weight-sixteen placements have the following exact owner status.

| placement of 16 | forced part/root information |
| --- | --- |
| attach at `a` | `A` depth `16` |
| attach at `d_6` | `C` depth `22` |
| join `a` to edge 4 | edge 4 is in `A`, new depths `16,20` |
| join `d_6` to edge 4 | edge 4 is in `C`, new depths `22,26` |
| join `d_6` to edge 5 | edge 5 is in `C`, new depths `22,27` |
| attach at `b_2` | `B` depth `18` |
| attach to edge 4 | the `4--16` component is in one undetermined part |
| attach to edge 5 | the `5--16` component is in one undetermined part |
| join edges 4 and 5 | the `4--16--5` component is in one undetermined part |
| new edge 16 | its two-vertex component is in one undetermined part |

Any untouched edge-four or edge-five component is likewise assigned to one
part only after a later internal edge connects it to that part.  Calling such
a component “floating” records missing information; it does not allow an edge
to cross `q` or `r`.

For each of the six rooted rows, direct expansion of the named rooted factors
reproduces exactly the new global distances in the FW299 certificate.  All new
root depths are at least sixteen, so none changes the required coefficients
of `U*Lambda` through offset three or `Rho*W` through offset six.  Consequently
the exact-return local ledgers eliminate none of the ten states.

## 2. One exact forced edge farther

For each weight-sixteen state, insert its least missing value in every possible
way: join two displayed components, attach one unused vertex, or form a new
edge.  Quotient unused isolated-vertex labels and then quotient weighted-forest
isomorphism by the complete incident-weight profile invariant.

The exact result is

```text
ten FW299 states  -->  75 globally distinct canonical first successors,

next missing 19 : 61,      20 : 2,      21 : 8,
             22 : 3,       24 : 1.                 (FW300.1)
```

Two rows are especially rigid.  If edge sixteen joins `d_6` to edge four or
edge five, its next forced weight is eighteen and every join or singleton
attachment repeats a distance.  The sole survivor is a **new isolated edge
eighteen**.  This is an exact fresh-component obligation, but it is not yet a
contradiction: the following weight can reconnect components.

The full state-by-state counts are stored in the certificate.  They are a
complete uncoloured first-successor classification only; part and sink data
must be retained before any deeper iteration.  Cross-parent deduplication is
explicitly checked.  Equivalently, the final forced edge has a recognizable
weight, and deleting it recovers its unique canonical FW299 parent.

## 3. Nontrivial-sink support witnesses

Sink nontriviality removes none of the ten states locally.  Recall that `q,r`
are standing FW284 skeleton edges.  If both sides of one of them have diameter
strictly larger than its weight, that edge is bidirectionally supported.  A
bidirectionally supported standing skeleton edge lies in the sink core, so its
two endpoints already make the sink nontrivial.  Adding later internal edges
cannot decrease either side diameter.

Five states have this property immediately at weight sixteen:

```text
attach at a, join a to edge 4:             q is bidirectional;
attach at d_6, join d_6 to edge 4 or 5:    r is bidirectional.
```

The remaining five acquire it using exactly their already forced next edge:

| weight-16 state | next edge | supported skeleton edge |
| --- | --- | --- |
| attach to edge 4 | `a--(edge-4 endpoint)=18` | `q` |
| attach to edge 5 | `d_6--(16-leaf)=18` | `r` |
| join edges 4 and 5 | `d_6--(edge-4 endpoint)=18` | `r` |
| new edge 16 | `a--(edge-16 endpoint)=18` | `q` |
| attach at `b_2` | `d_6--(edge-4 endpoint)=20` | `r` |

Every displayed prefix is distance-injective.  Exact cut-side recomputation
gives both diameters strictly above `10` or `7`, respectively; the largest
distance in all ten witnesses is `66<153=N_18`.  These are bounded support
witnesses, not complete Leech realizations.

Two actual connected weighted trees give stronger pressure controls.  They
show directly that the owner lift plus nontrivial sink geometry still does not
close all ten rows.

The first realizes the `attach at edge 5` state and continues with edges
eighteen and nineteen:

```text
z-b_1:1, z-b_2:2, e_4-e'_4:4, e_5-e'_5:5,
c-d_6:6, z-c:7, z-a:10, e_5-x:16,
e_4-x:18, c-e'_5:19.
```

It has order eleven, all 55 pair distances distinct, exact
`(delta,eta,ell)=(3,3,0)`, and five sink vertices.  Its first missing distance
is twenty and it has outliers above its pair cap, so it is not Leech.

The second realizes `join edge 4 to edge 5`, followed by edge eighteen:

```text
z-b_1:1, z-b_2:2, e_4-e'_4:4, e_5-e'_5:5,
c-d_6:6, z-c:7, z-a:10, e_4-e_5:16, d_6-e'_4:18.
```

It has order ten, all 45 pair distances distinct, the same exact return, and
five sink vertices.  It first misses nineteen and is again non-Leech.

These controls prove only that a universal contradiction cannot follow from
the weight-sixteen owner lift and sink nontriviality alone.  They do not show
that every one of the ten states has a compatible full completion.

## 4. Strict stop and successor

> **OWNER-LIFT STOP (FW300).**  Do not infer a `g=7` contradiction from the
> six forced rooted lifts, the four floating-component alternatives, or the
> nontrivial-sink hypothesis.  Exact local ledgers remove no state, all ten
> have bidirectional sink-support witnesses, and actual connected non-Leech
> controls survive two different owner types.

The weakest live successor is the **Coloured First-Successor Merge
Obstruction**: combine the 75 first successors with their actual `A/B/C`
assignment, full-range owner coefficients and sink ports, and prove that each
is impossible or produces a strictly smaller inherited forced-forest state.
Uncoloured iteration alone is explicitly outside the claim.

## 5. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_g7_owner_lift.py
theory-lab/topwindow/results/exact_return_33_g7_owner_lift_certificate.json
```

**Proved:** the six named rooted lifts, four floating alternatives, preservation
of the exact local convolution windows, the 75-state first-successor taxonomy,
the forced new edge eighteen in two rows, and bidirectional sink-support
witnesses for all ten states (five immediate and five after one forced edge).

**Verified pressure evidence:** two connected distance-injective non-Leech
trees with the exact return and nontrivial five-vertex sinks.  The other eight
support witnesses are prefixes, not connected trees.

**Not proved:** compatibility or exclusion of every one of the ten states,
the Coloured First-Successor Merge Obstruction, exclusion of `g=7`, ERTC,
NSSC, any order exclusion, G18, or global nonexistence.

**Verdict: EXACT OWNER LIFT + FIRST-SUCCESSOR STRICT STOP.**
