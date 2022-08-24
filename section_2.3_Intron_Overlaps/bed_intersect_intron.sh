#!/bin/bash
FILE="$1" 
for line in $(cat "$FILE" )    
do
    echo "$line"

bedtools intersect -s -a "$line".gtftrial_forward.txt.bed -b "$line".gtftrial_reverse.txt.bed>"$line"int_comp.txt
done
