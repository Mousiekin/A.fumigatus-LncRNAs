#!/bin/bash 


ls -1 *long.gtf > gtf_list2.txt
while read file; do
gtf2bed <$file>$file.long.bed
done < gtf_list2.txt
