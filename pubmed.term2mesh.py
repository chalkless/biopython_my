#/usr/bin/env python3

from Bio import Entrez
import sys
import pprint
import re


Entrez.email = "nakazato.tkr@gmail.com"

term_search = sys.argv[1]

# eserach部
handle = Entrez.esearch(db = "pubmed", term = term_search, usehistory="y")
records = Entrez.read(handle)

#print(records)
count   = records['Count']
print(str(count) + " articles found", file=sys.stderr)

if int(count) > 9999:
    print("Results: " + count, file=sys.stderr) 
    print("Entrez efetch accepts up to 9999 entries. Change more restrict query, or use edirect.", file=sys.stderr)

token   = records['WebEnv']
q_key   = records['QueryKey']
count = int(records['Count'])

    
# efetch部

retmax = 1000
print("Retrieving articles...", file=sys.stderr)
for start in range(0, count, retmax):
    print(start, file=sys.stderr)
    handle = Entrez.efetch(db='pubmed', retmode='xml', retstart=start, retmax=retmax, webenv=token, query_key=q_key)
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
    handle.close()                
