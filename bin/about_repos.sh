#!/bin/bash -e
OUT='var/about_repos.txt'
python about_repos.py login $1 > $OUT

echo "Wrote to: $OUT"
