// mdd_topo.c -- independent-method cross-check for M(n): per-topology DFS (no forcing lemma, no forest, no isomorph rejection).
// For a fixed unlabeled tree, edges are assigned in BFS order from a max-degree root (each new edge attaches a new vertex c to
// parent p), weight w in [1, D]; new distances d(c,u) = d(p,u) + w for all placed u must be pairwise distinct, unused and <= D
// (bitset).  Prunes: distinct edge weights (an edge is a distance); Hall-type count: remaining pairs to realise <= free values;
// w + max placed distance from p <= D (necessary for the new distances).  Counts all labelings (raw, i.e. not modulo Aut).
// Usage: mdd_topo n D < topologies.jsonl [--print] [--id I]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
#define NW 4
static int n, D, E; static int eu[32], ev[32], ord[32]; static int dist[32][32]; static int placed[32], nplaced; static u64 used[NW]; static long long nodes, cur; static int printSol; static int lab[32];
static inline int tst(int d) { return (used[d >> 6] >> (d & 63)) & 1; }
static void rec(int i) {
  nodes++;
  if (i == E) { cur++; if (printSol) { printf("SOL:"); for (int j = 0; j < E; j++) printf(" %d-%d:%d", eu[j], ev[j], lab[j]); printf("\n"); } return; }
  int e = ord[i], p = eu[e], c = ev[e];
  int hp = 0; for (int j = 0; j < nplaced; j++) if (dist[p][placed[j]] > hp) hp = dist[p][placed[j]];
  // count prune: pairs still to realise (all pairs not both placed) vs unused values in [1, D]
  int cnt = 0; for (int q = 0; q < NW; q++) cnt += __builtin_popcountll(used[q]);
  int realised = nplaced * (nplaced - 1) / 2; if (n * (n - 1) / 2 - realised > D - cnt) return;
  for (int w = 1; w + hp <= D; w++) {
    u64 add[NW] = {0, 0, 0, 0}; int ok = 1;
    for (int j = 0; j < nplaced; j++) { int u = placed[j]; int d = dist[p][u] + w; if (tst(d) || ((add[d >> 6] >> (d & 63)) & 1)) { ok = 0; break; } add[d >> 6] |= 1ULL << (d & 63); }
    if (!ok) continue;
    for (int j = 0; j < nplaced; j++) { int u = placed[j]; dist[c][u] = dist[u][c] = dist[p][u] + w; }
    dist[c][c] = 0; placed[nplaced++] = c; for (int q = 0; q < NW; q++) used[q] |= add[q]; lab[e] = w;
    rec(i + 1);
    nplaced--; for (int q = 0; q < NW; q++) used[q] &= ~add[q];
  }
}
int main(int argc, char** argv) {
  n = atoi(argv[1]); D = atoi(argv[2]); E = n - 1; int onlyId = -1;
  for (int i = 3; i < argc; i++) { if (!strcmp(argv[i], "--print")) printSol = 1; else if (!strcmp(argv[i], "--id")) onlyId = atoi(argv[++i]); }
  char line[8192];
  while (fgets(line, sizeof line, stdin)) {
    int id = -1; char* q = strstr(line, "\"id\":"); if (q) id = atoi(q + 5); if (onlyId >= 0 && id != onlyId) continue;
    q = strstr(line, "\"edges\":"); if (!q) continue; q += 8; int m = 0;
    while (*q) { while (*q && (*q < '0' || *q > '9')) { if (*q == '}') break; q++; } if (!*q || *q == '}') break; int u = atoi(q); while (*q >= '0' && *q <= '9') q++; while (*q && (*q < '0' || *q > '9')) q++; int v = atoi(q); while (*q >= '0' && *q <= '9') q++; eu[m] = u; ev[m] = v; m++; }
    if (m != E) { fprintf(stderr, "id %d: %d edges != %d\n", id, m, E); continue; }
    int deg[32] = {0}; for (int i = 0; i < E; i++) { deg[eu[i]]++; deg[ev[i]]++; }
    int root = 0; for (int v = 0; v < n; v++) if (deg[v] > deg[root]) root = v;
    int seen[32] = {0}, queue[32], qh = 0, qt = 0; seen[root] = 1; queue[qt++] = root; int no = 0; int usedE[32] = {0};
    while (qh < qt) { int x = queue[qh++]; for (int i = 0; i < E; i++) if (!usedE[i]) { int y = -1; if (eu[i] == x) y = ev[i]; else if (ev[i] == x) y = eu[i]; if (y >= 0 && !seen[y]) { usedE[i] = 1; eu[i] = x; ev[i] = y; seen[y] = 1; queue[qt++] = y; ord[no++] = i; } } }
    nodes = 0; cur = 0; nplaced = 0; placed[nplaced++] = root; dist[root][root] = 0; memset(used, 0, sizeof used);
    rec(0);
    printf("{\"id\": %d, \"n\": %d, \"D\": %d, \"raw_sols\": %lld, \"nodes\": %lld}\n", id, n, D, cur, nodes); fflush(stdout);
  }
  return 0;
}
