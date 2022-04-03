#!/bin/bash

file="dependencies.txt"
pwd
while read dependency separator version
do
echo -e "\t $dependency\n\
    \t $separator\n\
    \t $version\n"
done < 