#!/bin/bash

set -euo pipefail

# I can ssh to the site with filezilla but can't figure out how to do it from bcs2.  Hence, nasty shell scripts.
baseurl=ftp://ftp-trace.ncbi.nlm.nih.gov:21/sra/sra-instant/reads/ByStudy/sra/SRP/SRP045/SRP045452/
curl "$baseurl" |
awk '{print $NF}' |
while read fname; do
    wget -P sra "$baseurl/$fname/$fname.sra"
done