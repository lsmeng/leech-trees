# Exact-return `(3,3)` `g=7` marked-core packets (FW309)

FW308 reduces the first-seven geometry to three fixed signatures.  FW309
classifies all 55 owner paths from FW307 relative to the marked six-vertex
core.  Every owner is either carried wholly inside one remote component, or
its `b_1`-rooted LCA is one of six fixed core vertices.  Consequently one
gets an exact nested two-cut carrier packet, or ten owners with one common
fixed LCA.

Neither packet is yet excluded.  This is a strict reduction, not a descent
theorem.

## 1. Remote/core-visible partition

Let `C_0` be the fixed core and let

```text
H={h_1,...,h_55} subset [1,82],
d(u_h,v_h)=s+h
```

be the first 55 actual internal owners.  Every component `J` of
`K-V(C_0)` has a unique boundary edge

```text
f_J=g_J u_J,       g_J in C_0,       w_J=w(f_J).       (FW309.1)
```

If both endpoints of `P_h` lie in the same `J`, the complete path lies in
`J`; call it remote.  Otherwise the path meets `C_0`, and its LCA rooted at
`b_1` is one of the six fixed depths

```text
0,1,3,8,11,14.                                        (FW309.2)
```

Thus the 55 owners partition exactly as

```text
55=sum_J |H_J| + sum_ell m_ell.                        (FW309.3)
```

This retains actual endpoints and actual LCAs.

## 2. Exact remote carrier identity

Fix a nonempty remote packet in `J`.  Delete `f_J=gu` and let `L` be the
component containing `C_0`.  Put

```text
w=w(f_J),       a=d_L(b_1,g),
A=R_(L,b_1),    B=R_(L,g),    R=R_(J,u).              (FW309.4)
```

The root profile and internal spectrum of `K` decompose exactly:

```text
D=A dotunion X^(a+w)R,
F_K=F_L+F_J+X^wBR.                                    (FW309.5)
```

Substitution into the final-cap identity gives six actual disjoint pair
classes:

```text
I_N = F_L + F_J + X^wBR + X^4
      + X^s(1+X^4)A + X^(s+a+w)(1+X^4)R.             (FW309.6)
```

Equivalently, at the carrier cut define

```text
Q=B+X^(a+s)(1+X^4).                                   (FW309.7)
```

Then

```text
I_N=F_J+(F_L+X^4+X^s(1+X^4)A)+X^wRQ,
(R-R) intersect (Q-Q)={0}.                            (FW309.8)
```

This is a genuine simultaneous two-cut state, not a formal factorization.

## 3. Carrier geometry and the translated pair

If `P_h` lies in `J`, then

```text
diam(J)>=s+h>s>w.                                      (FW309.9)
```

The other side of `f_J` contains the final bridge edge of weight `s`, so
both sides have diameter greater than `w`.  The carrier boundary is therefore
full-bidirectional.

At its cut put `eta=s-w`.  The final bridge is a noncarrier internal owner at
offset `eta`, while `P_h` is a carrier internal owner at offset `eta+h`:

```text
eta          : noncarrier colour,
eta+h        : carrier colour,       1<=h<=82.         (FW309.10)
```

These are named opposite-colour holes of the carrier rooted product.  They
need not be its first holes, so FW286--FW288 cannot yet be transferred.

The carrier has order `r>=3`, while the complement in the full tree contains
the six core and two cap vertices, hence `n-r>=8`.  For `n>=18`,

```text
r(n-r)>=45.                                            (FW309.11)
```

The certified excess ladder is edgewise, not restricted to the heaviest
edge.  Its product-44 threshold applies to `f_J`, forcing excess at least nine
and the first nine carrier-cut holes by

```text
10,19,22,31,34,37,40,48,51.                           (FW309.12)
```

Thus every remote packet produces another exact nine-hole rooted handoff.

## 4. Gate, radius, and carrier-size bounds

The new rooted depth `a+w` is not one of the fixed depths.  FW305's unique
support through 18 gives

```text
a+w>=19.                                               (FW309.13)
```

If `rho=max R`, a path of length `s+h` in `J` gives
`rho>=ceil((s+h)/2)`.  The final cap then gives

```text
s+23+ceil((s+h)/2)<=N,
3sigma>=P+h+50-4k.                                    (FW309.14)
```

This is exact but not uniformly stronger than FW307's `sigma>=55`.

If one carrier contains `m` of the window owners, none is an edge pair
because every edge weight is below `s`.  Hence

```text
m<=binom(r,2)-(r-1)=binom(r-1,2).                      (FW309.15)
```

A carrier holding all 55 owners therefore has order at least 12.

## 5. Core-visible packet

For a core-visible owner write its endpoint root depths as `lambda_h,mu_h`
and its fixed LCA depth as `ell_h`.  The exact LCA identity is

```text
lambda_h+mu_h=s+h+2ell_h,
ell_h in {0,1,3,8,11,14}.                             (FW309.16)
```

If there is no remote packet, 55 owners are distributed among six LCA
depths, so one depth supports at least

```text
ceil(55/6)=10                                          (FW309.17)
```

distinct equations (FW309.16).

The rigid FW308 signatures seed these packets.  Signature `B` places its six
fan offsets `16,17,19,24,27,30` at LCA depth zero.  Signature `D` places

```text
offset:     10  16  23  24  25  33
LCA depth:  14   8   1   0   1   1.                  (FW309.18)
```

## 6. Why remote is not inherited descent

Below the final bridge, the punctured interval decomposes among three actual
owner classes:

```text
[1,s-1] minus {4}
 = (Spec(L) dotunion Spec(J) dotunion (w+B+R))
   intersect [1,s-1].                                 (FW309.19)
```

Nothing here forces `Spec(J)` to contain an initial interval, makes `J`
prefix-defect-one, nests the carrier-cut holes inside `J`, or transfers the
fixed `q/r` core.  Calling `J` an inherited exact-return state would therefore
repeat the known interval-inheritance error.

## 7. Replayed pressure controls

Three actual distance-injective trees show the sharpness of the packet
reduction.  Each has exact `(3,3,0)` return, cap edge four,
`D intersect (D+4)=empty`, and a nontrivial full-window sink.  Each first
misses global distance five and violates its own Leech cap.

1. One order-23 remote carrier contains all seven endpoint-heavy paths.  Its
   boundary is attached to `a` with weight 132, `s=10000`, all 253 pair
   distances are distinct, and its maximum is 17,842.
2. An order-18 tree splits `P_2,P_9` and `P_6,P_10` between two distinct
   remote carriers.  All 153 distances are distinct and the maximum is 1,038.
3. An order-28 star supplies ten owners at offsets
   `2,6,9,10,13,16,17,19,20,21`, all with LCA `b_1`.  All 378 distances are
   distinct and the maximum is 91,581.

The verifier also reconstructs (FW309.5--8) coefficientwise on the remote
controls and confirms the translated opposite-colour offsets.  These controls
show that neither a unique sink, connectivity, nor coherent LCA geometry
closes either packet without the punctured low spectrum and global cap.

## 8. Marked-Core Packet Exclusion Lemma

> No full `R2,t=4` punctured-tiling state can realize either:
>
> 1. a remote carrier satisfying (FW309.5--15), the shared low-spectrum
>    identity (FW309.19), and the final cap; or
> 2. ten owner pairs at one fixed LCA satisfying (FW309.16), the punctured low
>    spectrum, directness, and the final cap.

By (FW309.3) and (FW309.17), this lemma excludes all three FW308 signatures.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_marked_core_packets.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_marked_core_packets_certificate.json
```

**Proved analytically:** the remote/core partition, simultaneous two-cut
identity, full-bidirectional boundary, edgewise nine-hole handoff, translated
two-colour pair, carrier bounds, and carrier-or-ten-LCA dichotomy.

**Exact finite audit:** all polynomial identities on the controls, all three
pressure trees, and the carrier arithmetic.

**Not proved:** the Marked-Core Packet Exclusion Lemma, inherited descent,
`R2,t=4`, the two-point cap, `g=7`, ERTC, NSSC, or global nonexistence.

**Verdict: REMOTE TWO-CUT OR TEN-FIXED-LCA STRICT STOP.**
