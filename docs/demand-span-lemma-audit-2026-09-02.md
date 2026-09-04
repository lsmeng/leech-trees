# Demand-span 容量引理草稿与审计

日期：2026-09-02  
项目：FW319 exact-return-33 / Leech-tree

## 目的

这是对当前 `P_v -> depth-Hall` 路线的一个更强但仍然必要的容量条件。它的
目标是先在 abstract structure 层排除不可能的 `(s,L)`，而不是替代完整
depth/forest 证书。

## 设置

令 `C0=2m-3`，`B=delta+1-s`。对每个 low-LCA 类 `v`：

- `l_v` 是 low depth；
- `S_v` 是该类 high-high pair 的未平移 raw-sum 集合；
- `P_v` 是该类 pair 数；
- 平移后的真实距离集合为
  `T_v = 2B - 2l_v + S_v`。

高-LCA 类记为 `H`，其真实距离集合落在 `[1,C0]`，pair 数为 `W`。

若某个候选是可行的，则同一 LCA 类内 raw sums 必须无重复，故
`|S_v|=P_v`；不同类的 `T_v` 以及 `H` 彼此必须不交。

## 引理（需求跨度）

对任意 low-class 子集 `Q`，任何可行候选都满足

```text
sum_{v in Q} P_v
  <= C0 + 2*(max_{v in Q} l_v - min_{v in Q} l_v).
```

证明：每个 `T_v` 都包含在长度为 `C0` 的整数区间
`[2B-2l_v+1, 2B-2l_v+C0]` 中。所有这些区间的并包含在由最小和最大
`l_v` 决定的端点区间中，其整数长度为右端减左端加一，即右式。可行性
要求 `T_v` 两两不交，且 `|T_v|=P_v`，所以总基数不超过该长度。证毕。

与高-LCA 类合并，单个 `v` 还满足

```text
W + P_v <= C0 + min(C0, 2*(B-l_v)).
```

因为 `H` 落在 `[1,C0]`，而 `T_v` 落在
`[2B-2l_v+1, 2B-2l_v+C0]`；两段区间的并长度正是右式。若考虑
`[1,delta]` 截断，实际可用集合只会更小，因此不改变必要性方向。

## 边界与反误用

1. 若某个 `S_v` 内部有重复 raw sum，候选已因同类距离碰撞而不可能；不能
   把集合大小误当作 pair 数后继续接受。
2. 若不同 `T_v` 发生交集、或与 `H` 发生交集，直接拒绝；跨度不等式只
   是更便宜的必要条件，不能证明通过。
3. `Q` 可以取任意子集（至多 `2^r` 个）；但只有在 `lowpar`、深度顺序、
   `0<=l_v<B`、以及 `W+sum(P_v)=C(m,2)` 已验证时，所得拒绝才有解释。
4. 这条引理不处理 LL/LH/holes 的全部 owner 约束；因此即使所有不等式
   通过，也只能标为 `necessary-pass`。

## 与纯 component-mass 的关系

`W` 和逐点 `P_v` 容量本身不能关闭所有高层情形。一个最小警示是：在
`r=5,m=19,C0=35` 的 chain 质量剖面中，可以同时有

```text
W=21,
P=(35,31,27,23,34),
W+sum(P)=171=C(19,2),
```

并且每个单点容量都不超 `C0`。因此更有希望的对象是上面的跨类跨度，
而不是继续增强 aggregate `W/P` 计数。

## 证据等级与最小验收

- **VERIFIED（数学方向）**：引理只使用整数区间包络和距离单射；在上述
  设置与边界条件成立时，拒绝方向 sound。
- **CANDIDATE（工程收益）**：对 `delta=284/285` structure corpus 的实际
  削减尚未测量。
- **GAP**：尚未对真实冻结 structure 和 genuine positive controls 做实现
  differential，也没有证明它能单独关闭任一完整 `r=8/9` shape。

最小后续验证：在 Geo Workstation 上用一个 order-6 genuine control、一个
已冻结的 `r=8` structure 和一个 `r=9` structure，独立重建 `S_v,H,P_v,W`，
枚举已有有限 `(s,L)` 输入，比较跨度拒绝与 exact owner checker；要求
`false_rejects=0`，并记录每一层的拒绝数。单进程 `nice -n 15`、有界
`timeout`，不触碰现有远程 arrays。
