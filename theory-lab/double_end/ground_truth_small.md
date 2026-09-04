# Ground truth: small Leech trees (independent brute force)

Generated `2026-09-02T15:48:05.518013+00:00` by `brute_leech_small.py`.

**Definition.** A Leech tree of order n is a tree on n vertices with positive integer edge weights whose C(n,2) pairwise path distances are exactly {1,...,C(n,2)}.

Vertices are 0-based; an edge is written `u-v (w)`.

This file is produced by an implementation written from scratch for this purpose;
it shares no code with any other search engine in this repository, so it can be
used as an independent oracle.

## 1. Counts per n

| n | N=C(n,2) | tree shapes | shapes match known | Leech trees (up to iso) | DFS nodes | time (s) | exhaustive |
|---|---|---|---|---|---|---|---|
| 2 | 1 | 1 | yes | 1 | 2 | 0.00 | yes |
| 3 | 3 | 1 | yes | 1 | 5 | 0.00 | yes |
| 4 | 6 | 2 | yes | 2 | 31 | 0.00 | yes |
| 5 | 10 | 3 | yes | 0 | 200 | 0.00 | yes |
| 6 | 15 | 6 | yes | 1 | 3048 | 0.12 | yes |
| 7 | 21 | 11 | yes | 0 | 37008 | 1.40 | yes |
| 8 | 28 | 23 | yes | 0 | 586699 | 29.35 | yes |
| 9 | 36 | 47 | yes | 0 | 8631331 | 265.71 | yes |

Search limits used: node limit / wall-clock limit per n are recorded in the JSON.
An `exhaustive = yes` row means the DFS finished the whole search space for
every tree shape on n vertices, so the count is a complete count.

**Regression fixture.** For every n marked exhaustive above, the count is a
complete count of Leech trees of order n up to isomorphism of the weighted tree:

```python
EXPECTED_LEECH_COUNTS = {2: 1, 3: 1, 4: 2, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0}
```

These agree with the literature: Leech trees exist only for n = 2, 3, 4, 6 in
this range, with two of them at n = 4, and none for n = 5, 7, 8, 9.

## 2. Claim summary over all Leech trees found

| claim | trees checked | passed | failed | non-vacuous trees | verdict |
|---|---|---|---|---|---|
| (i) E,F disjoint, size n-2, in [1,N-1] | 5 | 5 | 0 | 4 | PASS |
| (ii) e=f mod 2, e+f<=N, e!=f  (all three) | 5 | 3 | 2 | 4 | **FAIL** |
| (ii-a) e(u) = f(u) mod 2 | 5 | 3 | 2 | 4 | **FAIL** |
| (ii-b) e(u)+f(u) <= N | 5 | 5 | 0 | 4 | PASS |
| (ii-c) e(u) != f(u) | 5 | 5 | 0 | 4 | PASS |
| (iii) N-d(u,v) = min(f_u+e_v, f_v+e_u) + 2h_c, h_c>=0, forced 0, h_c<=min(h_u,h_v) | 5 | 5 | 0 | 3 | PASS |
| (iv) {0} u E u F u {N-d(u,v)} = {0..N-1} | 5 | 5 | 0 | 5 | PASS |

A tree is *vacuous* for a claim when the claim quantifies over an empty set
(n = 2 has no non-anchor vertices; n = 2, 3 have no non-anchor pairs), so the
`non-vacuous trees` column is the number of trees where the claim had content.

### 2a. What these numbers do and do not establish

Only 5 Leech trees exist in this range, so the sample is tiny. Per-claim caveats:

* **(i), (ii-b), (ii-c) and (iv) are forced by the Leech property itself**, so
  passing them is a consistency check on this enumerator rather than evidence for
  a nontrivial structural theorem. `d(a,u)` and `d(b,v)` are distances of distinct
  vertex pairs, hence distinct, which gives (i) and `e != f`; `d(a,u)+d(b,u) >=
  d(a,b) = N` gives `e+f <= N`; and (iv) is just the image of the bijection
  `{pairs} -> {1..N}` under `d |-> N-d`.
* **(ii-a) `e(u) = f(u) (mod 2)` is FALSE as stated.** Writing `h(u)` for the
  distance from `u` to the `a`-`b` path, `d(a,u)+d(b,u) = d(a,b) + 2h(u) = N + 2h(u)`,
  so `e(u)+f(u) = N - 2h(u)` identically. Hence `e(u) = f(u) (mod 2)` **iff N is
  even**. It holds for n = 4 (N = 6) and fails for n = 3 (N = 3) and n = 6 (N = 15).
  The correct universal statement is `e(u) + f(u) = N (mod 2)`. This prediction
  matched the data on every tree: True.
* **(iii) passed, but is barely exercised.** Only 8 non-anchor pairs exist across
  all Leech trees found (5 with `f_u-e_u != f_v-e_v`, 3 with them equal). Every
  observed `h_c` was 0 (observed values: [0]). So `min(f_u+e_v, f_v+e_u)` is exact
  on all available data, and the two refinements -- `h_c = 0` when the slopes
  differ, and `h_c <= min(h_u,h_v)` -- are satisfied but never discriminating:
  no pair in this data set could have distinguished them from the blanket
  statement `h_c = 0`. Treat (iii) as *not contradicted*, not as *confirmed*.

## 2b. Independent cross-check of the counts

The counts above were re-derived by `crosscheck_independent.py`, which shares
no code with `brute_leech_small.py`: it builds trees from Prufer sequences
instead of leaf addition, decides isomorphism by brute-force search over all
`n!` vertex bijections instead of AHU canonical forms, and searches weights
using only the definition.

| check | n range | counts | agrees |
|---|---|---|---|
| tree shape counts (Prufer + n! iso) | 2-9 | {2: 1, 3: 1, 4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47} | yes |
| A: full scan of the entire cube `[1..N]^(n-1)`, definition only | 2-6 | {2: 1, 3: 1, 4: 2, 5: 0, 6: 1} | yes |
| B: DFS with the distinctness prune only | 2-8 | {2: 1, 3: 1, 4: 2, 5: 0, 6: 1, 7: 0, 8: 0} | yes |

Method A scanned every one of the 4556250 weight tuples for n = 6 with no
mathematical pruning at all, and returned the same single tree.

**Caveat for n = 9.** INCONCLUSIVE -- the run spent its whole budget generating the 9-vertex shapes via Prufer sequences and timed out before the weight search did any real work.
So the n = 9 result (no Leech tree of order 9) rests on `brute_leech_small.py`
alone. Its extra prunes are provably necessary conditions -- the weight-sum
identity `sum_e a_e b_e w_e = N(N+1)/2` and the rearrangement bound derived
from it, plus distinctness of edge weights -- but they were not independently
re-implemented at n = 9. (The literature also reports no Leech tree of order 9.)

## 3. The Leech trees and their double-end data

### n = 2  (N = 1)

Edges: `0-1 (1)`

Distances sorted: `[1]`  ->  equals {1..1}: **yes**

Anchor pair (unique pair at distance N): **(0, 1)**

E = []

F = []

| claim | result |
|---|---|
| (i) disjoint / size 0 / range [1,0] | PASS |
| (ii-a) e = f (mod 2) | PASS |
| (ii-b) e+f <= N | PASS |
| (ii-c) e != f | PASS |
| (iii) cross-distance formula | PASS |
| (iv) full multiset = {0..0} | PASS |

_No non-anchor pairs: claim (iii) is vacuous for n = 2._

Multiset check (iv): `[0]` vs expected `{0..0}` -> PASS

### n = 3  (N = 3)

Edges: `0-1 (1)`, `0-2 (2)`

Distances sorted: `[1, 2, 3]`  ->  equals {1..3}: **yes**

Anchor pair (unique pair at distance N): **(1, 2)**

| u | d(a,u) | d(b,u) | e(u) | f(u) | h(u) | f-e |
|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 2 | 1 | 0 | -1 |

E = [2]

F = [1]

| claim | result |
|---|---|
| (i) disjoint / size 1 / range [1,2] | PASS |
| (ii-a) e = f (mod 2) | **FAIL** |
| (ii-b) e+f <= N | PASS |
| (ii-c) e != f | PASS |
| (iii) cross-distance formula | PASS |
| (iv) full multiset = {0..2} | PASS |

Parity failures (ii-a): `[{'u': 0, 'e': 2, 'f': 1}]`

_No non-anchor pairs: claim (iii) is vacuous for n = 3._

Multiset check (iv): `[0, 1, 2]` vs expected `{0..2}` -> PASS

### n = 4  (N = 6)

Edges: `0-1 (1)`, `0-2 (2)`, `0-3 (4)`

Distances sorted: `[1, 2, 3, 4, 5, 6]`  ->  equals {1..6}: **yes**

Anchor pair (unique pair at distance N): **(2, 3)**

| u | d(a,u) | d(b,u) | e(u) | f(u) | h(u) | f-e |
|---|---|---|---|---|---|---|
| 0 | 2 | 4 | 4 | 2 | 0 | -2 |
| 1 | 3 | 5 | 3 | 1 | 1 | -2 |

E = [3, 4]

F = [1, 2]

| claim | result |
|---|---|
| (i) disjoint / size 2 / range [1,5] | PASS |
| (ii-a) e = f (mod 2) | PASS |
| (ii-b) e+f <= N | PASS |
| (ii-c) e != f | PASS |
| (iii) cross-distance formula | PASS |
| (iv) full multiset = {0..5} | PASS |

Non-anchor pairs (claim iii):

| u | v | d(u,v) | N-d | min(f_u+e_v, f_v+e_u) | h_c | slopes differ | h_u | h_v | note |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 5 | 5 | 0 | no | 0 | 1 |  |

Multiset check (iv): `[0, 1, 2, 3, 4, 5]` vs expected `{0..5}` -> PASS

### n = 4  (N = 6)

Edges: `0-1 (3)`, `0-2 (1)`, `1-3 (2)`

Distances sorted: `[1, 2, 3, 4, 5, 6]`  ->  equals {1..6}: **yes**

Anchor pair (unique pair at distance N): **(2, 3)**

| u | d(a,u) | d(b,u) | e(u) | f(u) | h(u) | f-e |
|---|---|---|---|---|---|---|
| 0 | 1 | 5 | 5 | 1 | 0 | -4 |
| 1 | 4 | 2 | 2 | 4 | 0 | 2 |

E = [2, 5]

F = [1, 4]

| claim | result |
|---|---|
| (i) disjoint / size 2 / range [1,5] | PASS |
| (ii-a) e = f (mod 2) | PASS |
| (ii-b) e+f <= N | PASS |
| (ii-c) e != f | PASS |
| (iii) cross-distance formula | PASS |
| (iv) full multiset = {0..5} | PASS |

Non-anchor pairs (claim iii):

| u | v | d(u,v) | N-d | min(f_u+e_v, f_v+e_u) | h_c | slopes differ | h_u | h_v | note |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 3 | 3 | 3 | 0 | yes | 0 | 0 |  |

Multiset check (iv): `[0, 1, 2, 3, 4, 5]` vs expected `{0..5}` -> PASS

### n = 6  (N = 15)

Edges: `0-1 (5)`, `0-2 (1)`, `0-3 (2)`, `1-4 (4)`, `1-5 (8)`

Distances sorted: `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`  ->  equals {1..15}: **yes**

Anchor pair (unique pair at distance N): **(3, 5)**

| u | d(a,u) | d(b,u) | e(u) | f(u) | h(u) | f-e |
|---|---|---|---|---|---|---|
| 0 | 2 | 13 | 13 | 2 | 0 | -11 |
| 1 | 7 | 8 | 8 | 7 | 0 | -1 |
| 2 | 3 | 14 | 12 | 1 | 1 | -11 |
| 4 | 11 | 12 | 4 | 3 | 4 | -1 |

E = [4, 8, 12, 13]

F = [1, 2, 3, 7]

| claim | result |
|---|---|
| (i) disjoint / size 4 / range [1,14] | PASS |
| (ii-a) e = f (mod 2) | **FAIL** |
| (ii-b) e+f <= N | PASS |
| (ii-c) e != f | PASS |
| (iii) cross-distance formula | PASS |
| (iv) full multiset = {0..14} | PASS |

Parity failures (ii-a): `[{'u': 0, 'e': 13, 'f': 2}, {'u': 1, 'e': 8, 'f': 7}, {'u': 2, 'e': 12, 'f': 1}, {'u': 4, 'e': 4, 'f': 3}]`

Non-anchor pairs (claim iii):

| u | v | d(u,v) | N-d | min(f_u+e_v, f_v+e_u) | h_c | slopes differ | h_u | h_v | note |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 5 | 10 | 10 | 0 | yes | 0 | 0 |  |
| 0 | 2 | 1 | 14 | 14 | 0 | no | 0 | 1 |  |
| 0 | 4 | 9 | 6 | 6 | 0 | yes | 0 | 4 |  |
| 1 | 2 | 6 | 9 | 9 | 0 | yes | 0 | 1 |  |
| 1 | 4 | 4 | 11 | 11 | 0 | no | 0 | 4 |  |
| 2 | 4 | 10 | 5 | 5 | 0 | yes | 1 | 4 |  |

Multiset check (iv): `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]` vs expected `{0..14}` -> PASS

