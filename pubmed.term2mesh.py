#/usr/bin/env python3

from Bio import Entrez
import sys
import pprint
import re


Entrez.email = "A.N.Other@example.com"

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
        pmid = record["MedlineCitation"]["PMID"]
        
        if 'MeshHeadingList' in record['MedlineCitation']:
            for mesh in record['MedlineCitation']['MeshHeadingList']:
                
                descr = mesh['DescriptorName']

                mesh = descr.title()

                m_str = Entrez.Parser.StringElement.__repr__(descr)
                m_atr = re.findall(r'StringElement\((.*)\)$', m_str)
                for ele in m_atr:
                    if "attributes=" in ele:
                        m_id_l = re.findall(r'attributes={\'UI\':\s+\'(.*)\',\s+\'MajorTopicYN\':\s\'.\'', ele)
                        m_id = m_id_l[0]
                        print('\t'.join((pmid, m_id, mesh)))
                
