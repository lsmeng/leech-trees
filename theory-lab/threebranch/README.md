# Exact three-centre prototype

**OBSERVED exact exclusions at orders 18, 25 and 27; uniform exclusion
UNVERIFIED.**

`threebranch_cleanroom.py` is the first exact weighted search for the normal
form proved in `docs/threebranch-engine.md`. It keeps the three branch centres
implicit, recomputes every distance from scratch, and covers four exhaustive
types for the unique distance-`N` leaf pair:

```text
AA  two anchor tips at the same end centre
BB  two anchor tips at the middle centre
AB  one anchor tip at an end and one at the middle
AC  anchor tips at the two opposite ends
```

Reflection is removed only in the `BB` and `AC` cases where it preserves the
anchor class. Every complete state is converted to weighted edges and must
pass both `src/checker_a.py` and `src/checker_b.py` before being reported.

The validator independently checks the anchor partition and cap formula,
compares the geometric metric with a separate tree traversal, compares the
solved-partner option generator with brute one/two-mark enumeration, and
matches exact solution counts with the fixed-topology engine at orders 8 and
9:

```text
nice -n 10 python3 theory-lab/threebranch/verify_threebranch_cleanroom.py --max-order 10
```

The exact prototype has also completed all four modes at order 10. The frozen
calibration is `results/threebranch_cleanroom_certificate.json`.

`threebranch_exact.c` is the C/bitset implementation of the same search. It
keeps a paranoid full-recomputation mode and an explicit two-new-mark branch.
The verifier checks a three-child positive pair probe, exact Python invariant
agreement through order 10, paranoid/fast agreement through order 12, and the
independent fixed-topology result at order 11:

```text
nice -n 10 python3 theory-lab/threebranch/verify_threebranch_exact.py
```

**OBSERVED calibration:** exact C runs through order 15 are complete with zero
solutions. Order 15 has 225,554 valid anchors and 25,379,164 states. Across
orders 8--15 no legal search child requires two simultaneous new marks, although
the positive probe confirms that the branch is live. This is now explained by
the shape-independent **OBSERVED anchored one-vertex lemma**, proved in
`docs/anchored-one-vertex-lemma.md` and audited by
`verify_one_vertex_lemma.py`; the `--no-pairs` engine path applies it. Frozen summary:
`results/threebranch_exact_certificate.json`.

The same binary has an exact numeric top-window mode and a disjoint outer-
parameter shard partition:

```text
threebranch_exact 25 AB --no-pairs --window 25 --shard I K
```

`frontier=0` means that every numeric anchor in that shard dies while filling
the requested top window. A positive frontier is deliberately not called
UNSAT. The validator checks that three order-10 shards sum exactly to the
unsharded anchor, node, child, frontier and solution invariants.

The first order-25 `W=25` survey is only a diagnostic because it leaves
166,321,078 frontier states. The widened `W=60` campaign closes all 384
paranoid shards with 14,164,880,449 nodes, zero frontier and zero solutions.
Its resumable runner enforces bounded concurrency, rejects unfinished rows and
passes every reported witness through both checkers. The deterministic 25 KB
archive and frozen aggregate are replayed by
`verify_threebranch_n25.py`. Thus **OBSERVED computationally, no order-25
Leech tree has exactly three branch vertices**. Trees with four or more branch
vertices and the all-order theorem remain **UNVERIFIED**.

The order-27 stability campaign uses `W=70` and 128 shards per mode. All 512
paranoid shards are `DONE`: 10,055,214 anchors, 33,425,785,566 nodes, zero
frontier and zero solutions. The deepest missing offset is 52 and at most 15
non-centre marks occur. `verify_threebranch_n27.py` replays the deterministic
archive through the shared strict archive audit, which sends every reported
witness through both repository checkers. Thus **OBSERVED computationally,
no order-27 Leech tree has exactly three branch vertices**. This remains a
finite theorem, not the all-order affine lift.

The `--max-nodes` option is diagnostic. A run that reaches it reports
`status=UNKNOWN`; zero solutions in such a run is not a theorem.

## UNVERIFIED affine all-order research probe

`threebranch_parametric_probe.py` replaces the numeric diameter and the three
anchor parameters by affine integer forms and uses quantifier-free linear
integer solving to merge parameter regions. It keeps the four exact anchor
modes, the proved one-vertex rule and diameter-endpoint introduction, but
deliberately omits the finite-order remaining-vertex prune. Consequently a
surviving `FRONTIER` is only a partial top-window geometry, never a Leech-tree
witness; even a future `CLOSED` grid needs an independent checker before it is
promoted.

The fixed-order `n=10` calibration is **OBSERVED**: all four modes reproduce
the exact C engine's closing offsets and maximum non-centre mark counts. The
verifier recompiles the exact engine and checks the frozen affine rows:

```text
python3 theory-lab/threebranch/verify_threebranch_parametric_n10.py
```

`run_threebranch_parametric_grid.py` partitions each anchor parameter into
half-open rational cells. Its resume manifest binds the probe and runner
hashes, Python/Z3 versions and every search/resource setting; a mismatched
configuration is rejected rather than reusing old output. A workstation
`AB,W=8` 8-by-8 diagnostic with 32 one-core workers was deliberately stopped
after eight minutes: ten geometrically empty cells closed immediately, while
none of the first 32 feasible cells completed. This is an **UNVERIFIED
negative scalability diagnostic**, not a result about Leech trees. It shows
that the relaxation over every integer `N>=153` is too broad to justify a
larger cluster run without first adding a sound order/vertex-budget lemma.
