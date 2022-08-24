#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
bedToMake=pd.read_csv("bedMake_list.txt", header=None)
def bed_making(x):
    y=pd.read_csv(x, header=None)
    y.columns= ["name"]
    y[["chr","start"]]=y.iloc[:,0].str.split(":", expand=True)
    y[["start","end"]]=y["start"].str.split("-", expand=True)
    y["strand"]="+"
    y["score"]=1
    y= y[["chr", "start","end","name","score","strand"]]
    y.to_csv(x+".bed", sep="\t",index=False, header=None)
for i in range(len(bedToMake.iloc[:,0])):
    bed_making(bedToMake.iloc[i,0])
bedToMake.iloc[:,0]=(bedToMake.iloc[:,0]).str.split(".gtf", expand=True)[0]
x=bedToMake.drop_duplicates()
x.to_csv("to_comp_introns2.txt",index=False, header=None)

