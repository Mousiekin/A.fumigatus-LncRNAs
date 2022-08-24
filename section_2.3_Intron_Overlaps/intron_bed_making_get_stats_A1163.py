#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
bed_stats=pd.read_csv("to_comp_introns2.txt", header=None)
def stat_making(a,b,c):
    aa=pd.read_csv(a, header=None, sep="\t")
    aa["amount"]=aa.iloc[:,2].astype("int64")-aa.iloc[:,1].astype("int64")
    asum=sum(aa["amount"])
    bb=pd.read_csv(b, sep="\t",header=None)
    bb["amount"]=bb.iloc[:,2].astype("int64")-bb.iloc[:,1].astype("int64")
    bsum=sum(bb["amount"])
    cc=pd.read_csv(c,sep="\t", header=None)
    cc["amount"]=cc.iloc[:,2].astype("int64")-cc.iloc[:,1].astype("int64")
    csum=sum(cc["amount"])
    print(200*csum/(asum+bsum))
    print(asum,bsum,csum)
    return (200*csum/(asum+bsum))
intron_overlap={}
for i in range(len(bed_stats.iloc[:,0])):
    j=bed_stats.iloc[i,0]
    print(j)
    a=j+".gtftrial_forward.txt.bed"
    b=j+".gtftrial_reverse.txt.bed"
    c=j+"int_comp.txt"
    k = (j.split("default")[0])
    k=(k.split("A1163")[1])
    intron_overlap[k] = stat_making(a,b,c)
df=pd.DataFrame.from_dict(intron_overlap, orient='index')
df.to_csv("intron_overlap.csv")




