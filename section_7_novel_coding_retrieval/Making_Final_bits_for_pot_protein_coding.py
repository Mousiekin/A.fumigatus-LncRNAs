#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import csv
import argparse
# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    '-p',
    '--prefix')
args = parser.parse_args()
# read stuff in for unannotated genes
file1 = args.prefix+"_unknown_and_antisense_longest_transcripts.gtf"
file2 = args.prefix+"_dropped_FEELNC_CPC2_BLAST_notRFAM_DISCARDS.txt"
file3 = args.prefix+"_Pot_Proteins_removed.gtf"

df=pd.read_csv(file1, comment ="#",header=None,sep=("\t"))
df["transcripts"]=df.iloc[:,8].str.split('transcript_id "', expand=True)[1].str.split('";', expand=True)[0].str.strip()
# Get discarded potential protein coding
keepers=pd.read_csv(file2, header=None)
to_keep=keepers[0].tolist()
df_PotProt=df.copy()[(df.transcripts.isin(to_keep))]
df_PotProt.iloc[:,:9].to_csv(file3, header=False, index= None, sep="\t",quoting=csv.QUOTE_NONE)

