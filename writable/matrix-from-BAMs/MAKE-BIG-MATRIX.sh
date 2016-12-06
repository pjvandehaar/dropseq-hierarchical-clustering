#!/bin/bash


#for f in out/SRR*tsv; do srr=$(echo $f | perl -nale 'print m{(SRR[0-9]*)}'); (echo $srr; cut -f2 $f) > out2/$srr; done


# (echo; cut -f1 out/SRR1544693.tsv) > out2/genes
# (echo SAMPLE; seq 57773 | perl -pale '{$_=""}') > out2/empty-col
#paste -s out2/genes out2/empty-col out2/SRR* > mat.tsv


# (echo -e "\tSAMPLE"; cut -f1 out/SRR1544693.tsv | perl -pale 's{$}{\t}') > out2/genes
# paste -s out2/genes out2/SRR* > mat.tsv


# nrow=57773
# ncol=3457
# echo -e "CEF\t2\t1\t1\t$nrow\t$ncol\t0" > final.cef
# echo -e "Genome\tGRCh37" >> final.cef
# echo -e "Citation\thttp://www.sciencemag.org/content/347/6226/1138.abstract" >> final.cef

# echo -ne "\tGENE\t" >> final.cef
# cut -f1 out/SRR1544693.tsv | tr "\n" "\t" | perl -pale 's{\s*$}{}' >> final.cef

# echo "SAMPLE" >> final.cef

# for f in out/SRR*tsv; do
#     srr=$(echo $f | perl -nale 'print m{(SRR[0-9]*)}')
#     echo -ne "$srr\t\t" >> final.cef # Two breaks b/c "GENE" header column
#     cut -f2 $f | tr "\n" "\t" | perl -pale 's{\s*$}{}' >> final.cef
# done

rm out2/SRR*

nrow=3457
ncol=57773

echo -e "CEF\t0\t1\t1\t$nrow\t$ncol\t0" > out2/header

echo -ne "\tGENE\t" > out2/cols
cut -f1 out/SRR1544693.tsv |
head -n$ncol |
tr "\n" "\t" |
perl -pale 's{\s*$}{}' >> out2/cols

echo "SAMPLE" >> out2/cols

find out/SRR*tsv |
head -n$nrow |
while read f; do
    srr=$(echo $f | perl -nale 'print m{(SRR[0-9]*)}')
    echo -ne "$srr\t\t" > out2/$srr # Two breaks b/c "GENE" header column
    cut -f2 $f |
    head -n$ncol |
    tr "\n" "\t" |
    perl -pale 's{\s*$}{}' >> out2/$srr
done
sleep 1

cat out2/header out2/cols out2/SRR* > final.cef
