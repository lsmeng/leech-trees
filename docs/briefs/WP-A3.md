# WP-A3 — 跑完 δ=285 的残余 (split,shape) 对（Sonnet，Hoffman2）

目的：把 δ=285（m=15, r=9）的 depth 阶段跑完，得到 VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY 证书。
不改引擎、不改参数：必须用 2026-09-02 那次同一个二进制 `abstract_class_search7` 和同样的 flags
（见 `theory-lab/s1_crowding/hoffman2_s1_depth_v7_array_slurm.sh`：`--m 15 --shapes-file <shapes> --solve-depths
--max-witness 50 --split <LVL> K 256`）。**禁止**使用 abstract_class_search_moment。

已有：Hoffman2 `$SCRATCH/leech-trees/theory-lab/s1_crowding/depthv7_r9_partial_20260902/` 里是上次的 .txt/.tmp；
本地 `theory-lab/s1_crowding/certificates/depthv7_r9_partial_20260902/harvest_20260902.json` 记录：95 个 shapes、
256 splits、已完成 3,196 对、缺 21,124 对、survivors 0。shapes 文件与 split level 请从 Hoffman2 上次的 sbatch 命令/日志
（`logs/s1dv7.*.out` 头部或 research 目录下的提交记录）确认，不要猜；把确认到的 shapes 文件路径、LVL、引擎 sha256 写进结果。

步骤（全部 ssh hoffman2；登录节点只跑轻命令；不动其他作业；先 `squeue -u $USER | wc -l` 确认总作业数 +256 < 500）：
1. 在 Hoffman2 上用 `theory-lab/s1_crowding/harvest_partial_splits.py DIR 256 --m 15 --shapes SHAPES --resid-dir residual_wave2 --out harvest_wave2.json`
   收割现有 .tmp/.txt，得到每个 split 的残余 shapes 文件（脚本用法见其 docstring）。核对 harvest 的缺失对数 = 21124。
2. 复制 v7 脚本为 `hoffman2_s1_depth_v7_resid_slurm.sh`：唯一改动是 `SHAPES=residual_wave2/split_${K}...`（按 harvest 脚本实际输出的文件名），
   输出目录 tag 改为 `r9_wave2`；其余（partition campus, qos campus24, 23:50, --nice=10000, 1 cpu, 2G）不变。
3. `sbatch --array=0-255` 提交；记录 job id。空残余的 split 直接跳过（脚本内判断文件不存在或为空则 exit 0）。
4. 不等待完成。写 `docs/briefs/WP-A3-result.md`（≤40 行）：shapes 文件、LVL、引擎 sha256、harvest 统计、job id、提交时间、
   下一波的收割命令（原样可复制）。以后每波结束后由新 agent 重复 1–3，直到所有 split 的残余为空，再用
   `verify_depth_splits.py` 出证书。
回传 JSON：{status, job_id, missing_pairs_before, blocking}。禁读 research_state.md、paper/。
