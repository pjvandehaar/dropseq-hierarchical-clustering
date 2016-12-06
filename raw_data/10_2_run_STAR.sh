#!/bin/bash
set -euo pipefail

# TODO: read multimaping section of https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf

file_containing_names=$1
outdir=/users/pjvh/binf527-proj/writable/mapped2/
mkdir -p $outdir
tmpdir="$(mktemp -d)"

#for infile in /users/pjvh/binf527-proj/raw_data/fastq-cleaned-up4/SRR*_trimmed.fq.gz; do
cat $file_containing_names | while read infile; do
    echo $(date +"%b %d %T") $infile
    bname="$(basename $infile | perl -pale 's{_.*}{}')"

    # This way we can re-run this script and it won't repeat any work.
    if ! [[ -e $outdir/$bname.done ]]; then
        #unsafety measure
        rm -f $outdir/$bname.done
        /users/pjvh/binf527-proj/writable/STAR-2.5.2b/bin/Linux_x86_64_static/STAR \
            --runThreadN 4 \
            --genomeDir /users/pjvh/binf527-proj/writable/HumanReferences/startry1/ \
            --readFilesIn $infile \
            --readFilesCommand zcat \
            --outSAMtype BAM SortedByCoordinate \
            --outFileNamePrefix $outdir/$bname- \
            --outTmpDir "$tmpdir/foo" \
            --genomeLoad LoadAndKeep \
            --limitBAMsortRAM $((15*10**9)) \
            --quantMode TranscriptomeSAM GeneCounts

#            &> $outdir/$bname.stdout
        #safety measure
        touch $outdir/$bname.done
    fi
done

rm -r "$tmpdir"
echo DONE
