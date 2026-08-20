/* Max d such that there is a set W of d distinct positive integers with:
   all pairwise sums w_i+w_j (i<j) distinct, no sum equals an element, all elements and sums <= S.
   (Necessary condition on the edge weights at a vertex of degree d in a Leech tree of order n, S=C(n,2).)
   DFS in increasing order; elements+sums tracked in a 'used' array. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int S,D; static int w[64]; static unsigned char used[2048]; static long long nodes=0; static int found=0;
static void dfs(int k){
  if(found) return;
  if(k==D){found=1; printf("FOUND d=%d:",D); for(int i=0;i<D;i++) printf(" %d",w[i]); printf("\n"); return;}
  int lo = k? w[k-1]+1 : 1;
  /* the two largest remaining must sum <= S; if k>=1: p + (largest later) <= S; crude: p + (p+1) <= S when D-k>=2 */
  for(int p=lo;p<=S;p++){
    if(D-k>=2 && 2*p+1 > S) break;
    if(k>=1 && p + w[k-1] > S) break;
    if(used[p]) continue;
    int ok=1;
    for(int i=0;i<k;i++){ int s=w[i]+p; if(s>S||used[s]){ok=0;break;} }
    if(!ok) continue;
    /* also sums must be distinct among themselves for this p: s_i = w_i + p distinct automatically since w_i distinct */
    nodes++;
    used[p]=1; for(int i=0;i<k;i++) used[w[i]+p]=1;
    w[k]=p; dfs(k+1);
    used[p]=0; for(int i=0;i<k;i++) used[w[i]+p]=0;
    if(found) return;
  }
}
int main(int argc,char**argv){ S=atoi(argv[1]); D=atoi(argv[2]); memset(used,0,sizeof used); dfs(0);
 printf("S=%d D=%d found=%d nodes=%lld\n",S,D,found,nodes); return 0;}
