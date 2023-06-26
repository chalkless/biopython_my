#/usr/bin/env python3

from Bio import Entrez
import sys

Entrez.email = "nakazato.tkr@gmail.com"

term_search = sys.argv[1]

# eserach部
handle = Entrez.esearch(db = "pubmed", term = term_search, usehistory="y")
records = Entrez.read(handle)

# print(records)

token   = records['WebEnv']
q_key   = records['QueryKey']
count = int(records['Count'])

# efetch部

retmax = 1000

for start in range(0, count, retmax):
    handle = Entrez.efetch(db='pubmed', retmode='xml', restart=start, retmax=retmax, webenv=token, query_key=q_key)
    records = Entrez.read(handle)
    
    for record in records["PubmedArticle"]:
        print(record["MedlineCitation"]["PMID"])
        meshlist = record["MedlineCitation"]["MeshHeadingList"]

        for mesh in meshlist:
            print(mesh)
