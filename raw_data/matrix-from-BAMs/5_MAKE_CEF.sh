#!/bin/bash

set -euo pipefail

nrow=$(tail -n+2 umis-per-gene-with-good-cv-mean.tsv | wc -l)
ncol=$(head -n1 umis-per-gene-with-good-cv-mean.tsv | tr "\t" "\n" | wc -l)
fout="umis-per-gene-with-good-cv-mean.cef"

echo -e "CEF\t0\t1\t1\t$nrow\t$ncol\t0" > $fout

echo -ne "\tGENE\t" >> umis-per-gene-with-good-cv-mean.cef
head -n1 umis-per-gene-with-good-cv-mean.tsv >> $fout

echo "SAMPLE" >> $fout

tail -n +2 umis-per-gene-with-good-cv-mean.tsv |
perl -pale 's{^([^\t]*\t)}{\1\t}' >> $fout
