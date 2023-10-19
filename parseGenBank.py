#!/usr/bin/env python3

import sys
import os
import re
import inspect
import argparse
from Bio import SeqIO

debug = 1

# gb_file = sys.argv[1]     # input gb file path

parser = argparse.ArgumentParser()
parser.add_argument('--file_in', '-f')
parser.add_argument('--taxon', '-t')
parser.add_argument('--detail_each', '-d', action="store_true")
args = parser.parse_args()

gb_file = args.file_in
taxon_search = args.taxon
option_each = args.detail_each


for record in SeqIO.parse(gb_file, 'genbank'):

    if debug == 2:
        print(inspect.getmembers(record))   # for debug

#    if debug == 2:                          # another way to debug
#        print("[record]")
#        for x in dir(record):
#            print(x)

    id = record.id
    name = record.name
    desc = record.description
    xrefs = record.dbxrefs     # list
    annots = record.annotations     # dic
    features = record.features # list
    seq  = record.seq


#    print('ID:\t' + id)
#    print('name:\t' + name)
#    print('desc:\t' + desc)
#    print('seq:\t' + seq)

    # annotation
    ## source
    keyword = annots['keywords']    # list
    source = annots['source']
    organism = annots['organism']
    taxonomy = annots['taxonomy']   # list
    date = annots['date']

    if taxon_search in taxonomy:

#    print('source:\t' + source)
#    print('organism:\t' + organism)

        keyword_out = "|".join(keyword)

#    print('taxonomy:')
#    for t in taxonomy:
#       print('\t' + t)

        taxontree = '|'.join(taxonomy)

        ## reference
        for ref in annots['references']:
            pmid = ref.pubmed_id
            medline = ref.medline_id
            journal = ref.journal

#        print('pmid:\t' + pmid)
#        print('medline:\t' + medline)
#        print('journal:\t' + journal)

        # features
        gene = "-"
        organelle = "-"
        bold = "-"
        voucherID = "-"
        note = "-"

        for feat in features:
            type = feat.type
#        print('type:\t' + type)

            for k in feat.qualifiers.keys():
                vals = feat.qualifiers[k]

                if k == 'organism':
                    org = "|".join(vals)
                elif k == 'db_xref':
                    for v in vals:
                        if 'taxon:' in v:
                            taxon = v
                        elif 'BOLD:' in v:
                            bold = v
                            #                    taxon = re.match(r"taxon:", v)
                            #                    bold  = re.match("BOLD:", v)
                elif k == 'organelle':
                    organelle = "|".join(vals)
                elif k == 'specimen_voucher':
                    voucherID = "|".join(vals)
                elif type == 'gene' and k == 'gene':
                    gene = "|".join(vals)
                elif k == 'note':
                    note = "|".join(vals)
                            
        out = '\t'.join(map(str,[id, gene, organism, taxon, organelle, keyword_out, voucherID, bold, note, desc, taxontree]))
        print(out)

#            print('subtype:\t' + k, end="")
#            vals = feat.qualifiers[k]
#            for v in vals:
#                print('\t' + v)

#        quals = feat.qualifiers[type]  # list
#        for q in quals:
#            print(type + '\t' + q)





