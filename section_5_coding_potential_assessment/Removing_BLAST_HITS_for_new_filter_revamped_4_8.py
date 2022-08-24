#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import argparse
import numpy as np

# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input_name')
args = parser.parse_args()


args = parser.parse_args()
# read stuff in for un annotated genes
file1= "./"+args.input_name+"/"+args.input_name+"_LncRNA_refined.gff"
file2="./"+args.input_name +"/"+args.input_name+"_BLAST_HITS.csv"
file3="./"+args.input_name+"/"+args.input_name+"_LncRNA_refined_blast_removed.gff"
file4 = "./"+args.input_name+"/"+args.input_name+"_Dropped_blast.gff"
file5="./"+args.input_name+"/"+args.input_name+"_LncRNA_Final.txt"
file6="./"+args.input_name+"/"+args.input_name+"blast_removed_NF.txt"



df=pd.read_csv(file1, header=None,sep=("\t"))
df["transcripts"]=df.iloc[:,8].str.split(";", expand=True)[0].str.split("=", expand=True)[1]
df_blast=df.copy()
# BLAST genes


# read in blast results
removers=pd.read_csv(file2, header=None)
####IF Positive on same strand, negative on opposite
removers["dif"]=(removers.iloc[:,7])- (removers.iloc[:,6])
removers.columns=["A","B","C","D","E","F","G","H","I","J","K","L","dif"]
############# SIZE overlap on cDNA of subject
removers["overlap"]=abs(removers.iloc[:,9])- (removers.iloc[:,8])
removers["name"]=removers.iloc[:,0]
removers["subject"]=removers.iloc[:,1]
blast_hitsa=removers.copy()
blast_hitsb=removers.copy()
# then on same strand, sense blast_hitsa
blast_hitsa=blast_hitsa[blast_hitsa["dif"]>0]
# antisense blast_hitsb
blast_hitsb=blast_hitsb[(blast_hitsb["dif"]<0)]
# get out values
blast_hitsa_overlap_sum=blast_hitsa.groupby(by = "A").agg(
    SumA = ("overlap", np.sum),
    MinA = ("overlap", np.max),
    CountA = ("overlap", np.size))
blast_hitsb_overlap_sum=blast_hitsb.groupby(by = "A").agg(
    SumB = ("overlap", np.sum),
    MinB = ("overlap", np.max),
    CountB = ("overlap", np.size))
blast_hitsa_overlap_sum["names"]=blast_hitsa_overlap_sum.index
blast_hitsb_overlap_sum["names"]=blast_hitsb_overlap_sum.index

# Add 1 to each

#Now merge data frames
blast_hits_merge=blast_hitsa_overlap_sum.merge(blast_hitsb_overlap_sum, how="outer", on ="names").fillna(1)
blast_hits_merge.SumA=blast_hits_merge.SumA+1
blast_hits_merge.SumB=blast_hits_merge.SumB+1

# get a log10 ratio of antisense/sense - then anything where sense is much more will be below 0
a=blast_hits_merge.SumB/blast_hits_merge.SumA
b=np.log10(a)
blast_hits_merge["antisense_sense"]=a
blast_hits_merge["log10antisense_sense"]=b
blast_hits_merge["colour"]="r"
blast_hits_merge.colour[((blast_hits_merge.log10antisense_sense<-0.5)&(blast_hits_merge.MinA<30))|(blast_hits_merge.CountA <2)]="b"

blast_hits_merge.colour[(blast_hits_merge.log10antisense_sense>-0.5)]="g"
hits=blast_hits_merge[blast_hits_merge.colour=="r"].names.tolist()
with open(file6, "w") as output:
    for s in hits:
       output.write( s +'\n')





print(args.input_name, "length removers= ",len(hits))





to_remove=hits
print(to_remove)
df_blast=df.copy()[(df.transcripts.isin(to_remove))]
df_new_lncRNA=df.copy()[~(df.transcripts.isin(to_remove))]
print(args.input_name,": has this number LncRNAs after Blast removal",str(sum(df_new_lncRNA.iloc[:,2]=="transcript")),"\n" )
df_new_lncRNA.iloc[:,:9].to_csv(file3, header=False, index= None, sep="\t")
df_blast.iloc[:,:9].to_csv(file4, header=False, index= None, sep="\t")
with open(file5, "w") as output:
    for s in df_new_lncRNA.transcripts.unique():
        output.write(s +'\n')














