# Finite-search reduction contract

This note separates schema coverage from the computational reduction needed by
the final FW319 `b=27` nonexistence argument.  It is an unverified contract.

Let `G_res = Good_res(U_res) ∩ Phi_res`, conditional on the R2,t=4 branch-entry
lemma.  Let `K_L` be the universal literal residual low-state schema domain,
and let `E_L` be a total encoder with decoder `D_L` satisfying
`D_L(E_L(L(K))) = L(K)` for every `(K,x,s,cap4) in G_res`.

## Required reduction lemma

The search cannot use an arbitrary bounded pilot as a proof substitute.  It
must exhibit a concretely specified, computably enumerable finite set

```text
K_L_search subseteq K_L
```

such that

```text
forall (K,x,s,cap4) in G_res: E_L(L(K)) in K_L_search.
```

The same statement is required conditionally for the high stage: every genuine
completion of every retained low state must map to a generated high key in a
finite `K_H_search(l)`.

Equivalently, a compressed implementation must provide a map and realization
interface

```text
C: K_L -> K_L_search,       R: K_L_search -> low states,
forall (K,x,s,cap4) in G_res:
  exists k in K_L_search with R(k) isomorphic to L(K).
```

The map `C` may discard coordinates only when discarded subdivisions,
connectors, and incidences are uniquely recoverable or explicitly finitely
enumerated by `R`.  Recording only a terminal sum or a single attachment depth
is not lossless.

## What must be proved

1. **Total encoding.** Every legal literal low state (all edge endpoints and
   weights, components, ports, incidences, and named/shared identities) has a
   canonical key.
2. **Left inverse.** Decoding that key restores the literal state exactly,
   modulo anonymous renaming.
3. **Finite bound.** A structural theorem gives finite bounds on every key
   coordinate used by the search (not merely a timeout or a sampled range).
4. **Sound pruning.** Every filter or symmetry reduction `R` used by the
   computation satisfies `K in G_res => R(E_L(L(K)))`; no owner/incidence mode may
   be excluded only because it was absent from a pilot.
5. **Exact shard coverage.** Geo Workstation shards cover the complete reduced
   domain with deterministic semantic hashes, no unknowns, and independent
   replay of reconstruction and predicates.

The residual factor has exactly eight anonymous vertices beyond the fixed
packet.  Thus a real threshold projection has `0<=m<=8`; the current
`MAX_M=10`/all-66 code domain is an overinclusive syntactic superset, and only
the 45 pairs `0<=e<=m<=8` can represent real residual states.  This corrected
budget does not by itself prove that every low edge, port, or incidence is
represented.
In particular, assuming that all low edges lie on the fourteen H37 owner paths
would itself require a theorem.

The smallest load-bearing theorem that would supply this missing exhaustion is

```text
forall (K,x,s,cap4) in G_res, forall e in E(K) minus E(P),
  w(e) <= 37  =>  w(e) in H37 and e lies on the unique owner path P_{w(e)}.
```

Together with `|V(K)\V(P)|=8`, port-complete incidence records, and ordered
arc retention, this would give a finite literal weighted-forest domain.  The
repository currently has only the conditional version of this lemma: it
assumes complete punctured ownership, the fixed `S0` owners, the J-single-edge
`32` branch, and the literal `5/21` alternatives.  Those hypotheses have not
yet been shown to hold branch-wide for every genuine candidate, so the
finite-reduction gate remains open.

Only after branch entry and all five items are proved can a zero-survivor
result be promoted from finite evidence to a theorem about `G_res`.  A total encoder alone proves
schema-level L-surj but says nothing about the size or enumerability of
`K_L_search`.

## Current status

Items 1--2 are a design target, with bounded schema round trips only.  Items
3--5 are open.  In particular, the present `m<=3,e<=2` pilot is not a finite
search reduction theorem, and the existing high-skeleton order-10 runs do not
establish the conditional high-stage coverage.  No new computation is
authorized by this note.
