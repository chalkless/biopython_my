#!/usr/bin/env python3

from Bio import Entrez
import sys
import re
import time


Entrez.email = "A.N.Other@example.com"

f_in = sys.argv[1]

with open(f_in) as f:
    list = [s.rstrip() for s in f.readlines()]


# PMIDリストを100ごとに分割
count = 100
for i in range(0, len(list), count):
    list_sub = list[i:i+count]
    pmid_query = ",".join(list_sub)
    # print(pmid_query)   # for debug

    # PMID → abst
    time.sleep(4)
    handle = Entrez.efetch(db='pubmed', id=pmid_query, retmode='xml')
    
    # ファイルに出力
    f_out = f_in
    f_out = re.sub(".txt", "", f_out)
    f_out = re.sub(".pmid(s|)", "", f_out)
    num = '{:0=4}'.format(i)
    f_out += "." + num + ".abst.xml"
    print(f_out)

    f = open(f_out, 'x')
    
    line_xml_b = handle.read()
    line_xml = line_xml_b.decode('utf-8')
    # print(line_xml)   # for debug
    f.write(line_xml)

    f.close
