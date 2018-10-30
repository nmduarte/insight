#!/bin/bash
#
# The python script is using Python3.

#gets python version and extract it
version=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')
#parses the value
parsedVersion=$(echo "${version//./}")

#if it's not python3, then don't run it
if [[ "$parsedVersion" -lt "300" ]]
then
    echo "Invalid version - please use python 3"
else
    python ./src/h1b_certified_stats.py
fi

