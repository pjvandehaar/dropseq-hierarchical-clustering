#!/usr/bin/env Rscript

r <- read.table('umis-per-gene.tsv', row.names=1, header=T, sep="\t")
s <- r[,apply(r,2,sum) > 3000]
cv <- function(x) {sqrt(var(x)) / mean(x)}
s2 <- s[,apply(s,2,cv) > 1.5]
write.table(s2, file='umis-per-gene-with-good-cv-mean.tsv', sep='\t', quote=F)
