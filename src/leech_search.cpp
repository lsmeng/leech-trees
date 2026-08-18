// leech_search.cpp -- exact search for Leech labelings of ONE tree topology.
//
// Question: given a tree on n vertices, do positive integer edge weights exist such that the
// C(n,2) pairwise path sums are exactly {1..N}, N=C(n,2)?
//
// Two branching modes share the same incremental state and pruning:
//   value  (default): values are covered bottom-up.  Invariant at level t: every value < t is
//          realized, hence every edge of weight < t is assigned.  A path with >=2 edges realizing
//          t consists only of edges < t (already assigned, so t would already be realized); so if
//          t is not yet realized, some UNASSIGNED EDGE must get weight exactly t -> branch over
//          the (<= n-1) unassigned edges.  Branching factor <= 17 instead of ~N per edge.
//   edge : classical edge-driven backtracking; next edge = smallest domain (fail-first, "dyn"),
//          or static BFS-from-center order ("bfs") / its reverse ("rev"); domain computed with
//          bitset shift-ANDs of the missing set.
// Pruning (all switchable, all sound):
//   distinct  realized sums distinct and <= N (3-word bitset)
//   sum       sum_e w_e s_e(n-s_e) = N(N+1)/2 -> [min,max] on remaining budget + per-edge UB
//   hall      interval Hall counting: #pairs with LB<=v >= #missing<=v ; #pairs with UB>=v >= #missing>=v
//   fc        forward check: every unassigned edge keeps a nonempty domain (values w in M with
//             w + (partial sums of pairs completed by that edge) subset of M)
//   parity    Taylor: #vertices at odd weighted depth in {a, n-a}, a(n-a)=ceil(N/2); partial DP over
//             components of the assigned forest
//   sym       complete symmetry breaking of Aut(tree): iso sibling subtrees ordered by first
//             assignment (value mode) / by top-edge weight (edge mode); bicentral half swap.
// Output: one JSON line per topology (id, status SAT/UNSAT/UNKNOWN, nodes, time, witness).
// Deterministic.  No dependencies.  Build: scripts/build.sh
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <algorithm>
#include <chrono>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
using namespace std;
typedef uint64_t u64; typedef uint32_t u32;

#ifndef NW
#define NW 3   // bitset words: 3 -> values up to 191 (n<=18 needs 153); build tests with -DNW=8
#endif
static const int MAXE = 17, MAXV = 18, MAXP = 153, MAXN = 64 * NW - 2;

struct BS {
  u64 w[NW];
  void clear() { for (int i = 0; i < NW; i++) w[i] = 0; }
  bool test(int i) const { return (w[i >> 6] >> (i & 63)) & 1ULL; }
  void set(int i) { w[i >> 6] |= 1ULL << (i & 63); }
  void reset(int i) { w[i >> 6] &= ~(1ULL << (i & 63)); }
  bool any() const { u64 a = 0; for (int i = 0; i < NW; i++) a |= w[i]; return a != 0; }
  int count() const { int c = 0; for (int i = 0; i < NW; i++) c += __builtin_popcountll(w[i]); return c; }
  BS shr(int s) const {  // result bit i = bit (i+s) of *this
    BS r; r.clear(); int q = s >> 6, b = s & 63;
    for (int i = 0; i + q < NW; i++) { int j = i + q; u64 v = w[j] >> b; if (b && j + 1 < NW) v |= w[j + 1] << (64 - b); r.w[i] = v; }
    return r;
  }
  BS shl(int s) const {  // result bit (i+s) = bit i of *this
    BS r; r.clear(); int q = s >> 6, b = s & 63;
    for (int i = NW - 1; i - q >= 0; i--) { int j = i - q; u64 v = w[j] << b; if (b && j - 1 >= 0) v |= w[j - 1] >> (64 - b); r.w[i] = v; }
    return r;
  }
  void clearBelow(int lo) {  // clear all bits < lo
    for (int i = 0; i < NW; i++) { int base = i * 64; if (lo >= base + 64) w[i] = 0; else if (lo > base) w[i] &= ~((1ULL << (lo - base)) - 1); }
  }
  void clearAbove(int hi) {  // clear all bits > hi
    for (int i = 0; i < NW; i++) { int base = i * 64; if (hi + 1 <= base) w[i] = 0; else if (hi + 1 < base + 64) w[i] &= (1ULL << (hi + 1 - base)) - 1; }
  }
  void orw(const BS& o) { for (int i = 0; i < NW; i++) w[i] |= o.w[i]; }
  void andw(const BS& o) { for (int i = 0; i < NW; i++) w[i] &= o.w[i]; }
  void andnot(const BS& o) { for (int i = 0; i < NW; i++) w[i] &= ~o.w[i]; }
  u64 win(int off) const {  // bits [off, off+63] as a word (off may be negative or beyond the end)
    if (off >= 64 * NW) return 0;
    if (off < 0) { return off <= -64 ? 0 : (w[0] << (-off)); }
    int q = off >> 6, b = off & 63; u64 v = w[q] >> b; if (b && q + 1 < NW) v |= w[q + 1] << (64 - b); return v;
  }
  int lowest() const { for (int i = 0; i < NW; i++) if (w[i]) return i * 64 + __builtin_ctzll(w[i]); return -1; }
  int highest() const { for (int i = NW - 1; i >= 0; i--) if (w[i]) return i * 64 + 63 - __builtin_clzll(w[i]); return -1; }
};

struct Opts {
  int mode = 0;          // 0 value, 1 edge
  int order = 0;         // edge mode: 0 dyn, 1 bfs(center-first), 2 rev(leaf-first)
  bool useSum = true, useHall = true, useFC = true, useParity = true, useSym = true, useGrp = true, useCover = false, useMatch = false, useTop = true, useGrp2 = true;
  long long nodeLimit = -1; double timeLimit = -1;
  bool legacy = false; int wcover = 50; bool look = true; int hallW = 40; bool verbose = false; bool countAll = false; int dumpDepth = -1; long long dumpK = 0;
};

struct Solver {
  Opts o;
  int n, E, N, P; long long S;
  int eu[MAXE], ev[MAXE], cc[MAXE]; u32 sideV[MAXE];   // sideV[e]: vertex mask of ev[e]'s side of e
  int pid[MAXV][MAXV];                                  // pair index of (x,y)
  // component-group state (fast path): comp[x] = id of the assigned-forest component containing x (id = a vertex),
  // cmask[id] = its vertex mask, aliveC = live ids; G[a][b] (a<b) = bitset of partial sums of pairs (x in a, y in b).
  // All pairs of one group have the same unassigned-edge set (the path between the components in the quotient tree).
  int comp[MAXV]; u32 cmask[MAXV], aliveC; BS G[MAXV][MAXV];
  struct GI { int mn, mx, cnt; }; GI GIi[MAXV][MAXV]; GI saveGI[MAXE][MAXP];   // min/max/count of each group, kept incrementally
  BS saveG[MAXE][MAXP]; int saveIdx[MAXE][MAXP], saveCnt[MAXE]; int mergeA[MAXE], mergeB[MAXE];
  bool useFast; int wmax; bool tAllowed[MAXE];
  int pu[MAXP], pv[MAXP]; u32 pmask[MAXP]; int plen[MAXP];
  int pairLB[MAXP], pairUB[MAXP];    // static: OGR(hop+1) <= d(p) <= (s_x s_y)-th largest target value (containment)
  int topv[3]; int valPair[MAXN + 2]; // top-3 target values; which pair realized each value (-1)
  bool rootDead;                      // topology killed by static filters (degree/Golomb/containment)
  bool stdTarget; int m1Bound;        // Calhoun Thm 2.8: largest weight <= floor((4n-1)^2/48) (standard target only)
  int poff[MAXE + 1]; vector<int> plist; int epair[MAXE];  // pair index of each edge
  int eid[MAXV][MAXV]; int vdeg[MAXV], vedge[MAXV][MAXV], vnbr[MAXV][MAXV];
  // symmetry
  vector<u32> preq[MAXE];            // value mode: assign e only if amask & m != 0 for each m
  vector<pair<int, int>> ltEdge;     // edge mode: w[a] < w[b]
  vector<int> h1top, h2top;          // edge mode bicentral half rule
  // static order
  int sorder[MAXE];
  int par_a, oddTarget;              // Taylor a (or -1)
  // state
  int w[MAXE]; u32 amask; int s[MAXP]; int rem[MAXP]; BS R; long long Asum; int nAssigned;
  long long nodes, nsol; bool aborted; chrono::steady_clock::time_point t0;
  long long depthHist[MAXE + 1], tHist[MAXN + 2], pruneCnt[8], secT[8];
  // scratch per node
  int ub[MAXE], domsz[MAXE]; BS dom[MAXE];
  int gcnt[MAXE], glist[MAXE][MAXP], gpair[MAXE][MAXP]; int lo_e[MAXE], hi_e[MAXE]; int lb2min;
  BS sBits[MAXE]; BS shM[MAXN + 2]; unsigned shStamp[MAXN + 2]; unsigned shCur = 0;
  BS fullM;

  // ---------------- setup ----------------
  bool build(int n_, const vector<pair<int, int>>& edges, const vector<int>& target) {
    n = n_; E = n - 1; P = n * (n - 1) / 2;
    fullM.clear();
    stdTarget = target.empty();
    if (target.empty()) { N = P; for (int v = 1; v <= N; v++) fullM.set(v); }
    else { if ((int)target.size() != P) return false; N = 0; for (int v : target) { if (v < 1 || v > MAXN) return false; if (fullM.test(v)) return false; fullM.set(v); N = max(N, v); } }
    S = 0; { int oc = 0; for (int v = 1; v <= N; v++) if (fullM.test(v)) { S += v; oc += v & 1; } oddTarget = oc; }
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) eid[i][j] = -1;
    vector<vector<int>> adj(n);
    for (int i = 0; i < n; i++) vdeg[i] = 0;
    for (int e = 0; e < E; e++) { eu[e] = edges[e].first; ev[e] = edges[e].second; eid[eu[e]][ev[e]] = eid[ev[e]][eu[e]] = e; adj[eu[e]].push_back(ev[e]); adj[ev[e]].push_back(eu[e]);
      vedge[eu[e]][vdeg[eu[e]]] = e; vnbr[eu[e]][vdeg[eu[e]]++] = ev[e]; vedge[ev[e]][vdeg[ev[e]]] = e; vnbr[ev[e]][vdeg[ev[e]]++] = eu[e]; }
    // root at 0: parent, depth
    vector<int> par(n, -1), dep(n, 0), order; order.push_back(0); vector<char> seen(n, 0); seen[0] = 1;
    for (size_t i = 0; i < order.size(); i++) { int u = order[i]; for (int v : adj[u]) if (!seen[v]) { seen[v] = 1; par[v] = u; dep[v] = dep[u] + 1; order.push_back(v); } }
    // subtree sizes
    vector<int> sz(n, 1);
    for (int i = n - 1; i > 0; i--) { int v = order[i]; sz[par[v]] += sz[v]; }
    for (int e = 0; e < E; e++) { int child = (par[ev[e]] == eu[e]) ? ev[e] : eu[e]; cc[e] = sz[child] * (n - sz[child]); }
    { // sideV[e] = vertices on ev[e]'s side: subtree of child (if child == ev) else complement
      vector<u32> sub(n, 0); for (int i = n - 1; i >= 0; i--) { int v = order[i]; sub[v] |= 1u << v; if (par[v] >= 0) sub[par[v]] |= sub[v]; }
      for (int e = 0; e < E; e++) { int child = (par[ev[e]] == eu[e]) ? ev[e] : eu[e]; u32 m = sub[child]; sideV[e] = (child == ev[e]) ? m : (((1u << n) - 1) & ~m); } }
    // pairs
    int p = 0;
    for (int u = 0; u < n; u++) for (int v = u + 1; v < n; v++) {
      u32 m = 0; int a = u, b = v, len = 0;
      while (a != b) { if (dep[a] >= dep[b]) { m |= 1u << eid[a][par[a]]; a = par[a]; } else { m |= 1u << eid[b][par[b]]; b = par[b]; } len++; }
      pu[p] = u; pv[p] = v; pmask[p] = m; plen[p] = len; if (len == 1) epair[eid[u][v]] = p; pid[u][v] = pid[v][u] = p; p++;
    }
    // static per-pair windows (Lemma 3 Golomb, Lemma 4c containment)
    static const int OGR[18] = {0, 0, 1, 3, 6, 11, 17, 25, 34, 44, 55, 72, 85, 106, 127, 151, 177, 199};
    // sideSize[e][x]: number of vertices on x's side of edge e (x an endpoint of e)
    auto sideOf = [&](int e, int x) { int child = (par[ev[e]] == eu[e]) ? ev[e] : eu[e]; return (x == child) ? sz[child] : n - sz[child]; };
    // k-th largest target value (k>=1)
    vector<int> tv; for (int v = 1; v <= N; v++) if (fullM.test(v)) tv.push_back(v);
    auto kthLargest = [&](long long k) { if (k > (long long)tv.size()) return 0; return tv[tv.size() - k]; };
    rootDead = false;
    for (int q = 0; q < P; q++) {
      int x = pu[q], y = pv[q]; int ex = -1, ey = -1;
      { int a = x, b = y; while (a != b) { if (dep[a] >= dep[b]) { int e = eid[a][par[a]]; if (a == x) ex = e; if (par[a] == y) ey = e; a = par[a]; } else { int e = eid[b][par[b]]; if (b == y) ey = e; if (par[b] == x) ex = e; b = par[b]; } } }
      long long sx = sideOf(ex, x), sy = sideOf(ey, y);
      pairLB[q] = (plen[q] + 1 <= 17) ? OGR[plen[q] + 1] : 1 << 20; pairUB[q] = kthLargest(sx * sy);
      if (pairLB[q] > pairUB[q]) rootDead = true;
    }
    for (int i = 0; i < 3; i++) topv[i] = (int)tv.size() > i ? tv[tv.size() - 1 - i] : -1;
    m1Bound = stdTarget ? ((4 * n - 1) * (4 * n - 1)) / 48 : N;
    // Lemma 5b: OGR(d)+OGR(d-1)+2 <= (b(1) b(2))-th largest value, at every vertex of degree d>=2
    for (int v = 0; v < n; v++) {
      int d = adj[v].size(); if (d < 2) continue;
      vector<long long> bs; for (int u : adj[v]) bs.push_back(sideOf(eid[u][v], u)); sort(bs.begin(), bs.end());
      long long lhs = (d + 1 <= 17 ? OGR[d] + OGR[d - 1] + 2 : 1 << 20);
      if (lhs > kthLargest(bs[0] * bs[1])) rootDead = true;
    }
    plist.clear();
    for (int e = 0; e < E; e++) { poff[e] = plist.size(); for (int q = 0; q < P; q++) if (pmask[q] >> e & 1) plist.push_back(q); }
    poff[E] = plist.size();
    // Taylor a
    par_a = -1;
    for (int a = 0; a <= n; a++) if (a * (n - a) == oddTarget) { par_a = a; break; }
    setupSymmetry(adj);
    return true;
  }

  // ---- symmetry: centers, rooted canonical forms, sibling groups ----
  vector<int> rpar, rchildren_dummy; vector<vector<int>> rch; vector<string> canon; vector<u32> submask; vector<int> topedge;
  void rootAt(int r, const vector<vector<int>>& adj) {
    rpar.assign(n, -1); rch.assign(n, {}); vector<int> ord{r}; vector<char> seen(n, 0); seen[r] = 1;
    for (size_t i = 0; i < ord.size(); i++) { int u = ord[i]; for (int v : adj[u]) if (!seen[v]) { seen[v] = 1; rpar[v] = u; rch[u].push_back(v); ord.push_back(v); } }
    canon.assign(n, ""); submask.assign(n, 0); topedge.assign(n, -1);
    for (int i = n - 1; i >= 0; i--) {
      int v = ord[i]; vector<string> cs; u32 m = 0;
      for (int c : rch[v]) { cs.push_back(canon[c]); m |= submask[c]; }
      sort(cs.begin(), cs.end()); string sres = "("; for (auto& x : cs) sres += x; sres += ")"; canon[v] = sres;
      if (rpar[v] >= 0) { topedge[v] = eid[v][rpar[v]]; m |= 1u << topedge[v]; }
      submask[v] = m;
    }
  }
  void setupSymmetry(const vector<vector<int>>& adj) {
    for (int e = 0; e < E; e++) preq[e].clear();
    ltEdge.clear(); h1top.clear(); h2top.clear();
    // centers by leaf stripping
    vector<int> deg(n); for (int i = 0; i < n; i++) deg[i] = adj[i].size();
    vector<int> alive(n, 1); int remain = n; vector<int> layer; for (int i = 0; i < n; i++) if (deg[i] <= 1) layer.push_back(i);
    while (remain > 2) { vector<int> nl; for (int v : layer) { alive[v] = 0; remain--; for (int u : adj[v]) if (alive[u]) { if (--deg[u] == 1) nl.push_back(u); } } layer = nl; }
    vector<int> centers; for (int i = 0; i < n; i++) if (alive[i]) centers.push_back(i);
    if (n <= 2) { centers.clear(); for (int i = 0; i < n; i++) centers.push_back(i); }
    int c1 = centers[0], c2 = centers.size() > 1 ? centers[1] : -1;
    rootAt(c1, adj);
    // static BFS order from c1 (center-first connected growth)
    { vector<int> ord{c1}; vector<char> seen(n, 0); seen[c1] = 1; int k = 0;
      for (size_t i = 0; i < ord.size(); i++) { int u = ord[i]; for (int v : adj[u]) if (!seen[v]) { seen[v] = 1; sorder[k++] = eid[u][v]; ord.push_back(v); } } }
    // sibling groups at every vertex
    for (int v = 0; v < n; v++) {
      map<string, vector<int>> groups;
      for (int c : rch[v]) groups[canon[c]].push_back(c);
      for (auto& g : groups) {
        auto& vs = g.second; if (vs.size() < 2) continue;
        for (size_t i = 1; i < vs.size(); i++) {
          u32 prev = submask[vs[i - 1]], cur = submask[vs[i]];
          for (int e = 0; e < E; e++) if (cur >> e & 1) preq[e].push_back(prev);
          ltEdge.push_back({topedge[vs[i - 1]], topedge[vs[i]]});
        }
      }
    }
    // bicentral half swap
    if (c2 >= 0) {
      // half2 = subtree(c2) rooted at c1; half1 = rest minus central edge.  iso iff canon(c2 as child of c1) == canon(c1 with children except c2)
      vector<string> cs; for (int c : rch[c1]) if (c != c2) cs.push_back(canon[c]); sort(cs.begin(), cs.end());
      string h1 = "("; for (auto& x : cs) h1 += x; h1 += ")";
      if (h1 == canon[c2]) {
        int ce = eid[c1][c2]; u32 m2 = submask[c2] & ~(1u << ce); u32 m1 = ((1u << E) - 1) & ~submask[c2];
        for (int e = 0; e < E; e++) if (m2 >> e & 1) preq[e].push_back(m1);
        for (int c : rch[c1]) if (c != c2) h1top.push_back(topedge[c]);
        for (int c : rch[c2]) h2top.push_back(topedge[c]);
      }
    }
  }

  // ---------------- state ops ----------------
  void resetState() {
    for (int e = 0; e < E; e++) w[e] = 0; amask = 0; for (int p = 0; p < P; p++) { s[p] = 0; rem[p] = plen[p]; }
    memset(shStamp, 0, sizeof shStamp); shCur = 0;
    R.clear(); Asum = 0; nAssigned = 0; nodes = 0; nsol = 0; aborted = false; t0 = chrono::steady_clock::now(); wmax = 0;
    for (int x = 0; x < n; x++) { comp[x] = x; cmask[x] = 1u << x; }
    aliveC = (1u << n) - 1;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) { G[a][b].clear(); G[a][b].set(0); GIi[a][b] = {0, 0, 1}; }
    for (int d = 0; d <= E; d++) { wcSolNode[d] = -1; nodeIdAt[d] = -2; }
    memset(depthHist, 0, sizeof depthHist); memset(tHist, 0, sizeof tHist); memset(pruneCnt, 0, sizeof pruneCnt); memset(secT, 0, sizeof secT);
  }
  bool assign(int e, int wt) {
    if (!o.verbose) return assign2(e, wt);
    unsigned long long T0 = tick(); bool r = assign2(e, wt); secT[5] += tick() - T0; return r; }
  bool assign2(int e, int wt) {
    w[e] = wt; amask |= 1u << e; Asum += (long long)wt * cc[e]; nAssigned++;
    const int* pl = plist.data() + poff[e]; int cnt = poff[e + 1] - poff[e];
    for (int i = 0; i < cnt; i++) {
      int p = pl[i]; s[p] += wt;
      if (--rem[p] == 0) { int v = s[p];
        if (v > N || !fullM.test(v) || R.test(v) || v < pairLB[p] || v > pairUB[p]) { rollback(e, i, true); return false; }
        R.set(v); valPair[v] = p;
        if (v >= topv[2] && o.useTop && !topOK(v, p)) { rollback(e, i, false); return false; }
      } else if (s[p] > N) { rollback(e, i, false); return false; }
    }
    // merge the components of the endpoints.  In the quotient tree (components = nodes, unassigned edges = edges)
    // e joins a and b; every group whose quotient path uses e (c on a's side, c' on b's side) shifts by wt, then the
    // groups (a,c) and (b,c) merge (their partial sums must stay distinct: same unassigned set afterwards).
    { int d = nAssigned - 1; int a = comp[eu[e]], b = comp[ev[e]]; u32 sideA = aliveC & ~sideV[e], sideB = aliveC & sideV[e];
      // component ids are vertices, so a component lies on a's side iff its id vertex does
      mergeA[d] = a; mergeB[d] = b; int ns = 0; bool dead = false;
      for (u32 ta = sideA; ta; ta &= ta - 1) { int c = __builtin_ctz(ta);
        for (u32 tb = sideB; tb; tb &= tb - 1) { int c2 = __builtin_ctz(tb); if (c == a && c2 == b) continue;
          BS& g = gref(c, c2); GI& gi = giref(c, c2); saveIdx[d][ns] = c * MAXV + c2; saveG[d][ns] = g; saveGI[d][ns++] = gi; g = g.shl(wt); gi.mn += wt; gi.mx += wt; } }
      for (u32 t2 = aliveC & ~(1u << a) & ~(1u << b); t2 && !dead; t2 &= t2 - 1) {
        int c = __builtin_ctz(t2);
        BS& ga = gref(a, c); const BS& gb = gref(b, c);
        for (int i2 = 0; i2 < NW; i2++) if (ga.w[i2] & gb.w[i2]) { dead = true; break; }
        if (dead) break;
        GI& gia = giref(a, c); const GI& gib = giref(b, c);
        saveIdx[d][ns] = a * MAXV + c; saveG[d][ns] = ga; saveGI[d][ns++] = gia; ga.orw(gb); gia.mn = min(gia.mn, gib.mn); gia.mx = max(gia.mx, gib.mx); gia.cnt += gib.cnt;
      }
      saveCnt[d] = ns;
      if (dead) { for (int j = ns - 1; j >= 0; j--) { gref(saveIdx[d][j] / MAXV, saveIdx[d][j] % MAXV) = saveG[d][j]; giref(saveIdx[d][j] / MAXV, saveIdx[d][j] % MAXV) = saveGI[d][j]; } rollback(e, cnt - 1, false); return false; }
      for (u32 t2 = cmask[b]; t2; t2 &= t2 - 1) comp[__builtin_ctz(t2)] = a;
      cmask[a] |= cmask[b]; aliveC &= ~(1u << b);
    }
    if (wt > wmax) wmax = wt;
    return true;
  }
  BS& gref(int a, int b) { return a < b ? G[a][b] : G[b][a]; }
  GI& giref(int a, int b) { return a < b ? GIi[a][b] : GIi[b][a]; }
  void rollback(int e, int upto, bool lastFailed) {
    const int* pl = plist.data() + poff[e]; int wt = w[e];
    for (int i = upto; i >= 0; i--) {
      int p = pl[i];
      if (rem[p] == 0 && !(lastFailed && i == upto)) R.reset(s[p]);
      rem[p]++; s[p] -= wt;
    }
    w[e] = 0; amask &= ~(1u << e); Asum -= (long long)wt * cc[e]; nAssigned--;
  }
  void unassign(int e) { if (!o.verbose) { unassign2(e); return; } unsigned long long T0 = tick(); unassign2(e); secT[6] += tick() - T0; }
  void unassign2(int e) {
    int d = nAssigned - 1; int a = mergeA[d], b = mergeB[d];
    aliveC |= 1u << b; cmask[a] &= ~cmask[b];
    for (u32 t2 = cmask[b]; t2; t2 &= t2 - 1) comp[__builtin_ctz(t2)] = b;
    for (int j = saveCnt[d] - 1; j >= 0; j--) { gref(saveIdx[d][j] / MAXV, saveIdx[d][j] % MAXV) = saveG[d][j]; giref(saveIdx[d][j] / MAXV, saveIdx[d][j] % MAXV) = saveGI[d][j]; }
    rollback(e, poff[e + 1] - poff[e] - 1, false);
    if (w[e] == 0) { int m = 0; for (int f = 0; f < E; f++) if (w[f] > m) m = w[f]; wmax = m; }
  }
  // Lemma 4a: pairs realizing the 2nd/3rd largest values share an endpoint with the pair realizing the largest.
  bool topOK(int v, int p) const {
    auto meet = [&](int a, int b) { return pu[a] == pu[b] || pu[a] == pv[b] || pv[a] == pu[b] || pv[a] == pv[b]; };
    if (v == topv[0]) { for (int i = 1; i < 3; i++) if (R.test(topv[i]) && !meet(p, valPair[topv[i]])) return false; return true; }
    if (R.test(topv[0])) return meet(p, valPair[topv[0]]);
    return true;
  }

  // ---------------- pruning ----------------
  // m1 = smallest missing value.  Fills ub[], domsz[].  Returns false if node is dead.
  int uedges[MAXE], k;
  static inline unsigned long long tick() {
#if defined(__aarch64__)
    unsigned long long v; __asm__ volatile("mrs %0, cntvct_el0" : "=r"(v)); return v;
#elif defined(__x86_64__)
    unsigned int lo, hi; __asm__ volatile("rdtsc" : "=a"(lo), "=d"(hi)); return ((unsigned long long)hi << 32) | lo;
#else
    return 0;
#endif
  }
  bool prunes(int m1) {
    unsigned long long T0 = o.verbose ? tick() : 0, T1;
    BS M = fullM; M.andnot(R);
    k = 0; for (int e = 0; e < E; e++) if (!(amask >> e & 1)) uedges[k++] = e;
    if (k == 0) return true;
    // k smallest / largest missing values
    int ms[MAXE], ml[MAXE];
    { BS t = M; for (int i = 0; i < k; i++) { int b = t.lowest(); if (b < 0) return false; ms[i] = b; t.reset(b); } }
    { BS t = M; for (int i = 0; i < k; i++) { int b = t.highest(); if (b < 0) return false; ml[i] = b; t.reset(b); } }
    int pms[MAXE + 1]; pms[0] = 0; for (int i = 0; i < k; i++) pms[i + 1] = pms[i] + ms[i];
    long long B = S - Asum;
    { int wmax = 0; for (int e = 0; e < E; e++) if (w[e] > wmax) wmax = w[e];
      int cap = min(m1Bound, N - max(wmax, k >= 2 ? m1 : 0));   // any two edges lie on a common path: w_i + w_j <= N
      for (int i = 0; i < k; i++) { int e = uedges[i]; ub[e] = min(pairUB[epair[e]], cap); } }
    if (o.verbose) { T1 = tick(); secT[0] += T1 - T0; T0 = T1; }
    static u32 hkey[1024]; static int hstamp[1024]; static int stamp = 0; static BS mbits[1024];
    if (o.useGrp && !o.useFC) {
      // pairs with identical unassigned-edge set must have distinct partial sums (their final values differ by 0 otherwise)
      stamp++;
      for (int p = 0; p < P; p++) if (rem[p] > 0) {
        u32 um = pmask[p] & ~amask; u32 key = (um << 8) | (u32)s[p]; if (s[p] > N) { pruneCnt[0]++; return false; }
        u32 h = (key * 2654435761u) >> 22;
        while (hstamp[h] == stamp) { if (hkey[h] == key) { pruneCnt[0]++; return false; } h = (h + 1) & 1023; }
        hstamp[h] = stamp; hkey[h] = key;
      }
    }
    if (o.verbose) { T1 = tick(); secT[1] += T1 - T0; T0 = T1; }
    if (o.useSum) {
      // sort unassigned by c desc
      int idx[MAXE]; for (int i = 0; i < k; i++) idx[i] = uedges[i];
      for (int i = 1; i < k; i++) { int x = idx[i], j = i; while (j > 0 && cc[idx[j - 1]] < cc[x]) { idx[j] = idx[j - 1]; j--; } idx[j] = x; }
      long long minRem = 0, maxRem = 0;
      for (int i = 0; i < k; i++) { minRem += (long long)cc[idx[i]] * ms[i]; maxRem += (long long)cc[idx[i]] * ml[i]; }
      if (minRem > B || maxRem < B) { pruneCnt[1]++; return false; }
      // per-edge UB: others take k-1 smallest missing values greedily
      long long pref[MAXE + 1]; pref[0] = 0; for (int i = 0; i < k; i++) pref[i + 1] = pref[i] + (long long)cc[idx[i]] * ms[i];
      long long suf[MAXE + 2]; suf[k] = 0; for (int i = k - 1; i >= 1; i--) suf[i] = suf[i + 1] + (long long)cc[idx[i]] * ms[i - 1];
      for (int i = 0; i < k; i++) {
        long long others = pref[i] + suf[i + 1];
        long long u = (B - others) / cc[idx[i]];
        if (u < m1) { pruneCnt[1]++; return false; }
        if (u < N) ub[idx[i]] = (int)u;
      }
    }
    if (o.verbose) { T1 = tick(); secT[2] += T1 - T0; T0 = T1; }
    if (o.useFC) {
      shCur++;
      // singleton groups G_e (pairs whose only unassigned edge is e) and 2-crossing pairs
      static int list2[MAXP], list3[MAXP]; int n2 = 0, n3 = 0; int minS2 = N + 1;
      for (int i = 0; i < k; i++) { gcnt[uedges[i]] = 0; sBits[uedges[i]].clear(); }
      stamp++;
      for (int p = 0; p < P; p++) if (rem[p] > 0) {
        if (s[p] > N) { pruneCnt[0]++; return false; }
        u32 um = pmask[p] & ~amask;
        if (rem[p] == 1) { int e = __builtin_ctz(um); gpair[e][gcnt[e]] = p; glist[e][gcnt[e]++] = s[p];
          if (o.useGrp && sBits[e].test(s[p])) { pruneCnt[0]++; return false; }
          sBits[e].set(s[p]); }
        else { if (s[p] < minS2) minS2 = s[p]; if (rem[p] == 2) list2[n2++] = p; else if (o.useGrp2) list3[n3++] = p;
          if (o.useGrp) { u32 h = ((um << 8) * 2654435761u) >> 22;   // one slot per unassigned-edge set, holding the bitset of partial sums
            while (hstamp[h] == stamp && (hkey[h] >> 8) != um) h = (h + 1) & 1023;
            if (hstamp[h] != stamp) { hstamp[h] = stamp; hkey[h] = um << 8; mbits[h].clear(); }
            else if (mbits[h].test(s[p])) { pruneCnt[0]++; return false; }
            mbits[h].set(s[p]); } }
      }
      static BS forb[MAXE];
      for (int i = 0; i < k; i++) forb[uedges[i]].clear();
      if (o.verbose) { T1 = tick(); secT[6] += T1 - T0; T0 = T1; }
      if (o.useGrp) {
        for (int j = 0; j < n2; j++) {
          int p = list2[j]; u32 um = pmask[p] & ~amask; int e = __builtin_ctz(um), f = 31 - __builtin_clz(um); int sp = s[p];
          if (gcnt[e]) forb[f].orw(sBits[e].shr(sp));
          if (gcnt[f]) forb[e].orw(sBits[f].shr(sp));
        }
        if (o.useGrp2) {
          // general: pair p with unassigned set W and pair q with W \ {f}: w_f != s_q - s_p.  sBits per umask via hash table
          // mbits[] (bitset of partial sums per unassigned-edge set) was filled in the grouping pass (reuses the grp hash slots)
          for (int j = 0; j < n3; j++) { int p = list3[j]; u32 um = pmask[p] & ~amask; int sp = s[p]; u32 t2 = um;
            while (t2) { int f = __builtin_ctz(t2); t2 &= t2 - 1; u32 U = um & ~(1u << f); u32 h = ((U << 8) * 2654435761u) >> 22;
              while (hstamp[h] == stamp && (hkey[h] >> 8) != U) h = (h + 1) & 1023;
              if (hstamp[h] == stamp) forb[f].orw(mbits[h].shr(sp)); } }
        }
      }
      if (o.verbose) { T1 = tick(); secT[7] += T1 - T0; T0 = T1; }
      for (int i = 0; i < k; i++) {
        int e = uedges[i]; BS d = M;
        int hi = ub[e], lo = m1;
        for (int j = 0; j < gcnt[e]; j++) { int q = gpair[e][j]; if (pairUB[q] - s[q] < hi) hi = pairUB[q] - s[q]; if (pairLB[q] - s[q] > lo) lo = pairLB[q] - s[q]; }
        if (lo > hi) { pruneCnt[2]++; return false; }
        if (hi < N) d.clearAbove(hi);
        if (lo > 1) d.clearBelow(lo);
        d.andnot(forb[e]);
        for (int j = 0; j < gcnt[e]; j++) { int a = glist[e][j]; if (a > 0) { if (shStamp[a] != shCur) { shStamp[a] = shCur; shM[a] = M.shr(a); } d.andw(shM[a]); if (!d.any()) break; } }
        if (!d.any()) { pruneCnt[2]++; return false; }
        dom[e] = d; if (o.mode == 1) domsz[e] = d.count(); lo_e[e] = d.lowest(); hi_e[e] = d.highest();
      }
      if (o.useCover) {
        // values in [m1, hiCov] that are not realized must come from an edge weight or a singleton-crossing pair
        int hiCov = pms[2] + minS2 - 1; if (k < 2) hiCov = N; if (hiCov > N) hiCov = N;
        BS U = R;
        for (int i = 0; i < k; i++) {
          int e = uedges[i]; const BS& d = dom[e]; U.orw(d);
          for (int j = 0; j < gcnt[e]; j++) { int a = glist[e][j]; if (a > 0) U.orw(d.shl(a)); }
        }
        // check all bits in [m1, hiCov] set
        for (int v = m1; v <= hiCov; v++) if (fullM.test(v) && !U.test(v)) { pruneCnt[7]++; return false; }
      }
    }
    if (o.verbose) { T1 = tick(); secT[3] += T1 - T0; T0 = T1; }
    if (o.useHall) {
      static int cntLB[MAXN + 2], cntUB[MAXN + 2], lbPair[MAXP], ubOf[MAXP];
      memset(cntLB, 0, sizeof(int) * (N + 2)); memset(cntUB, 0, sizeof(int) * (N + 2)); lb2min = N + 1;
      for (int p = 0; p < P; p++) if (rem[p] > 0) {
        int lb = s[p] + pms[rem[p]]; if (pairLB[p] > lb) lb = pairLB[p];
        int u = s[p]; u32 um = pmask[p] & ~amask;
        if (o.useFC) { int lb2 = s[p]; u32 t2 = um; while (t2) { int e = __builtin_ctz(t2); t2 &= t2 - 1; lb2 += lo_e[e]; u += hi_e[e]; } if (lb2 > lb) lb = lb2; }
        else { while (um) { int e = __builtin_ctz(um); um &= um - 1; u += ub[e]; } }
        if (rem[p] >= 2 && lb < lb2min) lb2min = lb;
        if (lb > N) { pruneCnt[3]++; return false; }
        if (u > pairUB[p]) u = pairUB[p];
        if (u < lb) { pruneCnt[3]++; return false; }
        cntLB[lb]++; cntUB[u]++; lbPair[p] = lb; ubOf[p] = u;
      }
      int cumM = 0, cumL = 0;
      for (int v = 1; v <= N; v++) { if (M.test(v)) cumM++; cumL += cntLB[v]; if (cumL < cumM) { pruneCnt[4]++; return false; } }
      cumM = 0; int cumU = 0;
      for (int v = N; v >= 1; v--) { if (M.test(v)) cumM++; cumU += cntUB[v]; if (cumU < cumM) { pruneCnt[5]++; return false; } }
      if (o.useMatch) {
        // exact interval matching (Glover): pairs sorted by UB, each takes the smallest free missing value >= LB
        static int headUB[MAXN + 2], nxt[MAXP], lbOf[MAXP];
        for (int v = 0; v <= N + 1; v++) headUB[v] = -1;
        for (int p = 0; p < P; p++) if (rem[p] > 0) { int u = ubOf[p]; nxt[p] = headUB[u]; headUB[u] = p; }
        BS avail = M;
        for (int u = 1; u <= N; u++) for (int p = headUB[u]; p >= 0; p = nxt[p]) {
          int lb = lbPair[p]; BS t = avail; if (lb > 0) t = t.shr(lb); int b = t.lowest();
          if (b < 0 || b + lb > u) { pruneCnt[5]++; return false; }
          avail.reset(b + lb);
        }
      }
    }
    if (o.verbose) { T1 = tick(); secT[4] += T1 - T0; T0 = T1; }
    if (o.useParity && par_a >= 0) {
      // components of assigned forest with depth parity
      int comp[MAXV], parv[MAXV]; for (int v = 0; v < n; v++) comp[v] = -1;
      u32 reach = 1; int stack[MAXV];
      for (int v = 0; v < n; v++) if (comp[v] < 0) {
        int m = 0, odd = 0, sp = 0; stack[sp++] = v; comp[v] = v; parv[v] = 0;
        while (sp) { int x = stack[--sp]; m++; odd += parv[x];
          for (int j = 0; j < vdeg[x]; j++) { int e = vedge[x][j]; if ((amask >> e & 1)) { int y = vnbr[x][j]; if (comp[y] < 0) { comp[y] = v; parv[y] = parv[x] ^ (w[e] & 1); stack[sp++] = y; } } } }
        reach = (reach << odd) | (reach << (m - odd));
      }
      if (!((reach >> par_a & 1) || (reach >> (n - par_a) & 1))) { pruneCnt[6]++; return false; }
    }
    if (o.verbose) { T1 = tick(); secT[5] += T1 - T0; T0 = T1; }
    return true;
  }

  // ---------------- fast pruning (value mode) ----------------
  // Uses the component groups: for an unassigned edge e = (x,y) with components B = comp[x], C = comp[y]:
  //   S_e = G[B][C] = partial sums of the pairs completed by e  (domain: w + S_e subset of M);
  //   for every other live component A (say on B's side): pairs (A,B) [near, do not use e] and (A,C) [far, use e]
  //   have identical unassigned sets apart from e, so w_e != s_far - s_near  (general one-edge-difference rule =
  //   grp/grp2 of the legacy path).  Same-set duplicates are caught at merge time in assign().
  // Hall: pairs of one group share the unassigned set U, so lb = s + max(pms[|U|], sum lo_e adjusted for distinctness).
  const BS* nearPE[MAXE][MAXV]; const BS* farPE[MAXE][MAXV]; const GI* nearGI[MAXE][MAXV]; const GI* farGI[MAXE][MAXV]; int nAE[MAXE];
  BS reflectN(const BS& a) const {   // bit i -> bit N - i (only bits <= N are set in group bitsets)
    BS r; for (int i = 0; i < NW; i++) r.w[NW - 1 - i] = __builtin_bitreverse64(a.w[i]);   // bit i -> bit 64*NW-1-i
    return r.shr(64 * NW - 1 - N);
  }
  BS fbKnown[MAXE], fbVal[MAXE];   // per-node memo of forbiddenE
  bool forbiddenM(int e, int v) {
    if (fbKnown[e].test(v)) return fbVal[e].test(v);
    bool r = forbiddenE(e, v); fbKnown[e].set(v); if (r) fbVal[e].set(v); return r;
  }
  bool forbiddenE(int e, int v) const {
    int nA = nAE[e]; const BS* const* farP = farPE[e]; const BS* const* nearP = nearPE[e];
    for (int j = 0; j < nA; j++) { const BS& fa = *farP[j]; const BS& ne = *nearP[j];
      int q = v >> 6, b = v & 63;
      for (int i2 = q; i2 < NW; i2++) { u64 x2 = fa.w[i2 - q] << b; if (b && i2 - q - 1 >= 0) x2 |= fa.w[i2 - q - 1] >> (64 - b); if (x2 & ne.w[i2]) return true; }
    }
    return false;
  }
  // window cover: every missing value below the smallest lower bound of a multi-edge pair must be an edge weight or a
  // singleton-pair value w_e + s (s in S_e); the translates S_e + w_e of distinct edges must be disjoint, inside M, and
  // w_e must not be forbidden.  Small DFS on the lowest uncovered value; budget-limited (give up = alive).
  // 64-bit window version: everything is taken relative to t (bit i <-> value t+i); translates and clashes above t+63
  // are ignored (sound: fewer conflicts detected).  SeW[e] = partial sums s <= 63 of S_e, domW[e] = dom[e] window.
  int wcBudget; u64 wcW; int wcT; u64 SeW[MAXE], domW[MAXE], MwT;
  int wcStE[MAXE], wcStW[MAXE], wcSp;                       // current DFS assignment stack
  int wcSolE[MAXE + 1][MAXE], wcSolW[MAXE + 1][MAXE], wcSolN[MAXE + 1], wcSolT[MAXE + 1], lastEdge[MAXE + 1]; long long wcSolNode[MAXE + 1], nodeIdAt[MAXE + 1];
  bool wcover(u64 covered, u32 used) {
    u64 rest = wcW & ~covered; if (!rest) return true; int v = __builtin_ctzll(rest);   // relative value
    if (--wcBudget < 0) return true;
    for (int i = 0; i < k; i++) { int e = uedges[i]; if (used >> e & 1) continue;
      u64 x2 = SeW[e] & ((v >= 63) ? ~0ULL : ((2ULL << v) - 1));   // s <= v  (w = t + v - s >= t)
      const u64 dw = domW[e];
      while (x2) { int a = __builtin_ctzll(x2); x2 &= x2 - 1; int wv = v - a;   // relative weight
        if (!(dw >> wv & 1)) continue;
        u64 tr = SeW[e] << wv; if (tr & covered) continue;
        wcStE[wcSp] = e; wcStW[wcSp] = wv; wcSp++;
        if (wcover(covered | tr, used | (1u << e))) return true;
        wcSp--;
        if (wcBudget < 0) return true; }
    }
    return false;
  }
  // returns false if the window cannot be covered (node dead).  Warm-starts from the parent's cover when consistent.
  bool windowCover(int t, int V) {
    BS Mw = fullM; Mw.andnot(R); Mw.clearAbove(V); Mw = Mw.shr(t); wcW = Mw.w[0]; wcT = t;
    int d = nAssigned; u64 cov = 0; u32 used = 0; wcSp = 0;
    if (d >= 1 && wcSolNode[d - 1] == nodeIdAt[d - 1]) {
      // use the parent's cover only if it contains the edge/weight assigned since (else it is not an extension)
      bool consistent = false; int eLast = lastEdge[d - 1]; int dt = t - wcSolT[d - 1];
      for (int j = 0; j < wcSolN[d - 1]; j++) if (wcSolE[d - 1][j] == eLast && wcSolW[d - 1][j] + wcSolT[d - 1] == w[eLast]) consistent = true;
      if (consistent) for (int j = 0; j < wcSolN[d - 1]; j++) { int e = wcSolE[d - 1][j], wv = wcSolW[d - 1][j] - dt;
        if ((amask >> e & 1) || wv < 0 || wv > 63) continue;
        if (!(domW[e] >> wv & 1)) continue;
        u64 tr = SeW[e] << wv; if (tr & cov) continue;
        cov |= tr; used |= 1u << e; wcStE[wcSp] = e; wcStW[wcSp] = wv; wcSp++; }
    }
    wcBudget = o.wcover;
    bool ok = wcover(cov, used);
    if (!ok && used) { wcSp = 0; wcBudget = o.wcover; ok = wcover(0, 0); }
    if (ok) { wcSolNode[d] = nodeIdAt[d]; wcSolT[d] = t; wcSolN[d] = wcSp; for (int j = 0; j < wcSp; j++) { wcSolE[d][j] = wcStE[j]; wcSolW[d][j] = wcStW[j]; } }
    return ok;
  }
  bool prunesFast(int t) {
    unsigned long long T0 = o.verbose ? tick() : 0, T1;
    BS M = fullM; M.andnot(R);
    k = 0; for (int e = 0; e < E; e++) if (!(amask >> e & 1)) uedges[k++] = e;
    if (k == 0) return true;
    int ms[MAXE]; { BS tt = M; for (int i = 0; i < k; i++) { int b = tt.lowest(); if (b < 0) return false; ms[i] = b; tt.reset(b); } }
    int pms[MAXE + 1]; pms[0] = 0; for (int i = 0; i < k; i++) pms[i + 1] = pms[i] + ms[i];
    int cap = min(m1Bound, N - max(wmax, k >= 2 ? t : 0));   // any two edges lie on a common path: w_i + w_j <= N
    MwT = M.shr(t).w[0];
    if (o.verbose) { T1 = tick(); secT[0] += T1 - T0; T0 = T1; }
    shCur++;
    // Everything below works in the 64-value window [t, t+63] (bit i <-> value t+i); the full range is used only as a
    // fallback when the window is empty (rare).  Only lo_e, membership of t and the window domain are needed.
    for (int i = 0; i < k; i++) {
      int e = uedges[i]; int x = eu[e], y = ev[e]; int B = comp[x], C = comp[y];
      const BS& Se = gref(B, C);
      int hi = min(cap, pairUB[epair[e]]);
      u64 dW = MwT; if (hi - t < 63) dW &= (hi < t) ? 0 : ((2ULL << (hi - t)) - 1);
      // singleton pairs: w + s in M for all s in S_e  (bit 0 of S_e is the edge itself)
      for (int wi = 0; wi < NW && dW; wi++) { u64 x2 = Se.w[wi]; while (x2) { int a = wi * 64 + __builtin_ctzll(x2); x2 &= x2 - 1; if (a == 0) continue;
          dW &= M.win(t + a); if (!dW) break; } }
      if (o.verbose) { T1 = tick(); secT[1] += T1 - T0; T0 = T1; }
      int nA = 0;
      if (o.useGrp) {
        u32 others = aliveC & ~(1u << B) & ~(1u << C);
        const BS** nearP = nearPE[e]; const BS** farP = farPE[e]; const GI** nearI = nearGI[e]; const GI** farI = farGI[e];
        for (u32 t2 = others; t2; t2 &= t2 - 1) {
          int A = __builtin_ctz(t2);
          bool onV = (cmask[A] & sideV[e]) != 0;   // A on y's side -> (A,C) near, (A,B) far
          nearP[nA] = onV ? &gref(A, C) : &gref(A, B); farP[nA] = onV ? &gref(A, B) : &gref(A, C);
          nearI[nA] = onV ? &giref(A, C) : &giref(A, B); farI[nA] = onV ? &giref(A, B) : &giref(A, C); nA++;
        }
        nAE[e] = nA;
        if (dW) {
          // forbidden window F = union_A {b - f : b in near_A, f in far_A} restricted to [t, t+63]; iterate the smaller side
          int dlo = t + __builtin_ctzll(dW), dhi = t + 63 - __builtin_clzll(dW);
          u64 F = 0;
          for (int j = 0; j < nA && (dW & ~F); j++) { const BS& ne = *nearP[j]; const BS& fa = *farP[j]; const GI& ni = *nearI[j]; const GI& fi = *farI[j];
            int nlo = ni.mn, nhi = ni.mx, flo = fi.mn, fhi = fi.mx;
            int fa_lo = max(flo, nlo - dhi), fa_hi = min(fhi, nhi - dlo); if (fa_lo > fa_hi) continue;
            int ne_lo = max(nlo, flo + dlo), ne_hi = min(nhi, fhi + dhi); if (ne_lo > ne_hi) continue;
            if (fi.cnt <= ni.cnt) {
              for (int wi = fa_lo >> 6; wi < NW; wi++) { u64 x2 = fa.w[wi]; if (wi == (fa_lo >> 6)) x2 &= ~0ULL << (fa_lo & 63);
                while (x2) { int f = wi * 64 + __builtin_ctzll(x2); x2 &= x2 - 1; if (f > fa_hi) { wi = NW; break; } F |= ne.win(f + t); } }
            } else {
              BS rf = reflectN(fa);   // bit N - f
              for (int wi = ne_lo >> 6; wi < NW; wi++) { u64 x2 = ne.w[wi]; if (wi == (ne_lo >> 6)) x2 &= ~0ULL << (ne_lo & 63);
                while (x2) { int b = wi * 64 + __builtin_ctzll(x2); x2 &= x2 - 1; if (b > ne_hi) { wi = NW; break; } F |= rf.win(N - b + t); } }
            }
          }
          dW &= ~F;
        }
      } else nAE[e] = 0;
      int lo;
      if (dW) lo = t + __builtin_ctzll(dW);
      else {
        // fallback: full-range domain (values above t+63)
        BS d = M; if (hi < N) d.clearAbove(hi); d.clearBelow(t + 64);
        for (int wi = 0; wi < NW && d.any(); wi++) { u64 x2 = Se.w[wi]; while (x2) { int a = wi * 64 + __builtin_ctzll(x2); x2 &= x2 - 1; if (a == 0) continue;
            if (shStamp[a] != shCur) { shStamp[a] = shCur; shM[a] = M.shr(a); } d.andw(shM[a]); if (!d.any()) break; } }
        if (o.useGrp && d.any()) {   // exact forbidden test per candidate value
          const BS** nearP = nearPE[e]; const BS** farP = farPE[e];
          while (d.any()) { int v = d.lowest(); bool forb = false;
            for (int j = 0; j < nA && !forb; j++) { const BS& fa = *farP[j]; const BS& ne = *nearP[j]; int q = v >> 6, b = v & 63;
              for (int i2 = q; i2 < NW; i2++) { u64 x2 = fa.w[i2 - q] << b; if (b && i2 - q - 1 >= 0) x2 |= fa.w[i2 - q - 1] >> (64 - b); if (x2 & ne.w[i2]) { forb = true; break; } } }
            if (!forb) break; d.reset(v); }
        }
        if (!d.any()) { pruneCnt[2]++; return false; }
        lo = d.lowest();
      }
      tAllowed[e] = (lo == t);
      lo_e[e] = lo; hi_e[e] = hi; ub[e] = hi; SeW[e] = Se.w[0]; domW[e] = dW;
      if (o.verbose) { T1 = tick(); secT[2] += T1 - T0; T0 = T1; }
    }

    if (o.useHall) {
      // Hall lower-bound counting restricted to the window [t, t+HW] (kills beyond it are rare, see docs/engine-optimization.md)
      const int HW = o.hallW; int vmax = min(N, t + HW);
      int cntLB[80]; memset(cntLB, 0, sizeof(int) * (HW + 2)); lb2min = N + 1;
      for (u32 ta = aliveC; ta; ta &= ta - 1) { int A = __builtin_ctz(ta);
        for (u32 tb = ta & (ta - 1); tb; tb &= tb - 1) { int Bc = __builtin_ctz(tb);
          int rx = __builtin_ctz(cmask[A]), ry = __builtin_ctz(cmask[Bc]);
          u32 um = pmask[pid[rx][ry]] & ~amask; int r = __builtin_popcount(um);
          const GI& gi = GIi[A][Bc];
          int base;
          if (r == 1) base = lo_e[__builtin_ctz(um)];
          else {
            // distinctness-adjusted sum of the lower bounds
            int los[MAXE], nl = 0;
            for (u32 t2 = um; t2; t2 &= t2 - 1) { int e = __builtin_ctz(t2); los[nl++] = lo_e[e]; }
            for (int i = 1; i < nl; i++) { int v = los[i], j = i; while (j > 0 && los[j - 1] > v) { los[j] = los[j - 1]; j--; } los[j] = v; }
            int prev = -1; base = 0; for (int i = 0; i < nl; i++) { int v = los[i] > prev ? los[i] : prev + 1; base += v; prev = v; }
            if (pms[r] > base) base = pms[r];
            int l2 = gi.mn + base; if (l2 < lb2min) lb2min = l2;
          }
          if (gi.mx + base > N) { pruneCnt[3]++; return false; }
          if (gi.mn + base > vmax) continue;
          const BS& g = G[A][Bc];
          for (int wi = 0; wi < NW; wi++) { u64 x2 = g.w[wi]; while (x2) { int sv = wi * 64 + __builtin_ctzll(x2) + base; x2 &= x2 - 1; if (sv > vmax) { wi = NW; break; } cntLB[sv - t]++; } }
        }
      }
      int cumM = 0, cumL = 0;
      for (int v = t; v <= vmax; v++) { if (M.test(v)) cumM++; cumL += cntLB[v - t]; if (cumL < cumM) { pruneCnt[4]++; return false; } }
      if (o.wcover > 0 && k >= 2) {
        int V = min(N, lb2min - 1);
        if (V >= t && !windowCover(t, V)) { pruneCnt[7]++; return false; }
      }
    }
    if (o.verbose) { T1 = tick(); secT[3] += T1 - T0; T0 = T1; }
    if (o.useParity && par_a >= 0) {
      // components of the assigned forest with depth parity (via comp[] : DFS inside each component)
      int parv[MAXV]; u32 reach = 1;
      for (u32 ta = aliveC; ta; ta &= ta - 1) { int A = __builtin_ctz(ta); u32 cm = cmask[A]; int m = __builtin_popcount(cm);
        if (m == 1) { reach = (reach << 1) | reach; continue; }
        int root = __builtin_ctz(cm); int odd = 0; int stack[MAXV], sp = 0; u32 seen = 1u << root; stack[sp++] = root; parv[root] = 0;
        while (sp) { int x = stack[--sp]; odd += parv[x];
          for (int j = 0; j < vdeg[x]; j++) { int e = vedge[x][j]; if ((amask >> e & 1)) { int y = vnbr[x][j]; if (!(seen >> y & 1)) { seen |= 1u << y; parv[y] = parv[x] ^ (w[e] & 1); stack[sp++] = y; } } } }
        reach = (reach << odd) | (reach << (m - odd));
      }
      if (!((reach >> par_a & 1) || (reach >> (n - par_a) & 1))) { pruneCnt[6]++; return false; }
    }
    if (o.verbose) { T1 = tick(); secT[4] += T1 - T0; }
    return true;
  }
  bool symOK(int e) const { for (u32 m : preq[e]) if (!(amask & m)) return false; return true; }
  bool checkLimits() {
    if ((nodes & 4095) == 0) {
      if (o.nodeLimit > 0 && nodes >= o.nodeLimit) aborted = true;
      if (o.timeLimit > 0) { double dt = chrono::duration<double>(chrono::steady_clock::now() - t0).count(); if (dt >= o.timeLimit) aborted = true; }
    }
    return !aborted;
  }

  // ---------------- value-driven search ----------------
  bool recV(int t) {
    while (t <= N && (R.test(t) || !fullM.test(t))) t++;
    if (t > N) { nsol++; return !o.countAll; }
    nodes++; nodeIdAt[nAssigned] = nodes; if (o.verbose) { depthHist[nAssigned]++; tHist[t]++; } if (!checkLimits()) return false;
    if (nAssigned == E) return false;
    if (useFast ? !prunesFast(t) : !prunes(t)) return false;
    if (nAssigned == o.dumpDepth && o.dumpK > 0) { o.dumpK--; fprintf(stderr, "t=%d w:", t); for (int e = 0; e < E; e++) fprintf(stderr, " %d-%d:%d", eu[e], ev[e], w[e]); fprintf(stderr, " | R:"); for (int v = 1; v <= N; v++) if (R.test(v)) fprintf(stderr, " %d", v); fprintf(stderr, "\n"); }
    u32 allowed = 0;  // capture before recursion (dom/ub are per-node scratch overwritten by deeper calls)
    for (int e = 0; e < E; e++) if (!(amask >> e & 1) && (useFast ? tAllowed[e] : o.useFC ? dom[e].test(t) : ub[e] >= t)) allowed |= 1u << e;
    if (useFast && o.look) {
      // one-level lookahead: after (e,t) the next missing value t' must be placeable on some other edge f:
      // t' in dom_f (R part) and the translates S_f + t', S_e + t disjoint.  The child's allowed set is a subset of this.
      u64 SeWc[MAXE], dWc[MAXE]; for (int i = 0; i < k; i++) { int f = uedges[i]; SeWc[f] = SeW[f]; dWc[f] = domW[f]; }
      u64 Mw = MwT;
      for (int e = 0; e < E; e++) if (allowed >> e & 1) {
        u64 rest = Mw & ~SeWc[e]; if (!rest) continue; int dt = __builtin_ctzll(rest);   // t' - t
        bool ok = false;
        for (int i = 0; i < k && !ok; i++) { int f = uedges[i]; if (f == e) continue;
          if ((dWc[f] >> dt & 1) && !((SeWc[f] << dt) & SeWc[e])) ok = true; }
        if (!ok) { allowed &= ~(1u << e); pruneCnt[7]++; }
      }
    }
    for (int e = 0; e < E; e++) {
      if (!(allowed >> e & 1)) continue;
      if (o.useSym && !symOK(e)) continue;
      lastEdge[nAssigned] = e;
      if (!assign(e, t)) continue;
      if (recV(t + 1)) return true;
      if (aborted) { unassign(e); return false; }
      unassign(e);
    }
    return false;
  }

  // ---------------- fail-first value search ----------------
  // pick the missing value v (below every multi-crossing pair's LB) with the fewest realizations
  // (edge f with w_f = v, or singleton-crossing pair through f with w_f = v - s_p); branch on those.
  bool symOKw(int f, int wt) const {
    for (auto& pr : ltEdge) { if (pr.first == f && w[pr.second] && wt >= w[pr.second]) return false; if (pr.second == f && w[pr.first] && wt <= w[pr.first]) return false; }
    return true;
  }
  bool halfOK() const {
    if (h1top.empty()) return true;
    int mn = 1 << 30; for (int f : h1top) { if (!w[f]) return true; mn = min(mn, w[f]); }
    for (int f : h2top) if (w[f] && w[f] < mn) return false;
    return true;
  }
  bool recFF() {
    nodes++; if (o.verbose) depthHist[nAssigned]++; if (!checkLimits()) return false;
    BS M = fullM; M.andnot(R); int m1 = M.lowest();
    if (m1 < 0) { nsol++; return !o.countAll; }
    if (nAssigned == E) return false;
    if (!prunes(m1)) return false;   // requires useFC && useHall (dom, gcnt, lb2min)
    int hiV = min(N, lb2min - 1);
    // count candidates per value in [m1, hiV]
    static int cnt[MAXN + 2]; int span = hiV - m1 + 1; if (span <= 0) span = 1, hiV = m1;
    memset(cnt, 0, sizeof(int) * (span + 1));
    for (int i = 0; i < k; i++) { int f = uedges[i]; const BS& d = dom[f];
      for (int v = m1; v <= hiV; v++) if (d.test(v)) cnt[v - m1]++;
      for (int j = 0; j < gcnt[f]; j++) { int a = glist[f][j]; if (a == 0) continue; for (int v = max(m1, a + lo_e[f]); v <= hiV; v++) if (d.test(v - a)) cnt[v - m1]++; } }
    int bestV = -1, bestC = 1 << 30;
    for (int v = m1; v <= hiV; v++) if (M.test(v)) { if (cnt[v - m1] < bestC) { bestC = cnt[v - m1]; bestV = v; if (bestC == 0) break; } }
    if (bestC == 0) return false;
    // enumerate candidates (f, w) -- capture before recursion
    static int candF[MAXE * MAXP], candW[MAXE * MAXP]; int nc = 0;
    int cf[MAXE * (MAXP + 1)], cw[MAXE * (MAXP + 1)];
    for (int i = 0; i < k; i++) { int f = uedges[i]; const BS& d = dom[f];
      if (d.test(bestV)) { cf[nc] = f; cw[nc] = bestV; nc++; }
      for (int j = 0; j < gcnt[f]; j++) { int a = glist[f][j]; if (a > 0 && bestV - a >= 1 && d.test(bestV - a)) { cf[nc] = f; cw[nc] = bestV - a; nc++; } } }
    (void)candF; (void)candW;
    for (int c = 0; c < nc; c++) {
      int f = cf[c], wt = cw[c];
      if (o.useSym && !symOKw(f, wt)) continue;
      if (!assign(f, wt)) continue;
      if (o.useSym && !halfOK()) { unassign(f); continue; }
      if (recFF()) return true;
      if (aborted) { unassign(f); return false; }
      unassign(f);
    }
    return false;
  }

  // ---------------- edge-driven search ----------------
  bool recE() {
    nodes++; if (!checkLimits()) return false;
    if (nAssigned == E) { if (R.count() == P) { nsol++; return !o.countAll; } return false; }
    BS M = fullM; M.andnot(R);
    int m1 = M.lowest();
    if (!prunes(m1)) return false;
    // choose edge
    int e = -1;
    if (o.order == 0 && o.useFC) { int best = 1 << 30; for (int i = 0; i < E; i++) { int f = sorder[i]; if (amask >> f & 1) continue; if (domsz[f] < best) { best = domsz[f]; e = f; } } }
    else if (o.order == 2) { for (int i = E - 1; i >= 0; i--) if (!(amask >> sorder[i] & 1)) { e = sorder[i]; break; } }
    else { for (int i = 0; i < E; i++) if (!(amask >> sorder[i] & 1)) { e = sorder[i]; break; } }
    // domain
    BS d = M; int lo = m1, hi = ub[e];
    if (o.useSym) {
      for (auto& pr : ltEdge) { if (pr.first == e && w[pr.second]) hi = min(hi, w[pr.second] - 1); if (pr.second == e && w[pr.first]) lo = max(lo, w[pr.first] + 1); }
    }
    if (o.useFC) d = dom[e];
    else { const int* pl = plist.data() + poff[e]; int cnt = poff[e + 1] - poff[e];
      for (int j = 0; j < cnt && d.any(); j++) { int p = pl[j]; if (rem[p] == 1 && s[p] > 0) d.andw(M.shr(s[p])); } }
    for (int wt = max(lo, d.lowest()); wt <= hi && wt >= 0; wt++) {
      if (!d.test(wt)) continue;
      if (!assign(e, wt)) continue;
      bool ok = true;
      if (o.useSym && !h1top.empty()) {
        // half rule: min top-edge weight on c1 side < min on c2 side (checked once all h1top assigned)
        int mn = 1 << 30; bool all = true; for (int f : h1top) { if (!w[f]) { all = false; break; } mn = min(mn, w[f]); }
        if (all) for (int f : h2top) if (w[f] && w[f] < mn) { ok = false; break; }
      }
      if (ok && recE()) return true;
      if (aborted) { unassign(e); return false; }
      unassign(e);
    }
    return false;
  }

  bool solve() {
    resetState(); useFast = (o.mode == 0 && !o.legacy);
    if (o.useParity && par_a < 0) { nodes = 1; return false; }
    if (o.useTop && rootDead) { nodes = 1; return false; }
    for (int v = 0; v <= N + 1; v++) valPair[v] = -1;  // Taylor: no admissible bipartition size
    return o.mode == 0 ? recV(1) : o.mode == 2 ? recFF() : recE();
  }
};

static string jsonWitness(const Solver& S) {
  string r = "[";
  for (int e = 0; e < S.E; e++) { if (e) r += ","; r += "[" + to_string(S.eu[e]) + "," + to_string(S.ev[e]) + "," + to_string(S.w[e]) + "]"; }
  return r + "]";
}

// minimal JSONL record parser: "id":int, "n":int, "edges":[[a,b],...]
static bool parseRec(const string& line, long long& id, int& n, vector<pair<int, int>>& edges, vector<int>& target) {
  auto findInt = [&](const char* key, long long& out) -> bool {
    size_t p = line.find(key); if (p == string::npos) return false; p = line.find(':', p); if (p == string::npos) return false;
    p++; while (p < line.size() && line[p] == ' ') p++; out = atoll(line.c_str() + p); return true; };
  long long nn; if (!findInt("\"id\"", id)) id = -1; if (!findInt("\"n\"", nn)) return false; n = (int)nn;
  size_t p = line.find("\"edges\""); if (p == string::npos) return false; p = line.find('[', p);
  edges.clear(); vector<int> nums; int depth = 0; string cur;
  for (; p < line.size(); p++) {
    char c = line[p];
    if (c == '[') depth++;
    else if (c == ']') { if (!cur.empty()) { nums.push_back(atoi(cur.c_str())); cur.clear(); } depth--; if (depth == 0) break; }
    else if (isdigit((unsigned char)c) || c == '-') cur += c;
    else if (!cur.empty()) { nums.push_back(atoi(cur.c_str())); cur.clear(); }
  }
  for (size_t i = 0; i + 1 < nums.size(); i += 2) edges.push_back({nums[i], nums[i + 1]});
  target.clear();
  p = line.find("\"target\"");
  if (p != string::npos) { p = line.find('[', p); for (p++; p < line.size() && line[p] != ']'; p++) { if (isdigit((unsigned char)line[p])) { target.push_back(atoi(line.c_str() + p)); while (p + 1 < line.size() && isdigit((unsigned char)line[p + 1])) p++; } } }
  return (int)edges.size() == n - 1;
}

int main(int argc, char** argv) {
  Opts o; const char* file = nullptr;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--mode") { string m = argv[++i]; o.mode = (m == "edge") ? 1 : (m == "ff") ? 2 : 0; }
    else if (a == "--order") { string m = argv[++i]; o.order = (m == "bfs") ? 1 : (m == "rev") ? 2 : 0; }
    else if (a == "--no-sum") o.useSum = false;
    else if (a == "--no-hall") o.useHall = false;
    else if (a == "--no-fc") o.useFC = false;
    else if (a == "--no-parity") o.useParity = false;
    else if (a == "--no-sym") o.useSym = false;
    else if (a == "--no-grp") o.useGrp = false;
    else if (a == "--cover") o.useCover = true;
    else if (a == "--legacy") o.legacy = true;
    else if (a == "--wcover") o.wcover = atoi(argv[++i]);
    else if (a == "--no-look") o.look = false;
    else if (a == "--hallw") o.hallW = min(78, atoi(argv[++i]));
    else if (a == "--match") o.useMatch = true;
    else if (a == "--no-top") o.useTop = false;
    else if (a == "--no-grp2") o.useGrp2 = false;
    else if (a == "--nodes") o.nodeLimit = atoll(argv[++i]);
    else if (a == "--time") o.timeLimit = atof(argv[++i]);
    else if (a == "-v") o.verbose = true;
    else if (a == "--count") o.countAll = true;
    else if (a == "--dump") { o.dumpDepth = atoi(argv[++i]); o.dumpK = atoll(argv[++i]); }
    else if (a == "-h" || a == "--help") { fprintf(stderr, "usage: leech_search [--mode value|edge] [--order dyn|bfs|rev] [--no-sum|--no-hall|--no-fc|--no-parity|--no-sym] [--nodes L] [--time T] [file.jsonl]\n"); return 0; }
    else file = argv[i];
  }
  istream* in = &cin; ifstream fin; if (file) { fin.open(file); if (!fin) { fprintf(stderr, "cannot open %s\n", file); return 1; } in = &fin; }
  string line; Solver S; S.o = o;
  const char* modeName = o.mode == 0 ? "value" : o.mode == 2 ? "ff" : (o.order == 0 ? "edge-dyn" : o.order == 1 ? "edge-bfs" : "edge-rev");
  while (getline(*in, line)) {
    if (line.find('{') == string::npos) continue;
    long long id; int n; vector<pair<int, int>> edges; vector<int> target;
    if (!parseRec(line, id, n, edges, target) || n < 2 || n > MAXV) { fprintf(stderr, "bad record: %s\n", line.c_str()); continue; }
    if (!S.build(n, edges, target)) { fprintf(stderr, "bad target (size/range/dup) in record id %lld\n", id); continue; }
    bool sat = S.solve();
    double dt = chrono::duration<double>(chrono::steady_clock::now() - S.t0).count();
    if (o.countAll && S.nsol > 0) sat = true;
    const char* st = sat ? "SAT" : (S.aborted ? "UNKNOWN" : "UNSAT");
    if (o.verbose) { fprintf(stderr, "depth:"); for (int d = 0; d <= S.E; d++) fprintf(stderr, " %d:%lld", d, S.depthHist[d]); fprintf(stderr, "\nt:"); for (int t = 1; t <= S.N; t++) if (S.tHist[t]) fprintf(stderr, " %d:%lld", t, S.tHist[t]); fprintf(stderr, "\nprunes grp:%lld sum:%lld fc:%lld lbub:%lld hallL:%lld hallU:%lld par:%lld cover:%lld\n", S.pruneCnt[0], S.pruneCnt[1], S.pruneCnt[2], S.pruneCnt[3], S.pruneCnt[4], S.pruneCnt[5], S.pruneCnt[6], S.pruneCnt[7]);
      if (S.useFast) fprintf(stderr, "ticks(fast sections): setup:%lld dom:%lld forb:%lld hall:%lld par:%lld assign:%lld unassign:%lld\n", S.secT[0], S.secT[1], S.secT[2], S.secT[3], S.secT[4], S.secT[5], S.secT[6]);
      else fprintf(stderr, "ticks(prune sections): setup:%lld grp:%lld sum:%lld fc:%lld hall:%lld par:%lld | fc-group:%lld fc-forb:%lld\n", S.secT[0], S.secT[1], S.secT[2], S.secT[3], S.secT[4], S.secT[5], S.secT[6], S.secT[7]); }
    printf("{\"id\": %lld, \"n\": %d, \"status\": \"%s\", \"nsol\": %lld, \"nodes\": %lld, \"time\": %.4f, \"mode\": \"%s\", \"witness\": %s}\n",
           id, n, st, S.nsol, S.nodes, dt, modeName, sat ? jsonWitness(S).c_str() : "null");
    fflush(stdout);
  }
  return 0;
}
