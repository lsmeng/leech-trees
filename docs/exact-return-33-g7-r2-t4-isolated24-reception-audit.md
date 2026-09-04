# Isolated-24 reception: namespace and owner/depth audit

This note records two strict non-inferences encountered while auditing an
external proposal for FW319 Isolated-24 Reception.  It is a proof-state
guardrail, not an exclusion of the `b=24` row.

## 1. The carrier weight is not the numerical seven

In FW316--FW319, `g=d_6` names the fixed-core attachment **vertex**.  The
carrier boundary is the separate edge `f=gu` of weight `w`.  For the sharp
cell,

```text
a=d(b_1,d_6)=1+7+6=14.
```

The previously proved carrier bound `a+w>=19` therefore gives

```text
w>=5.
```

Consequently no Isolated-24 reception argument may replace `w` by the
unrelated numerical parameter seven from the distinct exact-return forcing
macro.  In particular, a proposed cross decomposition `22=1+15+6` is not a
legal instantiation of this carrier cut.

## 2. A required distance is not a rooted depth

At `b=24`, the five named FW319 owners already use the five globally unique
distances

```text
24,25,26,27,28.
```

The depth `26` is forbidden in the `d_6`-rooted factor `B` because its
difference from the existing depth `23` is three, while the monotone `J`
endpoints put three in `(R-R)_+`.  These statements are different:

* global completeness has already supplied the unique owner of **distance**
  `26`, namely `(z,P_1)`;
* it gives no second owner and does not identify either endpoint as a vertex
  of `B`-rooted depth `26`.

Likewise, actual owners of the still-unassigned low distances need not be
rooted depths: FW309.19 permits an L-internal, J-internal, or cross owner,
and each case retains an LCA/other-root term.  Thus a valid reception proof
must track the named owner endpoints and their LCAs; a scalar allocation of
low values cannot force a forbidden `B` depth.

## Check

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_isolated24_reception_audit.py
```

**VERIFIED audit guardrail; Isolated-24 Reception remains open.**
