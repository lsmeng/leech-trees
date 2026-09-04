# Isolated-24 combined root-consistent local control

The two previously separate checks for the sharp `b=24` FW319 cell can be
realized simultaneously on the `b1` side.  This is a negative control for a
tempting argument: the five-block data plus the forced final-root depths 27
and 38 do **not** already contradict the frozen `R2,t=4` rooted support.

Use the fixed core and the two named FW318 attachments

```text
z-b1=1, z-b2=2, z-c=7, z-a=10, c-d6=6,
d6-P0=24, c-P1=19.
```

Rooting at `b1` gives precisely

```text
D={0,1,3,8,11,14,27,38}.
```

In particular the named endpoints have the required depths

```text
d(b1,P1)=27,    d(b1,P0)=38,
```

and `D` has no two elements differing by four.  All 28 pair distances of the
eight-vertex tree are distinct; its spectrum is

```text
{1,2,3,6,7,8,9,10,11,12,13,14,15,17,19,23,
 24,25,26,27,28,30,36,37,38,39,47,49}.
```

It contains no pair at distance four and retains the exact FW318 block

```text
24:(d6,P0), 25:(d6,P1), 26:(z,P1),
27:(b1,P1), 28:(b2,P1).
```

Thus the base support among the eight states in the isolated-24 rooted-support
continuation is not merely an abstract oracle survivor: it has the same local
topology as the sharp five-block cell.

This is **not** a `K` factor satisfying the full exact-return identity, and
not a Leech tree.  It misses required low distances, including 5 and 16, and
does not impose the complete two-point convolution, cap, final bridge, or
least-remote conditions.  Consequently a valid exclusion of `b=24` must use
one of those genuinely global obligations; it cannot use only the fixed core,
the five block, depths 27/38, and the root-depth separation-four rule.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_isolated24_combined_root_control.py
```

**VERIFIED combined local control; no full continuation or nonexistence claim.**
