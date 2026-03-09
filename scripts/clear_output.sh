#!/usr/bin/env bash
# Clear output folder (preserves directory)
set -e
cd "$(dirname "$0")/.."
rm -rf output/*
mkdir -p output
echo "Cleared output/"
