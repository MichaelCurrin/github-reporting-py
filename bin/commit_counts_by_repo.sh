#!/bin/bash -e
OUT='var/commit_counts_by_repo.txt'
python commit_counts_by_repo.py login $1 > $OUT

echo "Wrote to: $OUT"
