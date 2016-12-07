#!/bin/bash

set -euo pipefail

cat /users/pjvh/binf527-proj/writable/mouseref/GCF_000001635.25_GRCm38.p5_genomic.gff |
grep -v '^#' |
grep '^NC_' |
perl -nale 'print if $F[2] eq "gene"' |
grep 'gene_biotype=protein_coding' |
perl -nale 'm{Dbxref=GeneID:([0-9]+).*Name=([^;]+)}; print "$F[0]\t$F[3]\t$F[4]\t$2::$1"' > good_genes.bed
