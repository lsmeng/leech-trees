# Exact search for Leech trees of hop-diameter at most four

**OBSERVED computer-assisted result — updated 2026-08-22.**  The recovered and audited
forced-forest engine finds exactly the five known Leech trees at orders 2--18
and no others.  Together with Taylor's **LITERATURE** restriction on possible
orders, these are the only hop-diameter-at-most-four Leech trees through order
25: a separate 512-shard order-25 sweep is complete and has zero solutions.

## 1. Forced-forest base

Let `N=binom(n,2)`.  In a Leech tree with edge weights
`w_1<...<w_(n-1)`, the forcing lemma says that `w_k` is the least value not
realised in the forest of the preceding edges.  The base engine therefore adds
the forced edge in all three possible ways: join two current components,
attach a new vertex to one component, or start a new isolated edge.

Every new cross-component distance is computed and must be a previously unused
member of `1,...,N`.  A child has a unique parent obtained by deleting its
largest-weight edge.  Since all edge weights are distinct, the only
automorphism of a reachable weighted forest is the endpoint swap of an
isolated one-edge component; using one distinguished endpoint removes exactly
that duplication.  These arguments and the underlying engine were already
audited in `docs/referee-forest.md`.

## 2. Exact diameter-four subforest invariant

Call a component *big* when its hop-diameter is at least three.

> **OBSERVED lemma D4-1.**  A forest is a subforest of some tree of
> hop-diameter at most four if and only if every component has hop-diameter at
> most four and at most one component is big.

Necessity of the first condition is immediate.  If two components each have
diameter at least three, every attachment vertex has eccentricity at least two;
joining the components in a tree creates a path of at least `2+1+2=5` edges.
Conversely, every non-big component is a star.  If a big component exists,
choose one of its radius-at-most-two centres and join every other star at its
centre.  If none exists, choose a star centre (or a new centre when vertices
remain) and join all other star centres to it.  The resulting diameter is at
most four.

The engine maintains all hop distances, rejects a component of diameter above
four, and rejects the creation of a second big component.  Thus its shape
restriction is exact rather than a heuristic prune.

## 3. Containment caps

Deleting a final edge gives sides of sizes `s` and `n-s`.  All
`s(n-s)` cross-cut distances contain that edge and are distinct integers in
`[w,N]`.  Hence

```text
w <= N+1-s(n-s) <= N-n+2.                         (D4-2)
```

The second inequality uses `s(n-s)>=n-1`.  It applies to every future edge.
When a partial edge joins components of current sizes `a,b`, its final side
size lies in `[a,n-b]`.  Since `s(n-s)` is concave, its minimum on that interval
is attained at an endpoint.  The stronger necessary cap is therefore

```text
w <= N+1-min(a(n-a), b(n-b)).                     (D4-3)
```

Both caps only reject an edge that cannot have enough available containing
distances in any completion.

## 4. Monotone endgame feasibility

This is the strongest new prune and the main audit target.  Let `t` be the
current forced value.

If a big component exists, the centre `c` of any diameter-four completion lies
inside it and currently has hop-eccentricity at most two.  Every other current
component is a star and must ultimately join its centre `s_i` directly to `c`
by an edge of some unused weight `x_i>=t`.  For each candidate `c`, the engine
constructs a domain of `x_i` values for which every distance between the two
current components is new and in the target set.

The cut side of the future edge contains at least the current star size
`sigma`.  All vertices in other current components remain on the centre side;
if their total is `M`, the branch side is at most `n-M`.  Concavity gives the
safe domain cap

```text
x_i <= N+1-min(sigma(n-sigma), M(n-M)).            (D4-4)
```

This is the corrected cap.  An exploratory draft used only the first endpoint;
that version was rejected and never promoted.  The final order-2--18 ladder
was rerun after the correction; its counts were unchanged.

For several stars, the centre-to-centre distances `x_i+x_j` must also be
unused, in range and mutually distinct.  A small CSP checks only these
necessary conditions.  It deliberately omits future vertices and many
cross-star distances, so satisfiability does not certify a completion.  Its
only rejecting outcome is exhaustive domain failure.  A 20,000-node CSP cap
returns *alive* on exhaustion, never dead.

If no big component exists yet, at most one current star can later contain the
eventual centre/big component.  Every other star needs a nonempty direct-join
domain of the form above.  Consequently two empty weak domains are impossible.
Again, allowing one exception is a relaxation.

All sets of realised distances only grow and the forced edge weights only
increase.  Testing a proposed future join against today's sets is therefore
monotone: a collision or range failure cannot be repaired later.

## 5. Reproduction and independent checks

The deterministic C++ node counts for orders 2 through 18 are

```text
2, 3, 6, 11, 47, 178, 497, 1289, 3311, 8778, 24264,
70639, 216040, 690247, 2282083, 7767003, 27157047.
```

The solution counts are `1,1,2,0,1` and then zero.  Every positive output
passes both independent repository checkers.  A separately written Python
engine uses immutable dictionaries, explicit component lists and an independent
cross-assembly bound.  It reproduces the same solution counts through order 13
in 996,551 states, although its state counts differ.

Forty planted distinct-distance targets of diameter at most four are all found.
Fifteen diameter-five targets act as diagnostics.  The structural window
identities are also checked on the known trees and 300 random distinct-distance
diameter-four trees.

Finally, compiling with `D4_NO_ENDGAME` disables the whole Section 4 prune.
Order 17 then takes 47,986,068 rather than 7,767,003 states and still has zero
solutions.  This does not prove the prune, but it is a strong regression and
direction-of-relaxation check.

One-command verification and the frozen transcript are in
`theory-lab/diameter4/`.  The verifier refuses optimized Python, rebuilds the
C++ source, freezes both ladders, and validates all positive witnesses.

## 6. Sharded order-25 acceptance rule

At one fixed depth, the engine numbers subtrees in deterministic traversal
order and sends number `j` to shard `j mod K`.  The pre-shard prefix is repeated
in every process, but every deeper subtree belongs to exactly one shard.
Therefore solution counts partition exactly even though summed node counts
include repeated prefixes.

An order-25 verdict requires all 512 keys `(i,512,8)`, each with status `DONE`.
`UNKNOWN`, a missing file or a wrong key makes the aggregate unknown.  Any SAT
line must be present and pass both checkers.  These conditions are enforced by
`verify_diameter4_shards.py`.  The aggregate additionally freezes hashes of
the audited C++ source, both repository checkers, the optional exact campaign
executable and every complete shard stdout, together with the reported
CPU/node totals.

The acceptance rule is now satisfied.  All 512 keys are `DONE`; the aggregate
has `nsol=0`, 322,189,234,739 reported nodes including repeated pre-shard
prefixes, and 3,403,240.387 reported CPU-seconds.  Its frozen certificate is
`theory-lab/diameter4/results/diameter4_n25_shards_certificate.json`; the
adjacent `n25_k512/` archive contains every shard stdout/stderr and the exact
Linux campaign executable.  The aggregate verifier matches the frozen JSON
exactly and freezes the full-stdout, source, executable, and both checker
hashes.  Hence nonexistence at order 25 within hop-diameter at most four is an
**OBSERVED finite computational theorem**.  It says nothing about arbitrary
order-25 trees or about orders above 25.
