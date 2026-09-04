// Abstract (depth-free) class-injectivity search for the singleton normal form.
//
// High vertices y=0..m-1 (depth B+y).  Low tree: r vertices, lowpar[i] < i,
// lowpar[0] = -1 (x).  A structure = parent(h_y) in {low i} u {h_p : p<y}.
// Every high-high pair falls into exactly one class:
//   * same high component, LCA h_q       : distance y+y'-2q            (class "within")
//   * different components, low LCA l_i  : distance 2B - 2 l_i + (y+y') (class i)
// Distance injectivity forces, inside each class, pairwise distinct
// within-distances / pairwise distinct sums.  These conditions do not involve
// the low depths, so the search below is exact and L-independent: if it has
// no complete structure for a given (m, low shape), no tree of the normal form
// exists for any low depths and any s.  Optional: --xcap S limits sums in the
// class of the root x to <= S (diameter cap 2B+sum <= delta).
//
// Usage: abstract_class_search --m 19 --lowpar 0,1,1,3 [--xcap 35] [--emit] [--nodes-limit X]
//        abstract_class_search --m 19 --r 5 --all-shapes [--xcap 35]
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <set>
#include <unordered_set>
#include <string>
#include <vector>

namespace {

constexpr int MAXH = 24;
constexpr int MAXR = 12;

int M, R;
int lowpar[MAXR];
int lowlca[MAXR][MAXR];
int xcap = 1000;
bool emit = false;
bool stop_first = false;
int split_level = -1, split_k = 0, split_n = 1;   // prefix sharding of the abstract DFS
uint64_t split_counter = 0;
uint64_t nodes = 0, nodes_limit = 0, leaves = 0;
bool aborted = false;

bool solve_depths = false;   // at each complete structure, search (s, L) for a full distance-injective tree
int order_n = 25;            // order of the target Leech tree (N = n(n-1)/2)
uint64_t depth_survivors = 0, depth_csp_nodes = 0, structures_with_survivor = 0;
int max_witness = 20;
int relaxed_vmax = 0;        // >0: relaxed differential-test target [1,relaxed_vmax], no holes
int fix_s = 0;               // >0: only this bridge weight s in the depth CSP
int rho_check_level = -1;    // legacy single level (kept for the summary line)
bool rho_check_at[MAXH + 1] = {false};   // levels at which the memoized rho-prefix CSP runs
std::unordered_set<std::string> dead_rho;   // memo of rho prefixes / full rho with no (s,L) survivor
uint64_t rho_csp_runs = 0, rho_memo_hits = 0, rho_prefix_prunes = 0, leaf_rho_dead = 0, leaf_checks = 0;
struct SL { int s; int l[MAXR]; };
std::vector<SL> rho_survivors;
constexpr size_t MAX_RHO_SURV = 5000000;
bool rho_overflow = false;
bool csp_existence_only = false;   // prefix checks: stop at the first (s,L) survivor
bool csp_found = false;
int csp_placed = 0;          // number of high vertices visible to the rho-level CSP
int hpar[MAXH];        // parent: >=0 high index, or -1-i for low i
int hroot[MAXH];       // low vertex index under which the component hangs
int hcomp[MAXH];       // component id
int hlca[MAXH][MAXH];  // within-component LCA offset q (valid when same comp)
uint64_t within_used;              // bit d set if within-distance d used
uint64_t class_used[MAXR];         // bit s set if sum s used in class i
int ncomp;

// ---------------------------------------------------------------------------
// Depth CSP for one complete abstract structure.
// Unknowns: s (bridge weight) and low depths l_1 < ... < l_{R-1} (l_0 = 0).
// N = n(n-1)/2, k = n-1, delta = C(k,2)+R, A = N-s, B = delta+1-s = A-M+1.
// All 276 pair values must be distinct and lie in [1,delta] \ (s+L).
// Values: within HH (fixed), class-i HH = 2B-2l_i+sum, LH below = B+y-l_i
// (i ancestor-or-equal of root(y) in the low tree), LH other =
// B+y+l_i-2 l_lca(i,root(y)), LL = l_i+l_j-2 l_lca, holes s+l_i.
// ---------------------------------------------------------------------------
int lowdep_edges[MAXR];      // edge-depth of low vertex in the low tree (for ancestor tests)
bool low_anc[MAXR][MAXR];    // low_anc[a][b]: a is an ancestor of b or a==b
int csp_l[MAXR];
int csp_s, csp_B, csp_delta, csp_N;
unsigned char csp_used[4096];
std::vector<int> class_sums[MAXR];   // sums per low class for the current structure
std::vector<int> within_vals;

bool csp_take(int v, std::vector<int>& taken) {
    int vmax = relaxed_vmax > 0 ? relaxed_vmax : csp_delta;
    if (v < 1 || v > vmax || csp_used[v]) return false;
    csp_used[v] = 1; taken.push_back(v); return true;
}
void csp_release(const std::vector<int>& taken) { for (int v : taken) csp_used[v] = 0; }

void csp_dfs(int i) {
    ++depth_csp_nodes;
    if (csp_found && csp_existence_only) return;
    if (i == R) {
        csp_found = true;
        if (csp_existence_only) return;
        SL x; x.s = csp_s; for (int j = 0; j < R; ++j) x.l[j] = csp_l[j];
        if (rho_survivors.size() < MAX_RHO_SURV) rho_survivors.push_back(x); else rho_overflow = true;
        return;
    }
    int lo = csp_l[lowpar[i]] + 1;       // parent strictly shallower; depths pairwise distinct (checked below)
    for (int l = lo; l <= csp_B - 1; ++l) {
        bool dup = false;
        for (int j = 0; j < i; ++j) if (csp_l[j] == l) { dup = true; break; }
        if (dup) continue;
        csp_l[i] = l;
        std::vector<int> taken;
        bool ok = true;
        // hole s + l (absent in relaxed mode)
        if (relaxed_vmax == 0 && l + csp_s <= csp_delta) { if (csp_used[csp_s + l]) ok = false; else { csp_used[csp_s + l] = 1; taken.push_back(csp_s + l); } }
        // low-low distances to earlier low vertices
        for (int j = 0; j < i && ok; ++j) {
            int a = lowlca[i][j];
            int d = l + csp_l[j] - 2 * csp_l[a];
            if (!csp_take(d, taken)) ok = false;
        }
        // low-high distances for this low vertex (placed high vertices only)
        for (int y = 0; y < csp_placed && ok; ++y) {
            int rt = hroot[y];
            int d;
            if (low_anc[i][rt]) d = csp_B + y - l;
            else { int a = lowlca[i][rt]; d = csp_B + y + l - 2 * csp_l[a]; }
            if (!csp_take(d, taken)) ok = false;
        }
        // class-i high-high values
        for (int sm : class_sums[i]) {
            if (!ok) break;
            int d = 2 * csp_B - 2 * l + sm;
            if (!csp_take(d, taken)) ok = false;
        }
        if (ok) csp_dfs(i + 1);
        csp_release(taken);
        if (csp_found && csp_existence_only) return;
    }
}

// rho-level CSP over the first `placed` high vertices: values that depend only
// on (s, L, rho): holes, x-h, low-low, low-high, cross-fibre HH class values.
// Fills rho_survivors.  Sound relaxation for any extension of the placed prefix.
void rho_level_csp(int placed) {
    ++rho_csp_runs;
    csp_placed = placed;
    for (int i = 0; i < R; ++i) class_sums[i].clear();
    for (int y = 0; y < placed; ++y)
        for (int yy = 0; yy < y; ++yy)
            if (hroot[y] != hroot[yy]) class_sums[lowlca[hroot[y]][hroot[yy]]].push_back(y + yy);
    rho_survivors.clear(); rho_overflow = false; csp_found = false;
    int k = order_n - 1;
    csp_N = order_n * (order_n - 1) / 2;
    csp_delta = k * (k - 1) / 2 + R;
    for (int s = 1; s <= csp_N; ++s) {
        if (fix_s > 0 && s != fix_s) continue;
        if (csp_found && csp_existence_only) break;
        int B = csp_delta + 1 - s;
        if (B < R) break;
        if (B + M - 1 != csp_N - s) { std::fprintf(stderr, "internal: block identity\n"); std::exit(3); }
        csp_s = s; csp_B = B;
        std::memset(csp_used, 0, sizeof(csp_used));
        std::vector<int> taken;
        bool ok = true;
        if (relaxed_vmax == 0 && s <= csp_delta) { csp_used[s] = 1; taken.push_back(s); }
        for (int sm : class_sums[0]) { if (!ok) break; if (!csp_take(2 * B + sm, taken)) ok = false; }
        for (int y = 0; y < placed && ok; ++y) if (!csp_take(B + y, taken)) ok = false;
        csp_l[0] = 0;
        if (ok) csp_dfs(1);
        csp_release(taken);
    }
    if (rho_overflow) { std::printf("RHO_SURVIVOR_OVERFLOW\n"); std::exit(5); }
}

std::string rho_key(int placed) {
    std::string k(placed, 0);
    for (int y = 0; y < placed; ++y) k[y] = (char)(hroot[y] + 1);
    return k;
}

// prefix check at DFS depth `placed` (memoized): true = alive, false = dead
bool rho_prefix_alive(int placed) {
    std::string key = rho_key(placed);
    if (dead_rho.count(key)) { ++rho_memo_hits; return false; }
    csp_existence_only = true;
    rho_level_csp(placed);
    csp_existence_only = false;
    if (!csp_found) { dead_rho.insert(key); return false; }
    return true;
}

void solve_depths_for_structure() {
    ++leaf_checks;
    std::string key = rho_key(M);
    if (dead_rho.count(key)) { ++rho_memo_hits; ++leaf_rho_dead; return; }
    rho_level_csp(M);
    if (rho_survivors.empty()) { dead_rho.insert(key); ++leaf_rho_dead; return; }
    // leaf-specific values: within-component distances and same-fibre cross-component class values
    within_vals.clear();
    for (int i = 0; i < R; ++i) class_sums[i].clear();
    for (int y = 0; y < M; ++y)
        for (int yy = 0; yy < y; ++yy) {
            if (hroot[y] != hroot[yy]) continue;
            if (hcomp[yy] == hcomp[y]) within_vals.push_back(y + yy - 2 * hlca[y][yy]);
            else class_sums[hroot[y]].push_back(y + yy);
        }
    uint64_t before = depth_survivors;
    for (const SL& x : rho_survivors) {
        int s = x.s, B = csp_delta + 1 - s;
        // rebuild the rho-level used set for this survivor
        std::memset(csp_used, 0, sizeof(csp_used));
        if (relaxed_vmax == 0) { csp_used[s] = 1; for (int i = 1; i < R; ++i) if (s + x.l[i] <= csp_delta) csp_used[s + x.l[i]] = 1; }
        for (int y = 0; y < M; ++y) csp_used[B + y] = 1;
        for (int y = 0; y < M; ++y)
            for (int yy = 0; yy < y; ++yy)
                if (hroot[y] != hroot[yy]) csp_used[2 * B - 2 * x.l[lowlca[hroot[y]][hroot[yy]]] + y + yy] = 1;
        for (int i = 1; i < R; ++i) {
            for (int j = 0; j < i; ++j) csp_used[x.l[i] + x.l[j] - 2 * x.l[lowlca[i][j]]] = 1;
            for (int y = 0; y < M; ++y) {
                int rt = hroot[y];
                int d = low_anc[i][rt] ? (B + y - x.l[i]) : (B + y + x.l[i] - 2 * x.l[lowlca[i][rt]]);
                csp_used[d] = 1;
            }
        }
        bool ok = true;
        std::vector<int> taken;
        for (int d : within_vals) if (!csp_take(d, taken)) { ok = false; break; }
        for (int i = 0; i < R && ok; ++i)
            for (int sm : class_sums[i]) { if (!csp_take(2 * B - 2 * x.l[i] + sm, taken)) { ok = false; break; } }
        if (ok) {
            ++depth_survivors;
            if (depth_survivors <= (uint64_t)max_witness) {
                std::printf("DEPTH_SURVIVOR s=%d L=", s);
                for (int j = 0; j < R; ++j) std::printf("%s%d", j ? "," : "", x.l[j]);
                std::printf(" lowpar=");
                for (int j = 1; j < R; ++j) std::printf("%s%d", j > 1 ? "," : "", lowpar[j]);
                std::printf(" hpar=");
                for (int v = 0; v < M; ++v) std::printf("%s%d", v ? "," : "", hpar[v]);
                std::printf("\n");
                std::fflush(stdout);
            }
        }
    }
    if (depth_survivors != before) ++structures_with_survivor;
}

uint64_t progress_every = 0;
void dfs(int y) {
    ++nodes;
    if (nodes_limit && nodes > nodes_limit) { aborted = true; return; }
    if (progress_every && nodes % progress_every == 0) {
        std::fprintf(stderr, "PROGRESS nodes=%llu leaves=%llu rho_csp_runs=%llu memo_hits=%llu csp_nodes=%llu depth_survivors=%llu\n",
                     (unsigned long long)nodes, (unsigned long long)leaves, (unsigned long long)rho_csp_runs,
                     (unsigned long long)rho_memo_hits, (unsigned long long)depth_csp_nodes, (unsigned long long)depth_survivors);
        std::fflush(stderr);
    }
    if (y == split_level) {
        uint64_t c = split_counter++;
        if (c % split_n != (uint64_t)split_k) return;
    }
    if (solve_depths && y < M && rho_check_at[y]) {
        if (!rho_prefix_alive(y)) { ++rho_prefix_prunes; return; }
    }
    if (y == M) {
        ++leaves;
        if (solve_depths) solve_depths_for_structure();
        if (stop_first) aborted = true;
        if (emit) {
            std::printf("STRUCT");
            for (int v = 0; v < M; ++v) std::printf(" %d", hpar[v]);
            std::printf("\n");
        }
        return;
    }
    // (a) attach to a low vertex i: new component
    for (int i = 0; i < R; ++i) {
        uint64_t add[MAXR]; std::memset(add, 0, sizeof(add));
        bool ok = true;
        for (int yy = 0; yy < y && ok; ++yy) {
            int l = lowlca[i][hroot[yy]];
            int s = y + yy;
            if (l == 0 && s > xcap) { ok = false; break; }
            uint64_t bit = 1ULL << s;
            if ((class_used[l] | add[l]) & bit) { ok = false; break; }
            add[l] |= bit;
        }
        if (!ok) continue;
        hpar[y] = -1 - i; hroot[y] = i; hcomp[y] = ncomp++;
        for (int l = 0; l < R; ++l) class_used[l] |= add[l];
        dfs(y + 1);
        for (int l = 0; l < R; ++l) class_used[l] &= ~add[l];
        --ncomp;
        if (aborted) return;
    }
    // (b) attach to an earlier high vertex p
    for (int p = 0; p < y; ++p) {
        uint64_t add[MAXR]; std::memset(add, 0, sizeof(add));
        uint64_t addw = 0;
        bool ok = true;
        for (int yy = 0; yy < y && ok; ++yy) {
            if (hcomp[yy] == hcomp[p]) {
                int q = (yy == p) ? p : hlca[p][yy];
                hlca[y][yy] = hlca[yy][y] = q;
                int d = y + yy - 2 * q;
                uint64_t bit = 1ULL << d;
                if ((within_used | addw) & bit) { ok = false; break; }
                addw |= bit;
            } else {
                int l = lowlca[hroot[p]][hroot[yy]];
                int s = y + yy;
                if (l == 0 && s > xcap) { ok = false; break; }
                uint64_t bit = 1ULL << s;
                if ((class_used[l] | add[l]) & bit) { ok = false; break; }
                add[l] |= bit;
            }
        }
        if (!ok) continue;
        hpar[y] = p; hroot[y] = hroot[p]; hcomp[y] = hcomp[p];
        within_used |= addw;
        for (int l = 0; l < R; ++l) class_used[l] |= add[l];
        dfs(y + 1);
        within_used &= ~addw;
        for (int l = 0; l < R; ++l) class_used[l] &= ~add[l];
        if (aborted) return;
    }
}

void compute_lowlca() {
    // depth in the low tree (number of edges) to compute LCA
    int dep[MAXR];
    dep[0] = 0;
    for (int i = 1; i < R; ++i) dep[i] = dep[lowpar[i]] + 1;
    for (int a = 0; a < R; ++a)
        for (int b = 0; b < R; ++b) {
            int u = a, v = b;
            while (u != v) {
                if (dep[u] >= dep[v]) u = lowpar[u]; else v = lowpar[v];
            }
            lowlca[a][b] = u;
            low_anc[a][b] = (lowlca[a][b] == a);
        }
    for (int i = 0; i < R; ++i) lowdep_edges[i] = dep[i];
}

// AHU canonical string of the rooted low tree (labels irrelevant for the
// depth-free search: only the LCA structure matters).
std::string ahu(int v) {
    std::vector<std::string> ch;
    for (int i = 1; i < R; ++i) if (lowpar[i] == v) ch.push_back(ahu(i));
    std::sort(ch.begin(), ch.end());
    std::string s = "(";
    for (auto& c : ch) s += c;
    return s + ")";
}

std::vector<int> parse_list(const char* s) {
    std::vector<int> out; std::string cur;
    for (const char* p = s;; ++p) {
        if (*p == ',' || *p == 0) { if (!cur.empty()) out.push_back(std::atoi(cur.c_str())); cur.clear(); if (!*p) break; }
        else cur += *p;
    }
    return out;
}

void run_one(const char* tag) {
    compute_lowlca();
    nodes = 0; leaves = 0; aborted = false; ncomp = 0; split_counter = 0;
    depth_survivors = 0; depth_csp_nodes = 0; structures_with_survivor = 0;
    dead_rho.clear(); rho_csp_runs = rho_memo_hits = rho_prefix_prunes = leaf_rho_dead = leaf_checks = 0;
    within_used = 0; std::memset(class_used, 0, sizeof(class_used));
    dfs(0);
    std::printf("ABSTRACT m=%d r=%d lowpar=%s xcap=%d split=%d:%d/%d leaves=%llu nodes=%llu %s", M, R, tag, xcap, split_level, split_k, split_n,
                (unsigned long long)leaves, (unsigned long long)nodes,
                (stop_first && leaves) ? "EXISTS" : (aborted ? "ABORTED" : "EXHAUSTED"));
    if (solve_depths) std::printf(" depth_survivors=%llu structures_with_survivor=%llu csp_nodes=%llu rho_csp_runs=%llu rho_memo_hits=%llu rho_prefix_prunes=%llu leaf_rho_dead=%llu leaf_checks=%llu",
                                  (unsigned long long)depth_survivors, (unsigned long long)structures_with_survivor,
                                  (unsigned long long)depth_csp_nodes, (unsigned long long)rho_csp_runs, (unsigned long long)rho_memo_hits,
                                  (unsigned long long)rho_prefix_prunes, (unsigned long long)leaf_rho_dead, (unsigned long long)leaf_checks);
    std::printf("\n");
    std::fflush(stdout);
}

} // namespace

int main(int argc, char** argv) {
    M = 19; R = -1;
    std::vector<int> lp;
    bool all_shapes = false;
    const char* shapes_file = nullptr;
    int shard_k = 0, shard_n = 1;
    bool dedup = true;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        auto next = [&]() -> const char* { if (i + 1 >= argc) std::exit(2); return argv[++i]; };
        if (a == "--m") M = std::atoi(next());
        else if (a == "--r") R = std::atoi(next());
        else if (a == "--lowpar") lp = parse_list(next());
        else if (a == "--xcap") xcap = std::atoi(next());
        else if (a == "--emit") emit = true;
        else if (a == "--stop-first") stop_first = true;
        else if (a == "--solve-depths") solve_depths = true;
        else if (a == "--split") { split_level = std::atoi(next()); split_k = std::atoi(next()); split_n = std::atoi(next()); }
        else if (a == "--order") order_n = std::atoi(next());
        else if (a == "--max-witness") max_witness = std::atoi(next());
        else if (a == "--relaxed") relaxed_vmax = std::atoi(next());
        else if (a == "--fix-s") fix_s = std::atoi(next());
        else if (a == "--rho-check") { for (int lv : parse_list(next())) if (lv > 0 && lv <= MAXH) { rho_check_at[lv] = true; rho_check_level = lv; } }
        else if (a == "--all-shapes") all_shapes = true;
        else if (a == "--shapes-file") shapes_file = next();
        else if (a == "--shard") { shard_k = std::atoi(next()); shard_n = std::atoi(next()); }
        else if (a == "--no-dedup") dedup = false;
        else if (a == "--progress") progress_every = std::strtoull(next(), nullptr, 10);
        else if (a == "--nodes-limit") nodes_limit = std::strtoull(next(), nullptr, 10);
        else { std::fprintf(stderr, "unknown arg %s\n", a.c_str()); return 2; }
    }
    if (M < 1 || M > MAXH) return 2;
    if (shapes_file) {
        // one labeled shape per line: comma-separated lowpar[1..r-1]; lines are
        // taken in order and sharded by --shard k n (no isomorphism dedup)
        FILE* f = std::fopen(shapes_file, "r");
        if (!f) { std::fprintf(stderr, "cannot open shapes file\n"); return 2; }
        char buf[512];
        uint64_t total_leaves = 0, total_surv = 0; int shapes = 0, idx = 0; bool any_abort = false;
        while (std::fgets(buf, sizeof(buf), f)) {
            std::string line(buf);
            while (!line.empty() && (line.back() == '\n' || line.back() == '\r' || line.back() == ' ')) line.pop_back();
            if (line.empty() || line[0] == '#') continue;
            int my = idx++;
            if (my % shard_n != shard_k) continue;
            std::vector<int> v = parse_list(line.c_str());
            R = (int)v.size() + 1;
            if (R > MAXR) return 2;
            lowpar[0] = -1;
            for (int i = 1; i < R; ++i) lowpar[i] = v[i - 1];
            run_one(line.c_str());
            total_leaves += leaves; total_surv += depth_survivors; ++shapes; any_abort |= (aborted && !(stop_first && leaves));
        }
        std::fclose(f);
        std::printf("SHAPES_FILE_SUMMARY m=%d shapes_run=%d shard=%d/%d total_leaves=%llu depth_survivors=%llu %s\n", M, shapes, shard_k, shard_n,
                    (unsigned long long)total_leaves, (unsigned long long)total_surv, any_abort ? "INCOMPLETE" : "COMPLETE");
        return 0;
    }
    if (all_shapes) {
        if (R < 1 || R > MAXR) return 2;
        // enumerate lowpar[i] in [0, i-1]
        std::vector<int> cur(R, 0);
        cur[0] = -1;
        std::vector<int> idx(R, 0);
        uint64_t total_leaves = 0; int shapes = 0, skipped_iso = 0, skipped_shard = 0; bool any_abort = false;
        std::set<std::string> seen;
        int class_index = 0;
        // mixed radix counter
        while (true) {
            for (int i = 0; i < R; ++i) lowpar[i] = cur[i];
            std::string tag;
            for (int i = 1; i < R; ++i) { if (i > 1) tag += ","; tag += std::to_string(cur[i]); }
            bool run = true;
            if (dedup) {
                std::string key = ahu(0);
                if (!seen.insert(key).second) { run = false; ++skipped_iso; }
            }
            if (run) {
                if (class_index % shard_n != shard_k) { run = false; ++skipped_shard; }
                ++class_index;
            }
            if (run) {
                run_one(tag.c_str());
                total_leaves += leaves; ++shapes; any_abort |= (aborted && !(stop_first && leaves));
            }
            int i = R - 1;
            while (i >= 1) { if (cur[i] + 1 < i) { ++cur[i]; break; } cur[i] = 0; --i; }
            if (i < 1) break;
        }
        std::printf("ABSTRACT_SUMMARY m=%d r=%d shapes_run=%d iso_classes=%d skipped_iso=%d skipped_other_shards=%d shard=%d/%d xcap=%d total_leaves=%llu %s\n",
                    M, R, shapes, class_index, skipped_iso, skipped_shard, shard_k, shard_n, xcap,
                    (unsigned long long)total_leaves, any_abort ? "INCOMPLETE" : (total_leaves ? "STRUCTURES_EXIST" : "NO_STRUCTURE"));
        return 0;
    }
    R = (int)lp.size() + 1;
    lowpar[0] = -1;
    for (int i = 1; i < R; ++i) lowpar[i] = lp[i - 1];
    std::string tag;
    for (int i = 1; i < R; ++i) { if (i > 1) tag += ","; tag += std::to_string(lowpar[i]); }
    run_one(tag.c_str());
    return 0;
}
