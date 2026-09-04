# Complete literal low-generator specification

This is the remote implementation contract conditional on the
`Fixed-Low/H37 Edge Exhaustion` lemma.  It is not itself a search result.

## Raw state

For `0<=m<=10`, with all named vertices of the fixed packet `K` held fixed, a
raw state is

```text
(m, E_new, lambda, omega, Pi, O)
```

* `E_new` is the literal endpoint set of every new low edge;
* `lambda` assigns distinct values from
  `H37={5,16,18,19,20,21,24,25,26,34,35,36,37}` to those edges (with the
  already fixed `32` edge retained in `K`);
* `omega(h)` records the actual owner pair/path for each `h`, or `NOT_L` when
  its owner is not in the low side;
* `Pi` gives the unique rootward port vertex of each non-root low component;
* `O` gives the complete subset of outward-incidence vertices of each low
  component.

Shared owner paths are not an independent shape label.  They are recomputed
from the literal edge list and owner endpoint pairs, so the representation
includes shared `5`/`21` edges, `(5,16)` and `(16,5)`, multi-owner forks, and
arbitrary vertex sharing automatically.

## Canonicalization and raw validity

Named vertices are immutable.  Only the `m` anonymous slots may be permuted;
the canonical key is the lexicographically least serialization containing all
literal edges/weights, owner records, component partition, ports, and outward
masks.  A hash is only a digest of that serialization.

For each raw state, materialize the low forest and check:

1. acyclicity and the unchanged literal packet `K`;
2. complete component-internal pair distances, no duplicate and no puncture 4;
3. fixed `S0` values are owned only by their literal fixed pairs;
4. `32` is not newly owned on the L side;
5. each realized `H37` value has exactly one owner pair;
6. the actual `5/21` path satisfies its theorem-level alternatives; and
7. every port/outward record refers to a real vertex of its component.

These checks are low-side checks only.  Full-tree injectivity, the cap,
least-remote condition, inherited descent, and `34--37` side geometry remain
full-completion predicates.

## Deterministic shards

Use hierarchical mixed-radix ranks

```text
(m, e, rank(E_new), rank(lambda), rank(Pi), rank(O))
```

and flatten them to `[0,N_raw)`.  Shards are half-open intervals and must carry
the semantic-input hash, ordering version, global count, interval, processed
count, rolling index digest, and canonical-key/orbit counts.  The merge must
prove exact interval partition and

```text
sum_k orbit_size(k) = sum_shards accepted_raw.
```

The exhaustion lemma supplies the only low-weight coverage step.  The ten-
vertex budget and this literal representation then make the raw low domain
finite.  A completed remote run would establish low-generator coverage only
under the lemma's branch-wide hypotheses; it would not prove high-completion
surjectivity or global nonexistence.

