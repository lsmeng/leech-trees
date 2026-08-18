#!/bin/bash
# Build the C++ Leech-tree search engine.  Usage: scripts/build.sh  -> bin/leech_search
set -e
cd "$(dirname "$0")/.."
mkdir -p bin
clang++ -O3 -march=native -std=c++17 -Wall -Wextra -o bin/leech_search src/leech_search.cpp
echo "built bin/leech_search"
