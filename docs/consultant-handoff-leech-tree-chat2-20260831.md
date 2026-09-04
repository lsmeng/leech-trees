# Consultant replacement handoff — `leech tree chat2`

## Identity

* Project: Leech-tree nonexistence research
* Controller root: `/Users/geoclaw/Documents/claude/projects/leech-trees`
* Required advisor surface: ordinary Desktop **Chat**, backing kind `chatgpt`
* Required title: `leech tree chat2`
* Generation: 2
* Required visible setting: Sol Extra High / XHigh
* Required connector: `DevSpace workstation`
* Required remote root: `/home/geo/codex-work/leech-trees`
* Allowed roots known to the connector: `/home/geo/`, `/home2/geo/`, `/media/geo/`

## Current verified frontier

The fixed-`m=4`, parent-depth-3 canonical weighted-base traversal has a
freshly accepted prefix of **52/64** shards over parent indices `[0,3089)`.
The prefix has 1,946,070 raw extensions and 6,126 emitted child orbits.
Shards 47--50 were freshly replayed by the controller and matched the preserved
replay files byte-for-byte.  Shard 51 was newly generated and independently
replayed with interval `[3030,3089)`, 224 child orbits, artifact SHA-256
`f4a43941f9f966a93de0d1216fc7aaabe3d28a73449b94fe7bd32611b52d3701`,
and replay SHA-256
`9853c3035f6ce6bbc773b69fef3707efb4cad7d59b03a9836350840160409f26`.

## Remote evidence root

The old computation tree survives under:

`/home/geo/codex-work/leech-trees/remote_scratch/canonical_traversal_shard_20260830`

The outer `/home/geo/codex-work/leech-trees` directory is not a Git checkout,
but the scratch tree contains the frozen sources, verified depth-2 parent
merge, and shard/replay pairs 0--51.  Shards 52--63 are missing.

Frozen source hashes:

* indexer `f524f469461de1304eadb33c077122ede55e01c4b9b06444c6387f25fd201ebd`
* transversal `fb127ff978241efafa856c350e52c9f804cf88ea9d6789b60558b8420451e496`
* runner `466ce529e85dca803de77980cf2c99ecf92afa6091fc526c656df4e48322441b`
* shard checker `378c0bb30695eaf64e2c9a68a5ec70d94acfa6e28fae267309bfd8011fb2fec2`
* merger `6c4129e2de6bdd78cf26769c8f31aefe3df8a240de90fafe9654d6f074dccf12`

## First task (`CONSULT-20260831-006`)

Perform a strictly read-only DevSpace preflight.  Confirm the exact remote
root, frozen source hashes, the depth-2 parent merge, complete shard/replay
pairs 0--51, and missing 52--63.  Do not run Python, create files, start jobs,
or edit state during the preflight.

Return the task ID, conclusion, evidence, commands, changed files (`none`),
transport/DevSpace errors, and the next bounded recommendation.  Before any
later write or computation, the controller must explicitly assign writer
ownership and resource bounds.

## Protected state

Do not edit `research_state.md`, existing sources, existing result artifacts,
or the controller checkpoint during preflight.  Do not commit, push, delete,
move, overwrite, change credentials, or alter DevSpace configuration.
