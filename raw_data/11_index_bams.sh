#!/bin/bash
set -euo pipefail

for b in /users/pjvh/binf527-proj/writable/mapped2/SRR*-Aligned.sortedByCoord.out.bam; do
    samtools index "$b"
done