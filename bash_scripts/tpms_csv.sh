#!/bin/bash
cd "$(dirname "$0")"
cd ..
mkdir -p outputs

# Argument to specify which *.db file to read and convert to csv.
input_file="${samples%.*}"
if [ -n "$1" ]; then
    input_file="$1"
fi
output_file=$input_file

sqlite3 -header -csv ${input_file}.db "SELECT * FROM TPMSSamples;" > outputs/$output_file.csv 

echo "Converted sql to csv under outputs/$output_file.csv"