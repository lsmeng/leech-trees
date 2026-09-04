# Second referee report and Fable takeover brief

- Date: 2026-09-04
- Manuscript: *There is no Leech tree on 18 vertices and no Leech spider of order at least five, with a leaf-deletion bound at order 25*
- PDF reviewed: `/Users/geoclaw/Downloads/main.pdf`
- PDF SHA-256: `6bf84c89c6d5fcbdf2032c83bd6bdfe8aecb9cba2e48b35d03b1a381f43b266a`
- Review instructions: `/Users/geoclaw/Downloads/REVIEWPROMPT.md`
- Prompt SHA-256: `50d370a27f6305a6aeadc2aa4016e18126208c200357526561590549271b05b4`
- Local repository HEAD inspected: `ffc201226e854e91b7274c9132dc36adfc6544ce`
- Public `master` inspected: `bad18900d196d8705d29c2538ea373f73d4af599`

## Scope and method

I read the 32-page PDF in full, rendered every page, and audited the numbered
statements and the claimed computation boundaries. I did not rerun any exhaustive
search. I re-derived the elementary reductions, the order-25 crowding algebra and
Table 7 arithmetic, and the diametral-endpoint case split. I also inspected the
current local source tree and the actual public GitHub branch, and checked the
two literature points below against original or first-party sources.

The findings are ordered by severity. “Blocking” means that the paper should not
be published in its present form; “major” means that the issue must be corrected
but does not presently overturn the central mathematical result.

## Findings

### 1. **BLOCKING — the data-and-code availability statement is presently false**

**Location.** Section 11, p. 30; also all computation-dependent results,
especially Theorems 1.1, 1.2, 7.1, 7.2 and 8.8.

**Problem.** The paper says that all code and data are already available at
<https://github.com/LSMENG/leech-trees> and then enumerates the current spider,
Section 7 and order-25 source/certificate archive. The live public `master` is
commit `bad18900...`, while the reviewed manuscript and current local work are at
local commit `ffc20122...` plus a large uncommitted research tree. In particular,
the public tree contains no `theory-lab/s1_crowding/` directory and no current
`verify_spider_uniform.py` or affine spider proof sources. The public PDF also has
SHA-256 `64df6a97...`, whereas the submitted PDF has SHA-256 `6bf84c89...`.

**Why it matters.** The paper's central results are computer-assisted. A referee
cannot inspect the claimed exhaustive search universe, acceptance tokens,
per-shard coverage, source hashes, or certificate collectors from the archive
that the paper identifies as the evidence. This is not merely a desirable
supplement: the paper expressly makes the archive part of the trust argument.

**Fix.** Before resubmission, deposit an immutable release containing the exact
submitted PDF/source, frozen program sources, build commands, input manifests,
raw or losslessly merged outputs, collectors, certificate JSON, and independent
checkers. Add a release tag and Zenodo DOI (or another immutable archive), state
the exact commit in Section 11, and run a clean-clone manifest/verification test.
Until this is done, replace “are available” by an accurate future-tense statement.

### 2. **MAJOR — the order-5 modular result is not new and the literature discussion is wrong**

**Location.** Abstract p. 1; Section 7.2, pp. 16–17; Table 6; reference [10].

**Problem.** The manuscript says the author could not obtain Leach and Walsh
(2011), speculates that their statement may differ or be erroneous, and presents
the two order-5 modular trees as found by the present search. The original paper
is openly available from Combinatorial Press:
<https://combinatorialpress.com/article/jcmcc/Volume%20078/vol-078-paper%202.pdf>.
Its Lemma 4.2 states that all trees on five vertices except the star are
`Z_11`-Leech trees and prints the same two topology/labeling classes. The
manuscript's two displayed labelings are unit multiples of those labelings.

Leach (2014) does indeed state that no order-5 example exists while citing the
2011 paper; that later summary is the erroneous item:
<https://onlinelibrary.wiley.com/doi/10.1155/2014/218086>.

**Why it matters.** The computation is a useful reproduction and identifies a
real error in the 2014 summary, but existence at order 5 and the two topology
classes cannot be claimed as a new discovery. The current wording misattributes
priority and speculates about a source that is directly checkable.

**Fix.** Cite and summarize Lemma 4.2 of Leach–Walsh (2011). Recast the order-5
row as a reproduction of their result and a correction of Leach's 2014 summary.
Remove the claim “we found these” and the suggestion that the 2011 paper might
have used a different definition. Keep order 9 and order 11 clearly separated as
the new computational claims.

### 3. **MAJOR — a concurrent independent order-18 proof is omitted**

**Location.** Introduction pp. 2–3, Discussion pp. 27–30, and the references.

**Problem.** The current draft describes order 18 as open up to this work, but a
public independent project by Maseeh Ghodsi now gives a separate hybrid
Lean/C++ proof with eight configurations and preserved certificates:
<https://github.com/chesshippo/LeechTrees-18>. The author's public forest-search
result appears to have been posted earlier (the 210/210-shard zero result is in
commit `656148f...`):
<https://github.com/LSMENG/leech-trees/commit/656148f9657a>.
Thus this is not necessarily a priority loss, but it is now relevant concurrent
work and cannot be omitted from a manuscript dated after both releases.

**Why it matters.** The independent proof materially changes the literature
context and provides an unusually valuable comparison of trusted bases:
forced-forest canonical generation here versus a Lean-reduced eight-case search
there. It is also the strongest genuinely independent external check of the
central conclusion.

**Fix.** Cite the concurrent project (or its archival paper/release when
available), give the public chronology without priority rhetoric, and compare
the two proof boundaries and search universes. Do not imply that either program
is a rerun of the other.

### 4. **MAJOR — Section 9 contradicts Section 8.4 about the `delta=284` rerun**

**Location.** Section 8.4, pp. 25–26 and Table 10 rows 15–16, versus Section 9,
p. 29.

**Problem.** Section 8.4 says that `delta=284` was rerun from frozen source
`abstract_class_search_d83323870704.cpp`, that all 448 `(split,shape)` records
match exactly, and that the certificate is row 15 of Table 10. Section 9 still
says the chain was run only once and that `delta=284` rests on an earlier
revision. These cannot both describe the present evidence. The adjacent phrase
“improvement of the constant 281 to 284” is also numerically misleading: the
computer search excludes `281,282,283,284`, so the resulting lower bound is
`285` (or equivalently the exclusion is “through 284”).

**Why it matters.** This is the evidence-status paragraph a referee will use to
decide how much independent reproduction exists. The stale version understates
the actual rerun while making the manuscript internally inconsistent.

**Fix.** Rewrite the Section 9 paragraph from the final Section 8.4/Table 10
record: frozen-source rerun completed, 448/448 keys matched, zero survivors,
with the remaining limitation being that the two depth implementations share
the depth-free abstraction. Say “raises the lower bound from 281 to 285” or
“excludes the four values through 284.”

### 5. **MAJOR — the small witness proving `M(13) <= 105` is not supplied**

**Location.** Theorem 7.1 and its proof, pp. 15–16.

**Problem.** The existence bound is justified by “appending one leaf to the
`n=12` witness with `D=79`,” but that `D=79` witness and the new edge are not
printed. The public `variants/RESULTS.md` likewise records only
“`... 4-12:62` appended to the D=79 tree.” This is not a complete checkable
witness.

**Why it matters.** Unlike the large UNSAT searches, an existence upper bound
has a tiny certificate. There is no reason to make the reader recover it from
unreleased history or trust a checker summary.

**Fix.** Print the full 12-edge labeled tree (or put it in a stable
machine-readable file named in the theorem), list its 78 distinct distances or
give the exact verifier command, and include the witness and output hashes.

### 6. **MINOR — the displayed draft date is stale**

**Location.** Title page, p. 1.

**Problem.** The PDF says “Draft of 2 September 2026,” but the reviewed file was
generated on 4 September and contains the later frozen-source `delta=284` rerun.

**Fix.** Update the date/version identifier and make it agree with the archived
release.

## Checks on which I found no mathematical defect

- Lemmas 2.1–2.4 and the exact-once canonical augmentation in Proposition 3.3
  are quantifier-correct as written. In particular, distinct edge weights make
  every non-single-edge component pointwise fixed, while endpoint swaps of
  isolated weighted edges give exactly the stated residual automorphisms.
- Theorem 6.2's division into the regular region and the two boundary strips is
  logically exhaustive in the prose. Its finite implementation remains part of
  Finding 1 until the claimed exact sources and verifier are publicly deposited.
- The crowding calculation in Theorem 8.6 is correct. Substituting `r=k-m`
  gives
  `5m^2-(4k+11)m+6k+6 <= 0`; at `k=24` this is
  `5m^2-107m+150 <= 0`, whose roots are approximately `1.508` and `19.892`.
  Hence integer `m>=2` implies `m<=19`. Every entry of Table 7 agrees with
  `binom(m,2)` and `(r+1)(2m-3)`.
- Theorem 8.5's endpoint case split covers distinct first branches, a common
  first branch with a nontrivial common prefix, and the degenerate prefix cases.
  I found no omitted configuration in the deduction of the `299`/`<=298`
  deletion diameters.
- The order-25 claims are honest about their limits. The paper expressly leaves
  `delta in [285,298]` open, treats the incomplete `delta=285` run only as partial
  evidence, and does not turn the normal-form reduction into a nonexistence
  theorem.
- The 32 rendered pages show no clipping, overlap, unreadable tables, or broken
  cross-reference visible at page scale.

## Verdict

**Is Theorem 1.1 established?** Yes, at the level normally meant by a
computer-assisted combinatorics theorem, conditional on faithful execution of
the archived program. The mathematical coverage argument and acceptance
criterion match the claimed finite universe, and I found no unsound quantifier
or canonical-generation step. The present submission still cannot be accepted
until the exact archive in Finding 1 is actually available.

**Is the order-25 material honest?** Yes. It proves a hand-derived lower bound,
adds four explicitly finite computer exclusions, and leaves fourteen normal-form
values open. I found no slide from partial search to global nonexistence.

**Recommendation.** Accept only after major revision. The central theorem does
not presently require rejection, but the false availability statement is a
publication blocker; the order-5 priority error, concurrent proof, stale
`delta=284` status, and missing `M(13)` witness must also be corrected.

## Fable takeover: highest-value next work

First, independently challenge the five substantive findings above. A useful
response is not agreement but either a source-backed correction or a precise
replacement paragraph. Do not rerun the long searches for this review.

After the paper is repaired, look for a shorter route to the still-open
order-25 range. The best target is not another full `delta=285` campaign. Try the
following in order:

1. **Joint Hall crowding, not single-class capacity.** For each low-LCA class,
   derive its actual interval of attainable high-high distances as a function of
   the low depth and component masses. Apply Hall to unions of several classes.
   The goal is a sound subset inequality stronger than
   `binom(m,2) <= (r+1)(2m-3)`. Either prove one that eliminates a new `delta`,
   or return the smallest explicit normal-form counterexample showing why this
   route cannot improve the bound.
2. **Endpoint-deficit additive structure.** Starting from
   `d(u,v)=N-f(u)-e(v)-2h_c`, isolate a set of pairs for which `h_c` is fixed or
   controlled. Determine whether distance injectivity forces a Sidon-type or
   additive-energy bound on the endpoint deficit sets. Again, a failed attempt
   should end in a minimal counterexample, not a vague statement that the
   variables are dependent.
3. **Parity coupled to crowding.** The high block has a fixed number of odd and
   even targets. Refine the class capacities by parity of the two depths and the
   low LCA. Test whether the parity-resolved Hall inequalities exclude any case
   with `r>=9` before depth search.
4. **Independent normal-form audit.** Re-derive both directions of Corollary 8.9
   without looking at the production enumerator, then compare the derived fields
   to the frozen source. The first deliverable should be a field-by-field
   coverage table, not new computation.

For every proposed new lemma, return: exact hypotheses and quantifiers, a proof
of necessity, the first `delta/r/m` it improves, and either a small independent
positive control or a minimal counterexample. Keep `PROVED`, `FINITE VERIFIED`,
`OBSERVED`, `CANDIDATE`, and `OPEN` separate.
