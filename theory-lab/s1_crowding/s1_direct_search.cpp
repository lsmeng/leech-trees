// Direct exhaustive search for the singleton-final-cap normal form of an
// order-n Leech tree (default n=25, N=300).
//
// Model.  Delete the heaviest edge (weight s) whose detached side is a single
// leaf.  K = remaining tree on k=n-1 vertices, rooted at the bridge endpoint
// x.  D = rooted depths (k distinct values, 0 in D), F = Spec(K),
// F disjoint-union (s+D) = [1,N].  With delta = max F = C(k,2)+r the top
// block lemma gives D = L u [B,A], |L| = r, A = N-s, B = A-m+1, m = k-r.
//
// Vertices: low 0..r-1 with depths L (L[0]=0 is the root x) and a given
// rooted low tree (lowpar[i] < i); high vertex y (0<=y<m) has depth B+y and
// index r+y.  A candidate tree is a parent function on the high vertices:
// parent(h_y) is a low vertex or an earlier high vertex h_p (p<y).  The
// search enumerates every such parent function whose 276 pairwise distances
// are pairwise distinct and lie in F = [1,delta] \ (s+L).  Nothing else is
// assumed: no core gate, no component-count bound, no weight alphabet.
//
// Modes:
//   --order n --r r --s s --L l1,...,l_{r-1} --lowpar p1,...,p_{r-1}
//        single instance (lowpar[i] is the index of the parent of low vertex i)
//   --r 3 --s s --shape chain|star --all-d      all even 0<d1<d2<B (or --all-d-any for any parity)
//   --plant SEED                                 planted positive control:
//        random high forest for the given low data; its own distance set
//        becomes the target (must be all distinct); the search must find >=1.
//   --nodes-limit X                              abort an instance after X nodes (reported as UNKNOWN)
//
// Output: one line per instance: params, survivors, nodes, status.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <random>
#include <string>
#include <vector>

namespace {

constexpr int MAXK = 64;
constexpr int MAXVAL = 4096;

struct Instance {
    int n = 25;      // order
    int k = 24;      // |K|
    int N = 300;     // C(n,2)
    int r = 3;       // |L|
    int m = 21;      // high block size
    int s = 0;       // bridge weight
    int A = 0, B = 0, delta = 0;
    std::vector<int> L;       // low depths, L[0] = 0
    std::vector<int> lowpar;  // lowpar[0] = -1
    std::vector<int> hdep;    // high depths, default B+y (consecutive top block)
};

struct Search {
    const Instance& I;
    int nv;                         // r + m
    int depth[MAXK];
    int parent[MAXK];
    int lcad[MAXK][MAXK];           // depth of LCA for placed vertices
    bool allowed[MAXVAL];           // target set membership
    bool used[MAXVAL];
    uint64_t nodes = 0;
    uint64_t level_nodes[MAXK] = {0};
    uint64_t survivors = 0;
    uint64_t nodes_limit = 0;
    bool aborted = false;
    bool print_witness = false;

    explicit Search(const Instance& inst) : I(inst) {
        nv = I.r + I.m;
        std::memset(lcad, 0, sizeof(lcad));
        std::memset(allowed, 0, sizeof(allowed));
        std::memset(used, 0, sizeof(used));
    }

    // distance between placed vertices a,b via LCA depths
    int dist(int a, int b) const { return depth[a] + depth[b] - 2 * lcad[a][b]; }

    bool place_low() {
        // low vertices are given; check pairwise low-low distances
        for (int i = 0; i < I.r; ++i) {
            depth[i] = I.L[i];
            parent[i] = I.lowpar[i];
        }
        for (int i = 0; i < I.r; ++i) lcad[i][i] = depth[i];
        for (int i = 1; i < I.r; ++i) {
            int p = parent[i];
            for (int j = 0; j < i; ++j) {
                int l = (j == p) ? depth[p] : lcad[p][j];
                lcad[i][j] = lcad[j][i] = l;
                int d = dist(i, j);
                if (d <= 0 || d >= MAXVAL || !allowed[d] || used[d]) return false;
                used[d] = true;
            }
        }
        return true;
    }

    void dfs(int y) {
        if (aborted) return;
        ++nodes;
        if (nodes_limit && nodes > nodes_limit) { aborted = true; return; }
        if (y == I.m) {
            ++survivors;
            if (print_witness) {
                std::printf("WITNESS");
                for (int v = I.r; v < nv; ++v) std::printf(" %d", parent[v]);
                std::printf("\n");
            }
            return;
        }
        int v = I.r + y;
        depth[v] = I.hdep[y];
        lcad[v][v] = depth[v];
        ++level_nodes[y];
        // candidate parents: all low vertices, all earlier high vertices
        for (int p = 0; p < v; ++p) {
            parent[v] = p;
            // compute distances to all placed vertices u < v
            int added[MAXK];
            int na = 0;
            bool ok = true;
            for (int u = 0; u < v; ++u) {
                int l = (u == p) ? depth[p] : lcad[p][u];
                lcad[v][u] = lcad[u][v] = l;
                int d = depth[v] + depth[u] - 2 * l;
                if (d <= 0 || d >= MAXVAL || !allowed[d] || used[d]) { ok = false; break; }
                used[d] = true;
                added[na++] = d;
            }
            if (ok) dfs(y + 1);
            for (int i = 0; i < na; ++i) used[added[i]] = false;
            if (aborted) return;
        }
    }
};

Instance make_instance(int n, int r, int s, const std::vector<int>& L, const std::vector<int>& lowpar) {
    Instance I;
    I.n = n; I.k = n - 1; I.N = n * (n - 1) / 2; I.r = r; I.m = I.k - r; I.s = s;
    I.A = I.N - s; I.B = I.A - I.m + 1; I.delta = I.k * (I.k - 1) / 2 + r;
    I.L = L; I.lowpar = lowpar;
    I.hdep.resize(I.m);
    for (int y = 0; y < I.m; ++y) I.hdep[y] = I.B + y;
    return I;
}

// returns false if the instance is structurally invalid (depths not distinct/ordered etc.)
bool valid_instance(const Instance& I) {
    if (I.r < 1 || I.m < 1 || I.B < 1) return false;
    if ((int)I.L.size() != I.r || I.L[0] != 0) return false;
    for (int i = 1; i < I.r; ++i) {
        if (I.L[i] <= I.L[i - 1] || I.L[i] >= I.B) return false;    // distinct increasing, below block
        if (I.lowpar[i] < 0 || I.lowpar[i] >= i) return false;       // parent shallower
    }
    return true;
}

int g_relaxed_vmax = 0;   // >0: relaxed differential-test target [1,vmax], no holes
void set_target_normal_form(Search& S) {
    // F = [1,delta] \ (s+L)
    const Instance& I = S.I;
    if (g_relaxed_vmax > 0) { for (int v = 1; v <= g_relaxed_vmax && v < MAXVAL; ++v) S.allowed[v] = true; return; }
    for (int v = 1; v <= I.delta && v < MAXVAL; ++v) S.allowed[v] = true;
    for (int l : I.L) if (I.s + l < MAXVAL) S.allowed[I.s + l] = false;
}

struct Result { uint64_t survivors, nodes; bool aborted; bool prefail; };

Result run_instance(const Instance& I, uint64_t nodes_limit, bool witness, bool levels = false) {
    Search S(I);
    set_target_normal_form(S);
    S.nodes_limit = nodes_limit;
    S.print_witness = witness;
    if (!S.place_low()) return {0, 0, false, true};
    // sanity: the bridge-to-high values s+[B,A] must be exactly (delta,N]
    if (I.s + I.B != I.delta + 1 || I.s + I.A != I.N) { std::fprintf(stderr, "top-block identity violated\n"); std::exit(3); }
    S.dfs(0);
    if (levels) {
        std::printf("LEVELS");
        for (int y = 0; y < I.m; ++y) std::printf(" %llu", (unsigned long long)S.level_nodes[y]);
        std::printf("\n");
    }
    return {S.survivors, S.nodes, S.aborted, false};
}

// Planted control: random high forest; its own distance set is the target.
Result run_planted(const Instance& I0, unsigned seed, uint64_t nodes_limit, int gap) {
    std::mt19937_64 rng(seed);
    for (int attempt = 0; attempt < 100000; ++attempt) {
        Instance I = I0;
        if (gap > 1) {  // spread the high depths so that a random tree can be distance-injective
            int d = I.B;
            for (int y = 0; y < I.m; ++y) { I.hdep[y] = d; d += 1 + (int)(rng() % gap); }
        }
        Search S(I);
        // random parent function
        std::vector<int> par(I.r + I.m, -1);
        for (int i = 0; i < I.r; ++i) par[i] = I.lowpar[i];
        for (int y = 0; y < I.m; ++y) par[I.r + y] = (int)(rng() % (I.r + y));
        // depths
        std::vector<int> dep(I.r + I.m);
        for (int i = 0; i < I.r; ++i) dep[i] = I.L[i];
        for (int y = 0; y < I.m; ++y) dep[I.r + y] = I.hdep[y];
        // all-pairs distances by explicit ancestor walk (independent of lcad logic)
        auto lca_depth = [&](int a, int b) {
            std::vector<char> anc(I.r + I.m, 0);
            for (int v = a; v != -1; v = par[v]) anc[v] = 1;
            int v = b;
            while (!anc[v]) v = par[v];
            return dep[v];
        };
        std::vector<int> vals;
        bool distinct = true;
        std::vector<char> seen(MAXVAL, 0);
        for (int a = 0; a < I.r + I.m && distinct; ++a)
            for (int b = a + 1; b < I.r + I.m; ++b) {
                int d = dep[a] + dep[b] - 2 * lca_depth(a, b);
                if (d <= 0 || d >= MAXVAL || seen[d]) { distinct = false; break; }
                seen[d] = 1; vals.push_back(d);
            }
        if (!distinct) continue;
        for (int d : vals) S.allowed[d] = true;
        S.nodes_limit = nodes_limit;
        if (!S.place_low()) { std::fprintf(stderr, "planted low placement failed\n"); std::exit(4); }
        S.dfs(0);
        std::printf("PLANTED seed=%u attempts=%d distinct_target=%zu survivors=%llu nodes=%llu %s\n",
                    seed, attempt + 1, vals.size(), (unsigned long long)S.survivors,
                    (unsigned long long)S.nodes, S.aborted ? "ABORTED" : (S.survivors >= 1 ? "FOUND_PLANTED" : "MISSED_PLANTED"));
        return {S.survivors, S.nodes, S.aborted, false};
    }
    std::printf("PLANTED seed=%u: no distance-injective random tree found\n", seed);
    return {0, 0, false, true};
}

std::vector<int> parse_list(const char* s) {
    std::vector<int> out;
    std::string cur;
    for (const char* p = s; ; ++p) {
        if (*p == ',' || *p == 0) { if (!cur.empty()) out.push_back(std::atoi(cur.c_str())); cur.clear(); if (!*p) break; }
        else cur += *p;
    }
    return out;
}

} // namespace

int main(int argc, char** argv) {
    int n = 25, r = 3, s = -1;
    std::vector<int> L, lowpar;
    std::string shape;
    bool all_d = false, all_d_any = false, witness = false, all_L = false;
    long plant = -1;
    int gap = 1;
    bool levels = false;
    uint64_t nodes_limit = 0;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        auto next = [&]() -> const char* { if (i + 1 >= argc) { std::fprintf(stderr, "missing value for %s\n", a.c_str()); std::exit(2); } return argv[++i]; };
        if (a == "--order") n = std::atoi(next());
        else if (a == "--r") r = std::atoi(next());
        else if (a == "--s") s = std::atoi(next());
        else if (a == "--L") L = parse_list(next());
        else if (a == "--lowpar") lowpar = parse_list(next());
        else if (a == "--shape") shape = next();
        else if (a == "--all-d") all_d = true;
        else if (a == "--all-d-any") { all_d = true; all_d_any = true; }
        else if (a == "--all-L") all_L = true;
        else if (a == "--plant") plant = std::atol(next());
        else if (a == "--gap") gap = std::atoi(next());
        else if (a == "--levels") levels = true;
        else if (a == "--nodes-limit") nodes_limit = std::strtoull(next(), nullptr, 10);
        else if (a == "--witness") witness = true;
        else if (a == "--relaxed") g_relaxed_vmax = std::atoi(next());
        else { std::fprintf(stderr, "unknown arg %s\n", a.c_str()); return 2; }
    }
    if (s < 0) { std::fprintf(stderr, "--s required\n"); return 2; }

    if (all_d) {
        if (r != 3 || shape.empty()) { std::fprintf(stderr, "--all-d needs --r 3 and --shape\n"); return 2; }
        std::vector<int> lp = (shape == "chain") ? std::vector<int>{-1, 0, 1} : std::vector<int>{-1, 0, 0};
        int k = n - 1, m = k - 3, N = n * (n - 1) / 2, A = N - s, B = A - m + 1;
        uint64_t tot_surv = 0, tot_nodes = 0; int inst = 0, prefail = 0, aborted = 0;
        int step = all_d_any ? 1 : 2;
        int start = all_d_any ? 1 : 2;
        for (int d1 = start; d1 < B; d1 += step)
            for (int d2 = d1 + step; d2 < B; d2 += step) {
                Instance I = make_instance(n, 3, s, {0, d1, d2}, lp);
                if (!valid_instance(I)) continue;
                Result R = run_instance(I, nodes_limit, witness);
                ++inst;
                if (R.prefail) { ++prefail; continue; }
                if (R.aborted) ++aborted;
                tot_surv += R.survivors; tot_nodes += R.nodes;
                if (R.survivors || R.aborted)
                    std::printf("INSTANCE n=%d r=3 s=%d shape=%s d1=%d d2=%d survivors=%llu nodes=%llu %s\n", n, s, shape.c_str(), d1, d2,
                                (unsigned long long)R.survivors, (unsigned long long)R.nodes, R.aborted ? "ABORTED" : "EXHAUSTED");
            }
        std::printf("SUMMARY n=%d r=3 s=%d shape=%s instances=%d low_prefail=%d aborted=%d survivors=%llu nodes=%llu %s\n",
                    n, s, shape.c_str(), inst, prefail, aborted, (unsigned long long)tot_surv, (unsigned long long)tot_nodes,
                    aborted ? "INCOMPLETE" : (tot_surv ? "SURVIVORS" : "EXHAUSTED_EMPTY"));
        return 0;
    }

    if (all_L) {
        // enumerate every strictly increasing L (l_i > l_{i-1}, any parity) for the given --lowpar
        std::vector<int> lp2 = {-1}; for (int v : lowpar) lp2.push_back(v);
        int k = n - 1, m = k - r, N = n * (n - 1) / 2, A = N - s, B = A - m + 1;
        uint64_t tot_surv = 0, tot_nodes = 0; int inst = 0, prefail = 0, aborted = 0;
        std::vector<int> Lv(r, 0);
        std::function<void(int)> rec = [&](int i) {
            if (i == r) {
                Instance I = make_instance(n, r, s, Lv, lp2);
                if (!valid_instance(I)) return;
                Result R = run_instance(I, nodes_limit, witness);
                ++inst; if (R.prefail) { ++prefail; return; }
                if (R.aborted) ++aborted;
                tot_surv += R.survivors; tot_nodes += R.nodes;
                return;
            }
            for (int l = Lv[i - 1] + 1; l < B; ++l) { Lv[i] = l; rec(i + 1); }
        };
        rec(1);
        std::printf("ALL_L_SUMMARY n=%d r=%d s=%d lowpar=", n, r, s);
        for (size_t i = 0; i < lowpar.size(); ++i) std::printf("%s%d", i ? "," : "", lowpar[i]);
        std::printf(" instances=%d low_prefail=%d aborted=%d survivors=%llu nodes=%llu\n", inst, prefail, aborted,
                    (unsigned long long)tot_surv, (unsigned long long)tot_nodes);
        return 0;
    }
    if ((int)L.size() != r - 1 && !(r == 3 && !shape.empty())) { std::fprintf(stderr, "--L needs r-1 values\n"); return 2; }
    std::vector<int> Lfull = {0}; for (int v : L) Lfull.push_back(v);
    std::vector<int> lp;
    if (!lowpar.empty()) { lp = {-1}; for (int v : lowpar) lp.push_back(v); }
    else if (r == 3 && shape == "chain") lp = {-1, 0, 1};
    else if (r == 3 && shape == "star") lp = {-1, 0, 0};
    else if (r == 1) lp = {-1};
    else if (r == 2) lp = {-1, 0};
    else { std::fprintf(stderr, "--lowpar required for r>=3 without --shape\n"); return 2; }
    Instance I = make_instance(n, r, s, Lfull, lp);
    if (!valid_instance(I)) { std::fprintf(stderr, "invalid instance\n"); return 2; }
    if (plant >= 0) { run_planted(I, (unsigned)plant, nodes_limit, gap); return 0; }
    Result R = run_instance(I, nodes_limit, witness, levels);
    std::printf("INSTANCE n=%d r=%d s=%d L=", n, r, s);
    for (size_t i = 0; i < Lfull.size(); ++i) std::printf("%s%d", i ? "," : "", Lfull[i]);
    std::printf(" lowpar=");
    for (size_t i = 1; i < lp.size(); ++i) std::printf("%s%d", i > 1 ? "," : "", lp[i]);
    std::printf(" B=%d A=%d delta=%d survivors=%llu nodes=%llu %s\n", I.B, I.A, I.delta,
                (unsigned long long)R.survivors, (unsigned long long)R.nodes,
                R.prefail ? "LOW_PREFAIL" : (R.aborted ? "ABORTED" : "EXHAUSTED"));
    return 0;
}
