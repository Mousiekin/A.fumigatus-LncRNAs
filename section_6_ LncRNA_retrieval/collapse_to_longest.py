#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import csv
import numpy as np
import argparse
# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input_file')
args = parser.parse_args()
df2=pd.read_csv(args.input_file,header=None,comment='#', sep="\t")
df2.columns=["zero","one","type","start","end","five","six","seven","info"]
df2["sizer"]=df2.loc[:,"end"]-df2.loc[:,"start"]
df2["xloc"]=df2["info"].str.split("xloc", expand=True)[1].str.split('"', expand=True)[1]
df2["transcript_id"]=df2["info"].str.split('"', expand=True)[1]
dfg=df2.groupby(by= "xloc").sizer.agg(np.max)
dfg2=pd.DataFrame(dfg)
dfg2["xloc"]=dfg2.index
x=list(range(0,dfg2.shape[0]))
dfg2["x"]= x
dfg2=dfg2.set_index("x")
df2_merge=df2.merge(dfg2, how="outer", on="xloc")
transcripts_to_keep=df2_merge[df2_merge.sizer_x==df2_merge.sizer_y].transcript_id.tolist()
df3=df2[df2.transcript_id.isin(transcripts_to_keep)]
# still have two the same if same size
transcript_ids=df3.groupby("xloc").first().transcript_id.tolist()
df4=df3[df3.transcript_id.isin(transcript_ids)]
new_file_name= args.input_file+"longest_.gtf"
df4.iloc[:,0:9].to_csv(new_file_name, header=False, index= None, sep="\t",quoting=csv.QUOTE_NONE) 
