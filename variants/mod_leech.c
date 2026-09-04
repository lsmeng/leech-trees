// mod_leech.c -- exact per-topology search for MODULAR LEECH TREES (Leach-Walsh 2011, Leach 2014):
// tree T on n vertices, k = C(n,2)+1, edge labels in Z_k such that the C(n,2) path sums mod k are exactly {1,...,k-1}.
// Method: edges are processed in BFS order from a root, so each new edge (p,c) attaches a new vertex c to the grown subtree;
// its new path sums are d(c,u) = d(p,u) + w (mod k) for every u already placed (and w itself); all must be nonzero and
// pairwise distinct from the used set (bitset of residues).  Symmetry (Leach Thm 3): multiplying all labels by a unit of Z_k
// gives another labeling and the action is free (some path sum is 1), so the first edge is restricted to label 1 (orbits with
// a unit on e0) or to a non-unit (orbits without a unit on e0, each counted phi(k) times).  Reported: raw counts A (w0=1),
// B (w0 non-unit), orbits = A + B/phi(k), plus every labeling (SOL lines) when --print.
// Usage: mod_leech n < topologies.jsonl  (each line {"id":..,"edges":[[u,v],..]})  [--print] [--id I]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
static int n, k, E; static int eu[32], ev[32], ord[32];  // ord: BFS order of edges, ev[ord[i]] is the new vertex
static int dist[32][32]; static int placed[32], nplaced; static u128 used; static long long nodes, cntA, cntB, cur; static int printSol;
static int lab[32]; static int firstEdgeUnit;
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static void rec(int i) {
  nodes++;
  if (i == E) { cur++; if (printSol) { printf("SOL:"); for (int j = 0; j < E; j++) printf(" %d-%d:%d", eu[j], ev[j], lab[j]); printf("\n"); } return; }
  int e = ord[i], p = eu[e], c = ev[e];
  for (int w = 1; w < k; w++) {
    if (i == 0) { int unit = gcd(w, k) == 1; if (unit && w != 1) continue; if (unit != firstEdgeUnit) continue; }
    u128 add = 0; int ok = 1;
    for (int j = 0; j < nplaced; j++) { int u = placed[j]; int d = (dist[p][u] + w) % k; if (d == 0) { ok = 0; break; } u128 b = (u128)1 << d; if ((used | add) & b) { ok = 0; break; } add |= b; }
    if (!ok) continue;
    for (int j = 0; j < nplaced; j++) { int u = placed[j]; dist[c][u] = dist[u][c] = (dist[p][u] + w) % k; }
    dist[c][c] = 0; placed[nplaced++] = c; used |= add; lab[e] = w;
    rec(i + 1);
    nplaced--; used &= ~add;
  }
}
int main(int argc, char** argv) {
  n = atoi(argv[1]); k = n * (n - 1) / 2 + 1; E = n - 1; int onlyId = -1;
  for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "--print")) printSol = 1; else if (!strcmp(argv[i], "--id")) onlyId = atoi(argv[++i]); }
  if (k > 127) { fprintf(stderr, "k too large\n"); return 1; }
  int phi = 0; for (int w = 1; w < k; w++) if (gcd(w, k) == 1) phi++;
  char line[4096];
  while (fgets(line, sizeof line, stdin)) {
    int id = -1; char* q = strstr(line, "\"id\":"); if (q) id = atoi(q + 5); if (onlyId >= 0 && id != onlyId) continue;
    q = strstr(line, "\"edges\":"); if (!q) continue; q += 8; int m = 0;
    while (*q) { while (*q && (*q < '0' || *q > '9')) { if (*q == '}') break; q++; } if (!*q || *q == '}') break; int u = atoi(q); while (*q >= '0' && *q <= '9') q++; while (*q && (*q < '0' || *q > '9')) q++; int v = atoi(q); while (*q >= '0' && *q <= '9') q++; eu[m] = u; ev[m] = v; m++; }
    if (m != E) { fprintf(stderr, "id %d: %d edges != %d\n", id, m, E); continue; }
    // BFS order from a max-degree root; orient edges parent->child
    int deg[32] = {0}; for (int i = 0; i < E; i++) { deg[eu[i]]++; deg[ev[i]]++; }
    int root = 0; for (int v = 0; v < n; v++) if (deg[v] > deg[root]) root = v;
    int seen[32] = {0}, queue[32], qh = 0, qt = 0; seen[root] = 1; queue[qt++] = root; int no = 0; int usedE[32] = {0};
    while (qh < qt) { int x = queue[qh++]; for (int i = 0; i < E; i++) if (!usedE[i]) { int y = -1; if (eu[i] == x) y = ev[i]; else if (ev[i] == x) y = eu[i]; if (y >= 0 && !seen[y]) { usedE[i] = 1; eu[i] = x; ev[i] = y; seen[y] = 1; queue[qt++] = y; ord[no++] = i; } } }
    if (no != E) { fprintf(stderr, "id %d: not a tree\n", id); continue; }
    nodes = 0; cntA = cntB = 0;
    for (firstEdgeUnit = 1; firstEdgeUnit >= 0; firstEdgeUnit--) { nplaced = 0; placed[nplaced++] = root; dist[root][root] = 0; used = 0; cur = 0; rec(0); if (firstEdgeUnit) cntA = cur; else cntB = cur; }
    printf("{\"id\": %d, \"n\": %d, \"k\": %d, \"raw_unit\": %lld, \"raw_nonunit\": %lld, \"orbits\": %.3f, \"nodes\": %lld}\n", id, n, k, cntA, cntB, cntA + (double)cntB / phi, nodes); fflush(stdout);
  }
  return 0;
}
