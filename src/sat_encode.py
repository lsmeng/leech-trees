"""SAT encoding of "tree topology T admits a Leech labeling" (all C(n,2) path sums = {1..N}).

Variables (one-hot): x[p][d]  "pair p has path-sum d", d in dom(p) subset of [1..N].
  dom(p) is pruned: a k-edge path strictly contains C(k+1,2)-1 sub-paths, all with distinct
  smaller sums, so d >= C(k+1,2); the a*b-1 paths strictly containing it (a,b = side sizes)
  are all larger, so d <= N-(a*b-1).
Bijection: exactly-one per pair (row) and exactly-one per value (column).
Structure: root at a center r.  Pairs (u,r) are the root distances D[u].  Every other pair
(u,v) with lca l satisfies exactly one ternary relation X = Y + Z among pair variables:
   l not in {u,v}:  (u,v) = (u,l) + (v,l)
   l = v         :  (u,r) = (v,r) + (u,v)         (v is an ancestor of u)
So there are C(n-1,2) relations, each encoded by support clauses over the one-hot literals
(variant "onehot", 1-3 directions) or by bounds clauses over an order encoding channelled to the
one-hot literals (variant "order").
Symmetry breaking: for isomorphic sibling subtrees under the rooted tree, order the weights of
the edges to the parent (all weights are distinct, so strict order is a valid lex-leader cut).
Optional Taylor parity condition (n=18: number of odd root-distances in {7,11}) as a redundant
cardinality constraint (off by default).
"""
import sys, json, itertools
from math import comb
from pysat.card import CardEnc, EncType


class Encoding:
    def __init__(self, n, edges, root=None, variant="order", dirs=3, symbreak=True,
                 amo="seqcounter", parity=False):
        self.n, self.edges = n, [tuple(e) for e in edges]
        self.N = comb(n, 2)
        self.variant, self.dirs, self.symbreak, self.parity = variant, dirs, symbreak, parity
        self.amo_enc = {"seqcounter": EncType.seqcounter, "ladder": EncType.ladder,
                        "pairwise": EncType.pairwise, "bitwise": EncType.bitwise,
                        "totalizer": EncType.totalizer}[amo]
        self.adj = [[] for _ in range(n)]
        for u, v in self.edges:
            self.adj[u].append(v); self.adj[v].append(u)
        self.root = self._center()[0] if root is None else root
        self._structure()
        self._domains()
        self.nv = 0
        self.clauses = []
        self._vars()
        self._bijection()
        self._relations()
        if symbreak:
            self._symbreak()
        if parity:
            self._parity()

    # ---------- tree structure ----------
    def _center(self):
        n = self.n
        deg = [len(a) for a in self.adj]
        leaves = [v for v in range(n) if deg[v] <= 1]
        removed = len(leaves)
        alive = set(range(n))
        while removed < n:
            alive -= set(leaves)
            new = []
            for v in leaves:
                for w in self.adj[v]:
                    deg[w] -= 1
                    if deg[w] == 1 and w in alive:
                        new.append(w)
            if not new:
                break
            leaves = new
            removed += len(new)
        return sorted(alive) if alive else sorted(leaves)

    def _structure(self):
        n, r = self.n, self.root
        self.parent = [-1] * n
        self.depth = [0] * n
        order = [r]
        seen = [False] * n; seen[r] = True
        for u in order:
            for v in self.adj[u]:
                if not seen[v]:
                    seen[v] = True; self.parent[v] = u; self.depth[v] = self.depth[u] + 1
                    order.append(v)
        self.order = order
        self.children = [[] for _ in range(n)]
        for v in range(n):
            if self.parent[v] >= 0:
                self.children[self.parent[v]].append(v)
        # subtree sizes
        self.sub = [1] * n
        for v in reversed(order):
            if self.parent[v] >= 0:
                self.sub[self.parent[v]] += self.sub[v]
        anc = []
        for v in range(n):
            s, x = [], v
            while x != -1:
                s.append(x); x = self.parent[x]
            anc.append(s)
        self.ancs = anc
        self.lca = {}
        for u in range(n):
            for v in range(u + 1, n):
                su = set(anc[u])
                x = v
                while x not in su:
                    x = self.parent[x]
                self.lca[(u, v)] = x
        self.pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        self.pidx = {p: i for i, p in enumerate(self.pairs)}

    def _side_size(self, u, v):
        """number of vertices x whose path to v passes through u (u's side of path(u,v))"""
        # remove first edge on path u->v ; count component of u
        nxt = self._next_on_path(u, v)
        seen = {u}; stack = [u]
        while stack:
            a = stack.pop()
            for b in self.adj[a]:
                if b not in seen and not (a == u and b == nxt):
                    seen.add(b); stack.append(b)
        return len(seen)

    def _next_on_path(self, u, v):
        l = self.lca[(min(u, v), max(u, v))]
        if u == l:
            # go down toward v
            x = v
            while self.parent[x] != u:
                x = self.parent[x]
            return x
        return self.parent[u]

    def _domains(self):
        N = self.N
        self.dom = {}
        for (u, v) in self.pairs:
            k = self.depth[u] + self.depth[v] - 2 * self.depth[self.lca[(u, v)]]
            lo = comb(k + 1, 2)
            a = self._side_size(u, v); b = self._side_size(v, u)
            hi = N - (a * b - 1)
            self.dom[(u, v)] = (lo, hi)

    # ---------- variables ----------
    def newvar(self):
        self.nv += 1
        return self.nv

    def _vars(self):
        self.x = {}
        for p in self.pairs:
            lo, hi = self.dom[p]
            self.x[p] = {d: self.newvar() for d in range(lo, hi + 1)}
        if self.variant in ("order", "hybrid"):
            # g[p][d] : value(p) >= d, for d in lo+1..hi ; g[lo]=True, g[hi+1]=False
            self.g = {}
            for p in self.pairs:
                lo, hi = self.dom[p]
                self.g[p] = {d: self.newvar() for d in range(lo + 1, hi + 1)}
        # value -> list of (pair, lit)
        self.byval = {d: [] for d in range(1, self.N + 1)}
        for p in self.pairs:
            for d, lit in self.x[p].items():
                self.byval[d].append(lit)

    def ge(self, p, d):
        """literal for value(p) >= d ; returns True/False constants for out-of-range"""
        lo, hi = self.dom[p]
        if d <= lo:
            return True
        if d > hi:
            return False
        return self.g[p][d]

    def add(self, cl):
        self.clauses.append(cl)

    def _exactly_one(self, lits):
        if len(lits) == 1:
            self.add([lits[0]]); return
        self.add(list(lits))
        if len(lits) <= 6:
            for a, b in itertools.combinations(lits, 2):
                self.add([-a, -b])
        else:
            c = CardEnc.atmost(lits=list(lits), bound=1, top_id=self.nv, encoding=self.amo_enc)
            self.nv = max(self.nv, c.nv)
            for cl in c.clauses:
                self.add(cl)

    def _bijection(self):
        for p in self.pairs:
            self._exactly_one(list(self.x[p].values()))
        for d in range(1, self.N + 1):
            lits = self.byval[d]
            assert lits, f"value {d} has no candidate pair"
            self._exactly_one(lits)
        if self.variant in ("order", "hybrid"):
            for p in self.pairs:
                lo, hi = self.dom[p]
                for d in range(lo, hi + 1):
                    xd = self.x[p][d]
                    gd = self.ge(p, d); gd1 = self.ge(p, d + 1)
                    # xd <-> gd & ~gd1
                    if gd is not True:
                        self.add([-xd, gd])
                    if gd1 is not False:
                        self.add([-xd, -gd1])
                    cl = [xd]
                    if gd is not True: cl.append(-gd)
                    if gd1 is not False: cl.append(gd1)
                    self.add(cl)
                for d in range(lo + 1, hi):
                    self.add([-self.g[p][d + 1], self.g[p][d]])

    # ---------- X = Y + Z ----------
    def _relations(self):
        r = self.root
        self.rels = []
        for (u, v) in self.pairs:
            if u == r or v == r:
                continue
            l = self.lca[(u, v)]
            if l == u or l == v:
                anc, desc = (v, u) if l == v else (u, v)
                X = (min(desc, r), max(desc, r)); Y = (min(anc, r), max(anc, r)); Z = (u, v)
            else:
                X = (u, v); Y = (min(u, l), max(u, l)); Z = (min(v, l), max(v, l))
            self.rels.append((X, Y, Z))
            if self.variant == "onehot":
                self._rel_onehot(X, Y, Z)
            elif self.variant == "order":
                self._rel_order(X, Y, Z)
            else:  # hybrid: order-encoding bounds clauses + one-hot support clauses (dirs)
                self._rel_order(X, Y, Z)
                self._rel_onehot(X, Y, Z)

    def _rel_onehot(self, X, Y, Z):
        xd, yd, zd = self.x[X], self.x[Y], self.x[Z]
        dX, dY, dZ = self.dom[X], self.dom[Y], self.dom[Z]
        # dir 1: Y=y & Z=z -> X=y+z
        for y, ly in yd.items():
            for z, lz in zd.items():
                s = y + z
                if dX[0] <= s <= dX[1]:
                    self.add([-ly, -lz, xd[s]])
                else:
                    self.add([-ly, -lz])
        if self.dirs >= 2:
            # dir 2: Y=y & X=x -> Z=x-y
            for y, ly in yd.items():
                for x, lx in xd.items():
                    s = x - y
                    if dZ[0] <= s <= dZ[1]:
                        self.add([-ly, -lx, zd[s]])
                    else:
                        self.add([-ly, -lx])
        if self.dirs >= 3:
            for z, lz in zd.items():
                for x, lx in xd.items():
                    s = x - z
                    if dY[0] <= s <= dY[1]:
                        self.add([-lz, -lx, yd[s]])
                    else:
                        self.add([-lz, -lx])

    def _imp(self, prem, concl):
        """clause: AND(prem) -> concl, with True/False constants handled"""
        cl = []
        for lit in prem:
            if lit is False:
                return
            if lit is True:
                continue
            cl.append(-lit)
        if concl is True:
            return
        if concl is not False:
            cl.append(concl)
        self.add(cl)

    def _rel_order(self, X, Y, Z):
        dX, dY, dZ = self.dom[X], self.dom[Y], self.dom[Z]
        ge = self.ge
        # Y>=a & Z>=b -> X>=a+b
        for a in range(dY[0], dY[1] + 1):
            for b in range(dZ[0], dZ[1] + 1):
                self._imp([ge(Y, a), ge(Z, b)], ge(X, a + b))
        # Y<=a & Z<=b -> X<=a+b   i.e.  ~Y>=a+1 & ~Z>=b+1 -> ~X>=a+b+1
        for a in range(dY[0], dY[1] + 1):
            for b in range(dZ[0], dZ[1] + 1):
                p1, p2, c = ge(Y, a + 1), ge(Z, b + 1), ge(X, a + b + 1)
                p1 = (not p1) if isinstance(p1, bool) else -p1
                p2 = (not p2) if isinstance(p2, bool) else -p2
                c = (not c) if isinstance(c, bool) else -c
                self._imp([p1, p2], c)
        # X>=x & Z<=b -> Y>=x-b ;  X<=x & Z>=b -> Y<=x-b  (and symmetric for Z)
        for (A, B) in ((Y, Z), (Z, Y)):
            dA, dB = self.dom[A], self.dom[B]
            for x in range(dX[0], dX[1] + 1):
                for b in range(dB[0], dB[1] + 1):
                    p2 = ge(B, b + 1); p2 = (not p2) if isinstance(p2, bool) else -p2
                    self._imp([ge(X, x), p2], ge(A, x - b))
                    p1 = ge(X, x + 1); p1 = (not p1) if isinstance(p1, bool) else -p1
                    c = ge(A, x - b + 1); c = (not c) if isinstance(c, bool) else -c
                    self._imp([p1, ge(B, b)], c)

    # ---------- symmetry breaking ----------
    def _canon(self, v):
        return "(" + "".join(sorted(self._canon(c) for c in self.children[v])) + ")"

    def _less(self, P, Q):
        """value(P) < value(Q)"""
        if self.variant in ("order", "hybrid"):
            for a in range(self.dom[P][0], self.dom[P][1] + 1):
                self._imp([self.x[P][a]], self.ge(Q, a + 1))
        else:
            for a, la in self.x[P].items():
                for b, lb in self.x[Q].items():
                    if b <= a:
                        self.add([-la, -lb])

    def _symbreak(self):
        self.sym_constraints = 0
        for v in range(self.n):
            groups = {}
            for c in self.children[v]:
                groups.setdefault(self._canon(c), []).append(c)
            for cs in groups.values():
                for c1, c2 in zip(cs, cs[1:]):
                    P = (min(v, c1), max(v, c1)); Q = (min(v, c2), max(v, c2))
                    self._less(P, Q)
                    self.sym_constraints += 1

    def _parity(self):
        """Taylor: with n=4k+1 or 4k+2 ... general form: number of vertices at odd
        (weighted) distance from the root must make #odd-pairs = #odd values in 1..N.
        Let m = number of vertices (incl. root, even) with odd root-distance; then the number
        of odd path sums is m*(n-m); it must equal ceil(N/2)."""
        n, N = self.n, self.N
        need = (N + 1) // 2
        ms = [m for m in range(n + 1) if m * (n - m) == need]
        if not ms:
            self.add([]); return   # unsat outright
        # odd[v] literal for v != root
        odd = {}
        for v in range(n):
            if v == self.root: continue
            p = (min(v, self.root), max(v, self.root))
            ov = self.newvar(); odd[v] = ov
            for d, lit in self.x[p].items():
                self.add([-lit, ov] if d % 2 else [-lit, -ov])
        lits = list(odd.values())
        # sum(lits) in ms : encode via totalizer-based equals disjunction (small n) -> use
        # a selector variable per allowed m
        sels = []
        for m in ms:
            s = self.newvar(); sels.append(s)
            c = CardEnc.equals(lits=lits, bound=m, top_id=self.nv, encoding=EncType.totalizer)
            self.nv = max(self.nv, c.nv)
            for cl in c.clauses:
                self.add(cl + [-s])
        self.add(sels)

    # ---------- IO ----------
    def write_dimacs(self, path):
        with open(path, "w") as f:
            f.write(f"p cnf {self.nv} {len(self.clauses)}\n")
            f.write("".join(" ".join(map(str, cl)) + " 0\n" for cl in self.clauses))

    def decode(self, model):
        """model: iterable of ints (positive = true). Returns weighted edge list."""
        pos = set(l for l in model if l > 0)
        val = {}
        for p in self.pairs:
            vs = [d for d, lit in self.x[p].items() if lit in pos]
            assert len(vs) == 1, (p, vs)
            val[p] = vs[0]
        return [(u, v, val[(min(u, v), max(u, v))]) for u, v in self.edges]

    def stats(self):
        return {"nv": self.nv, "ncl": len(self.clauses), "root": self.root,
                "nrel": len(self.rels), "variant": self.variant, "dirs": self.dirs,
                "sym": getattr(self, "sym_constraints", 0)}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("id", type=int)
    ap.add_argument("--variant", default="order"); ap.add_argument("--dirs", type=int, default=3)
    ap.add_argument("--no-sym", action="store_true"); ap.add_argument("--parity", action="store_true")
    ap.add_argument("--amo", default="seqcounter")
    ap.add_argument("-o", default=None)
    a = ap.parse_args()
    recs = {json.loads(l)["id"]: json.loads(l) for l in open(f"data/trees_{a.n}.jsonl")}
    rec = recs[a.id]
    E = Encoding(a.n, rec["edges"], variant=a.variant, dirs=a.dirs, symbreak=not a.no_sym,
                 amo=a.amo, parity=a.parity)
    print(json.dumps(E.stats()))
    if a.o:
        E.write_dimacs(a.o); print("wrote", a.o)
