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

def head(iterator):
    return list(itertools.islice(iterator, 0, 5))
def count(iterator):
    return sum(1 for _ in iterator)

Read = collections.namedtuple('Read', ['name', 'seq', 'qual'])
def extract_reads(iterator):
    while True:
        a = next(iterator).rstrip('\n')
        b = next(iterator).rstrip('\n')
        c = next(iterator)
        d = next(iterator).rstrip('\n')
        yield Read(name=a,seq=b,qual=d)
def get_reads(fname):
    with gzip.open(fname, 'rt') as f:
        for read in extract_reads(f):
            yield read

def write_reads_to_file(reads, output_filename):
    with gzip.open(output_filename, 'wt') as f:
        for read in reads:
            f.write(read.name)
            f.write('\n')
            f.write(read.seq)
            f.write('\n+\n')
            f.write(read.qual)
            f.write('\n')


def get_length_threshold(fname, log):
    reads = get_reads(fname)
    longest = -1
    n=0
    for read in reads:
        if len(read.seq) > longest: longest = len(read.seq)
        n+=1
    log['num reads']['initial'] = n
    log['longest_read_length'] = longest
    return int(longest * 0.8)

def get_sufficiently_long_reads(fname, log):
    length_threshold = get_length_threshold(fname, log)
    reads = get_reads(fname)
    n = 0
    for read in reads:
        if len(read.seq) > length_threshold:
            n+=1
            yield read
    log['num reads']['longenough'] = n

def convert_sample(args):
    in_fname, out_fname = args
    if os.path.exists(out_fname + '.log'):
        print('already did ' + out_fname)
        return

    log = {
        'num reads': {},
        'perc reads': {},
        'input_file': in_fname,
        'output_file': out_fname,
    }
    print(in_fname, '->', out_fname)
    try:
        reads = get_sufficiently_long_reads(in_fname, log)
        write_reads_to_file(reads, out_fname)
    except Exception as exc:
        with open(out_fname + '.err', 'wt') as f:
            f.write(str(exc))
        print(exc)
        print('')

    for filter in log['num reads']:
        log['perc reads'][filter] = log['num reads'][filter] / log['num reads']['initial']
    with open(out_fname + '.log', 'wt') as f:
        json.dump(log, f, indent=1, sort_keys=True)

def get_fnames_to_convert():
    infiles = list(glob.glob('fastq-cleaned-up/SRR*.fastq.gz'))
    print('found {} input files'.format(len(infiles)))
    for infile in infiles:
        out_fname = infile.replace('fastq-cleaned-up/', 'fastq-cleaned-up2/')
        if not os.path.exists(out_fname + '.log'):
            yield (infile, out_fname)

if __name__ == '__main__':
    todo = list(get_fnames_to_convert())
    print('found {} files that need to be processed'.format(len(todo)))

    pool = multiprocessing.Pool(16)
    pool.map(convert_sample, todo)

    # for args in todo:
    #     convert_sample(args)
