# Frozen sources, double-end programme

Hash-tagged copies of the exact sources behind every reported number.  File
names carry the first 16 hex of the SHA-256 of the file itself.

| date (EDT) | file | sha256 (16) | what it produced |
|---|---|---|---|
| 2026-09-02 ~11:00 | double_end_search.py | `934b24162db8c0c2` | the first frozen Python reference: n=3/4/6/9 = 3/8/44/24335 nodes with symmetry breaking, 5/15/87/48669 without.  Superseded the same day. |
| 2026-09-02 ~12:40 | double_end_search.py | `4916cae4bfc30da7` | same eight node counts, plus the stable-deferred fix in `undo` (restore the deferred entry at its original index) so that `rec()` is state-neutral and `--split` partitions correctly.  **Current reference.** |

The earlier name `frozen/double_end_search_frozen.py` was reused across both
freezes and has been removed to stop it pointing at two different files; use the
hash-tagged names.  `PORT_NOTES.md` refers to `934b2416…`; the C++ was
subsequently re-checked against `4916cae4…` and reproduces its numbers, and the
two Python versions differ only in the stable-deferred restore.
