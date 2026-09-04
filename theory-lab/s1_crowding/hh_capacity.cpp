// Exact capacities for the refined top-block crowding bound.
//
// High vertices carry labels y in [0,m-1] (depth B+y).  Two high vertices
// with a low LCA of depth l are at distance 2B-2l+y+y'; inside a fixed low
// LCA class the pairs are exactly the cross-branch pairs of the set of high
// vertices below that low vertex, and distinctness of distances forces the
// sums y+y' to be pairwise distinct.  Two high vertices with a high LCA
// (depth B+q) are at distance y+y'-2q, again pairwise distinct.
//
// Cap(m) = max number of cross-block pairs over all subsets Y of [0,m-1]
//          and all partitions of Y into >=2 blocks, such that all cross-block
//          sums y+y' are pairwise distinct.
// W(m)   = max number of within-component pairs over all rooted forests on a
//          subset of [0,m-1] (parent has a smaller label), such that all
//          within-component distances y+y'-2q are pairwise distinct.
//
// Necessary condition for the singleton normal form with r low vertices and
// m = 24-r high vertices:  C(m,2) <= W(m) + r*Cap(m).
//
// Usage: hh_capacity cap m | hh_capacity within m
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

namespace {

int M;
int best;
uint64_t nodes;

// ---------- Cap(m) ----------
int label[32];
int block_count;

int popc(uint64_t x) { return __builtin_popcountll(x); }

void cap_dfs(int y, int pairs, uint64_t used_sums) {
    ++nodes;
    if (pairs > best) best = pairs;
    if (y == M) return;
    int free_sums = (2 * M - 3) - popc(used_sums);
    if (pairs + free_sums <= best) return;           // every future pair needs a fresh sum
    // option 0: exclude y
    label[y] = 0;
    cap_dfs(y + 1, pairs, used_sums);
    // option: put y in an existing block b or a new block (symmetry: new block = block_count+1)
    for (int b = 1; b <= block_count + 1; ++b) {
        uint64_t add = 0;
        int np = 0;
        bool ok = true;
        for (int yy = 0; yy < y; ++yy) {
            if (label[yy] == 0 || label[yy] == b) continue;
            int s = y + yy;
            uint64_t bit = 1ULL << s;
            if ((used_sums | add) & bit) { ok = false; break; }
            add |= bit;
            ++np;
        }
        if (!ok) continue;
        label[y] = b;
        int saved = block_count;
        if (b == block_count + 1) block_count = b;
        cap_dfs(y + 1, pairs + np, used_sums | add);
        block_count = saved;
    }
    label[y] = 0;
}

// ---------- W(m) ----------
int par[32];          // -2 excluded, -1 root, else parent label
int lcad[32][32];     // lca label (as depth offset q) for included vertices in same component; -1 if different comps
int comp[32];
int ncomp;

void within_dfs(int y, int pairs, uint64_t used) {
    ++nodes;
    if (pairs > best) best = pairs;
    if (y == M) return;
    int free_vals = (2 * M - 3) - popc(used >> 1);   // values 1..2M-3
    if (pairs + free_vals <= best) return;
    // exclude
    par[y] = -2;
    within_dfs(y + 1, pairs, used);
    // new root
    par[y] = -1; comp[y] = ncomp++;
    for (int yy = 0; yy < y; ++yy) lcad[y][yy] = lcad[yy][y] = -1;
    within_dfs(y + 1, pairs, used);
    --ncomp;
    // child of an included earlier vertex p
    for (int p = 0; p < y; ++p) {
        if (par[p] == -2) continue;
        uint64_t add = 0; int np = 0; bool ok = true;
        for (int yy = 0; yy < y; ++yy) {
            if (par[yy] == -2) continue;
            int q;
            if (yy == p) q = p;
            else if (comp[yy] != comp[p]) { lcad[y][yy] = lcad[yy][y] = -1; continue; }
            else q = lcad[p][yy];
            lcad[y][yy] = lcad[yy][y] = q;
            int d = y + yy - 2 * q;
            uint64_t bit = 1ULL << d;
            if ((used | add) & bit) { ok = false; break; }
            add |= bit; ++np;
        }
        if (!ok) continue;
        par[y] = p; comp[y] = comp[p];
        within_dfs(y + 1, pairs + np, used | add);
    }
    par[y] = -2;
}

} // namespace

int main(int argc, char** argv) {
    if (argc != 3) { std::fprintf(stderr, "usage: %s cap|within m\n", argv[0]); return 2; }
    M = std::atoi(argv[2]);
    if (M < 2 || M > 30) return 2;
    best = 0; nodes = 0;
    if (!std::strcmp(argv[1], "cap")) {
        block_count = 0;
        cap_dfs(0, 0, 0);
        std::printf("Cap(%d) = %d   (trivial bound 2m-3 = %d, nodes %llu)\n", M, best, 2 * M - 3, (unsigned long long)nodes);
    } else if (!std::strcmp(argv[1], "within")) {
        ncomp = 0;
        for (int i = 0; i < 32; ++i) par[i] = -2;
        within_dfs(0, 0, 0);
        std::printf("W(%d) = %d   (trivial bound 2m-3 = %d, nodes %llu)\n", M, best, 2 * M - 3, (unsigned long long)nodes);
    } else return 2;
    return 0;
}
