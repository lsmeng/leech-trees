# Exact-return `(3,3)` nontrivial-sink stop (FW295)

FW294 leaves one type with both first holes at least three:

```text
(delta,eta)=(3,3),   ell=0.
```

FW295 supplies actual distance-injective trees with this exact-return state
and a nontrivial full-window sink.  They are deliberately not Leech.  Thus
complete global coverage—not merely sink nontriviality—is indispensable for
any exclusion of this row.

This is a **VERIFIED MECHANISM STOP**, not a counterexample to ERTC and not an
order exclusion.

## 1. Four exact controls

For `t in {18,19,21}`, take the weighted tree on vertices
`z,b_1,b_2,a,c,d,x` with edges

```text
z--b_1 : 1,
z--b_2 : 2,
z--a   : 10 = p,
z--c   : 7  = g,
c--d   : 6,
b_1--x : t.                                        (FW295.1)
```

Use `q=z--a` as the source edge and `r=z--c` as its target.  Direct skeleton
reconstruction gives

```text
q --path drop, eta=3--> r,
r --edge lift, eta=3--> q,
delta=p-g=3,
ell=0.                                             (FW295.2)
```

Removing `q,r` gives part orders `(1,4,2)`.  The full-window sink is

```text
{z,b_1},                                           (FW295.3)
```

so it is genuinely nontrivial.  The rooted shallow factors are the FW294
state

```text
U=W={0},
Lambda=Rho={0,1,2} below the first hole,
```

and the return at offset six is supplied on the `C` side by `c--d`.

There is also an independent `C`-side control: replace `b_1--x:t` by
`c--x:18`.  Its sink is `{z,c}` and its part orders are `(1,3,3)`, whereas
the three displayed `B`-side controls have sink `{z,b_1}` and part orders
`(1,4,2)`.

All 21 pair distances are distinct in every control.  Their spectra are

```text
t=18: 1,2,3,6,7,8,9,10,11,12,13,14,15,17,18,19,21,23,26,29,32;
t=19: 1,2,3,6,7,8,9,10,11,12,13,14,15,17,19,20,22,23,27,30,33;
t=21: 1,2,3,6,7,8,9,10,11,12,13,14,15,17,21,22,23,24,29,32,35.
C-tail 18: 1,2,3,6,7,8,9,10,11,12,13,14,15,17,18,23,24,25,26,27,35.
```

Each misses global distances four and five and has values above the pair cap
`N=21`; none is Leech.

## 2. What the controls disprove

The controls simultaneously realize

* the exact `BC^3 AB^3 BC` owner strip;
* both rooted convolution ledgers and their common inner root;
* global distance injectivity;
* a nontrivial full-window sink, extended independently through either `B`
  or `C`.

Therefore none of those ingredients, separately or jointly, excludes the
`(3,3)` row.  In particular, the shallow star at `z` does not force the sink
to be singleton: the edge `b_1--x` enlarges the sink behind the already fixed
depth-one owner without changing the strip.

> **STRICT STOP (FW295).**  Do not claim that `(3,3),ell=0` is impossible
> from the FW291 strip, FW294 unit-owner alignment, distance injectivity, or
> nontrivial-sink status.  Any successor must use complete `[1,N]` coverage.

## 3. Smallest live successor

The three controls isolate the first missing information at the actual owners
of global distances four and five.  In the forced `(3,3)` state, rooted depths
`3,4,5` are absent from `B` and from the `r`-outer factor throughout the zero
block, while the known `B` star already owns distances `1,2,3`.

The smallest falsifiable successor is the **`(3,3)` low-owner localization
lemma**:

> In a complete-spectrum exact-return `(3,3),ell=0` state with nontrivial
> sink, the actual owners of distances four and five force either a forbidden
> rooted depth in the `r`-cut zero block, a repeated coefficient in
> `U*Lambda`, or a strictly smaller skeleton return state.

This statement is **UNVERIFIED**.  It names the extra complete-coverage input
that the controls do not possess; merely extending either rooted prefix is
still the stopped FW283 mechanism.

## 4. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_nontrivial_stop.py
theory-lab/topwindow/results/exact_return_33_nontrivial_stop_certificate.json
```

It independently checks all pair distances and then invokes the FW291 owner,
transition, sink, convolution, and connector audit on all three controls.

**Verified:** four exact non-Leech pressure controls and the mechanism stop.

**Not proved:** the low-owner localization lemma, exclusion of `(3,3)`,
extension or exclusion of any other FW294 row, ERTC, NSSC, G18, any new order
exclusion, or global Leech-tree nonexistence.

**Verdict: VERIFIED NONTRIVIAL-SINK CONTROL + STRICT COMPLETE-COVERAGE STOP.**
