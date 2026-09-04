# Isolated-24 low-window pressure control

The previous isolated-24 control realizes the fixed core, the FW318 reverse
cell, the FW316 rectangle, and `q+2=(a,Q1)`, but leaves several low values
unowned.  This strengthened control fills the whole interval through 28
(apart from the designated value 4) while retaining distance injectivity.

Start with the twelve-vertex `b=24` control and add six buffered two-edge
branches:

```text
P0-H5=125,   H5-L5=5,
P0-H16=165,  H16-L16=16,
P1-H18=216,  H18-L18=18,
P0-H20=367,  H20-L20=20,
Q0-H21=429,  H21-L21=21,
Q0-H22=545,  H22-L22=22.
```

The resulting order-24 weighted tree has all `binom(24,2)=276` pair
distances distinct and contains every value in

```text
{1,...,28} minus {4}.
```

It retains the sharp FW318/FW319 mechanism:

```text
b=24;  five block 24,...,28;
q=144 and cross corners 144,145,147,148;
q+2=146 owned by (a,Q1).
```

This is not a Leech tree.  Its maximum pair distance is `1098`, whereas the
order-24 cap is `276`; it also does not check exact return, least-remote
minimality, final rooted support, or complete coverage up to its bridge.

Consequently a proof of Isolated-24 Reception must use more than the fixed
core, this rectangle, and a finite low prefix through 28.  The control makes
no claim about the full carrier directness relations after its added branches.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_isolated24_low_window_pressure.py
```

**VERIFIED finite low-window pressure control; no full-spectrum or global
Leech-tree statement is refuted.**
