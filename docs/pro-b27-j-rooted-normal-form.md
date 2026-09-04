# FW319/P25: J34--37 rooted normal-form interface

## Status

This is a conditional finite-parameterization lemma for a genuine J-internal
owner path.  It is not an exhaustion result and does not imply that the
existing finite catalogue is surjective.

## Hypotheses

Assume the branch-wide J word lemma already established that an owner of
`h in {34,35,36,37}` has either a single-edge word `[h]` or one of the
two-edge words

```text
34: [16,18] or [18,16]
35: [16,19] or [19,16]
36: [16,20] or [20,16]
37: [5,32], [32,5], [16,21], [21,16], [18,19], or [19,18].
```

Let `u` be the rooted J attachment and let `d6` be the fixed reference vertex,
with `w=d(d6,u)>=38`.  Let `P_h` be the literal owner path inside J and let
`e` be the first vertex of `P_h` reached by the path from `u` (if `u` already
lies on `P_h`, take `e=u`).

## Lemma (rooted normal-form necessity)

For every such realization:

1. `e` is an actual owner-path vertex.  For a two-edge word
   `A--alpha--M--beta--C`, `e` is exactly one of `A,M,C`; for a single edge
   `A--h--C`, `e` is `A` or `C` (or `u` coincides with that endpoint).
2. Writing `rho=d(u,e)`, the rooted data satisfy

   * entry at `A`: `0 <= rho <= 300-w-h`;
   * entry at `M`: `0 <= rho <= 300-w-max(alpha,beta)`;
   * entry at `C`: the symmetric endpoint bound.

3. The rooted realization has a finite descriptor consisting of

```text
h, word, entry_type, rho,
named_alias_pattern,
rooted_stem/branch topology,
literal rooted edge list with positive weights,
rooted depth table and owner-path endpoint identities.
```

The number of vertices is at most 25, so the alias/topology choices are finite;
all edge weights on a path of total distance at most 300 are positive integers
bounded by 300.  Thus the set of descriptors is finite once the complete edge
list (including any stem subdivision and side branches) is retained.

## Proof sketch

The intersection of two simple paths in a tree is connected.  Therefore the
path from `u` to the literal owner path has a unique first intersection vertex;
an entry in the interior of an edge would mean that edge was subdivided and
the asserted literal owner word was not the actual edge word.  Hence the entry
is one of the listed path vertices.  If entry is `A`, then
`d(d6,C)=w+rho+alpha+beta=w+rho+h<=300`; the other cases use the farther owner
endpoint and give the stated bounds.  Finiteness follows from the vertex
budget, finite positive integer compositions of bounded path lengths, and the
finite alias/topology choices.

## Required independent checks for a future enumeration

An implementation must materialize and independently replay the complete
rooted edge list.  It must check: treehood; literal owner-word edge weights;
first-entry vertex; absence of hidden subdivision; all rooted depths; owner
distance; fixed-L/J translates; puncture and pair injectivity; and a canonical
rooted hash.  A row with a collision records both pairs and their common value.

## First unsupported implication

This lemma only proves finite representability of genuine rooted realizations.
It does not show that every descriptor is realizable, nor that every genuine
descriptor is already present in the current `NONE/PATH2/FORK2` or label-state
catalogues.  Stem/branch decomposition, L-side geometry, arbitrary low forests,
and complete high-incidence coverage remain `GAP`.

## Bounded topology pilot

As a protocol smoke test, the topology-level generator was run on Geo
Workstation with at most four new vertices.  It produced `17` rooted topology
classes and `1388` canonical word embeddings.  The independent verifier passed
both on Geo Workstation and in the local project environment; the artifact is
`theory-lab/topwindow/results/pro_b27_j_rooted_normal_form_topology_k4_geoworkstation.json`
with SHA-256
`c73582236c55c0a64d9e5a04c16d19b982d809b0d55daf48dee1161525758ecf`.
This is only a topology/entry encoding check.  It deliberately leaves free
stem and branch weights unassigned and therefore provides no pair-spectrum or
surjectivity conclusion.

The streaming shard pilot uses the same state semantics but a distinct ordering
contract (`rooted-code-order-word-embedding-v1`) from the original full pilot,
which sorted rows by canonical key.  Therefore the valid cross-run check is
canonical key-set equality; rolling index digests are compared only among
shards that share the streaming ordering contract.
