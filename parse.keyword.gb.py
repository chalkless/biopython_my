#!/usr/env/python3

import sys
import os
import re
import inspect
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('--file_in', '-f')
parser.add_argument('--taxon', '-t')
parser.add_argument('--detail_each', '-d', action="store_true")
args = parser.parse_args()

file_gb_in = args.file_in
taxon_search = args.taxon
option_each = args.detail_each

for record in SeqIO.parse(file_gb_in, 'genbank'):

    id = record.id

    annots = record.annotations
    taxonomy = annots['taxonomy']


    if taxon_search in taxonomy:
        if option_each:
            source = annots['source']
            tmp = '\t'.join(map(str,[id, source]))
            print(tmp, file=sys.stderr)


#        keyword_out = record.description
        keyword = annots['keywords'] # list
        keyword_out = "|".join(keyword)

        out = '\t'.join(map(str,[id, keyword_out]))
        print(out)

