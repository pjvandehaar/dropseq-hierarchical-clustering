#!/bin/bash

set -euo pipefail

fin="best-genes.tsv"
fout="best-genes.cef"
nrow=$(tail -n+2 $fin | wc -l)
ncol=$(head -n1 $fin | tr "\t" "\n" | wc -l)


echo -e "CEF\t0\t1\t1\t$nrow\t$ncol\t0" > $fout

echo -ne "\tGENE\t" >> $fout
head -n1 $fin >> $fout

echo "SAMPLE" >> $fout

tail -n +2 $fin |
perl -pale 's{^([^\t]*\t)}{\1\t}' >> $fout
