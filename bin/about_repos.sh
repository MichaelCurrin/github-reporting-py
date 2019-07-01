#!/bin/bash -e
OUT='var/about.txt'
python about_repos.py login $1 > $OUT

echo "Wrote to: $OUT"
