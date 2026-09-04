/* cr_forest.c -- CLEAN-ROOM implementation of the forced-forest DFS for Leech trees
 * (Calhoun et al. 2007, Alg. 2.7 + Lemma 2.6), written only from the algorithm
 * description in docs/referee-forest.md Sections 1-5 and Calhoun's paper.
 * NOT derived from src/forest_search.cpp (never read).
 *
 * State = forest with distinct positive integer edge weights, all within-component
 * distances distinct.  Next weight t = least positive integer not realised.
 * Children: join two components / attach a leaf / new isolated edge.
 * Reject: repeated distance, distance > N = n(n-1)/2, > n vertices.
 * Isomorph rejection: only automorphisms of a distinct-weight forest without isolated
 * vertices are endpoint swaps of 2-vertex components -> the larger label of every
 * 2-vertex component is never used as an endpoint; joins run over unordered pairs.
 *
 * usage: cr_forest n [--shard i K --level L] [--maxlevel M] [--no-sumrule] [--json]
 * build: clang -O3 -march=native -o cr_forest cr_forest.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#ifndef NW
#define NW 3            /* 64*NW bits >= N+1 */
#endif
#define MAXV 20
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
    uint8_t dist[MAXV][MAXV];  /* within-component distances */
    bs D[MAXV];                /* distances from v to the other vertices of its component */
    uint8_t maxD[MAXV];
    bs R;                      /* realised distances (bit 0 always set) */
    uint8_t eu[MAXE], ev[MAXE], ew[MAXE];
} State;

static int n, N, E;
static int shard_i=0, shard_K=1, shard_L=-1, maxlevel=-1, sumrule=1, quiet=0;
static uint64_t hist[MAXV+1];
static uint64_t shard_counter=0;
static uint64_t nsol=0;
static State stk[MAXV+1];

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

/* apply a child of stk[lev] into stk[lev+1] and recurse */
static void child_join(int lev, int x, int y, int t, const bs *U){
    State *p=&stk[lev], *c=&stk[lev+1];
    memcpy(c,p,sizeof(State));
    int cx=c->comp[x], cy=c->comp[y];
    uint32_t mx=c->cmask[cx], my=c->cmask[cy];
    /* update D and dist */
    for(uint32_t m=mx;m;m&=m-1){ int a=__builtin_ctz(m); int sh=c->dist[a][x]+t; bs T; bs_shl1(&T,&p->D[y],sh); bs_or(&c->D[a],&T);
        int md=sh+p->maxD[y]; if(md>c->maxD[a]) c->maxD[a]=md;
        for(uint32_t m2=my;m2;m2&=m2-1){ int b=__builtin_ctz(m2); int d=sh+p->dist[y][b]; c->dist[a][b]=d; c->dist[b][a]=d; } }
    for(uint32_t m=my;m;m&=m-1){ int b=__builtin_ctz(m); int sh=c->dist[b][y]+t; bs T; bs_shl1(&T,&p->D[x],sh); bs_or(&c->D[b],&T);
        int md=sh+p->maxD[x]; if(md>c->maxD[b]) c->maxD[b]=md; }
    bs_or(&c->R,U);
    int nid = cx<cy?cx:cy, oid = cx<cy?cy:cx;
    c->cmask[nid]=mx|my; c->cmask[oid]=0;
    for(uint32_t m=c->cmask[oid==cx?cx:cy] , mm=(oid==cx?mx:my); mm; mm&=mm-1){ (void)m; c->comp[__builtin_ctz(mm)]=nid; }
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
    if(s->ne==E){ /* connected tree on n vertices: all N distances distinct and <= N => {1..N} */
        if(s->V!=n || bs_popcount(&s->R)!=N+1){ fprintf(stderr,"INTERNAL: bad leaf\n"); exit(2); }
        nsol++; print_solution(s); return;
    }
    if(lev==shard_L){ uint64_t idx=shard_counter++; if((int)(idx%shard_K)!=shard_i) return; }
    if(lev==maxlevel) return;
    int t=lowest_missing(&s->R);
    if(t>N){ fprintf(stderr,"INTERNAL: t>N without solution\n"); exit(2); }
    if(sumrule && s->ne>0 && t+s->ew[s->ne-1]>N) return;
    /* eligibility + attach translate per vertex */
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
            /* iterate over the smaller component */
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
    if(s->V+1<=n) for(int x=0;x<s->V;x++) if(elig[x]) child_attach(lev,x,t,&TA[x]);
    /* new isolated edge */
    if(s->V+2<=n && t<=N) child_new(lev,t);
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: %s n [--shard i K --level L] [--maxlevel M] [--no-sumrule] [-q]\n",argv[0]); return 1; }
    n=atoi(argv[1]); N=n*(n-1)/2; E=n-1;
    for(int i=2;i<argc;i++){
        if(!strcmp(argv[i],"--shard")&&i+2<argc){ shard_i=atoi(argv[++i]); shard_K=atoi(argv[++i]); }
        else if(!strcmp(argv[i],"--level")&&i+1<argc) shard_L=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--maxlevel")&&i+1<argc) maxlevel=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--no-sumrule")) sumrule=0; else if(!strcmp(argv[i],"--sumrule")) sumrule=1;
        else if(!strcmp(argv[i],"-q")) quiet=1;
        else { fprintf(stderr,"unknown arg %s\n",argv[i]); return 1; }
    }
    if(n<2||n>MAXV||N+1>64*NW){ fprintf(stderr,"n out of range for this build (MAXV=%d, NW=%d)\n",MAXV,NW); return 1; }
    if(shard_K>1 && shard_L<0){ fprintf(stderr,"--shard needs --level\n"); return 1; }
    if(shard_i<0||shard_i>=shard_K){ fprintf(stderr,"shard index out of range\n"); return 1; }
    memset(stk,0,sizeof stk); memset(hist,0,sizeof hist);
    stk[0].R.w[0]=1ULL; /* bit 0 */
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    dfs(0);
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double secs=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    uint64_t total=0; for(int l=0;l<=E;l++) total+=hist[l];
    printf("{\"n\":%d,\"shard\":[%d,%d,%d],\"maxlevel\":%d,\"sumrule\":%d,\"levels\":[",n,shard_i,shard_K,shard_L,maxlevel,sumrule);
    for(int l=0;l<=E;l++) printf("%s%llu",l?",":"",(unsigned long long)hist[l]);
    printf("],\"nodes\":%llu,\"nsol\":%llu,\"level_L_nodes\":%llu,\"secs\":%.3f,\"status\":\"DONE\"}\n",
        (unsigned long long)total,(unsigned long long)nsol,(unsigned long long)shard_counter,secs);
    return 0;
}
