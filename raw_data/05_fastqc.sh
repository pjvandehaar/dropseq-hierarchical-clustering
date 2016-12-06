fastqc -o fastq-cleaned-up-fastqc/ -t 6 fastq-cleaned-up/*.gz

multiqc fastq-cleaned-up-fastqc/ -o fastq-cleaned-up-multiqc/