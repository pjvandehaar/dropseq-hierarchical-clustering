#!/bin/bash

# rm out2/SRR*

# nrow=$(find no-pseudo/SRR* | wc -l)
# ncol=$(cat no-pseudo/SRR1544738 | wc -l)

# echo -e "CEF\t0\t1\t1\t$nrow\t$ncol\t0" > out2/header

# echo -ne "\tGENE\t" > out2/cols
# cut -f1 out/SRR1544693.tsv |
# head -n$ncol |
# tr "\n" "\t" |
# perl -pale 's{\s*$}{}' >> out2/cols

# echo "SAMPLE" >> out2/cols

# find out/SRR*tsv |
# head -n$nrow |
# while read f; do
#     srr=$(echo $f | perl -nale 'print m{(SRR[0-9]*)}')
#     echo -ne "$srr\t\t" > out2/$srr # Two breaks b/c "GENE" header column
#     cut -f2 $f |
#     head -n$ncol |
#     tr "\n" "\t" |
#     perl -pale 's{\s*$}{}' >> out2/$srr
# done
# sleep 1

# cat out2/header out2/cols out2/SRR* > final.cef


(echo -ne "\t"; cut -f1 no-pseudo/SRR1544693 |
tr "\n" "\t" |
perl -pale 's{\s*$}{}') > out2/cols

# for f in no-pseudo/SRR*; do
#     srr=$(echo $f | perl -nale 'print m{(SRR[0-9]+)}')
#     echo "$srr"
#     echo -ne "$srr\t" > out2/$srr
#     cut -f2 $f |
#     tr "\n" "\t" |
#     perl -pale 's{\s*$}{}' >> out2/$srr
# done
# sleep 1

cat out2/cols out2/SRR* > no-pseudo.tsv
