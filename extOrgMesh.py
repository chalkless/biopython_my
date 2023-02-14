#!/usr/bin/env python3

# extOrgMesh.ph
# Nakazato T.
# '22-09-08    Ver. 0.1
# '23-02-15    Ver. 0.2
# 
# NOTE: The txids extracted from RN section are sometimes outdated. Please compare your results with NCBI Taxonomy.
#       I may to write a script to solve it.

import sys
import re

p_term = r'^MH = '
p_id   = r'^UI = '
p_rn   = r'^RN = txid'
p_tree = r'^MN = '

term = ""
taxon = ""
id_m = ""
trees = []


f_mesh = sys.argv[1]      # d2022.bin

with open(f_mesh) as f:
    for line_p in f:
        line = line_p.rstrip()

        if re.compile(p_term).search(line):
            term = re.sub(p_term, '', line)
        elif re.compile(p_rn).search(line):
            taxon = re.sub(p_rn, '', line)
        elif re.compile(p_tree).search(line):
            tree = re.sub(p_tree, '', line)
            trees.append(tree)
        elif re.compile(p_id).search(line):
            id_m = re.sub(p_id, '', line)
            trees_out = ",".join(trees)
            if taxon:
                print("\t".join([id_m, term, trees_out, taxon]))
            
            id_m = ""
            term = ""
            trees = []
            taxon = ""

