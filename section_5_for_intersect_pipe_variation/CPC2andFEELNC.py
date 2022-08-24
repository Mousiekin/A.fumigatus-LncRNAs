#!/bin/bash

import pandas as pd
import argparse
# Parse arguments in from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input_CPC2')
parser.add_argument(
    '-g',
    '--input_FEELnc')

args = parser.parse_args()

coding_non=pd.read_csv(args.input_CPC2, sep="\t")
feelnc_ids=pd.read_csv(args.input_FEELnc, sep="\t").iloc[:,0].tolist()
cpc_ids = coding_non[coding_non.label=="noncoding"].loc[:,"#ID"].tolist()
cpc_noncod=[]
feelnc_noncod=[]
cpat_noncod=[] 
for line in cpc_ids:
    line=line.rstrip()
    cpc_noncod.append(line.upper())
for line in feelnc_ids:
    line=line.rstrip()
    feelnc_noncod.append(line.upper())
overlap = list(set(feelnc_noncod) & set(cpc_noncod)) 
with open("AF293_Both_NC.txt", "w") as output:
    for s in overlap:
        output.write( s +'\n')
                      

