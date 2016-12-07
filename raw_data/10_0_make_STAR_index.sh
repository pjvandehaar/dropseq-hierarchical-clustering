#!/bin/bash

set -euo pipefail
#Genome Indices
/users/pjvh/binf527-proj/writable/STAR-2.5.2b/bin/Linux_x86_64_static/STAR \
    --runThreadN 4 \
    --runMode genomeGenerate \
    --genomeDir /users/pjvh/binf527-proj/writable/mouseref/index \
    --genomeFastaFiles /users/pjvh/binf527-proj/writable/mouseref/GCF_000001635.25_GRCm38.p5_genomic.fa \
    --sjdbGTFfile /users/pjvh/binf527-proj/writable/mouseref/GCF_000001635.25_GRCm38.p5_genomic.gff
#    --sjdbGTFfile /users/pjvh/binf527-proj/writable/mouseref/gencode.vM11.annotation.gtf
