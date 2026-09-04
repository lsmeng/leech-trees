# Fable 接手单：Leech-tree 当前前沿、对抗审计与更好路线

日期：2026-09-02  
项目：FW319 exact-return-33 / Leech-tree 研究  
本地根目录：`/Users/geoclaw/Documents/claude/projects/leech-trees`  
Geo Workstation checkout：`/home/geo/codex-work/leech-trees`  
允许远程根目录：`/home2/geo/`、`/media/geo/`

## 0. 你的任务

请接管并独立审计当前研究。目标不是盲目增加 DFS 节点数，而是：

1. 明确 `delta=284/285` 已经排除的范围，以及仍然只是 `UNKNOWN/GAP` 的范围；
2. 找到一个比完整 depth/forest 枚举更短、更强、可以人工审计并写成论文引理的路线；
3. 只有新路线通过小例零误删、量词和 provenance 审计后，才提出最小远程验证批次。

顾问口头说“完成”、脚本输出 `UNSAT`、空输出、timeout 或前缀统计，都不能自动升级为全域证明。

## 1. 接手时只读检查

先只读读取并记录实际 SHA-256、Git `HEAD` 和工作区状态：

- `research_state.md`；
- 本文件；
- `docs/fable-takeover-audit-current-2026-09-02.md`；
- `docs/fable-handoff-audit-new-ideas-2026-09-02.md`；
- `docs/demand-span-lemma-audit-2026-09-02.md`；
- `theory-lab/s1_crowding/colored_moment_hall_presolve.py`；
- `theory-lab/s1_crowding/translated_difference_domains.py`；
- `theory-lab/s1_crowding/partial_depth_domain_audit.py`；
- `theory-lab/s1_crowding/partial_depth_domain_differential.py`；
- `theory-lab/s1_crowding/verify_depthv7_partial_shard.py`；
- 相关 `remote_scratch/*` 证书和结果。

不要清理、重置、覆盖、提交或推送已有研究产物。

## 2. 当前证据边界（以实际文件复核为准）

### VERIFIED / REPRODUCED

- top-block 容量计数直接排除 `r=3,m=21`（`delta=279`）和 `r=4,m=20`（`delta=280`）；这是容量矛盾，不依赖 LCA 叙述。
- order-6 genuine positive control 的统一树、ancestor-list LCA、BFS、translated-sumset、parity 和第一矩审计通过；它只是零误删控制。
- 固定候选 presolver 已在 Geo Workstation 单进程、`nice -n 15`、有界 timeout 下回放：
  - r8：`s=158,L=[0,18,40,41,51,59,88,92]`，`exact=true`，global parity 与 Wiener 失败（`154!=150`，`47194!=45150`）。
  - r9：`s=157,L=[0,13,1,2,3,24,33,77,101]`，`exact=true`，Wiener 失败（`150=150`，`47064!=45150`）。
- `partial_depth_domain_audit.py` 的三个独立控制通过：genuine L6 保留；r8 singleton 由 parity/Wiener 拒绝；r9 三值域盒由 Wiener 拒绝；独立 differential 报告 `soundness_ok=true`。
- Hoffman2 r8 的 `split_9_of_64` 和 `split_10_of_64` 已分别通过本地及远程原地验收：末尾 `COMPLETE`、7 个结构齐全、depth/structure survivors 均为 0、无 `NODE_LIMIT/TIMEOUT`。这只是 2/64 分片。

### FINITE-EVIDENCE / CANDIDATE

- r8/r9 的完整 depth 数组仍须等所有最终 `.txt` 分片后逐片验收，再运行完整 coverage verifier；中途 `.tmp` 计数不能算结论。
- partial-domain、component-mass、demand-span、Hall、parity-Hall、moment-Hall 都是必要条件或传播器；通过只表示 `NOT-EXCLUDED`。
- 旧搜索中的 `NODE_LIMIT`、timeout、空 JSON/空输出必须分别记为 `UNKNOWN`、`TIMEOUT` 或 `OUTPUT_MISSING`，绝不能写成 `UNSAT`。

最近记录的远程状态（仅供定位，接手必须重新只读查询）：Hoffman2 r8 数组 `118375` 曾为 64 片中 2 个最终文件、其余临时文件；r9 数组 `118376` 曾为 0 个最终文件、38 个运行中和 1 个排队。不得取消、重启或改参数。

## 3. 必须核对的数学量词

对固定 abstract structure、`delta`、`s`、low-depth 向量 `L`，令

```text
B = delta + 1 - s
H   = high-LCA raw-sum set
S_v = low-LCA class v 的 raw-sum set
T_v = 2B - 2l_v + S_v
```

必须保留真实 owner 和全部量词：`H/S` 内部唯一性、不同 `S_i-S_j`、平移后 `T_v` 与 `H` 互斥、holes/x-high/LL/LH owner、范围、depth 顺序、parent 约束、parity coloring、全局 odd-pair 条件和 Wiener 第一矩。禁止静默 `set()` 去重后再声称证明。

## 4. 请优先寻找更好的思路

请先做数学审计，再决定是否写代码。至少比较下列路线，并明确接受、拒绝或保留理由：

### A. 统一的 colored completion lemma（首选）

把 `H`、各 `T_v`、parity 槽位、差集禁配和 Wiener 第一矩放进同一个 completion 问题。对任意类子集 `Q`，审计：

```text
D_Q <= |union(A_q)|
even-demand(Q) <= even-capacity(union(A_q))
odd-demand(Q) <= odd-capacity(union(A_q))
min_sum(Q) <= exact_class_sum(Q) <= max_sum(Q)
```

必须证明 `A_q` 是实际可用距离集合的超集；occupied 只能删除已确认的 owner。给出精确量词、边界条件和最小反例，不能只给算法直觉。

### B. Difference-domain + parity/Wiener 联立

核对

```text
2(l_i-l_j) ∉ S_i-S_j
```

的符号、除以 2、奇偶和边界。尝试把 forbidden depth-difference、colored Hall 和 Wiener 仿射同一化，而不是仅增加 DFS 剪枝。

### C. Component-mass / demand-span 的统一不等式

审计

```text
W + sum(P_v) = C(m,2)
sum_{v in Q} P_v <= (2m-3) + 2(max l_v-min l_v)
W + P_v <= (2m-3) + min(2m-3, 2(B-l_v))
```

明确这些式子是否覆盖完整 LL/LH/holes owner ledger。若能被一个最小可行或不可行例子击破，请保存反例，不得把它们当全局定理。

### D. 其他可审计路线

可探索模类容量、区间压缩、生成函数、整数流/匹配、ILP/SAT、对称性商或 shape signature，但每条路线必须回答：

1. 约束的是完整必要系统，还是一个投影？
2. 是否能输出人工复核的证书，而不只是 `UNSAT`？
3. 是否在 genuine positive、局部双-low、局部三-low控制上零误删？
4. 用于 284/285 时如何记录输入、版本、命令、资源、终止状态和覆盖？

如果只是又一个启发式过滤器、没有 sound lemma 或显著削减，请建议停止投入。

## 5. 计算和文件边界

- 本机只做文本、diff、哈希、语法和小型审计；不要启动本机枚举、参数扫描或长 Python/C++。
- 重计算只能放 Geo Workstation 或 Hoffman2；Geo 使用 `DevSpace workstation`，checkout 为 `/home/geo/codex-work/leech-trees`，允许根目录只有 `/home2/geo/` 和 `/media/geo/`。
- 新任务最多 4 workers，使用低优先级和明确 timeout；开始前查残留，结束后查孤儿。
- 已有远程作业只读观察，不取消、不重启、不修改。
- 新代码和结果先放 `scratch`/`remote_scratch`，保存脚本、输入、命令、机器、revision、SHA-256 和终止状态。

## 6. 最小验收实验

先不碰生产 DFS，完成以下轻量 gate：

1. genuine order-6 `s=8,L=[0]` 必须保留；
2. 局部双-low 正例专门核对 raw difference、平移、parity 和 owner；
3. 局部三-low 负例分别定位 exact-difference、Hall、moment-Hall 失败；
4. 冻结 r8/r9 一个固定 witness 只做 presolver，不重跑慢 DFS；
5. 新路线只有在 zero-false-reject 和独立 differential 通过后，才可拟议远程最小批次。

## 7. 交付格式

请在新的日期文件或 scratch 结果中返回：

```text
实际读取的 HEAD / git 状态：
实际读取文件及 SHA-256：
远程 DevSpace / checkout / 作业状态（是否修改）：

VERIFIED：
REPRODUCED：
FINITE-EVIDENCE：
CANDIDATE：
UNKNOWN / GAP：

translated-sumset soundness verdict：
colored moment-Hall / difference-domain verdict：
component-mass / demand-span verdict：
parity + Wiener verdict：

更好的路线：命题、证明草图、最小反例或零误删结果：
实际改动文件、命令、测试与结果：
唯一推荐下一步：
停止或转向条件：
```

唯一科学停止条件是：找到可闭合的全局 lemma/完整证书，或给出证明某条路线不可能闭合的最小反例。任何单个 shape、单个分片、顾问口头判断、timeout 或 `NODE_LIMIT` 都不是 Leech-tree 全域猜想的证明。

## 8. 接手包之后的最新只读进展（2026-09-02）

Hoffman2 只读轮询显示：r8 数组 `118375` 已有 4/64 个最终 `.txt` 分片，60 个仍为
`.txt.tmp`；r9 数组 `118376` 仍有 0 个最终分片，39 个临时分片，且其余任务受
`QOSMaxJobsPerUserLimit` 排队。没有取消、重启或修改任何作业。

本轮新增的 r8 分片已从 Hoffman2 回收并在本地及 Hoffman2 原地各验收一次：

```text
split_12_of_64.txt
  shard SHA-256: 61e8dcf05a50595bfd03a016f5fa40c6f5f543d005255dcfbd12a3c6c00fb0ad
  certificate SHA-256: 5def33f340028724b11eecf321474d262bbe422e6114c84c44b20c15d429e005
  status: VERIFIED_PARTIAL_SHARD_EMPTY; abstract_lines=7; survivors=0

split_13_of_64.txt
  shard SHA-256: 55c164e9f092f9cb5e9f2c9324c193fa753f1b09792939e665245bba5eb636f2
  certificate SHA-256: 623e62a4095031ffce6b97733733aeaaa9d0bacf07521609264b1e2c2df69a94
  status: VERIFIED_PARTIAL_SHARD_EMPTY; abstract_lines=7; survivors=0
```

这把 r8 的可验证空分片计数从 2/64 提高到 4/64，仍然不是 r8 全数组覆盖，更不是
`delta=284/285` 的全域非存在证明。Fable 接手后只需继续按同一验收器处理新出现的
最终文件，并把主要精力放在第 4 节的统一引理/最小反例上。

## 9. 再次只读更新（2026-09-02）

Hoffman2 数组 `118375` 随后出现 `split_8_of_64.txt`。该分片已在本地和 Hoffman2
原地各验收一次，均为 `VERIFIED_PARTIAL_SHARD_EMPTY`，无错误、无
`NODE_LIMIT/TIMEOUT`，`total_depth_survivors=0`、`total_structure_survivors=0`。

```text
split_8 shard SHA-256: 97dcee74e6242bb4982dd092cebc4ed10e51318990e96675393b4d490765f67b
split_8 certificate SHA-256: e2598b34994de3706c45d788b63a020f1282e0e66a46b2192ff61093880ea30b
```

因此 r8 当前已有 5/64 个可验证空分片；r9 当前仍为 0 个最终分片。该更新仍只
增强有限分片证据，不改变全域猜想的证明状态。

## 10. 再次只读更新（2026-09-02）

Hoffman2 r8 数组 `118375` 新出现 `split_5_of_64.txt`；当前 r8 有 6/64 个最终
分片、58 个临时分片。该分片已在本地和 Hoffman2 原地各验收一次，均为
`VERIFIED_PARTIAL_SHARD_EMPTY`，无错误、无 `NODE_LIMIT/TIMEOUT`，7 个结构齐全且
survivors=0。

```text
split_5 shard SHA-256: 88888ae52d01fbbcdd9c8a73936de07ab3b58c3bb53cbbb8c8c29d476ff4e37a
split_5 certificate SHA-256: ddacb7f72777b4fe40ebbecd466db4ee54ae30bea80c08a9bcbe560ef04811b2
```

r9 仍为 0 个最终分片；这仍只是有限分片证据，不改变全局证明状态。

## 11. 再次只读更新（2026-09-02）

Hoffman2 r8 数组 `118375` 新出现 `split_11_of_64.txt`；当前 r8 有 7/64 个最终
分片、57 个临时分片。该分片已在本地和 Hoffman2 原地各验收一次，均为
`VERIFIED_PARTIAL_SHARD_EMPTY`，7 个结构齐全、survivors=0、无
`NODE_LIMIT/TIMEOUT`。

```text
split_11 shard SHA-256: 3a39cb5f177e471d70a332a03c98ee2e7c9129987338114cf52ec03b847a12e4
split_11 certificate SHA-256: 2b26eadf7db5e0684d2213d6d70ea7e22dff7d498a493ed1bb9fa77e88736357
```

r9 仍为 0 个最终分片；该更新仍是有限分片证据，不改变全局证明状态。

## 14. 再次只读更新（2026-09-02）

Hoffman2 r8 数组 `118375` 新出现 `split_7_of_64.txt`；当前 r8 有 10/64 个最终
分片、54 个临时分片。该分片已在本地和 Hoffman2 原地各验收一次，均为
`VERIFIED_PARTIAL_SHARD_EMPTY`，7 个结构齐全、survivors=0、无
`NODE_LIMIT/TIMEOUT`。

```text
split_7 shard SHA-256: ac401f5da8ba5f5ec8457d305f4d19a0e3e07ab30ab6e59f8372d6a5a9dc6853
split_7 certificate SHA-256: 083ac2db4238b78f5a0b2654e3b3305a93fc58f9aa5fe4690c7760ecccd568c6
```

r9 仍为 0 个最终分片；该更新仍是有限分片证据，不改变全局证明状态。

## 13. 再次只读更新（2026-09-02）

Hoffman2 r8 数组 `118375` 新出现 `split_4_of_64.txt`；当前 r8 有 9/64 个最终
分片、55 个临时分片。该分片已在本地和 Hoffman2 原地各验收一次，均为
`VERIFIED_PARTIAL_SHARD_EMPTY`，7 个结构齐全、survivors=0、无
`NODE_LIMIT/TIMEOUT`。

```text
split_4 shard SHA-256: a1159ab1bc61d52710fe9609de26db8468e3963bfc27772fd28d5524eeb9f46e
split_4 certificate SHA-256: de3e9d9c275f86d9900bebdf1b9e9d534afbf8362100b8dd45d984eaae80bdd9
```

r9 仍为 0 个最终分片；该更新仍是有限分片证据，不改变全局证明状态。

## 12. 再次只读更新（2026-09-02）

Hoffman2 r8 数组 `118375` 新出现 `split_6_of_64.txt`；当前 r8 有 8/64 个最终
分片、56 个临时分片。该分片已在本地和 Hoffman2 原地各验收一次，均为
`VERIFIED_PARTIAL_SHARD_EMPTY`，7 个结构齐全、survivors=0、无
`NODE_LIMIT/TIMEOUT`。

```text
split_6 shard SHA-256: d6b6778c2801bfbebea848919c1475ca7b0bb2e4b2a55e22d3296976ffb1940b
split_6 certificate SHA-256: afcf3b65c6fd4ecd227d569d658094408178e24603c93b042d859f27fb459362
```

r9 仍为 0 个最终分片；该更新仍是有限分片证据，不改变全局证明状态。
