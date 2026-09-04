# FW319 `b=27`: J-rooted difference 32 reduces to one edge

The remaining J-internal Tail-5 alternative is an ancestor--descendant owner
of distance `32`.  The fixed L spectrum and the endpoint floor force this
path to have a very specific shape.

## Lemma

A J-internal ancestor--descendant owner of distance `32` is either a single J
edge of weight `32`, or impossible.

## Proof

Every J edge is a distinct pair from every fixed-L pair.  Therefore its weight
cannot lie in

```text
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
    27,28,29,30,31,33,39,40,41,42,50,55}.
```

The endpoint-floor lemma rules out an endpoint edge of weight at most `5` on
a multi-edge 32-owner path.  Among positive weights below `32`, the remaining
endpoint possibilities are therefore

```text
{16,18,19,20,21,24,25,26}.
```

If the path has at least two edges, its two endpoint edges already contribute
at least `16+16=32`.  Equality forces both to be `16`, but those are two
distinct J edges with the same pair distance, violating global injectivity.
Three or more edges have total length greater than `32`.  Thus no multi-edge
J path exists.  The only remaining shape is one edge of weight `32`.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_rootdiff32_shape.py
```

## Trust boundary

This does not exclude the single-edge J branch.  Its exclusion must use the
other forced low owners (`34,35,36,37`), the final no-outlier cap, or a
least-remote descent.
