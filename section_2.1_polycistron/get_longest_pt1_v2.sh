#!/bin/bash 

FOLDER="$1"

ls "$FOLDER"/*.gtf -1 > gtf_list.txt



while read file; do
python get_longest.py -i $file
done < gtf_list.txt

