# Exact-return `(3,3)` pre-target countercontrol (FW297)

FW296 proposed that the disjoint parts `A,B,C` cannot internally cover every
distance below the target weight `g`.  FW297 gives an actual order-seventeen
countercontrol with `g=10` that covers not only `1,...,g-1` but the complete
global prefix `1,...,18`.

Thus the Pre-Target Internal-Gap Lemma is **FALSE**.  The exact-return row can
now be attacked only with genuinely full-range coverage information.

## 1. The countercontrol

Use vertices `0,...,16`, with `z=0`, source edge `q=0--3` and target edge
`r=0--8`.  The weighted edges are

```text
0--1:1,    0--2:2,
0--3:13,   3--4:27,  4--5:4,   3--6:48,  6--7:5,
0--8:10,   8--9:6,   8--10:24,
3--11:83,  11--12:7,
8--13:134, 13--14:8,
1--15:216, 15--16:9.                              (FW297.1)
```

All `binom(17,2)=136` pair distances are distinct.  The skeleton audit gives

```text
p=13, g=10, delta=eta=3, ell=0,
sink={0,1,3,8},
(|A|,|B|,|C|)=(7,5,5).                              (FW297.2)
```

The full `BC^3 AB^3 BC` owner strip and both rooted convolution ledgers are
exactly the FW291 state.  The rooted factors are

```text
U      ={0,27,31,48,53,83,90},
Lambda =Rho={0,1,2,217,226},
W      ={0,6,24,134,142}.                          (FW297.3)
```

The global spectrum contains every value `1,...,18`.  In particular,
`{1,...,g-1}={1,...,9}` is completely covered by internal pairs in `A,B,C`,
contradicting the FW296 candidate lemma.  The control is not Leech: its first
missing value is 19, and 58 distances lie above the pair cap `N=136`.

## 2. Why bounded-prefix successors are exhausted

The construction hides the small edges `4,5,7,8,9` behind large, mutually
separated stems in different parts.  Those edges supply the requested low
internal owners without altering the exact-return strip near weights
`g=10,p=13`.  The final depth-nine branch also enlarges the support sink
through `B`, so the four-vertex sink is not an artifact of only the cut roots.

Therefore all of the following can coexist:

* exact `(3,3),ell=0` return geometry;
* global distance injectivity;
* a nontrivial four-vertex full-window sink;
* complete coverage of the entire pre-target interval;
* complete coverage well beyond the target and source weights.

> **STRICT STOP (FW297).**  No argument using only a bounded low spectrum,
> even the whole pre-target interval, can exclude `(3,3)`.  A successor must
> use the full pair-cap range or a global statistic equivalent to it.

## 3. Smallest live full-range invariant

Let `I_A,I_B,I_C` be the internal distance polynomials of the three parts and
retain the FW291 rooted-depth polynomials `U,Lambda,Rho,W`.  Since `ell=0`,
`Lambda=Rho` as actual rooted `B` data.  Complete coverage is exactly the
coefficientwise identity

```text
X+X^2+...+X^N
 = I_A+I_B+I_C
 + X^p U*Lambda
 + X^g Lambda*W
 + X^(p+g) U*W.                                   (FW297.4)
```

Every coefficient on the right must be one inside `[1,N]` and zero outside.
FW291--FW296 used only bounded pieces of this identity.  The smallest live
successor is the **Full-Range Three-Part Tiling Lemma**:

> No nontrivial-sink `(3,3),ell=0` rooted state can satisfy (FW297.4) on the
> entire range `[1,N]` with no outliers.

This is **UNVERIFIED**.  Useful attacks may evaluate the full identity through
edge-cut moments, roots of unity, or a global owner involution, but another
fixed prefix extension is ruled out by (FW297.1).

## 4. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_pretarget_countercontrol.py
theory-lab/topwindow/results/exact_return_33_pretarget_countercontrol_certificate.json
```

It checks all 136 pair distances independently and replays every FW291
transition, owner, convolution, connector, partition, and sink assertion.

**Verified:** the countercontrol and falsity of the Pre-Target Internal-Gap
Lemma.

**Not proved:** the Full-Range Three-Part Tiling Lemma, exclusion of `(3,3)`,
any other FW294 row, ERTC, NSSC, G18, an order exclusion, or global
nonexistence.

**Verdict: COUNTERCONTROL + STRICT FULL-RANGE STOP.**
