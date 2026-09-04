#!/usr/bin/env bash
# Install the SAT toolchain used by src/sat_encode.py + src/run_sat.py:
#   cadical, kissat (Homebrew), python-sat (repo venv; only pysat.card is used, no pblib needed),
#   drat-trim (built from source into tools/drat-trim).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if command -v brew >/dev/null; then
  brew list cadical >/dev/null 2>&1 || brew install cadical
  brew list kissat  >/dev/null 2>&1 || brew install kissat
else
  echo "no Homebrew: install cadical/kissat manually (https://github.com/arminbiere/{cadical,kissat})" >&2
fi
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install -q python-sat networkx
mkdir -p tools
if [ ! -x tools/drat-trim/drat-trim ]; then
  [ -d tools/drat-trim ] || git clone -q https://github.com/marijnheule/drat-trim.git tools/drat-trim
  (cd tools/drat-trim && make -s drat-trim lrat-check)
fi
echo "cadical:   $(cadical --version)"
echo "kissat:    $(kissat --version)"
echo "drat-trim: $(ls -la tools/drat-trim/drat-trim | awk '{print $5" bytes"}')"
.venv/bin/python -c "import pysat; print('python-sat', pysat.__version__)"
