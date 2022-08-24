#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import argparse
# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input_file')
args = parser.parse_args()
df2=pd.read_csv(args.input_file,header=None,skiprows=2, sep="\t")
df2.columns=["zero","one","type","start","end","five","six","seven","info"]
df2["size"]=df2.loc[:,"end"]-df2.loc[:,"start"]
df2[["gene_id","transcript_id"]]=df2["info"].str.split(";", expand=True)[[0,1]]
df3=df2.copy()[df2["type"]=="transcript"]
df3=df3.loc[df3.groupby("gene_id")["size"].idxmax()]
list_poss=df3["transcript_id"].tolist()
df2=df2[df2["transcript_id"].isin(list_poss)]    
df2=df2.drop(columns=["size", "gene_id","transcript_id"])
x=args.input_file.split("/")[-1]  
df2.to_csv(x+"long.gtf",sep="\t",header=False, index=False)   

