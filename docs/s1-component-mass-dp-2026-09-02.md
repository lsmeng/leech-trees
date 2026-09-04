# Component-mass DP：`delta >= 284` 的 sound 预筛

这是一个独立的必要条件预筛，不是完整 forest solver。它把 high vertices
暂时忘掉 label 和具体 parent shape，只记录每个 low vertex 上直接挂着的
high-component 质量分拆 `n_{v,j}`。

对 low tree 的 rooted parent 数组 `lowpar`，令 `M_v` 是 low 子树 `v` 中的
high 总数，令

```text
W_v = sum_j C(n_{v,j}, 2)
W   = sum_v W_v
P_v = C(M_v,2) - sum_{u child of v} C(M_u,2) - W_v
C0  = 2m - 3
```

high-LCA 的 pair 必须落在 `1..C0`，所以任何真实距离单射树都必须满足：

```text
W <= C0
P_v <= C0  for every low vertex v
W + sum_v P_v = C(m,2)
```

其中等式是 pair 按 high LCA 类的精确分拆；前两个是不等式必要条件。
因此脚本只会排除不可能的质量模式，绝不会把一个可能模式当成充分解。

脚本：

`theory-lab/s1_crowding/component_mass_dp.py`

它只生成独立 JSONL/汇总，不读取或覆盖既有结果。由于当前用户要求重计算
放在远程机器，尚未在本机执行；后续可在 Geo Workstation 上对 `m=16,r=8`
和 `m=15,r=9` 的 structure-bearing low shapes 运行，并把通过的质量模式
作为 `abstract_class_search_v4` 的前置过滤候选。

## 验收要求

1. 用小规模手算或独立实现验证整数分拆、`M_v` 反向聚合和 `P_v` 恒等式；
2. 对每个被过滤的模式保存 `lowpar`、质量分拆、`W`、全部 `P_v` 和阈值；
3. 与完整 parent search 的小规模 relaxed target 做差分，确认没有误删；
4. 过滤器只能作为必要条件，最终仍须运行完整 depth CSP/独立 checker。

## 2026-09-02 压缩实现与远程 smoke 验收

完整 local-partition 笛卡尔积在 `m=16,r=8` 上增长过快，因此新增压缩实现：

`theory-lab/s1_crowding/component_mass_dp_compressed.py`

它把每个局部 partition 只按 `(a,w)` 归并，并在每个 low 子树保留可达的
`(M,W)` 状态；父节点只需由子节点质量重算
`Q=sum C(M_child,2)` 和本节点 `P_v`。因为容量过滤器只依赖这些量，
该归并对这个**必要条件测试**是完备的；它没有声称保留完整 high-label
结构，也不能单独证明存在性。

Geo Workstation 远程 smoke（未在本机执行）与原始枚举对照：

```text
m=5, lowpar=-1,0,1
compressed: root_W_states = [0,1,2,3,4,6], root_possible=true
original:   total_mass_patterns=108, necessary_pass_patterns=73
root W 集合相等：true
compressed elapsed=0.05s, MAXRSS=12272 KB, RC=0
```

远程压缩脚本 SHA-256：
`7ed764d97ff45e9eca16e79c48d2d6328f32c3cc99c35a3b58f902587473d162`。
该结果只验证压缩状态在微型例上的接口一致性；在 `m=16/15` 生产使用前，
仍需做一个远程小规模 relaxed-target 差分，并保存完整命令与输出哈希。

## `m=16,r=8` 形状探针结果

对一个当前 structure-bearing 形状
`lowpar=-1,0,0,1,3,4,5,6` 做了远程单进程探针。压缩 DP 在
`0.08s`、`MAXRSS=12568 KB`、`RC=0` 完成，得到
`states_per_vertex=[280,280,84,280,272,215,156,84]`，根节点有
`W=0..29` 的可达状态，因而 `root_possible=true`。

这不是该形状的树存在性结论，也没有排除它；它说明压缩 DP 已经能在
实际 `m=16` 尺度上快速完成必要条件层。生产接入前仍需对其他
structure-bearing shapes 做覆盖，并用独立 relaxed-target checker 验证
没有误删。

远程保存的 summary SHA-256 为
`46a13ff99aa4ae32d1613374c86b598ca0fc1e9ac80820234cc29a257cc63766`，
计时文件 SHA-256 为
`d4b3e16c67767b19350db925ca055459c202d46e5016b5b18503d07c023226c6`。
作为对照，旧的未压缩探针在同一形状上按 `timeout 600` 退出（`RC=124`），
其远程 `.time` SHA-256 为
`b90e0581b51115e43b81e870e929a5bf35cca6f52abe923f315504a7a923432d`；
该超时不是数学上的零结果。

随后在 Geo Workstation 做了 `m=6` 的独立有限差分，比较原始枚举与压缩
状态 DP 的根 `W` 集合，覆盖三个 low-tree 形状：
`chain3=-1,0,1`、`star3=-1,0,0`、`branch4=-1,0,1,1`。三者均得到
`old_W = new_W = [0,1,2,3,4,6,7]`，逐形状 `equal=True`，所有命令均
`RC=0`、单进程 `nice -n 15`、`timeout 120`。差分汇总 TSV 的远程
SHA-256 为
`0b46185ca691b84d40fa6c08f25fef057f40061f7c31b216d90ff4d929fca89d`。
这仍是小规模接口/完备性证据，不是 `delta=284/285` 的最终结论。

## `delta=284,285` structure-bearing shape census

从 Hoffman2 的现有清单读取 7 个 `r=8,m=16` 与 95 个 `r=9,m=15`
structure-bearing rooted low shapes（清单省略根标记，运行时显式补回
`-1`）。在 Geo Workstation 上以一个 `nice -n 15`、`timeout 120` 的
单进程压缩 DP 完成 102 个形状：

```text
r=8,m=16: 7/7 root_possible, 0 excluded
r=9,m=15: 95/95 root_possible, 0 excluded
elapsed=4.61s, MAXRSS=12472 KB, RC=0
```

因此这条最便宜的 shape-level mass-capacity 过滤器在当前
`delta=284,285` structure-bearing 清单上没有排除任何形状；它仍然是
有价值的 sound 预筛，但下一步应把精力放到 `P_v→depth-Hall` 或更强的
global distance-slot flow，而不是期待仅靠 `W/P_v` 完成证明。完整 JSONL
SHA-256 为
`1d807357e5708a9f1b482101ab775b55a6e39b9d8a5078bc01079da4270666ff`，
计时文件 SHA-256 为
`83b0ccb9e404893d7ea6a5c073ccefee012ed76aaad44f434eb0340a8a839c57`。

## Global distance-slot flow（候选下一层）

新增 `theory-lab/s1_crowding/global_distance_slot_flow_pilot.py`。它把
high-LCA 类需求 `W` 和每个 low-LCA 类需求 `P_v` 接到实际距离槽的一个
放宽二分图：high 类允许 `[1,2m-3]`，low 类允许
`{2B-2l_v+t:1<=t<=2m-3}` 与 `[1,delta]` 的交集，并以每个距离槽容量
1 做最大流。由于这些允许集合是实际可用集合的超集，若最大流小于
`W+sum(P_v)=C(m,2)`，则是 sound 必要性排除；最大流通过不代表存在。

Geo Workstation toy 验证（`m=5, delta=10, s=8`）用独立回溯匹配对照
Dinic 流：3 个 fail 案例均 `max_flow<demand` 且与 brute matching
一致；另一个 demand=6 的案例如 `max_flow=demand=6`。脚本 SHA-256 为
`e316dd3dc71bca967f7a3aa474c500b108a7981b45160e4296eb84c220a99228`（旧版，
仅作历史记录）。随后加入输入 guard 的当前版本 SHA-256 为
`ac3c016d28cab791e3ef61eb7ba89458698096522b56d622ffa039f56f339518`。
当前版本远程回归验证：满足 `W+ΣP=C(m,2)` 的 toy 输入返回
`demand=10,max_flow=8,necessary_pass=false`，重复 occupied 槽位被正确
拒绝（`DUPLICATE_GUARD_OK`）；另搜索到合法通过例
`W=2,P=[0,1,7]`、`max_flow=10`。这些仍是候选必要剪枝，尚未接入实际
284/285 structure/depth 结果。

顾问审计要求的生产门槛：独立提供完整结构的 `W`、`P_v`、准确 `(s,L)`、
`lowpar`，并核对 `W+ΣP_v=C(m,2)`。`occupied` 只能包含已知由不同 pair
占用的槽位；重复 occupied 值代表上游碰撞，必须拒绝，不能静默集合去重。
因此当前工具应标为 `LOGIC-AUDITED / CANDIDATE NECESSARY FILTER`，尚未
是 production VERIFIED。

## `P_v -> depth-Hall` 独立 pilot

新增独立小脚本 `theory-lab/s1_crowding/mass_depth_hall_pilot.py`，先把
mass pattern 导出的 `P_v` 转成 low-depth 下界，再用 suffix-interval Hall
做必要性拒绝，并用直接枚举 low depths 检查被拒样本。Geo Workstation
单进程、`nice -n 15`、`timeout 120` 的 toy 参数
`m=5, delta=10, s=5..8` 得到：

```text
shape       mass_s_pairs  hall_reject  exact_depth_possible  false_rejects
chain3      432           68           83                    0
star3       432           16           56                    0
branch4     1008          522          70                    0
```

三种形状均 `soundness_ok=true`。这验证了 Hall 层作为必要条件的方向，
但 Hall 通过不代表存在；参数 `delta=10` 只是小规模逻辑测试，不是
Leech-tree 结论。远程脚本 SHA-256 为
`0b1c94639cec6b66c0b90aa229df35ef825268806c2413045a3592f314a13025`，
汇总结果 SHA-256 为
`41c6b01396d058a729603a909202c033ee9faaa16865133554530686f41c56fb`。

## Exact-state differential（补强）

按顾问建议，在 Geo Workstation 用原始 `component_mass_dp.py` 作为 oracle，
对 `m=4..7`、`r=1..5` 的全部 136 个 depth-order rooted lowpar shapes，
比较最终根节点 `(M_root=m,W)` 集合。结果：

```text
shapes_checked=136
mismatch_count=0
ELAPSED=2.38s, MAXRSS=12020 KB, RC=0
```

这使压缩 DP 在“root reachable-state 必要条件判定”上获得了完整的小规模
exact differential 支持；仍需注意它不能恢复具体 `P_v` 向量，因此不能直接
替代后续 depth/Hall 的 mass-pattern 枚举。summary SHA-256 为
`38e4ddf355244bf7db5d8cec1af2846ccae87fd6050665a35dc72fcbc69046ab`，
计时文件 SHA-256 为
`2de409dd97778502adacc117d68dad2a4edfaedbf6f636c1d72c7a37e9e7a3b2`。
