/* Exhaustive search: does a Golomb ruler with M marks and length <= L exist?
   marks 0=m0<...<m_{M-1}<=L, all pairwise differences distinct.
   Symmetry break: first gap < last gap (rulers are taken up to reversal); we allow equality-free by requiring m1-m0 < m_{M-1}-m_{M-2}, but since we do not know the last gap in advance, we instead require m1 <= L/2 style bound: standard trick: first mark m1 <= (L - ...). Simpler: enforce m1 - m0 <= last gap by post-check is impossible; so we just require m1 <= L/2 (mirror image has first gap+last gap symmetric; at least one of the two orientations has first gap <= last gap and hence first gap <= L/2). Correct and simple. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int M, L; static int marks[64]; static unsigned char used[1024]; static long long nodes=0; static int found=0;
static void dfs(int k){ /* k marks placed */
  if(found) return;
  if(k==M){ found=1; printf("FOUND:"); for(int i=0;i<M;i++) printf(" %d",marks[i]); printf("\n"); return; }
  int last=marks[k-1]; int rem=M-k; /* rem more marks */
  /* minimal extra span for rem more marks: differences among them + to last are distinct positives: need >= rem*(rem+1)/2 */
  int minspan = rem*(rem+1)/2;
  int hi = L - minspan + 1; /* candidate positions p with p + (span for remaining rem-1) <= L: p <= L - (rem-1)*rem/2 */
  hi = L - (rem-1)*rem/2;
  for(int p=last+1;p<=hi;p++){
    if(k==1 && p> L/2) break;
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
  printf("M=%d L=%d found=%d nodes=%lld secs=%ld\n",M,L,found,nodes,(long)(time(0)-t0)); return 0; }
