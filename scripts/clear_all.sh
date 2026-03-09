#!/usr/bin/env bash
# Clear output and log folders
set -e
cd "$(dirname "$0")/.."
rm -rf output/* log/*
mkdir -p output log
echo "Cleared output/ and log/"
