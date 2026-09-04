// depth_search.cpp -- exact rooted-depth search for Leech trees (C++17, single file, no deps).
//
// =====================================================================================
// MODEL
// =====================================================================================
// A Leech tree of order n is a tree on n vertices with positive integer edge weights whose
// C(n,2) pairwise path distances are exactly [1,N], N = C(n,2).
//
// Root the tree at a vertex rho.  Then dep(v) = d(rho,v) and for every pair
//        d(u,v) = dep(u) + dep(v) - 2*dep(lca(u,v)).
// The n-1 numbers dep(v), v != rho, are the distances from rho, hence PAIRWISE DISTINCT
// and in [1,N].  So a rooted Leech tree has n distinct depths and can be built by placing
// the vertices in strictly increasing depth order; every ancestor of a vertex is strictly
// shallower, hence already placed, so the parent of the new vertex is always among the
// placed ones.  Conversely each rooted weighted tree with distinct depths gives exactly one
// such sequence (sort by depth).  The enumeration is therefore a bijection: no rooted tree
// is produced twice and none is missed.
//
// The engine places vertex v (v = 1..nv-1) by choosing
//      * a depth  delta > dep(v-1)   and
//      * a parent p in {0,...,v-1},
// then computes lcad[v][u] = (u==p ? dep(p) : lcad[p][u]) and the v new distances
// delta + off(u), off(u) = dep(u) - 2*lcad[v][u].  A "node" of the search tree is a
// consistent partial placement; level L = "L+1 vertices placed", so level nv-1 nodes are
// exactly the complete solutions.
//
// =====================================================================================
// PRUNES (each with its soundness argument)
// =====================================================================================
// Throughout, Vmax = largest admissible distance (N in general mode, delta in normal-form
// mode), "allowed" = the target value set, "used" = values already realised.
//
// [P0] Distance validity.  Every new distance must be allowed and not yet used.
//   Sound: in a Leech tree all C(n,2) distances are distinct and lie in the target set.
//   Since the number of pairs equals |target|, a complete placement realises the target
//   set exactly -- so "distinct + inside target" at every step is necessary and, at the
//   leaf, sufficient.
//
// [P1] Offset distinctness (per candidate parent, before the depth loop).
//   For a fixed parent p the new distances are delta + off(u), u < v, with off(u) not
//   depending on delta.  If off(u1) == off(u2) for u1 != u2 then d(v,u1) == d(v,u2) for
//   every delta, so p can be discarded outright.  Sound: two equal distances are forbidden.
//   This is a pure win -- it removes a whole depth loop in O(v).
//
// [P2] Ceiling cap  delta <= Vmax - G(p),  G(p) = max_{u<v} off(u).
//   Sound: it is exactly the statement "the largest new distance delta + G(p) is <= Vmax",
//   i.e. P0's upper test hoisted out of the depth loop.  Note G(p) >= 0 because u = root
//   gives off = 0, so the cap never exceeds Vmax.
//
// [P3] Two-edge cap  delta <= dep(p) + Vmax - wmax.
//   Soundness: for any two distinct edges e,f of a tree there is a path containing both
//   (take the endpoint of e farther from f and the endpoint of f farther from e), so
//   w(e) + w(f) <= diameter <= Vmax.  The new edge has weight delta - dep(p) and wmax is
//   the largest weight already placed, giving delta - dep(p) + wmax <= Vmax.
//
// [P4] Depth headroom  delta <= Vmax - (#vertices still to place after v)  (general mode),
//   resp. delta <= B-1 - (#low vertices still to place after v) in normal-form mode.
//   Sound: depths are strictly increasing and bounded by Vmax (resp. by B-1 for low
//   vertices), so at least one unit of room must be left for each later vertex.
//
// [P5] FORCING / GAP CAP  delta <= dep(v-1) + q,  where q is the (C(k,2)+1)-st smallest
//   value that is allowed and not yet used, k = nv - v = number of vertices not yet placed
//   (v included).  If fewer than C(k,2)+1 such values exist the cap is vacuous.
//   (In normal-form mode the low depths chosen later still create holes s+l that are
//   counted as free here, so C(k,2) is replaced by C(k,2) + #(low depths still to choose);
//   without that slack the prune would be too strong and could lose solutions.)
//   Soundness.  Because vertices are placed in increasing depth order, the placed set is
//   exactly {vertices of depth <= D}, D = dep(v-1); every unplaced vertex has depth >= delta.
//   Take a placed u and an unplaced w.  lca(u,w) is an ancestor of u, hence placed, hence
//   of depth <= dep(u), so d(u,w) = dep(w) + dep(u) - 2*dep(lca) >= dep(w) - dep(u)
//   >= delta - D.  Therefore every target value strictly below delta - D must be realised
//   by a pair of two *unplaced* vertices, and there are only C(k,2) such pairs, all of
//   whose distances are distinct.  Hence #{unrealised target values <= delta-D-1} <= C(k,2),
//   which is equivalent to delta <= D + q.  This is the depth-order analogue of the forcing
//   lemma: at k = 1 it says the last vertex must sit within t_min of the deepest placed
//   vertex, where t_min is the smallest value still missing.
//
// [P6] Hall / capacity condition on small values  (option --hall).
//   Let the unplaced vertices be w_1,...,w_k in increasing depth with lower bounds
//   fut[1] <= ... <= fut[k] (fut[i] = delta + i - 1 when the depth is unknown; in
//   normal-form mode the whole top block of depths is known exactly).  For a threshold t,
//   a target value <= t can be realised by
//     (a) (placed u, unplaced w_i) only if fut[i] - dep(u) <= t, i.e. dep(u) >= fut[i] - t;
//     (b) (w_i, w_j), i<j -- counted exactly when both depths are known (needs
//         fut[j] - fut[i] <= t), conservatively counted otherwise.
//   Every unrealised target value <= t needs its own such pair, so
//         #{unrealised target values <= t}  <=  cap(t)
//   for every t.  Sound by the same lca argument as P5 (of which this is a refinement:
//   P5 is the case t = delta - D - 1, where (a) contributes nothing).  Checked at the
//   smallest --hall-max unrealised values only, which is where it can bind.
//
// [P8] delta is attained:  no low depth equals B-1.
//   Sound: delta is DEFINED as diam(K) = max Spec(K) = max F.  Since F = [1,delta] \ (s+L)
//   and the holes s+l are <= s + (B-1) = delta, max F = delta holds iff delta is not a hole,
//   i.e. iff B-1 = delta - s is not in L.  Dropping this would only make the search
//   redundant across different r (a tree with diam(K) < delta is really an instance of a
//   smaller r), never incomplete.
//
// [P7] Forced smallest edge weights  (option --force-edges, normal-form mode with s >= 3).
//   Forcing lemma: sort the edge weights w_1 < w_2 < ... (they are distinct, being
//   distances).  Let F be the target set and F_i the forest of the i lightest edges.  Then
//   w_{i+1} = min(F \ Spec(F_i)):  "<=" because w_{i+1} is a target value and cannot be
//   realised inside F_i (a path in F_i realising it would duplicate the distance w_{i+1});
//   ">=" because a path realising min(F \ Spec(F_i)) must leave F_i, so it contains an edge
//   of weight >= w_{i+1}.  For i = 0,1 this gives w_1 = f_1 = min F and w_2 = f_2 = the
//   second smallest element of F.  In normal-form mode the holes of F are s + L with all
//   elements >= s, so s >= 3 forces f_1 = 1 and f_2 = 2 independently of L.  The engine
//   then requires an edge of weight 1 and an edge of weight 2, and prunes as soon as no
//   still-unplaced vertex could carry the missing weight (in the top-block phase every
//   remaining depth is known, so this test is exact).
//
// =====================================================================================
// SYMMETRY BREAKING (general mode; each choice is argued to lose nothing)
// =====================================================================================
// --sym none : root anywhere.  Complete but each tree is found once per vertex orbit.
// --sym w1   : the value 1 is a distance; in a positively weighted tree a path of length 1
//              is a single edge, so there is exactly one edge {a,b} of weight 1 (edge
//              weights are distances, hence distinct).  Rooting at a makes dep(b) = 1,
//              the smallest possible positive depth, so b is placed first with parent a.
//              Every Leech tree is therefore enumerated (exactly twice, once for each
//              endpoint of its weight-1 edge).  Vertex 1 is pinned: depth 1, parent 0.
// --sym diam : the largest distance is N and it is realised by a unique pair {a,b}; then
//              ecc(a) = N so a is an endpoint of a diametral path, hence a leaf.  Rooting
//              at a gives dep(b) = N = max depth, so b is the LAST vertex placed and its
//              depth is pinned to N; and since a is a leaf the root has exactly one child,
//              namely vertex 1, so no v >= 2 may take parent 0.  Complete (twice per tree).
// --sub-diam Kv (only with --sym diam) : imposes diam(T - a) >= Kv.  Since a is a leaf,
//              [1,N] is the disjoint union of the depths (= distances from a) and
//              Spec(T-a), so diam(T-a) = max([1,N] \ Depths) and
//              diam(T-a) >= Kv  <=>  [Kv,N] is not contained in Depths
//                                <=>  |Depths cap [1,Kv-1]| >= (n-1) - (N-Kv)
//                                <=>  dep(v) <= Kv-1 for v <= (n-1)-(N-Kv).
//              (An external hypothesis; see README.  Not re-derived here.)
//
// =====================================================================================
// NORMAL-FORM MODE  (--nf --r R --s S, with --order n)
// =====================================================================================
// Structure supplied by the project (see README): let {a,b} be the unique pair at distance
// N, x the neighbour of a, s = w(a,x), K = T - a on k = n-1 vertices rooted at x, D its
// depth set, delta = diam(K).  Then Spec(K) = [1,delta] \ (s + D) exactly,
// delta = C(k,2) + r, m = k - r, A = N - s, B = A - m + 1, and
//        D = L  disjoint-union  [B, A],   |L| = r,  0 in L,  L subset of [0, B-1].
// So the searched object is a rooted tree on k vertices whose r shallowest depths are free
// (increasing, in [0,B-1], starting at 0) and whose deepest m depths are the FORCED
// consecutive block B, B+1, ..., A, with target set F = [1,delta] \ (s+L).  The holes s+l
// are removed from "allowed" as each low depth l is chosen (and must not already be used).
// No nonexistence claim is made anywhere by this program.
//
// Usage:
//   depth_search --order n [--sym none|w1|diam] [--sub-diam K] [--hall] [--hall-max J]
//                [--nodes-limit X] [--split L k K] [--levels] [--quiet] [--verify]
//   depth_search --order n --nf --r R --s S [--force-edges] [--hall] ...
//   depth_search --order n --nf --r R --all-s [...]        (loops s, one summary line each)

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

namespace {

constexpr int MAXV = 34;
constexpr int MAXVAL = 576;    // > C(33,2) = 528 >= N; holes s+l <= N too
constexpr int NW = (MAXVAL + 63) / 64;

// ---------------- parameters ----------------
int n = 6;                 // order of the Leech tree
int N = 15;                // C(n,2)
int nv = 6;                // vertices actually placed (n, or n-1 in normal-form mode)
int Vmax = 15;             // largest admissible distance (N, or delta in nf mode)
bool nf = false;
int nf_r = 0, nf_s = 0, nf_m = 0, nf_A = 0, nf_B = 0, nf_delta = 0;
int symmode = 1;           // 0 none, 1 w1, 2 diam
int subdiam = 0;
bool use_hall = false;
int hall_max = 24;
bool force_edges = false;
bool fe_active = false;   // force_edges AND the instance justifies f1=1, f2=2
bool verify = false;
bool quiet = false;
bool print_witness = true;
long long nodeLimit = -1;
int splitLevel = -1, splitK = 0, splitN = 1;
long long splitCounter = 0;

// ---------------- state ----------------
int dep[MAXV], par[MAXV];
int lcad[MAXV][MAXV];
bool allowedv[MAXVAL];
bool usedv[MAXVAL];
// freeBS: bit t set  <=>  allowedv[t] && !usedv[t].  Maintained incrementally.
uint64_t freeBS[NW];
inline void bsSet(int t)   { freeBS[t >> 6] |= 1ULL << (t & 63); }
inline void bsClear(int t) { freeBS[t >> 6] &= ~(1ULL << (t & 63)); }
inline bool bsTest(int t)  { return (freeBS[t >> 6] >> (t & 63)) & 1ULL; }
// smallest free value >= t, or MAXVAL if none
inline int bsNext(int t) {
    if (t >= MAXVAL) return MAXVAL;
    int w = t >> 6;
    uint64_t m = freeBS[w] & (~0ULL << (t & 63));
    while (!m) { if (++w >= NW) return MAXVAL; m = freeBS[w]; }
    return (w << 6) + __builtin_ctzll(m);
}
int wmaxAt[MAXV];          // largest edge weight among the first v placements
long long nodes = 0, nsol = 0;
long long levelNodes[MAXV];
bool aborted = false;
int nHoleUndo[MAXV], holeUndo[MAXV][2];
int haveW1 = 0, haveW2 = 0;          // counts of edges of weight 1 / 2 (force-edges)
std::vector<std::string> witnesses;

int stampOff[2 * MAXVAL];
int stampGen = 0;

// ---------------- helpers ----------------

// (j)-th smallest value that is allowed and not used; returns Vmax+1 if there are fewer.
inline int kthFree(long long j) {
    if (j <= 0) return 0;
    long long c = 0;
    for (int w = 0; w < NW; ++w) {
        uint64_t m = freeBS[w];
        int pc = __builtin_popcountll(m);
        if (c + pc < j) { c += pc; continue; }
        while (m) {
            int b = __builtin_ctzll(m);
            if (++c == j) { int t = (w << 6) + b; return t <= Vmax ? t : Vmax + 1; }
            m &= m - 1;
        }
    }
    return Vmax + 1;
}

// Independent recomputation of all pairwise distances of the current complete placement.
bool verifyPlacement(std::string& out) {
    int d[MAXV][MAXV];
    for (int i = 0; i < nv; ++i) {
        for (int j = 0; j < nv; ++j) d[i][j] = 0;
    }
    // ancestor walk
    for (int a = 0; a < nv; ++a)
        for (int b = a + 1; b < nv; ++b) {
            bool anc[MAXV] = {false};
            for (int u = a; u != -1; u = par[u]) anc[u] = true;
            int u = b;
            while (!anc[u]) u = par[u];
            d[a][b] = d[b][a] = dep[a] + dep[b] - 2 * dep[u];
        }
    std::vector<int> vals;
    for (int a = 0; a < nv; ++a)
        for (int b = a + 1; b < nv; ++b) vals.push_back(d[a][b]);
    std::sort(vals.begin(), vals.end());
    for (size_t i = 0; i + 1 < vals.size(); ++i)
        if (vals[i] == vals[i + 1]) return false;
    for (int x : vals)
        if (x < 1 || x > Vmax || !allowedv[x]) return false;
    char buf[64];
    out.clear();
    for (int v = 1; v < nv; ++v) {
        std::snprintf(buf, sizeof buf, "%s%d-%d:%d", v == 1 ? "" : " ", par[v], v, dep[v] - dep[par[v]]);
        out += buf;
    }
    out += "  depths:";
    for (int v = 0; v < nv; ++v) { std::snprintf(buf, sizeof buf, " %d", dep[v]); out += buf; }
    return true;
}

// [P6] Hall / capacity check.  Returns false to prune.
// fut[] = sorted lower bounds on the depths of the k unplaced vertices, futExact[] flags.
bool hallOK(int v, int nextLow) {
    int k = nv - v;
    if (k <= 1) return true;
    const int holeSlack = (nf && v < nf_r) ? (nf_r - v) : 0;   // see [P5] note
    static int fut[MAXV];
    static bool futExact[MAXV];
    int kk = 0;
    if (nf) {
        // remaining low vertices: unknown, >= nextLow + i ; then the whole top block
        for (int i = v; i < nf_r; ++i) { fut[kk] = nextLow + (i - v); futExact[kk] = false; ++kk; }
        int firstHigh = (v > nf_r) ? v : nf_r;
        for (int i = firstHigh; i < nv; ++i) { fut[kk] = nf_B + (i - nf_r); futExact[kk] = true; ++kk; }
    } else {
        for (int i = 0; i < k; ++i) { fut[i] = nextLow + i; futExact[i] = false; }
        kk = k;
    }
    if (kk != k) return true;   // defensive
    // sorted unrealised target values
    static int t[MAXVAL];
    int nt = 0;
    for (int x = bsNext(1); x <= Vmax && nt < hall_max; x = bsNext(x + 1)) t[nt++] = x;
    for (int idx = 0; idx < nt; ++idx) {
        int tau = t[idx];
        long long cap = 0;
        for (int i = 0; i < k; ++i) {
            int lo = fut[i] - tau;                       // need dep(u) >= lo
            for (int u = 0; u < v; ++u)
                if (dep[u] >= lo) ++cap;
            for (int j = i + 1; j < k; ++j) {
                if (futExact[i] && futExact[j]) { if (fut[j] - fut[i] <= tau) ++cap; }
                else ++cap;
            }
            if (cap + holeSlack > idx) break;
        }
        if (cap + holeSlack < idx + 1) return false;
    }
    return true;
}

// [P7] can an edge of weight w still appear?  Exact once every remaining depth is known
// (normal-form top-block phase); conservative (returns true) otherwise.
bool weightStillPossible(int v, int w) {
    if (!nf || v < nf_r) return true;   // low depths still free -> cannot decide, allow
    // all depths known: low depths dep[0..r-1], high depths B..A
    for (int i = v; i < nv; ++i) {
        int dv = nf_B + (i - nf_r);
        int need = dv - w;
        if (need < 0) continue;
        for (int u = 0; u < nf_r; ++u) if (dep[u] == need) return true;
        if (need >= nf_B && need <= nf_A) return true;
    }
    return false;
}

void report_solution() {
    ++nsol;
    if (print_witness) {
        std::string s;
        if (verify) {
            if (!verifyPlacement(s)) { std::fprintf(stderr, "INTERNAL: bad solution\n"); std::exit(4); }
        } else {
            char buf[64];
            for (int v = 1; v < nv; ++v) {
                std::snprintf(buf, sizeof buf, "%s%d-%d:%d", v == 1 ? "" : " ", par[v], v, dep[v] - dep[par[v]]);
                s += buf;
            }
            s += "  depths:";
            for (int v = 0; v < nv; ++v) { std::snprintf(buf, sizeof buf, " %d", dep[v]); s += buf; }
        }
        witnesses.push_back(s);
    }
}

int offbuf[MAXV];

void dfs(int v) {
    if (aborted) return;
    if (v == nv) {
        if (fe_active && (haveW1 == 0 || haveW2 == 0)) return;
        report_solution();
        return;
    }
    const int D = dep[v - 1];
    const int k = nv - v;                        // unplaced, v included
    const long long unpl_pairs = (long long)k * (k - 1) / 2;

    // ---- depth range, independent of the parent ----
    int lo = D + 1, hi = Vmax;
    bool depthFixed = false;
    if (nf) {
        if (v >= nf_r) { lo = hi = nf_B + (v - nf_r); depthFixed = true; }
        else hi = std::min(hi, nf_B - 2 - (nf_r - 1 - v));   // [P4]+[P8] room for later low depths, and l <= B-2
    } else {
        hi = std::min(hi, Vmax - (nv - 1 - v));              // [P4]
        if (symmode == 1 && v == 1) { lo = hi = 1; depthFixed = true; }
        if (symmode == 2) {
            if (v == nv - 1) { lo = hi = N; depthFixed = true; }
            if (subdiam > 0) {
                int mlim = (n - 1) - (N - subdiam);
                if (v <= mlim) hi = std::min(hi, subdiam - 1);
            }
        }
    }
    if (!depthFixed) {
        // [P5].  In normal-form mode the holes s+l of the not-yet-chosen low depths are
        // still counted as "free" here, so the free set over-counts the values that really
        // have to be realised; add that slack or the prune would be unsound (too strong).
        int slack = (nf && v < nf_r) ? (nf_r - v) : 0;
        int q = kthFree(unpl_pairs + slack + 1);
        if (D + q < hi) hi = D + q;
    }
    if (lo <= D || lo > hi) return;
    if (use_hall && !hallOK(v, lo)) return;

    for (int p = 0; p < v; ++p) {
        if (!nf && symmode == 2) {
            if (v >= 2 && p == 0) continue;                  // root is a leaf
        }
        // offsets + [P1] distinctness + [P2] ceiling
        ++stampGen;
        int G = 0;
        bool ok = true;
        for (int u = 0; u < v; ++u) {
            int l = (u == p) ? dep[p] : lcad[p][u];
            int o = dep[u] - 2 * l;
            offbuf[u] = o;
            int idx = o + MAXVAL;
            if (stampOff[idx] == stampGen) { ok = false; break; }
            stampOff[idx] = stampGen;
            if (o > G) G = o;
        }
        if (!ok) continue;
        int cap = hi;
        if (Vmax - G < cap) cap = Vmax - G;                  // [P2]
        int t2 = dep[p] + Vmax - wmaxAt[v - 1];              // [P3]
        if (t2 < cap) cap = t2;
        if (cap < lo) continue;

        for (int d = bsNext(lo); d <= cap; d = bsNext(d + 1)) {
            // bsNext already guarantees allowedv[d] && !usedv[d]  (u = root gives off = 0)
            bool good = true;
            for (int u = 1; u < v; ++u) {
                int val = d + offbuf[u];
                if (usedv[val] || !allowedv[val]) { good = false; break; }
            }
            if (!good) continue;
            // ---- place ----
            int w = d - dep[p];
            dep[v] = d; par[v] = p; lcad[v][v] = d;
            for (int u = 0; u < v; ++u) {
                int l = (u == p) ? dep[p] : lcad[p][u];
                lcad[v][u] = lcad[u][v] = l;
                int val = d + offbuf[u];
                usedv[val] = true; bsClear(val);
            }
            wmaxAt[v] = std::max(wmaxAt[v - 1], w);
            nHoleUndo[v] = 0;
            bool holeOK = true;
            if (nf && v < nf_r) {                            // new low depth -> new hole s+l
                int hval = nf_s + d;
                if (hval <= Vmax) {
                    if (usedv[hval]) holeOK = false;
                    else if (allowedv[hval]) { allowedv[hval] = false; bsClear(hval); holeUndo[v][nHoleUndo[v]++] = hval; }
                }
            }
            if (holeOK && fe_active) {
                if (w == 1) ++haveW1;
                if (w == 2) ++haveW2;
                if (haveW1 == 0 && !weightStillPossible(v + 1, 1)) holeOK = false;
                if (holeOK && haveW2 == 0 && !weightStillPossible(v + 1, 2)) holeOK = false;
            }
            if (holeOK) {
                ++nodes;
                ++levelNodes[v];
                if (nodeLimit >= 0 && nodes > nodeLimit) aborted = true;
                if (!aborted) {
                    if (v == splitLevel) {
                        long long c = splitCounter++;
                        if (c % splitN == splitK) dfs(v + 1);
                    } else dfs(v + 1);
                }
            }
            if (fe_active) { if (w == 1) --haveW1; if (w == 2) --haveW2; }
            for (int i = 0; i < nHoleUndo[v]; ++i) { allowedv[holeUndo[v][i]] = true; bsSet(holeUndo[v][i]); }
            for (int u = 0; u < v; ++u) { int val = d + offbuf[u]; usedv[val] = false; bsSet(val); }
            if (aborted) return;
        }
    }
}

void setupTarget() {
    std::memset(allowedv, 0, sizeof allowedv);
    std::memset(usedv, 0, sizeof usedv);
    std::memset(freeBS, 0, sizeof freeBS);
    for (int t = 1; t <= Vmax; ++t) { allowedv[t] = true; bsSet(t); }
    if (nf) {
        // the hole s + 0 = s (root depth 0 is in L)
        if (nf_s <= Vmax) { allowedv[nf_s] = false; bsClear(nf_s); }
    }
}

long long runOnce() {
    nodes = 1; nsol = 0; aborted = false; splitCounter = 0;
    // f_1 = 1 and f_2 = 2 hold for every L exactly when every hole s+l is >= 3, i.e. s >= 3.
    fe_active = force_edges && nf && nf_s >= 3;
    haveW1 = haveW2 = 0;
    witnesses.clear();
    std::memset(levelNodes, 0, sizeof levelNodes);
    levelNodes[0] = 1;
    setupTarget();
    dep[0] = 0; par[0] = -1; lcad[0][0] = 0; wmaxAt[0] = 0;
    dfs(1);
    return nsol;
}

void printLevels() {
    std::printf("LEVELS");
    for (int v = 0; v < nv; ++v) std::printf(" %lld", levelNodes[v]);
    std::printf("\n");
}

}  // namespace

int main(int argc, char** argv) {
    bool levelsFlag = false, allS = false;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        auto next = [&]() { return std::atoi(argv[++i]); };
        if (a == "--order") n = next();
        else if (a == "--sym") { std::string s = argv[++i]; symmode = (s == "none") ? 0 : (s == "w1") ? 1 : 2; }
        else if (a == "--sub-diam") subdiam = next();
        else if (a == "--nf") nf = true;
        else if (a == "--r") nf_r = next();
        else if (a == "--s") nf_s = next();
        else if (a == "--all-s") allS = true;
        else if (a == "--hall") use_hall = true;
        else if (a == "--hall-max") hall_max = next();
        else if (a == "--force-edges") force_edges = true;
        else if (a == "--nodes-limit") nodeLimit = std::atoll(argv[++i]);
        else if (a == "--split") { splitLevel = next(); splitK = next(); splitN = next(); }
        else if (a == "--levels") levelsFlag = true;
        else if (a == "--quiet") { quiet = true; print_witness = false; }
        else if (a == "--no-witness") print_witness = false;
        else if (a == "--verify") verify = true;
        else { std::fprintf(stderr, "unknown arg %s\n", a.c_str()); return 2; }
    }
    N = n * (n - 1) / 2;
    if (n < 2 || n >= MAXV) { std::fprintf(stderr, "bad order\n"); return 2; }

    auto runReport = [&](int s) {
        if (nf) {
            int kk = n - 1;
            nf_m = kk - nf_r;
            nf_s = s;
            nf_delta = kk * (kk - 1) / 2 + nf_r;
            nf_A = N - s;
            nf_B = nf_A - nf_m + 1;
            nv = kk;
            Vmax = nf_delta;
            if (nf_m < 1 || nf_r < 1 || nf_B < 1) return false;
            if (nf_s + nf_B != nf_delta + 1 || nf_s + nf_A != N) {
                std::fprintf(stderr, "top-block identity violated (r=%d s=%d)\n", nf_r, s); std::exit(3);
            }
            if (nf_B - 2 < nf_r - 1) return false;   // not enough room for r distinct low depths <= B-2
        } else {
            nv = n; Vmax = N;
        }
        auto t0 = std::chrono::steady_clock::now();
        long long sols = runOnce();
        double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
        if (!quiet) for (const auto& w : witnesses) std::printf("SOL %s\n", w.c_str());
        if (nf)
            std::printf("RESULT order=%d nf r=%d s=%d m=%d delta=%d A=%d B=%d sols=%lld nodes=%lld secs=%.3f%s\n",
                        n, nf_r, s, nf_m, nf_delta, nf_A, nf_B, sols, nodes, secs, aborted ? " ABORTED" : "");
        else {
            char sd[32] = "";
            if (subdiam) std::snprintf(sd, sizeof sd, " subdiam=%d", subdiam);
            std::printf("RESULT order=%d sym=%s%s sols=%lld nodes=%lld secs=%.3f%s\n", n,
                        symmode == 0 ? "none" : symmode == 1 ? "w1" : "diam", sd,
                        sols, nodes, secs, aborted ? " ABORTED" : "");
        }
        if (levelsFlag) printLevels();
        return true;
    };

    if (nf && allS) {
        int kk = n - 1, m = kk - nf_r;
        for (int s = 1; s <= N - m; ++s) runReport(s);
    } else {
        runReport(nf_s);
    }
    return 0;
}
