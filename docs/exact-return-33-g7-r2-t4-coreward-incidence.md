# FW317: coreward incidence for the monotone rectangle

FW316 leaves a branched monotone `(3,1)` rectangle at the leaf gates `a` and
`d_6`.  The two L endpoints have consecutive `g`-rooted depths.  The actual
fixed core has its own named consecutive depths, and global distance
injectivity prevents both L endpoints from lying beyond new external gate
branches.

This is an incidence reduction, not a rectangle exclusion.

## 1. Named fixed-core data

Deleting either gate from the L-side tree leaves one component containing
the rest of the fixed core.  Call it `C_core`.  The named depths are

```text
g=d_6:  d(g,z),d(g,b_1),d(g,b_2) = 13,14,15;
g=a:    d(g,z),d(g,b_1),d(g,b_2) = 10,11,12.
```

Let the two monotone-rectangle L endpoints be `P_0,P_1`, with depths
`b,b+1`.

The boundary value `b=0` is impossible: then `P_0=g` and the rooted pair
`(g,P_1)` owns distance one, repeating the fixed-core owner `(z,b_1)`.
Hence `b>0`.

## 2. Coreward incidence theorem

Suppose both endpoints lie in components of `L-g` other than `C_core`.
Choose fixed-core vertices `X_0,X_1` at consecutive depths `r,r+1`.  Every
`X_i--P_j` path passes through `g`, even when `P_0,P_1` lie in the same
external component.  Therefore

```text
d(X_0,P_1)=r+b+1=(r+1)+b=d(X_1,P_0).
```

The two unordered endpoint pairs are distinct, contradicting distance
injectivity.  Thus at least one L endpoint lies in `C_core`.

Let `kappa` be the `g`-depth of `LCA(P_0,P_1)`.  The surviving placements are
exactly:

```text
exactly one endpoint coreward  <=>  kappa=0;
both endpoints coreward        <=>  kappa>0.
```

Indeed, one coreward and one external endpoint lie in different components
after deleting `g`, while two coreward endpoints share the positive first
edge of `C_core`.

In the FW316 notation this sharpens

```text
S=w+m                 in the one-coreward case,
S=w+m+kappa>w+m       in the both-coreward case.
```

It does not by itself remove the lower, middle, or upper `D` regime.

## 3. Why the second consecutive pair does not close

If `P_c` is coreward and `P_e` external, a named fixed-core vertex `X` has
positive

```text
lambda_X=d(g,LCA(P_c,X)).
```

The collision from the both-external case becomes a strict difference of
`2lambda_X`.  Repeating the calculation with `(z,b_1)` and `(b_1,b_2)`
therefore supplies inequalities, not another forced equality.

Two abstract seven-vertex weighted trees realize the one-coreward incidence
pattern with all pair distances distinct, one for depth pattern `10,11,12`
and one for `13,14,15`.  They are mechanism controls only; they do not
contain the actual fixed core or the full carrier state.

## 4. Successor

The next exact task is **One-Coreward Fixed-Core Attachment Classification**.
For each gate and each orientation, classify

```text
(d(g,LCA(P_c,z)),
 d(g,LCA(P_c,b_1)),
 d(g,LCA(P_c,b_2)))
```

using the actual fixed-core topology, then test every named distance against
the external endpoint and the six FW316 rectangle pairs.

The rooted-depth spectrum alone cannot do this; the attachment cell inside
the fixed core is now load-bearing.

## 5. Replay and trust boundary

Run

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_coreward_incidence.py
```

The replay reconstructs the fixed core, checks both consecutive depth rows,
exhausts the symbolic both-external collision through `b=128`, and verifies
the abstract one-coreward controls.

**VERIFIED incidence reduction; no monotone rectangle, owner mode, order, or
global conjecture is excluded.**
