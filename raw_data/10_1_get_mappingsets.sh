#!/bin/bash
set -euo pipefail

mkdir -p /users/pjvh/binf527-proj/raw_data/mappingsets/

find /users/pjvh/binf527-proj/raw_data/fastq-cleaned-up4/*stdout |
perl -pale 's{(^.*SRR[0-9]+)\..*$}{\1_trimmed.fq.gz}' |
tee /users/pjvh/binf527-proj/raw_data/mappingsets/all |
# `man split` is broken here but on macOS run `man gsplit` to see docs for r/6.
split -d -n r/6 - /users/pjvh/binf527-proj/raw_data/mappingsets/x
