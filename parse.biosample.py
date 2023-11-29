#!/usr/bin/env python3

# parse.biosample.py
# '23-11-23-Thu.    Ver.0.1
# Nakazato T.

import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str)
args = parser.parse_args()

file_in = args.file

tree = ET.parse(file_in)
root = tree.getroot()

#print(root.tag)
#print(root.attrib)

for biosample in root:
#    print(biosample.tag)

    for ele1 in biosample:
#        print(ele1.tag)

        if ele1.tag == "Ids":

            for each_id in ele1:
            
#                print(each_id.tag)
#                print(each_id.attrib)
#                print(each_id.text)

                id_attrib = each_id.attrib
                
                if id_attrib.get('namespace'):    # for DDBJ
                    db = id_attrib.get('namespace')
                elif id_attrib.get('db'):        # for NCBI
                    db = id_attrib.get('db')
                    
                if db == "BioSample":
                    id_bs = each_id.text
                    print(id_bs)
                elif db != None:
                    #print("[db]\t" + db)
                    None
                else:
                    print("[OtherID]\t" + id_attrib)

                    
        elif ele1.tag == "Description":
            for each_desc in ele1:
                #print("[tag]\t" + each_desc.tag)
                #print("[attrib]\t" + str(each_desc.attrib))
                #print("[text]\t" + str(each_desc.text))

                desc_tag = each_desc.tag

                if desc_tag == "Title":
                    title = each_desc.text
                    print(title)
                elif desc_tag == "Organism":
                    desc_org = each_desc.attrib
                    taxid = desc_org.get('taxonomy_id')
                    if taxid == None:
                        taxid = "0"
                    taxon_name = desc_org.get('taxonomy_name')
                    if taxon_name == None:
                        for each_taxon in each_desc:
                            if each_taxon.tag == "OrganismName":
                                taxon_name = each_taxon.text
                        
                    print("\t".join([taxid, taxon_name]))
                elif desc_tag == "SampleName":
                    None
                elif desc_tag == "Comment":
                    None
                else:
                    print("[Other_desc]\t" + desc_tag)

        elif ele1.tag == "Owner":
            None
            
        elif ele1.tag == "Models":
            for each_model in ele1:
                #print("[tag]\t" + each_model.tag)
                #print("[attrib]\t" + str(each_model.attrib))
                #print("[text]\t" + str(each_model.text))

                model_tag = each_model.tag

                if model_tag == "Model":
                    model = each_model.text
                    print(model)
                else:
                    print("[Oter_model]\t" + model_tag)

        elif ele1.tag == "Package":
            None
            
        elif ele1.tag == "Attributes":
            for each_attr in ele1:
                print("[tag]\t" + each_attr.tag)
                print("[attrib]\t" + str(each_attr.attrib))
                print("[text]\t" + str(each_attr.text))

                attr_attr = each_attr.attrib
                print("[attr]\t" + attr_attr.get("attribute_name"))
                
        elif ele1.tag == "Status":
            status_attr = ele1.attrib
            status = status_attr.get('status')
            status_date = status_attr.get('when')
            print("\t".join([status, status_date]))
