# Fable 接手审计报告 — 2026-09-01/02

对应 handoff：`docs/handoff-fable-leech-tree-audit-2026-09-01.md`。
技术细节、哈希与命令在 `docs/checkpoint-2026-09-01-s1-top-block-crowding.md`；
新代码全部在 `theory-lab/s1_crowding/`（与 `remote_scratch` pipeline 无共享代码）。

## 1. 接手日期与 revision

- 接手：2026-09-01 16:30 左右（EDT）；本报告截至 2026-09-02 03:40 EDT。
- 本地 checkout：`master`，HEAD `ffc2012`（"Record exact cut-owner retention
  audit"），工作区含未提交的 checkpoint 文档；本轮未 commit、未 push、未删除任何
  已有文件，只追加。
- 远程：Geo Workstation `/home/geo/codex-work/leech-trees/`（`remote_scratch/...`
  与新目录 `theory-lab/s1_crowding/`）；Hoffman2
  `$SCRATCH/leech-trees/theory-lab/s1_crowding/`（SLURM campus/campus24）。

## 2. 读取过的文件

- `research_state.md`（首尾及 S1-279 相关章节）、`README.md`（问题定义、FW283–FW308
  链）、`docs/exact-return-33-g7-singleton-final-cap-sharpening.md`（S1-279 normal
  form、top-block lemma、parity、crowding 归约）、`docs/checkpoint-2026-08-31-s1-279-s152-chain-d1-16/18/20.md`、
  `docs/checkpoint-2026-09-01-s152-chain-remainder-forest.md`、
  `docs/consultant-handoff-leech-tree-chat2-20260831.md`、`data/known_leech_trees.json`、
  `src/checker_a.py`。
- `remote_scratch/s1_279_high_s_five_value_root_signature_20260831/` 全部 `_s154`
  文件及其 s152 原版：`exact10_full_low_root_signature.cpp`、
  `replay_exact10_full21_s154.cpp`、`prefilter_fw303_gate_compatibility_s154.py`、
  `search_fw303_all_class_forests_s154.py`、`replay_fw303_all_class_forests_s154.cpp`、
  `replay_fw303_remaining_classa_forests_s154.cpp`、`forest_batch_job_v2.sh`。
- 远程结果：`forest_shards_s154_chain/python_0000_000549.json`（首片）、
  `forest_pilot_cpp_s154_chain_0_50/summary.json`、`forest_shard_plan_s154_chain.json`。

## 3. 分类结论

### VERIFIED（我独立重推导并机器核对）

- singleton final cap 的 spectrum identity `F ⊔ (s+D) = [1,300]`、top-block lemma
  `D = L ⊔ [B,A]`、`δ=277,278` 的 parity 排除、`δ=279` 强制 `s,d1,d2` 偶、
  `δ=280` 强制 `s,d1,d2,d3` 偶（`verify_s1_top_block_crowding.py` 第 (1) 节）。
- **Top-block crowding 定理（新）**：`m=24-r` 个 high 顶点的 `C(m,2)` 个两两距离按
  LCA 分成 `r+1` 类，类内距离是 `y+y'` 的单射函数（LCA high：`y+y'-2q`；LCA 为深度
  `l` 的 low 顶点：`2B-2l+y+y'`），每类至多 `2m-3` 个不同值。
  `r=3`：210 > 4×39=156；`r=4`：190 > 5×37=185。因此 **S1-279 与 S1-280 对所有 `s`、
  所有 low shape、所有 `d_i` 都不可能**，不依赖 FW303 core、`c` 范围或
  `{4,5,16,18,19,20}` 字母表。

### REPRODUCED（独立实现复现旧结论）

- 直接 DFS（`s1_direct_search.cpp`，只用 normal form）扫 `δ=279`：`s∈[13,160]`、两种
  shape、任意奇偶 `0<d1<d2<B`，5,725,972 个实例、零幸存、零中止（geo-ws，4 分钟）。
  覆盖并超出旧 pipeline 的 `s=152/154` star/chain 全部分片；旧结果与之一致。
- 首片 `python_0000_000549.json`：已自然结束（440 s、2.2 GB、1530 jobs、幸存 0），
  与定理一致。

### CERTIFIED FINITE IMPOSSIBLE（新，有限但完整的机器证书）

- `δ=281`（`r=5`，9 个 rooted low-tree 同构类）与 `δ=282`（`r=6`，20 类）：depth-free
  class search（`abstract_class_search.cpp`，只用类内单射条件，不依赖 `s` 与 low 深度）
  零结构。
- `δ=283`（`r=7`，48 类）：47 类零结构；链状类恰 14,730 个结构，对每个结构穷举
  `(s,L)` 零幸存。两套独立运行（geo-ws 单进程；Hoffman2 64 片）在
  `leaves=14730, csp_nodes=16302184, survivors=0` 上一致。
- 工具验证：depth-free search 与子代理独立写的暴力枚举器在 8 个小案例上计数与结构集
  完全一致；depth-CSP 与直接 DFS 在 relaxed target 上逐案计数一致（chain 相等，star 恰
  为自同构 2 倍）；已知 6 点 Leech 树作为正向对照被找回。

### FINITE-EVIDENCE / 进行中

- **`δ=284`（`r=8`）：CERTIFIED FINITE IMPOSSIBLE**（2026-09-02 07:05 EDT）。Hoffman2
  数组 64 任务全部完成（每任务 2–4 小时），验收脚本返回
  `VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY`、`errors=[]`：7 个形状共 16.4 亿个 depth-free
  结构、4921 万个不同 ρ、零幸存（链状形状占 16.2 亿）；证书 SHA-256 `b5769434…`。
  非链状形状的逐片叶子数与逐叶 CSP 的 v4 实现一致。
- `δ=285`（`r=9`）：286 类中 95 类有结构；v7 数组 256 任务运行中。每个任务按同一顺序
  处理 95 个形状，所以即使触及 24 小时上限，所有任务都完成的前几个形状仍构成这些形状的
  完整证书。
- 已停掉 geo-ws 上冗余的 4 个 worker（与 Hoffman2 数组重复，且工作站 load 已近 190）。
- `δ=286`（`r=10`）：depth-free 扫描完成，719 类中 317 类有结构（Hoffman2，无中止）；
  深度阶段未启动。
- `δ=287`（`r=11`）：1842 类中 1523 类有结构——depth-free 结构在此已接近普遍，
  纯 top-block 方法到此为止；更大 `δ` 需要新论证。
- 实验记录：纯 ρ-first 搜索（`rho_first_search.cpp`）与前缀级 ρ-CSP 剪枝
  （`--rho-check`）在 `r=7,8` 上都比 abstract-first + 叶子级记忆化慢，已放弃部署但
  代码与对照结果保留。

### CANDIDATE（未验收的思路）

- 两点 final cap（`h=2`）的 top-block 版本：`D ∪ (D+t)` 覆盖顶端区间，只能给出宽度
  `46-r'+t` 的窗口，crude counting 不够；未进一步做。
- 大 `δ`（`r>=10`）的 singleton 分支：top-block 约束随 `m=24-r` 变小而失效，但 FW303
  core（6 顶点、边权 1,2,6,7,10 的刚性子树，本轮未审计）会把 6 个顶点的深度差固定成
  一个刚性模式；若把 core 放置与 ρ-first CSP 结合，`L` 的自由度从 `r-1` 降到约 `r-6`，
  可能使 `r=10..14` 可计算。这依赖 FW303 core 定理的正确性，属候选路线。
- 记忆化 ρ-CSP 的前缀剪枝（`--rho-check`）：已实现并通过对照，效果待计时。

### UNKNOWN / 未审计

- FW283–FW303 整条链（final-cap 结构、"最重边是最后 activation"）我只核对了 singleton
  case 所需的 identity；其余未审。
- 非 singleton 的 final cap、`R2-COVER`、`T4-COVER`、全局非存在性：本轮不涉及。

## 4. 发现的量词或实现问题（旧 pipeline，只读审计）

1. `replay_fw303_remaining_classa_forests_s154.cpp` 与 s152 版本逐字节相同
   （`S=152,B=128,D1=18,c<=13`，四个 s152 case）。未被任何驱动脚本调用，但若当作
   s154 证据则错误。
2. `replay_fw303_all_class_forests_s154.cpp:469` `"d1_max": 124` 为 s152 残留（s154
   应为 122；仅 JSON 标签，L431 的 `d2>=126` 守卫正确）。
3. `replay_exact10_full21_s154.cpp:61` 不检查 `REPLAY_D1` 奇偶：奇数 shard 会静默返回
   `params_valid=0`（primary 会报错）。
4. `replay_fw303_all_class_forests_s154.cpp:221` 用计数器而非 map 大小计 `f_c`，同
   index core 碰撞会静默丢边（几何上不可达，未设防）。
5. 主链路四文件（prefilter/search/replay/exact10-replay）的 `B=280-s`、`c<=14`、
   `d2<126`、38 行目录与 A/B/C 分类均正确；边账本无重复计数路径。整个 forest 的唯一
   承重外部前提是“非 core HH 边权 ∈ {4,5,16,18,19,20}”（FW303），代码中未推导。
6. 更根本的问题：exact-10 只检查 10 个 root 的 root-root 与 low-high 距离，是极弱的
   松弛（5.2M 幸存），而完整 21 个 high 顶点的 210 个 HH 距离按 4 类计数即矛盾。旧路线
   把一个鸽巢命题变成了 1286 片重型枚举。

## 5. 更优结构性路线（soundness）

- 见 §3 定理：完整性来自“每对 high 顶点恰属一类、类内距离单射于 `y+y'`”，均为树度量
  恒等式，已用 BFS 随机树核对。
- `r>=5` 的推广：depth-free class search 是该定理的机械化（必要条件，不含 `s`、`L`），
  空则关闭整个 `δ`；非空时进入深度阶段（`(s,L)` CSP），幸存者即真实候选树。
- rho-first 分解（`rho_first_search.cpp`）：先枚举 high→low 归属 `ρ`，只依赖 `ρ` 的
  值（x-h、low-high、low-low、holes、跨纤维 HH）先解 `(s,L)`，几乎所有 `ρ` 在此被杀；
  幸存的 `ρ` 才枚举纤维内部结构。与前两种实现在对照上一致。

## 6. 对首片运行的建议

**改路线。** 首片已结束且无需继续；1286 片 forest、38-row 预筛与 555,397 签名 union 全
部被定理涵盖。旧 pipeline 的零结果可作为一致性证据保留，但不应再消耗算力。

## 6b. 目录中不属于本轮的文件

`theory-lab/s1_crowding/` 在 2026-09-02 00:24–03:27 EDT 间被另一会话写入了
`audit_abstract_aggregate.py`、`colored_moment_hall_audit.py`、
`colored_moment_hall_presolve.py`、`component_mass_dp.py`、
`component_mass_dp_compressed.py`、`global_distance_slot_flow_pilot.py`、
`joint_interval_hall_differential.py`、`joint_interval_hall_pilot.py`、
`mass_depth_hall_pilot.py`、`parity_moment_audit.py`、
`translated_difference_domains.py`、`translated_sumset_csp_pilot.py`（按其
docstring 是基于本轮 STRUCT 记录的必要条件预筛/审计）。这些文件不是我写的，
我未读其正文、未验证、未同步到远程，也不计入本报告的任何结论。

## 7. 实际修改文件与命令

新增（未改动任何旧文件）：
- `theory-lab/s1_crowding/verify_s1_top_block_crowding.py`、`s1_direct_search.cpp`、
  `abstract_class_search.cpp`、`rho_first_search.cpp`、`hh_capacity.cpp`、
  `brute_abstract_check.py`（子代理）、`run_r3_full_sweep.sh`、
  `hoffman2_s1_abstract_array_slurm.sh`、`hoffman2_s1_depth_array_slurm.sh`、
  `shapes_r7_chain.txt`。
- `docs/checkpoint-2026-09-01-s1-top-block-crowding.md`、本报告。
- `research_state.md`：只追加两段。

关键命令（均在对应机器 `theory-lab/s1_crowding/` 下）：

```bash
python3 verify_s1_top_block_crowding.py
./s1_direct_search --r 3 --s 154 --shape chain --all-d
./run_r3_full_sweep.sh                      # geo-ws, 4 x nice -n 15
./abstract_class_search --m 19 --r 5 --all-shapes
./abstract_class_search --m 18 --r 6 --all-shapes
./abstract_class_search --m 17 --r 7 --all-shapes --stop-first --shard K 4   # geo-ws
./abstract_class_search --m 17 --lowpar 0,1,2,3,4,5 --solve-depths            # geo-ws
sbatch --array=0-63 hoffman2_s1_depth_array_slurm.sh 17 shapes_r7_chain.txt 5 64 r7chain
sbatch --array=0-15 hoffman2_s1_abstract_array_slurm.sh 8 16
sbatch --array=0-31 hoffman2_s1_abstract_array_slurm.sh 9 32
```

## 8. 独立验证命令及结果

见 checkpoint §3.1–3.7；摘要：

```text
verify_s1_top_block_crowding.py      -> VERIFIED_S1_TOP_BLOCK_CROWDING_ARITHMETIC
s1_direct_search  L6 control         -> survivors=1 (s=8)
s1_direct_search  r=3 full sweep     -> 5,725,972 instances, survivors=0  (SHA d130f57d...)
brute_abstract_check.py (8 cases)    -> counts and structure sets identical to abstract_class_search
abstract_class_search r=5/6          -> NO_STRUCTURE (9 / 20 classes)
abstract_class_search r=7            -> 47 classes empty; chain 14730 leaves, depth_survivors=0 (two runs)
rho_first_search differential test   -> 1385/501/190/34 and 5182/2232/714/126, identical to direct search
```

## 8b. 2026-09-02 新定理：直径端点归约（改变全局策略）

设 (a,b) 是唯一的距离 300 的点对（都是叶子）。对任意两个非端点 u,v，
`d(u,v) = 300 − f(u) − e(v) − 2h_c`（e、f 是到 a、b 的"缺口"，均 ≥ 1，h_c ≥ 0），
所以避开 a、b 的点对距离 ≤ 298，299 必须由 (a,w) 或 (b,w) 实现；改名后
`d(a,w)=299`，于是 `diam(T−b)=299`，`diam(T−a) ≤ 298`。再由本轮结果（任意叶子
`diam(T−ℓ) ≥ 284`），得 **284 ≤ diam(T−a) ≤ 298**。因此 25 阶不存在性 ⟸
singleton normal form 对 δ∈[284,298]（所有 s、所有 low 结构）无解。这条归约只用
叶子 a 的谱恒等式，不需要"最重边悬挂"假设，也不再需要两点帽子等其它分支。
δ≥286 时 top-block 变短，必须引入第二个锚点（K 的最小边权 forcing lemma）。

## 8c. 论文草稿 v4（2026-09-02，由 Opus 子代理撰写、我抽查了新定理的表述与证明）

`paper/Meng-Leech-draft-v5-2026-09-02.pdf`（31 页，tectonic 零错误零警告；v4 为 30 页的
前一版）。v5 已把 δ=284 证书并入（证书定理覆盖 281–284，归约范围 [285,298]），并注明
链状形状只有记忆化实现的单次运行、其余六个形状有两套实现逐片一致。新增第 8 节
"Removing a diametral endpoint: top-block crowding at order 25"：叶子谱恒等式与
top-block 引理（对任意叶子）、parity 引理、直径端点归约定理（含加强：避开 a、b 的
点对距离 ≤ N−3）、crowding 不等式（一般阶：`diam(T−ℓ) > C(n−1,2) + (n−12)/5`）、
δ=281–283 的有限证书（含全部 SHA-256）、25 阶归约推论（iff 形式）、以及"未证明什么"
段落。标题、摘要、引言、讨论、数据可用性均已更新。δ=284/285 按"运行中"处理，
未作声明；源码哈希漂移已在论文中标为 `\todo`（本轮把当前源码冻结到
`theory-lab/s1_crowding/frozen/`，文件名含哈希）。论文对 δ=277/278 的处理改为
"parity 只用于确定 s 与低深度的奇偶"（crowding 计数本身已排除 δ≤280）。

## 8d. 思路二（全局深度序搜索）的 pilot 结论（Opus 子代理，`theory-lab/depth_search/`）

按深度递增放置顶点、带类内单射/forcing/Hall 等剪枝的通用引擎已实现并在 n≤11 上
验证（找回全部已知 Leech 树、7–11 阶为空）。结论是**否定的**：节点数每加一阶增长
9–10 倍，比按边权序的 forest 引擎在 n=11 就多 288 倍且差距随 n 扩大；forcing lemma
在深度序下几乎无剪枝力（<1%）；normal form 的 top block 只削掉便宜的深层分支，代价
集中在 r 个自由的低深度上。外推 25 阶：普通模式 4e12–2e14 CPU 小时，normal-form
扫描 3e14–1e16 CPU 小时（forest 引擎外推约 2e6–1e7，也不可行）。因此 δ≥286 的剩余
情形不能靠现有设计的直接搜索完成，需要新的数学想法。该代理提交的 22 个测量任务
（数组 118739）我已取消，以免占用队列。

## 8e. 思路一（顶端窗口和集平铺）的初步实验（`theory-lab/s1_crowding/top_window_skeletons.py`）

把两端缺口 `(e,f)` 与恒等式 `d(u,v)=300−f(u)−e(v)−2h_c` 做成"顶端窗口骨架"枚举器：
对每个层级 `t=1..W`（距离 `300−t`）决定它由 A-step `(a,v)`、B-step `(u,b)` 还是
交叉对实现，顶点按需创建，所有 e 值/f 值互异且 `E∩F=∅`、同一顶点 e≡f (mod 2)、
p-序与同支修正都纳入。它是必要条件枚举器（骨架不含树的其余部分）。结果：

```text
W   distinct level patterns   distinct small structures (pattern,E',F',cross)
3           4                        94
4           8                       510
5          14                     2,192
6          24                     7,638
7          42                    27,932
```

模式数约每层翻倍、结构数约 ×3.6/层，主导模式是 `AAA…AB`（即 a 的 top block 后接
一个 B-step，正是 §3.10 的 `F={0,m,…}` 结构）。结论：顶端窗口本身约束不强，单独
不能杀死任何 δ；它的价值在于作为 S1 搜索顶端的模式级预筛，以及与底端（最小边权
forcing）联立——这是下一阶段的方向，本轮未再推进。

## 9. 仍未闭合的最小命题

- **S1-285**（`r=9`）：95 个形状的深度阶段（Hoffman2 数组 `118376`，256 任务运行中；
  监视器会在完成时自动验收）。
- **S1-286 及以上**：`r=10` 有 317/719 类、`r=11` 有 1523/1842 类存在 depth-free
  结构，abstract-first 方法的代价随 `r` 指数增长（r=8 约 150 CPU 小时，r=9 运行中），
  直接搜索按 pilot 估算不可行。需要新的论证：把顶端窗口的和集平铺结构
  （缺口集 E、F 的唯一表示分解）与类内单射结合，或找到把大 δ 情形归约到小 δ 的
  结构性引理。
- singleton 之外的 final cap 分支（两点 cap 的 FW304–319 主线等）未触及。

## 10. 远程作业与文件位置（交接）

- Hoffman2（SLURM 登录节点 `192.154.2.206/.207`；`.205` 本轮后半段不可达，
  `.201–.204` 是旧 UGE 节点、无 squeue）：`$SCRATCH/leech-trees/theory-lab/s1_crowding/`。
  数组 `118375`（r=8，`depthv7_r8/`）、`118376`（r=9，`depthv7_r9/`）；已完成的证据目录
  `depth_r7chain/`（含 `certificate.json`）、`abstract_r8..r11/all_sorted.txt`。
- geo-ws：`/home/geo/codex-work/leech-trees/theory-lab/s1_crowding/`，已完成
  `r3_full_sweep/`、`abstract_r7/`、`depth_r7/`；当前无我的进程。
- 本地：`theory-lab/s1_crowding/`（源码），`docs/checkpoint-2026-09-01-s1-top-block-crowding.md`。

## 11. 新方向（本轮后半段）：双端 normal form 与 gap-order 引擎

思路一（顶端和集平铺）推到底之后变成了一个**完整的重新表述**，比原来的"顶端窗口"
强得多，且**没有 δ 参数**：整个 n 阶问题变成一个有限的加法覆盖问题。

**表述。** (a,b) 为唯一直径点对（必为叶子），P 为 a–b 路径，长 N。对其余 V=n−2 个
顶点令 e=N−d(a,u)、f=N−d(b,u)，则 p=(N+f−e)/2、h=(N−e−f)/2，e+f≤N、e+f≡N (mod 2)、
E 与 F 不交。核心公式（Lemma A，与顺序无关）：

    gap(u,v) = min(f_u+e_v, f_v+e_u) + 2 h_c(u,v)

h_c=0 除非 p_u=p_v。于是 T 是 Leech 树 **当且仅当**
`{0} ⊔ E ⊔ F ⊔ {gap(u,v)} = [0,N−1]`（共 1+2V+C(V,2)=N 个互不相同的值）。

**由此立刻得到的引理**（全部在 `theory-lab/double_end/THEORY.md`，并经数值验证）：
- 奇偶劈分：n=25 时 (α,β)∈{(13,10),(8,15)}，α=e 为偶数的顶点数。这是 Taylor 奇偶
  障碍在本表述下的精确化。
- 附着引理：h>0 的顶点所在分支必挂在同一 p 处的一个 h=0 顶点上，该顶点的两个坐标
  **完全确定**为 ((N−d)/2,(N+d)/2)，d=f−e。
- 覆盖引理（Lemma D 及推论）：`(A+1)(B+1) = [0,N−1] + H + Σ x^{M_ij} + 并列修正`，
  故 E∪{0} 与 F∪{0} 的和集覆盖 [0,N−1]，例外只可能是 h_c>0 的并列对所实现的 gap。
- Golomb：路上顶点连同 a,b 的位置构成长度 N 的 Golomb ruler；由已知最优 Golomb ruler
  长度，N=300 最多 20 个刻度，故 25 阶至少有 5 个顶点挂在主路之外。
- 球计数：任何半径 D 的球 B 满足 C(|B|,2) ≤ 2D。

**搜索。** 每个 e、f 本身都是一个 gap，于是可以按 gap g=1,2,… 递增处理，并**延迟指派
配偶坐标**。关键引理：若某 pair 的 gap ≤ g，则相关两个坐标都 < g、已知，故该 pair 已
确定或已登记为并列待定。因此**最小未实现的 gap 只能是某个坐标，或某个并列待定对的
解析**——其余 gap 全部被强制。搜索深度恰为 2V 次坐标决策。

**验收（重要）。** `brute_double_end.py` 是一个**完全独立**的顶点序枚举器；
`differential_test.py` 在关闭全部可选剪枝后对拍两者：n=3,4,6 **完全一致**（n=6 纯松弛
有 12 个解）。开启全部剪枝后引擎恰好保留真树，并用重建树 + BFS 验证：n=3,4,6 各 1 棵
（对称性破缺后）。**n=9 穷尽、零解**。（该处初稿写的 67,432 是加入 `ub_prune` 与祖先一致性条件之前的
数字，已作废；当前值为 24,335（对称性破缺开）/ 48,669（关）。）
验收过程中发现并修正三个真 bug（此前数字作废）：不健全的 `hc_heights`；deferred 列表
边遍历边删的索引错位；以及最严重的——**待定 pair 会因 g 增大而自动变确定**，必须每步
重扫，否则漏解。这三个都会给出错误的"无解"结论，记录在此以便复核。

**现实评估。** 节点数 n=6→9 增长约 10^3。C++ 移植 + Hoffman2 分片（约 10^4–10^5 倍）
之后，n=16、可能 n=18 是可及的——那将是对已知不存在性的**独立第二证明**，有论文价值。
n=25 按当前增长仍不可及，需要进一步的结构性引理。**在得到完整证明之前，任何有限计算
的零结果只能标为固定范围的 CERTIFIED FINITE IMPOSSIBLE。**

### 11.1 与已有证书链的接口，以及一个独立复核目标

在双端语言里，令 `s := min(F ∪ {pair gaps})`。则 `diam(T−a) = N − s`，而按定义 gap
`1,…,s−1` 全部是 e-值。于是

    diam(T−a) ≤ 284   ⟺   s ≥ 16   ⟺   gap 1,…,15 全部是 e-值。

因此：**把双端引擎限制为"gap 1..15 全部指派为 e-坐标"并穷尽，若零解，就独立重证了
δ=279..284 的整条证书链**（top-block crowding 定理 + 四个有限证书），且是完全不同的
算法与不同的正规形。这正是项目要求的"双实现验收"。该子搜索被前 15 步完全锁死，规模
应远小于完整的 25 阶搜索，是下一步最值得跑的目标。

反过来，仍然开放的 `δ∈[285,298]` 对应 `s ≤ 15`，在双端搜索里是**弱**限制，所以已有
证书对完整 25 阶双端搜索帮助不大。

### 11.2 规模外推（诚实版）

节点数（Python，全部剪枝 + 对称性破缺）：n=3:3、n=4:8、n=6:44、n=9:24,335。
按 `log10(nodes) ≈ 0.92·V − 2.0`（V=n−2）外推：

| n | V | 预计节点数 | C++ 约 3e6 节点/秒时的 CPU 时间 |
|---|---|---|---|
| 11 | 9 | ~2e6 | 秒级 |
| 16 | 14 | ~6e10 | 约 6 CPU 小时 |
| 18 | 16 | ~5e12 | 约 500 CPU 小时 |
| 25 | 23 | ~1e19 | 约 1e9 CPU 小时 |

**该外推随即被实测推翻，记录在此以示错误。** C++ 实测：n=11 在 2.5e7 节点未完成，
本地再跑（负载 112–120 的机器上）超过 1e8 节点仍未完成。故 n=9→n=11 的增长 >4000×
（ΔV=2），即每单位 V 约 65×，远高于 n=6→n=9 的 8.2×/V；增长率本身在增长。修正后
n=16 的估计升到 1e17 级，n=18 更高。**因此"n=16、n=18 可及"这个说法在拿到 Hoffman2
的实测之前不成立**，已提交 n=11（32 分片，作业 119549）与 n=16 抽样（8/128 分片，
作业 119550）测量真实规模。在实测结果回来之前，对 n≥11 不作任何可及性断言。


### 11.3 C++ 移植的验收（Opus agent 完成，我复核）

`theory-lab/double_end/double_end_search.cpp`（925 行，C++17，无依赖）。验收强度超出
节点数比对：agent 增加了 `--trace`（每次 `rec()` 输出 g、nv、e[]、f[]、|deferred|），
并用 monkey-patch 从 Python 生成同格式 trace，**8 种配置（n=3,4,6,9 × 对称性开/关）
逐字节相同**。我本机独立复跑 n=9 得 24,335 节点 / 0 解 / EXHAUSTED，与 Python 一致；
Hoffman2 上重新编译后 n=3,4,6,9 亦全部一致。

剪枝消融（n=9）：`--no-hall`、`--no-lb`、`--no-cover` 无影响；`--no-parity` 24,450；
`--no-deferred-check` 25,997；`--no-ub` 28,338；`--no-ultra` 1,462,492；
`--no-hc` 11,942,021；`--no-attach` 105,230 **且解数从 0 变成 18**——这是正确方向
（`attach_ok` 是树可实现性条件，关掉它松弛变大），且这 18 个解全部被 `--verify` 以
`no on-path attachment vertex at p=…` 否决。**没有任何剪枝丢失过真树。**

移植过程中发现两个 bug：(a) agent 自己的候选列表被递归覆写（由 trace 差分定位）；
(b) **我的 Python 的 `undo` 把恢复的 deferred 对追加到列表末尾，使 `rec()` 非状态中性**。
这不影响未分片的结果（节点数与解集不变，已复核），但会破坏 `--split`：实测 n=9、
LEVEL=10、M=4 时各分片节点之和比正确值少 468。已在 C++（`--stable-deferred`，由
`--split` 自动启用）和 Python（按原索引 `insert` 恢复）中修正，修正后 n=3,4,6,9 的
八个基准数字全部不变。分片划分性由 trace 多重集逐一比对证明（6 种配置全部相等）。

## 12. 切合实际的论文计划（2026-09-02 更新）

**论文一（现稿，v5，31 页，可投）——"18 阶 Leech 树不存在"。**
已有：18 阶穷尽 + 逐拓扑验收、蜘蛛图的一致定理、M(12)=77、相邻问题、以及第 8 节的
25 阶 top-block crowding 定理与直径端点归约、δ=281..284 的有限证书。
待补三处 `\todo`：(1) n=18 逐拓扑复跑；(2) δ=284 冻结源码复跑（约 130 CPU 小时）；
(3) δ=285 证书。其中 (3) 正在 Hoffman2 上跑，成本约 1e4 CPU 小时，会撞墙一次、
需收割重投（工具 `harvest_partial_splits.py` 已就位并测试过）。
**必须写清楚：δ≤285 是固定范围的 CERTIFIED FINITE IMPOSSIBLE，不是 25 阶猜想的证明。**

**论文二（新，起草中）——"Leech 树的双端正规形"。**
内容：Lemma A 与等价定理（整个 n 阶问题化为一个无 δ 参数的有限加法覆盖问题）、
奇偶劈分的精确形式、附着引理、Lemma D 及其（诚实标注的）平凡推论、主路的 Golomb
ruler 界、球计数界；gap 序搜索引擎及其判定引理与重扫步骤；三重验收（独立顶点序枚举器
对拍、独立暴力枚举真值、逐字节相同的 C++ 移植）；n≤9 的独立重证；以及 25 阶的归约：
`diam(T−a) ≤ 284` 等价于"gap 1..15 全为 e-值"，故一次受限运行即可用完全不同的算法
独立重证整条 δ=279..284 证书链。
论文二**不宣称** n≥11 的任何可及性，除非 Hoffman2/geo-ws 的实测支持。
第 5 节须保留"验收中发现四个真 bug、此前数字全部作废"的记录——这是可复现性的一部分，
不得淡化。

**优先级。** 论文一先投；论文二等 n=11 与 25 阶受限运行的实测数字落地后再定篇幅：
若受限运行能穷尽，论文二有一个硬结果（独立第二证明）；若不能，论文二仍是一个干净的
新正规形加验收充分的引擎，但结论只到 n≤9。

## 13. 收官（2026-09-03/04）：双端引擎的最终定位、论文 todo 清理、以及我自己的错误

### 13.1 双端引擎的确定结论

**正面（VERIFIED / CERTIFIED FINITE）**
- `n = 3,4,6,9,11` 全部由双端引擎独立判定。`n=11` 穷尽、零解、**3,338,887,905 节点**
  （geo-ws 单进程约 9 小时 wall）。这是用与项目原有方法完全不同的正规形与算法，
  独立重证了 11 阶不存在。`n = 5,7,8,10` 由奇偶命题不展开一个节点即排除。
- 独立验收三方一致：原理不同的枚举器对拍、从零重写的暴力枚举 oracle、
  Python 与 C++ 逐节点轨迹逐字节相同。

**负面（实测，非估计）**
- 节点数序列 3、8、44、24,335、3,338,887,905（V = 1,2,4,7,9），每单位 V 的增长为
  2.7、2.3、8.2、**370**，增长率本身在加速。**n=16、n=18 不可及**（n=16 外推约 1e22 节点）。
- **25 阶受限运行（`--force-e-upto 15`，等价于 diam(T−a) ≤ 284）不可行。** 采样实测：
  从 20000 路切分（第 47 层）取 200 个分片、各 2 小时墙，**运行的 100 个无一穷尽**。
  按实测 1.4e5 节点/秒/核，每个 1/20000 分片 > 9.8e8 节点，故
  **总规模 > 1.96e13 节点 ≈ 4e4 CPU 小时，且这是下界**。
  对照：δ=284 证书是 1.64e9 个结构，δ=285 估价约 1e4 CPU 小时。
  **结论：25 阶上双端搜索比它本要检验的 δ 程序贵至少一个量级。** 原因清楚：固定 δ 就固定了
  顶块、crowding 随即剪枝，而无参数形式一次探索所有可行 δ。

### 13.2 论文状态

正文三个 `\todo` 已按作者批准的方案处理，全部改写为终稿正文而非删除：
1. **n=18 逐拓扑旁证**——明确"有意停在 91.6%"（112,082/122,344，零 SAT），
   给出成本（剩余 1,169 个正是最难实例，projected 1e4–1e5 CPU 小时）与"不增加逻辑强度"
   的理由，保留"若报出 SAT 则定理必须撤回"。
2. **δ=285**——本文不作主张；记录 24,320 个 (split,shape) 对中完成 3,196 个、
   全部 EXHAUSTED 零幸存者、连逐文件哈希存档可续；开放区间明确为 δ∈[285,298]。
3. **δ=284 冻结源码复跑**——正在集群上运行（作业 200873，64 分片，源码
   `abstract_class_search_d83323870704.cpp`）；验收器与逐形状比对脚本
   `compare_frozen_rerun.py` 已部署并自测通过，接受判据是 7 个形状的叶子数、节点数、
   幸存者数与已记录证书 `b5769434011afa56…` 逐项相同。

双端一节（954 行）已写完，与正文零标签冲突、合并试编译零警告，`\input` 一行即可并入。
AI statement 已按作者指定的统一段落替换。

### 13.3 我在本轮犯的错误（完整列出）

1. **成本判断错误。** 我建议"25 阶受限运行的每 CPU 小时价值高于 δ=285"，作者据此把队列切走。
   我当时并不知道受限运行的规模。实测表明它至少贵 4 倍，可能更多。代价：约 400 CPU 小时、约一天。
2. **SLURM 脚本 bug。** 用了 `cd "$(dirname "$0")"`，而 SLURM 把脚本复制到 spool 目录，
   导致所有任务 3 秒内失败；我此前多次报告"排队中"是错的。已改绝对 `ROOT=`。
3. **进程检查方式错误。** Linux `comm` 截断到 15 字符，`double_end_search` 是 17 字符，
   `pgrep -x` 恒返回 0。我据此三次误判"启动失败"并重启，导致 geo-ws 上同时有 12 个进程
   （超出约定的 4 个上限两倍）、三代进程互相截断日志。
4. **"前 24 步强制"的错误结论。** 读自被节点上限截断的深度直方图；深度优先会先下潜再回溯，
   浅层计数为 1 不能证明强制。分片测试与穷尽小例都推翻了它，真实强制链恰为约束蕴含的 15 步。
5. **文档三处错误**（起草论文一节的 agent 发现，我复核确认）：`e ≡ f (mod 2)` 应为
   `e + f ≡ N (mod 2)`；判定引理的常数阈值 `g+2` 在决策时刻不健全；一处过时的节点数 67,432。
6. **杜撰标签。** 改写 todo 时引用了不存在的 `sec:deengine`、`thm:deconstraints`，
   自查时发现并改正。
7. **4 小时时限的配置失误。** 第一批 128 个分片全部撞墙，引擎无断点，该批工作全废（约 16 小时）。

以上均已写入 `research_state.md` 的对应条目，可逐条复核。
