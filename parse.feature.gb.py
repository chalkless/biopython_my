#!/usr/bin/env python3

import sys
import os
import re
import inspect
import argparse
from Bio import SeqIO

#file_gb_in = sys.argv[1]       # input gb file path

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

#    features = record.features   # list
#    for feat in features:
#        for k in feat.qualifiers.keys():
#            vals = feat.qualifiers[k]
#            vals_out = "|".join(vals)

    annots = record.annotations
    taxonomy = annots['taxonomy']

#    if option_each:
#        print(id, file=sys.stderr)
#        source = annots['source']
#        tmp = '\t'.join(map(str,[id, source]))
#        print(tmp, file=sys.stderr)



    if taxon_search in taxonomy:
#        print(id)

        if option_each:
#            print(id, file=sys.stderr)
            source = annots['source']
            tmp = '\t'.join(map(str,[id, source]))
            print(tmp, file=sys.stderr)


        features = record.features   # list
        for feat in features:
            for k in feat.qualifiers.keys():
                vals = feat.qualifiers[k]
                vals_out = "|".join(vals)

                out = '\t'.join(map(str,[id, k, vals_out]))
                print(out)




        
