#!/bin/bash

(echo -ne "\t"; cut -f1 umis-per-gene/SRR1544693.tsv |
tr "\n" "\t" |
perl -pale 's{\s*$}{}') > out2/cols

for f in umis-per-gene/SRR*; do
    srr=$(echo $f | perl -nale 'print m{(SRR[0-9]+)}')
    echo "$srr"
    echo -ne "$srr\t" > out2/$srr
    cut -f2 $f |
    tr "\n" "\t" |
    perl -pale 's{\s*$}{}' >> out2/$srr
done
sleep 1

cat out2/cols out2/SRR* > umis-per-gene.tsv
