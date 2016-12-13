#!/bin/bash

fin='best-genes.cef'
fout='best-genes-clustered.cef'

/users/pjvh/binf527-proj/writable/BackSPIN-1.0/backSPIN.py -i $fin -o $fout -v -d 5
