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
// Moment layer (WP-A1): two exact integer linear equations of the whole tree,
//   (W)  sum_e w_e |A_e| (n-|A_e|) = sum_{d=1}^{N} d
//   (M)  sum_e w_e q_e  (S-q_e)    = sum_{d=1}^{N} (-1)^d d ,
// with sigma_v = (-1)^{depth(v)}, S = sum_v sigma_v, q_e = sum_{v in A_e} sigma_v
// (using (-1)^{d(u,v)} = sigma_u sigma_v).  Both hold for any Leech tree because
// its N distances are exactly 1..N.  In the singleton normal form every depth is
// affine in (s, l_1..l_{R-1}); |A_e| is a structural constant and, once the
// parity pattern of (s, l_1..l_{R-1}) is fixed, q_e and S are constants, so (W)
// and (M) are integer linear equations in the depth variables.  --moment-level:
//   0  off (legacy engine)
//   1  exact (W),(M) test on every complete (s,L) only
//   2  1 + a per-structure screen that kills a structure when no (s, parity
//      pattern) passes the box / gcd / 2-column-lattice solvability tests; the
//      depth DFS itself is untouched, so the coarse rho memo stays sound
//   3  2 + in-DFS pruning: per-s solvability skip and pinning of the last two
//      depths from (W) alone and from (W),(M) jointly.  This makes the DFS
//      structure-dependent, so the hroot-keyed rho memo can no longer be
//      written; a finer moment-equivalence memo replaces it.
// --no-moment = level 0.  Default 2.
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

// ---------------------------------------------------------------------------
// Moment layer.  Vertices of the full order-n tree: 0..R-1 low (0 = x, depth 0),
// R..R+M-1 high (depth B+y), R+M anchor (depth s, parent x).  Edge weights and
// depths are affine in the coefficient basis [const, s, l_1, ..., l_{R-1}].
// ---------------------------------------------------------------------------
constexpr int MAXV = MAXH + MAXR + 1;
constexpr int MOM_PAT_CAP = 1024;

int moment_level = 2;                 // see header
bool use_memo = true;                 // --no-memo: debug/differential only
bool emit_rho = false;                // --emit-rho: dump every rho-level survivor
bool mom_ready = false;               // structure built for the current leaf
bool mom_pats_ok = false;             // parity table small enough to use
bool mom_on = false, mom_full = false;
bool mom_pruned_run = false;          // a moment test removed something this run
bool mom_unconstrained_leaf = false;  // csp_dfs reached i==R ignoring the moment
int mom_n = 0, mom_parent[MAXV], mom_size[MAXV], mom_even[MAXV];
long long mom_wc[MAXV][MAXR + 1];     // weight of the edge above v
long long mom_W[MAXR + 1];            // Wiener affine form
long long mom_TW = 0, mom_TM = 0;
int mom_oddhigh[2] = {0, 0};
long long mom_target_oddpairs = 0;
uint64_t mom_s_prunes = 0, mom_pat_prunes = 0, mom_pins = 0, mom_leaf_rejects = 0,
         mom_fine_hits = 0, mom_pin_kills = 0, mom_struct_prunes = 0;
std::unordered_set<std::string> dead_moment;

struct MomPat { unsigned pat; long long J[MAXR + 1]; long long cW, cM, gW, gM, gDet; };
std::vector<MomPat> mom_pats[2];
std::vector<int> mom_alive;

long long mom_gcd(long long a, long long b) {
    if (a < 0) a = -a; if (b < 0) b = -b;
    while (b) { long long t = a % b; a = b; b = t; }
    return a;
}

// signed subtree sums q_e and the resulting affine form J for one parity pattern
void moment_pattern_J(unsigned pat, int sp, long long* J) {
    int sub[MAXV];
    int S = 0;
    for (int v = 0; v < mom_n; ++v) {
        int odd;
        if (v < R) odd = (v == 0) ? 0 : (int)((pat >> (v - 1)) & 1u);
        else if (v < R + M) odd = (csp_delta + 1 + (v - R) + sp) & 1;
        else odd = sp;
        sub[v] = odd ? -1 : 1;
        S += sub[v];
    }
    for (int v = mom_n - 1; v >= 1; --v) sub[mom_parent[v]] += sub[v];
    for (int i = 0; i <= R; ++i) {
        long long acc = 0;
        for (int v = 1; v < mom_n; ++v) acc += (long long)sub[v] * (S - sub[v]) * mom_wc[v][i];
        J[i] = acc;
    }
}

void moment_build_patterns() {
    mom_pats_ok = false;
    int freebits = R - 1;
    if (freebits < 0 || freebits > 20) return;
    long long total = 0;
    for (int sp = 0; sp < 2; ++sp) {
        mom_pats[sp].clear();
        bool okpop[MAXR + 1];
        for (int pc = 0; pc <= freebits; ++pc) {
            long long o = pc + mom_oddhigh[sp] + sp;
            okpop[pc] = (o * (mom_n - o) == mom_target_oddpairs);
        }
        for (unsigned pat = 0; pat < (1u << freebits); ++pat) {
            if (!okpop[__builtin_popcount(pat)]) continue;
            if (++total > MOM_PAT_CAP) { for (int q = 0; q < 2; ++q) mom_pats[q].clear(); return; }
            MomPat mp; mp.pat = pat;
            moment_pattern_J(pat, sp, mp.J);
            long long sumWb = 0, sumJb = 0, gW = 0, gJ = 0;
            for (int v = 1; v < R; ++v) {
                long long b = (pat >> (v - 1)) & 1u;
                sumWb += mom_W[v + 1] * b;
                sumJb += mp.J[v + 1] * b;
                gW = mom_gcd(gW, 2 * mom_W[v + 1]);
                gJ = mom_gcd(gJ, 2 * mp.J[v + 1]);
            }
            long long gd = 0;
            for (int v = 1; v < R; ++v)
                for (int w = v + 1; w < R; ++w)
                    gd = mom_gcd(gd, 4 * (mom_W[v + 1] * mp.J[w + 1] - mom_W[w + 1] * mp.J[v + 1]));
            mp.cW = mom_TW - mom_W[0] - sumWb;
            mp.cM = mom_TM - mp.J[0] - sumJb;
            mp.gW = gW; mp.gM = gJ; mp.gDet = gd;
            mom_pats[sp].push_back(mp);
        }
    }
    mom_pats_ok = true;
}

// build parent / subtree sizes / affine edge weights of the complete structure
void moment_build_structure() {
    mom_ready = false;
    int k = order_n - 1;
    csp_delta = k * (k - 1) / 2 + R;
    csp_N = order_n * (order_n - 1) / 2;
    mom_n = R + M + 1;
    if (mom_n != order_n || mom_n > MAXV) return;
    for (int v = 0; v < mom_n; ++v) {
        mom_size[v] = 1; mom_even[v] = 0;
        for (int i = 0; i <= R; ++i) mom_wc[v][i] = 0;
    }
    mom_parent[0] = -1;
    for (int i = 1; i < R; ++i) {
        mom_parent[i] = lowpar[i];
        mom_wc[i][i + 1] += 1;
        if (lowpar[i] > 0) mom_wc[i][lowpar[i] + 1] -= 1;
    }
    for (int y = 0; y < M; ++y) {
        int v = R + y;
        if (hpar[y] < 0) {
            int i = -1 - hpar[y];
            mom_parent[v] = i;
            mom_wc[v][0] = (long long)csp_delta + 1 + y;
            mom_wc[v][1] = -1;
            if (i > 0) mom_wc[v][i + 1] -= 1;
        } else {
            mom_parent[v] = R + hpar[y];
            mom_wc[v][0] = y - hpar[y];
        }
        mom_even[v] = (y % 2 == 0) ? 1 : 0;
    }
    mom_parent[R + M] = 0;
    mom_wc[R + M][1] = 1;
    for (int v = mom_n - 1; v >= 1; --v) {
        mom_size[mom_parent[v]] += mom_size[v];
        mom_even[mom_parent[v]] += mom_even[v];
    }
    for (int i = 0; i <= R; ++i) {
        long long acc = 0;
        for (int v = 1; v < mom_n; ++v) acc += (long long)mom_size[v] * (mom_n - mom_size[v]) * mom_wc[v][i];
        mom_W[i] = acc;
    }
    long long NN = (long long)order_n * (order_n - 1) / 2;
    mom_TW = NN * (NN + 1) / 2;
    mom_TM = (NN % 2 == 0) ? NN / 2 : -(NN + 1) / 2;
    mom_target_oddpairs = (NN + 1) / 2;
    for (int sp = 0; sp < 2; ++sp) {
        int c = 0;
        for (int y = 0; y < M; ++y) if (((csp_delta + 1 + y + sp) & 1) != 0) ++c;
        mom_oddhigh[sp] = c;
    }
    mom_ready = true;
    moment_build_patterns();
}

// exact structure-equivalence key: (hroot, per-high subtree size / even-index
// count / parent gap) determines mom_W and every J, hence the moment system.
std::string moment_fine_key() {
    std::string k;
    k.reserve(4 * M);
    for (int y = 0; y < M; ++y) k += (char)(hroot[y] + 1);
    for (int y = 0; y < M; ++y) {
        k += (char)(mom_size[R + y] + 1);
        k += (char)(mom_even[R + y] + 1);
        k += (char)((hpar[y] < 0 ? 0 : (y - hpar[y])) + 1);
    }
    return k;
}

// parity-free screen of one bridge weight s against (W) alone
bool moment_s_box_ok(int s, int B) {
    long long need = mom_TW - mom_W[0] - mom_W[1] * (long long)s;
    long long lo = 0, hi = 0, g = 0;
    for (int v = 1; v < R; ++v) {
        long long c = mom_W[v + 1];
        long long a = c, b = c * (long long)(B - 1);
        lo += (a < b ? a : b); hi += (a < b ? b : a);
        g = mom_gcd(g, c);
    }
    if (need < lo || need > hi) return false;
    if (g == 0) return need == 0;
    return need % g == 0;
}

// gcd / lattice solvability of {(W),(M)} for one parity pattern at this s
bool moment_pattern_alive(const MomPat& mp, int s) {
    long long RW = mp.cW - mom_W[1] * (long long)s;
    long long RM = mp.cM - mp.J[1] * (long long)s;
    if (mp.gW == 0) { if (RW != 0) return false; } else if (RW % mp.gW) return false;
    if (mp.gM == 0) { if (RM != 0) return false; } else if (RM % mp.gM) return false;
    if (mp.gDet) {
        for (int v = 1; v < R; ++v)
            if ((2 * mom_W[v + 1] * RM - 2 * mp.J[v + 1] * RW) % mp.gDet) return false;
    }
    return true;
}

// --moment-selftest: recompute both moments directly from the explicit tree and
// compare with the affine forms.  Validates mom_W and moment_pattern_J.
bool moment_selftest = false;
void moment_check_affine() {
    int dep[MAXV];
    for (int v = 0; v < mom_n; ++v)
        dep[v] = (v < R) ? csp_l[v] : (v < R + M ? csp_B + (v - R) : csp_s);
    long long wsum = 0, msum = 0;
    for (int u = 0; u < mom_n; ++u)
        for (int v = u + 1; v < mom_n; ++v) {
            int a = u, b = v;
            bool anc[MAXV] = {false};
            while (a != -1) { anc[a] = true; a = mom_parent[a]; }
            while (!anc[b]) b = mom_parent[b];
            long long d = dep[u] + dep[v] - 2 * dep[b];
            wsum += d;
            msum += (d % 2 ? -d : d);
        }
    unsigned pat = 0;
    for (int v = 1; v < R; ++v) if (csp_l[v] & 1) pat |= (1u << (v - 1));
    long long w = mom_W[0] + mom_W[1] * (long long)csp_s;
    for (int v = 1; v < R; ++v) w += mom_W[v + 1] * (long long)csp_l[v];
    long long J[MAXR + 1];
    moment_pattern_J(pat, csp_s & 1, J);
    long long j = J[0] + J[1] * (long long)csp_s;
    for (int v = 1; v < R; ++v) j += J[v + 1] * (long long)csp_l[v];
    if (w != wsum || j != msum) {
        std::printf("MOMENT_SELFTEST_FAIL s=%d wiener_affine=%lld wiener_tree=%lld signed_affine=%lld signed_tree=%lld\n",
                    csp_s, w, wsum, j, msum);
        std::exit(7);
    }
}

// per-structure screen: dead when no bridge weight admits any parity pattern
// whose (W),(M) system is solvable.  Reads nothing the depth DFS writes, so it
// leaves the hroot-keyed memo semantics untouched.
bool moment_structure_dead() {
    if (!mom_ready) return false;
    for (int s = 1; s <= csp_N; ++s) {
        if (fix_s > 0 && s != fix_s) continue;
        int B = csp_delta + 1 - s;
        if (B < R) break;
        if (!moment_s_box_ok(s, B)) continue;
        if (!mom_pats_ok) return false;
        const std::vector<MomPat>& pl = mom_pats[s & 1];
        for (size_t t = 0; t < pl.size(); ++t) if (moment_pattern_alive(pl[t], s)) return false;
    }
    return true;
}

// exact terminal test of (W) and (M) on a complete (s, L)
bool moment_final_ok() {
    unsigned pat = 0;
    for (int v = 1; v < R; ++v) if (csp_l[v] & 1) pat |= (1u << (v - 1));
    int sp = csp_s & 1;
    long long w = mom_W[0] + mom_W[1] * (long long)csp_s;
    for (int v = 1; v < R; ++v) w += mom_W[v + 1] * (long long)csp_l[v];
    if (w != mom_TW) return false;
    long long o = __builtin_popcount(pat) + mom_oddhigh[sp] + sp;
    if (o * (mom_n - o) != mom_target_oddpairs) return false;
    long long J[MAXR + 1];
    moment_pattern_J(pat, sp, J);
    long long j = J[0] + J[1] * (long long)csp_s;
    for (int v = 1; v < R; ++v) j += J[v + 1] * (long long)csp_l[v];
    return j == mom_TM;
}

// Candidate depths for level i.  -1 = enumerate the whole range (no pin).
// i == R-1: (W) alone pins the last depth.  i == R-2: (W) and (M) together
// pin the pair, one 2x2 solve per surviving parity pattern.
int moment_candidates(int i, int lo, int* cand) {
    if (i == R - 1 && R >= 2) {
        long long a = mom_W[R];
        long long T = mom_TW - mom_W[0] - mom_W[1] * (long long)csp_s;
        for (int v = 1; v <= R - 2; ++v) T -= mom_W[v + 1] * (long long)csp_l[v];
        ++mom_pins; mom_pruned_run = true;
        if (a == 0) { if (T != 0) { ++mom_pin_kills; return 0; } return -1; }
        if (T % a) { ++mom_pin_kills; return 0; }
        long long l = T / a;
        if (l < lo || l > csp_B - 1) { ++mom_pin_kills; return 0; }
        cand[0] = (int)l;
        return 1;
    }
    if (i == R - 2 && R >= 3 && mom_pats_ok) {
        long long Wa = mom_W[R - 1], Wb = mom_W[R];
        long long TWr = mom_TW - mom_W[0] - mom_W[1] * (long long)csp_s;
        unsigned prefmask = 0, prefbits = 0;
        for (int v = 1; v <= R - 3; ++v) {
            TWr -= mom_W[v + 1] * (long long)csp_l[v];
            prefmask |= 1u << (v - 1);
            if (csp_l[v] & 1) prefbits |= 1u << (v - 1);
        }
        const std::vector<MomPat>& pl = mom_pats[csp_s & 1];
        int k = 0;
        for (size_t t = 0; t < mom_alive.size(); ++t) {
            const MomPat& mp = pl[mom_alive[t]];
            if ((mp.pat & prefmask) != prefbits) continue;
            long long Ja = mp.J[R - 1], Jb = mp.J[R];
            long long det = Wa * Jb - Wb * Ja;
            if (det == 0) return -1;                    // dependent rows: enumerate
            long long TMr = mom_TM - mp.J[0] - mp.J[1] * (long long)csp_s;
            for (int v = 1; v <= R - 3; ++v) TMr -= mp.J[v + 1] * (long long)csp_l[v];
            long long num = TWr * Jb - Wb * TMr;
            if (num % det) continue;
            long long la = num / det;
            if ((la & 1LL) != (long long)((mp.pat >> (R - 3)) & 1u)) continue;
            if (la < lo || la > csp_B - 1) continue;
            bool dup = false;
            for (int q = 0; q < k; ++q) if (cand[q] == (int)la) { dup = true; break; }
            if (!dup && k < MOM_PAT_CAP) cand[k++] = (int)la;
        }
        ++mom_pins; mom_pruned_run = true;
        if (!k) ++mom_pin_kills;
        return k;
    }
    return -1;
}


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
        mom_unconstrained_leaf = true;
        if (moment_selftest && mom_ready) moment_check_affine();
        if (mom_on && !moment_final_ok()) { ++mom_leaf_rejects; if (mom_full) mom_pruned_run = true; return; }
        csp_found = true;
        if (csp_existence_only) return;
        SL x; x.s = csp_s; for (int j = 0; j < R; ++j) x.l[j] = csp_l[j];
        if (emit_rho) {
            std::printf("RHO s=%d L=", csp_s);
            for (int j = 0; j < R; ++j) std::printf("%s%d", j ? "," : "", csp_l[j]);
            std::printf(" hpar=");
            for (int v = 0; v < csp_placed; ++v) std::printf("%s%d", v ? "," : "", hpar[v]);
            std::printf("\n");
        }
        if (rho_survivors.size() < MAX_RHO_SURV) rho_survivors.push_back(x); else rho_overflow = true;
        return;
    }
    int lo = csp_l[lowpar[i]] + 1;       // parent strictly shallower; depths pairwise distinct (checked below)
    int mom_cand[MOM_PAT_CAP];
    int mom_nc = mom_full ? moment_candidates(i, lo, mom_cand) : -1;
    int mom_steps = (mom_nc < 0) ? (csp_B - lo) : mom_nc;
    for (int mom_t = 0; mom_t < mom_steps; ++mom_t) {
        int l = (mom_nc < 0) ? (lo + mom_t) : mom_cand[mom_t];
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
    mom_on = (moment_level >= 1 && mom_ready && placed == M && relaxed_vmax == 0 && R + M + 1 == order_n);
    mom_full = mom_on && moment_level >= 3;
    mom_pruned_run = false; mom_unconstrained_leaf = false;
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
        if (mom_full) {
            if (!moment_s_box_ok(s, B)) { ++mom_s_prunes; mom_pruned_run = true; continue; }
            if (mom_pats_ok) {
                mom_alive.clear();
                const std::vector<MomPat>& pl = mom_pats[s & 1];
                for (size_t t = 0; t < pl.size(); ++t) if (moment_pattern_alive(pl[t], s)) mom_alive.push_back((int)t);
                if (mom_alive.empty()) { ++mom_pat_prunes; mom_pruned_run = true; continue; }
            }
        }
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
    mom_ready = false;                    // prefix relaxation: no complete structure
    std::string key = rho_key(placed);
    if (use_memo && dead_rho.count(key)) { ++rho_memo_hits; return false; }
    csp_existence_only = true;
    rho_level_csp(placed);
    csp_existence_only = false;
    if (!csp_found) { if (use_memo) dead_rho.insert(key); return false; }
    return true;
}

void solve_depths_for_structure() {
    ++leaf_checks;
    std::string key = rho_key(M);
    if (use_memo && dead_rho.count(key)) { ++rho_memo_hits; ++leaf_rho_dead; return; }
    mom_ready = false;
    std::string fkey;
    bool fine_memo = false;
    if (moment_level >= 1 && relaxed_vmax == 0 && R + M + 1 == order_n) {
        moment_build_structure();
        if (mom_ready && moment_level >= 2) {
            fkey = moment_fine_key();
            fine_memo = true;
            if (use_memo && dead_moment.count(fkey)) { ++mom_fine_hits; ++leaf_rho_dead; return; }
            if (moment_structure_dead()) {
                ++mom_struct_prunes;
                if (use_memo) dead_moment.insert(fkey);
                ++leaf_rho_dead; return;
            }
        }
    }
    rho_level_csp(M);
    if (rho_survivors.empty()) {
        // the coarse rho key is only sound when the run was not narrowed by the
        // moment layer: it is shared by every structure with the same hroot.
        if (use_memo && !mom_pruned_run && !mom_unconstrained_leaf) dead_rho.insert(key);
        if (use_memo && fine_memo) dead_moment.insert(fkey);
        ++leaf_rho_dead; return;
    }
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
    dead_rho.clear(); dead_moment.clear();
    rho_csp_runs = rho_memo_hits = rho_prefix_prunes = leaf_rho_dead = leaf_checks = 0;
    mom_s_prunes = mom_pat_prunes = mom_pins = mom_pin_kills = mom_leaf_rejects = mom_fine_hits = mom_struct_prunes = 0;
    within_used = 0; std::memset(class_used, 0, sizeof(class_used));
    dfs(0);
    std::printf("ABSTRACT m=%d r=%d lowpar=%s xcap=%d split=%d:%d/%d leaves=%llu nodes=%llu %s", M, R, tag, xcap, split_level, split_k, split_n,
                (unsigned long long)leaves, (unsigned long long)nodes,
                (stop_first && leaves) ? "EXISTS" : (aborted ? "ABORTED" : "EXHAUSTED"));
    if (solve_depths) std::printf(" depth_survivors=%llu structures_with_survivor=%llu csp_nodes=%llu rho_csp_runs=%llu rho_memo_hits=%llu rho_prefix_prunes=%llu leaf_rho_dead=%llu leaf_checks=%llu",
                                  (unsigned long long)depth_survivors, (unsigned long long)structures_with_survivor,
                                  (unsigned long long)depth_csp_nodes, (unsigned long long)rho_csp_runs, (unsigned long long)rho_memo_hits,
                                  (unsigned long long)rho_prefix_prunes, (unsigned long long)leaf_rho_dead, (unsigned long long)leaf_checks);
    if (solve_depths) std::printf(" moment_level=%d mom_s_prunes=%llu mom_pat_prunes=%llu mom_pins=%llu mom_pin_kills=%llu mom_leaf_rejects=%llu mom_fine_hits=%llu mom_struct_prunes=%llu",
                                  moment_level, (unsigned long long)mom_s_prunes, (unsigned long long)mom_pat_prunes,
                                  (unsigned long long)mom_pins, (unsigned long long)mom_pin_kills,
                                  (unsigned long long)mom_leaf_rejects, (unsigned long long)mom_fine_hits,
                                  (unsigned long long)mom_struct_prunes);
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
        else if (a == "--no-moment") moment_level = 0;
        else if (a == "--moment-selftest") moment_selftest = true;
        else if (a == "--no-memo") use_memo = false;
        else if (a == "--emit-rho") emit_rho = true;
        else if (a == "--moment-level") moment_level = std::atoi(next());
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
