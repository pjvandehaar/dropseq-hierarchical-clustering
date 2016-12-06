#!/bin/bash

# rm out2/SRR*

nrow=3457
ncol=424

echo -e "CEF\t0\t1\t1\t$nrow\t$ncol\t0" > small.cef

echo -ne "\tGENE\t" >> small.cef
head -n1 only-genes-with-good-cv-mean.tsv >> small.cef

echo "SAMPLE" >> small.cef

tail -n +2 only-genes-with-good-cv-mean.tsv |
perl -pale 's{^([^\t]*\t)}{\1\t}' >> small.cef
