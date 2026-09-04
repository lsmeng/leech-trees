# Independent audit of the uniform no-spider theorem

**OBSERVED — verdict: SOUND (2026-08-20).** This was an internal adversarial
review by a separate AI agent with read-only instructions, not an external
human referee report.  The reviewed source revision was `968338896b0b`.

## Claim reviewed

> No spider of order `n >= 5` is a Leech tree.

The audit treated the statement as a computer-assisted theorem and checked the
normalisation, exhaustive realiser case split, regular-window relaxation,
affine quantifiers, parameter partition and executable certificate.  It found
no missing parameter regime, unsound pruning rule, symmetry loss or
counterexample.

## Load-bearing chain

1. Every spider is represented by positive cumulative marks on legs.  If `T>U`
   are the two largest leg tips, the largest distance is `T+U=N`.
2. For the greatest missing value, the exact search exhausts the cases with
   zero, one or two unpinned endpoints: centre, same-leg difference and
   cross-leg sum, including the necessary fresh-leg placements.
3. When `U>10` and `T-U>10`, the top ten missing targets can only be realised
   as `(T-a)+(U-b)` with `a+b=k`.  The offset program enforces a relaxation of
   necessary collision constraints, so closing its supertree is sound.
4. In the `small-U` and `small-delta` strips, every numeric high-window branch
   at `P>=51` has the affine encoding enumerated by the programs.  This is a
   branch-by-branch lift, not an assumption that one numeric spider belongs to
   a family.  All reached affine comparisons are stable on the full tail.
5. For `n>=16`, the inequalities `N>=120`, `2U+(T-U)<=70` and
   `2U+(T-U)<=110` partition every non-regular anchor into one of the two
   affine tails.  Exact orders `5,...,15` supply the finite base.

## Reproduction and adversarial checks

- The full verifier reproduced the archived counts: `16,153` exact base
  states, `111` regular-relaxation states, and `1,123` affine states in each of
  the two implementations, with zero solution/frontier count.
- Paranoid full-distance recomputation closed every order `5,...,15` with the
  archived node counts.  Orders `3` and `4` reproduced the known Leech
  path/star cases.
- All `2,000` boundary anchors with `P=51,...,150` agreed field-for-field
  between affine and exact numeric searches.
- All `2,500` regular anchors `11<=U,T-U<=60` closed under the exact paranoid
  search inside the ten-value window.
- No counterexample was found.

## Defect found and repaired

The original verifier used Python `assert` statements for certificate
invariants, and the primary affine prover used two load-bearing assertions.
Under `PYTHONOPTIMIZE=1`, those checks disappeared while the program could still
print `"status": "VERIFIED"`.  This did not affect the documented ordinary run
or the mathematical verdict, but it was an unsafe executable trust boundary.

The repair replaces certificate assertions with explicit exceptions in the
verifier, both affine implementations, the regular prover and the paranoid
numeric recomputation.  The top-level verifier additionally rejects `-O/-OO`.
After the repair:

```text
python3 theory-lab/catspider/verify_spider_uniform.py     -> VERIFIED
python3 -O theory-lab/catspider/verify_spider_uniform.py  -> nonzero exit
```

The repaired ordinary run used CPython 3.14.7.

## Presentation requirements

- The affine lift must be stated as an induction and must include bounded
  constant marks on the top leg in the `small-U` strip.
- The clean-room program is an independent implementation, not an independent
  proof; it shares the affine abstraction and realiser case split.
- Numeric spot checks are regression evidence, not proof of the infinite
  quantifier.
- The JSON file is an archived transcript/regression target; the verifier does
  not consume it.
- The general two-witness checker rule is irrelevant here because the theorem
  is a nonexistence certificate and produces no SAT witness.

These qualifications have been incorporated into
`docs/spider-uniform-theorem.md` and `paper/main.tex`.
