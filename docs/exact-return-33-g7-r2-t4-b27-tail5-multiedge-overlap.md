# FW319 `b=27`: multi-edge Tail-5 L-overlap closure

The previous FW319 audit excluded a one-edge completion of the L-overlap
branch, but left open the possibility that the complementary arm used two or
more edges.  This checkpoint closes that branch against the exact fixed-L
topology.

## Exhaustive local lemma

Suppose the unique owner of `b+5=32` is L-internal, has a positive-arm LCA
split, and one arm is an existing fixed-L arm.  The six possible fixed arms
are

```text
LCA  endpoint  fixed arm  complementary arm
d6   b1         14         18
d6   z          13         19
d6   c           6         26
d6   P0         27          5
c    b1          8         24
c    z           7         25
```

The complementary arm can either start at the LCA through new vertices or
first follow a branch of the fixed L tree that is disjoint from the fixed
arm, then branch into new vertices.  Every such possibility is an ordered
positive edge sequence whose total length is the displayed complement.

The verifier enumerates all those sequences.  It rejects a sequence as soon
as one of its internal distances is already in the fixed spectrum (or is the
punctured value `4`), and then checks every pair in the induced subtree
consisting of the fixed eight vertices and the new arm.  No candidate has all
pair distances distinct while retaining exactly one owner of distance `32`.

After the necessary fixed-spectrum pruning, the only nonempty rows are:

```text
fixed arm d6--c, complement 26:  new suffixes (5,21), (21,5)
fixed arm c--b1, complement 24: new suffixes (5,19), (19,5),
                                  or fixed prefix d6--c (6) + edge 18
fixed arm c--z, complement 25:   new suffixes (5,20), (20,5),
                                  or fixed prefix d6--c (6) + edge 19
```

Each of these eight induced subtrees has a repeated pair distance.  For
example, the first row `(5,21)` repeats `11` between `(a,b1)` and
`(c,new_0)`, while the fixed-prefix row `d6--c (6)+18` repeats `31` between
`(P1,b2)` and `(new_0,z)`.  The other rows and their first collision witnesses
are emitted by the replay certificate.

Therefore the L-overlap branch is impossible under the exact FW319 fixed-L
topology, not merely for a one-edge completion.

## Why the enumeration is exhaustive

The fixed core edges are actual unsubdivided tree edges.  At the actual LCA,
the two owner arms are edge-disjoint.  If the complementary arm uses an
existing fixed vertex, its path from the LCA must lie on a branch disjoint
from the fixed arm; otherwise the actual LCA would be deeper.  Once it leaves
the fixed factor, all remaining vertices on the owner path are new and form
a positive chain.  These are exactly the prefix-plus-suffix cases enumerated
by the verifier.

Any additional side branches in a full tree cannot rescue a collision already
present in this induced subtree, since global distance injectivity restricts
every pair in the induced subtree as well.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_tail5_multiedge_overlap.py
```

The replay returns `status: VERIFIED` and zero injective `32` completions in
all six rows.

## Trust boundary

This is a local closure for the `b=27` L-internal overlap alternative.  The
ancestor--descendant rooted-difference-`32` alternatives on either the L or J
side remain open; the result does not prove global Leech-tree nonexistence.
