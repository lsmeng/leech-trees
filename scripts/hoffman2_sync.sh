#!/bin/bash
# Sync repo (no venv/results) to Hoffman2 scratch and set up env once.
set -e
REMOTE=hoffman2
RDIR='$SCRATCH/leech-trees'
rsync -az --exclude .venv --exclude __pycache__ --exclude .git --exclude 'results/*' ~/Documents/claude/projects/leech-trees/ $REMOTE:'$SCRATCH/leech-trees/'
ssh $REMOTE 'cd $SCRATCH/leech-trees && (test -d env || python3 -m venv env) && ./env/bin/pip install -q ortools networkx && ./env/bin/python -c "import ortools,networkx;print(\"env ok\")"'
