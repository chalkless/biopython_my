#!/usr/bin/env python3                                                          

import argparse
import pprint
import re
import time
from Bio import Entrez

Entrez.email = "A.N.Other@example.com"
# Entrez.api_key = "XXX"

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str)
parser.add_argument('-i', '--pmid', type=str)
args = parser.parse_args()

file_in = args.file
pmid_in = args.pmid

list_pmid = []

if len(file_in):
    with open(file_in) as f:
        p_list = [s.rstrip() for s in f.readlines()]

        retmax = 100
        for i in range(0, len(p_list), retmax):
            list_sub = p_list[i:i+retmax]
            pmid_query = ",".join(list_sub)
            #        print(pmid_query)   # for debug                            

            # PMID → abst
            time.sleep(4)
            handle = Entrez.efetch(db='pubmed', id=pmid_query, retmode='xml')
            records = Entrez.read(handle)

            for record in records["PubmedArticle"]:

                pmid  = record["MedlineCitation"]["PMID"]

                article = record["MedlineCitation"]["Article"]

                title   = article["ArticleTitle"]
                journal = article['Journal']['ISOAbbreviation']
                pubyear = article['Journal']['JournalIssue']['PubDate']['Year']

                extlinks = article['ELocationID']
                for eachlink in extlinks:
                    extstr = str(eachlink)

                    doi_tmp = re.search("10\.\d+/.*", extstr)
                    if doi_tmp:
                        doi = doi_tmp.group()

#                print(pmid)                                                    
#                print(title)                                                   
#                print(journal)                                                 
#                print(pubyear)                                                 
#                print(doi)                                                     

                str_out = '\t'.join((pmid, doi, title, journal, pubyear))
                print(str_out)

                doi = ""
