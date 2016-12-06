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

def get_constG_positions(fname, log):
    num_G_at_pos = []
    num_reads = 0
    reads = get_reads(fname)
    #reads = itertools.islice(reads, 0, 100) # while debugging
    for read in reads:
        while len(read.seq) > len(num_G_at_pos):
            num_G_at_pos.append(0)
        num_reads += 1
        for pos, base in enumerate(read.seq):
            if base == 'G':
                num_G_at_pos[pos] += 1
    const_G_positions = []
    mostly_G_positions = []
    for pos, numG in enumerate(num_G_at_pos):
        if numG/num_reads > .7:
            const_G_positions.append(pos)
        elif numG/num_reads > .55:
            mostly_G_positions.append(pos)
    log['num reads']['initial'] = num_reads
    log['num G by pos'] = {pos:num for pos,num in enumerate(num_G_at_pos)}
    log['frac G by pos'] = {pos:num/num_reads for pos,num in enumerate(num_G_at_pos)}
    if mostly_G_positions:
        log['mostlyG positions'] = mostly_G_positions
        #raise Exception('oh noes, found positions that were 55-70% G with {!r}'.format(log))
    num_G_in_5_thru_10 = count(pos in const_G_positions for pos in [5,6,7,8,9,10])
    if 0 == len(const_G_positions):
        raise Exception("file doesn't have any constG positions, {!r}".format(log))
    if num_G_in_5_thru_10 < 2:
        raise Exception('oh noes, only {} positions in bases 5-10 were const G with {!r}'.format(
                num_G_in_5_thru_10, log))
    if len(const_G_positions) > num_G_in_5_thru_10:
        raise Exception('oh noes, some positions outside 5-10 have const G with {!r}'.format(log))
    return const_G_positions

def _get_constG_reads(fname, const_g_positions, log):
    reads = get_reads(fname)
    n = 0
    #reads = itertools.islice(reads, 0, 10) # while debugging
    for read in reads:
        if all(read.seq[pos] == 'G' for pos in const_g_positions):
            n += 1
            yield read
    log['num reads']['with correct Gs'] = n

def get_constG_reads(fname, log):
    constG_positions = get_constG_positions(fname, log)
    log['constG_positions'] = constG_positions

    constG_reads = _get_constG_reads(fname, constG_positions, log)
    return constG_reads, constG_positions


def get_qual(c):
    phred = ord(c) - 33
    if not 0 <= phred <= 60:
        raise Exception("bad qual (letter {!r}, number {})".format(c, phred))
    return phred
def filter_by_UMI_qual(reads, log):
    n = 0
    for read in reads:
        if all(get_qual(read.qual[i]) > 20 for i in range(5)):
            yield read
            n += 1
    log['num reads']['with good UMI phred'] = n

def push_UMI_into_readname(reads, constG_positions, log):
    n=0
    for read in reads:
        umi = read.seq[:5]
        last_cgp = max(constG_positions)
        start_pos = last_cgp+1
        while start_pos < len(read.seq) and read.seq[start_pos] == 'G':
            start_pos += 1
        if start_pos < len(read.seq):
            yield Read(name=read.name + ' ' + umi,
                       seq=read.seq[start_pos:],
                       qual=read.qual[start_pos:])
            n+=1
    log['num reads']['that arent all G'] = n

def filter_out_repeating_suffix(reads, log):
    n = 0
    bad_suffixes = [b*10 for b in 'ACTG']
    for read in reads:
        if not any(read.seq.endswith(bad_suffix) for bad_suffix in bad_suffixes):
            yield read
            n += 1
    log['num reads']['with okay suffixes'] = n

def write_reads_to_file(reads, output_filename):
    with gzip.open(output_filename, 'wt') as f:
        for read in reads:
            f.write(read.name)
            f.write('\n')
            f.write(read.seq)
            f.write('\n+\n')
            f.write(read.qual)
            f.write('\n')

def convert_sample(fname):
    out_fname = fname.replace('fastq/', 'fastq-cleaned-up/')
    if os.path.exists(out_fname + '.log'):
        print('already did ' + out_fname)
        return

    log = {
        'num reads': {},
        'perc reads': {},
        'input_file': fname,
        'output_file': out_fname,
    }
    print(fname, '->', out_fname)
    try:
        reads, constG_positions = get_constG_reads(fname, log)
        reads = filter_by_UMI_qual(reads, log)
        reads = push_UMI_into_readname(reads, constG_positions, log)
        reads = filter_out_repeating_suffix(reads, log)
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
    infiles = list(glob.glob('fastq/SRR*.fastq.gz'))
    print('found {} input files'.format(len(infiles)))
    for infile in infiles:
        log_fname = infile.replace('fastq/', 'fastq-cleaned-up/') + '.log'
        if not os.path.exists(log_fname):
            yield infile

if __name__ == '__main__':
    fnames = list(get_fnames_to_convert())
    print('found {} files that need to be processed'.format(len(fnames)))

    pool = multiprocessing.Pool(8)
    pool.map(convert_sample, fnames)

    # for fname in fnames:
    #     convert_sample(fname)
