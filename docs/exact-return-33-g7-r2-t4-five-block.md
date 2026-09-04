# FW319: the pre-z five-block window

FW318 leaves a sharp reverse-orientation cell at `g=d_6`: `P_0` is external,
`P_1` is coreward in the `c`-side cell before `z`, and five named pairs own
the consecutive values `b,...,b+4`.  The fixed-core spectrum and carrier
directness reduce its rooted depth to one isolated value plus a tail.

This is a parameter-window theorem, not a cell exclusion.

## 1. Named block and the fixed-core coincidence

The owners are

```text
b       (d_6,P_0)
b+1     (d_6,P_1)
b+2     (z,P_1)
b+3     (b_1,P_1)
b+4     (b_2,P_1).
```

Since exactly one endpoint is coreward, their LCA is `d_6` and

```text
d(P_0,P_1)=2b+1.
```

The only fixed-core vertex in the pre-z cell is `c`.  If `P_1=c`, then
`b+1=6`, so `b=5`; the L pair has distance eleven and repeats the fixed-core
pair `(b_1,a)`.  Thus `b=5` is impossible.

Otherwise all five block owners are new pairs.  Their values must avoid the
fixed-core spectrum

```text
{1,2,3,6,7,8,9,10,11,12,13,14,15,17,23}.
```

The only five-term gap below 23 is `18,...,22`, so this first gives

```text
b=18 or b>=24.
```

## 2. Carrier difference three

The monotone J endpoints have rooted-depth difference three.  Carrier
directness requires this value to be absent from `(B-B)_+`.  The fixed
`d_6`-root depths are

```text
{0,6,13,14,15,23},
```

and the rectangle adds `b,b+1`.  Among `b=18` or `b>=24`, a rooted difference
three occurs exactly at

```text
b=18: 18-15=3;
b=25: 26-23=3;
b=26: 26-23=3.
```

Therefore the exact surviving window is

```text
b=24 or b>=27.
```

This does not assert that any survivor extends to a full carrier.

## 3. Successor

The smallest live row is `b=24`.  It names the block `24,...,28` and the L
pair distance 49.  The next task is **Isolated-24 Reception**: determine
whether complete low ownership forces an additional `B` depth at 21, 22, or
26 (or another depth differing by three from 24 or 25), contradicting the J
difference-three row.

If `b=24` is excluded, the entire pre-z reverse cell jumps to `b>=27`.

## 4. Replay and trust boundary

Run

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_five_block.py
```

The replay checks every `b<=512`, the endpoint-coincidence row, the fixed
spectrum, and the rooted difference-three filter.  It does not produce a
rooted-reception theorem, a carrier, or a Leech tree.

**VERIFIED parameter window `b=24` or `b>=27`; no full cell, owner mode,
order, or global conjecture is excluded.**
