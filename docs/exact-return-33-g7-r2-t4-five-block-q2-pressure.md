# Five-block `q+2` pressure control

FW318's sharp survivor has `g=d_6`, external `P_0`, and coreward `P_1`
through `c`.  Its first focused alternative is `b=24`, where the missing
rectangle value `q+2` can be owned by `(a,Q_1)`.  The following actual
weighted tree realizes all of that local mechanism with pair-distance
injectivity.

Use the fixed core

```text
z-b1=1, z-b2=2, z-c=7, c-d6=6, z-a=10,
```

and add

```text
d6-P0=24, c-P1=19, d6-u=44, u-j=31,
j-Q0=45, j-Q1=48.
```

At the carrier cut `d6-u`, the L depths are `24,25`, the second endpoint is
coreward through `c`, and the J LCA has depth `m=31` with arms `45,48`.
Consequently

```text
q=144,
cross corners = 144,145,147,148,
J=93, L=49,
q+2=146=d(a,Q1).
```

The FW318 five-block has its displayed unique owners:

```text
24:(d6,P0), 25:(d6,P1), 26:(z,P1),
27:(b1,P1), 28:(b2,P1).
```

All `binom(12,2)=66` pair distances are distinct.  Thus the `b=24` fixed
core/cross-rectangle/`q+2` configuration is not locally contradictory.

This is not a Leech tree: its maximum distance is `148`, exceeding the
order-12 cap `66`, and it omits many required low distances.  It establishes
only that full low coverage, the global cap, exact-return, least-remote data,
and rooted support remain load-bearing for the `b=24` route.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_five_block_q2_pressure.py
```

**VERIFIED local pressure control; no complete FW318 survivor or global
Leech-tree state is realized.**
