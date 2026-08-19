// mdd_forest.cpp -- exact feasibility search for DISTINCT DISTANCE TREES (Calhoun-Ferland-Lister-Polhill 2007, JCMCC 61):
// does a tree on n vertices with positive-integer weights and pairwise distinct distances, all <= D, exist?
// M(n) = least such D.  Adapted (variants/, own copy) from src/forest_search.cpp (Leech forest engine, Calhoun Alg 2.7 with
// complete isomorph rejection) by adding a GAP branch: the forcing lemma no longer applies, so at value level t (all values
// < t decided) either t is already a distance, or t is declared a gap (a value that will never be a distance; at most
// g = D - C(n,2) gaps), or t is the weight of the next edge (join two components / attach a new vertex / new disjoint edge).
// Every abstract weighted forest is generated exactly once (parent = remove max-weight edge; Aut = endpoint swaps of
// single-edge components), and the level t is a function of the forest and the gap decisions, so the search tree has no
// redundant nodes.  Prunes (all necessary conditions): all distances distinct and <= D; gaps <= g; t + w_max <= D (any two
// edges of a tree lie on a common path); vertex/component budget; if F is not yet a spanning tree, every component X of F
// must satisfy ceil(hi_X/2) + t <= D (some outside vertex is at distance >= t from X, and >= hi_X/2 from a diametral end),
// and if two components exist ceil(hi_X/2)+ceil(hi_Y/2)+t <= D.
// Output: SOL lines (one per weighted tree up to isomorphism with all distances distinct and <= D), node counts per depth.
// Usage: mdd_forest n D [--shard i K [--shard-level L]] [--nodes L] [-q] [--maxsol S]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <chrono>
#include <algorithm>
using namespace std; typedef uint64_t u64; typedef uint32_t u32;
#ifndef NW
#define NW 4
#endif
struct BS { u64 w[NW];
  void clear() { for (int i = 0; i < NW; i++) w[i] = 0; }
  void set(int i) { w[i >> 6] |= 1ULL << (i & 63); }
  bool test(int i) const { return w[i >> 6] >> (i & 63) & 1; }
  void reset(int i) { w[i >> 6] &= ~(1ULL << (i & 63)); }
  BS shl(int s) const { BS r; r.clear(); int q = s >> 6, b = s & 63; for (int i = NW - 1; i - q >= 0; i--) { int j = i - q; u64 v = w[j] << b; if (b && j - 1 >= 0) v |= w[j - 1] >> (64 - b); r.w[i] = v; } return r; }
  void orw(const BS& o) { for (int i = 0; i < NW; i++) w[i] |= o.w[i]; }
  int count() const { int c = 0; for (int i = 0; i < NW; i++) c += __builtin_popcountll(w[i]); return c; }
  bool inter(const BS& o) const { for (int i = 0; i < NW; i++) if (w[i] & o.w[i]) return true; return false; }
};
static const int MAXV = 20;
static int n, N, E, G; static long long nodes = 0, nsol = 0, depthHist[40], nodeLimit = -1, maxSol = -1; static bool printSol = true, aborted = false;
static int shardI = 0, shardK = 1, shardLevel = 8; static long long shardCnt = 0;
static int dist_[MAXV][MAXV], comp[MAXV], V; static u32 cm[MAXV]; static BS D0[MAXV]; static int hiD[MAXV];   // D0[x] = {0} U {d(x,x') : x' in comp(x)}
static BS R, FULL; static int eu[MAXV], ev[MAXV], ew[MAXV], ne = 0; static int lvl = 1, gaps = 0;
static BS saveD[MAXV][MAXV]; static int saveHi[MAXV][MAXV]; static u32 saveCm[MAXV][2]; static int saveV[MAXV];
static void rec(bool fresh = true);
static void tryAdd(int x, int y, int t, bool ynew) {
  u32 mx = cm[comp[x]], my = ynew ? (1u << y) : cm[comp[y]];
  int ncx = __builtin_popcount(mx), ncy = __builtin_popcount(my);
  BS Dy; int hy; if (ynew) { Dy.clear(); Dy.set(0); hy = 0; } else { Dy = D0[y]; hy = hiD[y]; }
  BS U; U.clear(); BS RnotF; for (int i = 0; i < NW; i++) RnotF.w[i] = R.w[i] | ~FULL.w[i];
  if (ncx <= ncy) { for (u32 m = mx; m; m &= m - 1) { int xi = __builtin_ctz(m); int sh = dist_[xi][x] + t; if (sh + hy > N) return; BS T = Dy.shl(sh); if (T.inter(RnotF) || T.inter(U)) return; U.orw(T); } }
  else { const BS& Dx = D0[x]; int hx = hiD[x]; for (u32 m = my; m; m &= m - 1) { int yj = __builtin_ctz(m); int sh = (ynew ? 0 : dist_[yj][y]) + t; if (sh + hx > N) return; BS T = Dx.shl(sh); if (T.inter(RnotF) || T.inter(U)) return; U.orw(T); } }
  int lv = ne; saveV[lv] = V; int cxid = comp[x], cyid = ynew ? y : comp[y];
  saveCm[lv][0] = cm[cxid]; if (!ynew) saveCm[lv][1] = cm[cyid];
  for (u32 m = mx; m; m &= m - 1) { int xi = __builtin_ctz(m); saveD[lv][xi] = D0[xi]; saveHi[lv][xi] = hiD[xi]; }
  for (u32 m = my; m; m &= m - 1) { int yj = __builtin_ctz(m); saveD[lv][yj] = D0[yj]; saveHi[lv][yj] = hiD[yj]; }
  if (ynew) { V++; comp[y] = y; cm[y] = 1u << y; D0[y].clear(); D0[y].set(0); hiD[y] = 0; }
  for (u32 m = mx; m; m &= m - 1) { int xi = __builtin_ctz(m); for (u32 m2 = my; m2; m2 &= m2 - 1) { int yj = __builtin_ctz(m2); int d = dist_[xi][x] + t + (ynew ? 0 : dist_[yj][y]); dist_[xi][yj] = dist_[yj][xi] = d; } }
  { BS Dx = D0[x]; int hx = hiD[x];
    for (u32 m = mx; m; m &= m - 1) { int xi = __builtin_ctz(m); int sh = dist_[xi][x] + t; D0[xi].orw(Dy.shl(sh)); hiD[xi] = max(hiD[xi], sh + hy); }
    for (u32 m = my; m; m &= m - 1) { int yj = __builtin_ctz(m); int sh = (ynew ? 0 : dist_[yj][y]) + t; D0[yj].orw(Dx.shl(sh)); hiD[yj] = max(hiD[yj], sh + hx); } }
  for (u32 m = my; m; m &= m - 1) comp[__builtin_ctz(m)] = cxid;
  cm[cxid] = mx | my;
  R.orw(U); eu[ne] = x; ev[ne] = y; ew[ne] = t; ne++;
  int savL = lvl; lvl = t + 1;
  rec();
  lvl = savL;
  ne--; for (int i = 0; i < NW; i++) R.w[i] &= ~U.w[i];
  for (u32 m = mx; m; m &= m - 1) { int xi = __builtin_ctz(m); D0[xi] = saveD[lv][xi]; hiD[xi] = saveHi[lv][xi]; }
  for (u32 m = my; m; m &= m - 1) { int yj = __builtin_ctz(m); D0[yj] = saveD[lv][yj]; hiD[yj] = saveHi[lv][yj]; comp[yj] = cyid; }
  cm[cxid] = saveCm[lv][0]; if (!ynew) cm[cyid] = saveCm[lv][1];
  V = saveV[lv];
}
static void rec(bool fresh) {
  if (aborted) return;
  nodes++; depthHist[ne]++;
  if (nodeLimit > 0 && nodes >= nodeLimit) { aborted = true; return; }
  if (ne == E) { if (V == n) { nsol++; if (printSol) { printf("SOL:"); for (int i = 0; i < ne; i++) printf(" %d-%d:%d", eu[i], ev[i], ew[i]); printf("\n"); fflush(stdout); } if (maxSol > 0 && nsol >= maxSol) aborted = true; } return; }
  if (fresh && ne == shardLevel && shardK > 1) { if ((shardCnt++) % shardK != shardI) return; }   // only forests entering level L by an edge; gap-chain descendants stay in the same shard
  int t = lvl; while (t <= N && R.test(t)) t++;
  if (t > N) return;
  int r = E - ne;                                                 // edges still to add, distinct weights >= t: largest >= t + r - 1
  if (ne > 0 && t + r - 1 + ew[ne - 1] > N) return;             // any two edges lie on a common path: w_i + w_j <= N
  if (r >= 2 && 2 * t + 2 * r - 3 > N) return;                   // the two largest future edges
  int ncomp = V - ne; if (E - ne < ncomp - 1 + (n - V)) return;   // each remaining edge fixes at most one unit of deficit
  // diameter prunes: components with the two largest ceil(hi/2)
  { int h1 = 0, h2 = 0; for (int i = 0; i < V; i++) if (comp[i] == i) { int h = (hiD[i] + 1) / 2; if (h > h1) { h2 = h1; h1 = h; } else if (h > h2) h2 = h; }
    if (h1 + h2 + t > N) return; }
  BS RnotF; for (int i = 0; i < NW; i++) RnotF.w[i] = R.w[i] | ~FULL.w[i];
  // (a) gap branch: t is never a distance
  if (gaps < G) { int savL = lvl; gaps++; lvl = t + 1; rec(false); lvl = savL; gaps--; if (aborted) return; }
  // (b) t is the next edge weight
  u32 elig = 0; for (int i = 0; i < V; i++) { u32 c = cm[comp[i]]; if (__builtin_popcount(c) == 2 && (int)__builtin_ctz(c) != i) continue;
    if (hiD[i] + t > N) continue; BS T = D0[i].shl(t); if (T.inter(RnotF)) continue;
    elig |= 1u << i; }
  for (u32 m = elig; m; m &= m - 1) { int x = __builtin_ctz(m); u32 rest = elig & ~cm[comp[x]] & ~((2u << x) - 1); for (u32 m2 = rest; m2; m2 &= m2 - 1) tryAdd(x, __builtin_ctz(m2), t, false); }
  if (V < n) for (u32 m = elig; m; m &= m - 1) tryAdd(__builtin_ctz(m), V, t, true);
  if (V + 2 <= n) { int x = V, y = V + 1; int lv = ne; saveV[lv] = V; V += 2; comp[x] = x; comp[y] = x; cm[x] = (1u << x) | (1u << y); dist_[x][y] = dist_[y][x] = t;
    D0[x].clear(); D0[x].set(0); D0[x].set(t); D0[y] = D0[x]; hiD[x] = hiD[y] = t; R.set(t); eu[ne] = x; ev[ne] = y; ew[ne] = t; ne++; int savL = lvl; lvl = t + 1; rec(); lvl = savL; ne--; R.reset(t); V = saveV[lv]; }
}
int main(int argc, char** argv) {
  if (argc < 3) { fprintf(stderr, "usage: mdd_forest n D [--shard i K] [--shard-level L] [--nodes L] [--maxsol S] [-q]\n"); return 1; }
  n = atoi(argv[1]); N = atoi(argv[2]); E = n - 1; V = 0; R.clear(); FULL.clear(); G = N - n * (n - 1) / 2;
  for (int i = 3; i < argc; i++) {
    if (!strcmp(argv[i], "--shard")) { shardI = atoi(argv[++i]); shardK = atoi(argv[++i]); }
    else if (!strcmp(argv[i], "--shard-level")) shardLevel = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--nodes")) nodeLimit = atoll(argv[++i]);
    else if (!strcmp(argv[i], "--maxsol")) maxSol = atoll(argv[++i]);
    else if (!strcmp(argv[i], "-q")) printSol = false;
  }
  if (G < 0) { printf("{\"n\": %d, \"D\": %d, \"status\": \"DONE\", \"nsol\": 0, \"nodes\": 0, \"time\": 0, \"note\": \"D < C(n,2)\"}\n", n, N); return 0; }
  for (int v = 1; v <= N; v++) FULL.set(v);
  if (n > MAXV - 1 || N > 64 * NW - 2) { fprintf(stderr, "n or D too large for this build (NW=%d)\n", NW); return 1; }
  auto t0 = chrono::steady_clock::now();
  rec();
  double dt = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  printf("{\"n\": %d, \"D\": %d, \"gaps\": %d, \"status\": \"%s\", \"nsol\": %lld, \"nodes\": %lld, \"time\": %.3f, \"shard\": [%d, %d, %d]}\n", n, N, G, aborted ? (maxSol > 0 && nsol >= maxSol ? "SAT_STOP" : "UNKNOWN") : "DONE", nsol, nodes, dt, shardI, shardK, shardLevel);
  fprintf(stderr, "n=%d D=%d nodes=%lld nsol=%lld time=%.2f\ndepth:", n, N, nodes, nsol, dt); for (int d = 0; d <= E; d++) fprintf(stderr, " %d:%lld", d, depthHist[d]); fprintf(stderr, "\n");
  return 0;
}
