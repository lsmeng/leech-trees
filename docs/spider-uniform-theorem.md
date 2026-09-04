# Uniform nonexistence of Leech spiders

**Status: PROVED (computer-assisted), independently audited, 2026-08-20.** The
proof is internal to this repository and has two implementations of its only
infinite-parametric step.  A separate adversarial review found no missing
regime, unsound pruning rule or counterexample; it also found and prompted the
repair of an optimization-mode weakness in the verifier.  This is not an
external human referee report.

## Theorem

> **Theorem.** No spider of order `n >= 5` is a Leech tree.

A spider is a tree with at most one vertex of degree at least three; paths are
included.  Give its centre the coordinate zero.  Each leg is then a strictly
increasing sequence of positive integer marks.  Distances are centre marks,
same-leg differences, and cross-leg sums.

### Relation to the 2023 tristar theorem

Varghese, Lakshmanan Savithri and Arumugam, *Leech labeling problem on
tristar*, AIP Conference Proceedings 2649 (2023), 020007,
<https://doi.org/10.1063/5.0114834>, define a tristar `T_{m,r,l}` by attaching
leaves at each vertex of a three-vertex path.  They prove that its diameter-4
cases are non-Leech.  Their subfamily `T_{1,r,1}` is a spider with two legs of
length two and `r` unit legs, so it is a previously known special case.  The
theorem here extends from that subfamily to arbitrary numbers and lengths of
spider legs.

## 1. Normalisation and the exact top-down search

Put `N = n(n-1)/2`.  In a Leech labelling all pair distances are distinct and
are exactly `1,...,N`.  In particular all centre marks are distinct.  If `T`
and `U` are the two largest leg tips, then `T > U` and the largest distance is

```text
N = T + U.
```

The exact search starts from the two tip marks `T,U`, with realised values
`T,U,N`, and examines `N-1,N-2,...`.  If a target value is absent, every way of
realising it by the centre or by a same-leg or cross-leg pair is enumerated,
adding the one or two endpoints not already pinned.  A proposed addition is
kept exactly when all resulting distances are positive, at most `N`, and
pairwise distinct.  Thus any complete Leech spider extending a state survives
in at least one child.  This is the completeness invariant of
`spider_topdown.py` and its cap-aware equivalent `spider_window_probe.py`.

## 2. A ten-value closure for the regular region

Write `delta = T-U` and process a target `N-k`, where `k <= W`.  If

```text
U > W and delta > W,
```

then the target cannot be a centre distance or a same-leg difference, since
both would require `U <= k`.  It cannot be a sum of two lower-leg marks either,
since that would require `delta <= k`.  Therefore every realiser has one mark
on the top leg and one on a lower leg, necessarily of the form

```text
T-a and U-b, with a,b >= 0 and a+b = k.
```

Let `A` be the top-leg offsets and let `B_i` be the offsets on lower leg `i`.
Every real spider must satisfy these bounded necessary conditions:

- all high sums `a+b` are distinct;
- all same-leg offset differences are distinct;
- all sums `b+b'` from two different lower legs are distinct;
- the offsets `a`, and separately all offsets `b`, identify distinct centre
  marks.

`spider_offset_prover.py` enumerates all states satisfying these conditions.
It deliberately ignores other collision classes.  This makes it a
**relaxation**: it can admit spurious states but cannot delete a real spider
state.  With `W=10` the relaxed tree has 111 states, 110 accepted children and
57 dead states; its deepest missing offset is 10 and no state reaches offset
11.  Hence no Leech spider has `U>10` and `delta>10`.

## 3. The two boundary strips

It remains to treat `U<=10` or `delta<=10`.  For each fixed value
`s=1,...,10`, the unbounded parameter is represented symbolically:

```text
small-U:      U=s,       P=delta, T=P+s, N=P+2s;
small-delta:  delta=s,   P=U,     T=P+s, N=2P+s.
```

Every mark and distance is stored as an affine form `qP+c`.  The option list is
the same complete centre/same-leg/cross-leg list as in the exact numeric
search.

There is a small quantifier point here.  A spider at one particular value of
`P` need not belong in advance to a family of spiders varying with `P`.
Nevertheless, every branch through the high window has an affine **lift**:

- in the `small-U` strip a lower mark is bounded by `s`, while every unbounded
  top mark introduced by a target `N-k` is `P+c` with bounded `c`;
- in the `small-delta` strip, for `P>=51` and `k<=25`, each endpoint of a
  cross-leg realiser is at least `P-k` and at most `P+s`, hence is `P+c` with
  bounded `c`;
- the centre and same-leg cases, when permitted, give the same two affine
  types directly by addition or subtraction from the affine target.

Thus a numeric branch for any fixed `P>=51` maps to one of the enumerated
bounded affine branches.  All signs, cap comparisons, orders and equalities
between affine forms are checked for the entire real tail `P>=51`; the programs
abort if a comparison could change there.  The cutoff is audited rather than
guessed: attempting the common cutoff `P=50` encounters the changing equality
`25 = P-25`, while every comparison reached from `P=51` onward is stable.

`spider_affine_prover.py` closes all 20 strips inside the window `k<=25`:

| strip | regimes | states | deepest missing offset | max marks | frontier |
|---|---:|---:|---:|---:|---:|
| `U=1,...,10`, `delta>=51` | 10 | 209 | 9 | 6 | 0 |
| `delta=1,...,10`, `U>=51` | 10 | 914 | 25 | 9 | 0 |

The independent `spider_affine_cleanroom.py` imports no production-prover
code, uses immutable leg states, and recomputes every distance from scratch
after each addition.  It agrees in every regime on nodes, accepted children,
dead states, deepest offset, maximum marks, and frontier count.  This is an
independent implementation of the affine search, not an independent proof: it
shares the affine abstraction and realiser case split.  Sixty exact numeric
instances at `P=51,52,137` also agree field for field; these are regression
checks, not the justification of the infinite quantifier.

## 4. Finite base and coverage

The exact numeric search closes every order `n=5,...,15`, with zero solutions
in 16,153 states.  For `n>=16`, `N>=120`.  Any anchor not in the regular region
is in one of the following cases:

- `U<=10`.  If `delta<=50`, then `N=2U+delta<=70`, impossible; otherwise it is
  in the affine `small-U` tail.
- `delta<=10`.  If `U<=50`, then `N=2U+delta<=110`, impossible; otherwise it is
  in the affine `small-delta` tail.

These cases cover every `T>U>=1`, completing the proof.

## 5. Reproduction and trust boundary

Run the complete verifier from the repository root:

```bash
nice -n 10 python3 theory-lab/catspider/verify_spider_uniform.py
```

The expected summary is archived in
`theory-lab/catspider/results/spider_uniform_certificate.json`.  The verifier
checks the exact base-case node counts, the relaxed regular closure, both
affine implementations, and 60 affine-versus-numeric instances.  The affine
part is finite (1,123 states per implementation) and contains no timeouts,
caps, random choices or unverified solver answers.

The JSON file is an archived transcript and regression target, not a standalone
proof object: the verifier recomputes the search rather than consuming the
JSON.  The reviewed run used CPython 3.14.7.  Certificate invariants use
explicit exceptions, and the verifier rejects `python -O` and `python -OO`.
The independent report is `docs/referee-spider-uniform.md`; it records the
reviewed source revision and the adversarial test counts.

No witness is produced by this nonexistence proof, so the two-witness-checker
rule is not invoked.  If any future variant does produce a SAT witness, it must
pass both `src/checker_a.py` and `src/checker_b.py` before being reported.
