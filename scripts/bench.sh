#!/bin/bash
# usage: scripts/bench.sh BIN file.jsonl [extra flags]  -> per topology id status nodes wall(s); totals incl. user CPU time
BIN=$1; F=$2; shift 2
TMP=$(mktemp)
{ /usr/bin/time -p "$BIN" "$@" "$F" > "$TMP"; } 2> "$TMP.time"
python3 - "$TMP" "$TMP.time" <<'PY'
import sys,json
tn=0; tt=0
for l in open(sys.argv[1]):
    r=json.loads(l); tn+=r['nodes']; tt+=r['time']; print(r['id'], r['status'], r['nodes'], round(r['time'],2), round(r['nodes']/max(r['time'],1e-9)/1e6,3),'Mn/s')
user=[l.split()[1] for l in open(sys.argv[2]) if l.startswith('user')]
u=float(user[0]) if user else float('nan')
print('TOTAL nodes',tn,'wall',round(tt,1),'user',u,'rate(user)',round(tn/max(u,1e-9)/1e6,3),'Mn/s')
PY
rm -f "$TMP" "$TMP.time"
