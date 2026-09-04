# Terminal AB-to-BC local transport theorem (FW288)

FW287 classifies every terminal `AB -> BC` switch at a path drop into a
shared-endpoint state or one of the three disjoint modes `R,D,U`.  FW288
retains the right datum in each mode.  The result is an exhaustive local
transport record for one path drop.

This is a **PROVED all-order local theorem** under the FW286/FW287 hypotheses.
It does not prove that records from different skeleton arcs compose.

## 1. Setup

Use

```text
A -- q -- B -- r -- C,
X=d(a,b)=p+eta-1,          Y=d(b',c)=p+eta,
x=t_(b')-t_b,              y=h_(b')-h_b.
```

The crossed pairs satisfy

```text
X'=d(a,b')=X+x+y,          Y'=d(b,c)=Y+x-y.       (FW288.1)
```

FW287 excludes cone `L`.  It remains to interpret `D,R,U` and the direct
shared-endpoint case.

## 2. D: canonical earlier-AB bridge

In `D`, `x+y<=-1` and `x-y>=1`.  The pair `(a,b')` is `AB`, so it crosses
`q` and has distance at least `p`.  Equation (FW288.1) also gives

```text
X'<=p+eta-2.
```

Therefore

```text
X'=p+j,              j=eta-1+x+y in [0,eta-2].    (FW288.2)
```

FW286 says the unique owner of every such offset is `AB`; hence that earlier
owner is exactly `(a,b')`.  The retained endpoint chain is

```text
(a,b) --a-- (a,b') --b'-- (b',c).                 (FW288.3)
```

If `j=0`, the middle owner is the edge `q` itself.  If `eta=1`, the interval
`[0,eta-2]` is empty, so mode `D` cannot occur.

## 3. U: canonical sub-p BC bridge

In `U`, `x+y>=2` and `x-y<=-2`.  The pair `(b,c)` is `BC`, hence same-side
at the `q` cut, and

```text
Y'<=p+eta-2.
```

If `Y'>=p`, it would occupy an offset `0<=j<=eta-2`.  FW286 gives the unique
owner there as `AB`—including `j=0`, whose owner is `q`.  The distinct `BC`
pair would repeat that distance.  Thus

```text
Y'=d(b,c)<=p-1,            x-y<=-eta-1.             (FW288.4)
```

The retained endpoint chain is

```text
(a,b) --b-- (b,c) --c-- (b',c),                    (FW288.5)
```

with an actual named bridge below the source weight.  This includes
`eta=1`; known `L6` realizes `p=8`, `Y'=5`.

## 4. R: canonical oriented connector interval

In `R`, `x+y>=2` and `x-y>=1`.  Hence `2x>=3`, so integrality gives

```text
t_(b')>=t_b+2.                                      (FW288.6)
```

Retain the actual marked interval

```text
J_R=[pi(b),pi(b')]
```

on the named connector, oriented from the `q` root toward the `r` root.  Its
length is `x>=2`.  This is stronger than retaining only the scalar `x`: the
endpoints, projections, connector and orientation are part of the record.

Mode `R` is impossible when `ell=0`; `b'` cannot project to the `q` root and
`b` cannot project to the `r` root.  Other connector-root endpoint cases do
not alter (FW288.6).

## 5. Exact exhaustive output

Every path-drop terminal switch has exactly one record:

```text
S: b=b'                         direct shared endpoint;
D: (a,b)->(a,b')->(b',c)        earlier AB owner, j<=eta-2;
R: pi(b)<pi(b')                 oriented interval |J_R|>=2;
U: (a,b)->(b,c)->(b',c)         named BC bridge d(b,c)<p.
```

Together with FW287's cone-`L` exclusion, this proves the single-path-drop
local TABC obligation, provided `D/U` retain their named intermediate pair
and `R` retains its oriented marked interval.

The remaining path-drop problem is no longer local existence of a transport
record.  It is the following separate theorem.

> **UNVERIFIED Path-Record Composition Compatibility (PRCC).**  Show how an
> `S/D/R/U` output at `q -> r` is read by the next FW284 arc from `r`, so that
> shared endpoints or marked connector intervals concatenate without losing
> orientation or escaping to an unrelated coefficient.

Cap lifts still require the independent **UNVERIFIED Cap-to-Boundary Owner
Transport** theorem.  Both PRCC and cap transport are needed before a
cycle-wide NSSC argument.

## 6. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_terminal_local_transport.py
theory-lab/topwindow/results/terminal_local_transport_certificate.json
```

It reconstructs all frozen FW287 controls and checks the four retained record
types, including the `D` earlier offset, `R` interval orientation and length,
and the strengthened `U` sub-`p` bound.

**Proved:** the exhaustive `S/D/R/U` local transport theorem for one FW284
path drop.

**Not proved:** PRCC, cap-to-boundary transport, compatibility around a cycle,
NSSC, nontrivial-sink exclusion, G18, any new order exclusion, or global
Leech-tree nonexistence.

**Verdict: PROOF (local).**

## 7. FW289 cap-lift boundary

FW289 treats the independent cap-lift layer.  An incoming cap endpoint below
the target first offset has a canonical shared prefix owner; equality with the
first offset is impossible; failure forces both endpoints beyond that prefix.
The remote pair and target inward owner give an exact four-cross-pair
rectangle and a conditional Leech bound, but an actual non-Leech control
survives with all four cross distances inside the pair cap.  Thus bounded
target-prefix cap transport is strictly stopped; the live cap successor is
Remote Cap Rectangle Transport.  See `docs/cap-endpoint-depth-stop.md`.

FW290 supplies the first compatibility fact at the target of a path drop.
The target first offset is at most the old edge's returned offset.  Equality
forces the exact edge-lift return and a two-cycle; strict inequality gives a
next owner below the dropped source weight.  A cap lift can erase that scalar
decrease, so exact-return exclusion and strict-branch cap compatibility remain
unverified.  See `docs/pathdrop-target-owner-fork.md`.

FW291 gives the exact equality-branch strip `BC^delta AB^eta BC` and strictly
stops its bounded two-root continuation.  Full ERTC must combine nontrivial
connector geometry with coefficients outside that strip.  See
`docs/exact-return-switchback-stop.md`.
