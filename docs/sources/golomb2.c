#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
/* G[m] = optimal Golomb ruler length for m marks, used ONLY as pruning bounds; values for m<=13 verified by golomb.c above; 14,15 are literature (127,151) and are only used when searching M>=15/16 */
static int G[]={0,0,1,3,6,11,17,25,34,44,55,72,85,106,127,151,177,199};
static int M, L; static int marks[64]; static unsigned char used[1024]; static long long nodes=0; static int found=0;
static void dfs(int k){
  if(found) return;
  if(k==M){ found=1; printf("FOUND:"); for(int i=0;i<M;i++) printf(" %d",marks[i]); printf("\n"); return; }
  int last=marks[k-1]; int rem=M-k;
  int hi = L - G[rem]; /* after placing p, need rem-1 more marks: span >= G[rem] (rem marks incl p) */
  for(int p=last+1;p<=hi;p++){
    if(k==1 && p> L/2) break;
    if(k==1 && p + G[M-1] > L) break;
    int ok=1; for(int i=0;i<k;i++){ if(used[p-marks[i]]){ok=0;break;} }
    if(!ok) continue;
    nodes++;
    for(int i=0;i<k;i++) used[p-marks[i]]=1;
    marks[k]=p; dfs(k+1);
    for(int i=0;i<k;i++) used[p-marks[i]]=0;
    if(found) return;
  }
}
int main(int argc,char**argv){ M=atoi(argv[1]); L=atoi(argv[2]); memset(used,0,sizeof used); marks[0]=0; time_t t0=time(0); dfs(1);
  printf("M=%d L=%d found=%d nodes=%lld secs=%ld\n",M,L,found,nodes,(long)(time(0)-t0)); fflush(stdout); return 0; }
