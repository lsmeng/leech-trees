# Finite incidence-plus-partition catalogue

The script
`theory-lab/topwindow/verify_pro_b27_incidence_partition_catalogue.py`
enumerates, for every rooted non-isomorphic tree through order seven, every
low/high edge partition and every placement of the three forced incidence
tokens `L5`, `L21`, and `J32`.  Its canonical rooted code retains both edge
colour and vertex marks, so equivalent rooted states are deduplicated.

The replay returned `VERIFIED_MARKED_EDGE_PARTITION_CATALOGUE`:

| maximum order | cumulative raw assignments | cumulative canonical states |
| ---: | ---: | ---: |
| 6 | 283,285 | 93,053 |
| 7 | 1,973,589 | 663,215 |

The order-6 raw-assignment total in the table is the cumulative sum of the
per-order rows (`1 + 32 + 324 + 4,096 + 30,000 + 248,832 = 283,285`); the
machine-readable output is authoritative for the exact per-order values.

An independent stdin-only implementation on `geo-workstation` reproduced the
order-6 and order-7 per-order rows and canonical counts exactly
(`1/16/163/1,398/10,927/80,548/570,162`), without reading or writing the
project checkout.

This is a topology-layer prototype for the completeness bridge.  It does not
enumerate ordered high-edge weights, arbitrary low-component internal trees,
complete pair spectra, or all seven `34--37` owner incidences.  In particular,
its finite state count is not a global nonexistence result.
