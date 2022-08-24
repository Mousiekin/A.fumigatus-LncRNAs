#!/bin/bash 


ls -1 *long.bed > bed_list.txt
while read file; do
bedtools intersect -a AF1163.v1.53.bed -b $file -wa -wb -s > $file.csv
done < bed_list.txt

ls -1 *long.bed.csv > csv_bed_list.txt


