#!/bin/bash 
counter = 0
for line in $(cat ./links/all.txt)
do
((counter++)) 
echo "$line $counter"
#sleep 1
done
