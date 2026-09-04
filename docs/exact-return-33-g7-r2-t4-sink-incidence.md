# Exact-return `(3,3)` `g=7` remote sink-incidence localization (FW310)

FW309 leaves a remote carrier clause and a ten-fixed-LCA clause.  FW310
strengthens the remote clause using the all-order full-window quotient theorem
FW282.  Every remote carrier boundary belongs to the unique canonical sink,
as does the nonpendant unit edge.  Hence the sink contains the complete marked
path from `b_1` to the carrier.  Moreover, a remote owner of length `s+h`
cannot hide in one first-level thin cap: its path must meet the sink.

This is a strict localization, not a packet exclusion or an inherited descent.
In particular, meeting the sink does **not** force two distinct external sink
ports.

## 1. Full-window setting

Use the FW309 notation.  A remote owner is an actual pair

```text
P_h={u_h,v_h} subset J,       d(u_h,v_h)=s+h,       1<=h<=82,   (FW310.1)
```

where `J` is a component of `K-V(C_0)` with boundary

```text
f=gu,       g in C_0,       u in J,       w=w(f)<s.              (FW310.2)
```

FW309 proves that `f` is full-bidirectional.  Apply FW282 to the full final
tree `T`: contract every maximal component of full-bidirectional edges and
orient every remaining quotient edge toward its unique supporting side.  The
quotient has a unique sink `C`, and the away basin `B_e` of every nonroot
quotient node satisfies

```text
diam(B_e)<w(e).                                                   (FW310.3)
```

All uses of FW282 here are full-window uses.  No bounded-window orientation
or FW286--FW288 path-drop statement is transferred.

## 2. The remote carrier component is the sink

Let `C_f` be the maximal full-bidirectional component containing `f`.

Suppose `C_f` were not the quotient sink and let `e` be its outgoing boundary
edge.  The final bridge cannot be `e`: its cap side has diameter four and does
not support weight `s`, while the `K` side contains the actual pair `P_h` of
length `s+h>s`, so the bridge is oriented into `K`.

The two actual same-side witnesses at the `f` cut are:

```text
J side:             P_h, with length s+h;
opposite side:      the final bridge, with length s.              (FW310.4)
```

Because `e!=f`, the component beyond `e` toward the quotient sink lies in at
most one of the two `f` sides.  The other witness remains wholly in the away
basin of `e`.  Consequently

```text
diam(B_e)>=s>w(e),                                                   (FW310.5)
```

contradicting (FW310.3).  Therefore

```text
C_f=C.                                                              (FW310.6)
```

This argument uses both named colors from FW309.10; full bidirectionality
alone would not identify an arbitrary full component as the sink.

## 3. The unit component is the same sink

The unit edge `b_1z` is full-bidirectional.  On its `z` side, the edge
`zb_2` gives an internal distance two.  On its `b_1` side, the final bridge
and its four-edge cap give an internal distance `s+4`.

Let `C_1` be its maximal full-bidirectional component.  If `C_1` were
nonroot, its outgoing boundary could not be the final bridge, which is
oriented from its thin cap toward `K`.  The complete final cap is therefore
inside the away basin of that outgoing edge.  Since every other edge weight
is strictly below the globally heaviest weight `s`,

```text
diam(B_e)>=s+4>w(e),                                                 (FW310.7)
```

again contradicting FW282.  Hence `C_1=C`.  Combining this with (FW310.6),
the unique sink contains

```text
b_1z,       the complete C_0 path from b_1 to g,       and f=gu.    (FW310.8)
```

Every edge on that marked path is full-bidirectional.  In particular the
remote carrier is not merely attached somewhere to a thick quotient branch;
its gate is connected to the final-cap root by a named path inside the one
canonical sink.

## 4. First-level incidence localization

Delete every boundary edge of `C`.  Let `A_i` be the resulting exterior
components, attached to sink vertices `c_i` by boundary weights `g_i`.
FW282 gives

```text
diam(A_i)<g_i<=s.                                                     (FW310.9)
```

Partition the vertices into **sink-incidence atoms**:

```text
{ {c}: c in C } union { A_i }.                                      (FW310.10)
```

The endpoints of `P_h` cannot belong to one atom.  They are distinct if both
are sink vertices, and if both lay in one `A_i`, then

```text
s+h=d(u_h,v_h)<=diam(A_i)<g_i<=s,
```

which is impossible.  Therefore the endpoints occupy two distinct incidence
atoms, and their unique path meets `C`.  Since the entire path lies in `J`,
its sink connector lies in `C intersect J` and does not cross `f`.

Thus every FW309 remote packet is in fact an **anchored sink-incidence
packet**:

```text
final cap at b_1 -- marked sink path -- f -- sink-visible P_h in J. (FW310.11)
```

The exact FW309 two-cut identities, nine-hole handoff and opposite-color
offsets `eta=s-w, eta+h` remain unchanged.

## 5. What incidence localization does not imply

Two distinct incidence atoms need not use two distinct external ports.
There are three unresolved geometric forms:

1. both endpoints may be sink vertices;
2. one endpoint may be in the sink and the other in one exterior cap;
3. both may lie in distinct exterior caps, possibly attached at the same sink
   vertex.

Hence FW283's requested simultaneous two-*distinct*-port invariant is not an
automatic consequence of a remote owner.

The replay includes a new order-18 radial control.  Its fixed core and final
cap have `s=10000`; the remote carrier attaches to `a` by weight 132 and has

```text
u --6000-- x --4002-- y,
```

plus seven singleton caps at `u` of weights

```text
6038,5354,7911,7112,3414,2840,5121.
```

The unique owner of `s+2` is `{u,y}`.  Here `u` is a sink vertex and `y` lies
in the single strict thin cap behind the weight-6000 boundary.  All 153 pair
distances are distinct; the exact `(3,3,0)` return and
`D intersect (D+4)=empty` hold.  The tree first misses distance five and has
maximum distance 20,149, so it is a pressure control, not a Leech tree.

The FW309 remote-star control realizes the other failure: every first-seven
owner uses two distinct singleton caps, but both ports attach at the same
sink vertex.  The split-carrier control has both remote carrier boundaries in
the same canonical sink, while their owner packets remain in different
components of `K-V(C_0)`.

These controls rule out the shortcuts

```text
remote owner => two distinct sink vertices,
remote owner => two distinct external ports,
unique sink  => one marked-core carrier.
```

They do not test the punctured low spectrum or global cap; each fails both.

## 6. Sharpened successor and trust boundary

The remote half of FW309's Marked-Core Packet Exclusion Lemma can now be
replaced by the smaller statement:

> **Anchored Sink-Incidence Packet Exclusion Lemma.**  No full `R2,t=4`
> punctured-tiling state realizes the FW309 simultaneous carrier cut together
> with (FW310.6)--(FW310.11), the complete punctured low spectrum and the
> final no-outlier cap.

Together with the unchanged ten-fixed-LCA clause, this remains exhaustive for
the 55 owners.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_sink_incidence.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_sink_incidence_certificate.json
```

**Proved analytically:** the remote carrier component is the unique FW282
sink; the unit component is the same sink; the marked core-to-carrier path is
inside it; every remote owner crosses distinct sink-incidence atoms and meets
the sink.

**Exact finite audit:** the quotient geometry, thin first-level caps, actual
owner incidences, FW309 two-cut identities, three earlier remote controls and
the new one-port radial control.

**Not proved:** two distinct external ports, a proper inherited low interval,
the Anchored Sink-Incidence Packet Exclusion Lemma, the ten-fixed-LCA clause,
`R2,t=4`, the two-point cap, `g=7`, ERTC, NSSC, or global nonexistence.

**Verdict: REMOTE PACKET MEETS THE UNIQUE SINK; INCIDENCE EXCLUSION OPEN.**
