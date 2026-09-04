# Port-complete `H37` search contract

This document specifies the smallest finite model that could legitimately
close the `J32` branch.  It is a model contract, not a claimed theorem.

## Quantified objects

Fix the audited `b=27` exact-return branch and its 15-vertex packet `K`.  A
candidate state must quantify over:

1. a forest `F` of every low edge (weight at most 37) outside the fixed packet;
2. every connected component `C` of `F`, represented by its actual weighted
   tree `T_C`, its unique rootward port `p(C)`, carrier tag `sigma(C)`, and
   global port depth `H(C)`;
3. the high quotient connecting these components and `K`, retaining every
   endpoint incidence;
4. every maximal high-only arc, retaining its ordered edge-weight tuple rather
   than only its terminal sum; and
5. all owner assignments for `34,35,36,37` and the forced `5,21,32` owners.

The total order is 25, so the state has at most ten vertices outside `K`.
Every high arc has at most seven edges because each edge is at least 38 and
every pair distance is at most 300.

## Required constraints

The model must enforce, in one shared all-different structure:

- every pair distance in the reconstructed connected tree;
- all fixed-core and named-J translates;
- exactly one owner for each value in `H37`;
- no puncture value 4;
- distinct positive edge weights;
- the rooted `Delta(B0)` and carrier-orientation restrictions; and
- the order-25 cap (equivalently, 300 distinct distances in `1..300`).

The quotient/port representation is admissible only if reconstructing all
retained incidences gives the same weighted tree and all child-side exits are
preserved.  A terminal-metric or total-length compression is not admissible.

## Rootward-port lemma (general tree fact)

The port convention does not assume that a low component has only one
attachment.  Let `T` be any finite tree, choose a root `r` in the fixed packet
`K`, and let `C` be a connected component of the low-edge subgraph outside
`K`.  Contract `C` to one vertex (and leave every other vertex uncontracted).
Contraction of a connected subgraph of a tree is again a tree.  Hence the
quotient has a unique path from the contracted `C` vertex to `r`, and exactly
one incident edge of `C` is the first edge on that path.  This edge is
`p(C)`, the rootward port.  Every other boundary edge of `C` is oriented
childward away from `r`.

The same argument applies independently to every low component: contracting
all of them produces a tree quotient, so these rootward choices cannot form a
cycle.  After marking the quotient vertices incident to low components and all
vertices of high-subgraph degree different from two, every remaining maximal
high-only path has unmarked degree-two interior.  Such paths are edge-disjoint
and partition the high edges; retaining their ordered edge-weight tuples is
therefore lossless.  This proves the port convention and the ordered-arc
decomposition for an arbitrary supplied tree.  It does **not** prove that the
currently enumerated catalogue covers every resulting state.

## Acceptance gates

A finite run can change proof state only if:

1. the topology/port/arc generator proves coverage of every state satisfying
   the quantified objects and budget;
2. every shard is deterministically merged with exact input-row coverage;
3. no row is `UNKNOWN` or `FEASIBLE` (a survivor must include full owner and
   endpoint data); and
4. an independent implementation replays both the state reconstruction and
   the reported solver result.

The current order-seven incidence catalogue and all existing profile/Steiner
scans satisfy only fragments of these gates.  In particular, this contract
does not assert that the model has yet been enumerated or solved.

## Smallest next obligation: rooted realization of J-side words

The first uncovered quantifier is narrower than the full contract.  For each
currently admissible J-internal owner word for `h in {34,35,36,37}`, enumerate
every rooted realization of the owner path within the remaining order-25
vertex budget.  The realization must retain the actual path vertices, the root,
and any extra branch/LCA vertices; a single attachment depth or terminal sum is
not a substitute.

Each row must contain `h`, the ordered owner-path word and endpoints, the root
and attachment vertex (or explicit outside branch), all fragment edge weights,
rooted depths, internal pair distances, fixed-L/named translates, and a
canonical rooted-fragment hash.  An excluded row must also record its first
collision as two pairs and their common distance.  An independent verifier must
rebuild the fragment from the edge list and recompute these fields.

This obligation may be accepted only when an independent generator supplies an
exactly-once key set for every admissible word, no row is `UNKNOWN`, and the
replay agrees on the owner distances, injectivity, puncture, translates, and
canonical hashes.  A zero result would close only the J-side rooted-realization
quantifier.  It would not close L-side owner geometry, arbitrary low-forest or
high-incidence coverage, `Label-State Completeness`, or the global `b=27`
nonexistence claim.
