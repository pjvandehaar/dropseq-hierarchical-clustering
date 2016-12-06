mkdir -p fastq-cleaned-up2-fastqc

fastqc -o fastq-cleaned-up2-fastqc/ -t 6 fastq-cleaned-up2/*.gz

multiqc fastq-cleaned-up2-fastqc/ -o fastq-cleaned-up2-multiqc/