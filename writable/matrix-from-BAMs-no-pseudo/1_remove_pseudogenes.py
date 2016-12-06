#!/usr/bin/env python3

import pysam
import pybedtools
import collections
import os.path
import glob
import multiprocessing
import re

good_genes = {g.strip() for g in open('good-genes')}

for in_fname in glob.glob('/users/pjvh/binf527-proj/writable/matrix-from-BAMs/out/SRR*.tsv'):
    srr = re.search('(SRR[0-9]+)', in_fname).groups()[0]
    out_fname = '/users/pjvh/binf527-proj/writable/matrix-from-BAMs-no-pseudo/no-pseudo/{}'.format(srr)
    with open(out_fname, 'w') as fout:
        with open(in_fname) as fin:
            for l in fin:
                if l.split()[0] in good_genes:
                    fout.write(l)
