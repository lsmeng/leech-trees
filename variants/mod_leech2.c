// mod_leech2.c -- modular Leech trees, per-topology DFS, version 2 of mod_leech.c with
//  (a) complete unit-group symmetry breaking: the label vector (in BFS edge order) must be the lexicographically smallest in
//      its orbit under U(k) (multiplication by units, Leach 2014 Thm 3): maintain the set of units fixing the prefix; a new
//      label w is allowed only if u*w >= w (mod k, as integers 1..k-1) for every such unit u; then keep the units with u*w == w.
//      Every orbit is generated exactly once -> counts are orbit counts directly.
//  (b) forward checking: after each assignment, every pending edge (parent placed, child not) must still have some label w
//      whose translate D(parent)+w avoids the used residues; otherwise prune.
// Cross-checked against mod_leech.c (orbit counts) on n <= 10.  Usage: mod_leech2 n < topologies.jsonl [--print] [--id I] [--nofc]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
static int n, k, E; static int eu[32], ev[32], ord[32]; static int dist[32][32]; static int placed[32], nplaced; static u128 used; static long long nodes, cur; static int printSol, useFC = 1;
static int lab[32]; static int units[128], nunits; static int stab[32][128], nstab[32];   // stab[i] = units fixing labels of edges ord[0..i-1]
static int isPlaced[32];
static u128 Dset[32];  // Dset[v] = bitset of residues d(v,u) for placed u (u != v), maintained incrementally
static int fcOK(int from) {  // every pending edge ord[j], j >= from, whose parent is placed must admit some label
  for (int j = from; j < E; j++) { int p = eu[ord[j]]; if (!isPlaced[p]) continue; u128 Dp = Dset[p]; int any = 0;
    for (int w = 1; w < k && !any; w++) { u128 tr = ((Dp << w) | (Dp >> (k - w))) & (((u128)1 << k) - 1); tr |= (u128)1 << w; if (!(tr & used)) any = 1; }
    if (!any) return 0; }
  return 1;
}
static void rec(int i) {
  nodes++;
  if (i == E) { cur++; if (printSol) { printf("SOL:"); for (int j = 0; j < E; j++) printf(" %d-%d:%d", eu[j], ev[j], lab[j]); printf("\n"); } return; }
  int e = ord[i], p = eu[e], c = ev[e];
  for (int w = 1; w < k; w++) {
    int okS = 1; for (int s = 0; s < nstab[i]; s++) { int u = stab[i][s]; if ((long long)u * w % k < w) { okS = 0; break; } } if (!okS) continue;
    u128 add = 0; int ok = 1;
    for (int j = 0; j < nplaced; j++) { int u = placed[j]; int d = (dist[p][u] + w) % k; if (d == 0) { ok = 0; break; } u128 b = (u128)1 << d; if ((used | add) & b) { ok = 0; break; } add |= b; }
    if (!ok) continue;
    for (int j = 0; j < nplaced; j++) { int u = placed[j]; int d = (dist[p][u] + w) % k; dist[c][u] = dist[u][c] = d; Dset[u] |= (u128)1 << d; }
    dist[c][c] = 0; Dset[c] = add; placed[nplaced++] = c; isPlaced[c] = 1; used |= add; lab[e] = w;
    nstab[i + 1] = 0; for (int s = 0; s < nstab[i]; s++) { int u = stab[i][s]; if ((long long)u * w % k == w) stab[i + 1][nstab[i + 1]++] = u; }
    if (!useFC || fcOK(i + 1)) rec(i + 1);
    nplaced--; isPlaced[c] = 0; used &= ~add;
    for (int j = 0; j < nplaced; j++) { int u = placed[j]; Dset[u] &= ~((u128)1 << dist[c][u]); }
  }
}
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
int main(int argc, char** argv) {
  n = atoi(argv[1]); k = n * (n - 1) / 2 + 1; E = n - 1; int onlyId = -1;
  for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "--print")) printSol = 1; else if (!strcmp(argv[i], "--id")) onlyId = atoi(argv[++i]); else if (!strcmp(argv[i], "--nofc")) useFC = 0; }
  if (k > 127) { fprintf(stderr, "k too large\n"); return 1; }
  nunits = 0; for (int w = 1; w < k; w++) if (gcd(w, k) == 1) units[nunits++] = w;
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
    if (no != E) { fprintf(stderr, "id %d: not a tree\n", id); continue; }
    nodes = 0; cur = 0; nplaced = 0; memset(isPlaced, 0, sizeof isPlaced); memset(Dset, 0, sizeof Dset); placed[nplaced++] = root; isPlaced[root] = 1; dist[root][root] = 0; used = 0;
    nstab[0] = nunits; for (int s = 0; s < nunits; s++) stab[0][s] = units[s];
    rec(0);
    printf("{\"id\": %d, \"n\": %d, \"k\": %d, \"orbits\": %lld, \"nodes\": %lld}\n", id, n, k, cur, nodes); fflush(stdout);
  }
  return 0;
}
