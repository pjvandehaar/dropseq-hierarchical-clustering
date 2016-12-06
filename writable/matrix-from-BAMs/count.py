#!/usr/bin/env python3

import pysam
import pybedtools
import collections
import os.path
import glob
import multiprocessing
import re

count = lambda it: sum(1 for _ in it)

chroms = [str(c) for c in range(1,1+22)]+['X','Y','MT']
gencode = pybedtools.BedTool('/users/pjvh/binf527-proj/writable/HumanReferences/Homo_sapiens.GRCh37.75.gtf')
genes = [dict(chrom=r.chrom, start=r.start, end=r.end, strand=r.strand, ensg=r.attrs['gene_id'], name=r.attrs['gene_name']) for r in gencode if r.fields[2] == 'gene' and r.chrom in chroms]

get_umi = lambda read: str(read).split('\t')[0].split('-')[-1]
def count_sample(fname):
    bamfile = pysam.AlignmentFile(fname)
    reads_in_gene = lambda gene: bamfile.fetch(gene['chrom'], gene['start']-100, gene['end']+100)

    def count_umis(gene):
        umis = collections.Counter(get_umi(r) for r in reads_in_gene(gene)).most_common()
        umi_counts = [r[1] for r in umis]
        return count(n for n in umi_counts if n > 1)

    return sorted((gene['ensg'], count_umis(gene)) for gene in genes)

def write_out(out_fname, counts):
    with open(out_fname, 'w') as f:
        for gene, count in sorted(counts):
            f.write('{}\t{}\n'.format(gene, count))

def handle(in_fname):
    srr = re.search('(SRR[0-9]+)', in_fname).groups()[0]
    out_fname = '/users/pjvh/binf527-proj/writable/matrix-from-BAMs/out/{}.tsv'.format(srr)
    try:
        counts = count_sample(in_fname)
        write_out(out_fname, counts)
    except:
        print('Error with {}'.format(in_fname))
        raise
    print('{} -> {}'.format(in_fname, out_fname))


if __name__ == '__main__':
    fnames = glob.glob('/users/pjvh/binf527-proj/writable/mapped2/SRR*-Aligned.sortedByCoord.out.bam')

    # for fname in fnames:
    #     handle(fname)

    pool = multiprocessing.Pool(16)
    pool.map(handle, fnames)