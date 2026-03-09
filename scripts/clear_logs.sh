#!/usr/bin/env bash
# Clear log folder (preserves directory)
set -e
cd "$(dirname "$0")/.."
rm -rf log/*
mkdir -p log
echo "Cleared log/"
