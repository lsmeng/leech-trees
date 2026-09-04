# Fable 接手＋对抗审计委托：Leech-tree 主线（当前版）

日期：2026-09-02  
项目：FW319 exact-return-33 / Leech-tree 研究  
本地项目根目录：`/Users/geoclaw/Documents/claude/projects/leech-trees`  
Geo Workstation checkout：`/home/geo/codex-work/leech-trees`  
允许的远程根目录：`/home2/geo/`、`/media/geo/`

这份文件是给 Fable 的自包含接手单。请把它当作研究任务和审计清单，而不是“已有证明”的摘要。顾问或脚本说“完成”不等于数学结论成立；所有结论必须回到真实文件、命令、输入、输出和精确量词。

## 1. 目标

接手当前 Leech-tree 主线，回答两个问题：

1. 当前 `delta=284/285` frontier 到底已经排除了什么，哪些仍是 `UNKNOWN/GAP`？
2. 是否存在比继续扩大 depth/forest DFS 更短、更强、可人工审计并能写成论文引理的路线？

优先寻找能同时利用 exact translated sums、low-LCA 类、奇偶、第一矩（Wiener）和 component mass 的统一约束。若没有 sound 的统一矛盾，也要给出最小反例，说明为什么某条路线不能升级成全局证明。

## 2. 接手时先做的只读检查

先不要跑枚举、不要清理工作区、不要提交或重置。只读检查并记录：

- `research_state.md`；
- 本文件以及 `docs/fable-handoff-audit-new-ideas-2026-09-02.md`；
- `docs/demand-span-lemma-audit-2026-09-02.md`；
- `theory-lab/s1_crowding/colored_moment_hall_audit.py`；
- `theory-lab/s1_crowding/translated_difference_domains.py`；
- `theory-lab/s1_crowding/colored_moment_hall_presolve.py`；
- `theory-lab/s1_crowding/translated_sumset_csp_pilot.py`；
- 对应的 `remote_scratch/*/structure_certificate.remote.json`。

记录实际读取的 Git `HEAD`、工作区是否 dirty、文件 SHA-256，以及远程 checkout、DevSpace 和现有作业状态。工作区中已有大量用户研究产物，全部保留。

## 3. 当前证据边界

### 已验证或可独立复现的部分

- Top-block 值域容量计数已经直接排除 `r=3,m=21`（`delta=279`）和 `r=4,m=20`（`delta=280`）；这是容量矛盾，不依赖未经证明的 LCA 叙述。
- order-6 genuine positive control 的统一树、ancestor-list LCA、BFS 距离、translated-sumset、parity/first-moment 审计通过；它只能证明测试链条没有误删该正例。
- r8、r9、r10 的冻结结构证书已能独立生成并回放，覆盖 `H/S` 分割、内部唯一性、pair 总数、`W/P` 和 Wiener 仿射数据；证书只属于 structure-only 层。
- `translated_sumset_csp_pilot.py` 的 occupied-hole 越界现在明确拒绝并计数 `hole_out_of_range_rejects`；这属于安全边界修正，不是全局结论。

### 仍只是有限证据、不能当定理的部分

- `delta=284`：已有 115 个 low shapes，其中 7 个 structure-bearing；`delta=285`：286 个中 95 个 structure-bearing。完整 corpus 的来源、覆盖、终止状态和 provenance 仍要逐项核对。
- r8 的历史单结构搜索到 `NODE_LIMIT`；r9 的 occupied 输出曾为空/超时。两者均不能解释为“没有 survivor”。
- r10 的旧 translated-sumset 全搜索在 120 秒上限 `RC=124`、JSON 为空；应标为 `TIMEOUT/OUTPUT_MISSING`，不得重述成 `UNSAT`。
- component-mass、demand-span、`(W,P)`、parity 或单个 Wiener 方程单独都只是必要条件；通过它们只表示 `NOT-EXCLUDED`。
- `colored_moment_hall_presolve.py` 是候选 presolver。它的失败可以对一个固定 `(structure,s,L)` 给出必要条件意义下的 `UNSAT_FOR_THIS_CANDIDATE`；全部通过仍不能证明存在，更不能证明整个 structure/corpus 无解。兼容远程 Python 3.8 的最新改动尚需重新做最小回放。

## 4. 关键数学对象（请先核对定义）

对固定 abstract structure、`delta`、`s` 和 low-depth 向量 `L=(l_v)`，令

```text
B = delta + 1 - s
H       = high-LCA raw-sum set
S_v     = low-LCA class v 的 raw-sum set
T_v     = 2B - 2l_v + S_v
```

必须保留以下精确信息，不得静默 `set()` 去重：

- `H` 与每个 `S_v` 的内部唯一性；
- 不同 `S_v` 的 raw-sum 差集 `S_i-S_j`；
- 平移后的 `T_v` 与 `H` 的互斥、值域边界和 owner 去重；
- hole、x-high、LL、LH 的真实 owner 及其删除范围；
- depth 顺序、`0 <= l_v < B`、parent 约束；
- parity coloring、全局 odd-vertex/odd-pair 条件；
- Wiener 第一矩仿射等式。

一个固定候选只有在所有这些量词都通过后，才可写 `NOT-EXCLUDED`；任何失败必须同时报告失败层和具体 witness。

## 5. 请优先审计并改进的路线

### A. Colored moment-Hall completion lemma

把 `H`、各 `T_v`、parity 槽位和第一矩作为一个带颜色、带需求量、带总和约束的 completion 问题。对任意 class 子集 `Q`，核对：

```text
D_Q <= |union(A_q)|
even-demand(Q) <= even-capacity(union(A_q))
odd-demand(Q)  <= odd-capacity(union(A_q))
min_sum(Q) <= exact_class_sum(Q) <= max_sum(Q)
```

其中 `A_q` 必须是实际可用距离集合的超集；occupied 只能删除已确认由其他 owner 占用的槽位。请给出完整证明、边界条件和最小反例，而不是只给算法直觉。

### B. Difference-domain 约束

验证

```text
2(l_i-l_j) ∉ S_i-S_j
```

的符号、奇偶和边界是否与实际距离公式完全一致。优先把它与 Hall/moment-Hall 联合，而不是单独增加 DFS 剪枝。检查 `translated_difference_domains.py` 输出的 raw difference 与除以 2 后的 forbidden depth difference 是否一致。

### C. Component-mass / demand-span

审计下列式子的精确适用范围，寻找能覆盖多个 structure 的统一矛盾：

```text
W + sum(P_v) = C(m,2)
sum_{v in Q} P_v <= (2m-3) + 2(max l_v-min l_v)
W + P_v <= (2m-3) + min(2m-3, 2(B-l_v))
```

若不能覆盖 LL/LH/holes 的完整 owner ledger，请明确指出缺哪一个量词，或构造一个通过该不等式但实际可行/不可行的最小例子。

### D. 更大胆但仍需可审计的替代思路

可以探索生成函数、整数流/匹配、区间压缩、模类容量、对称性商、整数规划或 SAT，但必须先回答：

1. 它约束的是完整必要系统，还是只约束了一个投影？
2. 是否有可人工复核的证书，而不是只输出 `UNSAT`？
3. 是否在 order-6 genuine positive、人工双-low 正例、人工三-low 负例上零误删？
4. 若用于 284/285，如何记录输入、版本、命令、资源、终止状态和覆盖？

如果新想法只比现有 DFS 多一个启发式过滤器，却没有 sound 证明或显著削减，请明确建议停止投入。

## 6. 最小验收实验（先 scratch，后远程）

先只做轻量、可复现的测试：

1. order-6 genuine `s=8,L=[0]`：必须保留，不能误判 UNSAT；
2. 人工双-low 正例：专门检查差集符号、平移、parity 颜色；
3. 人工三-low 负例：分别制造 exact-difference、Hall、moment-Hall 失败，并确认失败层可定位；
4. 取冻结 r8/r9 的一个固定 witness，只做 presolver，不重跑旧的慢 DFS。

只有上述 differential 通过且新条件确实减少候选，才提出 Geo Workstation 最小批次。远程重计算必须使用 `DevSpace workstation`、`nice -n 15`、最多 4 workers、明确 timeout；开始前查残留，结束后查孤儿。不要碰当前已经运行的 `abstract_class_search7` 或 Hoffman2 作业。

## 7. 交付格式

请在 scratch 或新的日期文件中返回：

```text
接手时实际 HEAD / git 状态：
实际读取文件与 SHA-256：
远程 DevSpace / checkout / 现有作业：

VERIFIED（可复核证明或证书）：
REPRODUCED（独立回放）：
FINITE-EVIDENCE（范围和终止完整）：
CANDIDATE（尚未闭合）：
UNKNOWN / GAP：

对现有 translated-sumset 的审计结论：
对 colored moment-Hall / difference-domain 的结论：
对 component-mass / demand-span 的结论：
是否发现更好的路线（命题、证明草图或最小反例）：
实际改动文件、命令、测试与结果：
唯一推荐下一步及停止/转向条件：
```

## 8. 明确禁止的表述和操作

- 不得把 `NODE_LIMIT`、timeout、空输出、前缀统计、单个 shape、顾问口头判断或“没有找到 survivor”写成全域证明。
- 不得在本机启动枚举、参数扫描、长 Python/C++ 或无上限并行；本机只做文本、diff、哈希和小例审计。
- 不得清理、重置、覆盖既有产物，不得提交/推送，不得取消、重启或改动已有远程作业。
- 新代码先放 scratch；生产 DFS 只有在零误删、soundness 和 provenance 都明确后才可考虑接入。

## 9. 当前最小科学缺口

我们还没有 `delta=284/285` 完整、不可变、可复跑的 structure/depth corpus 证书，也没有一个已经证明 sound 且能终止的全局 presolver。因此当前最诚实的状态是：结构层必要条件和若干固定候选已得到有证据的排除，但 Leech-tree 全域猜想仍未证明。Fable 的首要价值是找到能闭合这个缺口的统一引理，或尽早证明某个看似漂亮的路线必然丢失关键信息，从而避免继续烧远程算力。

## 10. presolver 回放（历史 v1 与当前 v2 分开记录）

早先 v1 回放的脚本哈希为
`edf3a11672175862c085776e61a97f36cee1ce6d9fdc483b40f006791b625717`；下面的 v1
输出仅作历史 provenance，不能覆盖当前结果。当前脚本
`theory-lab/s1_crowding/colored_moment_hall_presolve.py` 的 SHA-256 是
`d9192dad56c30d3bc01be0c494d7dc82b8eb2d495b6dc8f391caa877b206efef`（接手时仍请
以实际 `sha256sum` 为准）。当前版本增加了 `failure_layers` 字段，但没有放宽
任何必要条件。order-6 L6 正控（`hpar=-1,-1,1,1`, `delta=11`, `s=8`,
`depths=0`）轻量回放为 `NOT-EXCLUDED` 且 `failure_layers=[]`。

当前 v2 已在 Geo Workstation 以单进程、`nice -n 15`、30 秒上限回放两个冻结
witness，结果已回收至本地：

```text
remote_scratch/translated_sumset_delta284_one_shape_20260902/
  colored_moment_hall_presolve.remote.json
  SHA-256 7d8a193439e770d784ae5de24245bef7a41fbbb69ab6925e676779cd44cf4c35
  r8: exact=true; parity 154!=150; Wiener 47194!=45150;
      UNSAT_FOR_THIS_CANDIDATE

remote_scratch/translated_sumset_delta285_one_shape_20260902/
  colored_moment_hall_presolve.remote.json
  SHA-256 71ace6f9e6e9b22754892e385998bba63119dbd03db2d5f998ab52ec34a102b3
  r9: exact=true; parity 150=150; Wiener 47064!=45150;
      UNSAT_FOR_THIS_CANDIDATE
```

两次回放都通过 exact `H/T`、范围、互斥、Hall、parity-Hall、moment-Hall；失败
分别来自全局 parity/Wiener（r8）和 Wiener（r9）。这只是两个固定候选的必要条件
排除，绝不是整个 r8/r9 structure 或 `delta=284/285` 全域证明。Fable 接手时应
继续做人工双-low/三-low differential，并审计 failure-layer 的 soundness；在此
之前不要把 presolver 接入 production DFS，也不要重跑旧的 `NODE_LIMIT` 路线。

## 11. failure-layer 可审计性更新

presolver 现已增加 `failure_layers` 字段，当前脚本 SHA-256 为
`d9192dad56c30d3bc01be0c494d7dc82b8eb2d495b6dc8f391caa877b206efef`。
（接手时请以实际 `sha256sum` 为准。）本机 L6 正控回放结果为
`failure_layers=[]`；两个 Workstation witness 用同一新版本重放后仍为：

```text
r8: [global_parity, wiener]
    output SHA-256 7d8a193439e770d784ae5de24245bef7a41fbbb69ab6925e676779cd44cf4c35
r9: [wiener]
    output SHA-256 71ace6f9e6e9b22754892e385998bba63119dbd03db2d5f998ab52ec34a102b3
```

这只是改善拒绝原因的 provenance；两者仍只是固定 `(structure,s,L)` 的必要条件
排除。下一项仍是人工双-low/三-low differential 和 failure-layer soundness 审计，
不是放大 284/285 的旧 DFS。

## 12. 重要审计结论：Hall 层对完整候选是冗余的

请不要把当前脚本对完整 `(s,L)` 的 Hall、parity-Hall、moment-Hall 输出误写成
额外的独立排除能力。若 exact `H/T` 已通过，则这些精确类集本身就是互不相交
的真实槽位，并分别包含于 `A_H/A_v`；所以任意类子集的容量和矩约束自动成立。
order-6 L6 的全部 `s=1..11` 轻量性质检查也得到：3 个 exact 通过者均无
Hall/parity-Hall/moment-Hall 失败，`counterexamples=0`。

这并不是删除这些代码的理由：它们应改作未来**部分 low-depth 域**的传播器，
在那里 allowed domains 尚未选定 exact `T_v`，Hall 和 moment-Hall 才可能提前
剪枝。Fable 接手时请分别设计“完整候选证书”和“部分域传播”接口，并继续把
global parity、Wiener 作为可独立拒绝完整候选的条件。

## 13. 新增的部分域传播原型（只作保守审计）

已新增 `theory-lab/s1_crowding/partial_depth_domain_audit.py`，当前 SHA-256
为 `66e11f8fffd7dc1b37505421692ae617b01d60c179a29518d164b0a76e784d7c`。它接收
每个 low vertex 的有限 depth domain（格式如 `0;12,13,14;1,2`），不枚举域盒中
所有深度组合，而是对每个 `T_v` 取所有可能平移的并集。现在还加入了 `W/P` 的
component-capacity 和 demand-span 上界。只有以下情形才报告域盒整体
`UNSAT_FOR_ALL_ASSIGNMENTS_IN_DOMAIN_BOX`：并集 Hall/parity-Hall/moment-Hall
容量矛盾、component/demand-span 矛盾、pairwise forbidden-difference 无可用值、
深度注入/parent 约束不可能、全局奇偶无目标值，或 Wiener 的安全区间/同余条件
不可能。通过只写
`NOT-EXCLUDED_BY_PARTIAL_DOMAIN_AUDIT`，绝不写成存在性证明。

已完成的轻量检查：

- genuine order-6 L6（`s=8`, domains=`0`）通过，`failure_layers=[]`；
- r8 冻结域的失败层为 `[global_parity,wiener]`；
- r9 冻结域的失败层为 `[wiener]`；
- r9 全深度宽域通过（说明该原型不会把宽域凭空判死），而只含
  `12..14,1..2,1..3,2..4,23..25,32..34,76..78,100..102` 的窄域仍由
  Wiener 必要条件拒绝。

这只是候选传播器，尚未接入 production DFS，也没有启动任何 284/285 批量计算。
Fable 应先给出它的 soundness 引理和一个独立小型 matching/differential oracle；
若不能证明“失败必排除整个域盒”，应撤回该剪枝而保留为诊断工具。

同一差分随后在 Geo Workstation 的独立 scratch 上复跑：
`remote_scratch/partial_domain_v2_smoke_20260902/result.json`，单进程
`nice -n 15`、`timeout 60s`，`RC=0`、`ELAPSED=19.96s`、`MAXRSS=11796 KB`，
结果哈希为
`02d515b68aa39ebe4d11008659f796d2ec39930fbd3a354fd4dd8c3598a6d578`。三项控制
与本地输出一致，`soundness_ok=true`；这仍是接口级远程复现，不授权 284/285 批量。

独立差分脚本为 `theory-lab/s1_crowding/partial_depth_domain_differential.py`，
SHA-256 为
`b41c061b84220f760bcdd8339a8c0dad52dce598f3b08a382b823cb6ea8c8131`。它直接逐个
检查具体 depth tuple（不导入 fixed-candidate `presolve`），并以 genuine L6 正例、
r8 singleton、r9 三值域盒作 soundness gate；本轮输出为 `soundness_ok=true`，
L6 有 1 个具体必要系统 survivor 且域审计未拒绝，r8/r9 均无 survivor 且拒绝层
分别为 `[global_parity,wiener]`、`[wiener]`。这仍是小型接口验证，不足以授权
284/285 远程批量。

## 14. 域并集拒绝的 soundness 说明（给 Fable 复核）

设某一 low 类的当前域为 `D_v`，定义
`U_v = ⋃_{l∈D_v} (2B-2l+S_v) \ (H ∪ occupied)`。任意真实域内赋值的
`T_v` 都是 `U_v` 的子集；因此真实的互斥类集合若存在，就必满足每个类子集的
Hall 和 parity-Hall 容量不等式。真实类和的取值也落在代码计算的
`possible_sum_interval` 内，所以若该区间与可用槽的最小/最大 `D_Q` 项和完全不交，
moment-Hall 拒绝也是 sound。类似地，若所有域值对都违反
`2(l_i-l_j) ∉ S_i-S_j`，或 Wiener 的安全区间/同余筛无解，则域盒确实没有
必要系统 survivor。

这里的关键限制是并集忘掉了不同 low 类之间的深度相关性；所以通过不能证明存在，
也不能把“域并集通过”当作 production 搜索已完成。任何更强的传播（例如把
component-mass 或 exact LL/LH owner ledger 加进来）都必须先给出同样的全域量词
证明和独立差分。

## 15. 人工双-low/三-low 控制的边界

仓库里已有的人工双-low 正例（`delta=10,s=9,L=[0,1]`）和三-low 负例来自
translated-sumset/BFS 接口控制；它们不是满足 order-25（甚至不一定满足完整
order-6）Wiener 与全局奇偶目标的 Leech 候选。因此把它们直接喂给本 presolver
而要求整体通过，会得到全局 `parity/Wiener` 拒绝，这不是误删，而是控制层次不匹配。
Fable 若要用它们做 zero-false-reject，应只比较 raw `S_i-S_j`、平移互斥、LL owner
账本等局部接口；全局 parity/Wiener 必须另用 genuine positive control 校验。
H/S 完整分割 guard 补上后，又在同一 Workstation scratch 复跑，结果文件为
`remote_scratch/partial_domain_v2_smoke_20260902_result.v2.guard.json`，哈希仍为
`02d515b68aa39ebe4d11008659f796d2ec39930fbd3a354fd4dd8c3598a6d578`；
`RC=0`、`ELAPSED=3.34s`、`MAXRSS=11732 KB`，且 `soundness_ok=true`。这只确认
新 guard 没有改变三个控制的已知结果，不是生产搜索证书。

## 16. Hoffman2 首个完成分片的独立验收

r8 的 `split_10_of_64.txt` 已原子完成。新增的
`theory-lab/s1_crowding/verify_depthv7_partial_shard.py` 在本地复制文件和
Hoffman2 原地各运行一次，均返回 `VERIFIED_PARTIAL_SHARD_EMPTY`：7 个预期结构
全部出现，末尾为 `COMPLETE`，无 `NODE_LIMIT/TIMEOUT`，
`total_depth_survivors=0`、`total_structure_survivors=0`。分片文件 SHA-256 为
`d36bdb73344a7a4f319dd6c743804acf6ce1625d2f332f302389efe1b49aef0b`，形状输入
SHA-256 为 `928f5f178e0f0848c8d1d45bbb0141f50cd46832932fc69344e2268fc816fb41`，
验收证书 SHA-256 为 `86c0450b9d77ac3ec604f19a2870be74d12cee326043f48876b3c9b94e2dd068`。
这只验证 r8 的一个分片，不代表其余 63 片、r9 或全域证明。

随后 `split_9_of_64.txt` 也在本地复制文件与 Hoffman2 原地各通过同一验收器：
7 个结构全部出现、末尾 `COMPLETE`、survivor=0、无 `NODE_LIMIT/TIMEOUT`。
分片 SHA-256 为
`bde5093f4ecc2f7b216088aa494978af06b1c59cdfb0f804e59007b06a5b22dd`，验收证书
SHA-256 为
`992a0a3a96b004b113bc451ee10fe90d01a2b14b304b61da5675507eecbf0b7b`。当前 r8
可验证空分片为 2/64，仍不代表全数组覆盖。
