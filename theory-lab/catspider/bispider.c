/* bispider.c -- C port of bispider_topdown.py (top-down exact prover for Leech
 * BI-SPIDERS: trees with at most two vertices of degree >= 3).  The algorithm,
 * case analysis and enumeration order mirror the Python reference line by line;
 * validation = exact node-count agreement with the Python for n <= 13 plus the
 * built-in paranoid recheck (full from-scratch recomputation of the pair-value
 * multiset at every node, always on).
 *
 * usage: bispider n [LR|LL|both] [T-lo T-hi]   (T range restricts the outer
 *        anchor loop of BOTH cases for sharding: LR shards on TL, LL on T1)
 * build: clang -O3 -o bispider bispider.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define NWB 8                    /* 64*NWB bits >= N+1; N<=506 for n<=32 */
#define MAXM 40

static int n, N, Q;
static int capL0, capL1, capR0, capfL, capfR;   /* leg0/leg1 caps; fresh caps */
static uint64_t vals[NWB];
static struct { int8_t side; int8_t leg; int16_t x; } marks[MAXM];
static int nmarks, nlegsL, nlegsR;
static uint64_t nodes=0, nsol=0, branches=0;
static int paranoid=1;

static inline int bit(int w){ return (vals[w>>6]>>(w&63))&1; }
static inline void setb(int w){ vals[w>>6] |= 1ULL<<(w&63); }
static inline void clrb(int w){ vals[w>>6] &= ~(1ULL<<(w&63)); }

static inline int capL(int leg){ return leg==0?capL0 : (leg==1?capL1:capfL); }
static inline int capR(int leg){ return leg==0?capR0 : capfR; }
/* note: capL1 is used only in the LL case (two pre-created L legs); in the LR
 * case capL1 is set equal to capfL so leg 1, if created fresh, gets the fresh cap */

/* pair value of a new mark (side,leg,x) with existing mark i */
static inline int pairval(int side,int leg,int x,int i){
    int s2=marks[i].side, l2=marks[i].leg, y=marks[i].x;
    if(side=='S'&&s2=='S') return abs(x-y);
    if(side=='S') return (s2=='L'? x+y : (Q-x)+y);
    if(s2=='S') return (side=='L'? y+x : (Q-y)+x);
    if(side!=s2) return x+Q+y;
    if(leg==l2) return abs(x-y);
    return x+y;
}
static inline int dL(int side,int x){ return side=='L'?x:(side=='R'?Q+x:x); }
static inline int dR(int side,int x){ return side=='L'?x+Q:(side=='R'?x:Q-x); }

typedef struct { int nvals; int16_t added[MAXM+4]; int wasfreshL, wasfreshR; } Undo;

static int legal(int side,int leg,int x){
    if(x<1) return 0;
    if(side=='L') return x<=capL(leg);
    if(side=='R') return x<=capR(leg);
    return x<Q; /* spine */
}

/* apply mark; returns 1 and fills undo, or 0 (state unchanged) */
static int apply_mark(int side,int leg,int x,Undo*u){
    if(!legal(side,leg,x)) return 0;
    if(nmarks+1>n-2) return 0;
    if(side=='L'&&leg>nlegsL) return 0;
    if(side=='R'&&leg>nlegsR) return 0;
    int nv[MAXM+4]; int k=0;
    nv[k++]=dL(side,x); nv[k++]=dR(side,x);
    for(int i=0;i<nmarks;i++) nv[k++]=pairval(side,leg,x,i);
    /* check range, freshness, internal dup */
    uint64_t tmp[NWB]; memset(tmp,0,sizeof tmp);
    for(int i=0;i<k;i++){
        int w=nv[i];
        if(w<1||w>N) return 0;
        if(bit(w)) return 0;
        if((tmp[w>>6]>>(w&63))&1) return 0;
        tmp[w>>6]|=1ULL<<(w&63);
    }
    u->nvals=k; u->wasfreshL=0; u->wasfreshR=0;
    for(int i=0;i<k;i++){ setb(nv[i]); u->added[i]=nv[i]; }
    if(side=='L'&&leg==nlegsL){ nlegsL++; u->wasfreshL=1; }
    if(side=='R'&&leg==nlegsR){ nlegsR++; u->wasfreshR=1; }
    marks[nmarks].side=side; marks[nmarks].leg=leg; marks[nmarks].x=x; nmarks++;
    return 1;
}
static void undo_mark(const Undo*u){
    for(int i=0;i<u->nvals;i++) clrb(u->added[i]);
    nmarks--;
    if(u->wasfreshL) nlegsL--;
    if(u->wasfreshR) nlegsR--;
}

static void paranoid_check(void){
    int allv[MAXM*MAXM]; int k=0;
    allv[k++]=Q;
    for(int i=0;i<nmarks;i++){
        allv[k++]=dL(marks[i].side,marks[i].x);
        allv[k++]=dR(marks[i].side,marks[i].x);
        for(int j=i+1;j<nmarks;j++)
            allv[k++]=pairval(marks[i].side,marks[i].leg,marks[i].x,j);
    }
    uint64_t tmp[NWB]; memset(tmp,0,sizeof tmp);
    int cnt=0;
    for(int i=0;i<k;i++){
        int w=allv[i];
        if(w<1||w>N){ fprintf(stderr,"PARANOID: range\n"); exit(2); }
        if((tmp[w>>6]>>(w&63))&1){ fprintf(stderr,"PARANOID: dup\n"); exit(2); }
        tmp[w>>6]|=1ULL<<(w&63); cnt++;
    }
    for(int i=0;i<NWB;i++) if(tmp[i]!=vals[i]){ fprintf(stderr,"PARANOID: mismatch\n"); exit(2); }
    (void)cnt;
}

static void report_solution(void){
    nsol++;
    printf("BISPIDER SOL: n=%d Q=%d marks:",n,Q);
    for(int i=0;i<nmarks;i++) printf(" %c%d:%d",marks[i].side,marks[i].leg,marks[i].x);
    printf("\n"); fflush(stdout);
}

static void dfs(int v);
static inline void child1(int v,int side,int leg,int x){
    Undo u;
    if(apply_mark(side,leg,x,&u)){ dfs(v-1); undo_mark(&u); }
}
static inline void child2(int v,int s1,int l1,int x1,int s2,int l2,int x2){
    Undo u1,u2;
    if(x1==x2&&s1==s2&&l1==l2) return;
    if(!apply_mark(s1,l1,x1,&u1)) return;
    /* second mark: if same-side fresh with id == pre-apply nlegs, it now refers
       to the leg just created (same fresh leg); id nlegs(new) is a second fresh */
    if(apply_mark(s2,l2,x2,&u2)){ dfs(v-1); undo_mark(&u2); }
    undo_mark(&u1);
}

static void dfs(int v){
    nodes++;
    if(paranoid) paranoid_check();
    while(v>=1 && bit(v)) v--;
    if(v==0){
        if(nmarks!=n-2){ fprintf(stderr,"INTERNAL: leaf with %d marks\n",nmarks); exit(2); }
        report_solution(); return;
    }
    int nl=nlegsL, nr=nlegsR;
    /* ---- center pairs ---- */
    for(int i=0;i<=nl;i++) child1(v,'L',i,v);
    if(v-Q>=1){
        for(int i=0;i<=nr;i++) child1(v,'R',i,v-Q);
        for(int i=0;i<=nl;i++) child1(v,'L',i,v-Q);
    }
    if(v<Q) child1(v,'S',0,v);
    for(int i=0;i<=nr;i++) child1(v,'R',i,v);
    if(Q-v>0&&Q-v<Q) child1(v,'S',0,Q-v);
    /* ---- one new mark, one pinned partner ---- */
    for(int p=0;p<nmarks;p++){
        int side=marks[p].side, leg=marks[p].leg, y=marks[p].x;
        if(side=='L'){
            int x=v-y;
            if(x>=1) for(int i=0;i<=nl;i++) if(i!=leg) child1(v,'L',i,x);
            child1(v,'L',leg,y+v);
            if(y-v>=1) child1(v,'L',leg,y-v);
            if(v-y>0&&v-y<Q) child1(v,'S',0,v-y);
            if(v-Q-y>=1) for(int i=0;i<=nr;i++) child1(v,'R',i,v-Q-y);
        } else if(side=='R'){
            int x=v-y;
            if(x>=1) for(int i=0;i<=nr;i++) if(i!=leg) child1(v,'R',i,x);
            child1(v,'R',leg,y+v);
            if(y-v>=1) child1(v,'R',leg,y-v);
            if(Q-(v-y)>0&&Q-(v-y)<Q) child1(v,'S',0,Q-(v-y));
            if(v-Q-y>=1) for(int i=0;i<=nl;i++) child1(v,'L',i,v-Q-y);
        } else { /* spine */
            if(y+v<Q) child1(v,'S',0,y+v);
            if(y-v>=1) child1(v,'S',0,y-v);
            if(v-y>=1) for(int i=0;i<=nl;i++) child1(v,'L',i,v-y);
            if(v-(Q-y)>=1) for(int i=0;i<=nr;i++) child1(v,'R',i,v-(Q-y));
        }
    }
    /* ---- both marks new ---- */
    int maxcapL=capfL, maxcapR=capfR;
    for(int i=0;i<nl;i++) if(capL(i)>maxcapL) maxcapL=capL(i);
    for(int i=0;i<nr;i++) if(capR(i)>maxcapR) maxcapR=capR(i);
    /* L-L sum, different legs (i covers existing+1 fresh, j existing+2 fresh) */
    for(int x=1;x<=(v-1)/2;x++){
        int y=v-x; if(x==y) continue;
        if(y<=maxcapL)
            for(int i=0;i<=nl;i++) for(int j=0;j<=nl+1;j++){
                if(i==j) continue;
                if(j==nl+1&&i!=nl) continue;   /* second fresh only after first */
                child2(v,'L',i,x,'L',j,y); }
        if(y<=maxcapR)
            for(int i=0;i<=nr;i++) for(int j=0;j<=nr+1;j++){
                if(i==j) continue;
                if(j==nr+1&&i!=nr) continue;
                child2(v,'R',i,x,'R',j,y); }
    }
    /* same-leg diff both new: (x, x+v) */
    for(int x=1;x+v<=maxcapL;x++)
        for(int i=0;i<=nl;i++) child2(v,'L',i,x,'L',i,x+v);
    for(int x=1;x+v<=maxcapR;x++)
        for(int i=0;i<=nr;i++) child2(v,'R',i,x,'R',i,x+v);
    /* S-S both new */
    for(int s=1;s+v<Q;s++) child2(v,'S',0,s,'S',0,s+v);
    /* L-S both new: b+s=v */
    for(int s=1;s<Q&&s<v;s++){
        int b=v-s;
        if(b>=1) for(int i=0;i<=nl;i++) child2(v,'L',i,b,'S',0,s);
    }
    /* S-R both new: (Q-s)+c=v */
    for(int s=1;s<Q;s++){
        int c=v-(Q-s);
        if(c>=1) for(int i=0;i<=nr;i++) child2(v,'R',i,c,'S',0,s);
    }
    /* L-R both new: b+Q+c=v */
    for(int b=1;b<v-Q;b++){
        int c=v-Q-b;
        if(c>=1) for(int i=0;i<=nl;i++) for(int j=0;j<=nr;j++) child2(v,'L',i,b,'R',j,c);
    }
}

static void run_branch(int Q_,int cL0,int cL1,int cfL,int cR0,int cfR,
                       int tipsL[2],int ntipsL,int tipR,int hasR){
    Q=Q_; capL0=cL0; capL1=cL1; capfL=cfL; capR0=cR0; capfR=cfR;
    memset(vals,0,sizeof vals); nmarks=0; nlegsL=0; nlegsR=0;
    if(Q<1||Q>N) return;
    setb(Q);
    Undo us[3]; int nu=0; int ok=1;
    for(int i=0;i<ntipsL&&ok;i++) ok=apply_mark('L',i,tipsL[i],&us[nu++]);
    if(ok&&hasR) ok=apply_mark('R',0,tipR,&us[nu++]);
    if(ok){ branches++; dfs(N-1); }
    /* no undo needed: state reset per branch */
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: %s n [LR|LL|both] [lo hi]\n",argv[0]); return 1; }
    n=atoi(argv[1]); N=n*(n-1)/2;
    const char* mode = argc>2?argv[2]:"both";
    int lo=1, hi=N;
    if(argc>4){ lo=atoi(argv[3]); hi=atoi(argv[4]); }
    if(N+1>64*NWB||n+2>MAXM){ fprintf(stderr,"n too big for build\n"); return 1; }
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    if(!strcmp(mode,"LR")||!strcmp(mode,"both")){
        for(int TL=(lo>1?lo:1);TL<=N/2&&TL<=hi;TL++)
            for(int TR=TL+1;TR<=N-TL-1;TR++){
                int tips[2]={TL,0};
                run_branch(N-TL-TR, TL,TL-1,TL-1, TR,TR-1, tips,1, TR,1);
            }
    }
    if(!strcmp(mode,"LL")||!strcmp(mode,"both")){
        for(int T1=(lo>N/2+1?lo:N/2+1);T1<=N-1&&T1<=hi;T1++){
            int T2=N-T1;
            for(int Qv=1;Qv<T2;Qv++){
                int tips[2]={T1,T2};
                int capR_= T2-Qv-1>0 ? T2-Qv-1 : 0;
                run_branch(Qv, T1,T2,T2-1, capR_,capR_, tips,2, 0,0);
            }
        }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double secs=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("{\"n\":%d,\"N\":%d,\"mode\":\"%s\",\"range\":[%d,%d],\"branches\":%llu,"
           "\"nodes\":%llu,\"nsol\":%llu,\"secs\":%.2f,\"status\":\"DONE\"}\n",
        n,N,mode,lo,hi,(unsigned long long)branches,(unsigned long long)nodes,
        (unsigned long long)nsol,secs);
    return 0;
}
