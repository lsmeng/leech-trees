# Central-edge sumset descent

**OBSERVED theorem.** Every distinct-distance tree has a genuine central edge,
and every Leech tree admits an exact two-set sum representation of the window
above the larger half-diameter. This gives a rigorous global descent dichotomy;
closing either branch of that dichotomy uniformly remains **UNVERIFIED**.

## Central edge and deficit sets

Let `T` be a positively weighted tree with distinct vertex-pair distances,
unique diameter endpoints `a,b`, and `d(a,b)=N`. Realise each weighted edge as
an interval and let `c` be the midpoint of `[a,b]`.

The point `c` lies strictly inside an edge. Indeed, if it were a vertex, the
two distinct pairs `(a,c)` and `(b,c)` would both have distance `N/2`. Let
`L,R` be the two vertex sets obtained by cutting the central edge at `c`, with
`a` in `L` and `b` in `R`. Put

```text
A = {alpha_x = N-d(x,b) : x in L},
B = {beta_y  = N-d(a,y) : y in R}.
```

These are sets of nonnegative integers and both contain zero. For every cross
pair `(x,y)` in `L x R`, its path passes through `c`, so

```text
d(x,y) = N-(alpha_x+beta_y).
```

All cross distances are distinct. Therefore the sum map `A x B -> A+B` is
injective: `|A+B|=|L||R|`.

## Exact Leech prefix and descent dichotomy

Now assume `T` is Leech. Let

```text
D = max(diameter(T[L]), diameter(T[R])),
M = N-D.
```

No within-half pair has distance greater than `D`. Hence every value
`D+1,...,N` is a cross distance. In deficit coordinates this says that

```text
0,1,...,M-1
```

are represented exactly once by `A+B`.

Consequently, for every chosen constant `C`, exactly one of the following
holds:

1. `M<=C`, and a proper half contains a pair of distance
   `D=N-M>=N-C`; or
2. `M>C`, and the bounded prefix `0,1,...,C` has a unique exact
   representation by the two central deficit sets.

This is the precise global form of “descent or bounded top-window tiling.” It
does not assume a spider, a bounded number of branch vertices, or bounded hop
diameter. `QED`

## Computational audit and trust boundary

`theory-lab/topwindow/verify_central_edge_decomposition.py` constructs 900
deterministic random distinct-distance trees of orders 4 through 12 using
powers-of-two edge weights. It independently locates the metric midpoint,
requires it to lie strictly inside an edge, and checks the cross formula and
sum injection on 9,107 cross pairs. It then requires all five known Leech
witnesses to pass both repository checkers and verifies their exact cross
prefixes (14 prefix values in total).

Run:

```text
python3 theory-lab/topwindow/verify_central_edge_decomposition.py
```

The frozen summary is
`theory-lab/topwindow/results/central_edge_decomposition_certificate.json`.

The remaining gap is now explicit. A proper half is not itself a Leech tree,
so case 1 cannot simply invoke induction. In case 2, arbitrary deficit sets
can have long mixed-radix tilings, so injectivity alone is insufficient. The
next proof step must either show that the tree-realised deficit sets exclude
those long tilings, or show that the near-diameter pair in case 1 carries a
smaller active component with enough inherited exact-window data to iterate.

A related extremal case is now closed in
`docs/heaviest-edge-rigidity.md`: when the *heaviest-edge* containment bound is
exact, its two complete rooted distance sets factor an entire interval, and
the only Leech realizations have orders `2,3,4`. This proves strict positive
excess for every order at least five. It does not by itself close the central
prefix case here, where the represented interval may be only a proper prefix
of the cross sumset.
