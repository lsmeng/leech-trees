# Top-window connectivity

**OBSERVED theorem.** This is a graph-theoretic corollary of the stronger
diameter-endpoint introduction lemma for every Leech tree.

## Statement

Let `T` be a Leech tree with `N` vertex pairs. For `q>=0`, define the far-pair
graph `H_q` on `V(T)` by

```text
xy is an edge of H_q  iff  d(x,y) >= N-q.
```

Then `H_q` has exactly `q+1` edges (for `q<N`), and after isolated vertices
are discarded it is connected. More strongly, list its edges by their unique
distances

```text
N, N-1, ..., N-q.
```

Every edge after the first shares an endpoint with the union of the preceding
edges. Thus the displayed order is a connected edge order rooted at the unique
diameter pair.

In particular, `H_q` uses at most `q+2` vertices. Together with far-pair
crowding, its matching number is at most `floor(sqrt(2q+1))` and it has a vertex
cover of at most twice that size.

## Proof

The Leech interval property gives exactly one pair at each distance
`N,N-1,...,N-q`, so `H_q` has `q+1` edges. Begin with the two endpoints of the
distance-`N` pair. Suppose the endpoints of all pairs with distance greater
than `v` have been selected. The diameter-endpoint introduction lemma says
more than one-vertex completion: a pair disjoint from the diameter has both
endpoints in strictly longer cross pairs, while a pair meeting the diameter
adds at most its other endpoint. Hence its edge meets the preceding edge union
and any new vertex first arrives adjacent to a diameter endpoint. Induction
down to `v=N-q` proves the connected edge order and connectivity. A connected
graph with `q+1` edges has at most `q+2` non-isolated vertices. `QED`

## Computational audit and trust boundary

`theory-lab/topwindow/verify_top_window_connectivity.py` independently computes
all distances of the five known Leech trees, first requires every witness to
pass both `src/checker_a.py` and `src/checker_b.py`, and then checks every one
of their 31 descending top-window prefixes. Run:

```text
python3 theory-lab/topwindow/verify_top_window_connectivity.py
```

The frozen summary is
`theory-lab/topwindow/results/top_window_connectivity_certificate.json`.

Connectivity supplies a canonical value descent, but not yet the required
geometric descent: an edge can attach a new vertex in a different off-diameter
component without moving into a smaller active branch. Proving that the exact
top-window sequence forces such a proper-branch move (or a thick endpoint) is
still **UNVERIFIED**.
