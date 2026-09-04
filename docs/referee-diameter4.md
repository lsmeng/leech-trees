# Adversarial review of the hop-diameter-four engine

**OBSERVED referee verdict — SOUND for the stated completed orders, updated
2026-08-22.**  I found no unsound shape restriction, cap, endgame prune,
sharding rule or lost positive witness in the final recovered source.  The
order-25 acceptance conditions have now been met by a complete frozen shard
aggregate.

## Scope and provenance

The final scratch source was recovered with MD5
`5a292292d2b43668dd4218675d8e75f4` and SHA-256
`60be619bb2e0c122057ed8c21091c9df7b11de501057a292d2795eee221fa97b`.
The repository version removes two unused draft helpers and adds a compile-time
ablation switch; neither lies on the normal search path.  The recovered
order-2--18 ladder was reproduced from source on both macOS/clang and
Linux/GCC.

## Findings

1. **Forced-forest completeness: verified.**  The three edge placements are
   exhaustive, every child has its maximum-edge parent, and the only surviving
   automorphism is the already-audited isolated-edge endpoint swap.

2. **Shape invariant: verified.**  Two separate diameter-at-least-three
   components would force a five-edge path.  All remaining components are
   stars and can be joined at a radius-two centre, proving the converse used by
   the engine.

3. **Universal and partial cut caps: verified.**  They follow from counting
   distinct cut-crossing distances and minimising the concave function
   `s(n-s)` at the two possible side-size endpoints.

4. **Endgame feasibility: verified as a relaxation.**  With a big component,
   the final centre is one of its current eccentricity-at-most-two vertices and
   every other current star joins that centre directly.  The per-star domains
   contain every genuine future join.  The CSP checks only necessary centre
   distances and returns alive when its budget is exhausted.  Without a big
   component, allowing one weak-domain failure accounts for the single current
   component that may contain the eventual centre; two failures are impossible.

5. **Draft-cap defect: fixed before promotion.**  The exploratory `weakFeas`
   bound initially treated the current star size as the only possible cut
   endpoint.  The final source takes the minimum over both endpoints
   `sigma` and `n-M`.  All certificate runs use the corrected source.  Counts
   happened to be unchanged, showing the defective branch did not fire in the
   completed small-order ladder, but that fact is not used as a proof of the
   correction.

6. **Positive and differential checks: passed.**  The five known witnesses
   pass both checkers.  Forty arbitrary-target positive plants are all found.
   The independent Python engine agrees on solution counts through order 13.
   Disabling the complete endgame block preserves zero solutions at order 17
   while increasing the search to exactly 47,986,068 states.

7. **Sharding: verified.**  The depth-`L` counter assigns each deeper subtree
   to exactly one residue class.  Small positive sharding at order 6 preserves
   its unique witness, which passes both checkers; a seven-way order-13 run
   preserves its zero solution count.  Node sums deliberately repeat the
   common prefix and are labelled accordingly.

## Verdict boundary

The engine soundly proves the reported diameter-four exclusions at every
completed order.  It is not a certificate for arbitrary diameter.  At order
25, all 512 records are `DONE`, their aggregate has zero solutions, and the
frozen certificate records the per-shard and full-stdout digests, audited
source/checker hashes, and exact campaign-executable hash.  A seven-shard
positive smoke run separately confirms that the same witness path sends every
SAT output through both repository checkers.  Thus the order-25 restricted
exclusion is **OBSERVED**; arbitrary-diameter order 25 remains **UNVERIFIED**.
