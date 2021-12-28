#!/usr/env/python3

import sys
import os
import re
import argparse
import inspect
from Bio import GenBank

debug = 1

parser = argparse.ArgumentParser()
parser.add_argument('--file_in', '-f')
parser.add_argument('--taxon', '-t')
parser.add_argument('--detail_each', '-d', action="store_true")
args = parser.parse_args()

file_gb_in = args.file_in
taxon_search = args.taxon
option_each = args.detail_each

with open(file_gb_in) as handle:
    for record in GenBank.parse(handle):
        print(inspect.getmembers(record))
        if option_each:
            print(record.accession, file=sys.stderr)
        taxonomy = record.taxonomy
        if taxon_search in taxonomy:
            print(record)
