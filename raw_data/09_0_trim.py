#!/usr/bin/env python3

from __future__ import division, print_function
import glob
import gzip
import itertools
import collections
import re
import json
import multiprocessing
import os.path
import subprocess

def convert_sample(d):
    infile, logfile = d
    print('converting {}'.format(infile))
    cmd = '''/users/pjvh/binf527-proj/raw_data/trim_galore --quality 20 --gzip --path_to_cutadapt "/users/pjvh/.linuxbrew/bin/cutadapt" -o "./fastq-cleaned-up4/" "{}"'''.format(
        infile)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    with open(logfile, 'wb') as f:
        f.write(output)

def get_fnames_to_convert():
    infiles = list(glob.glob('fastq-cleaned-up3/SRR*.fastq.gz'))
    print('found {} input files'.format(len(infiles)))
    for infile in infiles:
        basename = os.path.basename(infile)
        logfile = './fastq-cleaned-up4/{}.stdout'.format(basename)
        if not os.path.exists(logfile):
            yield (infile, logfile)

if __name__ == '__main__':
    todo = list(get_fnames_to_convert())
    print('found {} files that need to be processed'.format(len(todo)))

    pool = multiprocessing.Pool(8)
    pool.map(convert_sample, todo)

    # for args in todo:
    #     convert_sample(args)
