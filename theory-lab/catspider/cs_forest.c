/* cs_forest.c -- forced-forest DFS for Leech trees RESTRICTED to structured shapes
 * (caterpillars / spiders), adapted from the validated clean-room engine
 * cleanroom/cr_forest.c (same algorithm, same node ordering, same sharding);
 * differences: (1) --shape all|cat|spider adds shape pruning, (2) MAXV=28 and
 * 16-bit distances so orders 25 and 27 (N=300, 351) fit, (3) NW is compile-time.
 *
 * Shape pruning (only for --shape cat / spider; PROVED necessary conditions):
 *  A forced forest of a Leech tree T is a subgraph of T, and vertex degrees only
 *  grow, so:
 *  - cat: every component of a subforest of a caterpillar is a caterpillar
 *    (non-leaf vertices of a subtree are non-leaves of T, they lie on T's spine
 *    path and induce a path). Test: no vertex has >= 3 neighbours of degree >= 2.
 *    Also #\{v : deg(v) >= 2\} <= Dmax(n) - 1, because in a caterpillar the
 *    non-leaf vertices are exactly the interior of the (hop-)diameter path, and
 *    the hop diameter D satisfies OGR(D+1) <= N (Golomb ruler bound, Lemma 3).
 *  - spider: at most ONE vertex of degree >= 3 in the whole forest (degrees only
 *    grow; a spider has at most one such vertex). Also every component's hop
 *    diameter <= Dmax(n) (a component path of h hops is a path of the final tree).
 *  OGR lengths for m marks (literature: Shearer / distributed.net OGR project,
 *  confirmed optimal through 28 marks): see ogr[] below.
 *
 * usage: cs_forest n [--shape all|cat|spider] [--shard i K --level L]
 *                    [--maxlevel M] [--no-sumrule]
 * build: clang -O3 -DNW=3 -o cs_forest_nw3 cs_forest.c   (n <= 20)
 *        clang -O3 -DNW=5 -o cs_forest_nw5 cs_forest.c   (n = 25)
 *        clang -O3 -DNW=6 -o cs_forest_nw6 cs_forest.c   (n = 27)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#ifndef NW
#define NW 3            /* 64*NW bits >= N+1 */
#endif
#define MAXV 28
#define MAXE (MAXV-1)

typedef struct { uint64_t w[NW]; } bs;

static inline void bs_or(bs *a, const bs *b){ for(int i=0;i<NW;i++) a->w[i]|=b->w[i]; }
static inline int  bs_and_any(const bs *a, const bs *b){ uint64_t r=0; for(int i=0;i<NW;i++) r|=a->w[i]&b->w[i]; return r!=0; }
static inline int  bs_popcount(const bs *a){ int c=0; for(int i=0;i<NW;i++) c+=__builtin_popcountll(a->w[i]); return c; }
static inline void bs_set(bs *a, int b){ a->w[b>>6] |= 1ULL<<(b&63); }
/* out = (a | bit0) << s ; caller guarantees the result fits in NW words */
static inline void bs_shl1(bs *out, const bs *a, int s){
    int q = s>>6, r = s&63;
    uint64_t src[NW];
    for(int i=0;i<NW;i++) src[i]=a->w[i];
    src[0] |= 1ULL;
    for(int i=0;i<NW;i++) out->w[i]=0;
    for(int i=NW-1;i>=0;i--){
        int j=i-q; if(j<0) break;
        uint64_t v = src[j]<<r;
        if(r && j>0) v |= src[j-1]>>(64-r);
        out->w[i]=v;
    }
}

typedef struct {
    int V, ne;
    uint8_t comp[MAXV];        /* component id = smallest vertex label of the component */
    uint32_t cmask[MAXV];      /* vertex mask of component, indexed by comp id */
    uint16_t dist[MAXV][MAXV]; /* within-component distances */
    bs D[MAXV];                /* distances from v to the other vertices of its component */
    uint16_t maxD[MAXV];
    bs R;                      /* realised distances (bit 0 always set) */
    uint8_t eu[MAXE], ev[MAXE], ew16pad[MAXE]; /* ew below (16-bit weights) */
    uint16_t ew[MAXE];
} State;

#define SHAPE_ALL 0
#define SHAPE_CAT 1
#define SHAPE_SPIDER 2

static int n, N, E;
static int shard_i=0, shard_K=1, shard_L=-1, maxlevel=-1, sumrule=1;
static int shape=SHAPE_ALL, Dmax, deg2cap;
static uint64_t hist[MAXV+1];
static uint64_t shard_counter=0;
static uint64_t nsol=0;
static State stk[MAXV+1];

/* optimal Golomb ruler lengths, ogr[m] = minimal length with m marks (marks 1..28).
 * m<=13 re-verified in this repo (docs/sources/golomb.c); larger: literature
 * (Shearer's tables; distributed.net OGR-24..28 completions). */
static const int ogr[29] = {0,0,1,3,6,11,17,25,34,44,55,72,85,106,127,151,177,
                            199,216,246,283,333,356,372,425,480,492,553,585};

/* ---------- shape tests (necessary conditions; see header comment) ---------- */
/* Build degree table of forest = s plus one extra edge (u,v); v may be s->V (new). */
static int shape_test(const State *s, int u, int v){
    static uint8_t deg[MAXV]; static uint8_t adj[MAXV][MAXV]; static uint8_t nb[MAXV][8]; /* nb unused for cat */
    int V2 = s->V + (v >= s->V ? (u >= s->V ? 2 : 1) : 0);
    memset(deg,0,V2);
    for(int i=0;i<s->ne;i++){ deg[s->eu[i]]++; deg[s->ev[i]]++; }
    deg[u]++; deg[v]++;
    if(shape==SHAPE_SPIDER){
        int nbig=0;
        for(int i=0;i<V2;i++) if(deg[i]>=3) nbig++;
        if(nbig>1) return 0;
        /* hop diameter per component <= Dmax: BFS twice per component */
        static int8_t head[MAXV]; static uint8_t nxtv[2*MAXE], nxte[2*MAXE]; /* adjacency lists */
        static int8_t al[MAXV][4+MAXV]; static uint8_t aln[MAXV];
        memset(aln,0,V2);
        for(int i=0;i<s->ne;i++){ int a=s->eu[i],b=s->ev[i]; al[a][aln[a]++]=b; al[b][aln[b]++]=a; }
        al[u][aln[u]++]=v; al[v][aln[v]++]=u;
        (void)head;(void)nxtv;(void)nxte;(void)adj;(void)nb;
        static int8_t hd[MAXV]; static uint8_t q[MAXV]; static uint8_t seen[MAXV];
        memset(seen,0,V2);
        for(int seed=0;seed<V2;seed++){
            if(seen[seed]) continue;
            /* BFS 1 from seed */
            int qh=0,qt=0,far=seed;
            memset(hd,-1,V2); hd[seed]=0; q[qt++]=seed;
            while(qh<qt){ int x=q[qh++]; seen[x]=1; if(hd[x]>hd[far]) far=x;
                for(int k2=0;k2<aln[x];k2++){ int y=al[x][k2]; if(hd[y]<0){ hd[y]=hd[x]+1; q[qt++]=y; } } }
            /* BFS 2 from far */
            int ecc=0; qh=qt=0;
            memset(hd,-1,V2); hd[far]=0; q[qt++]=far;
            while(qh<qt){ int x=q[qh++]; if(hd[x]>ecc) ecc=hd[x];
                for(int k2=0;k2<aln[x];k2++){ int y=al[x][k2]; if(hd[y]<0){ hd[y]=hd[x]+1; q[qt++]=y; } } }
            if(ecc>Dmax) return 0;
        }
        return 1;
    }
    /* caterpillar */
    int n2=0;
    for(int i=0;i<V2;i++) if(deg[i]>=2) n2++;
    if(n2>deg2cap) return 0;
    /* coreN(v) = # neighbours of degree>=2 ; caterpillar forest iff all coreN<=2 */
    static uint8_t coreN[MAXV];
    memset(coreN,0,V2);
    for(int i=0;i<s->ne;i++){ int a=s->eu[i],b=s->ev[i];
        if(deg[a]>=2&&deg[b]>=2){ if(++coreN[a]>2) return 0; if(++coreN[b]>2) return 0; } }
    if(deg[u]>=2&&deg[v]>=2){ if(++coreN[u]>2) return 0; if(++coreN[v]>2) return 0; }
    return 1;
}

static void print_solution(const State *s){
    printf("SOL:");
    for(int i=0;i<s->ne;i++) printf(" %d-%d:%d", s->eu[i], s->ev[i], s->ew[i]);
    printf("\n"); fflush(stdout);
}

static int lowest_missing(const bs *R){ /* least b>=1 with bit b clear; bit 0 is set */
    for(int i=0;i<NW;i++){ uint64_t x=~R->w[i]; if(x) return i*64+__builtin_ctzll(x); }
    return 64*NW;
}

static void dfs(int lev);

static void child_join(int lev, int x, int y, int t, const bs *U){
    State *p=&stk[lev], *c=&stk[lev+1];
    memcpy(c,p,sizeof(State));
    int cx=c->comp[x], cy=c->comp[y];
    uint32_t mx=c->cmask[cx], my=c->cmask[cy];
    for(uint32_t m=mx;m;m&=m-1){ int a=__builtin_ctz(m); int sh=c->dist[a][x]+t; bs T; bs_shl1(&T,&p->D[y],sh); bs_or(&c->D[a],&T);
        int md=sh+p->maxD[y]; if(md>c->maxD[a]) c->maxD[a]=md;
        for(uint32_t m2=my;m2;m2&=m2-1){ int b=__builtin_ctz(m2); int d=sh+p->dist[y][b]; c->dist[a][b]=d; c->dist[b][a]=d; } }
    for(uint32_t m=my;m;m&=m-1){ int b=__builtin_ctz(m); int sh=c->dist[b][y]+t; bs T; bs_shl1(&T,&p->D[x],sh); bs_or(&c->D[b],&T);
        int md=sh+p->maxD[x]; if(md>c->maxD[b]) c->maxD[b]=md; }
    bs_or(&c->R,U);
    int nid = cx<cy?cx:cy, oid = cx<cy?cy:cx;
    c->cmask[nid]=mx|my; c->cmask[oid]=0;
    for(uint32_t mm=(oid==cx?mx:my); mm; mm&=mm-1){ c->comp[__builtin_ctz(mm)]=nid; }
    c->eu[c->ne]=x; c->ev[c->ne]=y; c->ew[c->ne]=t; c->ne++;
    dfs(lev+1);
}
static void child_attach(int lev, int x, int t, const bs *T){
    State *p=&stk[lev], *c=&stk[lev+1];
    memcpy(c,p,sizeof(State));
    int v=c->V; int cx=c->comp[x];
    c->D[v]=*T; c->maxD[v]=t+p->maxD[x];
    for(uint32_t m=c->cmask[cx];m;m&=m-1){ int a=__builtin_ctz(m); int d=c->dist[a][x]+t; c->dist[a][v]=d; c->dist[v][a]=d; bs_set(&c->D[a],d); if(d>c->maxD[a]) c->maxD[a]=d; }
    bs_or(&c->R,T);
    c->comp[v]=cx; c->cmask[cx]|=1u<<v; c->V++;
    c->eu[c->ne]=x; c->ev[c->ne]=v; c->ew[c->ne]=t; c->ne++;
    dfs(lev+1);
}
static void child_new(int lev, int t){
    State *p=&stk[lev], *c=&stk[lev+1];
    memcpy(c,p,sizeof(State));
    (void)p;
    int a=c->V, b=c->V+1;
    memset(&c->D[a],0,sizeof(bs)); memset(&c->D[b],0,sizeof(bs));
    bs_set(&c->D[a],t); bs_set(&c->D[b],t); c->maxD[a]=c->maxD[b]=t;
    c->dist[a][b]=c->dist[b][a]=t; c->dist[a][a]=c->dist[b][b]=0;
    bs_set(&c->R,t);
    c->comp[a]=a; c->comp[b]=a; c->cmask[a]=(1u<<a)|(1u<<b); c->cmask[b]=0;
    c->V+=2;
    c->eu[c->ne]=a; c->ev[c->ne]=b; c->ew[c->ne]=t; c->ne++;
    dfs(lev+1);
}

static void dfs(int lev){
    State *s=&stk[lev];
    hist[lev]++;
    if(s->ne==E){
        if(s->V!=n || bs_popcount(&s->R)!=N+1){ fprintf(stderr,"INTERNAL: bad leaf\n"); exit(2); }
        nsol++; print_solution(s); return;
    }
    if(lev==shard_L){ uint64_t idx=shard_counter++; if((int)(idx%shard_K)!=shard_i) return; }
    if(lev==maxlevel) return;
    int t=lowest_missing(&s->R);
    if(t>N){ fprintf(stderr,"INTERNAL: t>N without solution\n"); exit(2); }
    if(sumrule && s->ne>0 && t+s->ew[s->ne-1]>N) return;
    int elig[MAXV]; bs TA[MAXV];
    for(int i=0;i<s->V;i++){
        elig[i]=0;
        int c=s->comp[i]; uint32_t cm=s->cmask[c];
        if(__builtin_popcount(cm)==2 && __builtin_ctz(cm)!=i) continue;   /* isomorph rejection */
        if(t+s->maxD[i]>N) continue;
        bs_shl1(&TA[i],&s->D[i],t);
        if(bs_and_any(&TA[i],&s->R)) continue;
        elig[i]=1;
    }
    /* joins */
    for(int x=0;x<s->V;x++){ if(!elig[x]) continue;
        for(int y=x+1;y<s->V;y++){ if(!elig[y]) continue;
            int cx=s->comp[x], cy=s->comp[y]; if(cx==cy) continue;
            if(shape!=SHAPE_ALL && !shape_test(s,x,y)) continue;
            int px=x, py=y; if(__builtin_popcount(s->cmask[cx])>__builtin_popcount(s->cmask[cy])){ px=y; py=x; }
            bs U; memset(&U,0,sizeof U); int ok=1;
            for(uint32_t m=s->cmask[s->comp[px]];m;m&=m-1){ int a=__builtin_ctz(m); int sh=s->dist[a][px]+t;
                if(sh+s->maxD[py]>N){ ok=0; break; }
                bs T; bs_shl1(&T,&s->D[py],sh);
                if(bs_and_any(&T,&s->R)||bs_and_any(&T,&U)){ ok=0; break; }
                bs_or(&U,&T); }
            if(ok) child_join(lev,x,y,t,&U);
        } }
    /* attachments */
    if(s->V+1<=n) for(int x=0;x<s->V;x++) if(elig[x]){
        if(shape!=SHAPE_ALL && !shape_test(s,x,s->V)) continue;
        child_attach(lev,x,t,&TA[x]);
    }
    /* new isolated edge (always shape-ok) */
    if(s->V+2<=n && t<=N) child_new(lev,t);
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: %s n [--shape all|cat|spider] [--shard i K --level L] [--maxlevel M] [--no-sumrule]\n",argv[0]); return 1; }
    n=atoi(argv[1]); N=n*(n-1)/2; E=n-1;
    const char *shname="all";
    for(int i=2;i<argc;i++){
        if(!strcmp(argv[i],"--shard")&&i+2<argc){ shard_i=atoi(argv[++i]); shard_K=atoi(argv[++i]); }
        else if(!strcmp(argv[i],"--level")&&i+1<argc) shard_L=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--maxlevel")&&i+1<argc) maxlevel=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--no-sumrule")) sumrule=0; else if(!strcmp(argv[i],"--sumrule")) sumrule=1;
        else if(!strcmp(argv[i],"--shape")&&i+1<argc){ shname=argv[++i];
            if(!strcmp(shname,"all")) shape=SHAPE_ALL;
            else if(!strcmp(shname,"cat")) shape=SHAPE_CAT;
            else if(!strcmp(shname,"spider")) shape=SHAPE_SPIDER;
            else { fprintf(stderr,"bad shape %s\n",shname); return 1; } }
        else { fprintf(stderr,"unknown arg %s\n",argv[i]); return 1; }
    }
    if(n<2||n>MAXV||N+1>64*NW){ fprintf(stderr,"n out of range for this build (MAXV=%d, NW=%d)\n",MAXV,NW); return 1; }
    if(shard_K>1 && shard_L<0){ fprintf(stderr,"--shard needs --level\n"); return 1; }
    if(shard_i<0||shard_i>=shard_K){ fprintf(stderr,"shard index out of range\n"); return 1; }
    Dmax=1; while(Dmax+1<=28 && ogr[Dmax+1]<=N) Dmax++; Dmax--; /* max D with ogr[D+1]<=N */
    deg2cap = Dmax-1;
    memset(stk,0,sizeof stk); memset(hist,0,sizeof hist);
    stk[0].R.w[0]=1ULL;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    dfs(0);
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double secs=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    uint64_t total=0; for(int l=0;l<=E;l++) total+=hist[l];
    printf("{\"n\":%d,\"shape\":\"%s\",\"Dmax\":%d,\"shard\":[%d,%d,%d],\"maxlevel\":%d,\"sumrule\":%d,\"levels\":[",n,shname,Dmax,shard_i,shard_K,shard_L,maxlevel,sumrule);
    for(int l=0;l<=E;l++) printf("%s%llu",l?",":"",(unsigned long long)hist[l]);
    printf("],\"nodes\":%llu,\"nsol\":%llu,\"level_L_nodes\":%llu,\"secs\":%.3f,\"status\":\"DONE\"}\n",
        (unsigned long long)total,(unsigned long long)nsol,(unsigned long long)shard_counter,secs);
    return 0;
}
