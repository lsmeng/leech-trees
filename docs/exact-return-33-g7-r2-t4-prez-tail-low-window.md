# FW319 pre-z tail: certified low-owner window

This is the first tail statement that converts the `b>=27` five-block
geometry into a nontrivial interval of compulsory actual owners.  It uses
the already-certified FW312/FW313 receiving-window handoff; it does **not**
infer rooted depths from arbitrary owners.

## Theorem

In the FW319 `d6/(6,6,6)/O1` pre-z cell, let the two monotone J endpoints
have `u`-depths `r,r+3`, let the carrier weight be `w`, and put

```text
t=w+r,              Q=d(P0,y0)=b+t.
```

Under the full exact-return `R2,t=4` hypotheses, with the FW312 paired
receiving state and the FW313 bounded-order handoff, the following hold.

1. `t>=24`.

2. All four monotone cross distances are strictly below the heaviest edge:

   ```text
   Q,Q+1,Q+3,Q+4 <= s-1.
   ```

3. Consequently every integer in `[b,b+t+4]` is in the punctured low
   spectrum.  Besides the eleven fixed L-side offsets and four rectangle
   offsets, the following thirteen values have unique actual owners:

   ```text
   b+c,  c in {5,7,8,9,10,11,16,17,18,19,20,21,22}.    (LW)
   ```

4. The actual `b1`-root depths of the four rectangle endpoints give the
   genuine coupling

   ```text
   b-t notin {-4,-1,0,3,4,7,10,11,14,15,18}.           (RC)
   ```

## Proof

### 1. The small `t` audit

The endpoint-rectangle theorem leaves, below 24,

```text
t in {7,16,17,18,21}.
```

The fixed core has actual spectrum

```text
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,23}.
```

The distinct actual root pairs of lengths `w`, `r` (when positive), and
`r+3` must avoid `S0`.  Exhausting `w+r=t` with `w>=5` leaves no row for
`t=7,16,17,18`, and leaves only `(w,r)=(5,16)` for `t=21`.

That remaining row is also impossible: the actual cross pair `(P1,u)` has

```text
d(P1,u)=(b+1)+w=b+6=d(c,P0).
```

The first pair crosses the carrier cut and the second lies in L, so they are
distinct pairs of the same distance.  Thus `t=21` is excluded and `t>=24`.

### 2. Why the rectangle is low

In FW316 notation, `Q=b+t` is the lower paired receiving distance.  If
`Q+4>=s`, the contrapositive of the FW312 receiving-window implication puts
the state in the FW313 bounded top-strip handoff.  FW313 then gives

```text
Q in {s-4,...,s},   s<=33.
```

But the first part and `b>=27` give `Q>=48`, a contradiction.  Hence
`Q+4<=s-1`, proving the claimed low window.

The named L offsets are

```text
EL={0,1,2,3,4,6,12,13,14,15,23},
```

and the four cross offsets are `EX(t)={t,t+1,t+3,t+4}`.  Their disjointness
is precisely the verified endpoint-rectangle collision exclusion.  Removing
`EL union EX(t)` from `{0,...,t+4}` leaves the eleven universal offsets
`{5,7,8,9,10,11,16,17,18,19,20}`.  Since now `t>=24`, the additional
offsets `{21,22}` also remain.  This proves the thirteen-owner statement
in (LW).  At the special first row `t=24`, offset `26` is also free; it is
not universal because it becomes a rectangle offset when `t=25` or `26`.

### 3. Root coupling

Root at `b1`.  The four endpoints have actual depths

```text
d(b1,P1)=b+3,  d(b1,P0)=b+14,
d(b1,y0)=t+14, d(b1,y3)=t+17.
```

They cannot coincide, and the final-cap rooted profile has no two depths
differing by four.  Comparing the four displayed values yields exactly
(RC).

## Trust boundary

The thirteen owners in (LW) are actual and unique, but their endpoints and
LCAs are not yet localized.  In particular, this theorem does not exclude
`b>=27`, the pre-z attachment cell, `R2,t=4`, or global Leech-tree
existence.  The first missing structural assertion is:

> **Tail-5 Owner Anchoring.**  The unique owner of `b+5` must meet a named
> rectangle endpoint, force a named rooted depth, or yield a proper inherited
> exact-return state.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_prez_tail_low_window.py
```

**VERIFIED low-owner window and root coupling; owner anchoring remains open.**
