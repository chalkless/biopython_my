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
args = parser.parse_args()

file_gb_in = args.file_in
taxon_search = args.taxon

with open(file_gb_in) as handle:
    for record in GenBank.parse(handle):
#        print(inspect.getmembers(record))
        taxonomy = record.taxonomy
        if taxon_search in taxonomy:
            print(record)
