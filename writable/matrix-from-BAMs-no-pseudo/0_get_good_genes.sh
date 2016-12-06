#!/bin/bash

cat /users/pjvh/binf527-proj/writable/HumanReferences/Homo_sapiens.GRCh37.75.gtf | perl -nale 'if ($F[2] eq "gene" and $F[1] eq "protein_coding") { m{(ENSG[0-9]+)}; print $1}' > good-genes
