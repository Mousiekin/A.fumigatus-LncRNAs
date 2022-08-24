#!/usr/bin/env python
# coding: utf-8

# In[1]:

import argparse
import pandas as pd
import csv

import argparse
# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input_name')


args = parser.parse_args()




# read stuff in for unannotated genes
X= str(args.input_name)
Y= (X+ "_unknown_and_antisense_longest_transcripts.gff3")
Z= ("cmscan_"+X+ "_lncRNAs.tblout")
df=pd.read_csv(Y,comment="#", header=None,sep=("\t"))
df["transcripts"]=df.iloc[:,8].str.split(";", expand=True)[0].str.split("=", expand=True)[1]
print (df.head(5))
#Read in  transcripts to keep
keepers=pd.read_csv("AF293_Both_NC.txt",header=None, sep=("\t"))
keepers=list(keepers[0])
print(keepers)

# RNA genes
removers=pd.read_csv(Z, header=None,sep=("\t"), comment =("#"))
print(removers)
#want to keep lncrnas not in annotation
removers=removers[removers.iloc[:,0].str.split(" ", expand=True)[4].apply(lambda x: "5_ureB_sRNA" not in x)]
removers=removers[removers.iloc[:,0].str.split(" ", expand=True)[4].apply(lambda x: "Afu_182" not in x)]
removers=removers[removers.iloc[:,0].str.split(" ", expand=True)[4].apply(lambda x: "Afu_309" not in x)]
to_remove=removers.iloc[2:,0].str.split("MSTRG",expand=True)[1].str.split("-",expand=True)[0].str.strip()
to_remove=pd.DataFrame(to_remove)
to_remove=to_remove.dropna()
to_remove.columns=["numbers"]
to_remove["MSTRG"]="MSTRG"
to_remove["Transcript"]=to_remove["MSTRG"] + to_remove["numbers"]
#Make a new list of keepers
more_keepers=[]
for i in keepers:
    if i not in to_remove.Transcript.tolist():
        more_keepers.append(i)
        
LncRNA_longest_transcripts=df[(df.transcripts.isin(more_keepers))]
df_protein=df[~(df.transcripts.isin(keepers))]
                     
# write info to disc
k=["length after FeelNC and CPC2: ", len(keepers),"\n Length after RFAM removal: ", len(more_keepers)]
textfile = open(args.input_name+"after_rfam.txt", "w")
for i in range(0,len(k)):
    textfile.write(str(k[i]))
textfile.close()
LncRNA_longest_transcripts.iloc[:,:9].to_csv(X+"_LncRNA_refined.gff", header=False, index= None, sep="\t",quoting=csv.QUOTE_NONE)                     
df_protein.iloc[:,:9].to_csv(X+"_Dropped_protein_coding_potential.gff", header=False, index= None, sep="\t",quoting=csv.QUOTE_NONE)
                  

