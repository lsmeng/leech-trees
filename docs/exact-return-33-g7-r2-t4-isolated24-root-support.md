# Isolated-24 rooted-support continuation

The sharp FW319 cell with `b=24` imposes two additional depths on the rooted
support at the final bridge root `b1`:

```text
d(b1,P1)=d(b1,c)+d(c,P1)=8+19=27,
d(b1,P0)=d(b1,d6)+d(d6,P0)=14+24=38.
```

Together with the frozen `R2,t=4` depths, every candidate support therefore
contains

```text
D0 union {27,38},       D0={0,1,3,8,11,14}.
```

The exact rooted-support oracle enforces all of the following through depth
38:

- the fixed R2 parent relations;
- pair-distance injectivity of the realized rooted tree;
- no rooted distance four;
- the two-point coefficient condition
  `1_D(j)+1_D(j-4)<=1` at every processed offset.

There are exactly eight surviving partial supports:

```text
{0,1,3,8,11,14,19,27,38}
{0,1,3,8,11,14,21,27,38}
{0,1,3,8,11,14,22,27,38}
{0,1,3,8,11,14,27,29,38}
{0,1,3,8,11,14,27,30,38}
{0,1,3,8,11,14,27,32,38}
{0,1,3,8,11,14,27,33,38}
{0,1,3,8,11,14,27,38}.
```

Thus the local rooted-support conditions neither force 21/22/26 nor give an
immediate contradiction from 27 and 38.  This is a finite continuation only:
it does not assert that any listed support extends past 38, satisfies the full
low spectrum, cap, exact return, or owner-incidence constraints.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_isolated24_root_support.py
```

**VERIFIED eight-state rooted-support continuation; no full `b=24` state is
constructed or excluded.**
