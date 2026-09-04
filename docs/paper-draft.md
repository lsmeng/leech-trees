---
title: "There is no Leech tree on 18 vertices"
subtitle: "An exhaustive, replicated search over forced forests"
author: "[AUTHORS — TODO]"
date: "Draft of 2026-08-18 (working draft, not for circulation)"
---

<!--
DRAFTING CONVENTIONS
* Every number taken from the repository documentation is tagged in square brackets with its source
  file, e.g. [README], [ledger] = docs/literature-ledger.md, [theory] = docs/theory-notes.md,
  [ref-forest] = docs/referee-forest.md, [ref-engine] = docs/referee-report.md,
  [engine-opt] = docs/engine-optimization.md, [sat] = docs/sat-route.md,
  [hoffman2-err] = per-shard stderr histograms in results/hoffman2/ and results/hoffman2_rep2/
  (aggregated for this draft, 2026-08-18).
* "TODO" marks a claim that still depends on a pending cross-check (per-topology engine on the cluster,
  clean-room re-implementation) or on a decision by the authors. Remove the tags before submission.
* Target venue/style: short note (Discrete Mathematics note / Integers / EJGTA / Involve), 6-8 pages.
-->

# Abstract

A *Leech tree* of order $n$ is a tree on $n$ vertices with positive integer edge weights whose
$\binom n2$ pairwise path-weights are exactly $1,2,\dots,\binom n2$. Leech (1975) found five such
trees, of orders $2,3,4,4,6$; Taylor (1977) showed that the order must be a square or a square plus
two; computer searches by Székely, Wang and Zhang (2005) and by Calhoun, Ferland, Lister and Polhill
(2007) excluded the admissible orders $9$, $11$ and $16$, so that $n=18$ has been the smallest open
order. We show that there is no Leech tree on $18$ vertices. The proof is an exhaustive computer
search over "forced forests" in the sense of Calhoun et al., organised so that every weighted forest
that can occur as the set of lightest edges of a Leech tree is generated exactly once up to
isomorphism. The search tree has $59{,}779{,}854{,}336$ nodes and contains no tree on $18$ vertices;
its per-level node counts are a mathematical invariant (the number of non-isomorphic forced forests
with a given number of edges) which we report and which was reproduced bit-for-bit by three
independent runs on two architectures and two compilers, and, at the shallow levels, by an
independent enumerator. We also record the same statistics for $n\le 17$, where the search reproduces
the known results, and discuss what would be needed to turn the computation into a formally checkable
certificate.

**Keywords.** Leech tree, perfect distance tree, distinct distance tree, Golomb ruler, Sidon set,
exhaustive search, computer-assisted proof.

**MSC 2020.** 05C05, 05C78, 05C85, 11B83.

# 1. Introduction

Let $T$ be a tree on $n$ vertices with a weight $w(e)\in\mathbb Z_{>0}$ on every edge, and let
$d(x,y)$ denote the weight of the (unique) $x$–$y$ path. Following Leech [Le75] we call $(T,w)$ a
*Leech tree* (also *perfect distance tree*, *perfect distance-distinct tree*) if the multiset
$\{d(x,y):\{x,y\}\subseteq V(T)\}$ equals $\{1,2,\dots,N\}$ with $N=\binom n2$. Leech exhibited five
Leech trees—$K_2$; $P_3$ (weights $1,2$); the star $K_{1,3}$ (weights $1,2,4$); the path $P_4$
(weights $1,3,2$ in path order; the weight $3$ must be the middle edge, so this labelling is unique
up to isomorphism); and the
double star $B_{2,2}$ on six vertices (centres joined by an edge of weight $5$, pendant weights
$1,2$ and $4,8$) [README, ledger L7]—and asked whether there are any others. None has been found since.

Necessary conditions on the order were given by Taylor [Ta77]: counting odd distances shows that a
Leech tree of order $n$ exists only if $n=k^2$ or $n=k^2+2$ for some integer $k$ (Lemma 2.2 below).
The admissible orders are therefore $2,3,4,6,9,11,16,18,25,27,\dots$. Székely, Wang and Zhang [SWZ05]
excluded $n=9$ (also excluded by Shen Lin's search reported by Taylor [Ta91]) and $n=11$ by computer
search, and proved asymptotic upper bounds on the length of a path and on the maximum degree of a
Leech tree. Calhoun, Ferland, Lister and Polhill [CFLP07] introduced *distinct distance trees* (all
path weights distinct, not necessarily forming an interval), gave a backtracking algorithm over
weighted forests with a *forced next weight* (their Lemma 2.6 and Algorithm 2.7), and determined all
perfect distance trees of order $n<18$; in particular they excluded $n=16$ [ledger L14]. Their
summary states the bound as $n\le 24$, but their abstract, their Table 1 (where the entry for $n=18$
is only the trivial lower bound), and every later paper give $n<18$; we treat "24" as a misprint
[ledger L14]. Further structural results—the non-existence of Leech trees of diameter $3$ for
$n\ge 7$, of certain "brooms", the "leaf-Leech" transformation, and Luo and Yu's finiteness result
for diameter $4$ and improved degree bound—are in [OWY16], [VLA20], [LY24]; a Leech labelling of
general graphs was introduced in [EL24]. The order $n=18$ is listed as the smallest open case, for
instance in [VLA20], [OWY16] and in the FrontierMath problem set [FM] [README, ledger L19].

In this note we settle the case $n=18$.

> **Theorem 1.1.** There is no Leech tree on $18$ vertices.

The proof is a computer search. Its mathematical content is small—the forcing lemma of [SWZ05,
CFLP07] and an elementary description of the automorphism group of a forest with distinct edge
weights (Lemma 3.2), which yields a search tree in which every relevant weighted forest appears
exactly once up to isomorphism—and its cost is modest (about $6\times10^{10}$ search nodes, a few
CPU-hours). We nevertheless think that a careful account is warranted, for three reasons. First,
because $n=18$ has been repeatedly cited as open, the result should be stated with a precise
description of what was computed and how it was checked. Second, the per-level node counts of the
search are a well-defined combinatorial quantity (the number of non-isomorphic "forced forests" with
$k$ edges that fit inside a Leech tree of order $18$), so that the computation is falsifiable in a
much stronger sense than a bare "no solution found": any re-implementation must reproduce eighteen
integers, not one bit. Third, we want to be explicit about the status of the result as a
computer-assisted theorem, including the parts that are and are not covered by independent
verification (Section 6).

The rest of the note is organised as follows. Section 2 collects the lemmas that are used, marking
which are classical and which are (minor) additions. Section 3 describes the algorithm and proves
that it is complete and free of isomorphic duplicates. Section 4 describes the verification
strategy. Section 5 states the results for $n\le 18$, including the per-level tables. Section 6
discusses the status of the proof and what remains open.

# 2. Preliminaries

Throughout, $n$ is the order, $N=\binom n2$, and "distance" means weighted path length. Weighted
forests are considered up to isomorphism (a bijection of vertices preserving edges and weights). We
say that a weighted forest is *distance-distinct* if the distances between pairs of vertices in the
same component are pairwise distinct. All lemmas below are elementary; we include proofs of the two
that carry the main argument (Lemmas 2.1 and 3.2) and sketch the rest.

**Lemma 2.1 (forcing lemma; [SWZ05, "Find-Next-Weight"], [CFLP07, Lemma 2.6]).** Let $(T,w)$ be a
Leech tree with edge weights $w_1<w_2<\dots<w_{n-1}$, and for $1\le k\le n-1$ let $F_{k-1}$ be the
forest formed by the edges of weights $w_1,\dots,w_{k-1}$. Then $w_k$ equals the least positive
integer that is not a distance within a component of $F_{k-1}$.

*Proof.* Let $m$ be that least missing integer. If $w_k<m$ then $w_k$ is already a distance in
$F_{k-1}$, contradicting distinctness. If $w_k>m$ then $m$ is not an edge weight, and any path
realising $m$ has at least two edges, hence every edge on it has weight $<m<w_k$ and lies in
$F_{k-1}$; so $m$ would be a distance in $F_{k-1}$, contradiction. Hence $w_k=m$. $\square$
[ledger L4; ref-forest §2]

Consequently $w_1=1$, $w_2=2$, and $w_3\in\{3,4\}$ according as the edges of weight $1$ and $2$ are
non-adjacent or adjacent; a Leech labelling of a given tree is determined by the *order* in which
its edges receive their weights [ledger L1, L4]. Note that Lemma 2.1 fails for graphs with cycles
[CFLP07].

**Lemma 2.2 (Taylor's parity condition [Ta77]; see [SWZ05, Thm 1], [CFLP07, Thm 1.3, Prop 1.8]).** If
a Leech tree of order $n$ exists, then $n=k^2$ or $n=k^2+2$ for an integer $k$; the vertex classes
$A,B$ at even and odd weighted distance from a fixed vertex satisfy $|A||B|=\lceil N/2\rceil$. For
$n=18$: $N=153$, $\{|A|,|B|\}=\{11,7\}$.

*Sketch.* $d(x,y)\equiv d(x,z)+d(y,z)\pmod 2$ in a tree; a distance is odd iff its ends lie in
different classes, so $|A||B|=\lceil N/2\rceil$, and $(|A|-|B|)^2=n^2-4|A||B|\in\{n,n-2\}$.
$\square$ [ledger L2; theory Lemma 6]

**Lemma 2.3 (cut identity).** For any weighted tree, $\sum_{x<y}d(x,y)=\sum_e c_e\,w(e)$, where
$c_e=s_e(n-s_e)$ is the number of vertex pairs separated by $e$ and $s_e$ is the number of vertices
on one side of $e$. For a Leech tree the left side is $N(N+1)/2$. [theory Lemma 1]

**Lemma 2.4 (Golomb and containment bounds).** In a distance-distinct weighted tree:
(a) the vertices of any path with $h$ edges, placed on a line at their cumulative distances, form a
Golomb ruler with $h+1$ marks, so $d(x,y)\ge G(h+1)$ where $G(m)$ is the length of an optimal Golomb
ruler with $m$ marks; (b) if the tree is Leech, every path weight is at most $N$, so the (hop)
diameter $D$ satisfies $G(D+1)\le N$; (c) (containment) if $s_x,s_y$ denote the number of vertices
"behind" $x$ and $y$ on the $x$–$y$ path (so that $s_xs_y$ pairs have paths containing the $x$–$y$
path), then in a Leech tree $d(x,y)\le N+1-s_xs_y$; in particular $w(e)\le N+1-c_e$ for every edge.
[theory Lemmas 3, 4; ledger L6]

The values $G(1),\dots,G(17)=0,1,3,6,11,17,25,34,44,55,72,85,106,127,151,177,199$ (OEIS A003022) are
used; $G(m)$ for $m\le 13$ was re-verified by exhaustive search for this project, and $G(14..17)$ are
taken from the literature (Shearer's tables; the distributed.net OGR project) [ledger L6; ref-engine
§2]. Since $G(16)=177>153=N$, a Leech tree of order $18$ has hop-diameter at most $14$ [theory
Lemma 3; ledger L6]. This strengthens the exact finite form of [SWZ05, Thm 2] (which gives diameter
$\le 15$ at $n=18$ [ledger L5]).

**Lemma 2.5 (star-Sidon degree bound).** Let $v$ be a vertex of degree $d$ in a Leech tree of order
$n$ with incident weights $a_1<\dots<a_d$. Then the $a_i$ and the $\binom d2$ sums $a_i+a_j$
($i<j$) are $d+\binom d2$ pairwise distinct integers in $[1,N]$; call a set of positive integers with
this property (pairwise sums of *distinct* elements distinct and different from the elements)
*star-Sidon*. Let $S(d)$ be the minimum of $a_{d-1}+a_d$ over star-Sidon sets of size $d$; then
$S(d)\le a_{d-1}+a_d\le N+1-b_{(1)}b_{(2)}$, where $b_{(1)}\le b_{(2)}$ are the two smallest branch
sizes at $v$. Exhaustive computation gives

| $d$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $S(d)$ | 3 | 6 | 11 | 19 | 31 | 43 | 63 | 80 | 110 | 138 | 169 |

and $S$ is non-decreasing in $d$. Since $S(12)=169>153$, the maximum degree of a Leech tree of order
$18$ is at most $11$ (a degree-$11$ vertex is possible only with $b_{(1)}b_{(2)}\le 16$). [theory
Lemma 5 (corrected); ref-engine §5; ledger L11]

*Remark (correction).* An earlier version of this lemma asserted that the incident weights form a
Golomb ruler (equivalently a Sidon set in the strong sense) and used $G(d)+G(d-1)+2$ in place of
$S(d)$. That is false: the Leech condition only makes $\{a_i\}$ a *weak* Sidon set (sums of two
distinct elements distinct); three-term arithmetic progressions among the $a_i$ are not excluded. The
star $K_{1,7}$ with weights $\{1,2,4,8,14,19,24\}$ has all $28$ distances distinct, yet
$a_6+a_7=43<44=G(7)+G(6)+2$; the correct minima are those in the table (the two sequences differ from
$d=6$ on). The referee's counterexample was found during the internal audit of the search code
[ref-engine §5]. The maximum-degree consequence at $n=18$ ($\Delta\le 11$) is unaffected: it also
follows from an exhaustive search over star-Sidon sets with all elements and sums $\le 153$, which
finds a set of size $11$ (e.g. $\{1,2,4,7,12,23,32,41,56,70,83\}$) and none of size $12$ [ledger
L11]. Lemma 2.5 is a finite, explicit version of the idea behind [SWZ05, Thm 3] and, we believe, of
[LY24]; we could not access the text of [LY24] and make no claim of priority.

**Lemma 2.6 (weight bounds [CFLP07, Thms 2.8, 2.9]).** In a Leech tree of order $n$ the largest edge
weight satisfies $m_1\le\lfloor(4n-1)^2/48\rfloor$ and the second largest $m_2\le\lfloor(N-1)/2\rfloor$;
more generally the weights of any set of edges lying on a common path sum to at most $N$. At $n=18$:
$m_1\le 105$, $m_2\le 76$. [ledger L12, L13]

**What is used where.** It is worth being precise about which of these statements the proof of
Theorem 1.1 depends on. The forest search of Section 3 uses only Lemma 2.1, the trivial facts that
all distances are distinct and at most $N$ and that a subforest of a Leech tree has at most $n$
vertices, the "common path" case of Lemma 2.6 (any two edges lie on a common path, so
$w(e)+w(f)\le N$; this rule was found never to prune anything at $n\le 18$ [ref-forest §4]), and
Lemma 3.2 below. Lemmas 2.2–2.5 and the rest of 2.6 are *not* needed for Theorem 1.1; they are used
in the independent per-topology engine (Section 4.2) as pruning rules and as topology filters, and are
recorded here because they were verified in the course of the project and because Lemma 2.5 corrects
a statement that circulated in our own notes. Lemmas 2.1, 2.2, 2.6 and Lemma 2.4(a),(b) are from the
literature (2.4(b) as applied to the diameter is folklore; [CFLP07, Prop 1.2] uses it for paths); Lemma
2.3, Lemma 2.4(c), Lemma 2.5 (in the corrected form) and Lemma 3.2 do not seem to appear in the Leech
tree literature, though none of them is deep.

# 3. The algorithm

## 3.1 Forced forests

Fix $n$ and $N=\binom n2$. By Lemma 2.1, if $(T,w)$ is a Leech tree and $t\ge 1$, then the subforest
$F_t=\{e\in T:w(e)<t\}$ satisfies: (i) $F_t$ is distance-distinct with all distances in $[1,N]$; (ii)
$F_t$ has at most $n$ vertices (we regard $F_t$ as a forest without isolated vertices; the vertex set
is the set of endpoints of its edges); (iii) if $t'$ is the least positive integer that is not a
distance of $F_t$, then either $F_t=T$ (in which case $t'=N+1$), or $T$ has an edge of weight exactly
$t'$ and $F_{t'+1}=F_t+e$. Call a weighted forest *forced* (for the target $[1,N]$ and order $n$) if it
arises from the empty forest by repeatedly adding an edge whose weight is the least missing distance,
in one of three ways: *join* (the new edge connects two existing components), *attach* (one endpoint
is a new vertex), or *new* (both endpoints are new; a fresh single-edge component), never exceeding
$n$ vertices and never repeating a distance or exceeding $N$. This is exactly the search of
[CFLP07, Alg. 2.7]. By (iii) every Leech tree of order $n$ is a forced forest with $n-1$ edges and $n$
vertices; conversely a forced forest with $n$ vertices and $n-1$ edges is a tree in which every value
$1..N$ is realised (the least missing value has been pushed to $N+1$), hence a Leech tree.
[ref-forest §2, §3]

The natural DFS enumerates forced forests level by level (level $k$ = $k$ edges). Its cost is
dominated by the last few levels, and without symmetry reduction the same abstract forest is
generated many times, since the endpoints of single-edge components and the components themselves
can be listed in many orders. The one idea that makes the search cheap is complete isomorph
rejection, for which the following two lemmas suffice.

## 3.2 Isomorph rejection

**Lemma 3.1 (canonical parent).** In a forced forest the edge weights are pairwise distinct and the
weights of successive edges are strictly increasing; hence removing the edge of maximum weight from a
forced forest with $k+1$ edges yields a forced forest with $k$ edges, and this parent is well defined
up to isomorphism.

*Proof.* Each new weight $t$ is the least missing distance and becomes a distance once the edge is
added, so later weights are larger. Deleting the last edge returns to the previous state of the
DFS. $\square$ [ref-forest §1]

**Lemma 3.2 (automorphisms of a distinct-weight forest).** Let $P$ be a forest without isolated
vertices whose edge weights are pairwise distinct. Then the group of weight-preserving automorphisms
of $P$ is generated by the transpositions of the two endpoints of the single-edge components of $P$;
in particular $\mathrm{Aut}(P)\cong\mathbb Z_2^{\,s}$, where $s$ is the number of single-edge
components, and it acts on components independently.

*Proof.* Let $\varphi$ be a weight-preserving automorphism. Since the weights are distinct,
$\varphi$ fixes every edge setwise. If two distinct edges $e,f$ share a vertex $v$, then
$\varphi(v)\in e\cap f=\{v\}$, so $v$ is fixed. In a component with at least two edges every edge has
an endpoint of degree $\ge 2$; that endpoint is fixed, and then the other endpoint of the (setwise
fixed) edge is fixed too. So every component with $\ge 2$ edges is fixed pointwise. A single-edge
component admits exactly the identity and the endpoint swap, and swaps of different components
commute and are independent. $\square$ [ref-forest §1]

**Proposition 3.3 (exactly-once generation).** Consider the following restricted DFS. Vertices are
labelled in order of appearance. At a node $P$ (a labelled forced forest), the *eligible* vertices are
all vertices of $P$ except the larger-labelled endpoint of each single-edge component. Children are:
all joins between eligible vertices $x<y$ in different components; all attachments of a new vertex to
an eligible vertex $x$; and, if $P$ has at most $n-2$ vertices, the single "new" child. (Each child is
kept only if it is a forced forest, i.e. passes the distance and vertex tests.) Then every abstract
forced forest with $k$ edges is generated exactly once at level $k$, for every $k$.

*Proof.* Induction on $k$. Assume the level-$k$ nodes are pairwise non-isomorphic and cover every
abstract forced forest with $k$ edges. Let $G$ be an abstract forced forest with $k+1$ edges, $e$ its
maximum-weight edge and $P=G-e$; by Lemma 3.1, $P$ is a forced forest with $k$ edges, so it appears
exactly once as a labelled node $P'$. Two extensions $P'+(x,y,t)$ and $P'+(x',y',t)$ (with the same
forced weight $t$) are isomorphic iff some $\varphi\in\mathrm{Aut}(P')$ maps $\{x,y\}$ to $\{x',y'\}$:
an isomorphism of the children fixes the unique maximum-weight edge and restricts to an automorphism
of the parents. By Lemma 3.2, $\mathrm{Aut}(P')$ is the product of the endpoint swaps of the
single-edge components, so the orbit of an endpoint set is obtained by independently swapping the
endpoint(s) that lie in single-edge components. Choosing the smaller label in each single-edge
component therefore selects exactly one representative per orbit for joins (unordered pairs in
distinct components), for attachments (orbit of $x$), and trivially for the "new" child. Children of
non-isomorphic parents are non-isomorphic (their canonical parents would be isomorphic). $\square$
[ref-forest §1]

Proposition 3.3 is what allows the search tree to be *counted*: its level-$k$ node count equals the
number of non-isomorphic forced forests with $k$ edges for the given $(n,N)$. This makes the
computation checkable in the strong sense discussed in the Introduction. Because Aut is recomputed
from the current component structure at each node, no automorphism state is cached; the appearance
order labelling is used only to pick "the smaller endpoint of a two-vertex component" [ref-forest §1].

## 3.3 Implementation and sharding

The engine (`forest_search.cpp`, C++17, no dependencies) keeps, for each vertex $x$, the bitset
$D_0[x]$ of distances from $x$ within its component, and the bitset $R$ of realised distances. Adding
an edge $(x,y,t)$ generates the new distances as shifted unions $D_0[x]+t+D_0[y]$; a child is
rejected as soon as a shifted set meets $R$ or exceeds $N$, and a per-vertex prefilter discards $x$
when already the distances from $x$ to the *new neighbour* alone collide (these are a subset of the
new distances of any join or attachment at $x$) [ref-forest §4]. All state is undone on return
(incremental, no copies). The only other prune is $t+w_{\max}\le N$ (Lemma 2.6, common path), which
never fires at $n\le 18$ [ref-forest §4]. There are no bounds, counting arguments or lookahead in this
engine; its efficiency comes from Proposition 3.3 (which alone reduced the node count roughly tenfold
at $n=12$–$13$ relative to the same DFS without isomorph rejection [engine-opt §B]) and from bit-parallel
distance sets.

For parallelism the DFS is sharded at a fixed level $L$: the level-$L$ nodes are enumerated in DFS
order (deterministic), and shard $i$ of $K$ explores the subtrees of the level-$L$ nodes with index
$\equiv i \pmod K$; the levels $\le L$ are visited by every shard. Hence, if $h_i(d)$ is the number of
level-$d$ nodes visited by shard $i$, one must have $h_i(d)=h(d)$ for $d\le L$ and every $i$, and
$\sum_i h_i(d)=h(d)$ for $d>L$; the total number of visited nodes is $\sum_i\mathrm{nodes}_i =
\mathrm{unique}+(K-1)\cdot\mathrm{prefix}(\le L)$. These identities were checked in 36 $(n,\text{target},K,L)$
configurations, including $K$ not dividing the number of level-$L$ nodes and $K$ larger than it
[ref-forest §5]. The verdict script for a sharded run asserts: exactly $K$ records, indices $0..K-1$
each once, identical $(K,L)$, all `DONE`, and the histogram identities above [ref-forest §5, §8;
README].

# 4. Verification

The engine of Section 3 was written by an AI coding agent under human direction (see the statement
in Section 7). We therefore treated it as untrusted and audited it in the following ways. Everything
in this section refers to code that is available with the paper (Section 8).

## 4.1 Independent enumerator (oracle) and differential tests

A Python enumerator (`referee_forest_enum.py`), written independently of the C++ code from the
definition in Section 3.1, generates *all* labelled join/attach/new children of every node without
any symmetry rule, keeps a child iff its full distance multiset (recomputed from scratch by BFS) is
duplicate-free and inside the target, and de-duplicates each level by a complete canonical form for
distinct-weight forests without isolated vertices (the sorted multiset of per-vertex sorted
incident-weight tuples). Its per-level counts equal the engine's for every level and every
$n\le 12$ (at $n=12$: $1,1,2,8,41,229,1384,8877,58933,278539,356479$ nodes on levels $0..10$, 23 minutes
in Python), for planted targets with holes at $n=6..9$, and for the prefix of the $n=17$ and $n=18$
trees through level 9 (at $n=18$: $480{,}085$ level-9 forests) [ref-forest §1]. A second Python mode
that re-implements the engine's own generation rule *without* de-duplication produced zero
canonical-form collisions in all these cases, i.e. the isomorph rejection is irredundant as
implemented and not only as proved [ref-forest §1].

Two independent formulations of the same problem were used as further oracles [ref-forest §2, §6]:
(a) a per-topology engine (Section 4.2) whose solution counts, summed over *all* unlabelled trees of a
given order, must equal the forest engine's; this was checked on 45 instances ($n=6..12$, standard
and planted targets, including targets with two non-isomorphic solutions) with 0 mismatches; and (b) a
plain edge-by-edge backtracking over target values with *no* forcing lemma, summed over topologies as
labellings divided by $|\mathrm{Aut}|$, for $n\le 9$. Full-depth planted instances at $n=13,\dots,18$
(random weighted trees with distinct distances, custom target set) were run through the engine: in
all 16 instances the planted tree was found among the solutions and every reported solution was
re-checked; these are the only tests that exercise the $n=18$, full-vertex-count code path with a
witness [ref-forest §7]. Finally the production binary was shown to be a faithful build of the
archived source by reproducing its depth histograms at $n=4..14$ and the exact node count
($100{,}024{,}625$) of one $n=18$ production shard from a byte-for-byte rebuild [ref-forest §6].

## 4.2 Independent method: per-topology search

Before the forest engine we built a per-topology exact search (`leech_search.cpp`): for each of the
$123{,}867$ unlabelled trees on $18$ vertices (OEIS A000055; enumerated by two independent generators,
networkx/WROM and nauty `gentreeg`, which agree for $n=5,9,11,16,18$: $3,47,235,19320,123867$
[README]) it branches on which unassigned edge receives the least missing value (Lemma 2.1) and prunes
with distinctness, the containment and Golomb windows (Lemma 2.4), the cut identity (Lemma 2.3),
Hall-type counting on value windows, Taylor's parity (Lemma 2.2), Lemma 2.6, and complete symmetry
breaking over $\mathrm{Aut}$ of the topology (verified as *exactly one representative per orbit*
by the identity $\mathrm{count(sym)}\cdot|\mathrm{Aut}|=\mathrm{count(nosym)}$ on planted instances
with $|\mathrm{Aut}|$ up to $20{,}000$) [ref-engine §1–§4]. This engine was audited by a differential
harness against a rule-free DFS and against a CP-SAT enumeration: 574 instances (all topologies
$n=7..10$ with planted targets, the standard target $n=7..9$, parity-skewed families, symmetry stress
set) $\times$ 3 binaries $\times$ 32 flag subsets, and a second seed with 560 instances, with 0
discrepancies [ref-engine §7]. It reproduces the literature id-by-id at $n=9$ (47 topologies) and
$n=11$ (235), agreeing with CP-SAT and with the DRAT-certified SAT route (Section 4.3), and it decided
$19{,}308$ of the $19{,}320$ topologies of order $16$ on the cluster ($12$ hit the $1800$ s cap and are
being re-run) [README].

The per-topology engine is between three and four orders of magnitude slower in total than the
forest engine (it re-derives the same small-weight forests once per topology: $n=16$ took $321$ CPU-s
with the forest engine against roughly $500$–$700$ CPU-h per topology-by-topology [engine-opt §B]),
which is why it is used as a *cross-check* rather than as the primary proof. Its run over all $18$-vertex
topologies on the cluster is in progress. **TODO [pending]: report the per-topology outcome for
$n=18$ (first pass had reached $\sim$73k of $\sim$122k topologies; UNKNOWNs are to be re-run with the
v2 engine and larger caps) [README]. Until this is complete, Theorem 1.1 rests on the forest engine
and its audits alone.**

## 4.3 SAT encoding with checked proofs ($n\le 11$)

For small orders we also produced machine-checkable certificates: an order-encoding CNF per topology
(pair/value variables, ternary sum relations along a rooted tree, sibling-subtree symmetry breaking),
solved with CaDiCaL producing DRAT proofs, checked with `drat-trim`. All $47$ topologies at $n=9$ and
all $235$ at $n=11$ are UNSAT with verified proofs (also the 5 non-Leech topologies at $n=6$; the
sixth yields the known tree); this reproduces [SWZ05] with independent certificates [sat §2].
The approach does not scale (30 random $n=16$ topologies: $0/30$ decided in $600$ s each) [sat §3–§4],
so no DRAT-style certificate exists for $n=18$; see Section 6.

## 4.4 Replication of the $n=18$ run

The $n=18$ forest search was run three times, with two shard layouts, on two architectures and with
two compilers, and the per-shard depth histograms were compared [README; hoffman2-err]:

| run | machine / compiler | shards $(K,L)$ | $\sum$ nodes (with repeated prefix) | unique nodes | levels $9..16$ | level 17 | trees found |
|---|---|---|---|---|---|---|---|
| Hoffman2 job 83703 | x86\_64, gcc 11.5 | (210, 8) | 59,795,196,608 | 59,779,854,336 | as in Table 2 | 0 | 0 |
| Hoffman2 job 83752 | x86\_64, gcc 11.5 | (175, 9) | 59,876,162,118 | 59,779,854,336 | identical | 0 | 0 |
| local | arm64 (Apple M4), clang | (512, 8) | 59,817,365,824 | 59,779,854,336 | (histograms not retained) | — | 0 |

The three sums of visited nodes differ exactly by the multiplicity of the shared prefix
($(K-1)\cdot\mathrm{prefix}(\le L)$), and the unique node counts agree bit-for-bit. For the two cluster
runs the per-level sums agree with each other on every level, agree with the Python oracle on levels
$\le 9$, and agree on levels $10..12$ with a capped run of the engine and with the clean-room
implementation of Section 4.5 [ref-forest §8; results/cleanroom]. The node counts of the engine are
deterministic, so this replication detects hardware, compiler and job-management faults (lost or
truncated shards, mis-sharding), not algorithmic errors; the algorithmic checks are those of
Sections 4.1–4.2.

## 4.5 Clean-room re-implementation

**TODO [in progress].** A second implementation of the forced-forest search (`cr_forest.c`, C) was
written from the algorithmic description of Section 3 and [CFLP07] only, without access to the
production source, and is being run over the full $n=18$ tree. At the time of writing it reproduces
the per-level counts $1,1,2,8,41,229,1384,8899,62843,480085,3984162,35540837,332597341$ for levels
$0..12$ at $n=18$ (and $\dots,480084,3983102,35234962,303618177$ at $n=17$) [results/cleanroom\_forest\_18\_prefix12.out,
cleanroom\_forest\_17\_prefix12.out]. **The full-depth run must complete and reproduce all of Table 2
before this section is final; if it does, the sentence "reproduced by three runs" in the abstract
should be strengthened to "and by an independent implementation".**

# 5. Results

## 5.1 Orders $n\le 17$

The forest engine finds exactly the known Leech trees and no others: at $n=4$ two (the star and the
path), at $n=6$ one (the double star), and none at $n=5$ and $7\le n\le 17$ [README; engine-opt §B].
(The condition of Lemma 2.2 is not imposed, so the non-admissible orders are searched as well and
come out empty, as they must.) Node counts and CPU times (single core, Apple M4, under load) are:

| $n$ | nodes | CPU | Leech trees | last levels |
|---|---|---|---|---|
| 11 | 123,309 | 0.05 s | 0 | |
| 12 | 704,494 | 0.14 s | 0 | L8 58,933; L9 278,539; L10 356,479 |
| 13 | 4,178,290 | 0.9 s | 0 | L9 425k; L10 1.86M; L11 1.82M |
| 14 | 25,486,327 | 6.4 s | 0 | L10 3.25M; L11 13.0M; L12 8.66M |
| 15 | 162,497,458 | 44 s | 0 | L11 26.2M; L12 93.5M; L13 38.4M |
| 16 | 1,096,039,152 | 321 s | 0 | L12 220,001,476; L13 683,511,193; L14 154,735,257 |
| 17 | 7,877,582,541 (32 shards, incl. $32\times$ prefix $\le 8$) | 1.7 CPU-h | 0 | |

[engine-opt §B; results/forest\_order\_16.err for the exact $n=16$ level counts]. The full level
histogram at $n=16$ is $1,1,2,8,41,229,1384,8899,62843,480048,3968025,33269745,220001476,683511193,
154735257,0$ (levels $0..15$) [results/forest\_order\_16.err]. The counts at $n=16$ and $n=17$
reproduce the non-existence results of [CFLP07]; those at $n=9,11$ reproduce [SWZ05], and are also
confirmed by the per-topology engine, CP-SAT, and (for $n=9,11$) DRAT-checked SAT proofs. The
per-level counts at low levels are the same for all $n$ once $n$ is large enough for the vertex bound
not to bite ($1,1,2,8,41,229,1384,8899,62843,\dots$), and grow by a factor of roughly $7.5$ per
level; the whole tree grows by a factor of $6.5$–$7$ per unit of $n$ [engine-opt §B].

## 5.2 Order 18

**Theorem 5.1 (Theorem 1.1, quantitative form).** For $n=18$, $N=153$, the search tree of Section 3
has the per-level node counts of Table 2, a total of $59{,}779{,}854{,}336$ nodes, and no node at level
$17$. Consequently there is no Leech tree of order $18$.

*Table 2. Number of non-isomorphic forced forests with $k$ edges for $(n,N)=(18,153)$ [hoffman2-err;
verified identical in both cluster runs; levels $\le 9$ also by the Python oracle, levels $\le 12$ also
by the clean-room implementation].*

| level $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| forests | 1 | 1 | 2 | 8 | 41 | 229 | 1,384 | 8,899 | 62,843 |

| level $k$ | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|
| forests | 480,085 | 3,984,162 | 35,540,837 | 332,597,341 | 2,896,330,052 | 17,017,193,146 | 37,669,242,243 | 1,824,413,062 | **0** |

The tree dies at the last two levels: of the $1.8\times10^9$ distance-distinct forced forests with $16$
edges (i.e. one edge short of a spanning tree on $18$ vertices, or $17$ edges on fewer vertices), none
can be completed. The whole computation cost about $5$–$10$ CPU-hours (roughly $0.3\,\mu$s per node
unloaded) [engine-opt §B]; on the cluster each of the $210$ shard processes ran for about $1.5$
minutes of wall time [README]. For comparison, a per-topology search of the same order was projected
at $10^4$–$10^5$ CPU-hours [README; engine-opt §B].

We record for completeness that the published structural results prune very little at the topology
level: of the $123{,}867$ trees on $18$ vertices, the diameter bound (Lemma 2.4(b)), the degree bound
(Lemma 2.5), the exclusion of stars, double stars, paths and the broom of [VLA20] remove $152$,
leaving $123{,}715$; adding real relaxations (majorisation of the distance vector, projection bound)
leaves $122{,}344$ [ledger §2; theory §Results]. The forest search does not use topologies at all.

# 6. Discussion

**Status of the result.** Theorem 1.1 is a computer-assisted theorem in the usual sense: the
mathematics (Lemmas 2.1, 3.1, 3.2 and Proposition 3.3) is short and has been checked by hand and by
exhaustive small cases; the remainder is a finite computation whose correctness depends on the
faithful execution of a program. What distinguishes this computation from a bare "no solution found"
is that its intermediate output—the eighteen per-level counts of Table 2—is a mathematically defined
sequence (the number of non-isomorphic forced forests of each size), so that any independent
implementation can be checked against it level by level, and the shallow levels have already been
confirmed by an oracle written from the definitions. Three replications on different hardware and
compilers agree bit-for-bit. **TODO: once the per-topology cross-check (Section 4.2) and the
clean-room implementation (Section 4.5) are complete, state their outcome here; if either disagrees
the theorem must be withheld.**

**Certificates.** We do not have a proof certificate for $n=18$ that could be checked by a formally
verified checker, as we do for $n\le 11$ (DRAT). Two routes are open. (i) Cube-and-conquer: use the
forcing-lemma tree to a fixed depth as cubes and certify each cube with a CDCL solver producing DRAT
proofs; the completeness of the cube set follows from Lemma 2.1 by a one-paragraph argument, so the
search engine's pruning need not be trusted, only its branching order. Our experiments at $n=16$
suggest a cost of the order of one CPU-hour per topology and proofs of $10^2$ MB per cube [sat §3],
i.e. $10^4$–$10^5$ CPU-hours for all of $n=18$—feasible on a cluster but not done. (ii) Proof logging
inside the forest engine (VeriPB/pseudo-Boolean), which would certify the isomorph rejection as
well; not attempted. We regard the present level of verification (independent oracle for the shallow
levels, differential tests on planted instances, three bit-identical replications, and the pending
independent implementation) as adequate for the claim, and the per-level counts as the reproducible
artefact that a sceptical reader should target.

**What remains.** The next admissible orders are $n=25$ ($N=300$) and $n=27$ ($N=351$). Extrapolating
the growth factor of $6.5$–$7$ per unit of $n$ [engine-opt §B] gives of the order of $10^{16}$–$10^{17}$
nodes at $n=25$, which is beyond the present method by four to five orders of magnitude; new pruning
ideas (for instance exploiting the top-value structure and the parity classes inside the forest
search, or a meet-in-the-middle over the smallest and largest weights) or a genuinely different
argument would be needed. Whether Leech's five trees are the only Leech trees remains open; the
present note only moves the smallest open order from $18$ to $25$.

# 7. Statement on the use of AI systems

The search programs, the test harnesses, the literature ledger and a first draft of this note were
written by AI coding agents (Anthropic's Claude, in the Claude Code environment) working under the
direction of the human author(s), who set the problem, chose the algorithmic route (forced-forest
search with isomorph rejection), decided what had to be verified, ran the cluster jobs, and reviewed
the proofs and the code. An adversarial "referee" pass over both engines was likewise carried out by
an AI agent instructed to look for unsound pruning and incomplete symmetry breaking; it produced the
correction to Lemma 2.5 recorded in Section 2 and the verification scheme of Section 4 [ref-engine;
ref-forest]. The clean-room implementation of Section 4.5 was written by a separate agent that had
no access to the production source. All mathematical statements in this note were checked by the
human author(s). **TODO: authors to confirm and adjust this statement.**

# 8. Data and code availability

**TODO: repository URL / DOI.** The archive contains: the two search engines (`forest_search.cpp`,
`leech_search.cpp`) and the clean-room `cr_forest.c`; the independent Python enumerators and
differential harnesses; the SAT encoder and the DRAT-verified proofs for $n\le 11$; the frozen list
of the $123{,}867$ trees of order $18$ with the two-generator cross-check; the per-shard output
records and depth histograms of the three $n=18$ runs and of the $n\le 17$ runs; the verdict script;
and the referee reports on which Section 4 is based. The five known Leech trees are checked by two
independent checkers, and every witness produced by any engine in the project was passed through
both.

# References

<!-- TODO: complete bibliographic data; items marked (not read) were only accessible through
reprints/abstracts — see docs/literature-ledger.md §0. -->

- [Le75] J. Leech, Another tree labelling problem, *Amer. Math. Monthly* 82 (1975) 923–925.
- [Ta77] H. Taylor, Odd path sums in an edge-labeled tree, *Math. Mag.* 50 (1977) 258–259.
- [Ta91] H. Taylor, A distinct distance set of 9 nodes in a tree of diameter 36, *Discrete Math.* 93 (1991) 167–168. (TODO: verify title/pages; cited via [CFLP07].)
- [SWZ05] L. A. Székely, H. Wang, Y. Zhang, Some non-existence results on Leech trees, *Bull. Inst. Combin. Appl.* 44 (2005) 37–45.
- [CFLP07] B. Calhoun, K. Ferland, L. Lister, J. Polhill, Minimal distinct distance trees, *J. Combin. Math. Combin. Comput.* 61 (2007) 33–57.
- [OWY16] M. Ozen, H. Wang, C. Yalman, Note on leaf-Leech trees (TODO: exact title), *Integers* 16 (2016) #A21.
- [VLA20] S. Varghese, A. Lakshmanan S., S. Arumugam, Two classes of non-Leech trees, *Electron. J. Graph Theory Appl.* 8 (2020) 205–210.
- [LY24] X. Luo, G. Yu (TODO: initials), A graph labeling problem, *Involve* 17 (2024) 327–335.
- [EL24] M. M. Eldho, A. Lakshmanan S., On Leech labelings of graphs and some related concepts, *Discrete Math.* 347 (2024) 113837.
- [FM] Epoch AI, FrontierMath problem "Leech trees" (accessed 2026-08-18).
- [OEIS] OEIS Foundation, sequences A000055 (unlabelled trees) and A003022 (optimal Golomb rulers).
- [Sh] J. B. Shearer, Golomb ruler tables; distributed.net, OGR project. (TODO: precise citations for $G(14..17)$.)
- [Bi] A. Biere, CaDiCaL; M. Heule, drat-trim. (TODO: precise citations.)
