#!/bin/bash

while read file; do
try_play=$(echo $file | awk -F'2_7_GTF/' '{print $2}'|awk -F'.' '{print $1}')
echo "$try_play">crazy.txt

gffcompare $file -T -o "$try_play".stats -T -r Aspergillus_fumigatusa1163.ASM15014v1.53.gtf
echo "$try_play".stats >>stats_list.txt
done < gtf_list.txt

while read file; do

x=($(echo $file | awk -F'A1163' '{print $2}'|awk -F'default' '{print $1}' ;cat $file | grep "Base level"| awk -F':' '{ print $2 }'|awk -F'|' '{ print $1 "\t" $2  }'))

echo "${x[@]}"
done < stats_list.txt>trial_output.txt


