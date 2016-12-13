#!/bin/bash

# head -n1 umis-per-gene.tsv  | tr "\t" "\n" | egrep -n 'Mbp|Thy1|Gad1|Tbr1|Spink8|Aldoc|Aif1|Cldn5|Acta2'

cat umis-per-gene.tsv  | cut -d $'\t' -f1,793,1063,1064,1163,3509,6412,11253,18205,18888,19172 > best-genes.tsv