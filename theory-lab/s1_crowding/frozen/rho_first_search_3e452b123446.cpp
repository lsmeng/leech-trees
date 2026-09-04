// rho-first exhaustive search for the singleton-final-cap normal form.
//
// Same model as abstract_class_search.cpp / s1_direct_search.cpp:
//   order n, N = C(n,2), K on k = n-1 vertices, r low vertices (depths L,
//   l_0 = 0, low tree lowpar[i] < i), m = k - r high vertices h_y at depth
//   B + y, delta = C(k,2) + r, B = delta + 1 - s, F = [1,delta] \ (s+L).
//
// Decomposition.  Let rho(y) be the low vertex at which the high component
// of h_y hangs.  Every pair value except those inside a fiber rho^{-1}(i)
// is determined by (s, L, rho):
//   x-h:            B + y
//   low-high:       B + y - l_i        if i is an ancestor-or-equal of rho(y)
//                   B + y + l_i - 2 l_a  otherwise, a = lowlca(i, rho(y))
//   low-low:        l_i + l_j - 2 l_lca
//   holes:          s + l_i
//   cross-fibre HH: 2B - 2 l_c + (y+y'),  c = lowlca(rho(y), rho(y')),  rho(y) != rho(y')
// Same-fibre pairs are either within one high component (value y+y'-2q) or
// cross-component with LCA rho(y) (value 2B - 2 l_rho + (y+y')).
//
// Phase 1 enumerates rho (pruned by cross-fibre sum injectivity per class),
// then solves the rho-level (s, L) CSP.  Only if that CSP has survivors does
// phase 2 enumerate the internal forest structure of every fibre (pruned by
// within-distance injectivity and class sum injectivity) and check the
// remaining values against every rho-level survivor.  A full survivor is a
// genuine tree of the normal form.
//
// Usage: rho_first_search --order 25 --m 16 --lowpar 0,1,2,3,4,5,6 [--relaxed V] [--fix-s S]
//        [--split LEVEL K N] [--max-witness W] [--nodes-limit X]
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

namespace {

constexpr int MAXH = 24;
constexpr int MAXR = 24;
constexpr int MAXV = 4096;

int order_n = 25, M = 16, R = 8;
int lowpar[MAXR], lowlca[MAXR][MAXR];
bool low_anc[MAXR][MAXR];
int relaxed_vmax = 0, fix_s = 0, max_witness = 20;
int split_level = -1, split_k = 0, split_n = 1;
uint64_t split_counter = 0, nodes_limit = 0;
bool aborted = false;

int N, K, DELTA;

// phase-1 state
int rho[MAXH];
int fibre_size[MAXR];
uint64_t class_used[MAXR];       // cross-fibre sums per class
bool fibre_prune = true;

// Sound phase-1 prune (top-block crowding restricted to same-fibre pairs):
// every same-fibre pair of fibre i is either a within-component pair (value in
// [1,2m-3], all such values distinct over all fibres) or a class-i pair whose
// sum is distinct from the cross-fibre sums already in class i.  Hence
//   sum_i C(n_i,2) <= (2m-3) + sum_i (2m-3 - popcount(class_used[i])).
// Fibre sizes and class_used only grow along the DFS, so checking the
// inequality at every node is a valid necessary condition.
inline bool fibre_bound_ok() {
    int cap = 2 * M - 3;
    long lhs = 0, rhs = cap;
    for (int i = 0; i < R; ++i) {
        lhs += (long)fibre_size[i] * (fibre_size[i] - 1) / 2;
        rhs += cap - __builtin_popcountll(class_used[i]);
    }
    return lhs <= rhs;
}
uint64_t p1_nodes = 0, complete_rho = 0, rho_with_survivor = 0, rho_level_survivors = 0;
uint64_t p2_nodes = 0, p2_leaves = 0, full_survivors = 0, csp_nodes = 0;

// rho-level CSP
int csp_l[MAXR];
int csp_s, csp_B;
unsigned char used[MAXV];
std::vector<int> cross_sums[MAXR];        // cross-fibre sums per class for current rho
struct SL { int s; int l[MAXR]; };
std::vector<SL> survivors;                // rho-level survivors for current rho
constexpr size_t MAX_SURV = 2000000;
bool surv_overflow = false;

inline int vmax() { return relaxed_vmax > 0 ? relaxed_vmax : DELTA; }

inline bool take(int v, std::vector<int>& taken) {
    if (v < 1 || v > vmax() || used[v]) return false;
    used[v] = 1; taken.push_back(v); return true;
}
inline void release(const std::vector<int>& taken) { for (int v : taken) used[v] = 0; }

void csp_dfs(int i) {
    ++csp_nodes;
    if (i == R) {
        SL x; x.s = csp_s; for (int j = 0; j < R; ++j) x.l[j] = csp_l[j];
        if (survivors.size() < MAX_SURV) survivors.push_back(x); else surv_overflow = true;
        return;
    }
    int lo = csp_l[lowpar[i]] + 1;
    for (int l = lo; l <= csp_B - 1; ++l) {
        bool dup = false;
        for (int j = 0; j < i; ++j) if (csp_l[j] == l) { dup = true; break; }
        if (dup) continue;
        csp_l[i] = l;
        std::vector<int> taken;
        bool ok = true;
        if (relaxed_vmax == 0 && l + csp_s <= DELTA) {
            if (used[csp_s + l]) ok = false; else { used[csp_s + l] = 1; taken.push_back(csp_s + l); }
        }
        for (int j = 0; j < i && ok; ++j) {
            int a = lowlca[i][j];
            if (!take(l + csp_l[j] - 2 * csp_l[a], taken)) ok = false;
        }
        for (int y = 0; y < M && ok; ++y) {
            int rt = rho[y];
            int d = low_anc[i][rt] ? (csp_B + y - l) : (csp_B + y + l - 2 * csp_l[lowlca[i][rt]]);
            if (!take(d, taken)) ok = false;
        }
        for (int sm : cross_sums[i]) { if (!ok) break; if (!take(2 * csp_B - 2 * l + sm, taken)) ok = false; }
        if (ok) csp_dfs(i + 1);
        release(taken);
    }
}

// rebuild the used set of one rho-level survivor (for phase-2 checks)
void rebuild_used(const SL& x) {
    std::memset(used, 0, sizeof(used));
    int s = x.s, B = DELTA + 1 - s;
    if (relaxed_vmax == 0) { used[s] = 1; for (int i = 1; i < R; ++i) if (s + x.l[i] <= DELTA) used[s + x.l[i]] = 1; }
    for (int y = 0; y < M; ++y) used[B + y] = 1;
    for (int i = 0; i < R; ++i) for (int sm : cross_sums[i]) used[2 * B - 2 * x.l[i] + sm] = 1;
    for (int i = 1; i < R; ++i) {
        for (int j = 0; j < i; ++j) used[x.l[i] + x.l[j] - 2 * x.l[lowlca[i][j]]] = 1;
        for (int y = 0; y < M; ++y) {
            int rt = rho[y];
            int d = low_anc[i][rt] ? (B + y - x.l[i]) : (B + y + x.l[i] - 2 * x.l[lowlca[i][rt]]);
            used[d] = 1;
        }
    }
}

// phase-2 state
int hpar[MAXH], hcomp[MAXH], hlca[MAXH][MAXH];
uint64_t within_used;
uint64_t class_used2[MAXR];
std::vector<int> within_vals, samefibre_sums[MAXR];
int ncomp;

void report_full(const SL& x) {
    ++full_survivors;
    if (full_survivors <= (uint64_t)max_witness) {
        std::printf("FULL_SURVIVOR s=%d L=", x.s);
        for (int j = 0; j < R; ++j) std::printf("%s%d", j ? "," : "", x.l[j]);
        std::printf(" lowpar=");
        for (int j = 1; j < R; ++j) std::printf("%s%d", j > 1 ? "," : "", lowpar[j]);
        std::printf(" rho=");
        for (int y = 0; y < M; ++y) std::printf("%s%d", y ? "," : "", rho[y]);
        std::printf(" hpar=");
        for (int y = 0; y < M; ++y) std::printf("%s%d", y ? "," : "", hpar[y]);
        std::printf("\n");
        std::fflush(stdout);
    }
}

void phase2_leaf() {
    ++p2_leaves;
    // collect within values and same-fibre cross-component sums
    within_vals.clear();
    for (int i = 0; i < R; ++i) samefibre_sums[i].clear();
    for (int y = 0; y < M; ++y)
        for (int yy = 0; yy < y; ++yy) {
            if (rho[y] != rho[yy]) continue;
            if (hcomp[y] == hcomp[yy]) within_vals.push_back(y + yy - 2 * hlca[y][yy]);
            else samefibre_sums[rho[y]].push_back(y + yy);
        }
    for (const SL& x : survivors) {
        rebuild_used(x);
        int B = DELTA + 1 - x.s;
        bool ok = true;
        std::vector<int> taken;
        for (int d : within_vals) if (!take(d, taken)) { ok = false; break; }
        for (int i = 0; i < R && ok; ++i)
            for (int sm : samefibre_sums[i]) { if (!take(2 * B - 2 * x.l[i] + sm, taken)) { ok = false; break; } }
        if (ok) report_full(x);
    }
}

void phase2_dfs(int y) {
    ++p2_nodes;
    if (nodes_limit && p1_nodes + p2_nodes > nodes_limit) { aborted = true; return; }
    if (y == M) { phase2_leaf(); return; }
    int c = rho[y];
    // (a) new component rooted at low vertex c: pairs with earlier same-fibre vertices are class-c cross-component
    {
        uint64_t add = 0; bool ok = true;
        for (int yy = 0; yy < y && ok; ++yy) {
            if (rho[yy] != c) continue;
            uint64_t bit = 1ULL << (y + yy);
            if ((class_used2[c] | add) & bit) ok = false; else add |= bit;
        }
        if (ok) {
            hpar[y] = -1; hcomp[y] = ncomp++;
            class_used2[c] |= add;
            phase2_dfs(y + 1);
            class_used2[c] &= ~add;
            --ncomp;
            if (aborted) return;
        }
    }
    // (b) child of an earlier same-fibre vertex p
    for (int p = 0; p < y; ++p) {
        if (rho[p] != c) continue;
        uint64_t add = 0, addw = 0; bool ok = true;
        for (int yy = 0; yy < y && ok; ++yy) {
            if (rho[yy] != c) continue;
            if (hcomp[yy] == hcomp[p]) {
                int q = (yy == p) ? p : hlca[p][yy];
                hlca[y][yy] = hlca[yy][y] = q;
                uint64_t bit = 1ULL << (y + yy - 2 * q);
                if ((within_used | addw) & bit) ok = false; else addw |= bit;
            } else {
                uint64_t bit = 1ULL << (y + yy);
                if ((class_used2[c] | add) & bit) ok = false; else add |= bit;
            }
        }
        if (!ok) continue;
        hpar[y] = p; hcomp[y] = hcomp[p];
        within_used |= addw; class_used2[c] |= add;
        phase2_dfs(y + 1);
        within_used &= ~addw; class_used2[c] &= ~add;
        if (aborted) return;
    }
}

void solve_rho() {
    ++complete_rho;
    for (int i = 0; i < R; ++i) cross_sums[i].clear();
    for (int y = 0; y < M; ++y)
        for (int yy = 0; yy < y; ++yy)
            if (rho[y] != rho[yy]) cross_sums[lowlca[rho[y]][rho[yy]]].push_back(y + yy);
    survivors.clear(); surv_overflow = false;
    for (int s = 1; s <= N; ++s) {
        if (fix_s > 0 && s != fix_s) continue;
        int B = DELTA + 1 - s;
        if (B < R) break;
        csp_s = s; csp_B = B;
        std::memset(used, 0, sizeof(used));
        std::vector<int> taken; bool ok = true;
        if (relaxed_vmax == 0 && s <= DELTA) { used[s] = 1; taken.push_back(s); }
        for (int sm : cross_sums[0]) { if (!ok) break; if (!take(2 * B + sm, taken)) ok = false; }
        for (int y = 0; y < M && ok; ++y) if (!take(B + y, taken)) ok = false;
        csp_l[0] = 0;
        if (ok) csp_dfs(1);
        release(taken);
    }
    if (surv_overflow) { std::printf("RHO_SURVIVOR_OVERFLOW\n"); std::exit(5); }
    if (survivors.empty()) return;
    ++rho_with_survivor;
    rho_level_survivors += survivors.size();
    // phase 2 for this rho
    within_used = 0; ncomp = 0;
    for (int i = 0; i < R; ++i) class_used2[i] = class_used[i];
    phase2_dfs(0);
}

void phase1_dfs(int y) {
    ++p1_nodes;
    if (nodes_limit && p1_nodes + p2_nodes > nodes_limit) { aborted = true; return; }
    if (y == split_level) { uint64_t c = split_counter++; if (c % split_n != (uint64_t)split_k) return; }
    if (y == M) { solve_rho(); return; }
    for (int i = 0; i < R; ++i) {
        uint64_t add[MAXR]; std::memset(add, 0, sizeof(add));
        bool ok = true;
        for (int yy = 0; yy < y && ok; ++yy) {
            if (rho[yy] == i) continue;                 // same fibre: deferred to phase 2
            int c = lowlca[i][rho[yy]];
            uint64_t bit = 1ULL << (y + yy);
            if ((class_used[c] | add[c]) & bit) ok = false; else add[c] |= bit;
        }
        if (!ok) continue;
        rho[y] = i;
        for (int c = 0; c < R; ++c) class_used[c] |= add[c];
        ++fibre_size[i];
        if (!fibre_prune || fibre_bound_ok()) phase1_dfs(y + 1);
        --fibre_size[i];
        for (int c = 0; c < R; ++c) class_used[c] &= ~add[c];
        if (aborted) return;
    }
}

std::vector<int> parse_list(const char* s) {
    std::vector<int> out; std::string cur;
    for (const char* p = s;; ++p) {
        if (*p == ',' || *p == 0) { if (!cur.empty()) out.push_back(std::atoi(cur.c_str())); cur.clear(); if (!*p) break; }
        else cur += *p;
    }
    return out;
}

} // namespace

int main(int argc, char** argv) {
    std::vector<int> lp; bool have_lp = false;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        auto next = [&]() -> const char* { if (i + 1 >= argc) std::exit(2); return argv[++i]; };
        if (a == "--order") order_n = std::atoi(next());
        else if (a == "--m") M = std::atoi(next());
        else if (a == "--lowpar") { lp = parse_list(next()); have_lp = true; }
        else if (a == "--relaxed") relaxed_vmax = std::atoi(next());
        else if (a == "--fix-s") fix_s = std::atoi(next());
        else if (a == "--max-witness") max_witness = std::atoi(next());
        else if (a == "--split") { split_level = std::atoi(next()); split_k = std::atoi(next()); split_n = std::atoi(next()); }
        else if (a == "--nodes-limit") nodes_limit = std::strtoull(next(), nullptr, 10);
        else if (a == "--no-fibre-prune") fibre_prune = false;
        else { std::fprintf(stderr, "unknown arg %s\n", a.c_str()); return 2; }
    }
    if (!have_lp) { std::fprintf(stderr, "--lowpar required (empty string for r=1)\n"); return 2; }
    R = (int)lp.size() + 1;
    if (M < 1 || M > MAXH || R > MAXR) return 2;
    lowpar[0] = -1;
    for (int i = 1; i < R; ++i) { lowpar[i] = lp[i - 1]; if (lowpar[i] < 0 || lowpar[i] >= i) return 2; }
    K = order_n - 1; N = order_n * (order_n - 1) / 2; DELTA = K * (K - 1) / 2 + R;
    if (K != R + M) { std::fprintf(stderr, "r + m must equal order-1\n"); return 2; }
    int dep[MAXR]; dep[0] = 0;
    for (int i = 1; i < R; ++i) dep[i] = dep[lowpar[i]] + 1;
    for (int a = 0; a < R; ++a) for (int b = 0; b < R; ++b) {
        int u = a, v = b;
        while (u != v) { if (dep[u] >= dep[v]) u = lowpar[u]; else v = lowpar[v]; }
        lowlca[a][b] = u; low_anc[a][b] = (u == a);
    }
    std::memset(class_used, 0, sizeof(class_used));
    std::memset(fibre_size, 0, sizeof(fibre_size));
    phase1_dfs(0);
    std::printf("RHO_FIRST order=%d m=%d r=%d lowpar=", order_n, M, R);
    for (int i = 1; i < R; ++i) std::printf("%s%d", i > 1 ? "," : "", lowpar[i]);
    std::printf(" split=%d:%d/%d p1_nodes=%llu complete_rho=%llu rho_with_survivor=%llu rho_level_survivors=%llu csp_nodes=%llu p2_nodes=%llu p2_leaves=%llu full_survivors=%llu %s\n",
                split_level, split_k, split_n, (unsigned long long)p1_nodes, (unsigned long long)complete_rho,
                (unsigned long long)rho_with_survivor, (unsigned long long)rho_level_survivors, (unsigned long long)csp_nodes,
                (unsigned long long)p2_nodes, (unsigned long long)p2_leaves, (unsigned long long)full_survivors,
                aborted ? "ABORTED" : "EXHAUSTED");
    return 0;
}
