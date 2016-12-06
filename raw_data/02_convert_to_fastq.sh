#!/bin/bash

set -euo pipefail

mkdir -p fastq

for infile in sra/*.sra; do
    fname="$(basename "$infile")"
    outfile="fastq/${fname%.sra}.fastq.gz" # who knows whether this is correct.
    if [[ -e "$outfile" ]]; then
        echo "already exists: $outfile"
    else
        fastq-dump --gzip --outdir fastq/ "$infile"
    fi
done
