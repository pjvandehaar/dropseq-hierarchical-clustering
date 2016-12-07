#!/usr/bin/env python3

import pysam
import pybedtools
import collections
import os.path
import glob
import multiprocessing
import re
import os

ilen = lambda it: sum(1 for _ in it)

def get_genes():
    with open('good_genes.bed') as f:
        for line in f:
            f = line.strip('\n\r').split('\t')
            yield dict(chrom=f[0],
                       start=int(f[1]),
                       end=int(f[2]),
                       name=f[3])
genes = list(get_genes())

get_umi = lambda read: str(read).split('\t')[0].split('-')[-1]
def count_sample(fname):
    bamfile = pysam.AlignmentFile(fname)
    reads_in_gene = lambda gene: bamfile.fetch(gene['chrom'], gene['start']-100, gene['end']+100)

    def count_umis(gene):
        umis = collections.Counter(get_umi(r) for r in reads_in_gene(gene)).most_common()
        umi_counts = (r[1] for r in umis)
        return ilen(n for n in umi_counts if n > 1)

    return sorted((gene['name'], count_umis(gene)) for gene in genes)

def handle(in_fname):
    srr = re.search('(SRR[0-9]+)', in_fname).groups()[0]
    out_fname = '/users/pjvh/binf527-proj/raw_data/matrix-from-BAMs/umis-per-gene/{}.tsv'.format(srr)
    if os.path.exists(out_fname): return
    try:
        counts = count_sample(in_fname)
        with open(out_fname, 'w') as f:
            for gene, count in sorted(counts):
                f.write('{}\t{}\n'.format(gene, count))
    except:
        print('Error with {}'.format(in_fname))
        raise
    print('{} -> {}'.format(in_fname, out_fname))

def get_files_to_run():
    for fname in glob.glob('/users/pjvh/binf527-proj/raw_data/mapped3/SRR*-Aligned.sortedByCoord.out.bam'):
        if os.path.exists('{}.bai'.format(fname)):
            yield fname

if __name__ == '__main__':
    os.makedirs("/users/pjvh/binf527-proj/raw_data/matrix-from-BAMs/umis-per-gene/", exist_ok=True)
    fnames = list(get_files_to_run())
    print('{} files have been indexed.'.format(len(fnames)))

    # for fname in fnames:
    #     handle(fname)

    pool = multiprocessing.Pool(24)
    pool.map(handle, fnames)

    print('When done, check that `wc -l umis-per-gene | sort -nr` is all the same')