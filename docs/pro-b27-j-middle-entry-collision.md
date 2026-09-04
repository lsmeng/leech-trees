# `b=27`: middle-entry collision for two-edge J owners

This is a conditional, theorem-level exclusion inside the `J32` branch.  It
does not enumerate trees and does not claim global `b=27` nonexistence.

## Lemma

Let an owner path in `J` have two consecutive edges

\[
A\mathrel{\mathop{\longleftrightarrow}^{\alpha}}M
 \mathrel{\mathop{\longleftrightarrow}^{\beta}}C,
\qquad \alpha,\beta>0.
\]

Assume the geodesic from the carrier/root side first enters this path at the
middle vertex `M`.  Write `rho` for the distance from the `J` root `u` to `M`
(`rho=0` is allowed), and let the carrier edge from the fixed `d6` side to
`u` have weight `w`.  If

\[
|\beta-\alpha|\in\Delta B_0,
\qquad
B_0=\{0,6,13,14,15,23,27,28\},
\]
where `Delta B_0` is the set of positive differences of elements of `B_0`,
then this rooted realization is impossible in a globally pair-distance
injective tree.

### Proof

Suppose `beta>alpha`; the other orientation is symmetric.  Choose fixed
vertices `X,Y` in the literal `L` packet whose `d6`-depths satisfy
\[
d(d6,Y)-d(d6,X)=\beta-\alpha.
\]
The two cross-carrier geodesics then have lengths
\[
d(X,C)=d(d6,X)+w+\rho+\beta,
\]
and
\[
d(Y,A)=d(d6,Y)+w+\rho+\alpha.
\]
They are equal, while the unordered endpoint pairs `{X,C}` and `{Y,A}` are
distinct.  This contradicts global pair-distance injectivity.  The argument
also covers an outside stem entering at `M`, since only the common term
`rho` changes.

## Immediate branch consequences

The positive difference set of `B0` contains `1,2,4,5,27` (and more), while it
does not contain `3`.  Therefore the currently admissible two-edge J words
are affected as follows:

* `34=(16,18)` and `(18,16)` are excluded (`|18-16|=2`);
* `36=(16,20)` and `(20,16)` are excluded (`|20-16|=4`);
* `37=(5,32)` and `(32,5)` are excluded (`|32-5|=27`);
* `37=(16,21)` and `(21,16)` are excluded (`|21-16|=5`);
* `37=(18,19)` and `(19,18)` are excluded (`|19-18|=1`).

The only currently listed two-edge word not covered by this lemma is
`35=(16,19)` (or its reverse), because `19-16=3` is not a positive difference
of `B0`.

## Boundary

This closes only the **middle-entry** realization type for the listed words.
It does not address endpoint entry, a genuine edge-interior subdivision, any
single-edge owner, the `35=(16,19)` middle-entry case, L-internal owners, or
the completeness of the low/high state catalogue.  It therefore does not
upgrade the `J32` branch to a global contradiction.

## Conditional extension for `35=(16,19)`

If a separate theorem has already fixed two distinct named J vertices
`y0,y3` with
\[
d(y0,y3)=35,
\]
then any middle-entry owner path with edge word `(16,19)` has endpoint distance
`16+19=35`.  Global pair-distance injectivity forces its unordered endpoints
to be exactly `{y0,y3}`; a genuinely new realization is impossible.  If the
same theorem also fixes `d(u,y0)=16` and `d(u,y3)=19`, the middle vertex is the
root `u` and no positive external stem remains.

This is conditional because the current finite controls explicitly include
such a named packet, but the global proof state must still supply the
theorem-level implication that every real candidate has that literal 35-owner.
Without that implication, the fixed-L depth set has no difference `3`, and the
abstract path `A-16-M-19-C` with an external stem remains an unresolved model
for this case.
