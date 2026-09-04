# Leech-tree 项目：Fable 接手与独立审计包

日期：2026-09-01  
项目：FW319 exact-return-33，`b=27`，S1-279 残余分支  
主项目根目录：`/Users/geoclaw/Documents/claude/projects/leech-trees`

## 0. 给 Fable 的任务

请把本文件和 `research_state.md` 当作接手入口。你的任务不是只复述已有结果，而是：

1. 独立审计当前 `s=154, shape=chain` 路线的定义、代码范围、精确量词和证据链；
2. 检查当前 Python forest 与独立 C++ replay 是否真的覆盖同一问题；
3. 寻找比“555,397 个 signature 的完整 forest 枚举”更好的路线，优先考虑可证明的结构性剪枝、对称性商、Hall/流约束、根集组合恒等式、谱约束或分层反证；
4. 若没有更好的安全路线，再继续远程分片计算，并给出可复现的双实现验收结果。

任何有限计算的零结果都只能标为固定范围的 `CERTIFIED FINITE IMPOSSIBLE`；除非另有完整的普遍性证明，不得写成整个 Leech-tree 猜想已证明。

## 1. 资源与安全边界

- 本地 Mac 只有 24 GB 内存；禁止在本地运行枚举、参数扫描、大型 Python forest、bootstrap 或长脚本。
- 重计算只能放到 Geo Workstation：
  - SSH/DevSpace 目标：`geo-ws`
  - 远程副本：`/home/geo/codex-work/leech-trees/remote_scratch/s1_279_high_s_five_value_root_signature_20260831`
  - 允许根目录：`/home2/geo/`、`/media/geo/`（以及当前已授权的 `/home/geo/` 工作副本）
- 每台机器最多 4 个并发 worker；所有长任务使用 `nice -n 15` 和明确 `timeout`；启动前用 `pgrep -af` 检查残留，结束后确认没有孤儿进程。
- 不重启、取消或修改已有远程作业；不提交/推送；不删除已有文件；不读取或保存凭据。
- 优先使用 scratch 文件。若要修改正式状态，只追加可审计 checkpoint，不覆盖旧证据。

## 2. 当前数学范围与固定定义

本轮固定：

```text
delta = 279
s = 154
shape = chain
B = 280 - s = 126
A = 146
low depths = {0, d1, d2}
high depths = [126, 146]
d1,d2 even, 0 < d1 < d2 < 126
```

原始 `(d1,d2)` 对数为 `C(62,2)=1891`；排除 `d2=2*d1` 的 31 个非法 chain 参数后，合法参数数为 `1860`。允许的 `d1` shard 是 `2,4,...,124`，共 62 片。

FW303 的 38 个 `(gate,q)` profile 不变，但必须使用 `s=154,B=126` 的 depth embedding。完整 forest 的 `c` 量词必须是：

```text
Class A: c = 10,11,12,13,14
Class B: c = 11,12,13,14
Class C: c = 12,13,14
e = 21 - c - f_C
```

特别是 `c=14` 不能省略：A/B/C 的 `(e)` 分别是 `2/3/4`。非核心 HH 字母表为 `{4,5,16,18,19,20}`。每个 candidate 的 23 条边必须满足完整 edge ledger，不能重复安装 Class B/C 已由 forced-root attachment 提供的边。

## 3. 已验证事实（不得重复计算后才承认）

### 3.1 `s=154, star` 固定分支

独立整批核验已完成 62/62 个 `d1` shard：

```text
params_total = 1891
params_valid = 1556
params_with_survivor = 0
survivor_count = 0
```

结论只覆盖固定的 `s=154, shape=star`：`CERTIFIED FINITE IMPOSSIBLE`。不能外推到 chain 或整个 S1-279。

### 3.2 `s=154, chain` exact-10 子系统

Primary exact-10 已完成 62/62 个 `d1` shard，scope 正确：

```text
params_total = 1891
params_valid = 1860
params_with_survivor = 1318
survivor_count = 5201986
```

这些是 exact-10 必要子系统的幸存见证，不是完整树存在性结论。

### 3.3 独立 C++ replay 与 canonical union

参数化后的独立 replay 使用 `S=154,B=126`，逐 `d1` 完成 62/62。去重后的 canonical union：

```text
canonical_signature_count = 555397
SHA-256 = 81211a50c710cb3324fea47197fd0524295678dbfe08403e26d41007841567ce
```

输入文件的合法修复副本是远程的 `exact10_s154_chain_union_v2.json`。旧的 s=152 replay 和旧的 literal `\\n` malformed JSON 都不能当作当前证据。

### 3.4 FW303 prefilter

远程参数化预筛结果：

```text
signatures_checked = 555397
theoretical_38_row_assessments = 21105086
compatible_rows = 392049
Class A = 391129
Class B = 773
Class C = 147
```

所有 `392049` 个 compatible row 都保留到 `c=14`；row key 唯一。根组合计数恒等式通过：

```text
A,m=0: root_sets=15, root_colorings=1215, e=2
B,m=0: root_sets=35, root_colorings=2835, e=3
B,m=1: root_sets=20, root_colorings=540,  e=3
C,m=1: root_sets=35, root_colorings=945,  e=4
C,m=2: root_sets=15, root_colorings=135,  e=4
```

全域规模审计：

```text
(row,c) jobs = 1959178
root-coloring proxy = 748800068
W-injection weighted upper proxy ~= 64426821210
```

### 3.5 已通过的双实现 pilot

canonical index `0..49` 的 50-signature pilot 已由 Python forest 和独立 C++ replay 分别执行：

```text
jobs on each side = 110
c=14 jobs = 22
survivors on each side = 0
job key = (signature_index, gate, q, class, c)
mismatch_count = 0
```

七项计数（`root_sets, root_colorings, root_edge_legal, capacity_rejects, weight_assignments, parent_legal, spectrum_survivors`）逐 key 对齐。该 pilot 只证明小片接口一致，不能外推全域。

## 4. 当前运行中的事项

依据 workload proxy 已生成远程 `forest_shard_plan_s154_chain.json`：共 1286 个连续 signature 范围，每片目标约 50M weighted parent-attempt proxy，计划最多 4 个远程 worker。

首片为 canonical index `0..548`。当前 Python 实现正在 Geo Workstation 上运行，使用 `nice -n 15`，启动后约 3 分钟时 CPU 约 100%、RSS 约 1.7 GB；尚未产生最终 JSON，不能标为完成，也不能据 timeout 推断 survivor=0。

首片完成后的固定顺序：

1. 只读检查 Python JSON、`.time`、状态码和临时文件是否完整；
2. 从同一 canonical 子集生成 slice 输入；
3. 用独立 C++ replay 自行重建 38 rows 与 `c=14` jobs；不得读取 Python compatible rows 作为输入；
4. 以 `(canonical_signature, gate, q, class, c)` 为 key，逐项比较七项计数；
5. 只有 `job_keys_exact=true`、`mismatch_count=0` 且两边都完整结束，才能接受该片。

## 5. 请重点寻找的更好思路

请先做只读数学/代码审计，再决定是否扩大计算。至少回答：

### A. 是否存在 sound 的早期剪枝

- `c=14` 时 `e=2/3/4` 的 forced-root、high-vertex partition、edge ledger 是否能推出更强的必要条件？
- 能否在不枚举完整 W injection 的情况下，用颜色容量、局部谱、Hall/流不可行性或边拥有者约束证明整类 row 无解？
- 能否把 `root_colorings` 的解析计数进一步压缩成轨道/稳定子商，并证明不漏解？

### B. 是否能替代全 forest

- 是否可以按 Class A/B/C 或 `(m,c)` 分层，先证明稀有 B/C 类全部不可能，再处理 A 主体？
- 是否可以把 38-row 结果转成一个小型整数规划/精确覆盖或生成函数问题，并由独立 checker 验证？
- 是否能找到跨 signature 的不变量，使 555,397 个签名不必逐一跑完整 forest？

### C. 代码与量词审计

- 检查 `_s154` 版本是否仍残留 `s=152/B=128`、`d2<128` 或 `c<=13`；
- 检查 Class B/C 的 fixed LH/LL core edge 是否重复计数；
- 检查完整 roots 是否恰为 `c`，并保持 high partition 两两不交；
- 检查 Python 与 C++ 是否从相同 canonical signature 重建，而非共享同一中间产物。

如果提出新剪枝，必须给出：形式化必要条件、为什么 sound、对一个小片的独立验证、预期节省的 workload，以及失败时如何回退到现有分片路线。

## 6. Fable 交付格式

请返回一份短而可审计的报告，至少包含：

```text
接手日期与实际 revision
读取过的文件
VERIFIED / REPRODUCED / FINITE-EVIDENCE / CANDIDATE / UNKNOWN 分类
发现的量词或实现问题
是否有更优结构性路线（若有，给出 soundness 论证）
对当前首片运行的建议（继续、缩片、暂停或改路线）
实际修改文件与命令
独立验证命令及结果
仍未闭合的最小命题
```

不得把顾问（包括已有普通 Chat “Leech tree chat2”）的回复当作权威；顾问意见只能作为候选路线，必须用真实文件、独立 replay 和精确量词验收。

## 7. 最小结论

目前已经把 `s=154,star` 固定分支认证为有限不可行，并完成了 `s=154,chain` 的 exact-10、独立 union、38-row/c14 prefilter 和小片双实现 pilot。真正的 chain full-forest 尚未完成；最重要的开放问题是：能否找到一个 sound 的结构性剪枝/反证，避免 1286 片重型枚举，或者至少把首片 Python/C++ 双实现验收跑通并据此稳步扩展。

## 8. 后续审计补充（2026-09-02）

控制器和普通 Chat 顾问随后复核了 top-block crowding 论证。结论可保留，
但 high-LCA 类的容量理由必须写成“距离值域本身落在
`[1,2m-3]`”，不能写成 `q` 由 `y+y'` 决定。当前 source/binary/output
provenance 还存在哈希不一致：checkpoint 记录的 source hash `3a7a...`，
可见 source hash 为 `e72d...`；在补齐每次运行的 source、binary、命令行和
output 对应关系前，相关计算应标为 finite evidence/provisional。

对于 `delta >= 284`，优先审计并实现以下 sound 预筛，而不是直接扩大巨型
parent DFS：若 high components 在 low vertex `v` 上的大小为 `n_{v,j}`，
`M_v` 为其 low-subtree 总质量，则必须有

```text
W   = sum_{v,j} C(n_{v,j},2) <= 2m-3
P_v = C(M_v,2) - sum_{u child of v} C(M_u,2) - sum_j C(n_{v,j},2) <= 2m-3
W + sum_v P_v = C(m,2)
```

随后再做 depth-interval/Hall 可行性传播。该路线是必要条件剪枝，不等同于
证明；不得声称存在 `delta` 单调递推（目前没有安全依据）。
