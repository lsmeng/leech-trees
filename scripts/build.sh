#!/bin/bash
# Build the C++ Leech-tree search engine.  Usage: scripts/build.sh [name]  -> bin/<name> and bin/<name>_nw8 (-DNW=8, for tests)
# default name: leech_search.  Use e.g. `scripts/build.sh leech_search_v2` to build next to a running binary.
set -e
cd "$(dirname "$0")/.."
NAME=${1:-leech_search}
mkdir -p bin
clang++ -O3 -march=native -std=c++17 -Wall -Wextra -o bin/$NAME src/leech_search.cpp
clang++ -O3 -march=native -std=c++17 -DNW=8 -o bin/${NAME}_nw8 src/leech_search.cpp
echo "built bin/$NAME bin/${NAME}_nw8"
