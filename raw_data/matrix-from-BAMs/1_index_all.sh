#!/bin/bash

bamdir=/users/pjvh/binf527-proj/raw_data/mapped3

find $bamdir/*.done |
perl -nale 'm{(SRR[0-9]+)}; print $1' |
while read srr; do
    fname="$bamdir/$srr-Aligned.sortedByCoord.out.bam"
    if ! [[ -e "$fname.bai" ]]; then
        echo "$srr"
        samtools index "$fname"
    fi
done
