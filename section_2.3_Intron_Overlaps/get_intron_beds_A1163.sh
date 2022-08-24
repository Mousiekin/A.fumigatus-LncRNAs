#!/bin/bash
FILE="$1" 
for line in $(cat "$FILE" )    
do
    echo "$line"
  
file_name=$(echo $line|awk -F "/" '{print $2}')



#get splice sites need to downloadhisat2_extract_splice_sites.py from github
python hisat2_extract_splice_sites.py ../$line > "$file_name"_splice_sites.txt 

#split forward and reverse apart
#forward reads
#get forward reads
awk '{
        if($4 =="+")
        {
            print $1":"$2 "-"$3;
        }
}' "$file_name"_splice_sites.txt  >"$file_name"trial_forward.txt
echo "$file_name"trial_forward.txt >>bedMake_list.txt

#reverse reads
awk '{
        if($4 =="-")
        {
            print $1":"$2 "-"$3;
        }
}' "$file_name"_splice_sites.txt>"$file_name"trial_reverse.txt
echo "$file_name"trial_reverse.txt >>bedMake_list.txt
done


python intron_bed_making_just_beds1.py

