# Leech-tree research state

更新时间：2026-09-01（当前 checkout）

## 2026-08-31 S1-279 高 `s` 前沿补充

- **CERTIFIED FINITE：** `s=152`、chain 低子树、所有偶数 `2<=d1<=36` 的
  完整有限分片不可实现。`2<=d1<=16` 的主/独立 exact-10/full-21 扫描均为空；
  `d1=18` 的两套扫描穷尽为同一 19 个规范根签名，主/独立 FW303 38-row
  检查只留下同一 4 行，主/独立完整 24 点树搜索对 `c=10,11,12,13` 均
  返回零。`d1=20` 的两套 exact-10/full-21 扫描逐项得到同一 1353 个规范
  根签名；独立重建全部 38 个 FW303 行后，两套完整树搜索对同一 3716 个
  `(signature,row,c)` 任务的全部计数逐项一致，最终 276-distance 幸存为零。
  `d1=22` 的两套 exact 扫描逐项得到同一 8711 个规范根签名；独立重建
  38 行留下同一 6693 个 Class-A 与 6 个 Class-B 行，两套完整树实现对
  26790 个任务的全部计数逐项一致，最终幸存仍为零。
  `d1=24` 的两套 exact 扫描逐项得到同一 10829 个规范根签名；独立重建
  38 行留下同一 8153 个 Class-A 与 13 个 Class-B 行，两套完整树实现对
  32651 个任务的全部计数逐项一致，最终幸存仍为零。`d1=26` 的两套 exact
  扫描得到同一 19045 个规范签名集合（输出顺序不同）；独立重建 38 行留下
  同一 13776 个 Class-A、10 个 Class-B 与首次出现的 2 个 Class-C 行。
  两套完整树实现用规范签名正文作 job key，对 55138 个任务的全部计数逐项
  一致，最终幸存仍为零。`d1=28` 的两套 exact 搜索得到同一 24220 个规范
  签名与 26652 次顺序无关补齐调用；独立重建 38 行留下 17410 个 Class-A、
  34 个 Class-B 与 1 个 Class-C 行，两套完整树实现对 69744 个规范 job key
  逐项一致，最终幸存为零。`d1=30` 的两套 exact 搜索得到同一 25952 个规范
  签名与 28382 次顺序无关补齐调用；独立重建 38 行留下 19417 个 Class-A、
  28 个 Class-B 与 2 个 Class-C 行，两套完整树实现对 77756 个规范 job key
  逐项一致，最终幸存为零。`d1=32` 的两套 exact 搜索得到同一 20921 个规范
  签名与 30714 次顺序无关补齐调用；原始 first-witness 递归计数相差
  17332334，但只改变 replay 颜色顺序的诊断精确复现主计数且签名集不变。
  独立重建 38 行留下 14921 个 Class-A 与 22 个 Class-B 行；两套完整树实现
  对 59750 个规范 job key 的七项计数逐项一致，最终幸存为零。`d1=34`
  的两套 exact 搜索得到同一 29538 个规范签名与 33715 次顺序无关补齐调用；
  原始 first-witness 递归计数相差 582091，作为不同颜色遍历顺序下的非语义
  诊断透明保留。独立重建 38 行留下 20851 个 Class-A、26 个 Class-B 与
  1 个 Class-C 行；148 个主分片无缝覆盖 `[0,29538)`，独立 C++ 回放对
  83484 个规范 job key 的七项计数逐项一致，最终幸存仍为零。完整哈希见
  `d1=36` 的两套 exact 搜索得到同一 18562 个规范签名；93 个主分片无缝覆盖
  `[0,18562)`，独立 C++ 回放对 51119 个规范 job key 的七项计数逐项一致，
  最终幸存仍为零。其 exact 计数为 `45/44/26`（total/valid/with-survivor），
  两套实现的 order-independent invocation 为 `21684`；完整哈希见对应 checkpoint。
  对应的 `d1-16`、`d1-18`、`d1-20`、`d1-22`、`d1-24`、`d1-26`、`d1-28`、
  `d1-30`、`d1-32` 与 `d1-34` checkpoint。
- **仍是 GAP：** S1-279 整体没有关闭。仍需处理 `s=152` 的 star、chain
  `d1>=38`，以及 `s in {154,156,158,160}` 的两个低树形状。不得把该有限
  分片提升为 S1、R2-COVER、T4-COVER 或全局 Leech-tree 非存在性。

## 2026-09-01 remainder exact batch

Geo Workstation 已启动 `s=152`, `shape=chain`, even `d1=38,40,...,124`
的双实现 exact 批处理，远程目录为
`/home/geo/codex-work/leech-trees/remote_scratch/s1_279_high_s_five_value_root_signature_20260831/exact10_batch_s152_chain_20260901`。
批处理 PID 为 `3267845`；每轮同时处理两个 `d1`，每个进程 `nice -n 15`，
总计算并发不超过 4。顾问只读复核确认该域有 44 个 d1 shards、990 个原始
参数和 977 个有效参数；每片需逐项核对 canonical signature 集合及语义计数，
不能只比较聚合总数。44 个 d1 分片现已全部生成 primary/replay JSON，并全部
通过 exact v2 证书；统一 batch verifier 返回
`VERIFIED_REMAINDER_EXACT_BATCH`，44/44、990 个原始参数、977 个有效参数、
failures=0。独立 replay 的 canonical union 共 24077 个签名，union hash 为
`d3480e7940cb723832b3a3a937df1e687100d1d171c520fd10382773d9ebb218`。
一次性 38-row prefilter 已在 workstation 完成：24077 个签名全部检查，
17911 个兼容 signature-row，结果 hash 为
`cfd7d39e2083df15cf89768625f0fd2f46baa8825b218c6f2019477614a20247`。
完整 forest 已在 workstation 完成：`remainder_forest_shards_v2/` 共 121 个
分片，全部 `FW303_ALL_CLASS_FORESTS_EXHAUSTED`，严格连续覆盖 `[0,24077)`，
无 gap/overlap，错误 0。独立 C++ 混合 d1 replay（编译宏
`ALLOW_MIXED_D1`）从 primary/replay 已匹配的 24077-signature union 自行重建
全部 38-row，并生成 71578 个 job；增强版 verifier 返回
`VERIFIED_EXACT_PER_JOB_MATCH`，15 项检查全为 true、`mismatch_count=0`。
Python 与 C++ 的总计完全一致：`root_sets=752797`、`root_colorings=12440449`、
`root_edge_legal=11757721`、`capacity_rejects=80610`、
`weight_assignments=1493494020`、`parent_legal=16155018`、
`spectrum_survivors=0`。因此固定 `δ=279,s=152,shape=chain` 的全部偶数
`2<=d1<=124` 现在均可标为 `CERTIFIED FINITE IMPOSSIBLE`；这仍不扩大到
`shape=star`、其它 `s` 或整个 S1-279。完整哈希和命令见
`docs/checkpoint-2026-09-01-s152-chain-remainder-forest.md`。

## 主问题

## 2026-09-01 s=152 star independent check (certified)

Workstation 上已有 `exact10_shards_s152_star/` 的 63 个 primary 分片，覆盖
`d1=2,4,...,126`，均为 `EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，每片
`survivor_count=0`；这些 primary 结果尚未单独升格。为取得第二实现证据，
已启动 `star_independent_py_batch.sh`（控制器 PID `3289025`），在 workstation
以最多四个 `nice -n 15` worker 用 Python 集合/直接距离实现逐 d1 对照。完成前
不得把 star 分支称为 certified；若有 timeout 或 mismatch，只隔离对应 d1。
截至 2026-09-01，原批次控制器已自然结束；此前两个 timeout 分片
`d1=18,20` 均以单进程 `nice -n 15 timeout 3600` 延长重跑并正常结束（`rc=0`）。
两片最终 JSON 均通过逐字段语义核对；严格汇总脚本
`remote_scratch/.../verify_star_independent_batch.py` 在 workstation 上返回
`status=VERIFIED_STAR_INDEPENDENT_EXACT_BATCH`、`errors=[]`，覆盖恰为
`d1=2,4,...,126` 的 63 片，聚合为
`params_total=1953, params_valid=1612, params_with_survivor=0,
survivor_count=0`。因此固定 `δ=279,s=152,shape=star` 的独立批次现可标为
`CERTIFIED FINITE IMPOSSIBLE`；证据仍只覆盖该固定分支，不扩大到其它 `s`、
其它 shape 或整个 S1-279。汇总命令和远程结果路径保留在对应 scratch 目录。
早先的 `rc=124` 失败日志仍保留作历史记录，未被覆盖；只有上述正常结束且逐字段匹配
的最终 JSON 才计入正式批次。

## 2026-09-01 s=154 star primary batch (primary complete; independent check pending)

顾问建议在关闭 `s=152,star` 后优先处理 `s=154,star`。workstation 已启动
`exact10_root_signature` 的 primary 分片批次，覆盖合法偶数
`d1=2,4,...,124`，最多 4 个 `nice -n 15` worker，单片 timeout 900 秒，
临时文件成功后原子改名；本机未启动计算。批次已自然结束，生成完整的 62 个
primary JSON（`d1=2,4,...,124`），无 timeout、无失败、无临时残留，并写出
`exact10_shards_s154_star/SHA256SUMS`。完成前不得称为 certified；后续需逐片
解析、检查 status/coverage，并与独立 Python 实现逐字段核对后才能写入正式结论。

同一 workstation 上已随后启动 `star_independent_py_s154` Python 复核，覆盖相同
62 个 d1，最多 4 个 `nice -n 15` worker，单片 timeout 1200 秒；当前独立批次
尚未完成，故 `s=154,star` 仍为 pending。已观察到 `d1=12,14,16` 各以
`rc=124` 超时，均未生成最终 JSON；这些分片暂记 `GAP/timeout`，待其余批次
自然结束后再按单进程延长时限重跑，不把超时当作零结果。随后 `d1=18` 也以
`rc=124` 超时；当前四个分片均保留各自计时记录，未生成正式 JSON。
继续运行中 `d1=20`、`d1=22` 也各以 `rc=124` 超时；截至当前观察，
`d1=12,14,16,18,20,22` 均暂记 `GAP/timeout`，尚未进行延长重跑。
随后 `d1=24` 也以 `rc=124` 超时；当前已知超时集合扩展为
`d1=12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46`，仍待批次结束后逐片延长重跑。
截至当前实时检查，独立批次已有正式 JSON：
`d1=2,4,6,8,10,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112`（38/62）；当前活动 worker 为
`d1=114,116,118,120`。这些中间结果只作进度记录，尚未构成 s=154,star 的认证；
必须等全域完成并逐片语义核对，且对超时分片完成延长重跑后，才能聚合验收。

独立批次控制器随后以 `rc=123` 结束：无孤儿 worker，已生成 44/62 正式 JSON，缺失
恰为 `d1=12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46`。对这些
primary JSON 的只读 hash/解析预检全部通过。随后按单进程
`nice -n 15 timeout 3600` 延长重跑 `d1=12`，workstation 返回 `rc=0` 并生成非空
正式 JSON；其状态为 `INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`。除独立文件自带的 `d1=12` 身份字段外，
`s,B,shape,params_total,params_valid,params_with_survivor,survivor_count,
survivor_xor_fnv1a64,survivor_sum_fnv1a64,color_count_histogram` 均与 primary
逐项一致（`56/50/0/0`）。随后 `d1=14` 的同样延长重跑也返回 `rc=0`，
状态与 `expected_json_verified` 正确，全部上述语义字段与 primary 一致
（`55/48/0/0`）。随后 `d1=16` 的延长重跑也返回 `rc=0`，状态与
`expected_json_verified` 正确，全部上述语义字段与 primary 一致
（`54/46/0/0`）。随后 `d1=18` 的延长重跑也返回 `rc=0`，状态与
`expected_json_verified` 正确，全部上述语义字段与 primary 一致
（`53/44/0/0`）。随后 `d1=20` 的延长重跑返回 `rc=0`，生成非空最终 JSON，
状态与 `expected_json_verified` 正确，全部上述语义字段与 primary 一致
（`52/42/0/0`；耗时约 `2217.53 s`）。因此当前已完成 49/62，剩余缺失为
`d1=22,24,26,28,30,32,34,36,38,40,42,44,46`；原有 `rc=124`
日志仍保留，尚未计入正式覆盖。随后 `d1=22` 的延长重跑返回 `rc=0`，
生成非空最终 JSON，状态为 `INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并与 primary 逐字段一致（`51/40/0/0`）。
因此当前已完成 50/62，剩余缺失为
`d1=24,26,28,30,32,34,36,38,40,42,44,46`；`d1=22` 的临时文件已清理，
计时记录已保留。随后已在 workstation 上以单进程 `nice -n 15 timeout 3600`
启动缺失分片 `d1=24`；启动前确认 primary 基准存在且无同名 final/tmp，
当前尚未产生 final JSON，故覆盖数仍为 50/62。随后 `d1=24` 的延长重跑返回
`rc=0`，生成非空最终 JSON，状态为 `INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并与 primary 逐字段一致（`50/39/0/0`；耗时约
`1987.88 s`）。因此当前已完成 51/62，剩余缺失为
`d1=26,28,30,32,34,36,38,40,42,44,46`；`d1=24` 的临时文件已清理，计时记录已保留。
随后已在 workstation 上以单进程 `nice -n 15 timeout 3600` 启动缺失分片
`d1=26`，启动前确认 primary 基准存在且无同名 final/tmp；原 SSH 句柄仍存活。
之后的新建 SSH 状态查询触发 Tailscale 的 additional-check 页面，因此暂不以
该查询判定作业失败，继续依赖原句柄的终态输出；覆盖数仍为 51/62。

随后原 workstation 句柄返回 `RERUN_OK d1=26`。只读核验确认
`star_independent_py_s154/d1_26.json` 非空可解析，字段为
`s=154,B=126,shape=star,d1=26`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=49, params_valid=38,
params_with_survivor=0, survivor_count=0`。与 primary 的
`s,B,shape,params_total,params_valid,params_with_survivor,survivor_count,
survivor_xor_fnv1a64,survivor_sum_fnv1a64,color_count_histogram` 逐字段比较返回
`MATCH`。因此正式独立覆盖更新为 52/62；剩余缺失为
`d1=28,30,32,34,36,38,40,42,44,46`。原有失败日志与计时记录保留不变。

随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=28`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=28`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=48, params_valid=37,
params_with_survivor=0, survivor_count=0`。由于 primary 使用 `d1_shard`
而独立结果使用 `d1`，按对应语义键对齐后，所有计数、哈希和直方图字段逐项比较返回
`MATCH`。因此正式独立覆盖更新为 53/62；剩余缺失为
`d1=30,32,34,36,38,40,42,44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=30`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=30`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=47, params_valid=35,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 54/62；剩余缺失为
`d1=32,34,36,38,40,42,44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=32`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=32`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=46, params_valid=34,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 55/62；剩余缺失为
`d1=34,36,38,40,42,44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=34`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=34`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=45, params_valid=33,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 56/62；剩余缺失为
`d1=36,38,40,42,44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=36`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=36`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=44, params_valid=32,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 57/62；剩余缺失为
`d1=38,40,42,44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=38`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=38`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=43, params_valid=31,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 58/62；剩余缺失为
`d1=40,42,44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=40`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=40`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=42, params_valid=30,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 59/62；剩余缺失为
`d1=42,44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=42`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=42`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=41, params_valid=29,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 60/62；剩余缺失为
`d1=44,46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=44`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=44`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=40, params_valid=28,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 61/62；剩余缺失为
`d1=46`。原有失败日志与计时记录保留不变。
随后在 workstation 上以单进程 `nice -n 15 timeout 3600` 延长重跑
`d1=46`，返回 `RERUN_OK`。只读核验确认独立 JSON 非空可解析，字段为
`s=154,B=126,shape=star,d1=46`，状态为
`INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED`，
`expected_json_verified=true`，并且 `params_total=39, params_valid=27,
params_with_survivor=0, survivor_count=0`。按 primary 的 `d1_shard` 与独立
结果的 `d1` 对齐后，所有计数、哈希和直方图字段逐项比较返回 `MATCH`。
因此正式独立覆盖更新为 62/62；剩余缺失为无。原有失败日志与计时记录保留不变。

随后对 `s=154,star` 做了严格整批只读汇总。原有
`verify_star_independent_batch.py` 仍硬编码旧的 `s=152` 域（错误期待
`d1=126`、`1953/1612`），该脚本输出的 `GAP` 不作为结论。改用等价的
只读 scope-correct verifier，精确检查 `d1=2,4,...,124` 共 62 片，逐片要求
primary/independent 状态正确、`expected_json_verified=true`、所有语义字段
一致，并汇总得到 `params_total=1891, params_valid=1556,
params_with_survivor=0, survivor_count=0`，`errors=[]`，状态
`VERIFIED_S154_STAR_INDEPENDENT_EXACT_BATCH`。因此固定
`δ=279,s=154,shape=star` 可标为 **CERTIFIED FINITE IMPOSSIBLE**；该结论
仍只覆盖这一固定分支，不扩大到 `s=154,chain` 或整个 S1-279。

## 2026-09-01 s=154 chain exact/replay/prefilter checkpoint

在 workstation 上以最多 4 个 `nice -n 15` worker 完成了 `s=154,shape=chain`
的 primary exact-10 分片：`d1=2,4,...,124` 共 62 片，逐片只读 scope/status
核验通过（`s=154,B=126,shape=chain`、无临时残留），汇总为
`params_total=1891, params_valid=1860, params_with_survivor=1318,
survivor_count=5201986`。这只是 exact-10 必要子系统的幸存见证，不能直接当作
完整树存在性结论。

独立 C++ replay 已参数化为 `S=154,B=126`，并逐 `d1` 完成 62/62 片；每片
状态为 `INDEPENDENT_EXACT10_FULL21_D1_REPLAY`，scope 与输出均通过只读检查。
去重后的 canonical union 共 `555397` 个签名，
SHA-256 为
`81211a50c710cb3324fea47197fd0524295678dbfe08403e26d41007841567ce`。

FW303 预筛已使用带 `_s154` 后缀的参数化版本（`c=10..14/11..14/12..14`），
输入 union 的合法 JSON 修复副本为 `exact10_s154_chain_union_v2.json`。预筛
只读结果：`signatures_checked=555397`，理论 38-row 评估数
`21105086`，compatible rows `392049`，分类为 A=`391129`、B=`773`、C=`147`；
所有 `392049` 个 compatible row 都包含 `c=14`，且 row key 唯一。c14 解析
组合计数也逐类符合：A `(root_sets,root_colorings,e)=(15,1215,2)`；
B 的 `m=0/1` 分别为 `(35,2835,3)/(20,540,3)`；C 的 `m=1/2` 分别为
`(35,945,4)/(15,135,4)`。因此状态为
`PREFILTER_S154_CHAIN_SANITY_OK`。

当前仍未完成 `s=154,chain` 的 full forest。下一步按顾问建议，依据每个
signature 的 `Σ root_colorings` workload proxy 做连续范围分片，最多 4 个
远程 worker；独立 C++ replay 将从自身 38-row/c14 量词重建 job key，最后按
`(canonical_signature,gate,q,class,c)` 逐 key 对齐 Python 结果。只有双实现
完整覆盖且 `spectrum_survivors=0`，才能把该固定分支标为有限认证。

预筛后的规模审计为 `1,959,178` 个 `(row,c)` jobs、root-coloring proxy
`748,800,068`，按 W-injection 上界加权约 `64,426,821,210` 次 parent 尝试；
因此未直接启动巨型单作业，而是等待按 workload proxy 的连续范围分片方案。

随后完成了首个 50-signature 的双实现 pilot（canonical index `0..49`）：
Python forest 与独立 C++ replay 均处理 `110` 个 `(row,c)` jobs，其中 `22`
个为 `c=14`；两边 survivor 均为 0。按
`(signature_index,gate,q,class,c)` 逐 key 比较七项计数，返回
`PILOT_FOREST_CROSSCHECK_OK`、`mismatch_count=0`。据此确认实现接口和
`c=14` 量词在小片上对齐，但不能外推全域非存在性。

依据每个 signature 的 workload proxy 已生成 workstation 分片计划
`forest_shard_plan_s154_chain.json`：共 1286 个连续范围，目标每片约
`50,000,000` 加权 parent-attempt proxy（上限约 51.1M），计划最大 4 个
远程 `nice -n 15` worker。当前首片 `0..548` 正在 workstation 上由 Python
实现执行；完成后须对同一 canonical 子集运行独立 C++ replay 并逐 key 复核，
再决定是否扩展到下一片。

### 2026-09-01 s=154 chain interface audit (read-only)

在 workstation 远程副本中只读检查了后续 `chain` 路线的两个实现：
`exact10_full_low_root_signature.cpp` 的构造函数使用 `B=280-s`，并通过
命令行解析 `--shape chain`，因此 primary 接口本身可覆盖 `s=154`；但
`replay_exact10_full21_d1_18.cpp` 明确硬编码 `S=152, B=128`，输出也固定
为 `chain`。因此该 replay 不能直接作为 `s=154,chain` 的独立证据；在
`s=154,star` 完成后，必须先参数化/重审计独立 replay，并重新覆盖允许的
`c` 范围（包含顾问指出的 `c=14`）。本审计未启动计算、未改变远程文件。
同一只读检查还发现 `replay_fw303_all_class_forests.cpp` 在循环中固定
`c <= 13`，`replay_fw303_remaining_classa_forests.cpp` 也固定
`c=10..13`；这两个 forest replay 同样不能覆盖 `s=154,chain` 的完整
`c` 量词，必须先参数化并独立复核。
本轮尝试向普通 Chat 顾问发送一个只读的 `c=14` 审查问题时，内部通道两次
返回 `no rollout found`；记为顾问传输故障（不影响已取得的顾问建议），未
因此启动替代对话或改变计算路线。

随后保留旧 s=152 文件不变，新增并编译通过
`prefilter_fw303_gate_compatibility_s154.py`、
`search_fw303_all_class_forests_s154.py`、
`replay_fw303_all_class_forests_s154.cpp` 和
`replay_exact10_full21_s154.cpp`；这些版本分别显式使用 `s=154,B=126`、
`d2<126`、`c<=14`，作为后续独立 forest 的代码基线。

## 主问题

当前路线研究 FW319 exact-return-33 的 `b=27` 残余分支，目标是把有限
计算压力测试提升为可审计的普遍非存在性证明。当前不把任何有限枚举的
零结果写成全局定理。

## 已核对的结论

- 核心残余链的 replay 返回 `VERIFIED_FRONTIER`。它固定了
  `w>=38`、`r>=16`、`t>=54`，并把残余压缩为 L-internal 或 J-internal
  的单边 `32` owner。
- 完整 order-3 attachment/LCA 有限模型（Hoffman2 `99604`）共 `41,088`
  行，全部 `INFEASIBLE`，无 `UNKNOWN` 或 `FEASIBLE`；独立图/BFS 回放
  通过。结果文件 SHA-256：
  `12f9941bf7747e15867ba405dff9486705221d1dfa8aee35fe6df7ff68dfbbbc`。
- Pro 建议的 J32 outward 三态扩展（`NONE/PATH2/FORK2`）初始模型
  （Hoffman2 `99744`）共 `92,448` 行：`82,831 INFEASIBLE`、`9,617
  UNKNOWN`，无 `FEASIBLE`；独立图/BFS 回放通过。
  结果文件 SHA-256：
  `c8ff7915eb5f6e4a9fc46fa0706fa2bdfe7c5c124ee8667203e1642b660f05df`。
- 原 Hoffman2 `100025` 曾被队列占位但实际无进程，未产生结果；因此没有
  把它当作复核证据。对应的 `9,617` 行已改在 geoworkstation 上用两轮
  确定性分片完成，详见下文。
- 2026-08-28 后续只读核对发现 `100025` 虽仍被 SLURM 标为 `RUNNING`，但
  `scontrol listpids` 没有列出 batch/ Python 进程，`TotalCPU=00:00:00`，
  `slurm-100025.out` 和目标 `.log` 均保持 0 字节；节点 `n1181` 本身为
  `MIXED` 且健康。这是“队列占位但实际进程缺失”的疑似幽灵作业，不能把
  它当作正在取得进展；在获得明确授权前不执行 `scancel`、重排或分片重跑。
- 已只读探测备用 geoworkstation：SSH 别名 `geo-ws` 当前要求先完成
  Tailscale 设备认证，`geo-ws-vpn` 到 `128.97.31.210:22` 超时；因此目前
  还不能把新计算提交到该工作站。认证/网络恢复后，优先把 `100025` 的
  分片复核迁移到那里，并保留同一输入哈希与严格合并审计。
- Tailscale 认证现已完成。工作站独立目录
  `/home/geo/codex-work/leech-trees-j32-rerun-20260828` 已同步三份模型/分片
  脚本及 `99744` 输入（SHA-256
  `c8ff7915eb5f6e4a9fc46fa0706fa2bdfe7c5c124ee8667203e1642b660f05df`）。
  用户级环境使用 Python 3.8、OR-Tools 9.10.4067、NetworkX 3.1；10 行
  smoke shard 已正常运行。随后已启动 64 个确定性分片（每片 5 秒上限），
  当前以工作站批处理 PID `2227495` 运行；结果必须精确覆盖原始 9,617 个
  UNKNOWN 行并通过严格合并器和完整 verifier，才能改变证明状态。
- geoworkstation 第一轮 64 片已完成并由严格合并器合并为远端
  `theory-lab/topwindow/results/pass1.json`：精确覆盖 `9,617/9,617` 行，
  其中 `4,761 INFEASIBLE`、`4,856 UNKNOWN`，无报错。第二轮已以同样的
  64 片确定性划分、每行 30 秒上限、批处理 PID `2232296` 启动，当前仍在
  实际计算；完成后必须再严格合并并运行完整 verifier。
- geoworkstation 第二轮随后完成剩余 `64/64` 片，覆盖全部 `4,856` 行，
  全部为 `INFEASIBLE`，无错误。链式收口 artifact
  `theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_rerun_final.json`
  的 SHA-256 为
  `0f1a3ebd40e18e755f5d5287aa68cf3d31feba335d5cebb5ef4403415703f238`。
  目标复核器返回 `VERIFIED_J32_OUTWARD_DEEPER_TARGETED_RERUN`，完整
  artifact 审计返回 `VERIFIED_J32_OUTWARD_DEEPER_ARTIFACT`，并通过独立
  BFS replay；最终 `92,448/92,448 INFEASIBLE`、零 `UNKNOWN/FEASIBLE`。
  这只闭合所声明的有限 J32 outward order-3 模型，不能替代全局
  Label-State Completeness 或任意高子树/低森林的证明。
- 为防止单作业的八小时上限截断这次复核，已提交一套不改变当前作业的
  分片恢复工具：`theory-lab/topwindow/rerun_pro_b27_j32_outward_deeper_unknown_shard.py`
  （commit `fce66bb`）和严格合并器
  `theory-lab/topwindow/merge_pro_b27_j32_outward_deeper_unknown_shards.py`
  （commit `a442c0a`）。它按原始 UNKNOWN 行索引做确定性分片，并要求
  合并时精确覆盖全部原始 UNKNOWN 行；合并后仍必须通过原有完整验证器
  才能改变状态。该工具目前只是备用，尚未运行。
- 另一个 Pro 指导的低支撑控制（Hoffman2 `100060`）测试 `377,982`
  个有界候选，幸存者为零；独立结果审计返回
  `VERIFIED_J32_ISOLATED_CONTROL_ARTIFACT`。结果文件 SHA-256：
  `14fc9ec1c4ba3c787559d098f39780a8d5065893d6738a124eead61c65e040cc`。
- 旧的纯高链/共享 Steiner 结果已重新逐项审计：`98777` 两 Steiner 的全域
  CP-SAT、`98778` 三 Steiner 的全域 CP-SAT、`98722` 单共享 Steiner 扫描、
  `98774` 修正版共享多端口扫描均通过各自 verifier，声明的受限行全部
  `INFEASIBLE` 或零幸存者。它们都明确只覆盖指定的少量组件、网关和高权值池，
  不覆盖任意 high skeleton、较大 low forest、强制 L owners 或完整 spectrum，
  因而仅作为压力证据，不能推进全局量词。
- 端口 profile 扫描的独立 artifact 审计也已重跑：`98653`（严格三边）与
  `98658/98661`（四边、分别无 cap/带 order-25 cap）均通过 provenance/witness
  检查；其中严格三边的独立实现与主扫描逐项一致（`533` profiles、`585,234`
  个 H 候选、`127,629` 个必要条件 survivor）。这些 survivor 明确说明当前
  translate/profile 过滤仍非完备排除器，不能代替 H37 forest + port closure。
- 五重 fixed-L translate 的上尾探针精确验证了 `t=67..85` 仍有
  `h>=t+19`，但在 `t=86` 首次出现兼容浅端点
  `(w,r,h)=(54,32,38)`；独立算术回放一致。状态为
  `OBSERVED_TRANSLATE_PROBE`，因此不能把低行的 endpoint floor 延伸到
  整个 `t>=67` 上尾。
- 同一五重 translate 谓词已作一次完整的有限上尾扩展：在
  `86<=t<=300`、`38<=h<=268` 中检查 `26,015` 个三重行和
  `2,701,986` 个五重兼容三元组，其中 `1,937,923` 个违反
  `h>=t+19`，涉及 `208` 个 `t` 值；首个见证仍为
  `(t,w,r,h)=(86,54,32,38)`，末个违反值为 `t=300`。可复跑脚本为
  `theory-lab/topwindow/verify_pro_b27_j32_upper_tail_translate_extended_probe.py`，
  状态为 `OBSERVED_TRANSLATE_PROBE_EXTENDED`。这只否定 translate-only
  上尾路线，不使用完整 J 树或 attachment/LCA 完备性。
  在 `geo-workstation` 上用独立 stdin-only 实现重算，四个聚合计数完全
  一致；该复核不读写 checkout，仅作为跨机器算术一致性证据。
- 该上尾 probe 又在 geoworkstation 专用 `.venv` 中直接远程复跑，返回
  `2,701,986` 个五重兼容三元组、`1,937,923` 个 floor 违反、`208` 个
  违规 `t` 值及同一首个见证 `(86,54,32,38)`；artifact
  `results/pro_b27_j32_upper_tail_translate_extended_probe_geo.json` 的
  SHA-256 为 `24fd7648376f1e4a91e613a77ebe54cbcf6d51107cbe00795e7585d888cd267d`。
  这是同一有限算术 probe 的跨机器复现，不改变其 `OBSERVED` trust boundary。
- 既有的 exact forced `L(5,21)/J(32)` label-state 模型已通过 rooted
  skeleton order 7 与 order 8 的完整有限审计：order 7 为 `129,360/129,360`
  INFEASIBLE，order 8 为 `412,160/412,160` INFEASIBLE；两者均通过独立
  BFS replay，结果分别记录于
  `results/pro_b27_l521_j32_label_state_order7_merged.json`（SHA-256
  `100e6db398ceda441f872968b277e66f685983946fbaf05221e636839474524a`）和
  `results/pro_b27_l521_j32_label_state_order8_merged.json`（SHA-256
  `d490f3b40a75b34d59fd43458cfd0907031233a45f74df9adf0f8764797a632f`）。
  这只闭合固定 `L(5,21)/J(32)` 状态模型的两个有限阶数，仍不覆盖任意
  high 子树、任意 low forest 或 Label-State Completeness。
- order-4 attachment/LCA 扩展已在 geoworkstation 的独立目录
  `/home/geo/codex-work/leech-trees-j32-rerun-20260828` 完成 64 个确定性
  分片并严格合并。初始 artifact
  `results/pro_b27_attachment_lca_falsification_order4_geo_initial.json`
  的 SHA-256 为
  `c78cd41f019aa5e2977a41a3a20b14abde1f689e8f4073f18cbd4b38b01c4a70`，共
  `196,736` 行；独立图/BFS verifier 返回
  `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT`，状态为
  `158,421 INFEASIBLE`、`38,315 UNKNOWN`、无 `FEASIBLE`。
- 对上述 `38,315` 个 UNKNOWN 的第一轮确定性复核（64 分片、每行 1 秒）
  精确替换全部目标行，artifact
  `results/pro_b27_attachment_lca_falsification_order4_geo_rerun_1s.json`
  的 SHA-256 为
  `af52aaab15f29c52ad50f9e4c4086774fe3fc3928521ab14451b006319ca9be5`。
  严格合并器验证输入哈希与语义字段不变；结果为
  `161,864 INFEASIBLE`、`34,872 UNKNOWN`、无 `FEASIBLE`，所以仍未闭合。
- 第二轮针对这 `34,872` 个剩余 UNKNOWN 的 5 秒、96 分片复核已完成，
  精确替换全部目标行并通过严格合并器。最终 artifact
  `results/pro_b27_attachment_lca_falsification_order4_geo_rerun_5s.json`
  的 SHA-256 为
  `a7c8fb1d7cf6c5f6127b89ac435b08de193c1978616d4746984ed49cf9797492`；
  本地与 geoworkstation 独立 verifier 均返回
  `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` 和
  `VERIFIED_INDEPENDENT_BFS_REPLAY`。最终状态为
  `164,688 INFEASIBLE`、`32,048 UNKNOWN`、无 `FEASIBLE`。因此 order-4
  有限扩展在这一预算下仍是混合有限控制，不能把 UNKNOWN 当作零；随后
  已针对该精确 UNKNOWN 集合继续加时。
- 第三轮针对 `32,048` 个 UNKNOWN 的 30 秒/行、96 分片复核已完成并严格
  合并，最终 artifact
  `results/pro_b27_attachment_lca_falsification_order4_geo_rerun_30s.json`
  的 SHA-256 为
  `08addbaf987ac18217e3a3fb65a93096b6dea7a8331deb560932e32328f85239`。
  合并器精确替换全部目标行；远端与本地 verifier 均返回
  `VERIFIED_ATTACHMENT_LCA_FALSIFICATION_ARTIFACT` 和
  `VERIFIED_INDEPENDENT_BFS_REPLAY`，最终 `196,736/196,736` 行均为
  `INFEASIBLE`，零 `UNKNOWN`、零 `FEASIBLE`。这闭合了声明的 rooted
  skeleton order-4 attachment/LCA 有限模型，但仍不等于全局
  Label-State Completeness。
- 针对最终 `32,048` 个 UNKNOWN 的第三轮 30 秒/行加时已在
  geoworkstation 完成，使用输入
  `results/pro_b27_attachment_lca_falsification_order4_geo_rerun_5s.json`、
  96 个确定性分片，输出目录为
  `results/attachment_lca_order4_unknown_30s_20260828`。严格合并精确覆盖
  目标集合，远端与本地独立 verifier 均通过；最终
  `196,736/196,736` 行为 `INFEASIBLE`，零 `UNKNOWN/FEASIBLE`。
- `theory-lab/topwindow/verify_pro_b27_high_branch_skeleton_partition.py
  --max-order 10` 已在本地复跑并返回 `VERIFIED_HIGH_BRANCH_SKELETON_PARTITION`：
  覆盖 `1,809` 个树实例、`22,515` 个 marked instances、`143,654` 条
  ordered arcs，最大 arc 数为 `9`。这只是有序高弧分解的图论证据，尚未
  闭合 Label-State Completeness 或标签可行性。
- 同一有序高弧分解 verifier 又在 geoworkstation 专用 `.venv` 上远程复跑，
  返回完全相同的 `1,809/22,515/143,654` 计数、最大 arc 数 `9`；artifact
  `results/pro_b27_high_branch_skeleton_partition_order10_geo.json` 的 SHA-256
  为 `f1e9b168fbfa518d4b8edf2f1b6f200ab27723b5389bd238cc5541856a76784a`。
  这是跨机器可复现性证据（并非另一套实现），不提升全局覆盖结论。
- `theory-lab/topwindow/verify_pro_b27_ordered_outward_encoding.py
  --max-order 10` 已完成独立加权重建复核并返回
  `VERIFIED_ORDERED_OUTWARD_ENCODING`：覆盖 `1,809` 个根树实例、`22,515`
  个 degree-2 标记实例和 `143,654` 条有序弧，重建后的完整加权 pair-distance
  multiset 与原树一致。该结果只验证有序弧表示的图论无损性，不证明标签可行性
  或全局 `Label-State Completeness`。
  随后在 `geo-workstation` 上用独立 stdin-only 实现复算，返回相同状态及
  `1,809/22,515/143,654` 三个聚合计数，未读写远端 checkout。
- 顾问建议的第一层 incidence catalogue 已在本地复跑：
  `verify_pro_b27_marked_skeleton_catalogue_3port.py --max-order 10` 返回
  `VERIFIED_MARKED_SKELETON_CATALOGUE_3PORT`，规范化三端口（`L5,L21,J32`）
  状态总数为 `601,832`（order-10 为 `427,837`）。独立的
  `verify_pro_b27_port_incidence_exhaustive.py` 另复核了 `18,248` 个标记树拓扑
  和 `61,463` 个非平凡低组件端口检查，返回
  `VERIFIED_PORT_INCIDENCE_EXHAUSTIVE_REPLAY`。这两项只冻结有限拓扑/端口层，
  不包含有序边权、完整 spectrum 或 `Label-State Completeness`。
- 端口状态的距离接口也完成了更深一层独立重放：
  `verify_pro_b27_port_depth_decomposition.py --max-order 6` 返回
  `VERIFIED_PORT_DEPTH_DECOMPOSITION`，覆盖 `1,441` 个带标号拓扑、`259,384`
  个 low/high 分区、`642,886` 个非根组件和 `3,784,162` 个跨组件距离检查；
  `verify_pro_b27_port_state_combiner.py` 与 `verify_pro_b27_port_state_extractor.py`
  也通过。它们确认了端口 profile 的重建接口和 child-side exit 语义，但仍未
  证明 FW319 候选端口集合完备，也未闭合完整 spectrum。
- `verify_pro_b27_low_component_port_skeleton_roundtrip.py --max-order 6` 也已复跑
  返回 `VERIFIED_LOW_COMPONENT_PORT_SKELETON_ROUNDTRIP`：`65` 个根实例、
  `1,473` 个 low/high 分区和 `4,943` 个低组件均能用保留端点 incidence 的状态
  无损重建。该重放仍是有限的无权拓扑审计，不扩大全局量词。
- 同一 round-trip verifier 又在 geoworkstation 专用 `.venv` 上远程运行至
  `max-order 10`，返回 `VERIFIED_LOW_COMPONENT_PORT_SKELETON_ROUNDTRIP`：
  `201` 个 free topologies、`1,809` 个根实例、`680,961/680,961` 个
  low/high 分区和 `3,657,039` 个组件；最大边界 incidence 为 `9`。artifact
  `results/pro_b27_low_component_port_skeleton_roundtrip_order10_geo.json` 的
  SHA-256 为 `485640a1b630e95c05187c04fd85b66a46f22d9981824b939f23a8310cfc4d57`。
  这加强了 incidence 保留/无损 round-trip 的有限证据，仍不等于带权值、owner
  或完整 Label-State Completeness 证明。
- 已把顾问提出的桥梁整理成条件命题 `docs/pro-b27-bounded-ordered-outward-state.md`：
  在固定的 15 个已知顶点和 exact-return 假设下，任意残余 outward 高子森林只
  需要至多 10 个新增顶点，并以保留 incidence 的有序高弧 tuple 无损重建；由于
  high edge `>=38` 且总距离 `<=300`，单条高弧至多 7 条边。文档明确标注这不是
  `NONE/PATH2/FORK2` 的量词提升，也不是 Label-State Completeness 证明。
- 2026-08-29 经用户确认后，右侧 GPT 顾问对上述桥梁给出了一次完整的
  `Finite incidence-owner state lemma` 表述。它明确保留 low-support component
  的唯一 rootward port、pure-high quotient、每条有序高弧的全部内部顶点与边权，
  以及 `5,21,32,34,35,36,37` 的实际 owner endpoint/path；按 edge-for-edge
  重建可保留全部 pair distances 和 owner identities。独立对照现有文档后，未
  发现新的已证明内容；顾问同样指出第一处未支持蕴含仍是“每个真实状态都落入
  当前已枚举 catalogue”，尤其是剩余 low component/owner incidence 的完备分类。
  此条记录是 `ADVISOR_PROPOSAL_AUDITED`，不是全局定理。
- 将该表示命题及其证明边界整理为
  `docs/pro-b27-canonical-incidence-state-lemma.md`：对任意实际 connected
  fixed subtree `K`，收缩全部 low components、保留 rootward/outward high
  endpoint incidences，并保留有序 high-arc edge-weight tuples，即可
  vertex-for-vertex、edge-for-edge 重建原树；因此 pair distances、LCA 和
  owner identity 不丢失。该 lemma 只闭合“真实树到无损状态”的表示方向，
  不闭合“无损状态落入当前有限 catalogue”的覆盖方向。
- 为直接对应该 lemma 的全部字段，在 geoworkstation 专用 `.venv` 上远程运行
  `verify_pro_b27_port_complete_state_roundtrip.py`：
  `VERIFIED_PORT_COMPLETE_STATE_ROUNDTRIP`，检查 `2` 个 low components、`2`
  个 rootward ports、`3` 个 outward ports、`1` 个有序弧内部顶点，并确认
  `10` 顶点/`9` 边重建后的完整 distance table 保持不变。artifact
  `results/pro_b27_port_complete_state_roundtrip_geo.json` 的 SHA-256 为
  `5853104c4e53e6f0c68f407729eeb92a5fd8ba46325aee83e5c7201dc462ddf3`。
  这是合成接口的远程 replay，不是 catalogue coverage 或全局非存在性证明。
- 为把端口与 low/high 分区放进同一状态层，新增并复跑
  `verify_pro_b27_incidence_partition_catalogue.py`。在 order `<=7` 的全枚举中，
  对每个根树、每个 low/high 边分区和 `L5,L21,J32` 三个标记位置生成规范代码，
  返回 `VERIFIED_MARKED_EDGE_PARTITION_CATALOGUE`；累计原始赋值 `1,973,589`，
  规范状态 `663,215`（order-6 分别为 `283,285` 与 `93,053`）。这只是无权拓扑
  原型，仍未包含有序边权、全部 `34--37` owner 或完整 spectrum。
- 同一 order-6 目录已在 `geo-workstation` 用独立 stdin-only 实现复算，返回
  `VERIFIED_MARKED_EDGE_PARTITION_CATALOGUE_CROSS_HOST`，逐阶原始赋值与规范状态
  均与本地一致（累计 `283,285` 与 `93,053`），且未读写远端 checkout。
- 随后将同一实现以 stdin 方式扩展到 order `<=7`，工作站返回逐阶一致的
  `570,162` 个 order-7 规范状态（累计 `663,215`）与 `1,690,304` 个 order-7
  原始赋值；仍未在远端落盘或读写 checkout。
- order-7 目录已固化为 artifact
  `theory-lab/topwindow/results/pro_b27_incidence_partition_catalogue_order7.json`，
  SHA-256 为
  `1274450882819f6ca65eaadb50755d84dd95a22f0d5a1249f9a1bd4c96ec5d6e`；独立
  artifact verifier 返回 `VERIFIED_CATALOGUE_ARTIFACT`。该文件只保存有限无权
  拓扑层计数和信任边界，不保存或声称完整状态完备性。
- 因 `geo-ws` 满载，已在 `hoffman2` 低优先级作业 `101446` 完成同一拓扑目录
  的 order≤8 扩展。order-8 原始赋值为 `12,058,624`，规范状态为 `3,917,542`，
  累计规范状态 `4,580,757`；artifact
  `theory-lab/topwindow/results/pro_b27_incidence_partition_catalogue_order8.json`
  的 SHA-256 为
  `6b6e435eac35b8d82d7e805a0915eff351ab183611d86967c731b318beca9e46`。
  独立结构审计 `verify_pro_b27_incidence_partition_catalogue_order8_result.py`
  返回 `VERIFIED_CATALOGUE_ARTIFACT_STRUCTURAL`，重新核对了非同构树数、根实例
  数、边分区/三标记 raw-row 公式、聚合总数和 hash；它明确没有重新生成全部
  规范字符串，因此仍只是有限无权拓扑证据，不改变全局完备性状态。
- 为检验 order-8 规范计数本身，已在 `hoffman2` 另提交独立 tuple-canonical
  重放作业 `101526`（单 CPU、16 GB、`campus24`，低优先级），脚本为
  `replay_pro_b27_incidence_partition_catalogue_order8_independent.py`。它不导入
  生产枚举器，改用独立的 tuple-valued rooted canonical form。作业已完成，逐阶
  raw 行数与规范状态数均与生产 artifact 一致；独立结果审计返回
  `VERIFIED_INDEPENDENT_CATALOGUE_REGENERATION_MATCH`。重放 artifact
  `theory-lab/topwindow/results/pro_b27_incidence_partition_catalogue_order8_independent.json`
  的 SHA-256 为
  `cd46c1b5204b8c892bf9c2e07beec7a8238904b196583484e5c58bdba0fa3304`。
  这提升了 order-8 无权拓扑计数的独立可信度，但仍不涉及有序边权、完整
  spectrum 或全局 Label-State Completeness。
- 为直接扩展 attachment/LCA 覆盖，已在 `hoffman2` 提交 rooted skeleton
  order≤5 第一轮作业 `101531`（`--time-limit 0.20` 秒/行、单 CPU、6 GB、
  `campus24` 低优先级），包装器为
  `scripts/hoffman2_attachment_lca_order5_slurm.sh`。它预计覆盖 `859,136`
  个有限状态；任何 `UNKNOWN` 都必须按原始行索引再次分片并独立回放。作业
  尚未完成，故不改变 attachment/LCA 或全局证明状态。
- 对上述 order≤5 作业又做了独立的行数审计：使用 `.venv` 单独加载生成器，
  重算 rooted skeleton 数逐阶为 `1,1,2,4,9`，并按 `EDGE/FWD/REV` 三类
  状态循环的组合公式得到精确 `859,136` 行，与作业声明一致。该审计只确认
  输入覆盖计数和确定性循环边界，不确认任何 CP-SAT 状态或非存在性结论。
- 新增 `verify_pro_b27_h37_budget_gap.py` 的抽象反例审计返回
  `OBSERVED_BUDGET_GAP_ABSTRACT_WITNESS`：固定 15 个顶点之外，只用 8 个
  新顶点即可在断开的低森林中覆盖剩余 `{5,18,20,21,24,25,26}`，从而覆盖
  全部 36 个非穿孔低值。它不是连通 Leech 树，反而证明“10 个顶点预算 + H37
  owner 集合”本身不能闭合 `J32`；必须加入 attachment ports、carrier 方向和
  完整 spectrum。
- 下一次真正搜索的变量与验收门已整理到
  `docs/pro-b27-port-complete-h37-contract.md`：必须同时量化完整低森林、每个
  component 的 `(T_C,p(C),sigma(C),H(C))`、保留端点的高商树与有序高弧、全部
  owner 分配，并以统一 all-different 检查 25 阶的 300 个 pair distances；只有
  拓扑/端口覆盖、严格分片合并、零 UNKNOWN/FEASIBLE 和独立重放同时满足，才可
  改写 proof state。当前仍未运行该完整模型。
- 因 `geo-ws` 持续满载，已在低负载 `hoffman2` 以低优先级提交拓扑层扩展
  `sbatch` 作业 `101446`：运行
  `verify_pro_b27_incidence_partition_catalogue.py --max-order 8`，请求单 CPU、
  12 GB、`campus24`，输出目标为
  `results/pro_b27_incidence_partition_catalogue_order8.json`。作业已完成；
  本地生产验证保留 `4,580,757` 个规范状态（逐阶 `1,16,163,1398,10927,
  80548,570162,3917542`），原始行总数为 `14,032,213`（逐阶计数见 artifact）。
  独立 tuple-canonical 重放与生产结果逐阶完全一致，返回
  `VERIFIED_INDEPENDENT_CATALOGUE_REGENERATION`；独立 artifact
  `theory-lab/topwindow/results/pro_b27_incidence_partition_catalogue_order8_independent.json`
  的 SHA-256 为
  `cd46c1b5204b8c892bf9c2e07beec7a8238904b196583484e5c58bdba0fa3304`。
  这只验证了有限无权拓扑 catalogue，仍不覆盖有序边权、完整 spectrum 或全局
  `Label-State Completeness`，因此不改变全局证明状态。
- 新增并通过 `verify_pro_b27_port_complete_state_roundtrip.py` 的独立接口审计，
  返回 `VERIFIED_PORT_COMPLETE_STATE_ROUNDTRIP`：在含两个 low components、两个
  实际 rootward skeleton incidences、三个 outward ports 和一个有序内部顶点的
  合成状态上，重建得到 `10` 个顶点、`9` 条边，完整 pair-distance 表逐字一致。
  这补检了旧组合脚本中未实际使用的 `rootward_port` 语义，但仍只是合成接口
  审计，不能替代任意 low forest 的覆盖或全局 Label-State Completeness。
- `docs/pro-b27-port-complete-h37-contract.md` 现补入一般树论的
  `Rootward-port lemma`：收缩任意 low component 后仍是树，因此相对固定根恰有
  一个 rootward boundary edge，其余边自然为 childward；再标记 high-degree
  非二度点和 low-incidence 点，剩余 maximal high-only paths 的有序弧分解是
  edge-disjoint 且覆盖全部 high edges。这一段消除了端口/有序弧定义上的逻辑
  歧义，但明确不声称 catalogue coverage 已完成。
- 右侧 GPT 顾问随后给出 `Small-owner path word classification`。对未定位的
  `U={16,18,19,20,24,25,26}`，它的条件性结论是：每个 owner path 至少含一条
  新 low edge，至多含两条；若含两条，唯一可能的双边标签必为 `5+mu`；不同
  owner path 的交集只能是空、一个顶点或一段连续路径。顾问列出的七个签名数
  `2,3,4,5,10,12,14` 及乘积 `201,600` 已用独立秒级算术脚本重算；同时核对
  `5+16+18=39>26`。因此该答复记为 `ADVISOR_PROPOSAL_AUDITED`，可作为严格
  必要条件使用，但不是全局引理：固定段 `F_i` 的 attachment/LCA 仍未证明
  完备地落入现有 `EDGE/FWD/REV` catalogue。
- 右侧 GPT 顾问随后对“由上述两条引理推出 EDGE/FWD/REV 穷尽性”作了 adversarial
  审计，结论是否定的：在一个已有 port 顶点 `v` 上附加三条 low edge
  `vx=5, vy=16, vz=19`，得到六个局部 pair distances
  `5,16,19,21,24,35`，且全部互异；其中 `21=5+16`、`24=5+19`，形成同一
  `5`-edge 的三叉共享模式，并不属于当前仅含 `5+16` 及其高侧 outward 状态的
  `EDGE/FWD/REV` catalogue。独立 inline Python 重算了这六个距离及其唯一性，
  因而该审计记为 `ADVISOR_PROPOSAL_AUDITED`。它是最小的局部 branching
  obstruction（固定 `v` 时只需 3 个新增顶点、1 个 low component、1 个
  rootward port），但不是完整 Leech-tree 反例；它只证明必须新增 joint
  low-edge incidence classification。顾问同时给出一个形式上完备的有限生成器
  方案（枚举至多 10 个新增顶点的全部加权树、端口、ordered arcs 和 owner
  assignment），该方案尚未实现或运行，故不改变全局证明状态。
- 顾问针对上述三叉共享端口缺口又给出更精确的处理边界：应把状态写成
  `G=(T,omega,C,Pi,A,Omega)`，其中 `T` 是至多 10 个新增顶点的有权树，`C/Pi`
  保留 low components 与唯一 rootward ports，`A/Omega` 保留完整 high-only
  ordered arcs，`omega` 记录 `H37` 的实际 owner pairs，并统一检查所有 pair
  distances、puncture reuse 与 small-owner word 条件。由于顶点数、树拓扑、边权
  (`1..300`) 和 owner assignment 都有限，这确实给出一个形式上有限的完备容器；
  顾问给出的粗上界
  `sum_{n=15}^{25} n^(n-2) 300^(n-1) binom(n,2)^14`
  只是过度计数，不是实际状态数。该 decoder 只说明真实反例可编码进此容器，
  不说明容器中的状态都属于 `EDGE/FWD/REV`，也不说明容器已被枚举或全部
  `INFEASIBLE`。因此记为 `ADVISOR_PROPOSAL_AUDITED`；当前最早未支持量词仍是
  “每个允许的 fixed-segment attachment/LCA 与 joint low-edge incidence
  state 都已被有限生成并覆盖”。
- 重新运行 `theory-lab/topwindow/verify_pro_b27_port_incidence_exhaustive.py`，得到
  `VERIFIED_PORT_INCIDENCE_EXHAUSTIVE_REPLAY`：对 `18,248` 个带标号树拓扑、
  `61,463` 个非平凡 low-component 检查，均验证每个非根 low component 恰有一条
  rootward boundary edge，其余边均 childward。该结果只是有限重放；一般树论
  引理已有直接证明，但它不提供当前 catalogue 的覆盖性，也不改变全局缺口。
- 右侧 GPT 顾问针对 fixed connector 又给出端点-cell 分类；独立重放
  `theory-lab/topwindow/verify_pro_b27_port_skeleton_compression.py` 返回
  `VERIFIED_CONDITIONAL_DECOMPOSITION_LEMMA`。在额外假设 connector 的全部边确属
  已认证 fixed core `K` 时，正整数边权使 `K_Z` 中的端点/LCA cell 有限；若
  `delta∈S_0`，全局 pair-distance injectivity 更把端点 pair 压到该值的唯一 fixed
  owner，`delta=0` 则强制两条新边共享顶点。顾问同时明确了边界：若 connector
  含未识别的新 low edge，或允许 fixed-edge subdivision，必须把它重新纳入
  `H37` incidence state，不能只作 attachment metadata。该答复因此记为
  `ADVISOR_PROPOSAL_AUDITED`，并未提升全局证明。
- 对顾问指出的 `fixed-low exhaustion` 又作了条件性逻辑审计：若 exact-return
  假设明确给出 `K` 是实际连通未细分子树、`K` 在
  `[1,37]\\(H37\\cup{4})` 中拥有全部唯一 fixed owners、`4` 在全树中缺失，且
  `F` 是全部 `H37` owner paths 的并，则任意 `K\\cup F` 之外的边若为 low，权值
  属于 `S_0` 会与 `K` 的唯一 owner 冲突，等于 `4` 被禁止，属于 `H37` 则其
  owner path 已把该边纳入 `F`；故该边必为 high。于是 `h<=26` 的 5-配对
  connector 若不含新 low edge，确实完全位于 `K`。这验证了该**条件性蕴含**，
  但尚未证明这些 exact-return 前提已对所有待枚举状态以无损方式继承；右侧
  GPT 顾问随后给出同一结论的完整三分类证明（`4`、`H37`、`S_0`），并明确
  了连通/未细分子树、全局 owner path 与 small-owner 排除第三条新边等不可省略
  前提。故该局部缺口记为**条件性已闭合**，不把它当作全局
  `Label-State Completeness`。
- 在同一条件前提下又整理出 endpoint-incidence 的有限化接口：令 `F` 为全部
  `H37` 全局 owner paths 的边并，令 `F_new=F\\setminus K`。每条 `F_new` 边的权值
  属于 `H37`，且由全局边权互异性至多有 14 条；由于 `K` 是连通实际子树，
  `T\\setminus K` 的每个连通分支至多有一条回到 `K` 的边，否则会与 `K` 内路径
  形成环。故每个新低组件可记录一个唯一 rootward gateway 及任意 childward
  gateways；每条 `5+\\mu` owner path 的 connector 已是 `K` 中的唯一 literal
  geodesic。再加上至多 10 个新增顶点和树路径交集连通性，所有新边端点与
  `K` 子路径的联合 incidence 可无损编码为“有限加权低森林 + gateway/ordered
  high-skeleton incidences”。这是条件性 decoder 结构，不是已完成的全枚举。
- 右侧 GPT 顾问随后给出并完成 endpoint-incidence classification：在上述条件下，
  每条新 low edge 相对 `K` 只能是 `KX`（一个端点在 `K`）或 `XX`（两端在 `T-K`），
  每个 `E_*` 连通分支至多一个 `K` 接点；`5+\\mu` paired owner 的两条新边若
  通过 `K` connector，则必是 connector 两端的 `KX` 边，`delta=0` 时共享同一
  `K` 顶点，`delta>0` 时属于不同新低分支。顾问也明确 atomic `H37` 边仍可形成
  remote 或高阶外部树，不能压成 `EDGE/FWD/REV`。最小低几何 decoder 字段可取
  `(V_new,E_*,lambda,iota,omega,Pi)`，所有 connector/LCA/路径交集由重建树再算。
  这组结论已作树性与 owner 唯一性的逐项审计，记为
  `ADVISOR_PROPOSAL_AUDITED`；它是条件性有限容器，不是已实现或已求解的全局生成器。
- 右侧 GPT 顾问又给出 high-incidence completion 的无损状态：在 `R=K\\cup F`、
  `E_H=E(T)\\setminus E(R)` 且（由 conditional fixed-low exhaustion）每条边权
  `w(e)>=38` 的前提下，记录 `H=(Q,r,I,A,w)`。其中 `Q` 为收缩 low/fixed
  components 后的 rooted quotient，`I` 保留每条高边的两个真实端点 incidence，`A`
  是标记 root、分叉点及带 low/fixed incidence 的二度点后的 maximal high-only arcs，
  `w` 保留每条弧的有序原始边权 tuple。由于总阶 `25`、全局距离上界 `N=300` 及正权，
  quotient/端点分配/弧内部顶点数均有限，且单条纯高弧满足 `38m<=300`、故 `m<=7`；
  展开这些字段可逐边逐点重建树，因此这是条件性的 finite lossless container。
  逐项检查确认这里的有限性不等于 catalogue coverage：仍需证明 `forall T`（满足当前
  `b=27` branch hypotheses）`exists(D_L,H)` 落在已枚举 catalogue 中，且覆盖所有 quotient
  topologies、incidences、root orientations、弧分解、内部顶点数和有序高权 tuple。
  `least-remote/minimality`、`34--37` owner geometry、complete-spectrum/全局 injectivity、
  punctured `4` 缺失及 inherited descent 都不会由该表示自动推出。故该答复记为
  `ADVISOR_PROPOSAL_AUDITED`，不提升为全局证明。
- 右侧 GPT 顾问进一步给出关闭 coverage 量词的最小生成器规范：候选状态可写为
  `Sigma=(D_L,Q,I,A,w)`，先枚举允许的 low decoder，再枚举剩余顶点预算内的 rooted
  unlabeled high quotient、全部 low/fixed incidences、合法 ports、弧 subdivision 与
  有序高边权 `38..300`，最后按固定 named vertices、rooted-tree code、component/arc
  顺序做 canonical key 去重。逐项审计确认：展开后可机械检查连通无环、`|V|=25`、正整数
  边权及全局互异、全部 `300` 对距离的分支指定 cap/谱、punctured `4`、fixed-owner reuse、
  `5,16,18,19,20,21,24,25,26,32,34,35,36,37` 的实际 owner 与已定假设一致；若是未穿孔
  的目标且恰有 300 个互异距离落在 `[1,300]`，谱等式才可由计数自动推出，当前 exact-return
  分支仍须检查其指定目标集。生成器不能自行证明 least-remote/minimality、inherited
  descent，亦不能假定 `34--37` owner geometry 已由现有 catalogue 穷尽；这些须纳入状态
  或先有分类/保持性引理。故该方案记为 `ADVISOR_PROPOSAL_AUDITED`：它给出条件性的
  finite exhaustive container/interface，尚未实现、未在远程运行，也未证明对真实树的
  surjectivity，更未产生全局 `INFEASIBLE` 结论。
- 右侧 GPT 顾问随后把该生成器拆成可远程分片的四层接口，并经逐项审计确认其语义
  与现有原型相容：`incidence_partition_catalogue` 只产 rooted topology/low-high
  marks/ports/arcs；`ordered_outward_encoding` 保留每条弧的内部顶点与有序权 tuple；
  `composed_skeleton_state` 组合 `low_state`、owner assignments 与 shape tags；最后
  才由 `attachment_lca_falsification` 对固定 `(topology, incidence, low_state,
  subdivision)` 求 `38..300` 的高边权。建议的稳定分片键为
  `(skeleton_code, incidence_mark_code, low_state_code, arc_subdivision_code)`，并在
  每行保存 `semantic_input_hash`、`row_key`、solver status、pair/owner table hashes；
  SAT 必须附完整 materialized witness。合并器必须验证预期 row key 恰现一次、无跨 shard
  重复、语义哈希一致、结构字段不可变、UNKNOWN 不得冒充 UNSAT，以及从 edge list 独立
  重建 tree/pair/owner/canonical key。审计补充：`root_vertex` 必须包含在 rooted
  `skeleton_code` 或显式分片字段中，不能因同一 free-tree code 而合并不同 root。
  该接口只规定远程-only 的无损分片契约；现有脚本仍只覆盖其原型子族，尚未生成完整
  `low_state` 集合、提交 Geo Workstation 运行或证明 coverage surjectivity，故记为
  `ADVISOR_PROPOSAL_AUDITED`，不提升全局结论。
- 顾问随后把第一阶段的远程协议进一步钉死：稳定主键应为
  `(skeleton_code, incidence_mark_code, low_state_code, owner_assignment_code,
  arc_subdivision_code)`，高边具体权值留在 shard 内求解而不进入主键；每行至少保存
  `semantic_input_hash/state_id/row_key`、上述结构字段、rootward/outward incidences、
  ordered arcs、权值域、solver status，以及 SAT 时的高权 tuple、pair/owner hashes 和
  完整 witness edge list；shard 级另存 generator commit、constraint version、预期行数、
  shard id/count。审计确认合并必须检查哈希与版本一致、row key 恰现一次、无缺/重行、
  重跑不得改变结构字段、UNKNOWN 不得算 UNSAT，并从 witness 独立重建 tree、全 pair
  distances、cap/injectivity、punctured `4`、owner assignment 和 canonical key。
  第一阶段只包装已有且已审计的 order `<=3` attachment/LCA、J32
  `NONE/PATH2/FORK2`、`EDGE/FWD/REV` low-owner 以及 incidence-marked/ordered-arc
  子族；这份边界与现有代码逐项对照后记为 `ADVISOR_PROPOSAL_AUDITED`，仍不构成
  Label-State Completeness 或全局非存在性。
- 新增的 `theory-lab/topwindow/emit_pro_b27_legacy_protocol_manifest.py`（提交
  `788e377`）只作第一阶段协议适配器：它复用既有确定性 `iter_jobs`，不调用 solver，
  为 order `<=3` legacy attachment/LCA rows 生成稳定 `row_key`、`state_id` 和
  `semantic_input_hash`。为遵守本机资源边界，脚本及其两个依赖模块被临时复制到
  Hoffman2 `/tmp`，远程生成一份 `41,088` 行清单；再以两个 shard（各 `20,544` 行）
  重跑，远程合并检查返回 `VERIFIED_REMOTE_PROTOCOL_SHARD_COVERAGE`：row keys 无重复、
  两 shard 计数精确相加、semantic hash 唯一一致。该结果只验证远程协议/分片覆盖 plumbing，
  没有求解权值，也不证明 legacy 子族之外的 coverage 或全局非存在性；临时文件未写入
  远程项目 checkout，故记为 `VERIFIED_REMOTE_PROTOCOL_SHARD_COVERAGE` 的有限工程证据。
- 对上述 v1 适配器作 provenance 审计时发现其缺少协议要求的 shard 级
  `generator_commit/constraint_version`，因此不把 v1 结果作为完整协议证据。修正后的
  适配器提交为 `ab72b5c`，在 Hoffman2 `/tmp` 重新生成双 shard（各 `20,544` 行）；远程
  合并显式检查了两字段一致、`semantic_input_hash` 唯一、row key 无重复且总数为
  `41,088`，返回 `VERIFIED_REMOTE_PROTOCOL_SHARD_COVERAGE`。该 v2 结果才是当前可采信
  的协议 plumbing 证据，仍仅覆盖 legacy order `<=3`、不含权值求解或全局 coverage。
- 按顾问建议新增 `theory-lab/topwindow/emit_pro_b27_atomic1_protocol_manifest.py`
  （提交 `6b85dea`），把一条额外 atomic low edge `mu∈{16,18,19,20,24,25,26}`
  的 attachment slots 显式加入 legacy 状态；它只生成结构清单，不调用 solver。为避免
  本机计算，已在 Hoffman2 `/tmp` 远程运行 order `1` 的双 shard，并远程合并核对：总计
  `74,240` 行（各 `37,120`），`semantic_input_hash` 为
  `522bed8984f329f6175641d19dfcfbffcfc76aa7e8cb13eed06c0d30c0c834a0`，按 shape/order/
  `mu`/attachment class 的分层计数相加精确。该结果只证明 ATOMIC1 的**结构 manifest
  覆盖**；shared-low 行尚可做 legacy edge-list 重放，fixed-core 与 separate 行尚未
  materialize，故不称为 solver exclusion、全量 ATOMIC1 coverage 或全局定理。
- 新增 `verify_pro_b27_atomic1_protocol_manifest.py`（提交 `f7ddcb9`）后，在 Hoffman2
  对上述 ATOMIC1 双 shard 做了独立重放：`21,248` 个 `shared-low` 行逐行展开 legacy
  edge list、加入一个 fresh atomic leaf，并检查树性、μ 未与既有低边重复、row/state
  hash、legacy row 对应关系和分层计数；返回
  `VERIFIED_ATOMIC1_SHARED_LOW_REPLAY_PARTIAL`。另有 `47,104` 个 `fixed` 与 `5,888`
  个 `separate` 行只完成 key/slot 一致性检查，按设计保留为 deferred，不能计作
  fixed-core/separate materialization、权值求解或 ATOMIC1 全覆盖证据。
- 对这两个 deferred 类的接口审计中，右侧 GPT 顾问明确要求 `fixed` 必须绑定已审计的
  literal fixed-L edge list（`d6-c=6,c-z=7,z-b1=1,z-b2=2,z-a=10,d6-P0=27,
  c-P1=22`）并记录其版本/hash 与真实顶点；`separate` 必须显式记录 atomic 两端、
  哪个端点是 rootward port、实际 skeleton attach vertex、唯一 gateway edge/权值，
  以及所有 child-side outward incidences。树性只保证一个 parent/rootward edge，不能
  静默假设无 outward edge。因现有 legacy 模型没有这两类真实载体，当前行继续标为
  `GAP/DEFERRED`；该答复记为 `ADVISOR_PROPOSAL_AUDITED`，不提升全局结论。
- 将 fixed 类按上述 literal carrier 实际物化：`verify_pro_b27_atomic1_protocol_manifest.py`
  新增 `FW319-fixed-L-literal-v1` edge-list/hash、真实 fixed vertex、fresh atomic leaf、
  全部 fixed-core pair-distance 重算与原 fixed pair ownership 保持检查。为避免本机计算，
  在 Hoffman2 对既有 order-1 双 shard（`74,240` 行）远程独立重放，结果保存为
  `theory-lab/topwindow/results/pro_b27_atomic1_fixed_core_replay_order1_101531.json`：
  `47,104/47,104` fixed 行均成功物化；其中 `40,320` 行在该 8-vertex carrier 内碰撞，
  `6,784` 行在该有限 carrier 内未碰撞；另有 `5,888` separate 行仍 deferred。结果记录了
  `fixed_core_hash=01ad286e8de222cf1b9dd15d8a8cbe7fe0214b91b529b858e6fb98b2d6e9a3be` 和
  `fixed_materialization_record_hash=8fcaf90414a263741a9c7adbdbe4cfdac60a4e2023dac6161e514d332336dd8b`。
  该结果是有限 fixed-core 物化/碰撞证据，不是完整全树 solver exclusion，也不覆盖
  outward incidence。
- 同一 ATOMIC1 order-1 双 shard 又在 geoworkstation 的专用 `.venv`（Python 3.8.10、
  NetworkX 3.1、OR-Tools 9.10.4067）上独立生成并重放；返回同一状态、`74,240` 行、
  `40,320/6,784` fixed 碰撞/未碰撞分解、`5,888` separate deferred，且
  `fixed_core_hash` 与 `fixed_materialization_record_hash` 与 Hoffman2 结果逐字相同。
  这提供了跨机器复现证据，但仍不扩大 fixed-core 的有限 trust boundary。
- 2026-08-29 右侧 GPT 顾问针对当前首要缺口提出了参数化 coverage 目标。对任意真实
  `b=27`、order-25 候选树 `T`，把完整 low state 记为 `D_L(T)`（全部 low
  components、真实 weighted trees、唯一 rootward ports、全部 outward incidences、
  `H37` owner/path identities），把 high state 记为 `H(T)`（收缩后的 rooted quotient、
  所有实际 endpoint incidences、marked maximal arcs、内部 degree-2 vertices 与
  ordered weights）。由于固定包外最多 10 个顶点、每条 high edge 至少 38 且 pair cap
  为 300，所有 topology、`H37` assignments、incidence assignments、arc subdivision
  数与 high-weight tuples 组成一个严格有限的参数空间 `P25`。顾问给出的待证形式是：
  `forall T exists p in P25`，使 `(D_L(T),H(T))` 与 `Materialize(p)` 同构；现有
  canonical-incidence round-trip 只支持从 supplied state 无损重建 `T`，不支持
  `D_L(T)` 一定落在当前 EDGE/FWD/REV/ATOMIC1 catalogue。因而将下一条最小义务
  命名为 `Low-Catalogue Surjectivity Lemma`：证明每个真实 `D_L(T)` 都由明确的
  `(tau_L, omega_L, Pi)` 生成器恰覆盖。该建议已审计并记为 `ADVISOR_PROPOSAL_AUDITED`，
  不提升全局非存在性结论；下一版远程 shard key 可按
  `(tau_L, omega_L, Pi, tau_H, I, arc_subdivision_code)` 固定结构、在 shard 内求解
  high-weight tuple。
- 依据该接口新增 `theory-lab/topwindow/verify_pro_b27_parameter_space_bounds.py`，只
  审计 `P25` 的显式边界：固定包外最多 `10` 个顶点、pair cap 为 `300`、低边权域为
  `1..37` 去掉 puncture `4` 与固定边权、高边权域为 `38..300`（共 `263` 个值），
  每条纯高有序弧至多 `floor(300/38)=7` 条边，并固定记录
  `tau_L, omega_L, Pi, tau_H, I, arc_subdivision_code` 与 ordered high-weight tuples
  七类结构字段。该证书在 Geo Workstation 与 Hoffman2 独立运行，输出字节级相同，
  SHA-256 为
  `5c2a9300cdc1f0f36b40cdd11dd200fadb7974cc042d592d17d6a52897cbf9ab`，结果文件为
  `theory-lab/topwindow/results/pro_b27_parameter_space_bounds_geo_20260829.json`。
  这只证明参数空间的有限性和边界 bookkeeping；没有枚举 `P25`，没有证明
  `Low-Catalogue Surjectivity`，也没有进行本机计算或提升全局结论。
- 新增 `docs/pro-b27-universal-catalogue-surjectivity.md`，给出一个定义级兜底：对
  `m=0..10` 个匿名顶点，取所有包含固定 15-vertex packet `K` 的树拓扑、所有
  `{1..300}` 中的 injective 边权赋值，再对匿名顶点置换作 named-vertex-preserving
  canonicalization；完整 pair table 恰为 `D={1..300}\{4}` 的条件另记为 `Good` 过滤器。
  直接标号论证给出 `real tree -> U^can_25` 的 surjection，因此这个 universal
  catalogue 在数学上不漏状态；其规模远超当前可行搜索，尚未枚举或求解。顾问复核
  强调 puncture、owner、least-remote、descent 等必须作为独立的 `Phi(T)` 过滤谓词，
  不能偷塞进结构 catalogue。该文档是结构命题/路线基准，不是计算证书，也不提升任何
  `INFEASIBLE` 或全局非存在性结论。
- 2026-08-29 为推进受限 coverage，已在 Geo Workstation 专用 checkout
  `/home/geo/codex-work/leech-trees-j32-rerun-20260828` 启动
  `enumerate_pro_b27_two_component_port_states.py --max-edges 3 --h-max 240`
  （远程 PID `2384186`，单 CPU）。截至本次 checkpoint 仍为 `RUNNING`，输出 JSON
  尚为 0 字节；这是新的一项受限必要条件分片，尚未产生可写入的结果，不能与既有
  `max-edges=2` replay 或全局 catalogue coverage 混同。
- 右侧 GPT 顾问对该分片给出边界审计：若全零，最多只能排除“两个独立 low
  components、每个最多 3 条 low edge、固定 named offsets `(38,54,57)`、无共享
  high Steiner”的有限子族；不能推出 Label-State Completeness、全 `b=27` 排除、
  forced-L owners、任意 outward high tree、完整 punctured spectrum 或
  least-remote/descent。若有 survivor，必须保存两组件完整 weighted edge lists、
  rootward/attachment vertices、gateway 权值与方向、全部 pair distances、named
  translates、pair-table hash 和 canonical state hash。远程验收门槛为预期 shard
  无缺/无重，且所有 `UNKNOWN` 逐一重跑到 `INFEASIBLE` 或 `FEASIBLE`；该审计记为
  `ADVISOR_PROPOSAL_AUDITED`，不提升当前结论。
- Geo 分片的远程预审计（同一脚本的 profile/state 计数阶段）返回：`533` 个 J32
  profiles、`1,124` 个 generic profiles，经过 named-offset 过滤后分别为 `17,091`
  与 `49,943` 个 states，笛卡尔积为 `853,575,813` 个 pair tests。该计数用于解释
  `max-edges=3` 比既有 order-2 replay 大很多；最终 JSON 尚未生成，不能把预审计或
  正在运行的进程当作零 survivor 证据。
- 为该 Geo 分片预先加入独立结果验收器
  `theory-lab/topwindow/verify_pro_b27_two_component_port_states_e3_result.py`
  （commit `42cf6f7`，初版为 `d234d12`）。验收器只读 JSON，检查固定参数、预审计计数与精确
  `853,575,813` 笛卡尔积，并把 survivor 的当前字段不足明确标为不可直接 replay；
  它不运行枚举，也不把受限零结果升级为全局结论。
- 右侧 GPT 顾问进一步把下一条最小义务精化为 `Phi_pair(T)`：对任意真实
  exact-return `b=27` 候选树，显式要求 unordered pair-distance 单射、cap `300`、
  puncture `4` 缺失、已认证 fixed owners，以及 `H37` 每个值的唯一 owner；只加入
  已 theorem 化的 `5/21/32` owner 类型。顾问定位的最早未闭合量词是：是否已有对
  `34--37` owner endpoint/path 的全局 exhaustive 分类。该精化已写入
  `docs/pro-b27-constraint-completeness.md`（commit `bf7b59e`），仍不提升全局结论。
- 对该账本再补入一项已存在的条件性证据：若 `H37` owner 路径完全位于 `J`，则
  `verify_exact_return_33_g7_r2_t4_b27_j_low_path_compositions.py` 的穷尽区间组合
  replay 返回 `VERIFIED`，给出 `32` 只能是 `(32)`，以及 `34--37` 的有限两边形状表。
  这仍不判定 owner 在 `J` 还是 `L`，不定位端点，也不关闭全局量词；对应说明已写入
  `docs/pro-b27-constraint-completeness.md`（commit `1fa0236`）。
- 本轮重新运行两个轻量结构回放：`verify_pro_b27_port_state_extractor.py` 返回
  `VERIFIED_GRAPH_LEMMA`，确认低组件唯一 rootward port 及其条件性跨对公式；
  `verify_pro_b27_port_skeleton_compression.py` 返回
  `VERIFIED_CONDITIONAL_DECOMPOSITION_LEMMA`，确认最多 14 条新 low edges、
  high edge bound `263` 与有序 arc tuple 的无损要求。两者均只在明确的 exact-return
  / fixed-owner 假设下成立，不覆盖完整 catalogue 或全局非存在性。
- 2026-08-29 右侧 GPT 顾问把当前最早缺口精确收敛为
  `J34–37 rooted-realization exhaustion`：对每个已允许的 J-side path word，
  逐一覆盖 root 落在路径顶点、经路径顶点接入、以及经额外 branch/LCA 接入的
  全部真实几何；必须保留 edge list、端点、root/attachment、内部 pair 表、
  fixed-L/named translates 与 canonical hash，并由独立实现重放。该义务已写入
  `docs/pro-b27-port-complete-h37-contract.md`（commit `7f35f7a`）。它只可能关闭
  J-side rooted-realization 量词，不能关闭 L-side、任意 high-incidence coverage、
  `Label-State Completeness` 或全局 `b=27` 非存在性。
- 同日重新运行三个轻量边界审计：
  `verify_pro_b27_h37_budget_gap.py` 返回
  `OBSERVED_BUDGET_GAP_ABSTRACT_WITNESS`，
  `verify_pro_b27_h37_abstract_port_gap.py` 返回
  `OBSERVED_ABSTRACT_COUNTERMODEL`，
  `verify_pro_b27_h37_support_bound.py` 返回 `VERIFIED_LEMMA`。前两者明确是
  断开的低森林而非连通 Leech tree，第三者只证明 H37 支撑大小与 >37 gateway
  隔离；三项均不提升 J32 分支或全局非存在性结论。
- 右侧 GPT 顾问的资源审计为当前 Geo 单体分片设定硬停点：只有在远程 CPU
  持续推进且两小时墙钟内出现至少一次可审计的 processed-pair/row 计数时才继续；
  若届时 JSON 仍为空且无进度快照，则停止该单体作业并按确定性 key 分片，不能把
  超时/中断当作 `INFEASIBLE`。本次检查时 Geo 运行约 45 分钟、JSON 仍为空，
  尚未触发硬停点；Hoffman2 同样保持运行，未作重启或复制。
- 已预备远程分片脚本
  `theory-lab/topwindow/enumerate_pro_b27_two_component_port_states_sharded.py`
  （后续强化 commit `b62c397`）。它复用同一受限模型，以稳定的扁平 pair-index
  区间切分 `(J-state index, generic-state index)` 笛卡尔积，逐片保存总空间、
  `shard_id/count`、ordering/wrapper 版本与哈希、两侧 state-catalogue 哈希、
  `pair_start/end`、`processed_pairs`、状态计数和 survivor 索引；配套的
  `verify_pro_b27_two_component_port_states_shards.py` 独立检查所有区间恰好覆盖
  `0..853575812`、无 gap/overlap 且无 `ERROR/UNKNOWN`。本地只做了语法检查，未运行
  枚举。该脚本只用于 Geo Workstation 的硬停后续，不扩大搜索域，也不能把分片并集
  升级为全局非存在性证明。
- 右侧 GPT 顾问提出的 `J` 中点进入碰撞引理已完成独立形式化与轻量算术回放：若
  两边 owner `A-α-M-β-C` 的根侧 geodesic 首次在中点 `M` 进入，则只要
  `|β-α|` 是固定深度集 `B0={0,6,13,14,15,23,27,28}` 的正差，就可用两条
  不同的 fixed-L/J cross pairs 构造相等距离，违反全局单射。回放脚本
  `verify_pro_b27_j_middle_entry_collision.py` 返回
  `VERIFIED_CONDITIONAL_ARITHMETIC_LEMMA`（commit `1c01603`），排除
  `34=(16,18)`, `36=(16,20)` 和 `37` 的五个两边词的中点进入；仅留下
  `35=(16,19)`/反向词。该引理不覆盖端点进入、edge 内部细分、单边 owner、
  L-side geometry 或 catalogue completeness。
- 顾问随后指出 `35=(16,19)` 的另一条条件性闭合：若能引用 theorem-level
  固定 named pair `{y0,y3}` 满足 `d(y0,y3)=35`，则任何新 35 两边路径的端点
  必须复用该 pair（全局距离单射），若再固定 `d(u,y0)=16,d(u,y3)=19`，中点
  还被迫是 `u`。当前控制脚本确实显式使用这一 named packet，但全局候选树上
  该 literal owner 是否已由正式引理固定仍需核查；因此该扩展记录为
  `ADVISOR_PROPOSAL_AUDITED`，尚未提升为 branch-wide theorem。
- 2026-08-29 右侧 GPT 顾问完成 J 端点首次进入的 theorem-level 审计。若
  `A-α-M-β-C` 的 J-root geodesic 首次在端点进入，且已有 carrier-cut 公式与
  `B0={0,6,13,14,15,23,27,28}`，则 `α` 或 `β` 落在
  `Delta(B0)={1,2,4,5,6,7,8,9,10,12,13,14,15,17,21,22,23,27,28}` 时，
  可用 fixed-L 两个不同 unordered pairs 构造同距碰撞；C 端进入对称。由此
  严格排除 `37=(5,32),(32,5),(16,21),(21,16)` 的全部 endpoint-entry
  方向。`34=(16,18),35=(16,19),36=(16,20),37=(18,19)` 仍是 endpoint-entry
  缺口，因为 `16,18,19,20` 不在该差集。该结果已记录于
  `docs/pro-b27-j-endpoint-entry-translate-lemma.md`，仍只覆盖明确的
  carrier-cut 条件性子情形，不覆盖 L-side、edge-interior、catalogue
  completeness 或全局非存在性。
- 随后顾问进一步审计剩余 endpoint-entry words `34=(16,18)`、`35=(16,19)`、
  `36=(16,20)`、`37=(18,19)`：现有 theorem-level named packet 只固定
  `d(u,y0)=r`、`d(u,y3)=r+3`、`r≥16` 与 `d(d6,u)=w≥38`，没有把 endpoint
  stem 长度 `ρ=d(u,A)` 锚定到任何 named rooted depth。因此四个词的两个方向
  均不能无条件排除；`rho=1,r=40` 的抽象局部模式说明当前假设不蕴含不可能性。
  exact-spectrum 的 owner 唯一性也不能把新端点强行识别为 named pair，除非另有
  branch-wide identity。当前最小 theorem-level obligation 是证明 rooted-depth
  forcing lemma，把 `ρ` 压进由 named packet 强迫的有限集合；该审计记录于
  `docs/pro-b27-j-endpoint-entry-rooted-depth-gap.md`。
- 顾问随后尝试把 `rho` forcing 接到 inherited descent：若 endpoint-entry 的空 stem
  `[u,A]` 删除（或以 `A` 重根）仍保留 complete punctured spectrum、J32 单边
  owner、34--37 owner identities、carrier-cut、least-remote 与 no-outlier cap，
  则最小性会迫使 stem 含 named incidence，进而把 `rho` 压到有限 named-depth
  集。当前没有 theorem 证明该 trimming-preservation 前提，故这只是
  `CONDITIONAL` 接口；缺口与精确所需保持不变量已记录于
  `docs/pro-b27-j-empty-stem-descent-preservation-gap.md`。在此前提闭合前，不能
  用 inherited descent 排除剩余 endpoint-entry words。
- 2026-08-29 右侧 GPT 顾问进一步把上述 trimming 缺口收紧为
  `Low-owner retention lemma`：对每个允许的 endpoint-stem cut，smaller
  exact-return 仍需保留的每个谱值，其唯一 owner 的两个端点必须都在 retained
  side；同时被裁部分的 owner 值必须形成参数递降所需的 removable block。
  `exact-return + least-remote + no-outlier` 本身不蕴含该 owner-separation，
  因为谱值可在 cut 两侧交错。该建议已写入
  `docs/pro-b27-j-empty-stem-descent-preservation-gap.md`，等级仍为
  `GAP/CONDITIONAL`，不能用于排除剩余 endpoint-entry words。
- 2026-08-29 在 Geo 四片 restricted coverage 验收后，右侧 GPT 顾问提出下一项
  `PROPOSED_REMOTE_TASK`：先生成并认证 `P25 Low-Decoder Catalogue`，只枚举固定
  core 外最多十个匿名顶点的全部 `H37` low forests、真实 rootward/outward ports
  与 owner 状态，不先做 high-skeleton CP-SAT。验收必须由独立实现重建 literal
  forest、低距离、puncture、owner uniqueness、canonical key 集和 raw-to-canonical
  accounting；成功只关闭 low-catalogue surjectivity/port-complete low-forest
  coverage，不能关闭 high completion 或全局非存在性。精确规格见
  `docs/pro-b27-p25-low-decoder-catalogue-proposal.md`；尚未启动计算。
- Geo Workstation 的单体受限枚举现已结束：远程命令为
  `enumerate_pro_b27_two_component_port_states.py --max-edges 3 --h-max 240
  --witness-limit 20`，远程产物已保存为
  `theory-lab/topwindow/results/pro_b27_two_component_port_states_e3_geo_20260829.json`
  （SHA-256 `3163ab04ed16233ee228fdad692755b59535ca740d54d98615922c33aa98dbfe`）。
  JSON 报告 `j32_states_after_named_filter=17091`、
  `generic_states_after_named_filter=49943`、`pair_tests=853575813`，且
  `survivors_found=0`；独立轻量检查确认乘积计数一致。该结果等级只能是
  `OBSERVED_RESTRICTED_PORT_ENUMERATION`：产物自身明确声明省略 L 端强制
  `5/21` owners、其它 H37 components、任意 LCA/gateway 与 complete-spectrum
  completion，因此不能升级为 `VERIFIED` 或全局非存在性结论。
- 为获得可复现的区间覆盖，单体结束后在 Geo Workstation 同一 checkout 启动了
  4 个确定性 shard（`shard_count=4`，每片使用同一 `max-edges=3`、`h-max=240`、
  `witness-limit=20`）。启动时远程 wrapper/verifier 哈希分别为
  `728adc4f26f27d5869c5f8aa18a07d3a02d5270a80b520c398b709a981d0f37d` 与
  `c74fc0574bc7a4115ddad721eefe13150cb478183d71cafcb902c52df98c1446`；远程 PID
  为 `2407010..2407013`，输出目录为
  `/home/geo/codex-work/leech-trees-j32-rerun-20260828/theory-lab/topwindow/results/pro_b27_two_component_shards_20260829/`。
  这是对同一受限模型的协议级复现，不扩大模型；须待四片齐全后再用独立合并器验收。
- 在分片运行期间又强化了独立合并器（本地提交 `c476aca`，Geo 副本 SHA-256
  `95e90f343cc50652028e299f561925474e629108c065280721ee34f4ef1d68d2`）：现在除区间
  连续性外，还强制 `semantic_input_hash`、输入 catalogue 规模/版本、
  `expected_pair_tests` 与 survivor/status 计数在所有 shards 中一致，并核对
  `17091×49943=853575813`。四片现已全部完成；独立合并器返回
  `VERIFIED_SHARD_COVERAGE`、`coverage_exact=true`、`processed_pairs=853575813`
  且 `survivors_found=0`。四个 JSON 的 SHA-256 与 trust boundary 记录见
  `docs/pro-b27-two-component-shard-coverage-20260829.md`。这只提升了同一受限
  two-component 模型的分片覆盖证据，不覆盖 Label-State Completeness，也不能
  升级为全局非存在性定理。

- 2026-08-29 右侧 GPT 顾问对 Stem Owner-Separation 做了第二次精确审计：现有
  `exact-return + least-remote + no-outlier` 只给全局 owner 唯一性、几何选择和
  距离上界，不能推出 cut-local retention 或 removable-owner separation。其最小
  抽象模式是加权路径 `r-[2]-A-[5]-B-[9]-C`，全体距离
  `{2,5,7,9,14,16}` 互异；裁掉 `r` 后 removed-owner 集合 `{2,7,16}` 与保留
  集合 `{5,9,14}` 交错。该模式不是完整 FW319 候选，故只证明当前抽象公理不足，
  不反驳 genuine-candidate 版本。最小附加目标应写成对每个允许 cut 的
  `s in Sigma' => owner_T(s) subset T'`，并加上被裁 owner 值恰为 removable
  block；记录于 `docs/pro-b27-j-empty-stem-descent-preservation-gap.md`，等级
  `GAP/CONDITIONAL`。

## 仍未闭合的最小缺口

在上述 exact-return 前提下，`fixed-low exhaustion` 的局部蕴含已得到条件性
确认，且低几何已有条件性有限 decoder；但尚未把这些前提逐项证明为对所有候选
状态的 branch-wide 假设，也尚未实现并穷尽 `(V_new,E_*,lambda,iota,omega,Pi)`。
在此基础上，顾问指出的第一处联合量词是：对每个满足低状态必要条件的
`D_L`，其 high-incidence completion 是否都被现有 ordered-high state catalogue
覆盖。有限模型仍未覆盖任意低森林与高骨架的联合枚举、
全部 `34--37` owner 分配，以及把这些状态与 complete spectrum、
least-remote minimality 和 inherited descent 连接起来的
**Label-State Completeness**。此外，`t>=86` 的上尾不能只靠五重
translate 条件压住。因而当前仍不是全局 `b=27` 非存在性定理。

## 下一动作

1. order-4 attachment/LCA 有限扩展已闭合；下一步转向证明
   Label-State Completeness，尤其是任意 low forest 的端口/载体状态与
   任意高子树/有序高弧的覆盖，而不是继续把有限阶数当作全局结论。
2. `t>=86` 上尾仍必须使用完整 J 树的内部距离/owner 约束，不能假设
   `h>=t+19` 自动成立。
3. 不重复提交或重启疑似幽灵的 Hoffman2 `100025`，也不把它当作证据。
4. 后续处理 `t>=86` 时必须使用完整 J 树的内部距离/owner 约束，不能
  假设 `h>=t+19` 自动成立。

- 2026-08-29 顾问提出并经控制器独立审计的条件性命题已写入
  `docs/pro-b27-h37-owner-saturation.md`：在 complete punctured ownership、
  global pair injectivity、固定 `S0`、J32 single-edge 与 literal 5/21
  shared-edge 假设下，所有未固定的新增 low edges 只能取
  `H37={5,16,18,19,20,21,24,25,26,34,35,36,37}` 中的权重，且每个
  `d<=37` 的 low-component pair 都有唯一 owner。审计特别把已固定的
  `32` 从新权重集合中排除；该命题只给出有限 owner-state 上界，仍不证明
  现有 catalogue 的 incidence/rooted-realization 完备性。

- 2026-08-29 针对 J34--37 的下一最小接口已整理为
  `docs/pro-b27-j-rooted-normal-form.md`。在已证 admissible word、J-root
  和 `d6` 距离上界假设下，owner path 的首次进入点只能是实际 path
  vertex，`rho` 有显式有限上界；但 `word × entry × rho` 不能单独决定
  stem 的多边分解或旁支，因此 descriptor 必须保留完整 rooted edge-list、
  topology、alias pattern 和 depth table。该结果是 `PROVED (conditional
  finite representability)`；从 descriptor 到现有 catalogue 的 surjectivity
  仍是 `GAP`，尚未启动 rooted-realization 枚举。

- 2026-08-29 在 Geo Workstation 专用 `.venv` 上完成首个 rooted-normal-form
  拓扑 pilot（最多 4 个新增顶点）：`17` 个 rooted topology、`16` 个 admissible
  words、`1388` 个 canonical embeddings；远端和本地项目 `.venv` 的独立 verifier
  均返回 `VERIFIED_ROOTED_NORMAL_FORM_TOPOLOGY_PILOT`。artifact
  `theory-lab/topwindow/results/pro_b27_j_rooted_normal_form_topology_k4_geoworkstation.json`
  的 SHA-256 为 `c73582236c55c0a64d9e5a04c16d19b982d809b0d55daf48dee1161525758ecf`。
  该 pilot 只验证 rooted topology/entry 编码；stem/branch 的实际边权、pair
  spectrum、owner injectivity 和全量 `<=10` coverage 仍未完成，不能升级为定理。

- 2026-08-29 在 Geo Workstation 完成正确计数的 `max-new=10` rooted-normal-form
  拓扑分片：先独立得到 `global_row_count=1077588`，再以 8 个确定性区间覆盖
  `[0,1077588)`；8/8 分片 verifier 均返回
  `VERIFIED_ROOTED_NORMAL_FORM_TOPOLOGY_SHARD`。独立合并器返回
  `processed_rows=1077588`、`merged_index_digest=72733b6bf9d59974ab2cfe56dd82fae9097cb0beb8594d929f988842c1ff5327`
  和 `VERIFIED_ROOTED_NORMAL_FORM_TOPOLOGY_SHARD_MERGE`。此前错误声明
  `global_row_count=1639524` 的目录被保留但排除为无效证据。该结果仍只覆盖
  rooted topology/entry 编码，不包含 stem/side-branch 权重、完整 pair
  spectrum 或 J34--37 rooted-realization surjectivity。

- 2026-08-29 右侧 GPT 顾问给出下一最小桥梁
  `Weighted Incidence Lifting Lemma`：对每个 genuine J34--37 rooted realization
  `R`，必须证明存在唯一拓扑行 `tau` 及 `(lambda,iota,Omega)`，使
  `R` 同构于 `Lift(tau,lambda,iota,Omega)`；`lambda` 保存每条原始边权，
  `iota` 保存所有 low/high incidence，`Omega` 保存真实 owner/alias/reuse。
  顾问指出第一承重缺口是：拓扑行是否保留所有可能外部枝条的真实附着顶点，
  不能把边内部压缩掉。

- 对现有 rooted topology pilot 做了轻量 schema 审计（无枚举、无谱求解）：
  `audit_pro_b27_weighted_incidence_schema.py` 在 1388 行上返回
  `GAP_WEIGHTED_INCIDENCE_SCHEMA`；每行均缺少 `edge_weights`、`incidence_map`、
  `owner_marks`、`pair_table_hash`、`root_depth_table`，且 1388 行仍标记
  `OWNER_WORD_ONLY_FREE_STEM_UNASSIGNED`。因此当前 topology catalogue 不能
  升级为 weighted rooted-realization completeness；下一门槛是一个带完整
  edge-list/weight/incidence schema 的小 pilot 及独立 round-trip verifier。

- 2026-08-29 完成上述最小 codec gate：3 个手写 rooted fixtures 带有完整
  `edge_weights`、`incidence_map`、`owner_marks`、`named_aliases`、全 pair
  table 与 hash。独立 verifier 不导入 builder，重建树、检查树性、重算全部
  pair distances/root depths，并核对 owner word；返回
  `VERIFIED_WEIGHTED_INCIDENCE_SCHEMA_PILOT`。artifact
  `theory-lab/topwindow/results/pro_b27_weighted_incidence_schema_pilot.json`
  的 SHA-256 为
  `39172f25d856c1ec1834f3784415897446cc34159ff5cc22b41326e460e5d765`。
  这只验证 schema round-trip，不是候选树枚举、谱排除或 catalogue
  surjectivity；下一步仍需在 Geo Workstation 将该 schema 接到真实 rooted
  topology 行，并独立验收所有可能 incidence 点。

- 随后把现有 rooted topology pilot 的前 3 行实际接入完整 row schema：保留原
  `tree_edges`、owner word、entry/root，补入逐边 `edge_weights`、逐顶点
  incidence slots、owner/alias、pair table/hash 与 root-depth table；独立
  verifier 重建树并重算所有 pair distances，返回
  `VERIFIED_WEIGHTED_ROOTED_ROW_LIFT_PILOT`。artifact
  `theory-lab/topwindow/results/pro_b27_rooted_rows_schema_pilot.json` 的
  SHA-256 为 `d8dbb1595fa832e7baafc05ad29efb30c2bfbbfca30e8f2a560b558d6943d46d`。
  该 lift 明确把非 owner 边权标为 synthetic fixture、incidence 标为
  `UNCLASSIFIED_PLACEHOLDER`；因此只证明真实 topology 行可以进入无损 schema，
  不证明这些权重可实现、incidence 分类完备或 spectrum 通过。

- 在 Geo Workstation 对现有 bounded P25 low-decoder pilot 的全部 `3934` 个
  canonical rows 做了 full low-schema lift（固定 `m<=3,e<=2` 输入）：逐行保留
  literal low `edge_weights`、组件/端口、逐顶点 incidence、所有 H37 owner
  pairs、low pair table/hash 与 `d6` root-depth table。独立 verifier 重建每个
  低森林、检查组件树性与不相交分割，并逐行重算 pair distances/owner lookup；
  返回 `VERIFIED_P25_LOW_ROWS_SCHEMA_LIFT`。远端 artifact
  `/home/geo/codex-work/p25-low-schema-lift-20260829/lifted.json` 的 SHA-256
  为 `7d6908b88783fe7ae672af4293d5097442618a68b0279dffeea7d3e9088282cf`。
  这扩大了真实 low-row schema 的验证覆盖，但仍不含 high completion、m>3
  或全 P25 surjectivity。

- 2026-08-29 将顾问指出的“隐藏附着点”缺口拆为条件性
  `Literal-vertex retention lemma`：在 literal-edge convention、每个真实
  J-fragment 至多 10 个非根顶点、且相关联合 incidence 能放入同一 fragment
  的前提下，边内部附着点会自动成为显式 subdivision vertex，故不需要隐藏
  midpoint。对现有 1388-row pilot 的结构审计
  `audit_pro_b27_literal_vertex_retention.py` 返回
  `OBSERVED_LITERAL_VERTEX_RETENTION`。这只验证每行的树性、连续 vertex IDs
  和 owner path 引用；≤10 branch-wide bound、联合 incidence 以及 weighted
  lifting 仍是 GAP。

- 同一 rooted-row lift 在 Geo Workstation 目录
  `/home/geo/codex-work/schema-pilot-20260829` 独立运行并通过
  `VERIFIED_WEIGHTED_ROOTED_ROW_LIFT_PILOT`（3 fixtures，远端 artifact SHA-256
  `7b4ad9a543d91279ab1b0a5a7a04a1658798cdee49fc7173690a38ad0da8fd8d`）。由于
  source-path 元数据不同，该 hash 不要求与本机字节相同；状态、字段和独立
  重建检查一致。远端结果仍是 schema/adapter 证据，非 weighted catalogue
  surjectivity。

- 右侧 GPT 顾问进一步给出 `No Hidden Attachment Point Lemma` 的精确验收规则：
  只有“完整 incidence-expanded tree 中 degree 恰为 2 且未标记”的顶点才可
  被 suppress；若只按 owner-path fragment 内部 degree 判断，局部 degree-2
  点可能在全树携带外部枝条。最小 codec 反例是 `A-x-C` 加枝 `x-B`：压掉
  `x` 即使保留 `A--C` 总长，也无法重建 `d(B,A),d(B,C)`。因此当前
  `OBSERVED_LITERAL_VERTEX_RETENTION` 仅是结构事实；full-tree degree、联合
  incidence 与 ≤10 bound 仍需 branch-wide 证明。

- 重新核对 `docs/pro-b27-universal-catalogue-surjectivity.md` 后确认：定义级
  `U^can_25` 已在固定 15-vertex packet `K` 与剩余 ≤10 顶点的条件下给出
  `realization -> U^can_25` 的 named-preserving surjection，完整 edge list/weights
  和联合 incidence 不会在抽象 catalogue 中丢失。因此当前承重问题已精确化为：
  压缩 low/high generator 是否 surjective 到这些完整状态，或是否直接保留
  universal state；不能用 topology-only row count 替代该量词。该澄清不增加新
  计算，也不提升任何全局非存在性结论。

- 2026-08-29 将完整 `U^can_25` 到压缩状态的关系正式写成
  `docs/pro-b27-deterministic-threshold-projection.md`：按权重 37 阈值确定
  `F_L`、`tau_L`、`omega_L`、`Pi`，再收缩 low components 得到 `tau_H`、端点
  incidence `I`、有序 high-arc subdivision 与原始 high-weight tuples。只要
  保留所有边界端点和有序边元组，逆展开可逐边恢复原树，因此条件性得到
  `forall T in U^can_25 exists! P(T)`。但这不等于当前实现的
  `GeneratedStates` 对 `P(T)` 的 surjectivity；后者仍是
  `Low-Catalogue/Label-State Completeness` 的最小未闭合量词。

- 与上述投影接口对照现有 high-side 证据：`VERIFIED_HIGH_BRANCH_SKELETON_PARTITION`
  已覆盖 order `<=10` 的 `143654` 个 marked arcs；`VERIFIED_ORDERED_OUTWARD_ENCODING`
  已覆盖 `1809` 个 rooted tree instances、`22515` 个 degree-two mark cases。
  这些结果支持 `tau_H/I/arc_subdivision` 的逆展开无损性，但只是有限图论
  reconstruction audit，不证明固定 `K` 的全部联合 incidence 会进入实际
  generator。

- 右侧 GPT 顾问针对全部 `3934` 个 bounded low rows 给出下一条正式 contract：
  `Unique High-Quotient Completion Interface`。对每个 low row `D_L`，每个真实
  completion `T` 必须诱导 rooted quotient `Q_H`，且 (i) 收缩 low components
  后仍为树，(ii) 每个非根 low component 恰有一个 parent/rootward high edge，
  (iii) 每条 high edge 的两端真实 incidence 均保留，(iv) high-only degree-2
  subdivision 均进入 ordered arc state。等价的唯一承重条件是：不能有 high
  branch 附着在 `D_L∪Q_H` 之外的点。该 contract 已加入
  `docs/pro-b27-deterministic-threshold-projection.md`；它保证 materialization
  可无损重建，但实际 `Q_H` generator 的 surjectivity 仍是 GAP。

- 本轮轻量复核 `verify_pro_b27_vertex_budget.py` 与
  `verify_pro_b27_port_complete_state_roundtrip.py` 均通过：`known_vertices=15`、
  `maximum_additional_vertices=10`，以及 2 个 low components、2 个 rootward
  ports、3 个 outward ports 的完整 edge/距离 round-trip。两项均明确是条件性
  budget/interface 证据，不是任意 low forest 或全局 catalogue coverage。

- 右侧 GPT 顾问给出并审计了当前最小的 `Two-Stage Projection Surjectivity`
  contract（仅作为待验证命题）：设 `P(T)=(L(T),H(T))`，其中 `L` 保留完整
  literal low forest、边权、组件/端口、所有 boundary incidences、owner/alias
  与 shared identities，`H` 保留 rooted high quotient、每条 high edge 的两端
  incidence、所有 high-only subdivisions 与 ordered 原始权重。实际生成器必须
  同时满足
  `forall T exists l in G_L: l=L(T)`（`L-surj`）以及对每个匹配 low row 的
  `forall T exists h in G_H(l): h=H(T)`（`H-surj`），再结合既有 lossless
  materialization 才能推出完整状态覆盖。现有 `U^can_25` 定义、确定性投影和
  有限 round-trip 只支持 reconstruction direction，不支持这两个 generator
  surjectivity 量词。

- 因而当前第一未闭合量词精确收窄为 `L-surj` 的逐字段 decoder
  `T -> raw_key(L(T))`：low topology/anonymous slots、literal endpoint 与权重、
  所有 outward incidence subset、named/shared identity，以及 `34--37` 的实际
  owner/path 三态都必须对任意 genuine state 有定义。若某字段只有 bounded pilot
  或预设模式证据，状态仍是 `GAP_L_SURJECTIVITY`；下一步只做轻量字段审计，任何
  扩大枚举仍统一提交 Geo Workstation，暂不进入 `m=4`。

- 顾问随后将同一要求压缩为 `Projection-Key Surjectivity`：对
  `G=Good(U^can_25)∩Phi` 中每个真实 `T`，必须存在合法 `k_L,k_H`，使
  `Decode(k_L)=L(T)` 且 `Decode(k_H)=H(T)` 逐字段成立，并满足
  `Decode(encode(P(T)))=P(T)`。现有 `3934` rows 与 high round-trip 只证明
  `key -> tree` 的 reconstruction correctness；尚未证明 `tree -> key` 的
  覆盖。该输出进一步确认：在逐字段 encoder/合法域的 left-inverse contract
  完成前，不应把有限 pilot、EDGE/FWD/REV 或扩大枚举当作 surjectivity。

- 对 `enumerate_pro_b27_p25_low_decoder_pilot.py` 做了只读逐字段审计，记录于
  `docs/pro-b27-low-decoder-field-audit.md`。最早失败点是脚本硬性限制
  `m<=3`，而 `U^can_25` 允许最多 10 个非 `K` 顶点；独立遗漏还包括仅用
  `H37` 14 值而非完整 `<=37` 边权域、只允许触及匿名顶点的新增边、含多个
  fixed 顶点的 component 被拒绝、fixed component incidence 被强制为空，以及
  shared `(5,16)/(16,5)` 的 `21` 形状未实现。故当前状态明确为
  `GAP_L_SURJECTIVITY`；单纯扩大 `max_vertices` 不能闭合。

- GPT 顾问进一步确认：`U^can_25` 的 definition-level canonicalization 不能
  直接推出 `L-surj`。推荐路线是把 low generator 的**定义域**升级为 universal
  literal low-state domain（`0<=m<=10`、所有 literal low-edge sets/weights、
  component partitions、rootward/outward incidences 与 named/shared identities），
  再把 `5/21/32/34--37` 作为过滤谓词。这样可定义总的
  `T -> raw_key(L(T)) -> canonical key`；但直接全空间枚举不可行，仍需另一个
  finite-reduction/剪枝定理，或证明 compressed generator 完整覆盖该 universal
  domain，才能接到最终非存在性搜索。当前没有启动该巨大枚举。

- 顾问进一步区分了两个不能混淆的命题：非枚举的 total encoder/decoder
  `E_L,D_L` 加上 `D_L(E_L(L(T)))=L(T)`，足以在定义层证明
  `forall T in G exists k in K_L: D_L(k)=L(T)`；但要让“零 survivor”的计算
  具有证明意义，还必须另证 `Finite Search Reduction Lemma`，即存在可实际
  生成的有限子集 `K_L^search ⊆ K_L`，使所有 genuine `T` 的 `E_L(L(T))`
  都落入其中。故当前路线应先关闭 encoder totality/left-inverse，再单独证明
  剪枝/有限化保持所有真实状态；两者不可用有限 pilot 相互替代。

- 已将后续计算接口写成 `docs/pro-b27-finite-search-reduction-contract.md`：在
  `E_L,D_L` 的 totality/left-inverse 之外，必须另证一个可计算有限子集
  `K_L^search`，满足所有 genuine `T` 的 `E_L(L(T))` 都在其中；所有剪枝、对称
  约化、shard 覆盖和 high-stage conditional generator 也要逐量词验收。当前
  `m<=3,e<=2` pilot、高骨架 order-10 round-trip 仅是有限接口证据，不能充当该
  reduction lemma；没有启动新的本机或远程枚举。

- 按顾问建议补写了定义级 universal literal encoder/decoder 合同
  `docs/pro-b27-universal-low-encoder-left-inverse.md`：对 `0<=m<=10` 的所有
  literal low edges/weights、组件、ports、outward incidences、owner/alias 与
  shared identities，取匿名顶点规范化后的有限字典序最小序列 `E_L`，由完整
  literal 记录解析为 `D_L`。已给出 `D_L(E_L(L))=L`（仅允许匿名重标号）的
  left-inverse 证明，因此 definition-level `forall T exists k in K_L` 可以成立；
  但 `K_L` 不是可直接遍历的 search set，finite-search reduction、剪枝完备性
  和远程 shard coverage 仍未证明，不能提升为非存在性结论。

- GPT 顾问对 finite reduction 给出更严格的接口：压缩实现必须有
  `C:K_L -> K_L^search` 与 realization `R`，满足
  `forall T in G exists k in K_L^search: R(k) ≅ L(T)`；同时证明统一复杂度
  上界、无损恢复（或有限显式展开）、owner-completeness、命名保持及每条剪枝
  规则的 soundness。已有 H37 支撑边数上界和十顶点预算并不足够，不能假定
  所有低边都落在十四条 H37 owner paths 上；该额外假设仍是 GAP。

- 右侧 GPT 顾问进一步给出完整 Geo 接口，已固化为
  `docs/pro-b27-complete-low-generator-spec.md`：在 Fixed-L/H37 Edge
  Exhaustion 条件下，raw key 直接记录 `(m,E_new,lambda,omega,Pi,O)`，共享
  owner path 由 literal edge list 与 owner endpoints 自动重建，不另设有限
  shape 标签；匿名顶点只做 named-preserving canonicalization，`Pi/O` 枚举
  全部真实 port/outward 子集。低侧先验收树性、固定 owner、puncture、低 pair
  单射和 5/21 实际路径，再以 `(m,e,rank(E),rank(lambda),rank(Pi),rank(O))`
  做确定性分片。该接口可在 Geo 上实现 conditional L-surj，但 high completion、
  full cap/injectivity、least-remote/descent 仍需后续定理。

- 针对该 GAP，已把最小承重命题明确写成 `Fixed-Low / H37 Edge Exhaustion`：
  对任意 genuine `T` 和任意 `e∉E(K)`，若 `w(e)<=37`，则必须有
  `w(e)∈H37` 且 `e` 位于该值的唯一 owner path。它与十顶点预算、port-complete
  incidence 和 ordered-arc 保留结合后，才足以产生有限 literal low-forest
  search domain。仓库现有 `pro-b27-h37-owner-saturation.md` 只在 complete
  punctured ownership、固定 `S0`、J32 single-edge、literal 5/21 等条件下证明
  该蕴含；这些前提尚未 branch-wide 闭合，故仍标为 `GAP/CONDITIONAL`。

- 右侧 GPT 顾问完成了针对该承重命题的 branch-local 审计（只读、未计算）：现有
  exact-return 条件可严格推出 `34--37` 的 owner 只能位于 L-internal 或
  J-internal；若位于 J，则 `j-low-path-compositions` 给出的有限 word catalogue
  是 sound 的，故 J-side 不得生成表外 word。现有条件不能推出 `34--37` 在 L/J
  两侧的 endpoint、LCA、rooted attachment 的全局有限分类；例如 L 侧 literal
  `x-y=34`，或 J 侧 `16+18=34` 配不同 root 接入，均不违反已有假设。因此
  `Fixed-Low/H37 Edge Exhaustion` 的 saturation 蕴含本身可作为条件性 sound
  前提，但 `34--37 realization surjectivity` 仍是最小未闭合量词。Geo generator
  必须从 literal forest 的实际 pair table 派生 `L_ACTUAL`/`NOT_L`，不得把
  EDGE/FWD/REV 或固定 endpoint cells 当作剪枝前提；该审计未启动任何新计算。

- 完成了 H1--H5 的分支假设引用链审计，记录于
  `docs/pro-b27-branch-hypothesis-discharge-audit.md`。对 genuine order-25
  exact-return-33、固定 literal `K`、当前 J32 residual branch：H1（`[1,37]`
  除 4 的唯一 owner）和 H2（全局 pair-distance injectivity）来自 exact-return
  定义；H3 由固定 `K` 的 literal 距离保持性加 H2 推出；H4 由 residual two-branch
  replay、J32 single-edge、5/21 L-owner 与 L-shape 三份已核验文档组成；H5 是
  正整数边权的直接路径事实。因此 `Fixed-Low/H37 Edge Exhaustion` 的
  `w(e)<=37 => w(e)∈H37` 蕴含可提升为
  `VERIFIED_BRANCH_LOCAL_LOW_SATURATION`。这不分类 34--37 的端点/LCA/挂接，
  不关闭 high-completion、least-remote、descent 或全局非存在性；生成器仍须保存
  literal endpoint/path 或 `NOT_L`，不得使用 EDGE/FWD/REV shortcut。

- 在同一 branch-local 审计中进一步闭合了目前对 `34--37` 最强的安全精化：令
  `P_h` 为 `h∈{34,35,36,37}` 的唯一 owner path。由于 carrier floor `w>=38`
  且 `h<38`，`P_h` 必完全位于 L 或 J，不能跨 carrier cut。J 内部的 path word
  只能取已核验 catalogue；rooted-difference 检查还可安全删除除
  `35=(16,19)/(19,16)` 外的 middle-entry words，以及 `37` 中含
  `5,32,16,21` 的 endpoint-entry words。剩余 `(16,18),(16,19),(16,20),(18,19)`
  等必须保留为 literal endpoint/path 状态。L 内部则只有“非固定真子路径距离不得为
  4 或固定 `S0` 值”的 materialized-path 剪枝，不能推出有限 named endpoint/LCA
  列表。故当前缺口已精确改写为 residual L/J words 的实际 endpoint/incidence
  realization coverage，而非 H37 saturation。

- universal literal low-generator 的首个完整 smoke 域已仅在 Geo Workstation
  上执行：`m∈{0,1}`、`e∈{0,1}`，所有允许 literal endpoint pairs、13 个 H37
  权值候选、每个低组件的全部 rootward ports 与 outward masks；非法 base 保留为
  显式 sentinel。返回 `VERIFIED_UNIVERSAL_LOW_SMOKE`：
  `global_raw_count=15,925,432`、`processed_raw=15,925,432`、
  `accepted_raw=15,925,248`、`sentinel_raw=184`、`coverage_exact=true`；分块为
  `m0_e0=196,608`、`m1_e0=393,216`、`m1_e1=15,335,608`。sentinel 原因是
  `edge_weight_duplicate=60`、`fixed_owner_reuse=17`、
  `pair_distance_duplicate=107`。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_smoke_geo_20260829.json`，
  SHA-256 `02499645647d50b340c93781d27909a24487a904a1183978339c22716c25865a`。
  独立 verifier `verify_pro_b27_universal_low_smoke.py`（不导入生成器）在 Geo
  上重建全部 base/radix/拒绝原因并返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。这仍是 m≤1/e≤1 的编码与分片
  证据，不覆盖 m≤10、high completion 或全局非存在性。

- 在 smoke 生成器泛化 canonicalization 后，Geo Workstation 完成了下一层
  `m=2,e=0`：两个匿名孤立 low components，全部 rootward/outward incidence
  展开。返回 `VERIFIED_UNIVERSAL_LOW_SMOKE` 且 `global_raw_count=
  processed_raw=accepted_raw=786,432`、`sentinel_raw=0`、
  `coverage_exact=true`；匿名交换的 `S_2` canonicalization 得到
  `canonical_count=589,824`，`orbit_sum=786,432`。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e0_geo_20260829.json`，
  SHA-256 `94eab60ea194104416ad06f265938b479dbfaa79c59f2c123a39a94111a89223`。
  独立 verifier 在 Geo 上重建固定森林、radix 和 `S_2` 轨道比例，返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。这首次验证了 anonymous shared
  identity 的 canonical/orbit 层；仍未覆盖含新增 low edge 的 `m=2,e=1`、
  `m≤10` 完整域或 high completion。

- 进一步在 Geo Workstation 完成共享匿名端点分片：`m=2,e=1`、端点仅为
  `x0--x1`、权值候选 `{5,16}`，完整展开全部 ports/outward masks。返回
  `VERIFIED_UNIVERSAL_LOW_SMOKE`：`global_raw_count=1,572,865`、
  `processed_raw=1,572,865`、`accepted_raw=1,572,864`、`sentinel_raw=1`、
  `canonical_count=786,432`、`orbit_sum=1,572,864`、`coverage_exact=true`；
  `5` 的共享匿名 low edge 全部通过，`16` 因固定权重重复保留为一个 sentinel。
  artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_anon_pair_5_16_geo_20260829.json`，
  SHA-256 `28b604877cc934c12c4c029b0f434cae9c4862821979293b4540c4c2db9c6562`。
  独立 verifier 在 Geo 上重建该端点/权值分片与拒绝计数，返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。这验证了共享匿名顶点、权值冲突
  sentinel 和 orbit 处理；仍不覆盖其它端点类型、`m≤10` 或 high completion。

- 又完成了命名端点分片：`m=2,e=1`、端点类型 `x0--named`、权值候选 `{5,16}`，
  在 Geo Workstation 上完整展开 ports/outward masks。返回
  `VERIFIED_UNIVERSAL_LOW_SMOKE`：`global_raw_count=2,621,468`、
  `processed_raw=2,621,468`、`accepted_raw=2,621,440`、`sentinel_raw=28`、
  `coverage_exact=true`；sentinel 原因为 `edge_weight_duplicate=15`、
  `fixed_owner_reuse=4`、`pair_distance_duplicate=9`。独立 verifier（已修正
  允许 sentinel 出现在样本前缀）在 Geo 上重建端点/权值分片并返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_5_16_geo_20260829.json`，
  SHA-256 `723f652052669e4f5d492fdd5fa9b2c0334673e1ce4317ecbeabdd637c1b3a19`。
  这补上了命名端点与共享匿名端点之外的第二类 m=2 覆盖证据；完整 m=2 权值/端点
  域、m≤10 和 high completion 仍未完成。

- 重新生成了此前旧 schema 的 `m=2,e=1`, `x0--named`, 权值 `{5,16}` 分片。
  v2 结果在 Geo Workstation 上覆盖 `2,621,468` raw，接受 `2,621,440`，保留
  `28` 个显式 sentinel（`edge_weight_duplicate=15`、`fixed_owner_reuse=4`、
  `pair_distance_duplicate=9`），`canonical_count=2,621,440`、
  `orbit_sum=2,621,440`、`coverage_exact=true`。加强版独立 verifier 从样本的
  materialized edges 重算 owner-status，并返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`；每个 accepted sample 均含完整
  H37（14 值）owner-status 域。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_5_16_geo_20260829_v2.json`，
  SHA-256 `754a36c780e66ad76d9faaf6f6fb414994edd1c400b60b7e82fdc91ca31f815b`。
  这仍只闭合该 endpoint/weight shard；x1 对称 raw slice、其余命名权值及全
  `m≤2,e≤1` merge 尚未完成。

- 先前 `m=2,e=1`、`x0--x1`、权值 `{18,20,21,24,25,26}` 的远程结果确认了计数，
  但属于旧 schema（没有显式 total `owner_status`），因此只保留为 legacy smoke，
  不进入 theorem-supporting merge。随后在 Geo Workstation 用修正后的
  `literal-low-v2-owner-status` 生成器重跑同一分片：`global_raw_count=
  processed_raw=accepted_raw=9,437,184`、`sentinel_raw=0`、
  `canonical_count=4,718,592`、`orbit_sum=9,437,184`、`coverage_exact=true`。
  新 artifact 的每个 accepted sample 都含 H37 的完整 14 值 owner-status 域，
  未出现的值显式记为 `NOT_L`；Geo 独立 verifier（不导入生成器）返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_anon_pair_18_20_21_24_25_26_geo_20260829_v2.json`，
  SHA-256 `cdab3735a9185e116e120bb7cb7cdb34f024b23d8648b7689ece2756136c77da`。
  这只闭合该 endpoint/weight shard 的 schema 与 orbit 证据；`x0--named` 的其余
  权值、全 m≤2,e≤1 merge、m≤10、high completion 与全局非存在性仍未完成。

- `m=2,e=1`, `x0--named`, 权值 `{18,20,21}` 的 v2 分片已在 Geo Workstation
  完成并经加强版独立 verifier 验收：`global_raw_count=11,796,515`、
  `processed_raw=11,796,515`、`accepted_raw=11,796,480`、`sentinel_raw=35`、
  `canonical_count=11,796,480`、`orbit_sum=11,796,480`、
  `coverage_exact=true`；sentinel 为 `fixed_owner_reuse=8`、
  `pair_distance_duplicate=27`。样本 owner-status 从 materialized edges 独立
  重算一致，并含完整 H37 14 值域。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_18_20_21_geo_20260829_v2.json`，
  SHA-256 `057e8abcac361634f62c23e062ec4fa98ffe22fe99e124dca04ddcb17f0e3ca9`。
  `x0--named` 仍有其余权值块及 x1 raw slice 未完成，因此尚不能做全域 merge。

- `m=2,e=1`, `x0--named`, 权值 `{24,25,26}` 的 v2 分片已在 Geo Workstation
  完成并经加强版独立 verifier 验收：`global_raw_count=16,252,959`、
  `processed_raw=16,252,959`、`accepted_raw=16,252,928`、`sentinel_raw=31`、
  `canonical_count=16,252,928`、`orbit_sum=16,252,928`、
  `coverage_exact=true`；sentinel 为 `fixed_owner_reuse=5`、
  `pair_distance_duplicate=26`。accepted sample 的 owner-status 从 materialized
  edges 独立重算一致，并含完整 H37 14 值域。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_24_25_26_geo_20260829_v2.json`，
  SHA-256 `487d7b9c105f27494f4a793cbd0c7e3f7e0dd91dfc8eebf7e8861509bd393c8b`。
  `x0--named` 尚余 `{19,32,34,35,36,37}` 权值及 x1 raw slice，故仍不能做全域
  `m≤2,e≤1` merge。

- `m=2,e=1`, `x0--named`, 权值 `{34,35}` 的 v2 分片已在 Geo Workstation
  完成并独立验收：30 个 raw/base 状态全部为 sentinel，`34` 因固定边权重复，
  `35` 因 pair-distance 冲突；`accepted_raw=canonical_count=orbit_sum=0`，
  `coverage_exact=true`。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_34_35_geo_20260829_v2.json`，
  SHA-256 `2a111ba5ec1d165fd58571d4a990ded10197fcdb94a41f798d4c53ab533dda95`；
  独立 verifier 返回 `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。剩余 x0 权值
  `{36,37}` 与 x1 raw slice 仍待处理。

- `m=2,e=1`, `x0--named`, 权值 `{19,32}` 的 v2 sentinel-only 分片已在 Geo
  Workstation 完成并独立验收：30 个 raw/base 状态全部因固定边权重复而成为
  显式 sentinel，`accepted_raw=canonical_count=orbit_sum=0`，
  `coverage_exact=true`。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_19_32_geo_20260829_v2.json`，
  SHA-256 `a831737bb64f0f9119f7d553d4b544edf8d0c89eaa420d63bb7174a38bae5eed`；
  独立 verifier 返回 `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。这只闭合两个
  权值的拒绝语义，不增加 accepted coverage；剩余 `{34,35,36,37}` 与 x1 raw
  slice 仍待处理。

- GPT 顾问审计发现旧 v2 的 `H37` 把固定 J 单边权值 `32` 错当作可分配 low
  lambda。已冻结 branch-correct schema：可分配域
  `H37_L={5,16,18,19,20,21,24,25,26,34,35,36,37}`（13 值），owner-status
  域为 `H37_L∪{32}`，并强制 `owner_status[32]=NOT_L`。此前生成的 v2 artifact
  因 canonical/status 语义不同全部保留为 pre-freeze evidence，不得直接参与
  theorem-supporting merge；后续分片须用该冻结 schema 重跑或有严格迁移证明。

- `m=2,e=1`, `x0--named`, 权值 `{36,37}` 的 v2 分片已在 Geo Workstation
  完成并独立验收：30 个 raw/base 状态全部因 pair-distance 冲突成为显式
  sentinel，`accepted_raw=canonical_count=orbit_sum=0`，
  `coverage_exact=true`。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_36_37_geo_20260829_v2.json`，
  SHA-256 `270a52e8c94046dcb1a65681eebf02d5c9d9786f12d89ce21bb8fa84eb96ae02`；
  独立 verifier 返回 `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`。至此 x0 命名
  侧的 14 个 H37 权值候选均有 v2 raw 证据（其中部分为 sentinel-only），但 x1
  raw 对称片与全域 merge 仍未完成。

- 在冻结 `H37_L`/`32:NOT_L` 语义并修正 sample 采样后，`m=2,e=1`,
  `x0--named`, 权值 `{5,16}` 的 v4 分片在 Geo Workstation 重新完成：
  `global_raw_count=2,621,468`、`processed_raw=2,621,468`、
  `accepted_raw=2,621,440`、`sentinel_raw=28`、
  `canonical_count=2,621,440`、`orbit_sum=2,621,440`、
  `coverage_exact=true`；sentinel 计数为 `edge_weight_duplicate=15`、
  `fixed_owner_reuse=4`、`pair_distance_duplicate=9`。首个 accepted sample 的
  完整 owner-status（13 个 low 值加固定 `32:NOT_L`）由独立 verifier 从
  materialized edges 重算一致。artifact 为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_5_16_geo_20260829_v4.json`，
  SHA-256 `f95ee4d194805d5485bef9a985085190dda685abbcf9fdaa983016baa63c8f19`。
  该片是冻结 schema 下的正式 x0 named 基线；其余 x0 权值、x1 transport 与
  全域 merge 仍未完成。

- 对冻结 schema 下的 `x0--named {5,16}` 已生成严格 `S2` transport certificate，
  证明 `x0↔x1` 在 15 个 named endpoint、每个 weight block、全部 port/mask
  radix 上的 raw-rank 双射；同时记录 acyclicity、puncture、pair-distance、
  fixed-owner、H37_L owner-uniqueness 的谓词等变性，materialization/owner
  status（含 `32=NOT_L`）搬运规则和 canonical invariance。证书状态为
  `VERIFIED_X1_TRANSPORT_CERTIFICATE`，文件为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x1_transport_5_16_geo_20260829.json`，
  SHA-256 `9bde509c02fcd867ac83e955dca534ff399b60fd4599feeb6e159d09c41b2d56`。
  这可在严格 transport 假设下替代显式 x1 大枚举；其余 weight blocks 的
  transport 证书需在对应冻结-schema x0 分片完成后生成。

- 在同一冻结 `H37_L`/`32:NOT_L` schema 下，`m=2,e=1`, `x0--named`, 权值
  `{18,20,21}` 的 v3 分片已在 Geo Workstation 完成。artifact
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_18_20_21_geo_20260829_v3.json`
  的 SHA-256 为
  `26d7a84d53794a66588f9bada0e627433807a7a453bcc7be79f2e62cb1a99f89`。
  计数为 `global_raw_count=processed_raw=11,796,515`、
  `accepted_raw=canonical_count=orbit_sum=11,796,480`、
  `sentinel_raw=35`、`coverage_exact=true`；sentinel 原因为
  `fixed_owner_reuse=8`、`pair_distance_duplicate=27`。独立 verifier 返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`，并复放首个 accepted sample 的
  owner-status 全域（13 个 low 值及固定 `32:NOT_L`）。该结果可进入
  `ready for shard-wide schema audit`，但不等同于全局 surjectivity 或最终非存在性证明。

- 对冻结 schema 下的 `x0--named {18,20,21}` 生成并验收了对应的 `x0↔x1`
  严格 S2 transport certificate。证书文件为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x1_transport_18_20_21_geo_20260829.json`，
  文件 SHA-256 为
  `4713c97279bf13d9bc181d2fe0e7aaaa8e14c8102055b9b394ec44d7171ba7bf`，
  证书内 digest 为 `75bbb02674e8b540a2158b5219fcab43fd2c3fc3b10264eac484bcfb5b172d1c`。
  独立脚本返回 `VERIFIED_X1_TRANSPORT_CERTIFICATE`，覆盖 15 个 named endpoint、
  `{18,20,21}` 三个 weight block、全部 port/mask radix，并保留 owner-status
  transport（含 `32:NOT_L`）与 canonical invariance。该证书只覆盖此 weight block，
  不替代其余 block 或全域 merge 审计。

- 已按上述顺序在 Geo Workstation 启动冻结 schema 的下一分片：
  `m=2,e=1`, `x0--named`, 权值 `{24,25,26}`，脚本
  `enumerate_pro_b27_universal_low_smoke_v5.py`，远端 Python PID `2531250`，
  输出目标为 `smoke/universal_low_m2_e1_x0_named_24_25_26_v3.json`。启动前
  已通过 `py_compile`，脚本 SHA-256 与冻结源码一致为
  `d85477cbf156e1abdfa1e84559c03ec78443ce597143cdae3b5aa82e2739a5e6`；该任务
  仍在运行，尚无可验收结果。

- GPT 顾问在完成 `{18,20,21}` 后审计确认：该分片可标为
  `ready for shard-wide schema audit`，但不能升级为全局 surjectivity。冻结
  `m≤2,e≤1` 全覆盖、shard-wide owner-totality（不能只验 samples）、全局
  canonical/orbit merge certificate、扩展到完整 low finite domain、high-generator
  surjectivity，以及最终 full-tree predicates（pair-distance、puncture、cap、
  fixed owners、least-remote/inherited descent、`t≥86`）仍分别需要新证书或新
  数学桥接。`34--37` 全局 endpoint/LCA/attachment 分类、J-side rooted-depth
  forcing、以及“所有合法 low rows 都无 high completion”仍是未证结构。

- GPT 顾问进一步把 v3 合并验收拆成两个独立 contract：`owner-totality`
  与 `canonical/orbit merge`。前者必须对每个 accepted raw state、每个
  `h in H37_L` 重建唯一 owner 或 `NOT_L`，并强制 `owner_status[32]=NOT_L`；
  仅有样本 replay 不足。后者必须证明各 shard 的 half-open raw domains
  不重不漏、统一 `schema_version`/`semantic_input_hash`/ordering，且
  `sum_k multiplicity(k)=accepted_raw`；若用 x0--x1 transport，证书还要
  带 source/target scope、置换与 rank-bijection digest。即使两证书通过，
  结论仍只限于 declared frozen `m=2,e=1` 域，不能推出完整 `L`-surjectivity
  或全局 Leech-tree 非存在性。

- GPT 顾问确认：现有 `raw_stream_sha256` 与 `canonical_stream_sha256` 在一个
  真正独立、逐 raw index 重建并逐 accepted row materialize 的 replay 中，
  可以作为全行承诺，不必保存每行；但 replay 必须从冻结 scope/ordering
  独立重算 accepted/sentinel、全部 `H37_L` owner-status、canonical payload，
  并比较 raw/processed/accepted/sentinel 计数、reason counts、canonical_count
  及两条 stream digest。当前 verifier 只检查计数和 samples，因此尚未达到
  这个 owner-totality 证据等级。

- 已在 Geo Workstation 预置独立全流重放器
  `theory-lab/topwindow/verify_pro_b27_universal_low_stream_replay.py`，其
  SHA-256 为 `433d06c9bbc9638fea744627f1124e918ba1f06814070199555a9a99c1626e8e`，
  并已通过远端 `py_compile`。当前 `{24,25,26}` 任务结束后，优先用该重放器
  验收；在它通过前，不把该分片升级为 owner-totality verified。

- `{24,25,26}` 冻结 v3 分片已在 Geo 完成并复制到本地 artifact
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_24_25_26_geo_20260829_v3.json`，
  SHA-256 为 `37481140fb7c6a16018320bc231c29b921527aea15e276e73b27ad58a89118ff`。
  计数为 `global_raw_count=processed_raw=16,252,959`、
  `accepted_raw=canonical_count=orbit_sum=16,252,928`、`sentinel_raw=31`、
  `coverage_exact=true`，sentinel 为 `fixed_owner_reuse=5`、
  `pair_distance_duplicate=26`。普通独立 verifier 已返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`；全流 owner-totality replay
  已在 Geo 以 Python PID `2550180` 启动，尚未完成。

- `{24,25,26}` 的 Geo 全流 replay 已完成并通过：
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_STREAM_REPLAY`。它独立重建全部
  `16,252,959` raw rows，逐 accepted row 重算 owner/canonical payload，并与
  原 artifact 的 `raw_stream_sha256`、`canonical_stream_sha256`、全部计数及
  sentinel reason 完全匹配。replay 日志 SHA-256 为
  `8375b0606dd3c72ca05bf3a0cc542f262e0a9986aaac9addb615dba1a5a2d4e4`；
  结构化证书为
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x0_named_24_25_26_geo_20260829_v3_owner_replay_certificate.json`
  （SHA-256 `3ca65727ff81c0f2729ff08d2081bf7acb56b56d19a983449d1f7ee4b14270f9`）。
  因此该 declared shard 现在可安全标记为 owner-totality verified；它仍
  不是完整 `m=2,e=1` merge，也不推出全局 surjectivity。

- 在 `{24,25,26}` owner-totality replay 通过后，已生成并独立验收对应的
  `x0_named -> x1_named` 严格 S2 transport certificate。文件
  `theory-lab/topwindow/results/pro_b27_universal_low_m2_e1_x1_transport_24_25_26_geo_20260829.json`
  的 SHA-256 为 `8d22e9d7f9231d8cb623f84edc3ca459903f1f20addb6a667bdade2abd90c392`，
  内部 `transport_certificate_sha256` 为
  `a29c718749e6c9fbdc2c9d868ec7f5cb72ff008d7ee0937a0b33f9abcf71ea0f`，状态为
  `VERIFIED_X1_TRANSPORT_CERTIFICATE`。它覆盖 15 个 named endpoints、全部
  `{24,25,26}` lambda、port/mask radix，并保持 owner-status 与 canonical
  invariance；仍只覆盖该 weight block。

- x0_named 的剩余权值块 `{19,34,35,36,37}` 也已在 Geo 完成冻结 v3 审计：
  artifact SHA-256 `66d863019664c4187c269fa8fce3d9abab9f21dc72799ad9e5dd89e7cd35c84a`，
  `global_raw_count=processed_raw=75`、`accepted_raw=canonical_count=0`、
  `sentinel_raw=75`，reason 为 `edge_weight_duplicate=30`、
  `pair_distance_duplicate=45`。普通 verifier 与修正版全流 replay 均返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_STREAM_REPLAY`；对应 owner-totality
  证书 SHA-256 为 `4051f36285f739c070b1c18015782d294de7840b5c93d116bd09521dd716db02`。
  这是 vacuous accepted-domain block，但完成了该 x0_named 权值集合的冻结覆盖。

- 已为 x0_named `{19,34,35,36,37}` 生成并验收 vacuous x0--x1 transport
  certificate，状态 `VERIFIED_X1_TRANSPORT_CERTIFICATE`。文件 SHA-256 为
  `95885013b36cddc9bac7414885985ac02f9cbd26140f000bb00f261b6ceeaaa6`，内部
  digest 为 `f24e118fb69789735014c3273e676e329408d3e82e587b55a575e14efc84453c`。
  该证书覆盖 15 endpoints、五个 invalid weight blocks，raw domain 与
  sentinel 计数均由 transport 保持。

- x0_named 全部 13 个 `H37_L` 权值块及 x1 transport 已冻结覆盖后，已在 Geo
  启动唯一剩余的 `m=2,e=1`, `anon_pair` 全权值分片：
  `lambda_values={5,16,18,19,20,21,24,25,26,34,35,36,37}`，输出
  `smoke/universal_low_m2_e1_anon_pair_all13_v3.json`，Python PID `2590234`。
  该任务完成后将执行普通 verifier、provenance-hardened 全流 replay，并据此
  生成 `m=2,e=1` 的 canonical/orbit merge 输入；当前仍在运行。

- GPT 顾问随后审计 replay 实现，确认核心 byte-stream 逻辑一致，但要求
  严格强制 lambda 按冻结 `H37_L` 顺序、拒绝非法 `endpoint_kind`，并校验
  fixed vertices/edges 与 all-ports/all-masks provenance。首轮匹配结果因此
  只作 preliminary；上述修正后的 replay 脚本 SHA-256 为
  `70e11acfa5d9b7a751172aec1e44b01056ec574dcab1e4dde0beb56326118c62`，已在
  Geo 通过 `py_compile` 并以 Python PID `2569991` 重跑，等待最终确认。

- 修正版 replay 已在 Geo 完成并通过，状态再次为
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_STREAM_REPLAY`；全部 digest、计数和
  sentinel reason 与源 artifact 完全匹配。修正版 replay 日志 SHA-256 为
  `72deecfd0a3c5ae0931d9fff40125ff9d26e307f02740802def59f4f606ea9d3`，
  runtime `3296.20s`。结构化 owner-totality 证书已更新为正式版本，SHA-256
  为 `3cde22a398792609e18551de30d4aa2996221cc26ede846dfb887e0764383794`，
  并固定 provenance-hardened replay 脚本 SHA
  `70e11acfa5d9b7a751172aec1e44b01056ec574dcab1e4dde0beb56326118c62`。
  因此 `{24,25,26}` 现在可标记为正式 owner-totality verified；仍不等于
  完整 frozen `m=2,e=1` merge 或全局结论。

- GPT-only audit of the pending merge found a remaining provenance asymmetry:
  frozen-v3 x0_named artifacts `{5,16}` and `{18,20,21}` have ordinary
  verifier results and x0--x1 transport certificates, but no formal
  provenance-hardened full-stream owner-replay certificate is present in the
  local results directory.  They therefore cannot yet be treated as
  equivalent to the formally replayed `{24,25,26}` and all-sentinel
  `{19,34,35,36,37}` blocks.  After the running anon_pair shard is independently
  replayed, the strict order is: replay `{5,16}` on Geo, replay `{18,20,21}` on
  Geo, recheck the common frozen schema/provenance, then validate that each
  x0--x1 transport source points to a full-stream-certified x0 block, and only
  then construct the `m=2,e=1` endpoint merge.  Until this chain passes, the
  state must not be labeled `VERIFIED_FROZEN_V3_M2_E1_OWNER_ORBIT_COVERAGE`.

- Geo 已完成 `anon_pair` 全 13 权重生成；本地保存的 artifact
  `results/pro_b27_universal_low_m2_e1_anon_pair_all13_geo_20260829_v3.json`
  SHA-256 为 `f9ef1476156c0870a47fd4cf20c1db3ec142fcecb1854759b5fa966909685791`。
  普通 frozen-v3 verifier（精确 `m=2,e=1, endpoint=anon_pair` 参数）通过：
  `global_raw_count=processed_raw=11010054`、`accepted_raw=11010048`、
  `canonical_count=5505024`、`orbit_sum=11010048`、`sentinel_raw=6`，
  sentinel reasons 为 `edge_weight_duplicate=3`、`pair_distance_duplicate=3`。
  provenance-hardened full-stream replay 已在 Geo 启动（PID `2605007`），
  尚未完成；在其通过前不得将该 shard 标为 replay-verified。

- 为解决旧 artifact 中 `ordering_version=null`、`semantic_input_hash=null` 的
  provenance 缺口，新增轻量脚本
  `theory-lab/topwindow/emit_pro_b27_v3_provenance_certificate.py`（仅元数据绑定，
  已通过 `py_compile`，不做枚举）。它固定排序定义
  `m-e-endpoint-H37-filtered-lambda-port-mask;sentinel-1-slot-v1`，并要求
  replay 与 artifact 的计数及两个 stream digest 完全一致。
  已为 `{24,25,26}` 与全 sentinel `{19,34,35,36,37}` 生成显式 provenance
  certificates；但完整 `m=2,e=1` merge 仍需 anon replay 以及 `{5,16}`、
  `{18,20,21}` replay 通过后才能进行。
  新证书文件 SHA-256 分别为 `{24,25,26}` 的
  `ca6245ddc29b2068af83a9576d1ee6600804651edff59607aefbc77726ff1d8b`，以及
  `{19,34,35,36,37}` 的
  `5189106523de27c64c6e6f03589e216bde2e4d3a7d90ddb0a57f26a9aeee0ce4`。
  两份证书共享 semantic base hash
  `a193611ae7d07201e6c9a7e8ecaa00870910cb0f0fb0a21d9e92bd950b65c4b1`；
  各自的 scope-specific semantic input hash 保留在证书内。

- Provenance emitter 的后续只读审计发现并修复了一个证书门槛缺口：此前
  `sentinel_reason_counts` 被写入证书但没有要求 replay 同值。现已将该字段
  纳入 artifact/replay equality gate，并额外固定 `endpoint_kind`、m/e/lambda
  scope 的合法性、去重性及冻结 H37 顺序；脚本仍仅作元数据校验，已通过
  `python3 -m py_compile`。两份既有 provenance certificate 已据此重生成，
  新 SHA-256 分别为 `e07dc469f72fff9358073fb8e6be3fd58678e99b28b8c402b17cd4e35fc7edb7`
  （`{24,25,26}`）和
  `fbe05fd1b79772cda1a7440eb482bfc13fe65d23c9847f34ee7726732d0043a6`
  （`{19,34,35,36,37}`）。这不会把 pending anon replay 或未 replay 的
  `{5,16}`、`{18,20,21}` 提前提升为 verified，也不会改变全局结论边界。

- Geo Workstation 已完成 anon_pair 全 13 权值的 provenance-hardened full-stream
  replay。独立结果为 `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_STREAM_REPLAY`，并与
  artifact 逐字段相等：`global_raw_count=processed_raw=11010054`、
  `accepted_raw=11010048`、`canonical_count=5505024`、`sentinel_raw=6`，
  reason 为 `edge_weight_duplicate=3`、`pair_distance_duplicate=3`；
  `raw_stream_sha256=b257bb191ef07fa39cb210096405361638c50c73de1e421774831b61ff9d0081`，
  `canonical_stream_sha256=46ddc225ad708807c8ebb8f195b02bd9483a4d37f5898be4f909d3d9435c40af`。
  replay log SHA-256 为
  `32264fba1cc32099a3d86af060017f1a73ea316e3b557b1514c16afe7e81a430`；正式
  provenance certificate SHA-256 为
  `a39a32c01e14f7cab5c50be1d2d07edf5c285be980f88524f91f50c21bf36964`。
  该 shard 现在可标记为 replay/provenance verified，但尚不等于完整
  `m=2,e=1` merge 或全局结论。

- 按严格顺序，Geo 已启动下一块 x0_named `{5,16}` 的 full-stream replay，使用
  artifact SHA-256 `f95ee4d194805d5485bef9a985085190dda685abbcf9fdaa983016baa63c8f19`
  和 replay script SHA-256
  `70e11acfa5d9b7a751172aec1e44b01056ec574dcab1e4dde0beb56326118c62`。
  首次启动因远程路径错误在 0.01 秒内退出；随后已用远程根目录中的正确脚本重启，
  当前外层 PID `2616971`，Python PID `2616973`，输出
  `smoke/universal_low_m2_e1_x0_named_5_16_v4.replay_retry1.log`，尚未完成。

- `{5,16}` replay 已在 Geo 完成并返回
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_STREAM_REPLAY`。artifact/replay 字段级
  完全相等：`global_raw_count=processed_raw=2621468`、
  `accepted_raw=canonical_count=2621440`、`sentinel_raw=28`，reason 为
  `edge_weight_duplicate=15`、`fixed_owner_reuse=4`、
  `pair_distance_duplicate=9`；`raw_stream_sha256` 为
  `378700af367736ab48dac1ad8a816f491149389da0638a59aba1eb0c8a11128a`，
  `canonical_stream_sha256` 为
  `e81bf3e3a5b73b09183ff88528fd446587d2f2a8db13204866a4cfe76a1f734d`。
  replay log SHA-256 为
  `790d0557ace5e5913ddb73e0b2fd95765eacb7ee5448808df1908cdb6cab5465`；
  按加强后的 provenance gate 生成的证书 SHA-256 为
  `de4a5d13c5ff7222f3c75d93d6cfbb0e3b14229459081aabe61d1af318868a6d`。
  因此 `{5,16}` 现在可标记为正式 replay/provenance verified source。

- 按严格顺序，Geo 已启动 x0_named `{18,20,21}` full-stream replay，使用
  artifact SHA-256 `26d7a84d53794a66588f9bada0e627433807a7a453bcc7be79f2e62cb1a99f89`
  和 replay script SHA-256
  `70e11acfa5d9b7a751172aec1e44b01056ec574dcab1e4dde0beb56326118c62`。
  当前外层 PID `2619331`，Python PID `2619333`，输出
  `smoke/universal_low_m2_e1_x0_named_18_20_21_v3.replay.log`，尚未完成。

- 在等待 `{18,20,21}` replay 期间做了轻量 transport provenance 审计：已有
  `{24,25,26}`、`{19,34,35,36,37}`、`{5,16}` 三个 x0→x1 transport 的
  `source_counts`、stream digests、scope 与各自 frozen x0 artifact 逐项匹配，
  且各自 provenance certificate 的 `artifact_sha256` 也匹配。它们可进入
  后续 merge 的 source 审计链；`{18,20,21}` transport 的 counts/digests
  也匹配 artifact，但仍等待该 block 的正式 provenance certificate，故暂不
  标记为完整 source-certified。

- 为满足 exact `m=2,e=1` merge 的最后逻辑前提，新增独立结构 verifier
  `theory-lab/topwindow/verify_pro_b27_anon_pair_stabilizer.py`。它不枚举状态，
  只验证冻结 `anon_pair` 域的唯一新增边为 `x0--x1`、匿名分量恰为
  `{x0,x1}`，且完整 marked state 的 rootward port 必为 `x0` 或 `x1`；匿名
  swap 必交换该 port，故 `fixed_point_count=0`、每个 S2 orbit 大小为 2。
  本机和 Geo Workstation 均通过 `py_compile` 与 verifier；verifier SHA-256
  为 `364ee3b65d88a65de39090b345d2853222ef9c6758c3d53fdd7af6708a6b6adb`，
  certificate SHA-256 为
  `8d1b482e03b1e630eedc2b385042aef9665bd3c1283a0d3153dcf80f340a1792`。
  该证书是结构性 stabilizer lemma，不把计数倍数反过来当作证明。

- 已新增元数据-only merge emitter
  `theory-lab/topwindow/merge_pro_b27_m2_e1_scope_certificate.py`（仅语法检查，
  未执行 merge）。它要求四个 x0_named lambda block 完整无重叠地分割 H37、
  每个 hardened provenance certificate 与 transport source_counts 相符、anon
  provenance certificate 到位、以及独立 stabilizer certificate 给出
  `fixed_point_count=0`；随后按已证 x0↔x1 transport 和 named/anon-anon-edge
  不变量计算 frozen `m=2,e=1` scope totals。该脚本不会把这些 totals 扩大为
  L-surjectivity 或全局非存在性结论。

- `{18,20,21}` 的 Geo full-stream replay 已完成并通过
  `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_STREAM_REPLAY`。artifact/replay 完全
  相等：`global_raw_count=processed_raw=11796515`、
  `accepted_raw=canonical_count=11796480`、`sentinel_raw=35`，reason 为
  `fixed_owner_reuse=8`、`pair_distance_duplicate=27`；
  `raw_stream_sha256=7f0a1921ee799d3c7cfcbc01fdb264ee4aa0c3497f9d3a33050220d1c69c57bb`，
  `canonical_stream_sha256=72a5b5315efa1f787a3c8a674549d48b0e95412d6af2a58832f2a804fed9dc5a`。
  replay log SHA-256 为
  `14c5e703fe380ad7929f9ca6da2bb899f95538c48ac8b3ac8be45138a761fa56`；
  hardened provenance certificate SHA-256 为
  `0602baac977dc3a6fb2615650818dff2864c2ac8275ea81010700c37e21a8bd5`。

- 在四个 x0_named hardened source certificates、四个 x0↔x1 transport、anon
  provenance certificate 和独立 anon-pair stabilizer certificate 均通过后，
  运行 metadata-only merge emitter
  `theory-lab/topwindow/merge_pro_b27_m2_e1_scope_certificate.py`，返回
  `VERIFIED_FROZEN_M2_E1_SCOPE_MERGE_CERTIFICATE`。merge certificate SHA-256
  为 `acd3addd60da8d84f4dbdcfa50ccf6afc75a9b2fa7b8be70b5f8daf4f6998800`；
  frozen scope totals 为 raw/processed `72352088`、accepted `72351744`、
  sentinel `344`、canonical union `36175872`，并满足 accepted = 2 ×
  canonical union。该结果严格限于声明的 `m=2,e=1`、H37、all ports/masks
  endpoint scope；不推出全局 L-surjectivity 或 Leech-tree 非存在性。

- 同一 `m=2,e=1` merge verifier 与全部小型输入已复制到 Geo Workstation 做
  跨环境复核；Geo 返回同一状态
  `VERIFIED_FROZEN_M2_E1_SCOPE_MERGE_CERTIFICATE`，同一 certificate SHA-256
  `acd3addd60da8d84f4dbdcfa50ccf6afc75a9b2fa7b8be70b5f8daf4f6998800`，且
  source artifact/certificate/transport/stabilizer SHA 列表逐项相同。至此，
  声明的 frozen `m=2,e=1` scope gate 已闭合（本地与 Geo 双环境）；它仍
  不涉及 `m=2,e=2`、`m=3`、high completion 或全局非存在性。

- frozen `m=2,e=1` 闭合后，下一研究层尚未启动；已向 GPT 顾问请求只读比较
  `m=3,e=0` 与 `m=2,e=2` 的价值、资源和最低验收合同。当前保持无并行远程
  枚举，等待该建议后再提交下一项 Geo 任务。

- frozen `m=2,e=1` merge certificate 已在本机与 Geo 双环境通过；随后按既有
  顾问建议选择下一高价值层 `m=3,e=0`，用于先闭合纯 S3 匿名轨道机制。Geo
  在启动前通过 generator `py_compile`，源码 SHA-256 为
  `d85477cbf156e1abdfa1e84559c03ec78443ce597143cdae3b5aa82e2739a5e6`；当前
  generator Python PID `2628692`（外层 `/usr/bin/time` PID `2628691`），
  输出 `smoke/universal_low_m3_e0_all_v3.json`，尚未完成。该任务是远程单任务，
  本机未运行枚举。

- `m=3,e=0` Geo generator 已完成，artifact SHA-256 为
  `6db04e4a29d311b0b5cfaa9062f15e0a67bf94c908d6814b1629ef08813f06df`；普通
  独立 verifier 返回 `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_SMOKE`，精确计数为
  `global_raw_count=processed_raw=accepted_raw=1572864`、
  `canonical_count=786432`、`sentinel_raw=0`，raw stream SHA-256
  `aede8b670a7877b526291e683a2cd70a8f30b120ba7db1b8e4a295b63aff338b`，
  canonical stream SHA-256
  `b2b42f7f3cdc1dca41845f646412ea7a6e67c3176b1309cb80896e223eb7eb65`。
  full-stream independent replay 已在 Geo 启动，外层 PID `2633466`、Python
  PID `2633468`，输出 `smoke/universal_low_m3_e0_all_v3.replay.log`，尚未完成；
  本机未做枚举。

- `m=3,e=0` Geo full-stream replay 已完成，并与生成 artifact 逐字段匹配；
  replay status 为 `VERIFIED_INDEPENDENT_UNIVERSAL_LOW_STREAM_REPLAY`。artifact
  SHA-256 为 `6db04e4a29d311b0b5cfaa9062f15e0a67bf94c908d6814b1629ef08813f06df`，
  replay log SHA-256 为 `354db198c658760d85370c4eea7dc225c266a228a482408fd867a27991dbf55b`。
  exact counts 为 raw/processed/accepted `1572864`、canonical `786432`、
  sentinel `0`；raw stream SHA-256 为
  `aede8b670a7877b526291e683a2cd70a8f30b120ba7db1b8e4a295b63aff338b`，
  canonical stream SHA-256 为
  `b2b42f7f3cdc1dca41845f646412ea7a6e67c3176b1309cb80896e223eb7eb65`。
  metadata-only hardened provenance certificate 已生成，status 为
  `VERIFIED_PROVENANCE_HARDENED_UNIVERSAL_LOW_STREAM_REPLAY`；其 SHA-256 为
  `044bac422a100f3376b07996a76fb7cb3ced6da02839f3d1e8d66f10a394f315`。

- 右侧 GPT 顾问在其 DevSpace 直接新增并完成轻量验收：
  `theory-lab/topwindow/verify_pro_b27_m3_e0_s3_orbit.py`、
  `theory-lab/topwindow/results/pro_b27_m3_e0_s3_orbit_certificate.json`、
  `docs/pro-b27-m3-e0-s3-orbit-and-m2-e2-contract.md`。主 verifier 当前 SHA-256
  为 `4a9e00c69b7aab90d3e03a84dfa2b97dde24000277e46d81e93628dcda979363`，
  certificate SHA-256 为 `044bac422a100f3376b07996a76fb7cb3ced6da02839f3d1e8d66f10a394f315`，
  status 为 `VERIFIED_M3_E0_S3_ORBIT_STABILIZER_CERTIFICATE`。结构性结论是：
  三个匿名 singleton 的 marked state 等价于 `S3` 作用在 `{0,1}^3` 的
  outward-mask bit-vector；fixed-side factor `F=196608`，Burnside 给出 4 个
  canonical anonymous patterns，轨道大小按 mask 中 1 的个数为 `1,3,3,1`，
  因而 raw/accepted `8F=1572864`、canonical `4F=786432`。该证书是
  S3 轨道/稳定子与 aggregate-count 定理，不把计数比值反过来当作证明。
  结合上面的独立 full-stream replay，声明的 `m=3,e=0` frozen low-slice gate
  已闭合；仍不推出 shared-owner `m=2,e=2`、high completion 或全局
  L-surjectivity/Leech-tree 非存在性。

- 右侧 GPT 顾问随后在 DevSpace 完成 `m=2,e=2` bounded shard planner：
  `theory-lab/topwindow/plan_pro_b27_m2_e2_shards.py`（SHA-256
  `e52f598c8c8df7af5d0bb0b5120a73eaf2bbc366659180fe97fa17e431d7876d`）与
  `docs/pro-b27-m2-e2-shard-plan-and-schema-audit.md`（SHA-256
  `1e74bf91e49b2f710f85f6d598a076983cb8bb8c4c647cdc1c29b5b75dceb6de`）。
  独立 `py_compile` 与 planner fixture 返回
  `VERIFIED_M2_E2_SHARD_PLAN_FIXTURE`。它确认现有 universal-low generator
  只物化一条新边，直接传 `e=2` 会 under-model，不能用于覆盖定理。
  完整 two-edge base 域为 31 条 admissible literal edges、465 个无序端点
  对、每对 13*12=156 个 ordered distinct 权值赋值，共 72,540 个 validity
  前 base descriptors；S2 endpoint 类型分割为 `30+210+15+210=465`。
  首个 Geo pilot 建议为 `E={x0-d6,x1-d6}`、权值 `(5,16)` 与 `(16,5)`；
  在 generalized two-edge generator 完成前不启动正式 e=2 coverage。

- 顾问随后扩展 pilot 的 base-validity-only 接口，加入 `--weights`、`--base-only`
  和 `--find-valid-candidates`。对固定 endpoint set
  `{d6-x0,d6-x1}` 排除 fixed literal edge weights 后，90 个 ordered distinct
  tuples 全部 invalid：49 个 `fixed_owner_reuse`、41 个
  `pair_distance_duplicate`，因此该 topology 没有 accepted candidate。Geo 已
  运行原始 `(5,16)/(16,5)` 两个 base，结果为 raw=2、sentinel=2、accepted=0，
  明确验证 two-edge materialization 与 sentinel accounting；这不是全域剪枝定理。
  下一候选筛选转向 `same_anon_two_named` 或 `cross_anon_distinct_named`，仍只做
  base-validity selection，找到候选后才在 Geo 展开 ports/masks。

- 顾问已将 pilot 扩展到 `same_anon_two_named_u_p_swap`，并在 Geo 完成
  x0/x1 twin。源端点为 `{u-x0,p-x0}`，twin 为 `{u-x1,p-x1}`，两者使用
  ordered weights `(5,20)`，各自 raw/processed/accepted/canonical 均为
  `1572864`，sentinel=0；两者 raw stream SHA-256 均为
  `36600fb2636548f3afe7d6e4d10ec487d54db96372e5908b420f5b0da4dd08ba`，
  canonical stream SHA-256 均为
  `555e1bd5f645636ba32538b11d3684837cadecee0e81ab0b8f4c45acc007395e`。
  `verify_pro_b27_m2_e2_swap_transport.py` 的 metadata-only certificate 返回
  `VERIFIED_M2_E2_SWAP_TRANSPORT_METADATA_CERTIFICATE`，源 artifact SHA 为
  `49949ab25ba77e91f4fa4c440438652eec854a2a70af2d89f2d556829c2d6faf`，twin
  artifact SHA 为 `9d9da277250a41e1fa6b7ba720d3a9042c5e5f153e0ad3990a7d81c7687d875c`。
  组件、port/mask 域、owner-status、权值绑定和 canonical stream identity
  均通过；但 comparator 只比较 metadata/commitments，不替代逐行
  independent replay，因此 pilot 的 hardened proof gate 仍待回放 checker。

- 顾问新增 `theory-lab/topwindow/verify_pro_b27_m2_e2_two_edge_stream_replay.py`
  （SHA-256 `0bb0e2a61ff80cbf32291f4a760fcb0ea6ac7c25877bab62790770c507b61797`），
  不导入 pilot generator，独立重建两条 literal edges、actual components、
  ports/masks、owner status、S2 canonical payload，并逐 flat row 重放 stream。
  source `{u-x0,p-x0}` 与 twin `{u-x1,p-x1}` 的 Geo replay 均返回
  `VERIFIED_INDEPENDENT_M2_E2_TWO_EDGE_STREAM_REPLAY`，`base_records_match=true`，
  raw/processed/accepted/canonical `1572864`、sentinel `0`，两个 stream digest
  均分别为 `36600fb2636548f3afe7d6e4d10ec487d54db96372e5908b420f5b0da4dd08ba`
  与 `555e1bd5f645636ba32538b11d3684837cadecee0e81ab0b8f4c45acc007395e`。

- 顾问新增 metadata-only emitter
  `theory-lab/topwindow/emit_pro_b27_m2_e2_pilot_merge_certificate.py`；本机与
  Geo 均返回 `VERIFIED_M2_E2_PILOT_PROVENANCE_MERGE_CERTIFICATE`，证书 SHA-256
  为 `df26f96cf215b315bd185eff82830ebc79b37d10f8085de94c45b9db73a2c568`。
  该 pilot gate 现在在 source/twin 独立 replay、S2 transport 和 provenance
  绑定下闭合，但严格限于两个 endpoint sets `{u-x0,p-x0}`、`{u-x1,p-x1}`
  与 weights `(5,20)`；不覆盖其余 463 个 endpoint sets、其它权值、全域
  `m=2,e=2` 或 L-surjectivity。

- 顾问新增全域 pre-validity base/index 层
  `theory-lab/topwindow/index_pro_b27_m2_e2_base_domain.py`（SHA-256
  `2faef70afd38e037ef88a170bfd748e2bcb0a1afdba5c4292abc86a24d4aad72`）。本机
  与 Geo fixture 均返回 `VERIFIED_M2_E2_BASE_INDEX_FIXTURE`，确认 31 条
  admissible literal edges、465 个 unordered endpoint sets、156 个 ordered
  distinct weight tuples、共 72,540 descriptors；endpoint 类型分割与 S2
  transport/rank-unrank 均通过。该层只定义 deterministic base domain，不
  materialize forests/ports/masks 或宣称全域 coverage。

- 顾问新增 generalized incidence runner
  `theory-lab/topwindow/run_pro_b27_m2_e2_incidence_shard.py`（SHA-256
  `2102a1274c77f727cf9725e10b79aea71dc4733c8ffcf4505db1c0e49a213da8`）与
  独立 replay checker
  `theory-lab/topwindow/verify_pro_b27_m2_e2_incidence_shard_replay.py`（SHA-256
  `73509a0d50aa37802703b399e275fa550324366a824b7f4c0085c3e6ed211821`）。
  它们均仅在本机 `py_compile`；Geo 运行单 descriptor shard
  `base_shard_index=61467, base_shard_count=72540`，runner status 为
  `VERIFIED_M2_E2_INCIDENCE_SHARD_GENERATOR`，独立 replay status 为
  `VERIFIED_INDEPENDENT_M2_E2_INCIDENCE_SHARD_STREAM_REPLAY`，并且
  `base_records_match=true`。artifact SHA-256 为
  `7f087da9726ddac774b557201eb9ab7d31616ba490b7959609ee9d29e60f4b2b`；
  exact raw/processed/accepted/canonical `1572864`、sentinel `0`；raw stream
  SHA-256 `36600fb2636548f3afe7d6e4d10ec487d54db96372e5908b420f5b0da4dd08ba`，
  canonical stream SHA-256
  `555e1bd5f645636ba32538b11d3684837cadecee0e81ab0b8f4c45acc007395e`。
  该闭环严格限于 rank 61467 的单 descriptor，不代表相邻 shard 或全域
  e=2 coverage。

- The single-descriptor provenance emitter was corrected for the replay summary
  schema: `base_records_match=true` is mandatory, while duplicated
  `replay.base_records` is optional and compared when present.  Local
  metadata-only emission returned
  `VERIFIED_M2_E2_SINGLE_DESCRIPTOR_SHARD_PROVENANCE_CERTIFICATE` for scope
  `[61467,61468)`.  The runner artifact SHA-256 is
  `7f087da9726ddac774b557201eb9ab7d31616ba490b7959609ee9d29e60f4b2b`, replay
  result SHA-256 `0f57b08ac770e97006fd6517cd7a040cfae51f420ab37923925fe317ba19816e5`,
  provenance payload SHA-256
  `62e49915b3eec854394f191e155a3061d58b6de8027d846b61cb63ca791db31d`, and
  certificate file SHA-256
  `9c4fbba07ee960a3f60c241d5e49116bbf191aa071ebea621095e9238332b8c1`.
  This is still strictly a single-descriptor provenance result.

- The right-side GPT consultant delivered the validity-only runner
  `theory-lab/topwindow/run_pro_b27_m2_e2_validity_shard.py` (SHA-256
  `8205fccda9e96d548b6334d454d9187bddc3614583f8fd7d0564587d7014b7be`), whose
  local fixture returned `VERIFIED_M2_E2_VALIDITY_ONLY_FIXTURE`.  It was copied
  to Geo and run on all 64 half-open shards of `[0,72540)`, with no
  incidence-row expansion.  The metadata-only merge script
  `theory-lab/topwindow/merge_pro_b27_m2_e2_validity_shards.py` (SHA-256
  `35cef14ed1ced112dcad3f89bba640b511d833fbfd61e4b5ae7271b98a586cbe`)
  returned `VERIFIED_M2_E2_VALIDITY_CENSUS_MERGE`: 680 valid bases, 71,860
  invalid bases; rejection counts cycle 12,480, edge-weight duplicate 25,410,
  fixed-owner reuse 6,241, pair-distance duplicate 27,729; estimated incidence
  workload 1,092,091,904 rows; maximum single-base estimate 2,359,296.  The
  merged artifact SHA-256 is
  `3d4a620b16ae6fc80288c88106e6d7023e74bc52bdf7eb04c6e7590136da498c`, with
  merge payload SHA-256
  `8ee646dcf15db200fbd460be7448c13f388d07032f08913eef1c1b115a753e2f`.
  This closes only the universal base-validity/workload census; it does not
  cover incidence rows, S2 orbit completeness, full L-surjectivity, high
  completion, or Leech-tree nonexistence.

- The consultant then extended the generalized incidence runner in place with a
  deterministic workload-plan/rank-list mode (new SHA-256
  `4737556e80f8ab2706a8f4de9584ee1c1e24fbcfb49ffcbc583aa6374b3a7ebe`).  The
  mode reads a verified workload plan and `--workload-shard-index`, rechecks
  every listed descriptor's validity, expands only those valid ranks, keeps
  continuous raw offsets in rank-list order, and requires actual block-size
  totals/maxima to equal the plan.  The original contiguous base-interval mode
  is preserved.  Local `py_compile` and the no-expansion workload fixture
  returned `VERIFIED_M2_E2_WORKLOAD_RUNNER_FIXTURE`.

- Geo has started the first 128-way workload shard (7 valid bases, planned
  `8,650,752` rows) as a single remote task for resource/stream validation;
  Python PID was `2654666` at the last check, with about 256 MB RSS and one CPU
  core, no error output, and no local incidence computation.  It has not yet
  completed, so no incidence-shard theorem status is assigned.  The remaining
  workload shards are intentionally not started until this gate is accepted.

- The consultant's metadata-only incidence workload planner
  `theory-lab/topwindow/plan_pro_b27_m2_e2_incidence_workload.py` (SHA-256
  `d0277e59b15ee8e86eece8a6c42edac2f781f14cdb56d36b7d5f98148880402b`) passed
  its local fixture and was run on Geo against the verified validity census.
  The 64-way plan returned `VERIFIED_M2_E2_INCIDENCE_WORKLOAD_PLAN` for all
  680 valid ranks, with total estimated workload `1092091904` rows and shard
  min/mean/max estimates `16515072 / 17063936 / 18874368`; plan payload SHA-256
  is `83bac7eadf6386eea91b46031e9762a8a80a35769d65894aa277cc8acf2a0f1a`.
  The 128-way plan was also generated (local copy SHA-256
  `582e15d04aae4339bbfb7cdb87e1a5da066f0ea09e10239ae5eb46996f4475c4`).
  The planner initially recorded that the old incidence runner could not
  consume valid-rank lists; the consultant has since added a rank-list-aware
  mode.  The first 128-way workload shard is now running on Geo under that
  mode.

- The consultant also delivered the independent workload-shard replay checker
  `theory-lab/topwindow/verify_pro_b27_m2_e2_workload_shard_replay.py` (SHA-256
  `42a5603f7f67011a01d7648f56efc08002b2e8fe6f81972a6190446471405aaa`).  Local
  `py_compile` and structural fixture returned
  `VERIFIED_M2_E2_WORKLOAD_REPLAY_STRUCTURAL_FIXTURE`; the checker is copied to
  Geo and ready to replay the first completed workload artifact.  It has not
  yet been run on a long stream.

- The consultant delivered a metadata-only workload-shard provenance emitter
  `theory-lab/topwindow/emit_pro_b27_m2_e2_workload_shard_provenance.py`
  (SHA-256 `359954f0fb1693bd0a9233eb165f31670883a88c3b24715feab20d1edd99558d`).
  Local `py_compile` and fixture returned
  `VERIFIED_M2_E2_WORKLOAD_SHARD_PROVENANCE_FIXTURE`; it is copied to Geo and
  will be used only after the first incidence artifact and independent replay
  exist.

- A read-only consultant audit of the current incidence hot path found it is
  single-core CPU-bound (`decode_ports_masks`, two S2 canonicalizations, JSON,
  and two hashes per row), with an observed planning envelope of roughly
  0.7--1.0 GB RSS per worker.  It recommends keeping the 128-way plan, waiting
  for the first shard's measured peak, and starting only 4--8 remote workers
  initially; no code change or new local computation was made from this audit.

- Latest Geo observation of the first workload shard: Python PID `2654666`
  remained running at about 14 minutes elapsed, one CPU core, RSS approximately
  680 MB, with no output/error file yet.  This remains within the provisional
  remote memory envelope; exact peak and elapsed time will be taken from the
  final `/usr/bin/time` record before choosing concurrency.

- Subsequent Geo checks show the same shard still running at about 20 minutes,
  one CPU core, RSS approximately 1.04 GB, with no artifact or error output.
  Because this exceeds the initial memory estimate, no additional incidence
  workers have been launched; the first shard remains the sole remote gate.

- Geo host resource check during this run reports 251 GiB total RAM, about 222
  GiB available, and 2 GiB swap (1.1 GiB used); the single worker remains the
  only incidence task.  The local machine is not used for this computation.

- The first Geo workload shard completed with status
  `VERIFIED_M2_E2_INCIDENCE_WORKLOAD_SHARD_GENERATOR`.  It covers exactly the
  seven planned valid ranks `[46515,46697,46698,46824,46827,46828,46829]` and
  reports raw/processed/accepted `8650752`, sentinel `0`, canonical count
  `8650752`; raw stream SHA-256
  `28ab1791221280772e83e3b18c33ac3fec334ee4f8a3b96c4597c456d6ff7341`,
  canonical stream SHA-256
  `5360876b0c37194d32a76e0e5b12df90f287965ef67b740048d0d310140d3f8b`, and
  artifact SHA-256
  `13e87ad362185b2213c6252e35b1e0950f027282e25555ec7d59aa94c16798c`.
  Geo `/usr/bin/time -p` reports real `1769.09` seconds (user `1758.76`, sys
  `9.51`).  An independent replay of this artifact is now running on Geo;
  until it matches, this is a generator result only and not a hardened proof
  gate.

- At the latest gate check the first Geo workload shard remained active at about
  27 minutes, one CPU core, RSS approximately 1.30 GB, with no artifact or
  error output.  Geo has ample host memory, but this measured envelope rules
  out speculative parallel launch until completion and replay.

- The consultant's read-only proof-gap audit identifies the first post-census
  structural obligation as a **low finite-scope coverage lemma**: every genuine
  order-25 FW319 branch must have its frozen-v3 low projection in an explicitly
  finite, declared `(m,e)` scope union, with endpoint types and owner/incidence
  data represented by the corresponding generators.  Current evidence does
  not prove that a genuine branch must have `(m,e)=(2,2)`; order-25 only gives a
  vertex-budget bound.  Thus even a complete `(2,2)` incidence census would not
  by itself establish global L-surjectivity, high completion, or nonexistence.
  The next minimal mathematical target is the anonymous low-component
  decomposition lemma and its explicit admissible-scope table; this audit was
  read-only and introduced no new computation.

- Latest Geo replay observation: PID `2663960` remained active at about 20.6
  minutes, one CPU core, RSS approximately 1.06 GB, with no replay JSON or
  error output.  It remains the sole incidence/replay task.

- The independent replay of workload shard 0 remains active on Geo; latest
  check is about 14.7 minutes elapsed, one CPU core, RSS approximately 706 MB,
  with no error output or replay artifact yet.  No other incidence shard has
  been started while this independent gate is pending.

- Latest replay check: Geo replay PID `2663960` remained active at about 18.5
  minutes, one CPU core, RSS approximately 985 MB, with no error output or
  replay JSON yet.  The first workload shard remains the only incidence task.

- The first 128-way workload shard's independent full-stream replay has now
  completed on Geo.  Replay status is
  `VERIFIED_INDEPENDENT_M2_E2_WORKLOAD_SHARD_STREAM_REPLAY`; it matches the
  artifact on all counts and stream digests: raw/processed/accepted
  `8650752`, sentinel `0`, canonical `8650752`, raw SHA-256
  `28ab1791221280772e83e3b18c33ac3fec334ee4f8a3b96c4597c456d6ff7341`, and
  canonical SHA-256
  `5360876b0c37194d32a76e0e5b12df90f287965ef67b740048d0d310140d3f8b`.
  The replay result SHA-256 is
  `6b099a39276668961b40e16866a6310827c312f0424c582c2ec589c4b85674c1`; Geo
  `/usr/bin/time -p` reports real `1748.69` seconds (user `1737.72`, sys
  `10.20`).  This closes the independent replay gate for exactly shard 0,
  not the global `(m,e)=(2,2)` incidence workload.

- The metadata-only workload-shard provenance emitter was then attempted and
  correctly refused to certify because the replay summary omits
  `indexer_sha256`, while the artifact binds indexer SHA-256
  `2faef70afd38e037ef88a170bfd748e2bcb0a1afdba5c4292abc86a24d4aad72`.
  This is a schema/metadata compatibility gap, not a replay failure.  No
  incidence job was restarted and no additional shard was launched; the
  minimal next action is to make the emitter/replay schema bind this field
  explicitly, then rerun only the metadata certificate.

- The compatibility fix was applied only to the metadata emitter
  `theory-lab/topwindow/emit_pro_b27_m2_e2_workload_shard_provenance.py`
  (SHA-256 `abb6b78b90e2e043083b1d7b12c8c1903904db74ba39846e5093813b04ccfd85`).
  It accepts the older replay schema only when the replay explicitly binds the
  artifact, plan, scope, index version, and base-record equality, and records
  `replay_indexer_binding` as an omission rather than silently claiming an
  explicit replay indexer hash.  Local `py_compile` and the structural fixture
  still pass.  The metadata-only certificate now succeeds on Geo with status
  `VERIFIED_M2_E2_WORKLOAD_SHARD_PROVENANCE_CERTIFICATE`; certificate SHA-256
  is `fa1303980ca26ed5d7c769219c7e9c8ae6485b65a7957825e7bc737541cb9af8`,
  provenance payload SHA-256 is
  `df137bc33572a2457b2d666a3a90c333a368438ef3f766068a928b448d8c0044`, and
  replay result SHA-256 remains
  `6b099a39276668961b40e16866a6310827c312f0424c582c2ec589c4b85674c1`.
  This closes the generator/replay/provenance chain for exactly workload shard
  0; it does not close the remaining 127 shards or any global L/high-scope
  theorem.

- After shard 0's generator/replay/provenance chain closed, Geo started only
  workload shard 1 (128-way plan): valid ranks
  `[46830,46831,46848,46850,46852]`, planned `7,864,320` incidence rows.
  The task runs remotely under `/usr/bin/time -p` with output
  `smoke/m2_e2_incidence_workload_128_shard1.json`; no local incidence process
  and no parallel shard were started.  The shard must pass independent replay
  and provenance before another shard is considered.

- Latest check of workload shard 1: Geo process `2674370` remains active at
  about 2.8 minutes, one CPU core, RSS approximately 155 MB, with no output or
  error file yet.  It remains the sole incidence process.

- Follow-up check: the same Geo process `2674370` remains active at about 4.2
  minutes, one CPU core, RSS approximately 207 MB, still with no final output
  or error file.  No replay or additional shard has been started.

- Latest check: Geo process `2674370` remains active at about 5.1 minutes, one
  CPU core, RSS approximately 274 MB, with no final output or error file.  It
  remains the sole incidence process.

- Latest check: Geo process `2674370` remains active at about 5.5 minutes, one
  CPU core, RSS approximately 291 MB, with no final output or error file.  It
  remains the sole incidence process.

- Latest check: Geo process `2674370` remains active at about 5.9 minutes, one
  CPU core, RSS approximately 303 MB, with no final output or error file.  It
  remains the sole incidence process.

- Latest check on the next day boundary: Geo process `2674370` remains active
  at about 6.5 minutes, one CPU core, RSS approximately 325 MB, with no final
  output or error file.  The job remains the sole incidence process and no
  replay has begun.

- Follow-up check: Geo process `2674370` remains active at about 6.8 minutes,
  one CPU core, RSS approximately 340 MB, with no final output or error file.
  The job remains the sole incidence process and no replay has begun.

- A provenance preflight during shard 1 confirms the local and Geo runner SHA
  are identical (`4737556e80f8ab2706a8f4de9584ee1c1e24fbcfb49ffcbc583aa6374b3a7ebe`)
  and the 128-way plan SHA is identical (`582e15d04aae4339bbfb7cdb87e1a5da066f0ea09e10239ae5eb46996f4475c4`).

- With shard 0's measured peak near 1.3 GB and Geo reporting ample free RAM,
  a second remote worker was started conservatively: workload shard 2, valid
  ranks `[46853,46854,46855,47136,47160,47946,48075]`, planned `8,388,608`
  rows.  Shards 1 and 2 are now the only incidence workers; each remains
  subject to independent replay and provenance, and no further shard will be
  launched until one of these gates closes.

- Immediate two-worker check: shard 1 PID `2674370` is at about 9.2 minutes,
  100% of one CPU, RSS approximately 495 MB; shard 2 PID `2677339` is at about
  0.6 minutes, 100% of one CPU, RSS approximately 47 MB.  Both output logs are
  still empty and no final artifact exists yet.

- Follow-up two-worker check: shard 1 is at about 9.8 minutes (RSS ~517 MB) and
  shard 2 at about 1.2 minutes (RSS ~77 MB), each using one CPU core.  Geo
  reports 214 GiB available RAM and no swap pressure change; both logs remain
  empty and no final artifacts exist.

- Latest shard 1 check: Geo process `2674370` remains active at about 7.9
  minutes, one CPU core, RSS approximately 381 MB, with no final output or
  error file.  The task remains the sole incidence process.

- Current remote gate check: Geo workload shard 1 PID `2674370` remains active
  at about 21.8 minutes (one CPU core, RSS approximately 1.10 GB), while shard
  2 PID `2677339` remains active at about 13.3 minutes (one CPU core, RSS
  approximately 645 MB).  Neither final artifact nor error output exists yet;
  both remote jobs are unchanged and no third shard, replay, or local heavy
  computation was started.

- Geo workload shard 1 generation completed.  The copied artifact
  `research/antimagic/smoke/m2_e2_incidence_workload_128_shard1.json` has SHA-256
  `1b6edc7deba66ad2b92d673aa011f88e834effb8dab0c4411c01870bc46f85be` and
  status `VERIFIED_M2_E2_INCIDENCE_WORKLOAD_SHARD_GENERATOR`.  Its declared
  scope is `(m,e)=(2,2)`, workload shard `1/128`, valid ranks
  `[46830,46831,46848,46850,46852]`; all five blocks have size `1,572,864`,
  giving raw/processed/accepted/canonical `7,864,320` and sentinel `0`.
  Raw stream SHA-256 is
  `1f63525bf2e0911efb5e991a8e65564e4092281bf636093987c54a10fae08628` and
  canonical stream SHA-256 is
  `58ee0bebf37f3df19511dd7b7c6fc37649e83c4dd256a1045fbc01f09e7af9cb`.
  The artifact was only schema-checked locally; no local stream replay was
  run.  Geo independent replay was launched as wrapper PID `2683337` (Python
  PID `2683339`) with output
  `m2_e2_incidence_workload_128_shard1.replay.json`; provenance awaits replay.

- Geo workload shard 2 generation completed.  The copied artifact
  `research/antimagic/smoke/m2_e2_incidence_workload_128_shard2.json` has
  SHA-256 `60f12f79912b893343b853a5baff9d2ffc6039748d26e98102315487f01fd107`,
  status `VERIFIED_M2_E2_INCIDENCE_WORKLOAD_SHARD_GENERATOR`, scope
  `(m,e)=(2,2)`, workload shard `2/128`, and valid ranks
  `[46853,46854,46855,47136,47160,47946,48075]`.  It reports raw/processed/
  accepted/canonical `8,388,608`, sentinel `0`, raw stream SHA-256
  `3df7b9cee2b161999b7610d2a61097b2330d5eea7d4631970a60c57609931203`, and
  canonical stream SHA-256
  `70a4a9b3fd52f46f9aa1c642a52f859bf933da5c7f11486a5e47c54e8d727ae2`.
  Its actual workloads are `[(46853,1572864),(46854,1572864),
  (46855,1572864),(47136,1048576),(47160,1048576),(47946,393216),
  (48075,1179648)]`.  Only lightweight local schema inspection was performed;
  Geo independent replay was launched as wrapper PID `2685955` with output
  `m2_e2_incidence_workload_128_shard2.replay.json`.

- Both shard 1 and shard 2 independent replays are now active on Geo (Python
  PIDs `2683339` and `2685957`, respectively).  Their replay logs remain empty
  while streaming; no replay artifact or provenance certificate exists yet.
  Geo has not been asked to start any additional incidence generation.

- Following the consultant's minimal-check recommendation, a metadata-only
  local audit decoded the 680 `valid_descriptor_ranks` from
  `m2_e2_validity_census_merge.json` through the frozen index (no incidence
  expansion).  Endpoint classes are mutually exclusive and exhaustive:
  `aa_plus_named=116`, `same_anon_two_named=120`,
  `cross_anon_same_named=44`, `cross_anon_distinct_named=400`, total `680`;
  all 680 ranks are unique.  The SHA-256 of the comma-joined sorted valid-rank
  list is
  `ba76716fc62ddda039e0f2402c7d0bd16ef1afd9a6cf6073947c66eb73afac75`.
  This validates only the endpoint-type interface inside the existing
  `(m,e)=(2,2)` validity census; it does not prove finite-scope coverage of
  genuine FW319 branches.

- Workload shard 1 generator/replay/provenance chain is closed.  The Geo
  independent replay has status
  `VERIFIED_INDEPENDENT_M2_E2_WORKLOAD_SHARD_STREAM_REPLAY`, with exact
  raw/processed/accepted/canonical counts `7,864,320`, sentinel `0`, and the
  artifact raw/canonical stream digests.  Replay JSON SHA-256 is
  `e37e0e96daf0ba64abb358505f7404535d5508c370606e64d7ea1115b7cd18e4`.
  The metadata certificate
  `research/antimagic/smoke/m2_e2_incidence_workload_128_shard1.provenance.json`
  has SHA-256
  `e30e36c6c6a5aff7768a7c12bd7c2bfcfe5756ba7de6076cd0d05dc030b26463`, status
  `VERIFIED_M2_E2_WORKLOAD_SHARD_PROVENANCE_CERTIFICATE`, provenance payload
  SHA-256 `fef27190349f9b3b171b204575d838f08471dc2e765c97b3434cd2e576dc179c`,
  and exact valid ranks `[46830,46831,46848,46850,46852]`.  The certificate
  remains scoped to shard 1 only and makes no global L-surjectivity or
  nonexistence claim.  Shard 2 replay remains active on Geo.

- Workload shard 2 generator/replay/provenance chain is now also closed.  Its
  independent replay has status
  `VERIFIED_INDEPENDENT_M2_E2_WORKLOAD_SHARD_STREAM_REPLAY`, matching the
  generator on raw/processed/accepted/canonical counts `8,388,608`, sentinel
  `0`, raw SHA-256
  `3df7b9cee2b161999b7610d2a61097b2330d5eea7d4631970a60c57609931203`, and
  canonical SHA-256
  `70a4a9b3fd52f46f9aa1c642a52f859bf933da5c7f11486a5e47c54e8d727ae2`.
  Replay JSON SHA-256 is
  `881d038f09ce5fad19187dc2ff2bfd25f5caa5f2947c6fba1a6b574da8076317`.
  The certificate
  `research/antimagic/smoke/m2_e2_incidence_workload_128_shard2.provenance.json`
  has SHA-256
  `4d033b51eada49c7d467f000b357bdf16cc604b7f9a8dd922e78425d2201b6f7`, status
  `VERIFIED_M2_E2_WORKLOAD_SHARD_PROVENANCE_CERTIFICATE`, provenance payload
  SHA-256 `e69fd8fb4b68fa5d463219b2b742fed247946fdb8adfc343904fb57b4bf01868`,
  and exact valid ranks `[46853,46854,46855,47136,47160,47946,48075]`.
  Together with shards 0 and 1, three workload shards are now independently
  closed; this remains only a finite `(m,e)=(2,2)` slice and not a global
  coverage or Leech-tree nonexistence theorem.

- Consultant structural audit, independently checked against
  `docs/pro-b27-bounded-ordered-outward-state.md`,
  `docs/pro-b27-branch-hypothesis-discharge-audit.md`, and
  `docs/pro-b27-complete-low-generator-spec.md`: conditional on the audited
  genuine `b=27`, J32-single-edge branch, the fixed connected packet `K` has
  15 vertices and the order-25 tree budget gives `m=|V(T)\\K|<=10`.  Since
  both `K` and `T` are trees and `K` is connected, exactly `m` edges lie outside
  `K`; hence the number `e` of new low edges obeys `e<=m<=10` (and therefore
  also `e<=13` from H37 injectivity).  Connectedness rules out an outside edge
  with both endpoints in `K`, so the only endpoint types are
  named--anonymous and anonymous--anonymous.  Together with branch-local H37
  saturation and fixed `32:NOT_L`, this yields the safe conditional scope cover
  `S_cover={(m,e):0<=m<=10,0<=e<=m}` of 66 pairs.  This is recorded as a
  branch-local reduction only; the remaining proof obligation is to show that
  the actual generalized frozen-v3 generator enumerates every legal
  `(E_new,lambda,Pi,O,omega)` state in all 66 scopes.  It does not certify
  global L-surjectivity, high completion, or Leech-tree nonexistence.

- Consultant implementation audit verdict: `GAP_IMPLEMENTATION_L_SURJECTIVITY`.
  The frozen-v3 specification has the required raw fields, and the current
  `(m,e)=(2,2)` path is exhaustive within its slice (endpoint sets, injective
  H37 assignments, components, ports, masks, owners, `32:NOT_L`, and S2
  canonicalization).  However, legacy
  `enumerate_pro_b27_universal_low_smoke_v5.py` remains structurally one-edge
  (`endpoint_candidates()` returns one pair and `base_blocks()` one lambda),
  while `index_pro_b27_m2_e2_base_domain.py` hard-codes `ANON=(x0,x1)` and two
  slots.  Therefore no implementation currently covers scopes such as
  `(3,1)` through `(10,10)`.  The owner path is slightly over-inclusive for
  5/21 alternatives and 34--37 geometry, requiring later filtering, but is
  not under-inclusive in the `(2,2)` path.  The smallest remaining technical
  bridge is a generic source-level encoder/index lemma: for every
  `(m,e) in S_cover`, enumerate every e-subset of `E_m`, every injective lambda
  into H37, materialize all e edges, derive `(Pi,O)` and owner paths, force
  `32=NOT_L`, and canonicalize under `S_m`, before any large run.  No new
  enumeration was started.

- The consultant added standalone
  `theory-lab/topwindow/index_pro_b27_generic_low_base_domain.py` without
  touching old slice scripts or artifacts.  Local SHA-256 is
  `f524f469461de1304eadb33c077122ede55e01c4b9b06444c6387f25fd201ebd`.
  Local `py_compile` plus `--fixture-only` both pass with status
  `VERIFIED_GENERIC_LOW_BASE_INDEX_STRUCTURAL_FIXTURE`.  The fixture covers
  all 66 `(m,e)` scope pairs, 176 rank/unrank probes, reproduces the closed
  m2e2 compatibility rank `61467` and `1,572,864` incidence rows, verifies
  shared `21` path `[16,5]`, fixed owner paths for 34--37, and a higher-scope
  probe `(m,e)=(4,3)` at rank `72,235,057`; it forces `owner_status[32]=NOT_L`.
  The generic raw base descriptor count is
  `18,298,578,200,827,934,714,091,749` (~1.83e25), so this is a source-level
  domain/encoding closure only.  No all-scope enumeration or S_m orbit
  certificate exists; the next gap is a sound compression/reduction or
  scalable canonical finite-search layer, plus later high completion.

- Consultant bounded compression-interface pilot (DevSpace, no incidence expansion):
  `theory-lab/topwindow/pilot_pro_b27_generic_m3_e1_weighted_base.py` and the
  independent checker
  `theory-lab/topwindow/verify_pro_b27_generic_m3_e1_weighted_base.py` were
  created and run on the complete `(m,e)=(3,1)` generic base domain.  The
  result artifact is
  `theory-lab/topwindow/results/pro_b27_generic_m3_e1_weighted_base_pilot.json`
  with SHA-256 `21b6192d371aa55738e0eae6bef73b895aa8e093e4f173b3fdc9b990bb9e7c`,
  and the independent verification artifact is
  `theory-lab/topwindow/results/pro_b27_generic_m3_e1_weighted_base_pilot_verification.json`.
  Exact bounded counts: 624 raw ranks, 99 valid, 525 rejected, 33 canonical
  weighted-base orbits, all orbit sizes 3 and stabilizer sizes 2, zero
  incidence rows expanded.  Rejection reasons are edge-weight duplicate 144,
  fixed-owner reuse 51, and pair-distance duplicate 330.
  The independent checker reports status
  `VERIFIED_INDEPENDENT_GENERIC_M3_E1_WEIGHTED_BASE_PILOT`, with all 624
  rank-by-rank classifications, rejection reasons, canonical key/member sets,
  orbit multiplicities, stabilizers, and metadata-only incidence counts
  matching.  This validates the bounded pre-incidence filtering and S3
  canonicalization interface only; it does not scale to all 66 scopes or prove
  the compression theorem, high completion, or Leech-tree nonexistence.

- Consultant bounded multi-edge compression pilot (DevSpace): the complete
  generic `(m,e)=(3,2)` domain has `C(48,2)*P(13,2)=175,968` raw bases;
  its controlled 300-second run did not finish and was stopped without a
  result claim.  A complete S3-invariant `same_named_two_spokes` subdomain was
  then run: one common named center, two of three anonymous leaves, and all
  `P(13,2)` ordered H37_L weights, for exactly `15*3*156=7,020` bases.
  Scripts are
  `theory-lab/topwindow/pilot_pro_b27_generic_m3_e2_same_named_two_spokes.py`
  (SHA `ebbbb97f61c7cbca759011d1706df24a600b77ca2b6c45f6f34ad63189517d22`)
  and its independent checker
  `theory-lab/topwindow/verify_pro_b27_generic_m3_e2_same_named_two_spokes.py`
  (SHA `1ec7df655c0b27294d115f8bb72b22756e359cdae8de747f4ce35781b41bb663`).
  The pilot and verification artifacts are
  `theory-lab/topwindow/results/pro_b27_generic_m3_e2_same_named_two_spokes_pilot.json`
  and
  `theory-lab/topwindow/results/pro_b27_generic_m3_e2_same_named_two_spokes_verification.json`.
  Exact result: 7,020 raw, 132 valid, 6,888 rejected; rejection reasons are
  edge-weight duplicate 2,970, fixed-owner reuse 693, and pair-distance
  duplicate 3,225; 22 canonical S3 orbits, each stabilizer 1 and orbit size 6;
  zero incidence rows.  Reference/staged classification agrees on all 7,020
  ranks, and the independent checker reports
  `VERIFIED_INDEPENDENT_GENERIC_M3_E2_SAME_NAMED_TWO_SPOKES_PILOT` with zero
  mismatches.  This extends the interface evidence to genuine multi-edge
  interactions but remains only one subdomain: full m3e2, all 66 scopes,
  incidence-orbit compression, high completion, and global nonexistence remain
  open.  Full details are in
  `docs/checkpoint-2026-08-30-generic-m3-e2-multiedge-compression-pilot.md`.

- Consultant shared-anonymous endpoint pilot (DevSpace): fixed named pair
  `(u,p)`, shared anonymous endpoint `x_i`, edges `u-x_i` and `p-x_i`, all
  `i=0,1,2` and all ordered injective H37_L weight pairs, gives the complete
  S3-invariant subdomain of exactly `3*P(13,2)=468` weighted bases.  Pilot
  script SHA is `f4d6aafefc277e2644b993109e72076aaa8bdef609a16918ced339a75cd52b62`;
  independent checker SHA is
  `d3fb62c2a6b83b76ae6c8c17b3853dfed4aeb78898943ed056f1298cf7b90983`.
  Result artifacts are
  `theory-lab/topwindow/results/pro_b27_generic_m3_e2_same_anon_two_fixed_named_pair_pilot.json`
  and its `_verification.json` companion.  Exact result: 468 raw, 33 valid,
  435 rejected (`edge_weight_duplicate=198`, `pair_distance_duplicate=237`),
  11 canonical S3 orbits, all stabilizer 2 and orbit size 3, zero incidence
  rows.  The independent checker reconstructed all 468 ranks and matched
  rejection reasons, canonical keys, orbit ledger, stabilizers, and incidence
  metadata with zero mismatch.  Statuses are
  `VERIFIED_GENERIC_M3_E2_SAME_ANON_TWO_FIXED_NAMED_PAIR_PILOT` and
  `VERIFIED_INDEPENDENT_GENERIC_M3_E2_SAME_ANON_TWO_FIXED_NAMED_PAIR_PILOT`.
  Full details are in
  `docs/checkpoint-2026-08-30-generic-m3-e2-same-anon-two-fixed-named-pair.md`.
  This broadens multi-edge evidence to the shared-anonymous endpoint class only;
  the full m3e2 domain, all 66 scopes, incidence-orbit compression, high
  completion, and global nonexistence remain open.

- Consultant source-level canonical-augmentation contract (DevSpace): added
  `docs/pro-b27-sm-equivariant-canonical-augmentation-contract.md` (SHA
  `feaa8a68226aefe6c2bee846abdd1a5bb03864822749ae8e3f715a62f97a0049`) and
  independent structural fixture
  `theory-lab/topwindow/verify_pro_b27_sm_equivariant_canonical_augmentation.py`
  (SHA `a6631ca75ef460e4026b5b3505203d0bee91465f3d41795e96c8389f0ba56431`).
  Fixture artifact
  `theory-lab/topwindow/results/pro_b27_sm_equivariant_canonical_augmentation_fixture.json`
  has SHA `046a210d6459bba4e5205ee7cf4ddb33fa93f2c9b9ea7126adc6e0a956d88537`.
  Status `VERIFIED_SM_EQUIVARIANT_CANONICAL_AUGMENTATION_FIXTURE`: checks
  canonical idempotence and orbit invariance, orbit-stabilizer identity,
  canonical-parent gate, filter and owner-status equivariance, two monotone
  rejection extensions, and the rule that a fixed base's incidence fiber is
  quotiented only by `Stab(B)`; 8 representative states, 6 permutations each,
  zero incidence rows.  The document explicitly records the remaining load-
  bearing gap: proving that every genuine encoded base in all 66 scopes has an
  accepted canonical-augmentation path and that the practical generator
  enumerates every required parent orbit.  It does not claim all-scope
  surjectivity, high completion, or nonexistence.

- Consultant extension-transversal gap fixture (DevSpace): validated the
  smallest fixed-parent symmetry failure mode.  The checker
  `theory-lab/topwindow/verify_pro_b27_all66_extension_transversal_gap.py`
  (SHA-256
  `b5458c7bc2d60f693ee5666373c2796cbd788084871b2bfe52174f1cfc761296`)
  and result
  `theory-lab/topwindow/results/pro_b27_all66_extension_transversal_gap_fixture.json`
  (SHA-256
  `6bbd9108b062857d11efea4c6cb23c12e6e8b7c03158ff489b05054fabed716c`)
  were run in DevSpace with `py_compile` and `--fixture-only`; both exited 0.
  Status `VERIFIED_ALL66_EXTENSION_TRANSVERSAL_GAP_FIXTURE`: for
  `P={u-x0=5}` at `m=3`, `|Stab(P)|=2`, the three `p-x_i=20` candidates form
  one full-S3 orbit but two `Stab(P)` orbits of sizes 1 and 2, with the known
  valid child in the singleton orbit.  This verifies only the local
  symmetry/interface obstruction (incidence rows 0); it does not prove the
  complete extension universe, all-66 coverage, high completion, or
  Leech-tree nonexistence.

- Pro-level extension-transversal lemma audit (DevSpace): added
  `docs/pro-b27-extension-transversal-lemma-audit.md` (SHA-256
  `3ceedc5f183ed684310eb89dfa9c9c963b1c3091ca1b333e467ad49ef17952d1`).
  The audit gives a rigorous conditional induction: deletion-heredity and
  `S_m` transport guarantee a legal canonical parent for every accepted
  weighted-base child; if a generator exposes the complete
  `U_raw(P)` and one representative from every exact `Stab(P)` orbit, then
  it reaches exactly one canonical representative at every depth for each
  fixed `m`, and all 66 roots require separate instantiation.  It also
  verifies that the current fixed-depth rank/unrank indexer does not expose
  that parent-conditioned total interface.  Status remains CONDITIONAL/OPEN:
  the extension-transversal premise, incidence quotient, high completion, and
  global nonexistence are not proved.

- Remote Geo Workstation interface validation (2026-08-30): copied the
  isolated reference module and interface note to
  `/home/geo/codex-work/leech-trees/remote_scratch/extension_orbit_interface_20260830`
  and ran only tiny remote checks (no local Python).  For canonical `m=3`
  parent `{u-x0=5}`, the result was `endpoint_count=48`, `raw_count=564`,
  `stabilizer_size=2`, `orbit_count=372`, with pairwise-disjoint orbits,
  exact raw-universe coverage, and one representative per orbit.  For the
  canonicalized two-edge parent `{u-x0=20,u-x1=5}`, the result was
  `raw_count=506`, `stabilizer_size=1`, `orbit_count=506`, with the same exact
  checks.  A deliberate noncanonical input was rejected by the module's
  precondition.  These are tiny runtime checks of the reference interface
  only; they do not certify all-66 traversal or global nonexistence.

- Canonical traversal shard checkpoint (Geo Workstation, 2026-08-30): the Pro
  consultant added `theory-lab/topwindow/pro_b27_canonical_traversal_shard.py`
  (SHA-256 `f712825aa22780969f4ff43cfa75c770d9d420775d0a92f77b0837d0706d88da`)
  and `docs/pro-b27-canonical-traversal-shard-contract.md` (SHA-256
  `c6365c272542d6c4a6a92af1e59306f8ece69dd4ce7f194d7edd5f0e67adb13f`).  The
  runner is weighted-base only, uses exact parent-conditioned `Stab(P)`
  transversals and deterministic half-open parent shards, and does not enumerate
  ports, masks, incidence or high completion.  On Geo, the unsharded `m=3,
  parent depth=1` gate completed with status
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS`, global parent
  count 33, parent interval `[0,33)`, and 503 unique emitted child orbits.
  Artifact SHA-256: `d6a4656eaef54b270f14825600347c4c8390b296677ae334c6f65b425f9eca9b`
  under `remote_scratch/canonical_traversal_shard_20260830/.../results/` on Geo.
  This is an internal generator certificate only; independent replay/merge,
  all-66 coverage, incidence/high obligations, and global nonexistence remain
  open.

- Independent Geo replay of the canonical shard (2026-08-30): the Pro
  consultant added `theory-lab/topwindow/verify_pro_b27_canonical_traversal_shard.py`
  (SHA-256 `ce29713ec70464097cb659727294cd8b63ad5c3a1cf6edee1045cb5051a3da07`).
  The first replay exposed and the consultant corrected a schema mismatch
  (the generator has no invented top-level `filter_profile` field).  The
  corrected checker independently rebuilt all prefix levels, recomputed the
  half-open interval, reimplemented the exact extension orbit partition and
  weighted-base validity/gate checks, and matched the generator artifact on
  Geo with status `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.
  It matched 33 selected parents and 503 child orbits.  Verification artifact:
  `/home/geo/codex-work/leech-trees/remote_scratch/canonical_traversal_shard_20260830/theory-lab/topwindow/results/pro_b27_canonical_traversal_m3_d1_0_of_1.independent_verification.json`
  (SHA-256
  `691c779d78f0585ab969dad51df5854b2d4d000ac1b38edf67a6d934c3956763`;
  verification payload SHA-256
  `9697fcc40698e1310498cbc91db6527037a94eb41da8aa21cf8d8000bd20efac`).
  This closes only the fixed `m=3, depth=1` weighted-base shard replay gate;
  shard merge, depth-2/all-66 coverage, incidence/high completion, and global
  nonexistence remain open.

- v2 parent-layer binding and depth-2 probe (Geo Workstation, 2026-08-30):
  the runner now has SHA-256
  `466ce529e85dca803de77980cf2c99ecf92afa6091fc526c656df4e48322441b`,
  requires `--parent-layer` for depth>=2, and emits complete
  `child_layer_bases`.  The independent checker is
  `378c0bb30695eaf64e2c9a68a5ec70d94acfa6e28fae267309bfd8011fb2fec2`; the
  merge utility is
  `6c4129e2de6bdd78cf26769c8f31aefe3df8a240de90fafe9654d6f074dccf12`.
  The v2 `m=3, depth=1` shard was independently replayed and merged on Geo:
  generator artifact SHA `39bad2193bf9cc77367e68cf6494add600babe312c600e13fdd6c1fbbbc790e2`,
  replay SHA `07bf106b479ef4e73e6e4d3dcfbcb1cc7db76fcff54aa4486ae34931de4be136`,
  merge status `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_LAYER_MERGE`, 503 parent
  bases, layer SHA `dcba0b754cc3fc45954a96a840c72d97ecf9211591fdcf84c3e777ecaa4d7d85`.
  Using that verified layer, only shard `0/16` of `m=3, depth=2` was run and
  independently replayed: 31 selected parents, 130 child orbits, generator
  SHA `3f48f4c128a9f948852942ac647166615432d395bef2737b3639ddf0de8fb4d6`,
  replay SHA `24ebdda7f3b7575c376a9109289569bc000f9a01ea99998480d7e30bea4dc2c0`.
  The remaining 15 depth-2 shards, their merge, all-66 coverage, and
  incidence/high obligations remain open.

- Complete depth-2 canonical traversal layer (Geo Workstation, 2026-08-30):
  all 16 deterministic shards over the verified `m=3, depth=1` parent layer
  completed with generator status
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS` and matching
  independent replay status
  `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.  The 16 shard
  files cover the half-open parent intervals `[0,503)` exactly; remote
  completeness checks found 16 generator and 16 replay artifacts.  The
  metadata merge passed with status
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_LAYER_MERGE`, 2,293 canonical child
  bases, ordered digest
  `0979132fafa874256ad26eef7c86ccbed2171055c846c72c93556ddfa2704963`,
  canonical-bases SHA-256
  `8cbe4d7cbfd676d1564e341faf61d85594bd7c657c8a3c63386618268b91b325`, and
  layer artifact SHA-256
  `139ad0bfb3eaa8d21e183615535738ee2b7703c26213a84e41b86addf18149f9`.
  This closes only the fixed `m=3`, depth-2 weighted-base traversal layer;
  depth-3 terminal handling, all-66 coverage, incidence/outward-mask
  obligations, high completion, and global Leech-tree nonexistence remain
  open.

- Terminal depth-3 closure for the fixed `m=3` layer (Geo Workstation,
  2026-08-30): consumed the verified depth-2 merge layer and ran one
  unsharded terminal shard over all 2,293 parents.  Generator artifact
  SHA-256 `a95fd3cf2bcac6d9006d8a7cedd9bdedced2725df83e346dcfefbbf6c5bee3d5`
  returned internal status
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS`; its scope is
  `m=3, parent_depth=3, child_depth=null`, interval `[0,2293)`, and all
  aggregate candidate/orbit/gate counts are zero with an empty child ledger
  (SHA-256 `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`).
  Independent replay artifact SHA-256
  `a4abdd95bf38a9e5a8694cd4317f2852c3eabb037089530544d2c4e8a9d857a1`
  returned status `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.
  This closes the weighted-base traversal chain for `m=3, e=0,1,2,3` only;
  incidence/high obligations, all-66 coverage, and global nonexistence remain
  open.

- Fine-sharded `m=4, depth=3` probe (Geo Workstation, 2026-08-30): the prior
  16-way shard 0 exceeded 180 s, but increasing to 64 parent shards completed
  shard 0 in 89.6 s and shards 1--4 sequentially thereafter, each with
  independent replay.  The five verified shards cover `[0,297)` of the 3,803
  depth-3 parents and emit 413 child orbits in total; all five generator
  artifacts have status
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS` and all five
  replays have status
  `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.  Shard-0
  generator SHA-256 is
  `f8d844362996f8c4ae2ae31fdda2c11653369845049ad48e8bd918d140e569f6` and its
  replay SHA-256 is
  `573c421e2f4412e3f75799e7d27058200792ec001007da3df17a013e4c32dd66`.
  This establishes that finer sharding is viable, but it is only 5/64 of the
  depth-3 layer; the remaining shards, depth-4 terminal layer, all-66
  coverage, incidence/high obligations, and global nonexistence remain open.

- Fixed `m=4` depth-1 and depth-2 traversal (Geo Workstation, 2026-08-30):
  the root-based depth-1 shard covered `[0,33)` with 524 child orbits and
  passed independent replay; generator SHA-256
  `fed5d769f2818bb8aa97f3ee1c8333e29955ac9b150f29b6c9be236508a7adca`, replay
  SHA-256 `ef79105507637ce60b80cba2f5b62630c287dbdc59db280d118cd8fdf0f8846e`,
  and one-shard layer merge SHA-256
  `630d359b1e7756464f8d675127f90209135a6080ac481fb55558826e59b6d8b8`.
  The resulting 524-parent layer was traversed at depth 2 in all 16 exact
  shards, each independently replayed; total emitted child bases were 3,803.
  The merged depth-2 layer has ordered digest
  `116106efd26272f1ae70b9ebec239c99cdb0a461755c7428ceda43e258000bdc`,
  canonical-bases SHA-256
  `a52bf2e9625aed826183864cf3e6d3a779a6e6d09d3c4d294599bff17fbf0aa4`, and
  layer artifact SHA-256
  `b22486d8379e4e38e090c0877c42ebced65bb56cf70dbf519807d8c7fbd22610`.
  A bounded `m=4, depth=3, shard 0/16` probe was stopped by its 180 s
  timeout (exit 124) without a complete artifact; no depth-3 claim or retry
  is made.  Incidence/high obligations, all-66 coverage, and global
  nonexistence remain open.

- Fixed `m=2` weighted-base traversal chain (Geo Workstation, 2026-08-30):
  root-based depth 1 completed and independently replayed with 33 parents and
  340 child orbits; its one-shard merge passed with 340 canonical bases,
  ordered digest
  `47a2e15600a1d8d8c95f79a2ad47b28ee92c3ba56021f8461e129f91f67f55f6`, and
  canonical-bases SHA-256
  `0036ab3430f654e0ef4d99405c977adbb62eb5f8510474622c66f2b5181dfc9c`.
  Consuming that layer, the terminal depth-2 shard covered `[0,340)` with
  zero raw extensions, zero candidate/orbit/gate counts, and an empty child
  ledger.  Generator artifact SHA-256
  `6d4ff9620b6990fb30e93349fc9467cf5a61082807532e3b0e0f4586f1ae54aa` and
  independent replay SHA-256
  `b57ab8f47cf8620fcf4289c415e522279a5b0e7e04c71830806a9c3043c01c3c`
  returned the expected verified statuses.  This closes only the fixed
  `m=2` weighted-base traversal chain; incidence/high obligations, all-66
  coverage, and global nonexistence remain open.

- Low-`m` completion (Geo Workstation, 2026-08-30): `m=1, depth=1` terminal
  shard covered `[0,26)` with zero extensions and empty child ledger; generator
  SHA-256 `a0bedfb55db982b0aa8501b0981c92c7b5bda6005eb27d1133d77023d9c71a16`
  and independent replay SHA-256
  `dc29ae0df6c5662941189a2c62112720574cca6099a58b8e37a5a38cad21a147`
  returned the expected verified statuses.  The trivial `m=0, depth=0` shard
  likewise covered `[0,1)` with zero extensions; generator SHA-256
  `c4b3585e429b9c2e6b39d0be2e42891fc8484e63f0aff828fcca78d440696694` and
  replay SHA-256
  `f35984da9fd1f3c0970b3964ddfe17599faaf5d5b98a1a9ae4ec170c4ee295ed`
  passed.  These close only the fixed `m=0` and `m=1` weighted-base scopes;
  incidence/high obligations, all-66 coverage, and global nonexistence remain
  open.

- Fine-sharded `m=4, depth=3` continuation (Geo Workstation, 2026-08-30):
  64-way shards 5--8 completed sequentially with generator internal checks and
  independent replay.  Together with shards 0--4, the verified prefix now
  covers parent indices `[0,534)` of the 3,803 depth-3 parents (9/64 shards)
  and emits 647 depth-4 child orbits.  The per-shard child-orbit counts are
  `21,92,83,42,175,129,47,39,19`; every generator returned
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS` and every replay
  returned `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.  The
  newly completed shards have replay artifact SHA-256 values
  `51001a8b47917a9adc6143ead59b8fe3781ed1948c7b647aa0e0612b3bed0fa9`
  (shard 6),
  `752d982649b7fea90bc5e5493299d1e014af19998f9e848191b9b04ae1cdd169`
  (shard 7), and
  `6941fb60057621392a3ed30d52bafbf1c945974448e1f45b41ec068477855e48`
  (shard 8).  This remains a partial weighted-base layer only; all remaining
  depth-3 shards, the depth-4 merge/terminal run, all-66 coverage,
  incidence/high obligations, and global nonexistence remain open.

- Subsequent `m=4, depth=3` shard (Geo Workstation, 2026-08-30): shard 9/64
  independently passed after generator-first execution.  It covers
  `[534,594)` (60 parents), has exactly 37,800 raw extensions and 39 emitted
  child orbits.  Generator status is
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS` and replay
  status is `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.
  Generator artifact SHA-256 is
  `74a8336dcd8b5e2712188ed5a1d0438cf22f3be3b76557db038b9d6c628fbf62` and
  independent replay SHA-256 is
  `af0e328378b4df4e2b60a44b1be88e32fb932139c0c5a13ddb924f8d196ea3db`.
  The verified prefix is therefore 10/64, covering `[0,594)` and 686 child
  orbits in total; shards 10--63 and the subsequent merge/terminal steps
  remain open.

- Further `m=4, depth=3` continuation (Geo Workstation, 2026-08-30): shards
  10--12/64 completed sequentially with independent replay.  Shard 10 covers
  `[594,653)` (59 parents), 37,170 raw extensions and 24 child orbits; its
  generator/replay artifact SHAs are
  `e8bce85a3c7d61b0542ff23ca7a6ed825cdab4cca0eead3548f06b0087c16a45` and
  `55270d0f55de7253cef765757cb0807c61260c0fb284ebf6ef19edf957056c41`.
  Shard 11 covers `[653,713)` (60 parents), 37,800 raw extensions and 14
  child orbits; SHAs are
  `b6cfd1a13d62dd8e88d8b3e74461ee01f4dfda44a1aacfadffba00aa0426716a` and
  `f48ec6c299a205a33205d36648c6afbadfdf78b8b822f9f8492b636abac5898e`.
  Shard 12 covers `[713,772)` (59 parents), 37,170 raw extensions and 10
  child orbits; SHAs are
  `adb3faa3d03c0bcaf85d68762d3eb4cb9e470c8ea89e0ce928de3d87e595ec8e` and
  `6a7c3854a5fb402a62436b02ee376f4b4021b53fac2279fa7455a57e8d3e461b`.
  All six generator/replay statuses are the expected verified statuses.  The
  cumulative verified prefix is now 13/64, covering `[0,772)` with 772
  parents, 486,360 raw extensions and 734 child orbits; shards 13--63 and
  the later merge/terminal obligations remain open.  The consultant's
  non-authoritative execution record is
  `docs/scratch-pro-b27-m4-depth3-shards-9-12-20260830.md` (SHA-256
  `f9bac7c7ef4d55fe26b29ed957fdda61fab632bdc9566f3dce66f0aace8a4800`).

- Shard 13 continuation (Geo Workstation, 2026-08-30): the consultant's
  generator artifact for `m=4, depth=3, shard=13/64` was independently replayed
  after the browser turn failed.  The shard covers `[772,831)` (59 parents),
  has 37,170 raw extensions and 92 child orbits.  Generator status is
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS`; replay status
  is `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.  Artifact SHA-256
  is `e721b5485743237c820439b26cae7b45c75beb87a488610c450988ae27f22307` and
  independent replay SHA-256 is
  `a3267675182a22e30ea8d8f17cb80051c59e9f52c4a5e11ee3e71922fce9609b`.
  The verified prefix is now 14/64, covering `[0,831)` with 831 parents,
  523,530 raw extensions and 826 child orbits; shards 14--63 and all later
  merge/terminal obligations remain open.

- Shard 14 continuation (Geo Workstation, 2026-08-30): after a `jq`-only
  preflight error, the existing generator artifact was replayed directly by
  the consultant and passed independent verification.  It covers `[831,891)`
  (60 parents), with 37,800 raw extensions and 154 child orbits.  Generator
  status is `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS` and
  replay status is `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`.
  Artifact SHA-256 is
  `7724b26c4a1c0cb7c9a3e8cb09578f01e0acf79449599002f1c4322a12bfc061` and
  independent replay SHA-256 is
  `2f95d128089b57a14711a7f5441674c84480ab71ddd8400f42e27b6b1326c020`.
  The verified prefix is now 15/64, covering `[0,891)` with 891 parents,
  561,330 raw extensions and 980 child orbits; shards 15--63 and all later
  merge/terminal obligations remain open.

- Shard 15 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay both passed for `m=4, depth=3, shard=15/64`.  The shard
  covers `[891,950)` (59 parents), has 37,170 raw extensions and 111 child
  orbits.  Artifact SHA-256 is
  `9d3444e41c6059baddd45412eb2311a03d8aa351a02dd89390e740f13ee4403e` and
  independent replay SHA-256 is
  `20e1bdef4667b3ae52a51fc26291fa7ac09c35a5309944ab2e1fe41305b42916`.
  The verified prefix is now 16/64, covering `[0,950)` with 950 parents,
  598,500 raw extensions and 1,091 child orbits; shards 16--63 and all later
  merge/terminal obligations remain open.

- Shard 16 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=16/64`.  The shard covers
  `[950,1010)` (60 parents), with 37,800 raw extensions and 198 child orbits.
  Artifact SHA-256 is
  `39603460e263fd8e3dbe4dfa883d1484df9e811179ad2133ebe97ff1f64fe660` and
  independent replay SHA-256 is
  `032b7aacadf7c1f445c10d8c333ce62de290cc06025285c4cc48c1276c1f0220`.
  The verified prefix is now 17/64, covering `[0,1010)` with 1,010 parents,
  636,300 raw extensions and 1,289 child orbits; shards 17--63 and all later
  merge/terminal obligations remain open.

- Shard 17 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=17/64`.  The shard covers
  `[1010,1069)` (59 parents), with 37,170 raw extensions and 235 child
  orbits.  Artifact SHA-256 is
  `1bb7c2bee83f75184a4e3c993b76ba705fe7e24a0cfd978940f4ba5146b75f38` and
  independent replay SHA-256 is
  `36cb366422de686896055ea7bfd4ada48d884913ecd739127ff821d7c9fc30f0`.
  The verified prefix is now 18/64, covering `[0,1069)` with 1,069 parents,
  673,470 raw extensions and 1,524 child orbits; shards 18--63 and all later
  merge/terminal obligations remain open.

- Shard 18 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=18/64`.  The shard covers
  `[1069,1129)` (60 parents), with 37,800 raw extensions and 137 child
  orbits.  Artifact SHA-256 is
  `d71aa8550ccf21f471530d0ab12604ca2089df1336c795289f75fab2c1a91e4f` and
  independent replay SHA-256 is
  `e514dfd9238a38b6c7cfe90a896c566c4d96c6410de5595ca0668eebdc1e8433`.
  The verified prefix is now 19/64, covering `[0,1129)` with 1,129 parents,
  711,270 raw extensions and 1,661 child orbits; shards 19--63 and all later
  merge/terminal obligations remain open.

- Shard 19 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=19/64`.  The shard covers
  `[1129,1188)` (59 parents), with 37,170 raw extensions and 88 child
  orbits.  Artifact SHA-256 is
  `0cd932229443b51d20d7c40134e0febb305529b1e01b78be41d2249d96d5a93b` and
  independent replay SHA-256 is
  `c22aea908ce182a156456e874076cc85eec5f6205f1c7d85d4d1ac9646799e46`.
  The verified prefix is now 20/64, covering `[0,1188)` with 1,188 parents,
  748,440 raw extensions and 1,749 child orbits; shards 20--63 and all later
  merge/terminal obligations remain open.

- Shard 20 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=20/64`.  The shard covers
  `[1188,1247)` (59 parents), with 37,170 raw extensions and 170 child
  orbits.  Artifact SHA-256 is
  `8b982458491ab122c07afa4e2d3f4090e9d21dd6f4cc2c7efd4c144ef0ef0c1e` and
  independent replay SHA-256 is
  `670fd4f981b788634a7f145faead70674939a0eda73f449e1f8e8076d2ffb20a`.
  The verified prefix is now 21/64, covering `[0,1247)` with 1,247 parents,
  785,610 raw extensions and 1,919 child orbits; shards 21--63 and all later
  merge/terminal obligations remain open.

- Shard 21 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=21/64`.  The shard covers
  `[1247,1307)` (60 parents), with 37,800 raw extensions and 128 child
  orbits.  Artifact SHA-256 is
  `63c48a0839c2951e3bebe13df0ba63ef7c271335c145eab6980914e6fffd9b3d` and
  independent replay SHA-256 is
  `9a9e128ef91566354ecbf91d11d16408aa9f83aa01b48f4ae4b20d8a95719163`.
  The verified prefix is now 22/64, covering `[0,1307)` with 1,307 parents,
  823,410 raw extensions and 2,047 child orbits; shards 22--63 and all later
  merge/terminal obligations remain open.

- Shard 22 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=22/64`.  The shard covers
  `[1307,1366)` (59 parents), with 37,170 raw extensions and 160 child
  orbits.  Artifact SHA-256 is
  `caf67bc5977961bf693e14836822631cfd040fd096951ab974db16260a12d242` and
  independent replay SHA-256 is
  `f88f0b68e0fb44be34daf0cd51776f6497b4f186dbc50d5c5ce5eba64f760536`.
  The verified prefix is now 23/64, covering `[0,1366)` with 1,366 parents,
  860,580 raw extensions and 2,207 child orbits; shards 23--63 and all later
  merge/terminal obligations remain open.

- Shard 23 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=23/64`.  The shard covers
  `[1366,1426)` (60 parents), with 37,800 raw extensions and 90 child
  orbits.  Artifact SHA-256 is
  `96931203384a6cc54cb6ec3a32b975e72418af3a74c770d404fb14b473864256` and
  independent replay SHA-256 is
  `c90699952966641821dab7ca1ce50b21dd99c89d244ed70a60f087e811c0f3f6`.
  The verified prefix is now 24/64, covering `[0,1426)` with 1,426 parents,
  898,380 raw extensions and 2,297 child orbits; shards 24--63 and all later
  merge/terminal obligations remain open.

- Shard 24 continuation (Geo Workstation, 2026-08-30): generator and
  independent replay passed for `m=4, depth=3, shard=24/64`.  The shard covers
  `[1426,1485)` (59 parents), with 37,170 raw extensions and 152 child
  orbits.  Artifact SHA-256 is
  `80ce8813470548acd7fffa6547db5ff426e23b74506d1fa39eefcd4211091423` and
  independent replay SHA-256 is
  `08b401ceaa0801b938543d6bb45c7e274a9c0223a699ac7a5851cdf0cffa930a`.
  The verified prefix is now 25/64, covering `[0,1485)` with 1,485 parents,
  935,550 raw extensions and 2,449 child orbits; shards 25--63 and all later
  merge/terminal obligations remain open.

- Shard 25 continuation (Geo Workstation, 2026-08-30): after the advisor's
  DevSpace Bash route became unavailable, the controller ran this single
  bounded shard remotely on Geo Workstation; generator and independent replay
  both passed.  The shard covers `[1485,1544)` (59 parents), with 37,170 raw
  extensions and 150 child orbits.  Artifact SHA-256 is
  `2b22c5449b6868fc797ee0d6d69bb0f253354e7895139f8fa6c2a2d1e3ab8e56` and
  independent replay SHA-256 is
  `df546aaf3ad797747cb7d084d687cb541f887c819ffad9fb1f3fd30eeb3919d9`.
  The verified prefix is now 26/64, covering `[0,1544)` with 1,544 parents,
  972,720 raw extensions and 2,599 child orbits; shards 26--63 and all later
  merge/terminal obligations remain open.

- Shard 26 continuation (Geo Workstation, 2026-08-30): the advisor's DevSpace
  route was disabled, so the controller ran this single bounded shard remotely
  on Geo Workstation; generator and independent replay both passed.  The shard
  covers `[1544,1604)` (60 parents), with 37,800 raw extensions and 149 child
  orbits.  Artifact SHA-256 is
  `91d288708aa8e05e0b0c92e1556704fd7f65f0c07756b4a5db8c804b6e89e1e2` and
  independent replay SHA-256 is
  `e358fd1f8813bf6c6ff55c04d66b8d5772ea8eeb0af0ecfb836a68e0172a0be3`.
  The verified prefix is now 27/64, covering `[0,1604)` with 1,604 parents,
  1,010,520 raw extensions and 2,748 child orbits; shards 27--63 and all later
  merge/terminal obligations remain open.

- Shards 27--30 continuation (Geo Workstation, 2026-08-30): after the
  advisor DevSpace route was disabled, the controller ran four protected
  sequential generator/replay pairs remotely.  All eight statuses were the
  expected verified values.  Shard 27 covers `[1604,1663)` with 91 child
  orbits (artifact/replay SHA-256
  `385af23c8fd6386dfdb701329f8523746f02ab4760dcd3cca124ad679c63724d` /
  `57aa14a3be637a7b8f0efe2803d78ff956e0c1779952b847586d4d361dfa54bb`),
  shard 28 covers `[1663,1723)` with 151 (`13cbffc5d0ad061a5b1c284cb80d23fb210522faa2bea07945019d1594f28522` /
  `968e4283f45c2671f9cef287d42811525e5636fc5221ad301fbd6b69ab47098e`),
  shard 29 covers `[1723,1782)` with 139 (`675168d91d6ad035f7a26351a819fccda4e4dd06f0681254e7be7a256c43bb32` /
  `5aa89101a5ee1106f37ec49c4b9f770fed2b743dc30147ae6cec649a299f8d53`),
  and shard 30 covers `[1782,1842)` with 77 (`bc4f67dc6424f6348cc154342988988fceca255536587594f7b360b2e715353a` /
  `ee8d70c464b154080e18589ed0f2be039e33c25b8189997361ae08b88efe22b9`).
  The verified prefix is now 31/64, covering `[0,1842)` with 1,160,460 raw
  extensions and 3,206 child orbits; shards 31--63 and all later
  merge/terminal obligations remain open.

- Shards 31--34 continuation (Geo Workstation, 2026-08-30): four protected
  sequential generator/replay pairs were completed remotely; all statuses
  were verified.  Shard 31 covers `[1842,1901)` with 105 child orbits
  (`ecdeb366ddf6c296d45fc95d3c1eb95edac5efcc622bff32568fc2f4d158f203` /
  `e379534cd8d36ac6cd21c25096fde22a5d7738b25127d10f4ccd74fe44e92f7c`),
  shard 32 covers `[1901,1960)` with 172
  (`dc27be4394b4eff398d36dd1d5b529dabb45cfc4862cb5e45c94c297da949aa6` /
  `a470cdbb02f44fb9cb33385671b0e98dc9aee2bd1f0bad148ea86e83d6862578`),
  shard 33 covers `[1960,2020)` with 109
  (`55ec65caf42f2a32c83fb6ef0a35d47f5f8c4c303d1d8e0152959028d0d7300d` /
  `80cd45d0c768236f25bd776f0ac9a4f353b2a4847f006ff8ad92a718387af176`),
  and shard 34 covers `[2020,2079)` with 63
  (`a6aa6e5ac5fde911b6384531370522c885a64deb067d14a40d552cb692f6e07a` /
  `462eef0f1b0a1f3e414fc69db2eb00e13c697f071bc3d1ac904a13619060683b`).
  The verified prefix is now 35/64, covering `[0,2079)` with 1,309,770 raw
  extensions and 3,655 child orbits; shards 35--63 and all later
  merge/terminal obligations remain open.

- Shards 35--38 continuation (Geo Workstation, 2026-08-30): four protected
  sequential generator/replay pairs completed remotely, all with verified
  statuses.  Shard 35 covers `[2079,2139)` with 147 child orbits
  (`7e3208328bc7e32cea6471ffd5c9e9966450d3d3b7be45641ef92454d9cd80dc` /
  `4fd5d8e5373a10bf594a35c3d83491e5f2ecc5468506fe9b4a720eba9a3ff2c0`),
  shard 36 covers `[2139,2198)` with 112 (`004825815a3c8c071d9119ec80f48f9ecdfa54975895e8c4c85a9cf08c9a0f17` /
  `98a08b89bcb5dbc8f277871dfe70f35c499d6c9e12ec34ad989a81b1500cba84`),
  shard 37 covers `[2198,2258)` with 36 (`e26f061cd85ca238b079e439b2ddf123c047cf77d511f5d2864391c8941bb464` /
  `60f774c92dcbb0a52d9b7650af8c294b7fad327b8686f8734165b3fe31b324f9`),
  and shard 38 covers `[2258,2317)` with 188 (`97dd90aa405bb0124b9f6f383ab9a6571fa77fc35f1d0b9bb8f089c34f6aae81` /
  `f4c34b496c98156328db88d0b4b0a4e4553a84efb3febd0542a5a05d3d5181cd`).
  The verified prefix is now 39/64, covering `[0,2317)` with 1,459,710 raw
  extensions and 4,138 child orbits; shards 39--63 and all later
  merge/terminal obligations remain open.

- Shards 39--42 continuation (Geo Workstation, 2026-08-30): four protected
  sequential generator/replay pairs completed remotely, all verified.  Shard
  39 covers `[2317,2376)` with 64 child orbits
  (`9cc9db7e160efe1c3ba29bd1dcfe02e1a0308ae1ae9e96f6d8bc32713e15c9b8` /
  `b858f4615991454ca9cb85359e01482ec8a5dd867f1302626a925b249ae64f4b`),
  shard 40 covers `[2376,2436)` with 147 (`720233943b7572dcb93a6fadf4ae49a3b6e82c81c57c6a62b1482d7933de7632` /
  `c3b6000ded92d4bead4ba6ef10c9cd86216321c5dcded163318d3c8fbfdd4e2e`),
  shard 41 covers `[2436,2495)` with 214 (`52aa94e0b5b91c31752b3ec3a55fbe171780975fa46f9b789f8295e0b0145185` /
  `ad43cb1fd23470df2ee869bc250e291318f513f193792541f60dc985bfdcac59`),
  and shard 42 covers `[2495,2555)` with 210 (`3725b86fa2d1185f867e7fed151d62d1cc8ce7706890f32f4a0d2457162c73a4` /
  `337d59088f2828e53471120bdae9e882d586fd9f3acb26e8611168dc03eb0ba2`).
  The verified prefix is now 43/64, covering `[0,2555)` with 1,609,650 raw
  extensions and 4,773 child orbits; shards 43--63 and all later
  merge/terminal obligations remain open.

- Shards 43--46 continuation (Geo Workstation, 2026-08-30): four protected
  sequential generator/replay pairs completed remotely, all verified.  Shard
  43 covers `[2555,2614)` with 106 child orbits
  (`39a230f6110dd8932ad2f99952a6b43bb11ebed88235ceb6a0e6c37d57f130b9` /
  `6e89d2e1d4046f6df6fb7f61846a27b511861f1e985b1109c87381a0e2aaa598`),
  shard 44 covers `[2614,2673)` with 69 (`06c4a42ca190774fe482676c814814bdcb236f3a888adf391ed3b8dacce60a48` /
  `c28321eaf06f26d0f7c1488a30888e257f15e57e7be2324f723f3fa8e08872cc`),
  shard 45 covers `[2673,2733)` with 117 (`51c3409e4cdab4e40adce7ce631c0f56456368d4599b9f8abd3bffffbfb5e263` /
  `2c9882bcdca12968d935150db1f10e891b5376c1fe04a5d856d876f39bf62fef`),
  and shard 46 covers `[2733,2792)` with 199 (`4b45eca4448c0d2754549a6fa940ee4e625ebee9fbecc77b90c032ca769a5f6a` /
  `ac5ab06e1c941006eef0fa5a4e61ae929742ee6b967f19371341cb9c0ee86348`).
  The verified prefix is now 47/64, covering `[0,2792)` with 1,758,960 raw
  extensions and 5,264 child orbits; shards 47--63 and all later
  merge/terminal obligations remain open.

## 2026-09-01 Fable 接手审计：S1-279..S1-282 由 top-block crowding 关闭

- **THEOREM（S1-279、S1-280）：** 在 singleton final-cap normal form
  `D = L ⊔ [B,A]`（`m=24-r` 个连续 high 深度，`r` 个 low 顶点）下，
  `C(m,2)` 个 high-high 距离按 LCA 分成 `r+1` 类。high-LCA 类的距离
  `y+y'-2q` 本身落在 `1..2m-3`（`q` 不必由 `y+y'` 唯一决定）；固定深度
  `l` 的 low-LCA 类的距离为 `2B-2l+y+y'`，其中 `y+y'∈[1,2m-3]`，
  故在全局距离单射下每类至多 `2m-3` 个 pair。`C(m,2) <= (r+1)(2m-3)`
  在 `r=3`（210 > 156）与 `r=4`（190 > 185）均不成立。因此 S1-279 对
  **所有** `s`、两种 low shape、所有 `d1<d2` 不可能；S1-280 同理。不使用
  FW303 core、`c` 范围或 `{4,5,16,18,19,20}` 字母表。之前的 `s=152/154`
  star/chain 分片、555397 签名 union、38-row 预筛和 1286 片 forest 计划全部
  被涵盖，无需再跑。
- **FABLE-REPORTED FINITE IMPOSSIBLE（S1-281、S1-282；provenance pending）：** depth-free class search
  （`theory-lab/s1_crowding/abstract_class_search.cpp`，只用上述类内单射条件，
  不依赖 `s` 与 low 深度）对 `r=5` 的 9 个 rooted low-tree 同构类（24 个标号
  形状）与 `r=6` 的 20 个同构类（120 个标号形状）均返回零完整结构。
- **REPRODUCED：** 直接 DFS（`s1_direct_search.cpp`，不含任何 FW303 假设）在
  Geo Workstation 上扫完整个 `δ=279` normal form：`s∈[13,160]`、两种 shape、
  任意奇偶的 `0<d1<d2<B`，共 5,725,972 个实例、571,781,366 个节点、零幸存、
  零中止（4 个 `nice -n 15` worker，4 分钟）。正向对照：已知 6 点 Leech 树
  （最重边 8 为悬挂边）被找回；植入的距离单射随机树全部被找回。
- 代码审计（子代理，只读）：`_s154` 主链路四个文件量词正确（`B=280-s`、
  `c<=14`、`d2<126`）；`replay_fw303_remaining_classa_forests_s154.cpp` 与
  s152 版本逐字节相同（仍是 `S=152,B=128,c<=13`，未被任何驱动脚本调用，
  但若被当作 s154 证据则错误）；`replay_fw303_all_class_forests_s154.cpp`
  的 `d1_max=124` 标签为残留（应为 122，仅标签）。
- 首片 `forest_shards_s154_chain/python_0000_000549.json` 已自然结束
  （440 s，2.2 GB RSS，1530 jobs，幸存 0）；按上述定理无需继续。
- 详见 `docs/checkpoint-2026-09-01-s1-top-block-crowding.md`。
  `δ=283`（`r=7`，48 个同构类）正在 Geo Workstation 上以 4 片运行，
  尚无结论。S1 整体、非 singleton final cap、R2-COVER、T4-COVER 与全局
  非存在性仍然开放。

- **2026-09-01 补充（Fable；provenance pending）：** `δ=283`（`r=7`，`m=17`）现为 **FABLE-REPORTED
  FINITE IMPOSSIBLE**：48 个 rooted low-tree 形状中 47 个无 depth-free 结构
  （geo-ws 4 片，无中止）；链状形状恰有 14,730 个 depth-free 结构，深度阶段
  （对每个结构穷举 `s` 与 low 深度 `L`）零幸存。两套独立运行（geo-ws 单进程
  v2；Hoffman2 64 片 prefix-split v3）在 leaves=14730、csp_nodes=16302184、
  survivors=0 上完全一致。depth-CSP 已用 relaxed-target differential test 对照
  直接搜索验证（chain 计数逐 s 相等，star 恰为 2 倍）。`δ=284`（7/115 形状
  有结构）与 `δ=285`（95/286）的深度阶段已在 Hoffman2 启动，尚无结论。
  哈希见 `docs/checkpoint-2026-09-01-s1-top-block-crowding.md` §3.7–3.8。

## 2026-09-02 controller audit of Fable top-block checkpoint

对 `docs/checkpoint-2026-09-01-s1-top-block-crowding.md` 的独立审计发现：
§2 的 crowding 结论可以成立，但理由必须是每个 LCA 类中的**距离值域**至多
`2m-3`，而不是声称 high-LCA 时 `q` 由 `y+y'` 决定；后者并不成立。该表述
已在 checkpoint 中修正。

另外，计算 provenance 尚未完全闭合：checkpoint 记录的
`abstract_class_search.cpp` 哈希 `3a7a58...` 与当前本地、Geo Workstation、
Hoffman2 可见源文件的哈希
`e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c` 不同，
正在运行的 `abstract_class_search_v4` 二进制也有独立哈希。因此 `δ=281..283`
的零计数暂保留为 Fable-reported finite evidence；要恢复
`CERTIFIED FINITE IMPOSSIBLE` 标签，必须补齐每次运行的 exact source hash、
binary hash、命令行和 output hash 对应关系。`δ=284,285` 的 Hoffman2 深度数组
仍在运行，输出仍为 `.tmp`，不得据此作结论。

本次只读队列核对记录：Hoffman2 array `115848` 的提交行是
`hoffman2_s1_depth_array_slurm.sh 16 shapes_r8_exists.txt 5 64 r8`，当前
64 个 task 仍为 `RUNNING`；array `115912` 的提交行是
`... 15 shapes_r9_exists.txt 5 128 r9`，当前 36 个 task `RUNNING`、其余
`PENDING (QOSMaxJobsPerUserLimit)`。远程 `depth_r8` 有 64 个 `.tmp`、
`depth_r9` 有 36 个 `.tmp`，没有已提交的最终 `.txt`。可见的 Hoffman2
`abstract_class_search_v4` binary SHA-256 为
`8e1297579d67651e0728347325a0812bf9b5680d0fc6e9d380f23dd51e74e17c`；
这组运行仍只能标为 `RUNNING/UNKNOWN`。

随后只读复核 Hoffman2 的 `depth_r7chain` 产物：64/64 个
`split_*_of_64.txt` 均已生成且包含 `SHAPES_FILE_SUMMARY ... COMPLETE`，
汇总 `leaves=14730`、`depth_survivors=0`，`all_splits_sorted.txt` 的 SHA-256
为 `b1bce6b547ac84acf94aaa63a901f51472ea06569e82f32d8dac54e62de18c97`，
与 checkpoint 记录一致。这加强了 `δ=283` 的重复执行证据，但不解除前述
source/binary provenance gap；`δ=284,285` 仍只有 `.tmp` 中间输出。

普通 Chat 顾问的后续只读审计（`CONSULT-20260902-005`）给出了一条可实现的
更优预筛：对每个 low vertex `v`，设其下方各 high component 大小为
`n_{v,j}`、总 high mass 为 `M_v`，且 `C0=2m-3`。任何候选都必须满足

```text
W   = Σ_{v,j} C(n_{v,j},2) <= C0
P_v = C(M_v,2) - Σ_{u child of v} C(M_u,2) - Σ_j C(n_{v,j},2) <= C0
W + Σ_v P_v = C(m,2)
```

这是只依赖 component-mass 与 low-LCA 的 sound 必要条件，可在 high-label
DFS 前用树形 DP 排除结构；随后可用
`l_i >= ceil((δ+2-2s+M_i^sum)/2)` 和 root-class 的 `s` 下界做
depth-interval/Hall presolve。顾问未找到安全的 `δ` 单调递推；这些条件不能
单独当作充分条件。现有 `δ=284,285` 远程数组完成前不启动新路线计算。

为落实该建议，新增未运行的独立脚本
`theory-lab/s1_crowding/component_mass_dp.py` 及说明
`docs/s1-component-mass-dp-2026-09-02.md`。脚本只枚举 low-tree 上的
component-mass 分拆并输出 `W,P_v` 必要条件记录，不读取或覆盖已有结果；
已按远程 Python 3.8 环境改用兼容类型标注。待现有 Hoffman2 数组结束后，
再在 Geo Workstation 做小规模差分验收，禁止把该预筛当作充分条件。

在 Geo Workstation 已完成该脚本的最小远程 smoke test（未在本机运行）：
`m=5, lowpar=-1,0,1`，单进程 `nice -n 15 timeout 120`，返回 `RC=0`，
`total_mass_patterns=108`、`necessary_pass_patterns=73`、耗时 `0.04s`。
随后用独立内联校验重算分拆生成函数系数、子树质量、`W` 与全部 `P_v`，
返回 `COMPONENT_MASS_DP_SMOKE_VERIFIED total_patterns=108 pass=73
equation_checks=73`。远程脚本 SHA-256 为
`fb9af6357817f67cbfecf5932fa29248c69b1053ea717d12f7d0cbb9c84d7bf8`，
JSONL 产物 SHA-256 为
`e555d651b1be7399bf6d2ce1117828837313cd7c1ca37b94f3957a9cb6ed30f1`。
这只验证预筛实现的微型接口，不是 `δ=284/285` 的数学结论。

## 2026-09-02 Fable 接手与审计文档

已新增可直接交接给 Fable 的完整接手包：
`docs/handoff-fable-takeover-audit-2026-09-02.md`。该文档固定当前
frontier、证据等级、provenance 缺口、Hoffman2/Geo Workstation 资源边界，
并要求 Fable 优先审计 component-mass DP、depth-interval/Hall 传播及其他
sound 结构性替代路线，再决定是否扩展 `delta=284,285` 的远程计算。文档
明确禁止本地重计算、禁止修改现有远程作业，并给出短格式验收报告模板。

## 2026-09-02 普通 Chat 顾问补充审计（CONSULT-20260902-006）

顾问只读复核了新的 Fable 接手包和状态尾部：未发现 component-mass DP 的核心
量词漏洞；再次确认 `W`、各 `P_v` 及其恒等式只是 sound 必要条件，不能写成
充分条件。对 `delta=284,285`，建议先等待现有 Hoffman2 depth arrays 完成，
不要重复提交；若要加强 `delta=283` 的严格证据，最小增量是冻结已有 14,730
个结构，另写一个独立 depth checker 重放 `(s,L)`，成本远小于重做结构搜索。

顾问还明确区分：Geo/Hoffman2 的重复执行不等于独立算法；在 source/binary/
command/output provenance 闭合前，`delta=281..283` 仍应保留
`FINITE-EVIDENCE / PROVENANCE PENDING` 标签。没有找到可安全使用的 `r` 或
`delta` 单调递推；若质量 DP 的 shape-level 缩减很小，应回退现有 depth
checker，而不是引入高风险 partial residual 剪枝。

随后新增压缩版必要条件 DP
`theory-lab/s1_crowding/component_mass_dp_compressed.py`，只保留每个 low
子树的 `(M,W)` 可达状态，并按 `(a,w)` 合并局部整数分拆。该实现未在本机
运行；Geo Workstation `m=5, lowpar=-1,0,1` 远程 smoke 返回 `RC=0`、
`elapsed=0.05s`、`MAXRSS=12272 KB`，root `W` 状态集合
`[0,1,2,3,4,6]` 与原始枚举 108 个模式中 73 个通过模式的 `W` 集合完全
一致。远程/本地脚本 SHA-256 为
`7ed764d97ff45e9eca16e79c48d2d6328f32c3cc99c35a3b58f902587473d162`。
这只完成微型接口差分，尚未证明 `m=16/15` 的生产过滤效果；下一步应在
远程做一个有限 relaxed-target 差分后，再决定是否接入现有 depth checker。

## 2026-09-02 Hoffman2 provenance read-only check

在不改动任何作业的前提下，重新读取 Hoffman2 的当前工作目录
`/u/scratch/l/lsmeng/leech-trees/theory-lab/s1_crowding/`：

- `abstract_class_search.cpp` SHA-256 为
  `e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c`，与当前本地
  checkout 完全一致；
- `abstract_class_search_v4` SHA-256 为
  `8e1297579d67651e0728347325a0812bf9b5680d0fc6e9d380f23dd51e74e17c`；
- `hoffman2_s1_depth_array_slurm.sh` SHA-256 为
  `0f38e850f958d31b464e9abb46116f97ef2b654819ce526d79054b0c0d72a378`，脚本明确
  调用 `./abstract_class_search_v4 --m ... --shapes-file ... --solve-depths`；
- 远程文件时间顺序为 source `14:20:40`、binary `14:21:20`、r7 汇总
  `14:22:42`（2026-09-01，Hoffman2 本地时间）。

这把“当前源—当前 v4 binary—depth wrapper”链条闭合到可审计程度，并加强了
r7chain 运行的 provenance。它**不能**单独证明更早的 r5/r6 输出使用了同一
binary，也不能把重复运行称为独立算法；`delta=281,282` 仍保留
`FABLE-REPORTED FINITE EVIDENCE / PROVENANCE PENDING`，直到逐次命令、输入和
输出哈希完成对应。SSH 后续一次读取超时只记为观察失败，不改变已运行作业状态。

随后在 Geo Workstation 对一个实际 `m=16,r=8` structure-bearing 形状
`lowpar=-1,0,0,1,3,4,5,6` 运行压缩 DP（单进程、`nice -n 15`、
`timeout 120`），`RC=0`、`ELAPSED=0.08s`、`MAXRSS=12568 KB`，根节点
可达 `W=0..29` 全部状态，`root_possible=true`；各顶点状态数为
`[280,280,84,280,272,215,156,84]`。这验证了压缩实现可在实际 m=16
尺度快速完成必要条件层，但该形状未被排除，也不是存在性结论。旧的完整
笛卡尔积探针仍保留为 `RC=124` timeout/UNKNOWN，未被覆盖或重启。
压缩探针 summary 的本地副本 SHA-256 为
`46a13ff99aa4ae32d1613374c86b598ca0fc1e9ac80820234cc29a257cc63766`，
计时文件 SHA-256 为
`d4b3e16c67767b19350db925ca055459c202d46e5016b5b18503d07c023226c6`；
旧探针 `.time` SHA-256 为
`b90e0581b51115e43b81e870e929a5bf35cca6f52abe923f315504a7a923432d`。

同一轮只读复核 Hoffman2：array `115848` 仍为 `64 RUNNING`；array `115912`
仍为 `36 RUNNING + 1 PENDING`。没有最终 `depth_r8/r9` 文本输出，因此
`delta=284,285` 继续保持 `RUNNING/UNKNOWN`，未作任何重启、取消或修改。

后续只读检查发现临时输出已有部分逐形状记录：`depth_r8` 的 64 个 `.tmp`
合计 384 行 `EXHAUSTED`（可见 6 个 lowpar 记录各重复 64 次），汇总
`leaves=23332646`、`depth_survivors=0`、`csp_nodes=86859726336`；
`depth_r9` 的 36 个 `.tmp` 合计 216 行 `EXHAUSTED`（可见 6 个 lowpar
记录各重复 36 次），汇总 `leaves=111759`、`depth_survivors=0`、
`csp_nodes=5413170804`。这些只是仍在运行的 `.tmp` 中间证据；尚未覆盖
完整 7/95 shapes，也没有最终 `.txt` 或完整数组收尾标记，故仍保持
`RUNNING/UNKNOWN`，不得据此宣称 `delta=284/285` 已关闭。

为验证压缩 DP 不会在状态归并时误删，Geo Workstation 又完成了一个 `m=6`
有限差分：原始枚举与压缩 DP 对 `chain3=-1,0,1`、`star3=-1,0,0`、
`branch4=-1,0,1,1` 三个 low-tree 形状逐一比较根 `W` 集合；三者均为
`[0,1,2,3,4,6,7]` 且 `equal=True`，单进程 `nice -n 15 timeout 120`、
`RC=0`。远程差分汇总 TSV SHA-256 为
`0b46185ca691b84d40fa6c08f25fef057f40061f7c31b216d90ff4d929fca89d`。
这是压缩接口的更强小规模证据，仍不是生产尺度充分性或全局证明。

为把 `P_v/W` 与 depth feasibility 连接起来，新增独立 pilot
`theory-lab/s1_crowding/mass_depth_hall_pilot.py`。在 Geo Workstation
用 `m=5, delta=10, s=5..8`、单进程 `nice -n 15 timeout 120` 对
`chain3`、`star3`、`branch4` 三个 low-tree 形状比较 suffix-Hall 必要
拒绝与直接 low-depth 穷举；对应 `mass_s_pairs/hall_reject/exact_depth_possible/
false_rejects` 为 `432/68/83/0`、`432/16/56/0`、`1008/522/70/0`，三者
均 `soundness_ok=true`。远程脚本 SHA-256 为
`0b1c94639cec6b66c0b90aa229df35ef825268806c2413045a3592f314a13025`，
结果汇总 SHA-256 为
`41c6b01396d058a729603a909202c033ee9faaa16865133554530686f41c56fb`。
该 pilot 仅验证必要性方向，Hall 通过不构成存在性结论。

顾问随后复核压缩实现，确认 `(M,W)` 对 `W/P_v` 布尔必要性 DP 的父节点
转移信息是充分的，但提醒该压缩不能恢复具体 `P_v` 向量，不能直接用于
depth/Hall 的 mass-pattern 传播。按建议在 Geo Workstation 用未压缩脚本
作 oracle，对 `m=4..7,r=1..5` 全部 136 个 rooted lowpar shapes 做根
`(M_root=m,W)` 集合差分，`mismatch_count=0`、`RC=0`、`ELAPSED=2.38s`、
`MAXRSS=12020 KB`。summary SHA-256 为
`38e4ddf355244bf7db5d8cec1af2846ccae87fd6050665a35dc72fcbc69046ab`，
计时 SHA-256 为
`2de409dd97778502adacc117d68dad2a4edfaedbf6f636c1d72c7a37e9e7a3b2`。
因此该实现可标为 `LOGIC-AUDITED + SMALL-EXACT-DIFFERENTIAL`，但生产
depth/Hall 仍须保留 witness/profile 或重新展开 mass assignments。

## 2026-09-02 顾问替代路线审查（CONSULT-20260902-009）

普通 Chat 顾问在只读核对工作站副本和三份 pilot 后，定位出当前最早的数学缺口：
从单个 class 的容量 `W,P_v` 走到所有 low-LCA 平移类能否同时嵌入同一个全局距离槽集合。
从 `r=5`（`delta=281,m=19,C0=35`）起，纯 top-block 与 component-mass 总容量已经
到达天花板。顾问给出的最小 counterprofile 是 5 点 low-chain，直接挂接质量
`(1,1),(1,1),(1,1),(1,1),(7,1,1,1,1)`，其
`M=(19,17,15,13,11)`、`W=21`、`P=(35,31,27,23,34)`，满足
`W<=35`、各 `P_v<=35` 且 `W+sum(P)=171=C(19,2)`，因此不能靠总容量排除。

顾问提出更强的联合区间 Hall：固定合法 `(s,L)` 后，low class `v` 的所有距离落在
`I_v=[2B-2l_v+1, 2B-2l_v+C0]`，high-LCA class 落在 `[1,C0]`。对任意 class 子集
`Q`，真实 distance-injectivity 必须满足
`sum_{i in Q} demand_i <= |union_{i in Q} I_i|`；因此违反该不等式是 sound
必要性排除。当前实现为
`theory-lab/s1_crowding/joint_interval_hall_pilot.py`，只使用明确的、互异的
occupied slots；通过不表示存在。

在 Geo Workstation scratch
`remote_scratch/joint_interval_hall_pilot_20260902/` 做了独立小规模 matching
differential：`joint_interval_hall_differential.py` 重新实现逐槽位回溯 oracle，
覆盖 `m=5,delta=10,s=5..8` 的 chain3、star3、branch4，所有真实 class-slot
匹配与联合 Hall 结果逐例一致：

```text
chain3   exact_depth_assignments=151  hall_rejects=91   matching_mismatches=0
star3    exact_depth_assignments=188  hall_rejects=132  matching_mismatches=0
branch4  exact_depth_assignments=184  hall_rejects=120  matching_mismatches=0
soundness_ok=true, RC=0, timeout=120s, nice=15
```

脚本 SHA-256：`f2fd8e642707df5f3549505b6cc3839316ffdba30944128037554306df9b8c1f`；
差分脚本 SHA-256：`abbb102a09219758d6afef6511c5de738bcd57e8688493fc94e8f58db4072109`；
结果 SHA-256：`d33c718a721ccc266c39572d2030a108b61cf156cf181af7052b1e1cfa6cac9f`。

曾有一版错误对照把“depth-only 可行”当成完整解，产生 91/132/120 个所谓
false reject；该对照已标为无效，不进入证据。正确对照只验证联合 Hall 与独立
class-slot matching 的实现一致性，当前状态为
`LOGIC-AUDITED + SMALL-EXACT-MATCHING-DIFFERENTIAL`，还没有接入真实
`delta=284,285` 结构，也不是全局证明。下一步应在现有完整 `(structure,s,L)`
记录上做 post-processing，并先量化实际排除率；不应据此重启或扩大 Hoffman2 arrays。

CONSULT-20260902-008 对 flow 工具的最终审计：其放宽 class→slot 集合和
`max_flow< W+ΣP_v` 判据是 sound，但仅在输入字段真实且完整时成立。生产
前必须独立重建 `W/P_v/(s,L)/lowpar`、核对恒等式、深度合法性，并证明
occupied 槽位均由不同 pair 占用；重复 occupied 值应作为上游碰撞拒绝，
不能静默去重。当前 flow 保持 `LOGIC-AUDITED / CANDIDATE NECESSARY
FILTER`，尚未是 production VERIFIED。

在此基础上新增候选的 global distance-slot flow 工具
`theory-lab/s1_crowding/global_distance_slot_flow_pilot.py`：将 high-LCA
需求 `W`、low-LCA 需求 `P_v` 与放宽的距离槽做容量为 1 的最大流。允许
集合取实际选项的超集，因此 flow 不足是 sound 必要性排除，flow 通过不
表示存在。Geo Workstation toy 验证 `m=5,delta=10,s=8` 中，3 个 fail
案例均与独立回溯 matching 一致（`max_flow=9/10`、`9/10`、`1/10`），
另一个 demand=6 案例 `max_flow=6`；脚本 SHA-256 为
`e316dd3dc71bca967f7a3aa474c500b108a7981b45160e4296eb84c220a99228`。
尚未接入实际 284/285 结构；需先做 relaxed-target 差分再评估节省。

顾问复核后给 global-flow 工具增加了输入 guard：要求
`W+ΣP_v=C(m,2)`、根深度为 0、low depths 互异且在 `[0,B)`、父子深度
严格递增、`W/P_v>=0`，并拒绝重复或越界的 occupied slots。当前版本脚本
SHA-256 为 `ac3c016d28cab791e3ef61eb7ba89458698096522b56d622ffa039f56f339518`。
Geo Workstation 回归中，合法 toy 输入 `W=1,P=[5,3,1]` 得到
`demand=10,max_flow=8,necessary_pass=false`，重复 occupied 输入触发
`DUPLICATE_GUARD_OK`；枚举还找到通过例 `W=2,P=[0,1,7]`、`max_flow=10`。
这只验证 plumbing，不是实际 Leech-tree 结论；接入前仍需真实 survivor
样本和独立完整检查。

随后把 Hoffman2 现有 structure-bearing 清单（r=8 共 7 个、r=9 共 95 个）
同步到 Geo Workstation，运行压缩 mass DP census；输入清单省略根标记，
运行时显式补回 `-1`。单进程 `nice -n 15 timeout 120`，`RC=0`、
`ELAPSED=4.61s`、`MAXRSS=12472 KB`；`m=16,r=8` 为 `7/7` root_possible、
`0` 排除，`m=15,r=9` 为 `95/95` root_possible、`0` 排除。也就是说，
当前 `W/P_v` shape-level 过滤器没有减少 284/285 的结构清单；下一步应
优先评估 `P_v→depth-Hall` 或 global distance-slot flow，而不是把这层
误写成关闭结果。完整 JSONL SHA-256 为
`1d807357e5708a9f1b482101ab775b55a6e39b9d8a5078bc01079da4270666ff`，
计时文件 SHA-256 为
`83b0ccb9e404893d7ea6a5c073ccefee012ed76aaad44f434eb0340a8a839c57`。

## 2026-09-02 顾问补充审计（CONSULT-20260902-007）

顾问复核压缩 DP 后提出三项必须写入接手边界的修正：

1. `/home/geo/codex-work/leech-trees` 是当前已授权的 Geo Workstation 工作副本，
   不应因 `/home2/geo/`、`/media/geo/` 的允许根表述差异而自行迁移 checkout；
2. `5,201,986` 是较弱 exact-10 primary raw survivor count，`555,397` 是后续
   更强 canonical union，二者不是同一对象；
3. 旧 FW303 Class A/B/C 只对应 `delta=279` 的特定 embedding，不能未经新证明
   直接用于 `delta=284,285`。

顾问给出的下一层 sound 路线是将每个质量模式的 `P_v` 直接转成
`s` 下界和 low-depth suffix-Hall 检查：Hall 失败可严格排除，Hall 通过不代表
存在。该路线已在小规模 pilot 中验证 `false_rejects=0`；若仍需更强剪枝，
可在此基础上考虑 global distance-slot flow，但暂不引入旧 A/B/C 或高风险
partial residual DFS。

## 2026-09-02 translated-sumset STRUCT 重建正向控制

为验证 exact translated-sumset 路线的输入链条，在 Geo Workstation 对已有
r7 chain 结构执行单进程、`nice -n 15`、`timeout 120` 控制：

```text
abstract_class_search_v4 --m 17 --lowpar 0,1,2,3,4,5 --xcap 1000 --stop-first --emit
STRUCT -1 -2 -3 -4 -5 -6 -7 -7 6 6 6 -6 -5 -4 -3 -2 -1
source SHA-256: e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c
binary SHA-256: 38e3c2a5c0d58864809056699e84176d461ba4a70ba5ad141e52ca173cd9ebad
```

独立 `translated_sumset_csp_pilot.py` 从 `lowpar+hpar` 重建 high forest、
high LCA、`H=within_vals` 与 `S_v=class_sums[v]`，并检查精确平移集合的
high-high 必要条件。`RC=0`；在 `delta=283`、`node-limit=500000` 下
`tested_s=158`、`high_high_passes=474290`，最终状态 `NODE_LIMIT`，因此是
输入重建成功的远程 pilot，不是完整 census，也不构成存在性或非存在性结论。

产物位于 `remote_scratch/translated_sumset_positive_control_20260902/`：

```text
translated_sumset_csp_pilot.py   0b1e700038d8aaa91c9a81149ab8c0b3702bd65b6d47231ff7abb54cb38dbf61
struct_r7_chain.txt              4f59c070ed78bb3b2fe7d467f811ab25b98d80a1b6626c52d4b0fc0f839a449d
translated_sumset_result_v2.json c7d91c53d909000257ff8a290e5a2029c6c7b64633c0c8a27e17587005c569c7
translated_sumset_run_v2.stderr  5962f3cf8b2dca06f2e382685039396b96ad5a8ab5d51ec4341de966ae77c845
```

当前证据等级为 `REMOTE REPRODUCED INPUT-RECONSTRUCTION PILOT`。生产缺口仍是：
对真实 `delta=284/285` 完整 `STRUCT` survivor 做零误删 differential，并在
固定 `s` 或完整小例上取得可完成的终止状态；没有这些证据，不得把该过滤层
写成 production verified。

随后对同一 r7 chain 结构固定 `s=158`，用现有 `abstract_class_search_v4` 的
完整 depth checker 做独立对照（Geo Workstation，`nice -n 15 timeout 120`）：
`RC=0`、`leaves=1`、`depth_survivors=0`、`csp_nodes=24`。这说明
translated-sumset 层是较早的必要过滤而非完整求解器；不能把两次输出称为
独立完整算法，也不能外推为全局零计数。

对照文件哈希：

```text
cpp_fixs158.txt    04ffe728009db725909bc5a554ea9300d5d858c5312dcdc0686f8ff63c32b8d2
cpp_fixs158.stderr e321fd66e43908c3ec255c752ac518d47c383da51140731add2e65b0adc7930d
```

随后完成第一条 genuine positive control：Geo Workstation 上运行
`m=4,r=1,order=6,delta=11` 的 C++ 搜索（单进程、`nice -n 15 timeout 30`），
`RC=0`、`leaves=9`，得到 `DEPTH_SURVIVOR s=8 L=0 hpar=-1,-1,1,1`。
独立 translated-sumset post-processor 对同一 survivor 完整枚举 `s=1..11`，
输出 `H=[1,2,3]`、`S_0=[1,2,3]`、`high_high_passes=3`、`status=COMPLETE`，
并保留 `s=8,L=[0]` witness。该结果证明小例上没有误删 genuine survivor，
但仍不覆盖 `delta=284/285`。

产物哈希：

```text
order6_genuine.txt             ac530b6a13d7c718a3f26da6f8b30eab0f01c9d564614447905658d95365b270
order6_genuine.stderr          ac148848dd5934439bb7dabf6eae3bce3ec40974ded29a3d32a9d64386347ab6
order6_translated_result_v3.json 66beae67306c3f993f2424f5eb5ac85b9d62013439716398d6255d8efeb7c83a
order6_translated_v3.stderr       7df576a0964a5d85c4251642a04b3d709cf6a65522c42b6684d1c38fbba512ea
```

该 v3 结果还通过统一加权树的 BFS 逐对距离核对：`bfs_check.ok=true`、
`pair_count=6`，重建的 H/S 与 BFS 归一化结果完全相同。小例 H/S 接口因此
达到 `SMALL-EXACT-DIFFERENTIAL`；真实 `delta=284/285` production 接入仍是
GAP。

同一 r7 结构在脚本加入 BFS 后复跑：`RC=0`、`bfs_check.ok=true`、
`pair_count=136`、`high_high_passes=474290`、`status=NODE_LIMIT`。结果
`translated_sumset_result_v3.json` SHA-256 为
`12df3fb35bcca3bb59aac89015d0bd9e329fa967f9d738e347294349572c3c6a`，错误/计时
文件 SHA-256 为 `fab979ad8e4eb9bce2773eb8e18f6daa30bffa0ee75b5b1fc1a53a44ee046680`；
当前脚本 SHA-256 为 `0b1e700038d8aaa91c9a81149ab8c0b3702bd65b6d47231ff7abb54cb38dbf61`。

## 2026-09-02 顾问 011：translated-sumset 接入审查

顾问确认 generic unified-tree + ancestor-list LCA 是从 `lowpar+hpar` 重建
`H/S` 的最小独立算法；必须检查 high parent 只指向更早节点、负 parent 在
合法 low-root 范围、`|H|+Σ|S_v|=C(m,2)`，以及 H 和每个 S_v 内部无重复。
跨不同 S_v 的 raw sum 重复是允许的。

顾问建议把统一加权树 BFS 逐对距离作为生产 post-processor 的输入门槛；order-6
genuine control 已通过（`bfs_check.ok=true`, `pair_count=6`）。在没有不可变的
`delta=284/285` `STRUCT` corpus 时，正式状态必须保留
`PRODUCTION EFFECTIVENESS GAP`，不能从 `.tmp` 或 aggregate counters 推导排除率。
更强增强顺序为 holes → 固定 `[B,B+m-1]` x-high owners → exact LL，每层都先做
genuine-positive-control 零误删。

## 2026-09-02 occupied 增强层远程小例

按顾问建议，post-processor 增加可选的固定 x-high 槽位 `[B,B+m-1]` 与
holes `{s+l_v≤delta}`，仅在 owner 已确定且互异时加入，碰撞即拒绝而不去重。
order-6 genuine survivor 仍通过（`high_high_passes=1`、`occupied_rejects=2`、
`bfs_check.ok=true`）；r7 frozen STRUCT 在 500000 节点上限内为
`occupied_rejects=474290`、`high_high_passes=0`，但仍是 `NODE_LIMIT`，不是完整零计数。

脚本当前 SHA-256：`c993dec61b6ecd2d5797b4774d9aaacf5487f784319047ab10a2104d88ffc5d3`。
结果文件 SHA-256：

```text
order6_translated_occupied.json bf0bfba31315ca618de714ad4c2a4226a3cb8cf7fcf9be1775310a1f2667f980
r7_translated_occupied.json     fd58e739a51e5f285c68d6d35be899135b4f18e0427cc58b6f29414063f02156
```

该层仍为 `SMALL-EXACT-DIFFERENTIAL / CANDIDATE NECESSARY FILTER`，未接入真实
`delta=284/285` corpus。

又完成首个 `delta=285,m=15,r=9` structure-bearing 单形状控制：
`lowpar=0,0,0,0,1,5,6,7`，`STRUCT=-1,-2,-6,-7,-8,-9,-9,5,5,5,-8,-7,-6,-2,-1`，
Geo Workstation C++ 返回 `RC=0,leaves=1,nodes=7687`。独立 H/S+BFS 对
`C(15,2)=105` 个 high pairs 为 `bfs_check.ok=true`。普通层在 500000 节点
上限内 `high_high_passes=481494,status=NODE_LIMIT`；occupied 层为
`occupied_rejects=481471,high_high_passes=23,xhigh_out_of_range_rejects=14,
status=NODE_LIMIT`，不是完整排除。

产物哈希：

```text
struct.txt               bd6186f7b9afa58818e5aa3f0434ae9119399670758a0c3b7ca84268d935f0d5
translated.json          ba85cd3a12df17dfa63d3c5e0b5bf9edd0d0a35fe47edbd3e0460f6d95d85642
translated_occupied.json 9027d6a6be8bd6487a67cc8ce1dc2c7972a610116bc819339a185f3e0913571c
```

顾问 012 发现 occupied 模式缺少 x-high 槽位越界 guard；已加入
`xhigh_out_of_range_rejects`，只增加必要剪枝。回归中 order-6 genuine 仍为
`status=COMPLETE,high_high_passes=1,occupied_rejects=2,
xhigh_out_of_range_rejects=3,bfs_check.ok=true`；首个 delta-284 单形状在
500000 节点上限内为 `occupied_rejects=477145,high_high_passes=0,
xhigh_out_of_range_rejects=15,status=NODE_LIMIT`，不构成完整排除。

当前脚本 SHA-256：`a157174be591c65e8cab7d005ed2df871466386042542cb500ce6a3839c02df0`。
结果 SHA-256：

```text
order6_translated_occupied_v2.json e7a549e164f8e58a7645830db8a43e2852e3a4c5f154f6f0139b66a0601a121e
delta284_translated_occupied_v2.json e9e820776bf5864240d5c7db837156ad737c50310da8fd91c3161ddfe2869d28
```

## 2026-09-02 Hoffman2 latest read-only status

SSH 重新可读；作业没有结束，也未被重启或修改。最新 `squeue` 显示：

- array `115848`（r8/depth）：64 个 task 全部 `RUNNING`；
- array `115912`（r9/depth）：36 个 task `RUNNING`，其余数组 task 仍
  `PENDING`（QOS 限制）；
- `115949/115950`（s1abs）仍为 `PENDING`。

`depth_r8` 当前仍只有 `.tmp`，合计 384 行；`depth_r9` 仍只有 `.tmp`，
合计 216 行；尚无最终 `.txt` 或完整 coverage/收尾标记。故 `delta=284/285`
仍保持 `RUNNING/UNKNOWN`，不得把中间计数写成有限排除结论，也不采取取消、
重启或改参数动作。

随后完成首个 `delta=284,m=16,r=8` structure-bearing 单形状控制（Geo Workstation，
单进程 `nice -n 15 timeout 120`）：`lowpar=0,0,1,3,4,5,6`，
`STRUCT=-1,-2,-4,-5,-6,-7,-8,-8,-8,6,-7,-6,-5,-4,-2,-1`，C++ 返回
`RC=0,leaves=1,nodes=12346`。独立 H/S+BFS 对 `C(16,2)=120` 个 high pairs
给出 `bfs_check.ok=true`。无 occupied 时 500000 节点上限内
`high_high_passes=477145`；加入 holes+x-high 后为
`occupied_rejects=477145,high_high_passes=0`，但仍是 `NODE_LIMIT`，不是完整零计数。
这证明新层可以处理真实 delta=284 结构输入，并量化即时剪枝；production
结论仍须完整终止与 zero-false-reject differential。

source SHA-256：`e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c`；
Geo binary SHA-256：`38e3c2a5c0d58864809056699e84176d461ba4a70ba5ad141e52ca173cd9ebad`。
产物哈希：

```text
struct.txt               0c7541bb1dadd9f40a9d7064cd158044b5c84b1097fc934c36537b7b453fcf7d
translated.json          c0cc7172378d19165fed665d880f20527ef445ffa5b99562dc06b0587702087b
translated_occupied.json 83523c618649c5e9dfb23d07d03b82910c691492bd60b30772c1bb6c520f0afa
```

## 2026-09-02 early-prune 修订后的最新远程观测

当前 `theory-lab/s1_crowding/translated_sumset_csp_pilot.py` SHA-256 为
`005f506ac32fa77d2aa7da37a60c37fbb6c637802b281ca010f75aad81acfac8`。新版把
known occupied 的碰撞与 x-high 越界检查提前到 DFS 层，故新版应读取
`occupied_prune_rejects`，不与旧版 `occupied_rejects` 混比。
Geo scratch 中实际用于回归的
`remote_scratch/translated_sumset_positive_control_20260902/translated_sumset_csp_pilot.py`
已核对为同一 SHA；正式 checkout 根目录下未发现独立副本，后续运行须随脚本副本记录 hash。

Geo Workstation 对同一真实 `delta=284,m=16,r=8` structure-bearing shape 的
occupied-v3 回归为：`status=NODE_LIMIT`、`nodes=500001`、`tested_s=159`、
`occupied_prune_rejects=5332120`、`occupied_rejects=0`、`high_high_passes=17201`、
`xhigh_out_of_range_rejects=15`、`bfs_check.ok=true`、`pair_count=120`。结果
SHA-256 为 `13972f40ba78216367c3389e0d3e9723def965acafbb2611360334c9ff594502`。
这只是限额前缀的必要条件剪枝测量，不是完整排除。

同一批次的 `delta=285,m=15,r=9` occupied-v3 文件为空，记为
`OUTPUT_MISSING/TIMEOUT`，没有可用计数；不写成零结果，也不因空文件重启。
Hoffman2 arrays `115848/115912/115949/115950` 仍只读观察，未取消、重启或改参数。

当前 production gap 仍为：完整 immutable `delta=284/285` structure/depth corpus、
可复跑 provenance，以及真实 survivor 的 zero-false-reject differential。

## 2026-09-02 可选 exact low-low 剪枝

post-processor 新增 `--include-low-low`（默认关闭），在 DFS 每次加入新低深度时
计算与已加入低点的真实 low-low 距离 `l_i+l_j-2l_lca(i,j)`；越界、与已有
H/T/occupied 值冲突或新生成 low-low 距离重复时立即拒绝。它是距离单射的直接
必要条件，尚无 production 收益结论。

当前脚本 SHA-256：
`f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`。目前只完成
无副作用语法检查，尚未在 Geo Workstation 做 genuine-control 回归；下一步必须先
用同一 SHA 的远程副本在 order-6 genuine control 上确认 witness 保留和
`bfs_check.ok=true`。

## 2026-09-02 exact low-low genuine-control 回归

Geo Workstation 单进程、`nice -n 15 timeout 30` 回归命令：

```text
python3 translated_sumset_csp_pilot.py --delta 11 --lowpar= \
  --struct=-1,-1,1,1 --node-limit 100000 \
  --include-known-occupied --include-low-low
```

脚本 SHA-256 为 `f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`，
输出 `result.json` SHA-256 为
`1a206bcfc3814fe13e1d0224e353dc8cd809feed7231f5907df7f905c2c387cb`。
远程返回 `RC=0,status=COMPLETE,nodes=1,tested_s=11,high_high_passes=1`，已知
`s=8,L=0` witness 保留；`low_low_prune_rejects=0`、`occupied_prune_rejects=2`、
`xhigh_out_of_range_rejects=3`，且 `bfs_check.ok=true,pair_count=6`。该结果为
`VERIFIED GENUINE POSITIVE CONTROL / INTERFACE CHECK`，不构成 284/285 生产收益或
全局证明。

## 2026-09-02 low-low 双低点人工接口控制

因 order-6 genuine control 只有一个 low 点，Geo Workstation 另运行极小双 low
点人工控制（单进程、`nice -n 15 timeout 30`）：

```text
python3 translated_sumset_csp_pilot.py --delta 10 --lowpar=0 \
  --struct=-1,-1,-2 --node-limit 100000 \
  --include-known-occupied --include-low-low
```

脚本 SHA-256：`f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`；
`result.json` SHA-256：
`2e2d6a07bbd837e2ca9b35f8cd2741cee440ed8b4a2b6e2d7b0dd045e7eeb5e2`。
结果 `RC=0,status=COMPLETE,nodes=2,tested_s=9,high_high_passes=1`，保留
`s=9,L=[0,1]`；`low_low_prune_rejects=0`，`bfs_check.ok=true,pair_count=3`。
这是人工接口正控，不是 Leech-tree 全局结论。

## 2026-09-02 low-low 负向碰撞控制

Geo Workstation 对三 low 点路径做单进程负向接口控制（`nice -n 15 timeout 30`）：

```text
python3 translated_sumset_csp_pilot.py --delta 10 --lowpar=0,1 \
  --struct=-1 --node-limit 100000 --include-low-low
```

脚本 SHA-256：`f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`；
`result.json` SHA-256：
`16a494516c769a9d3acdcbb4b711d73eefc2437fb95d8a5e100ccc2c332a93f3`。
返回 `RC=0,status=COMPLETE,nodes=152,tested_s=8,high_high_passes=100`，
`low_low_prune_rejects=20`；保留 witness 的 `bfs_check.ok=true,pair_count=0`。
这确认重复/冲突 low-low 分支会被拒绝，但不是 Leech-tree 结论。

## 2026-09-02 latest remote observation after low-low controls

只读 `squeue` 显示当前 Hoffman2 队列按 job name 聚合为 `s1dep RUNNING=64`、
`s1dv7 RUNNING=36`、`s1dv7 PENDING=2`；未执行取消、重启或参数修改。该状态
不能替代最终输出文件和 coverage 标记。

Geo Workstation 上另有其他会话留下的 8 个 `abstract_class_search7` 进程，均在
`/home/geo/codex-work/leech-trees/theory-lab/s1_crowding`、约 100% CPU；本轮未
启动、停止或修改它们，按“保留已有远程作业”处理。此前新增的 low-low 控制进程
已退出，未发现由本轮留下的 translated-sumset 孤儿。

## 2026-09-02 parity + Wiener first-moment 三对象远程小批次

独立检查器 `theory-lab/s1_crowding/parity_moment_audit.py`（Geo SHA-256
`4233494c26a3504604785c55de7f855e705b5a0b7a33a7cf9e65e633a8ed3d96`）从
`lowpar+hpar+(s,L)` 建立加权树，交叉检查 parity、cut first moment 与直接 BFS
pair-sum。order-6 genuine：`all_checks_ok=true`，`cut=direct=target=120`、
`parity_ok=true`，结果 SHA
`5c8fabd00ef2efc449f4fab1761d51831728f7aeab266616fece1422246f2cdd`。

r8 `delta=284,s=158,L=[0,18,40,41,51,59,88,92]`：
`parity_ok=false (154 vs 150)`，第一矩 `47194 != 45150`，cut 与直接 BFS 一致；
结果 SHA `d50ef4f291e9831cc498e0f398d8086e871257e414d3ba2ea73655f44c271451`。
r9 `delta=285,s=157,L=[0,13,1,2,3,24,33,77,101]`：
`parity_ok=true (150)`，但第一矩 `47064 != 45150`，cut 与直接 BFS 一致；结果
SHA `eefefa59e95b0993a24ab3f94b0f23f6cef6ae6041b7a7f7504aefc4ad51272b`。

上述只排除两个具体候选，不构成 284/285 全域结论；生产接入仍需冻结 corpus、
bounded-DFS 计数和 zero-false-reject differential。

## 2026-09-02 当前脚本 hash 更新说明

随后仅修正 `translated_sumset_csp_pilot.py` 顶部 docstring，使 occupied/low-low
选项说明与实际 CLI 一致，算法逻辑未变。当前脚本 SHA-256 为
`93bca2c36c12baeb2361e78a438cadaf673fd250ca94971d5927d79d5783db2a`。之前控制
输出仍对应各自记录的 `f5b91b…` 版本；新运行必须重新记录 source hash。

## 2026-09-02 Fable 接手加审计文档

已新增可直接交给 Fable 的自包含接手与对抗审计文档：
`docs/fable-handoff-audit-new-ideas-2026-09-02.md`，SHA-256 为
`b1132751052779568e57a772abaf4d43cf12ee3b74463c0b3b585e10588631c3`。
文档要求先只读核对当前 frontier，再独立审计 translated-sumset、occupied/low-low、
component-mass/depth-Hall 和 parity + Wiener 路线，并优先寻找可写成统一 lemma 的
更短路线。它明确保留本机禁算、远程最多 4 workers、既有远程作业只读观察和严格
`VERIFIED/REPRODUCED/FINITE-EVIDENCE/CANDIDATE/UNKNOWN` 证据边界。

## 2026-09-02 远程作业只读轮询

在交接文档写入后进行了一次只读状态检查。Geo Workstation `geo-workstation` 上，
原有 8 个 `abstract_class_search7` 进程仍在运行（4 个约 99.6--99.7% CPU，4 个
为其 `/usr/bin/time` 父进程），启动时间均为远程 `2026-09-01 22:59:31 PDT`；
本轮未启动、停止或修改它们。`v7_r8/` 当前仍只有空的 `.tmp/.time` 与空
`driver.log`，没有新的完整结果，故继续记为未冻结输出而非零结果。

Hoffman2 `squeue` 只读观察到：`115848` 的 `s1dep` 数组仍运行，`115912` 的
`s1dv7` 有运行项且另有项因 `QOSMaxJobsPerUserLimit` 排队；`115949/115950`
仍按既有状态保留。没有取消、重启或改参数。由于没有新增冻结的 284/285
structure/depth corpus，本轮不启动 parity/Wiener 新计算；production gap 保持不变。

## 2026-09-02 23:19 PDT 复核

对同一批远程句柄再次只读轮询：Geo 上 PID `614006,614008,614009,614010` 的
`/usr/bin/time` 包装进程及 PID `614011--614014` 的实际搜索进程仍存在，已运行约
18 分 53 秒；实际搜索进程约 99.6--99.7% CPU。`v7_r8/` 文件仍全部为 0 字节，
没有可冻结输出。Hoffman2 的 `115848` 仍为 `RUNNING`，`115912` 同时有
`RUNNING` 与因 `QOSMaxJobsPerUserLimit` 的 `PENDING` 项。该次复核未改变任何远程
作业或参数，当前 production gap 不变。

## 2026-09-02 23:20 PDT 远程句柄复核

再次对同一批远程句柄做只读轮询：Geo 的 PID `614006,614008,614009,614010`
及 `614011--614014` 仍存在，`v7_r8/` 的 `driver.log`、`.tmp`、`.time` 文件
仍为 0 字节，未出现可冻结结果。Hoffman2 聚合状态仍为 `s1dep/RUNNING=64`、
`s1dv7/RUNNING=36`、`s1dv7/PENDING=2`。本轮未改变任何作业；由于没有新产物，
不启动新的 presolver 计算。

## 2026-09-02 Hoffman2 `s1abs` 新结构产物（只读取得）

Hoffman2 上已完成的一批 `s1abs` 任务产生了新的 `m=14,r=10` abstract
structure 层结果。按源码中的 `delta=C(24,2)+r` 公式，这对应 `delta=286`，
不是当前尚未闭合的 `delta=284/285`。远程源文件
`abstract_class_search.cpp` SHA-256 为
`5a0a726cc1d3280792ebbfc59d9809058fe7f67c28d19ca31b52a7fe1ca2b8ea`，与正式
checkout 中同名源文件一致。

已只读复制到本地 scratch 的聚合文件：
`remote_scratch/hoffman_abstract_20260902/all_sorted.txt`，SHA-256
`2f91a166a5ca9adfbbac0445782358c0ec7b9149e49e3d30aacef40ffac21723`。
远程另见 `shapes_r10_exists.txt`，其观察到的 SHA-256 为
`1af7ff9ffe6f42ad25fccbbc4d0d2337fc6bc0db126348984cde3b0cf0a25fa0`；因连接
随后中断，尚未复制到本地。

对聚合文件做了轻量独立审计：719 条 `ABSTRACT` 记录中 317 条为 `EXISTS`、
402 条为 `EXHAUSTED`；低树形状键 719 个且无重复；32 条分片汇总覆盖 shard
`0..31`；每条汇总均有 `iso_classes=719`，`shapes_run + skipped_other_shards`
为 719，`shapes_run + skipped_other_shards + skipped_iso` 为 362880=`9!`，
且汇总 `total_leaves` 总和为 317。当前可标为
`FINITE-EVIDENCE / STRUCTURE-ONLY / PROVENANCE-INCOMPLETE`：结果显示
`delta=286` 的 abstract 层有完整终止记录，但尚未独立取得每个分片原始输入、
作业命令和编译二进制哈希，不能升级为正式证书，也不能外推到 `delta=284/285`。

Hoffman2 `115950` 已显示 `COMPLETED`，新的 `118375`（`s1dv7`）仍有运行项；
Geo 上旧的 `abstract_class_search7` 任务仍在运行。本轮没有取消、重启或修改
任何远程作业；对新 `delta=286` 结果暂不启动额外计算，先保留为寻找跨层结构
不变量的资料。

## 2026-09-02 `delta=286` 聚合文件独立一致性审计

新增轻量审计器
`theory-lab/s1_crowding/audit_abstract_aggregate.py`，SHA-256 为
`b0f4be3ba27173fbbd39c01081625746bbbb26bd8fbc2293b66ed397bdbda7ef`。它只解析
文本，不枚举树；对本地复制的 Hoffman 聚合文件运行后生成
`remote_scratch/hoffman_abstract_20260902/audit.json`，SHA-256 为
`6c26483fe6a6649fee476a8f32fa89428b8a27fdfaf02f424d0afc663b30df0e`。

审计结果 `all_checks_ok=true`：无解析错误；719 条记录的 lowpar 唯一；
`EXISTS=317`、`EXHAUSTED=402` 完整分割；32 个 shard 恰为 `0..31`；每条
summary 的 `iso_classes` 与记录数一致；每条 summary 的 primary coverage 为
719；加上 `skipped_iso` 后的原始计数为 `362880=9!`；`leaves` 总和为 317 且
与状态一致。该结果仍只证明聚合文本的内部一致性，不能替代每个分片原始输入、
作业命令、编译二进制和深度阶段证书，因此证据等级保持
`FINITE-EVIDENCE / STRUCTURE-ONLY / PROVENANCE-INCOMPLETE`。

此前 Fable 文档在加入 demand-span 补充后的 SHA-256 为
`97f3228a63b32cee4b200a3480723e32b70719041468e7f3b053eac258e0114c`；本轮加入
顾问与 r10 pilot 附录后的当前 SHA-256 为
`1ac01b37a5622941ecdca9482462ca91c5b3ed8cf9be6f5a396ab1885cc052d1`。更早的
`757ca884...` 与 `b1132751...` 分别是此前版本哈希。

## 2026-09-02 `delta=286` 作业脚本 provenance 补充

本地保存的 `theory-lab/s1_crowding/hoffman2_s1_abstract_array_slurm.sh` 明确了
该批次的调用模板：`sbatch --array=0-31 ... <r> <NSHARDS>`，其中 `r=10`、
`NSHARDS=32`，每个 task `--cpus-per-task=1`、`--mem=2G`、`--time=23:50:00`，
并执行 `./abstract_class_search --m 14 --r 10 --all-shapes --stop-first
--shard K 32 --nodes-limit 100000000000`。脚本 SHA-256 为
`95a56eff9a5a5bbf8fa2d3d03f9dcca43a28d2cf0f999ac33d1ac832d2a24ac2`。这闭合了
作业参数模板，但仍不等于已取得远程编译二进制哈希或每个原始分片的独立复制，
所以 `delta=286` 证据等级继续保持 `PROVENANCE-INCOMPLETE`。

## 2026-09-02 demand-span 容量引理草稿

新增 `docs/demand-span-lemma-audit-2026-09-02.md`，把 low-LCA 类的平移和集合
`T_v=2B-2l_v+S_v` 写成跨类争槽问题。对任意 low-class 子集 `Q`，区间包络给出

```text
Σ_{v∈Q} P_v <= C0 + 2(max l_v - min l_v),  C0=2m-3,
```

并与 high-LCA 类合并得到
`W+P_v <= C0+min(C0,2(B-l_v))`。这两个式子在 raw-sum 无重复、深度顺序、
`0<=l_v<B`、`W+ΣP_v=C(m,2)` 等前提下是 **VERIFIED necessary direction**；
通过不代表存在，跨 LL/LH/holes 仍未覆盖。工程收益和 production 接入仍为
**CANDIDATE**，须在 genuine positive controls 与冻结的 r8/r9 structure 上做
zero-false-reject differential。

源码语义复核补充：`abstract_class_search.cpp` 将每个 low-LCA 类的 raw sums
保存在 `class_sums[i]`，并在 `csp_take` 中逐项检查重复/越界；因此 demand-span
引理中的 `|S_v|=P_v` 只对已通过同类 collision 检查的候选成立。若 raw sum
重复，应先拒绝而不能静默集合去重。该语义与新草稿的边界条件一致。

草稿文件 SHA-256：
`db511174370e8d6f3be3770d9d21d652b91fb5f1997c0eef9c8fdb5781107612`。

## 2026-09-02 23:36 PDT 远程状态与顾问委托复核

只读复核确认 Geo Workstation `geo-workstation` 仍可连接；既有 8 个
`abstract_class_search7` 进程（4 个 `/usr/bin/time` 包装进程及 4 个实际搜索进程）
仍在运行，命令参数和低优先级设置未改变。`v7_r8/` 仍未出现新的非空冻结结果。
本轮没有启动、停止、重启或修改任何远程作业，也没有在本机运行枚举或长计算。

已向普通 Chat 顾问 `Leech tree chat2`（thread ID
`6a95495c-3670-83ea-8e71-9bc4f67a0d15`，backing kind `chatgpt`）发送有界只读任务
`CONSULT-20260902-014`，要求审阅 `delta=286` 结构证据，并比较
translated-sumset difference CSP、demand-span、parity/Wiener 和 component-mass/Hall
能否形成统一 lemma。顾问回复仍待取得；未将其口头结论写入 proof state。

## 2026-09-02 23:50 PDT 顾问回收与 r10 结构审计 checkpoint

普通 Chat 顾问 `Leech tree chat2`（thread ID
`6a95495c-3670-83ea-8e71-9bc4f67a0d15`，backing kind=`chatgpt`）已完成
`CONSULT-20260902-014`。其最有价值的建议是把 translated-sumset、parity、
moment 和 Hall 约束统一成 **colored moment-Hall completion lemma**：固定
abstract structure 后保留精确的 `H`、各 `S_v`、差集 `S_i-S_j`、深度平移和
Wiener 仿射式；Hall/moment-Hall 失败可给出 sound necessary impossibility，
通过只表示“未被排除”。顾问明确指出：当前没有证据证明所有 `r=8/9/10`
structure 均 UNSAT；仅用 component mass 或 `(W,P)` 不足以闭合，且给出了保留
差集信息的最小反例。该回复已作为研究建议记录，不视为定理或最终证明。

在 Geo Workstation 冻结的 `m=14,r=10` 结构为
`lowpar=0,0,0,0,0,1,6,7,8`，得到
`STRUCT -1 -2 -7 -8 -9 -10 -10 -10 5 -9 -8 -7 -2 -1`，命令正常结束
（`RC=0`，`leaves=1`，`nodes=7173`）。远程二进制 SHA-256 为
`5270bd212a93e786549c1fd6f1e9da399b7c94b0d6f582042f8e278be949799e`；结构输出
SHA-256 为 `97cf0a8a656ebbb25b41de745dbb4bb5790c4bbe228ab4c6012d28ed8417e9e5`，
计时文件 SHA-256 为 `493d9e475af01b5379559979f0f7a8aa8920e403b9d544998961c9c743d00b5a`。

对该冻结结构完成了不枚举 `(s,L)` 的轻量审计：
`theory-lab/s1_crowding/colored_moment_hall_audit.py`（SHA-256
`dde5c4cebdf62cff40e97c0313f225efb69fdbf58c343cbe913e390ba755fd8a`）生成
`remote_scratch/demand_span_r10_20260902/colored_audit_v1/colored_audit.json`
（SHA-256 `3ea46c2c7dc74c7167947fbd49c3c586be9222d0b39908d35ca5ffb3754d6a38`）。
结果 `partition_ok=true`、`H_unique=true`、所有 `S_v` 内部唯一，
`W=1`、`P=[25,21,0,0,0,0,17,13,9,5]`、`pair_total=91`，并得到固定结构的
Wiener 仿射系数；这是 **VERIFIED structure-only necessary audit**，不是存在性
或深度排除证明。

同一结构上的旧 translated-sumset 全搜索基线在 Geo Workstation 以
`nice -n 15`、120 秒上限运行，最终 `RC=124`，JSON 为空（SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`），计时文件
SHA-256 `13de623a95fea8e111fc34eb3398e4ce5770b176a2c2adee078ce51303aab672`；
轮询确认没有残留新进程。因此该路线只能标为 **TIMEOUT / OUTPUT_MISSING / GAP**，
不可解释为“没有 survivor”，也不应重复同一路径。Geo 上原有的
`abstract_class_search7` 作业仍在运行，本轮未取消、重启或修改；Hoffman2 的
既有数组也未触碰。当前没有新的 `delta=284/285` 结果。

当前最小未闭合缺口：把上述结构层必要系统扩展到真实 `(s,L)` 的 sound、可终止
presolver，并用 genuine positive controls 验证 zero-false-reject；随后才有资格
对 `delta=284/285` 的完整 structure/depth corpus 做远程批处理。全局猜想仍未证
明，现有结果不能升级为 publication-level theorem。

## 2026-09-02 顾问 `CONSULT-20260902-016` 回收与安全边界修正

普通 Chat 顾问 `Leech tree chat2`（thread ID
`6a95495c-3670-83ea-8e71-9bc4f67a0d15`，kind=`chatgpt`）在一次短重试后返回了
完整审阅。其结论是：把固定 structure 的
`H,S_v,S_i-S_j` 压成小型整数域传播器，联合 exact translated-difference、
colored Hall、colored moment-Hall、全局 parity 和 Wiener affine equality；这是
**CANDIDATE，但规格可以完全 sound** 的必要条件 presolver。任何一层失败只能对
当前固定 structure 与 `(s,L)` 域判 `UNSAT`；全部通过只能写 `NOT-EXCLUDED`。

顾问明确补充了以下 sound 量词：`A_q` 必须是实际距离集合的超集；对任意 class
子集 `Q`，`D_Q <= |∪A_q|`；parity 版本分别限制偶/奇槽位；moment 版本用允许
集合中最小/最大 `D_Q` 个槽位和夹住精确 class sum。Wiener 仿射式在完整 `(s,L)`
不满足时可判 `UNSAT`，部分赋值只有有严格区间或 gcd 证书时才可提前剪枝。
occupied 只有在确定属于其它 unordered pair owner 时才能删除，owner 内部重复必须
拒绝，不能先 `set()` 静默去重。

顾问给出的最小 differential 集合为：已知 order-6 genuine `s=8,L=[0]` 正例、
人工双-low 正例（检查差集符号/平移/parity）以及人工三-low 负例（分别制造
exact-difference、Hall、moment-Hall 失败）。这只验证零误删与故障定位，不构成
`delta=284/285` 生产证明。最值得 Fable 实现的最小模块是只生成 structure
certificate 的 `translated_difference_domains`：输出 `H,S_v,P_v`、raw sums、
parity counts、`S_i-S_j` forbidden differences 和 Wiener 系数，不搜索 `(s,L)`。

本轮还修正 `theory-lab/s1_crowding/translated_sumset_csp_pilot.py` 的一个安全
边界：启用 occupied 时，hole owner 的距离 `s+l` 若超出 `[1,delta]`，现在明确
拒绝并计入 `hole_out_of_range_rejects`；此前只是忽略该值，属于漏剪枝而非误删。
脚本仅做语法检查（`python3 -m py_compile`）和 `git diff --check`，当前 SHA-256
为 `4e14150bf84817a448f419e76a385fa52e2c9891397a83eab2755ce662ed28d0`。没有运行
搜索，没有修改 production 计算，没有触碰任何远程作业。

本轮随后新增独立结构证书工具
`theory-lab/s1_crowding/translated_difference_domains.py`，只调用结构重建并
输出 `H/S/P`、raw-sum 差集、对应的偶数深度禁配值（将 raw difference 正确除以
2）和 Wiener 系数；不枚举 `(s,L)`。对冻结 r10 structure 做了一个 91-pair
轻量复核：`partition_ok=true`、`H_unique=true`、所有 `S_v` 内部唯一、
`W=1`、`P=[25,21,0,0,0,0,17,13,9,5]`，断言通过；结果为
`STRUCTURE_CERT_OK`。该工具当前 SHA-256 为
`98aefed17c6f104dec8254946aa3d8bfa9963a37ec83c9304b456c4fcfe0d007`。
这是结构层证书生成与接口验证，不是 depth 或全局非存在性证明。

随后将该只读工具复制到 Geo Workstation scratch，并以 1 worker、
`nice -n 15`、30 秒上限运行同一个冻结 r10 structure；实际耗时约 0.05 秒，
输出已回收为
`remote_scratch/demand_span_r10_20260902/colored_audit_v1/translated_difference_domains.remote.json`，
SHA-256 为
`96aca92b8f4c22a11134034c6ddf84b7ba7cd9a08b27e7a9374fdd40d27ab0a1`。独立解析断言
`partition_ok=true`、`H_unique=true`、所有 `S_v` 内部唯一、`pair_total=91`、
`W=1`、`P=[25,21,0,0,0,0,17,13,9,5]`，输出状态
`TRANSLATED_DIFFERENCE_STRUCTURE_CERTIFICATE`。这是远程 provenance 加固和
结构接口复核，不是 `(s,L)` 搜索或全局证明；运行后未留下 pilot 进程。

## 2026-09-02 远程只读复核

Geo Workstation `geo-workstation` 当前可连接。既有 8 个 `abstract_class_search7`
进程（4 个 `/usr/bin/time` 包装进程及 4 个实际搜索进程）仍按原参数、
`nice -n 15` 运行；`translated_sumset_csp_pilot` 没有残留新进程。scratch 中
最近文件仍是已登记的 `struct.out`、空的 translated baseline 和
`colored_audit_v1/colored_audit.json`，没有新的 `delta=284/285` 产物。本次只读
轮询未启动、停止、重启或修改任何远程作业。

## 2026-09-02 顾问代码复核状态

已向同一普通 Chat 顾问发送 `CONSULT-20260902-017`，要求只读审计新结构证书
工具和 hole 越界修正。截至本 checkpoint，线程仍为 idle、仅有该用户消息而无
`agentMessage`；因此按 `OUTPUT_MISSING` 记录，未把它当作证据，也未继续重复
发送。已有 `CONSULT-20260902-016` 的完整审阅仍是当前采用的外部建议来源。

## 2026-09-02 r8/r9 单结构证书补强

复查远程 scratch 后确认，先前已有的两个单结构 translated-sumset 结果仍分别为
`delta=284,m=16,r=8` 与 `delta=285,m=15,r=9`，且均为 `NODE_LIMIT`，不能当作
完整排除。为补足当前结构证书 provenance，在不触碰这些搜索结果的前提下，将
`translated_difference_domains.py` 复制到各自 Workstation scratch，以单进程、
`nice -n 15`、30 秒上限重放结构层证书。

远程证书均正常结束并与本地断言一致：

```text
delta=284: pair_total=120, W=1,
  P=[29,25,0,21,17,13,9,5]
  structure_certificate.remote.json
  SHA-256 6c31fa385a75d9292a7a4d06dbfd039738cfcbcc84e1c05c54c6f9f75abf9a8c

delta=285: pair_total=105, W=6,
  P=[27,23,0,0,0,19,15,11,4]
  structure_certificate.remote.json
  SHA-256 c3a7914bdc95f95ec3dfeeb0c973f2b88fb8f32460b5a733383c64e1bc331578
```

两份输出均验证 `partition_ok=true`、`H_unique=true`、所有 `S_v` 内部唯一；
这只加强结构层可复现性，不改变两个深度 pilot 的 `NODE_LIMIT/UNKNOWN` 等级，
也没有产生新的 284/285 全局结论。

## 2026-09-02 Fable 当前版接手＋对抗审计文档

新增自包含委托文件
`docs/fable-takeover-audit-current-2026-09-02.md`（SHA-256
`39217e5e0286e983a1027c4a3da2096bd5019fbb0ab817e4da2c123439047477`）。该文件面向
Fable，重新整理当前证据等级、结构层对象、colored moment-Hall / difference-domain /
demand-span 候选路线、最小 zero-false-reject 验收集、Geo Workstation 资源边界和
交付格式。它明确要求 Fable 主动寻找更短的统一引理或给出最小反例，并禁止把
`NODE_LIMIT`、timeout、空输出、单 shape 或顾问口头判断升级成全域证明。

本轮只写入该 handoff 并做哈希/`git diff --check`；没有启动本机或远程重计算，
没有修改、重启或取消既有远程作业，也没有提交或推送。

## 2026-09-02 colored moment-Hall presolver 固定 witness 回放

新增并修正后的 `theory-lab/s1_crowding/colored_moment_hall_presolve.py`（当前
SHA-256 `edf3a11672175862c085776e61a97f36cee1ce6d9fdc483b40f006791b625717`）先做
本机轻量语法检查，并以已知 order-6 genuine L6 参数
`lowpar=`, `hpar=-1,-1,1,1`, `delta=11`, `s=8`, `depths=0`, `order_n=6`
回放。输出 `necessary_pass=true`、`interpretation=NOT-EXCLUDED`，Hall、
parity-Hall、moment-Hall、全局奇偶（`8=8`）和 Wiener（`120=120`）均通过；这
只是零误删正控，不是 284/285 结论。

随后把同一脚本复制到 Geo Workstation checkout
`/home/geo/codex-work/leech-trees` 的两个既有 scratch 目录，以单进程、
`nice -n 15`、30 秒上限回放各一个冻结 witness；没有触碰已有
`abstract_class_search7` 作业：

```text
r8  delta=284, m=16, r=8
    lowpar=0,0,1,3,4,5,6
    STRUCT=-1,-2,-4,-5,-6,-7,-8,-8,-8,6,-7,-6,-5,-4,-2,-1
    s=158, depths=0,18,40,41,51,59,88,92
    RC=0, exact_translation=true
    global parity: 154 != 150 (false)
    Wiener: 47194 != 45150 (false)
    interpretation=UNSAT_FOR_THIS_CANDIDATE
    output SHA-256=924f0b1726a3c773368e72befefbd4dd8e91bdd6f93987310723151cd623ea9a

r9  delta=285, m=15, r=9
    lowpar=0,0,0,0,1,5,6,7
    STRUCT=-1,-2,-6,-7,-8,-9,-9,5,5,5,-8,-7,-6,-2,-1
    s=157, depths=0,13,1,2,3,24,33,77,101
    RC=0, exact_translation=true
    global parity: 150 = 150 (true)
    Wiener: 47064 != 45150 (false)
    interpretation=UNSAT_FOR_THIS_CANDIDATE
    output SHA-256=14b61855918da2a6ea7ccad333e25aa8ad6492ed6830b971ee016dbd40334de4
```

两次回放均 `H/T` 内部唯一、互斥、范围和 Hall/parity-Hall/moment-Hall 通过；
r8 由全局奇偶和 Wiener 双重拒绝，r9 由 Wiener 拒绝。它们只排除各自的一个
固定 `(structure,s,L)`，不能外推为整个 structure、`delta=284/285` corpus 或
全域猜想的证明。当前下一步应是：先完成人工双-low/三-low differential，确认
presolver 的 failure-layer soundness，再评估是否值得远程批量；不要因这两个
witness 被拒绝就重跑旧的 `NODE_LIMIT` 路线。

## 2026-09-02 presolver failure-layer 字段与重放

为便于审计，在 `colored_moment_hall_presolve.py` 输出中新增
`failure_layers`，按 `exact_translation`、`hall`、`parity_hall`、`moment_hall`、
`global_parity`、`wiener` 列出实际失败层；算法条件未放宽。当前脚本 SHA-256 为
`d9192dad56c30d3bc01be0c494d7dc82b8eb2d495b6dc8f391caa877b206efef`。

重新做了本机 order-6 L6 正控，仍为 `NOT-EXCLUDED` 且 `failure_layers=[]`。
随后将同一脚本复制到 Geo Workstation，并以单进程、`nice -n 15`、30 秒上限重新
回放两个固定 witness：

```text
r8: RC=0, exact=true, failure_layers=[global_parity,wiener]
    odd_pairs=154 vs target=150; Wiener=47194 vs 45150
    output SHA-256=7d8a193439e770d784ae5de24245bef7a41fbbb69ab6925e676779cd44cf4c35

r9: RC=0, exact=true, failure_layers=[wiener]
    odd_pairs=150 vs target=150; Wiener=47064 vs 45150
    output SHA-256=71ace6f9e6e9b22754892e385998bba63119dbd03db2d5f998ab52ec34a102b3
```

两次重放的 `H/T` 范围、内部唯一性、互斥、Hall、parity-Hall、moment-Hall 均通过，
且远程未留下 presolver/pilot 孤儿。该字段只改善 provenance 和失败定位；r8/r9
仍仅是固定候选的必要条件排除，不改变全局 `delta=284/285` 证据等级。

## 2026-09-02 presolver 层级审计：完整候选时 Hall 是冗余的

对固定完整 `(structure,s,L)`，若 `exact_translation` 已通过，则每个精确类集
`H,T_v` 都是互不相交的、大小分别为 `W,P_v` 的实际槽位集合，并且各自包含于
对应的允许超集 `A_H,A_v`。因此对任意类子集 `Q`，Hall 容量、parity-Hall 容量
和 moment-Hall 极值不等式按集合包含关系自动成立。换言之，当前 presolver 在
“完整候选”模式下的 Hall/moment 层不会比 exact `H/T` 再排除更多；它们的真正
价值在于未来把 `A_q` 作为**部分 low-depth 域**传播器时提前剪枝。

本机对 order-6 L6 的全部 `s=1..11` 做了轻量性质检查：11 个参数中 3 个
`exact_translation` 通过，所有这些通过者均无 Hall/parity-Hall/moment-Hall
失败（`counterexamples=0`）。因此下一版设计应把“完整候选审计”和“部分域传播”
分成两个接口，并避免把完整候选的冗余层误写成额外独立证据。该观察不削弱
global parity 或 Wiener，它们仍可在 exact 通过时独立拒绝候选。

## 2026-09-02 顾问通道回收状态

曾向 `Leech tree chat2` 发送 `CONSULT-20260902-018`，并向 `leech tree chat1`
发送 `CONSULT-20260902-019`，均要求只读审阅最新 presolver 和“完整候选时
Hall 冗余、部分域传播更有价值”的判断。截至本 checkpoint，两条普通 Chat
都只登记了用户消息，没有返回 `agentMessage`；因此均按 `OUTPUT_MISSING` 处理，
没有把它们当作证据，也没有因为缺少顾问回复而重试、换 Chat 或停止主线。当前
可依赖的外部数学建议仍是已回收的 `CONSULT-20260902-016`。

## 2026-09-02 部分 low-depth 域传播原型

为推进当前最小科学缺口，新增 scratch 原型
`theory-lab/s1_crowding/partial_depth_domain_audit.py`，SHA-256 为
`5443e8cc4a52f1b7f39826101bfa801d8666cd256bbe5ee9e062ffb48fcd7caa`。输入是每个
low vertex 的有限 depth domain；脚本不枚举域盒的深度组合，而对每个 `T_v` 取
所有域值对应的 translated-slot 并集。实现了 sound-by-construction 的必要层：
域盒内低深度注入、parent 顺序、pairwise forbidden difference、并集
Hall/parity-Hall/moment-Hall、全局奇偶可达值，以及 Wiener affine 的安全区间与
同余筛。失败才报告 `UNSAT_FOR_ALL_ASSIGNMENTS_IN_DOMAIN_BOX`；通过只报告
`NOT-EXCLUDED_BY_PARTIAL_DOMAIN_AUDIT`，不能当作存在性证明。

轻量验证（均未启动本机枚举或远程批量）：

```text
order-6 genuine L6: s=8, domains=0 -> failure_layers=[], NOT-EXCLUDED
r8 singleton witness -> [global_parity,wiener]
r9 singleton witness -> [wiener]
r9 全深度宽域 -> failure_layers=[], 说明宽域未被凭空判死
r9 窄域 12..14/1..2/1..3/2..4/23..25/32..34/76..78/100..102 -> [wiener]
```

当前结论：该原型适合作为未来 partial-domain 诊断/传播层，但尚未有独立
matching/differential oracle 证明，也尚未接入 production DFS；不得据此宣称
284/285 或全域非存在。Fable 的下一项最小任务是审阅其 soundness 引理并构造
人工双-low/三-low differential；若不能证明域盒整体拒绝的量词，应撤回剪枝，保留
为诊断工具。没有进行任何 284/285 批量计算。

- **2026-09-02 03:40 EDT 交接状态（Fable）：** `δ=284`（`r=8`）深度阶段在 Hoffman2
  数组 `118375`（64 片，`depthv7_r8/`）运行中：6 个非链状形状零幸存且与逐叶实现逐片一致，
  链状形状预计 12–20 小时完成；`δ=285`（`r=9`）数组 `118376`（256 片）运行中。验收用
  `theory-lab/s1_crowding/verify_depth_splits.py`（已在 `depth_r7chain/` 上返回
  `VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY`，证书 SHA-256 `32603c95…`）。`r=10`：317/719
  类有 depth-free 结构；`r=11`：1523/1842，纯 top-block 方法到此失效。geo-ws 上我的
  进程已全部停止。总报告：`docs/fable-audit-report-2026-09-01.md`。

## 2026-09-02 partial-domain 独立差分 gate

新增独立差分脚本
`theory-lab/s1_crowding/partial_depth_domain_differential.py`，SHA-256 为
`b41c061b84220f760bcdd8339a8c0dad52dce598f3b08a382b823cb6ea8c8131`。该 oracle
直接逐个检查具体 depth tuple，不导入 fixed-candidate `presolve`，用于验证域并集
审计不会拒绝一个具体必要系统 survivor。

本轮结果：

```text
genuine_L6_positive: 1 个 concrete survivor，域审计通过；
r8_singleton: 0 survivor，域审计 [global_parity,wiener]；
r9_three_value_box: 0 survivor（4,374 个 tuple），域审计 [wiener]；
soundness_ok=true
```

这只证明三个小型控制上的接口 soundness gate 通过，尚不等于数学完备性，也没有
启动 284/285 远程批量。下一步仍需 Fable 审阅量词、补充人工双-low/三-low
differential，并独立确认是否可把该原型安全接入生产搜索。

## 2026-09-02 partial-domain soundness 说明

对每个 low 类域 `D_v`，原型使用
`U_v = union_{l in D_v}(2B-2l+S_v) \\ (H union occupied)`。任何真实域内赋值的
`T_v` 都包含在 `U_v` 中，因此并集 Hall/parity-Hall 失败是域盒整体的必要条件
拒绝；真实类和落在代码的宽 `possible_sum_interval` 内，因此与可用槽最小/最大
`D_Q` 项和完全不交时 moment-Hall 拒绝也 sound。pairwise difference、深度注入、
parent 顺序、global parity 和 Wiener 区间/同余拒绝同理。并集会丢掉跨类相关性，
所以通过永远只写 `NOT-EXCLUDED`。

新增 parent-index 校验后，脚本 SHA-256 更新为
`66e11f8fffd7dc1b37505421692ae617b01d60c179a29518d164b0a76e784d7c`；重新编译、
独立差分和 `git diff --check` 均通过。没有启动本机枚举或 284/285 远程批量。

随后把已审计的 component-capacity 与 demand-span 必要条件接入同一 partial-domain
原型：使用 `W/P` 单类容量、low-class 子集的最大域跨度，以及 `H+L_v` 的端点上界。
这些都是宽上界，失败才可判域盒整体无解；通过仍是 `NOT-EXCLUDED`。重新编译和
既有独立差分仍为 `soundness_ok=true`，脚本 SHA-256 保持
`66e11f8fffd7dc1b37505421692ae617b01d60c179a29518d164b0a76e784d7c`。

补上 H/S 完整分割 guard 后，在同一 Geo Workstation scratch 重新复制并复跑
`partial_domain_v2_smoke_20260902`：单进程、`nice -n 15`、`timeout 60s`，
`RC=0 ELAPSED=3.34 MAXRSS=11732 KB`。回收文件
`remote_scratch/partial_domain_v2_smoke_20260902_result.v2.guard.json` 的
SHA-256 为 `02d515b68aa39ebe4d11008659f796d2ec39930fbd3a354fd4dd8c3598a6d578`，
内容仍为 `soundness_ok=true`，三项控制结果与前一版一致。没有触碰 Hoffman2 数组。

## 2026-09-02 顾问审阅任务 020

已向普通 Chat `Leech tree chat2`（thread ID
`6a95495c-3670-83ea-8e71-9bc4f67a0d15`，kind=`chatgpt`）发送
`CONSULT-20260902-020`，请其只读审阅 partial-domain 原型并寻找更好的 sound
路线。消息已登记，但截至本记录只有 `userMessage`、没有 `agentMessage`；按
`OUTPUT_MISSING` 处理，不把它当作数学证据，不重试、不换 Chat、不启动计算。

人工双-low/三-low 控制的层次审计：仓库中 `delta=10,s=9,L=[0,1]` 的双-low
正控和三-low 负控来自 translated-sumset/BFS 接口，并非完整 Leech 必要系统；
直接运行 partial-domain 全审计会因其不满足对应的 global parity/Wiener 目标而拒绝，
这不是误删。后续只应把它们用于 raw difference、平移互斥和 LL owner 的局部
zero-false-reject 检查；global parity/Wiener 仍须用 genuine positive control。

## 2026-09-02 Geo Workstation 只读状态复核

通过 `ssh -o BatchMode=yes -o ConnectTimeout=8 -o ConnectionAttempts=1 geo-ws` 做了
只读核对：主机返回 `geo-workstation`；当前 `ps` 没有匹配的
`abstract_class_search7`、partial-domain 或 translated-sumset worker。实际 checkout
`/home/geo/codex-work/leech-trees` 存在 14 个顶层项目项；`/home2/geo/codex-work/leech-trees`
存在但为空。远程 scratch 中最新可见的是已回收的 presolver v2 JSON；没有重启、停止、
修改任何远程作业，也没有启动新计算。

同轮对 `hoffman2` 做了单次只读查询：SSH 到达 `login1`，但 `squeue -u geo` 返回
`Invalid user: geo`，因此没有得到可靠的 Hoffman2 队列/输出状态。该结果仅记为
`REMOTE_STATE_UNRESOLVED`，不是作业完成、失败或空队列；没有重试、取消、重启或改动
任何远程作业。

## 2026-09-02 partial-domain v2 Geo Workstation smoke

将当前 `partial_depth_domain_audit.py`、独立差分脚本和依赖审计模块复制到
`/home/geo/codex-work/leech-trees/remote_scratch/partial_domain_v2_smoke_20260902/`，
仅运行一次：单进程、`nice -n 15`、`timeout 60s`。远程返回
`RC=0 ELAPSED=19.96 MAXRSS=11796 KB`。结果已回收为
`remote_scratch/partial_domain_v2_smoke_20260902_result.json`，SHA-256
`02d515b68aa39ebe4d11008659f796d2ec39930fbd3a354fd4dd8c3598a6d578`；三项控制
与本地一致，`soundness_ok=true`。这是接口级远程复现，不是 284/285 批量结果，
也没有触碰现有远程作业。

## 2026-09-02 Hoffman2 queue observation

使用正确账户 `lsmeng` 只读查询 Hoffman2：`118375`（r8/depthv7）为
`64 RUNNING`；`118376`（r9/depthv7）为 `36 RUNNING + 1 PENDING`，pending 原因
为 `QOSMaxJobsPerUserLimit`。`scontrol` 显示两者均运行
`hoffman2_s1_depth_v7_array_slurm.sh`，工作目录为
`/u/scratch/l/lsmeng/leech-trees/theory-lab/s1_crowding`。这是运行状态，不是最终
结果；没有取消、重启或修改作业。

当前临时输出的只读进度汇总：`depthv7_r8/*.txt.tmp` 有 384 行
`EXHAUSTED`，累计 `depth_survivors=0`、`structures_with_survivor=0`；
`depthv7_r9/*.txt.tmp` 有 216 行 `EXHAUSTED`，同样累计 survivor 为 0，且没有
`NODE_LIMIT` 或 `TIMEOUT` 字样。由于数组仍在运行且文件尚未原子改名为 `.txt`，
这只是中途进度观察，不能升级为完整 r8/r9 覆盖或全域非存在证明。

## 2026-09-02 Hoffman2 r8 首个完成分片验收

`depthv7_r8/split_10_of_64.txt` 已原子完成。新增
`theory-lab/s1_crowding/verify_depthv7_partial_shard.py` 在本地复制文件和
Hoffman2 原地各运行一次，均返回 `VERIFIED_PARTIAL_SHARD_EMPTY`：7 个预期结构
全部出现，末尾 `COMPLETE`，无 `NODE_LIMIT/TIMEOUT`，且
`total_depth_survivors=0`、`total_structure_survivors=0`。本地回收文件
`remote_scratch/hoffman2_depthv7_r8_partial_20260902/split_10_of_64.txt` 的
SHA-256 为 `d36bdb73344a7a4f319dd6c743804acf6ce1625d2f332f302389efe1b49aef0b`；
形状输入 SHA-256 为 `928f5f178e0f0848c8d1d45bbb0141f50cd46832932fc69344e2268fc816fb41`；
证书 SHA-256 为 `86c0450b9d77ac3ec604f19a2870be74d12cee326043f48876b3c9b94e2dd068`。
这只验证 r8 的 1/64 分片，不代表其余分片、r9 或全域证明。

同一数组的 `split_9_of_64.txt` 随后也原子完成，并在本地复制文件与 Hoffman2
原地各通过 `verify_depthv7_partial_shard.py`：7 个结构、末尾 `COMPLETE`、
`total_depth_survivors=0`、`total_structure_survivors=0`，无 `NODE_LIMIT/TIMEOUT`。
分片 SHA-256 为
`bde5093f4ecc2f7b216088aa494978af06b1c59cdfb0f804e59007b06a5b22dd`，本地回收
验收证书 SHA-256 为
`992a0a3a96b004b113bc451ee10fe90d01a2b14b304b61da5675507eecbf0b7b`。至此 r8
已有 2/64 个可验证空分片，仍不代表全数组覆盖。

进一步只读查看脚本确认：每个分片使用 `abstract_class_search7 --solve-depths
--max-witness 50 --split ...`，单 CPU、2G 内存、Slurm `nice=10000`，成功后才把
`.txt.tmp` 原子改名为 `.txt`。当前 r8/r9 可见的仍是 `.tmp` 文件，没有最终 `.txt`；
因此暂不读取或汇总任何分片为数学结果，等数组自然完成后再逐片验证。
- **2026-09-02 04:15 EDT 修正：** `δ=284` 链状分片实际约 2 小时/任务（首个完成的
  split 10：leaves=21496630、rho_csp_runs=653421、survivors=0），而非此前估计的
  12–20 小时；64 片预计 1–2 小时内全部完成。

## 2026-09-02 Hoffman2 r8 split 12/13 独立验收

只读轮询 Hoffman2 数组 `118375` 显示 r8 已有 4/64 个最终 `.txt` 分片、60 个
`.txt.tmp`；数组仍运行中。r9 数组 `118376` 仍有 0 个最终分片、39 个临时分片，
其余任务因 `QOSMaxJobsPerUserLimit` 排队。没有取消、重启或修改任何远程作业。

新完成的 r8 分片 `split_12_of_64.txt` 与 `split_13_of_64.txt` 已分别从
Hoffman2 回收，并在本地及 Hoffman2 原地运行
`verify_depthv7_partial_shard.py --m 16 --r 8 --split {12,13} --nsplit 64`。
两者均返回 `VERIFIED_PARTIAL_SHARD_EMPTY`：7 个预期结构、末尾 `COMPLETE`、
无 `NODE_LIMIT/TIMEOUT`，`total_depth_survivors=0`、`total_structure_survivors=0`。

```text
split_12 shard sha256 61e8dcf05a50595bfd03a016f5fa40c6f5f543d005255dcfbd12a3c6c00fb0ad
split_12 certificate sha256 5def33f340028724b11eecf321474d262bbe422e6114c84c44b20c15d429e005
split_13 shard sha256 55c164e9f092f9cb5e9f2c9324c193fa753f1b09792939e665245bba5eb636f2
split_13 certificate sha256 623e62a4095031ffce6b97733733aeaaa9d0bacf07521609264b1e2c2df69a94
```

这把 r8 的可验证空分片计数从 2/64 提高到 4/64；仍不是完整 r8 覆盖，也不是
`delta=284/285` 全域非存在证明。下一步保持只读等待最终文件，再逐片独立验收。

## 2026-09-02 Hoffman2 r8 split 8 独立验收

只读轮询显示 r8 数组 `118375` 已有 5/64 个最终 `.txt` 分片、59 个临时分片；
r9 数组 `118376` 仍有 0 个最终分片、41 个临时分片及 1 个排队任务。没有修改
远程作业。

`split_8_of_64.txt` 已回收至
`remote_scratch/hoffman2_depthv7_r8_partial_20260902/`，并在本地与 Hoffman2
原地通过 `verify_depthv7_partial_shard.py`：`VERIFIED_PARTIAL_SHARD_EMPTY`，
7 个结构齐全、末尾 `COMPLETE`、无 `NODE_LIMIT/TIMEOUT`，survivors=0。

```text
split_8 shard sha256 97dcee74e6242bb4982dd092cebc4ed10e51318990e96675393b4d490765f67b
split_8 certificate sha256 e2598b34994de3706c45d788b63a020f1282e0e66a46b2192ff61093880ea30b
```

这仍不是 r8 全数组覆盖；继续只读等待并逐片验收，不把中途计数写成全局结论。

## 2026-09-02 Hoffman2 r8 split 5 独立验收

只读轮询显示 r8 数组 `118375` 已有 6/64 个最终 `.txt` 分片、58 个临时分片；
r9 数组 `118376` 仍有 0 个最终分片、42 个临时分片及 1 个排队任务。没有修改
远程作业。

`split_5_of_64.txt` 已回收至
`remote_scratch/hoffman2_depthv7_r8_partial_20260902/`，并在本地与 Hoffman2
原地通过 `verify_depthv7_partial_shard.py`：`VERIFIED_PARTIAL_SHARD_EMPTY`，
7 个结构齐全、末尾 `COMPLETE`、无 `NODE_LIMIT/TIMEOUT`，survivors=0。

```text
split_5 shard sha256 88888ae52d01fbbcdd9c8a73936de07ab3b58c3bb53cbbb8c8c29d476ff4e37a
split_5 certificate sha256 ddacb7f72777b4fe40ebbecd466db4ee54ae30bea80c08a9bcbe560ef04811b2
```

这仍不是 r8 全数组覆盖；继续只读等待并逐片验收。

## 2026-09-02 Hoffman2 r8 split 7 独立验收

只读轮询显示 r8 数组 `118375` 已有 10/64 个最终 `.txt` 分片、54 个临时分片；
r9 数组 `118376` 仍有 0 个最终分片、46 个临时分片及 1 个排队任务。没有修改
远程作业。

`split_7_of_64.txt` 已回收至
`remote_scratch/hoffman2_depthv7_r8_partial_20260902/`，并在本地与 Hoffman2
原地通过 `verify_depthv7_partial_shard.py`：`VERIFIED_PARTIAL_SHARD_EMPTY`，
7 个结构齐全、末尾 `COMPLETE`、无 `NODE_LIMIT/TIMEOUT`，survivors=0。

```text
split_7 shard sha256 ac401f5da8ba5f5ec8457d305f4d19a0e3e07ab30ab6e59f8372d6a5a9dc6853
split_7 certificate sha256 083ac2db4238b78f5a0b2654e3b3305a93fc58f9aa5fe4690c7760ecccd568c6
```

这仍不是 r8 全数组覆盖；继续只读等待并逐片验收。

## 2026-09-02 Hoffman2 r8 split 4 独立验收

只读轮询显示 r8 数组 `118375` 已有 9/64 个最终 `.txt` 分片、55 个临时分片；
r9 数组 `118376` 仍有 0 个最终分片、45 个临时分片及 1 个排队任务。没有修改
远程作业。

`split_4_of_64.txt` 已回收至
`remote_scratch/hoffman2_depthv7_r8_partial_20260902/`，并在本地与 Hoffman2
原地通过 `verify_depthv7_partial_shard.py`：`VERIFIED_PARTIAL_SHARD_EMPTY`，
7 个结构齐全、末尾 `COMPLETE`、无 `NODE_LIMIT/TIMEOUT`，survivors=0。

```text
split_4 shard sha256 a1159ab1bc61d52710fe9609de26db8468e3963bfc27772fd28d5524eeb9f46e
split_4 certificate sha256 de3e9d9c275f86d9900bebdf1b9e9d534afbf8362100b8dd45d984eaae80bdd9
```

这仍不是 r8 全数组覆盖；继续只读等待并逐片验收。

## 2026-09-02 Hoffman2 r8 split 6 独立验收

只读轮询显示 r8 数组 `118375` 已有 8/64 个最终 `.txt` 分片、56 个临时分片；
r9 数组 `118376` 仍有 0 个最终分片、44 个临时分片及 1 个排队任务。没有修改
远程作业。

`split_6_of_64.txt` 已回收至
`remote_scratch/hoffman2_depthv7_r8_partial_20260902/`，并在本地与 Hoffman2
原地通过 `verify_depthv7_partial_shard.py`：`VERIFIED_PARTIAL_SHARD_EMPTY`，
7 个结构齐全、末尾 `COMPLETE`、无 `NODE_LIMIT/TIMEOUT`，survivors=0。

```text
split_6 shard sha256 d6b6778c2801bfbebea848919c1475ca7b0bb2e4b2a55e22d3296976ffb1940b
split_6 certificate sha256 afcf3b65c6fd4ecd227d569d658094408178e24603c93b042d859f27fb459362
```

这仍不是 r8 全数组覆盖；继续只读等待并逐片验收。

## 2026-09-02 Hoffman2 r8 split 11 独立验收

只读轮询显示 r8 数组 `118375` 已有 7/64 个最终 `.txt` 分片、57 个临时分片；
r9 数组 `118376` 仍有 0 个最终分片、43 个临时分片及 1 个排队任务。没有修改
远程作业。

`split_11_of_64.txt` 已回收至
`remote_scratch/hoffman2_depthv7_r8_partial_20260902/`，并在本地与 Hoffman2
原地通过 `verify_depthv7_partial_shard.py`：`VERIFIED_PARTIAL_SHARD_EMPTY`，
7 个结构齐全、末尾 `COMPLETE`、无 `NODE_LIMIT/TIMEOUT`，survivors=0。

```text
split_11 shard sha256 3a39cb5f177e471d70a332a03c98ee2e7c9129987338114cf52ec03b847a12e4
split_11 certificate sha256 2b26eadf7db5e0684d2213d6d70ea7e22dff7d498a493ed1bb9fa77e88736357
```

这仍不是 r8 全数组覆盖；继续只读等待并逐片验收。
- **2026-09-02 05:10 EDT 定理（Fable，直径端点归约）：** 对唯一直径点对 (a,b)，避开
  a、b 的点对距离 ≤ 298，故 299 由 (a,w) 或 (b,w) 实现；改名后 `diam(T−b)=299`、
  `diam(T−a)≤298`；结合"任意叶子 `diam(T−ℓ)≥284`"得 `284≤diam(T−a)≤298`。于是
  **25 阶不存在 ⟸ singleton normal form 在 δ∈[284,298] 全部无解**（任意 s、任意
  low 结构）；不需要"最重边悬挂"假设，两点帽子等分支不再需要。证明与推论见
  `docs/checkpoint-2026-09-01-s1-top-block-crowding.md` §3.10。
- **2026-09-02 07:10 EDT（Fable）：`δ=284`（`r=8`）CERTIFIED FINITE IMPOSSIBLE。**
  Hoffman2 数组 `118375` 64 片全部完成并通过 `verify_depth_splits.py`
  （`VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY`，`errors=[]`）：7 个有 depth-free 结构的
  low-tree 类共 1,641,497,082 个结构、49,212,675 个不同 ρ、零幸存；证书 SHA-256
  `b5769434011afa56dcc3d124f0bacfb831052b7fe3e39a699d837589248ca6be`。结合直径端点
  归约，25 阶问题现在等价于 singleton normal form 在 `δ∈[285,298]` 无解；`δ=285`
  （数组 `118376`）运行中。
- **2026-09-02 08:25 EDT（Fable）：** 用冻结源码 `frozen/abstract_class_search_d83323870704.cpp`
  在 geo-ws 单进程复跑 `δ=281,282,283`：全部与原始运行一致（r=5/6 零结构；r=7 仅链状
  有结构，链状深度阶段 leaves=14730、零幸存）；结果文件 SHA-256 `4d9ec498…`。
  `δ=284` 链状形状的非记忆化第二实现（Hoffman2 数组 `118830`）排队中。
- **2026-09-02 11:00 EDT（Fable）：新的"双端 (two-anchor) normal form"与 gap-order 搜索引擎。**
  设 (a,b) 为唯一直径点对，对其余 V=n−2 个顶点定义 e=N−d(a,u)、f=N−d(b,u)。则
  p=(N+f−e)/2、h=(N−e−f)/2，且 **gap(u,v)=min(f_u+e_v, f_v+e_u)+2h_c**（h_c=0 除非
  p_u=p_v）。Leech 树 ⟺ {0} ⊔ E ⊔ F ⊔ {gap(u,v)} = [0,N−1]。该表述**没有 δ 参数**，
  一次覆盖整个 n 阶问题。附带得到：奇偶劈分（n=25 时 (α,β)∈{(13,10),(8,15)}，等价于
  Taylor 条件的精确化）、附着引理、覆盖引理
  ((A+1)(B+1) = [0,N−1] + H + Σx^{M_ij} + 并列修正，故 E∪{0} 与 F∪{0} 的和集覆盖
  [0,N−1]，例外仅限 h_c>0 的并列对的 gap)、路上顶点构成长度 N 的 Golomb ruler
  （n=25 时路上非端点顶点 ≤18，至少 5 个顶点挂在路外）、球计数界。
  实现见 `theory-lab/double_end/`：`double_end_search.py`（gap 序引擎）、
  `brute_double_end.py`（独立的顶点序枚举器）、`differential_test.py`（关闭全部可选剪枝后对拍）。
  验收：n=3,4,6 两个实现在纯松弛上**完全一致**（n=6 为 12 个松弛解）；开启全部剪枝后
  恰好剩下真树（重建树 + BFS 验证），n=3/4/6 各 1 棵（对称性破缺后每棵计一次）。
  **n=9：67,432 节点穷尽、零解**（4.7 s，Python）。
  验收过程中发现并修正三个真 bug（此前任何数字作废）：`hc_heights` 不健全（要求 LCA
  顶点已存在）；deferred 列表边遍历边删除导致索引错位、漏分支；**待定 pair 会随 g 增大
  自动变确定**，必须在每个 gap 步重扫——这是最严重的一个，会漏解。
  C++ 移植 + 分片由 Opus agent 进行中；n=11 本地测量中。
- **2026-09-02 12:30 EDT（Fable）：双端引擎 C++ 移植验收通过，规模外推被实测推翻。**
  `theory-lab/double_end/double_end_search.cpp` 与 Python 参考在 n=3,4,6,9（对称性开/关）
  上**逐节点 trace 逐字节相同**；剪枝消融显示无任何剪枝丢失真树；分片划分性经 trace
  多重集比对证明。移植暴露出我 Python 的一个真 bug：`undo` 把恢复的 deferred 对追加到
  末尾，使 `rec()` 非状态中性——不影响未分片结果，但会让 `--split` 漏节点（n=9/LEVEL=10/M=4
  实测少 468 个）；已在两侧修正，八个基准数字不变。
  **但我之前 "n=16/18 可及" 的外推是错的**：C++ 实测 n=11 超过 1e8 节点仍未完成，
  n=9→n=11 增长 >4000×（ΔV=2），远高于 n=6→n=9 的 8.2×/V。已在 Hoffman2 提交
  n=11（作业 119549，32 分片）与 n=16 抽样（作业 119550，8/128 分片）测真实规模；
  在实测回来前不对 n≥11 的可及性作断言。
- **2026-09-02 12:20 EDT（Fable）：δ=285 将撞墙。** split_0 在 8 小时内只完成 95 个形状中的
  30 个；成本极不均匀（约每 5 个形状有 1 个约 1.4e9 csp 节点）。按此速率每任务需约 40 小时
  > 23:50 时限，任务会被墙杀死但 `.tmp` 里保留了已完成形状的 ABSTRACT 行，可收割重投。
  尝试提交尾部形状（61–95）的独立数组被 `QOSMaxSubmitJobPerUserLimit` 拒绝（上限 500，
  当前 321）。**δ=285 全量成本估计约 1e4 CPU 小时，δ=286 将再高约 60 倍——δ 阶梯到此为止。**
- **2026-09-02 13:40 EDT（Fable）：文档更正三处（由起草论文章节的 agent 发现，我复核确认）。**
  (1) `THEORY.md` §1 原写 `e ≡ f (mod 2)`，**错**；正确形式是 `e + f ≡ N (mod 2)`，两者
  只在 N 为偶时一致。独立暴力枚举在 n=3、n=6（N 奇）上判定其为假、n=4（N 偶）为真。
  代码一直用的是正确形式 `(e+f)%2 == N%2`，故所有数字不受影响。
  (2) `THEORY.md` §4 的判定引理阈值写成常数 `g+2`，**在"正在决定 gap g"这一时刻不健全**
  （此时未指派坐标可以等于 g，交叉和下界只有 g+1）；代码从来是与另一侧交叉和的**计算所得
  下界**比较，不是常数。已改写为区分两个不变量。
  (3) 报告 §11 里 "n=9 …… 67,432 节点" 是加入 `ub_prune` 与祖先一致性条件之前的数字，
  作废；当前 24,335（对称性破缺开）/ 48,669（关）。
  另澄清：n=6 松弛的 16 与 12 都对——16 是原始记录数，12 是不同的坐标系 `(E,F)` 个数，
  对拍比较的是后者。
  冻结文件改为按哈希命名（`frozen/MANIFEST.md` 记录两次冻结的差别仅为 stable-deferred
  修复），旧的 `double_end_search_frozen.py` 曾被两次复用指向不同内容，已删除。
- **2026-09-02 13:45 EDT（Fable）：奇偶劈分的闭式（起草 agent 提出，我独立验算通过）。**
  N 偶时 a、b 同色，`(2+α)β = N/2`，`β = (n ± √n)/2`；N 奇时 a、b 异色，
  `(1+α)(1+β) = ⌈N/2⌉`，`α = ((n−2) ± √(n−2))/2`。于是 Taylor 条件 `n = k²` 或 `k²+2`
  成为推论；n=25 给出 β ∈ {10,15}，与 `parity_splits()` 一致。
- **2026-09-02 14:15 EDT（Fable）：一个被我自己推翻的错误结论，记录在此。**
  我一度从 `--debug` 的逐深度直方图读出"25 阶受限搜索（`--force-e-upto 15`）前 24 步
  全强制"，并据此报告 E 继续为 18,36,54,72,90,108、F 继续为 16,32,48,64,80,96 的算术模式。
  **这是错的。** 该直方图取自撞到节点上限而中止的运行，深度优先会先下潜再回溯，浅层
  计数为 1 只说明兄弟分支尚未到达，不能证明"强制"。判据应当是分片测试或穷尽运行。
  实测：n=25、S=15 时 `--split 13 1 1000` 与 `--split 14 1 1000` 分别在 14、15 个节点后
  EXHAUSTED（只有前缀），而 `--split 15 1 1000` 跑到数百万节点仍未完；穷尽的小例
  （n=9、S=5）也给出同样形态。**强制链恰好是约束本身蕴含的 S 步，第一个自由决策在
  gap S+1，之后没有额外强制。** 那个算术模式只是深度优先的第一条路径。
  该方法学警告已写入 `theory-lab/double_end/THEORY.md` §9。起草论文章节的 agent 独立
  指出了同一问题，两条线索一致。
- **2026-09-02 14:20 EDT（Fable）：论文章节 `paper/section-double-end.tex` 起草完成**
  （898 行，tectonic 零警告，未改动 `main.tex`），含双端正规形、奇偶劈分闭式（推出 Taylor）、
  附着/Golomb/球计数引理、Lemma D 及其平凡推论的诚实标注、gap 序搜索与判定引理、
  三重验收、四个 bug 的记录、以及"n≥11 不作可及性断言"。冻结文件按哈希命名，
  含独立暴力枚举 oracle。三个 `\todo` 中已闭合一个（哈希表），余两个待 n=11/n=16 与
  25 阶受限运行的实测。
- **2026-09-02 14:45 EDT（Fable）：引理 E——受限情形为什么刚性（双端语言下重新得到 crowding）。**
  若 25 阶 Leech 树满足 `diam(T−a) ≤ 284`，则最大的 16 个距离 285..300 **全部**由含 a 的
  点对实现；记 W 为 `d(a,u) ≥ 285` 的 16 个顶点，则 `u ↦ d(a,u)` 是 W 到 `{285,…,300}`
  的双射（在 gap 坐标下即 `E ⊇ {1,…,15}`）。令 `α_u = 284 + i_u`，`i` 是 W 到 `[1,16]`
  的**双射**，则 `d(u,v) = 568 + i_u + i_v − 2μ_uv`（μ 为 a 到 u,v 中位点的距离，中位点
  必是 T 的顶点）。按中位点分组后组内距离是常数加 `i_u+i_v`，故组内 `i_u+i_v` 两两不同；
  `[1,16]` 中的两两和至多 29 个，于是每个中位点至多承载 29 个点对，且在其下方分成
  `n_1,…,n_t` 份时须有 `Σ_{i<j} n_i n_j ≤ 29`。
  两部分分裂给出 `p(m−p) ≤ 29`：m=16..13 最多剥 2 个、m=12 最多 3、m=11 最多 4、
  m≤10 不再受限（数值验算确认）。另由 `d(u,v) ≤ 284` 得 `μ ≥ 144`，即每个中位点 x 满足
  `e(x) ≤ 156`。
  这是 δ 程序里 top-block crowding 在双端表述下的重现，而且更锐利：那里顶块是连续的
  **深度**，这里标号 `i_u` 被迫恰好是区间 `[1,16]`。这解释了受限搜索为何远比全搜索便宜。
  **它本身不构成矛盾**（120 ≤ 15×29，中位点也够用），仍需搜索判定；但"毛毛虫约束 +
  μ≥144 + 中位点须为互异的 T 顶点"能否手工推到矛盾，是替换整条 δ=279..284 证书链的
  最有希望的路线。写入 `theory-lab/double_end/THEORY.md` §10（初稿曾误写成"一路都是
  毛毛虫"，已按上表更正）。
- **2026-09-02 15:35 EDT（Fable）：改写论文的 AI statement（`paper/main.tex` §12，备份 `main.tex.bak-1534`，tectonic 零警告）。**
  用户给了一份房版模板。其中「The scientific content is the authors' own」与
  「All scientific questions, study design decisions and interpretations are the authors'」
  **对本篇不准确**：top-block crowding 不等式与直径端点归约的初稿由助手提出，作者是审核、
  修正、采纳的一方。改写后如实区分"首次提出"与"审核采纳"，同时保留作者对选题、验收标准、
  运行授权、改写与最终责任的完整表述。图那一条按实情改为"本篇无图，10 个表全部由分析代码
  从证书文件生成"。并补记对抗性复核在 crowding 不等式早期形式中找出的三个缺失前提。
  待双端一节并入正文后，需在第二段补一句：双端正规形与引理 E 同由助手首先提出，
  该节记录了验收中发现的四个缺陷。最终措辞由作者定。
- **2026-09-02 15:36 EDT（Fable）：AI statement 按作者指定改为统一房版单段。**
  `paper/main.tex` §12 现为："Anthropic's Claude, OpenAI's ChatGPT and Google's Gemini were
  used as coding and analysis assistants throughout this project. They implemented and executed
  the processing, reasoning, and statistical code, prepared documentation, surveyed literature,
  and assisted in preparing manuscript text."（修正两处笔误：`as a ... assistants` 去 `a`；
  `Open AI's` → `OpenAI's`。）备份 `main.tex.bak-153621`，tectonic 零警告。
  我此前提出的顾虑（本篇中 crowding 不等式与端点归约的初稿由助手提出，"首次提出"与
  "审核采纳"宜分开写）已向作者说明，作者决定采用统一措辞，遵办并记录于此。
  已核实旧段承载的事实未随之丢失：clean-room 复现、差分对拍、对抗性复核在正文中分别仍有
  15/9/3 处；引理 2.9 的自我更正记录仍在正文第 396 行（"corrects a statement that circulated
  in our own notes"，并在其后标为 "in the corrected form"）。
- **2026-09-02 16:05 EDT（Fable）：n=11 由双端引擎穷尽，零解，3,338,887,905 个节点。**
  geo-ws 单进程、nice 15，约 9 小时 wall（机器负载 200–400，实际 CPU 远少于此）。
  与项目原有方法完全不同的算法独立重证了 11 阶不存在。
  节点数序列：n=3:3、n=4:8、n=6:44、n=9:24,335、n=11:3,338,887,905。
  n=9→n=11 的增长为每单位 V 约 370 倍（n=6→n=9 只有 8.2 倍），**增长率本身在加速**。
  据此外推 n=16 约 1e22 节点、n=18 更高——**n=16 与 n=18 在当前剪枝强度下不可及**，
  我早上"可及"的估计彻底作废。外推本身仍不可靠（增长率在变），但方向是明确的：
  双端引擎的价值在 n≤11 的独立重证与 25 阶的受限运行，不在于推进 n=16/18。
- **2026-09-02 16:20 EDT（Fable）：双端章节的并入安全性已验证。**
  `paper/section-double-end.tex`（954 行）与 `main.tex` 无标签冲突（31 vs 77，交集为空），
  它向正文发出的 14 个跨节引用全部命中已有标签（cor:reduction、thm:crowd280、thm:crowd283、
  thm:endpoint、lem:golomb、lem:taylor、tab:known、sec:{ai,algorithm,crowding,data,endpoint,
  prelim,verification}），且不引入任何新宏包或新宏。
  在临时文件上做了真实合并试编译（插在 Discussion 之前）：**零警告、零未定义引用、
  零重复标签**，PDF 由 263 KB 增至 344 KB；临时文件已清除，`main.tex` 未改动。
  并入只需一行 `\input{section-double-end}`，位置由作者定。
  该节记录：n≤11 的独立重证（n=11 为 3,338,887,905 节点、零解）、n≥16 不可及的两次更正、
  以及仍在运行的 25 阶受限搜索（128 分片、第 44 层，todo 保留、不作任何主张）。
- **2026-09-02 16:35 EDT（Fable）：按作者指定的优先级，把队列让给 25 阶受限运行；并修复我自己的一个 SLURM 脚本 bug。**
  作者的判断：25 阶受限运行（若穷尽零解，即用完全不同的算法把 δ=279..284 六个情形整条重证）
  优先于 δ=285（只把开放区间从 14 个缩到 13 个，且需约 1e4 CPU 小时与多轮收割重投）。
  **让队列前先保全证据**：把 δ=285 的 100 个分片 `.tmp` 原样复制并固化为
  `depthv7_r9_partial_20260902/`，跑 `harvest_partial_splits.py` 存档
  （报告 SHA-256 `b76ef60e414db3dffb2494d29359861f98c529b8ce5eae74c9691ed445c58678`；
  24,320 个 (split,shape) 对中 3,196 个已完成，**零幸存者**）。随后 scancel 118376
  （δ=285）、118830（δ=284 的 v4 链第二实现，被受限运行取代）及两个过时探针。
  **脚本 bug（我的）**：`hoffman2_double_end_v2.sh` 与 `hoffman2_double_end_array_slurm.sh`
  用了 `cd "$(dirname "$0")"`。SLURM 会把作业脚本复制到自己的 spool 目录，`$0` 因此指向
  一个无写权限的路径，所有任务在启动 3 秒后即以 `Permission denied` / `missing binary` 失败
  （作业 119549、119550、119624、119814 全部 FAILED，退出码 2）。**我此前报告的"排队中"是错的，
  它们早已失败。** 已改用绝对 `ROOT=`，并在脚本内注明原因；改后做了脱离 SLURM 的冒烟测试。
  重新提交后作业 `124763`（128 分片、第 44 层、`--force-e-upto 15`、节点上限 5e10、4 小时时限）
  **确认真正在跑**：100 RUNNING / 29 PENDING，99 个 `.tmp` 正在写入，二进制 SHA-256
  `4b615e5810a0fbaf…` 与部署一致。
  geo-ws 上的 4 个 worker 改跑尾部分片 124–127（集群最后才轮到），避免重复劳动；负载 89。
- **2026-09-03 15:30 EDT（Fable）：一次由我造成的并发违规，记录以备复核。**
  Linux 的 `comm` 名被截断到 15 字符，`double_end_search` 是 17 字符，故 `pgrep -x
  double_end_search` 恒返回 0。我据此三次判定"启动失败"并重启，实际上每次都成功了，
  最终 geo-ws 上同时有 12 个搜索进程（4 个分片各 3 份），超出约定的 4 个上限两倍，
  且三代进程用 `>` 写同一批日志、互相截断。已全部清理并重新以带去重守卫的启动脚本
  起 4 个（`de_launch2.sh`，日志改到 `runs2/`，每分片独立文件）。
  同一事件的另外两个坑：`pkill -f <模式>` 若模式文本也出现在调用它的命令行里会杀掉该
  shell（须用 `[d]ouble_end_search` 这种括号写法）；`ssh host 'bash -s' <<EOF` 里起的
  后台任务可能随会话被带走，应改用 `screen -dmS`。
  损失：约 2.7 小时/分片的重复计算被丢弃（约占单分片预算的 1%），以及本可用于其他分片
  的 CPU。工作站负载因此一度到 46，已回落到 31。
- **2026-09-04 （Fable）：25 阶受限双端搜索的规模实测——这条路不可行，已停。**
  采样实验：从 20000 路切分（第 47 层）中取 200 个分片，2 小时墙。**100 个全部超时，
  无一完成**（该批漏加 `--progress`，故无逐点进度，但结论不依赖它）。
  按同一二进制、同一机型实测的 136,000 节点/秒（来自 480 分片批次：100 分片 4 小时
  共 1.96e11 节点），每个 1/20000 分片 ≥ 9.79e8 节点仍未穷尽，故
  **总规模 ≥ 1.96e13 节点 ≥ 4.0e4 CPU 小时**（100 核并发 ≥ 17 天）。这是**下界**，真值可能高得多。
  对照：δ=285 证书估价约 1e4 CPU 小时；δ=284 整条证书是 1.64e9 个结构。
  **结论：双端引擎在 25 阶不具竞争力**，比专门化的 δ 程序贵至少一个量级。
  我此前建议"受限运行的每 CPU 小时价值更高"是**错的**——当时我不知道它的规模，
  据此让作者把队列从 δ=285 切走，代价是约 400 CPU 小时的沉没成本与约一天的时间。
  双端引擎的价值收敛为：正规形与引理（含引理 E）、n≤11 的独立重证。25 阶这条路作废。
  已停：集群作业 197587、200604；geo-ws 分片。
- **2026-09-04（Fable）：按作者批准的方案清理论文 todo。**
  (1) `main.tex` 中 n=18 逐拓扑旁证的 todo 改写为终稿：明确写"有意停在 91.6%"
  （112,082/122,344，零 SAT），给出理由（剩余 1,169 个正是引擎最难的实例，projected
  1e4–1e5 CPU 小时）并写明不增加逻辑强度（定理靠 forest 引擎、审计、三次逐位复现、
  clean-room 四条腿），保留"若将来报出 SAT 则定理必须撤回"。
  (2) δ=285 的 todo 改写为终稿：本文不作主张，如实记录 24,320 个 (split,shape) 对中
  完成 3,196 个、全部 EXHAUSTED 零幸存者、部分输出连同逐文件哈希已存档可续，
  并把开放区间明确写为 δ∈[285,298]。
  (3) `section-double-end.tex` 中 25 阶受限运行的 todo 改写为**实测负面结果**：
  引擎无断点故撞墙分片颗粒无收；实测 1.4e5 节点/秒/核（比 n≤11 慢一个量级，因为
  剪枝是每节点 O(N+V²) 而 N=300）；20000 路切分的 200 个采样分片在 2 小时墙上无一穷尽，
  故总规模 > 1.96e13 节点 ≈ 4e4 CPU 小时（下界）。结论：**25 阶上双端搜索比它本要检验的
  δ 程序贵至少一个量级**，独立重证未能完成，该节不依赖它；并解释了原因（固定 δ 就固定了
  顶块，crowding 随即剪枝，而双端一次探索所有可行 δ）。
  (4) 我杜撰的两个标签 `sec:deengine`、`thm:deconstraints` 已改为真实的
  `sec:de:search`、`thm:denormal`。合并试编译零警告，PDF 353 KB。
  正文现仅剩 δ=284 冻结复跑一个 todo，作业 200873 在跑。
- **2026-09-04（Fable）：δ=284 冻结源码复跑完成并通过验收——论文最后一个 todo 关闭。**
  作业 200873，64 分片，源码 `abstract_class_search_d83323870704.cpp`
  （SHA-256 `d83323870704cd5060abff3d0a5d879b43dc22a6131a25f11a27f4327a112a9d`）。
  `verify_depth_splits.py` 给出 `VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY`、零幸存者、
  错误列表为空；新证书 SHA-256
  `8f8ee5475b31ed852d55b59c41862d893c1478dc6568b6ca3f0ba7f4dadb0175`。
  **比对做到了最细粒度**：re-run 与原始运行各有 448 条 (split, shape) 记录，键集合完全相同，
  **每一条的叶子数、节点数、幸存者数逐条相同**——总计 1,641,497,082 叶子、
  39,312,834,366 节点，全部 EXHAUSTED，无幸存者。逐形状叶子数
  3,018,576 / 3,094,884 / 3,180,114 / 3,281,182 / 3,428,058 / 7,329,832 / 1,618,164,436
  （末项为链，占 98.6%）。
  过程中一个任务遇 NODE_FAIL，SLURM 自动重排队后重跑成功，不影响结果。
  论文相应段落改写为"四个 δ 值全部由同一份归档源码复现"，哈希表新增第 15、16 行
  （新证书与冻结源码）。**正文 `\todo` 归零**，`main.tex` 与合并双端一节的版本均零警告编译。
  备份：`paper/main.tex.bak-final-*`。
- **2026-09-04（Fable）：两份独立审稿意见的核查与处理。**
  来源：`docs/fable-second-referee-takeover-2026-09-04.md`（6 条，1 blocking）与
  Kimi 的 `REVIEW.md`（9 条，无 blocking）。两份独立得出，在两处撞车（§9 与 §8.4 矛盾、
  M(13) 见证缺失）。**十四条实质指控我逐条核查，一条都驳不倒。**
  一手证据：(a) 取得 Leach & Walsh, *Generalized Leech trees*, JCMCC **78** (2011), 15–22 全文，
  其 **Lemma 4.2** 原文为 "All trees on five vertices except for K_{1,4} are Z_11-Leech trees"，
  并印出两组标号；我验算确认论文的路径是其 5 倍、蜘蛛是其 7 倍（模 11），故五阶存在性
  **不是本文新发现**。(b) 同文参考文献 [7] 给出勘误的完整著录：BICA **52** (2008), 6。
  (c) `chesshippo/LeechTrees-18` 确实存在（创建 2026-08-24，Lean 4 归约到八种首边构型
  + C++ 穷尽，约 8.6e9 节点）；本项目 210/210 分片零结果提交于 2026-08-18、公开于 08-20，
  故我方在先，但必须引用。(d) 公开仓库最后 push 为 2026-08-20，25 阶材料确实不在其中，
  故 "All code and data are available" 一句为假。
  **B 第 1 条是我今天引入的错误**：未判定拓扑是 10,262（1,169 撞上限 + 9,093 未跑到），
  我改写时误作 1,169，少算九倍。
  **我与审稿方的一处分歧**：B 第 8 条称逐层增长因子为 8.3–9.4，我算得 7.1/7.6/8.3/8.4，
  无 9.4，无法复现；但同条关于逐阶因子（论文写 6.5–7，实为 5.71→7.59 单调递增）成立，已改。
  已修 12 条。待办两条：M(13) 见证（集群搜索中，现有可打印下界为 110，论文原称 105 依赖
  已丢失的 D=79 见证）；数据可用性（需作者授权推送并做不可变发布，交接规矩为"不推送"，
  暂已改为准确的将来时表述）。
