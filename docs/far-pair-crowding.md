# Far-pair crowding and pole cover

**OBSERVED theorem.** This is a shape-independent constraint on the top
distance window of any distinct-distance integer tree. It supplies the first
general ingredient of the Phase-III thick-tip argument, but it is not by
itself a nonexistence theorem.

## Statement

Let `T` be a positively weighted tree whose vertex-pair distances are distinct
integers, and let its maximum distance be `N`. Fix an integer `q>=0`, and call
a pair *q-far* when its distance is at least `N-q`.

1. If a matching consists of `k` q-far pairs, then

   ```text
   k^2 <= 2q+1.
   ```

2. Consequently all q-far pairs meet a set of at most

   ```text
   2 floor(sqrt(2q+1))
   ```

   vertices. We call such a set a *q-pole cover*.

For example, the top 25-wide window (`q=24`) has a pole cover of at most 14
vertices, independent of the order of the tree.

## Proof of far-pair crowding

Take two disjoint q-far pairs `(a,b)` and `(x,y)`. Their original-pair sum is

```text
d(a,b)+d(x,y) >= 2N-2q.
```

The tree four-point property says that the two largest of

```text
d(a,b)+d(x,y),
d(a,x)+d(b,y),
d(a,y)+d(b,x)
```

are equal. Therefore at least one of the two cross sums is at least
`2N-2q`. Each individual distance is at most `N`, so both summands in that
cross sum are at least `N-2q`.

Now start with a matching of `k` q-far pairs. Its `k` original pairs all have
distance in `[N-2q,N]`. For every unordered pair of matching edges, choose the
two cross pairs supplied above. These selected vertex pairs cannot repeat:
each cross pair identifies the two disjoint matching edges containing its
endpoints. Hence the construction gives

```text
k + 2 binom(k,2) = k^2
```

distinct vertex pairs, all with distinct integer distances in the interval
`[N-2q,N]`. That interval contains only `2q+1` integers. Thus
`k^2<=2q+1`.

## Proof of the pole-cover corollary

Take any maximal matching in the graph whose edges are the q-far pairs. Its
size `k` obeys the crowding bound. The `2k` endpoints cover every q-far edge:
an uncovered edge would be disjoint from the matching and could be added,
contradicting maximality. Therefore the cover has at most
`2 floor(sqrt(2q+1))` vertices. `QED`

## Computational audit and trust boundary

`theory-lab/topwindow/verify_far_pair_crowding.py` independently audits both
load-bearing steps. It checks 308,880 quartet pairings in arbitrary positive
weighted trees. It also constructs 720 deterministic random trees with
powers-of-two edge weights, which guarantees globally distinct path sums, and
checks every one of their 22,560 far-graph threshold changes using an exact
bitmask maximum-matching solver and a separate greedy maximal matching.

Run:

```text
nice -n 10 python3 theory-lab/topwindow/verify_far_pair_crowding.py
```

The frozen summary is
`theory-lab/topwindow/results/far_pair_crowding_certificate.json`.

The theorem bounds how many independent near-diameter pairs and how many
vertices are needed to meet them. It does **not** yet prove that the poles lie
near the two endpoints of one fixed diameter, nor that a pole is a branch
vertex, nor the thin-tip descent or thick-tip contradiction. Those links
remain **UNVERIFIED**.
