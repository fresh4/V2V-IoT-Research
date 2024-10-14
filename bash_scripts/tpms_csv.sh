#!/bin/bash
cd "$(dirname "$0")"
cd ..
mkdir -p outputs

# Argument to customize output filename
output_file="samples"
if [ -n "$1" ]; then
    output_file="$1"
fi
output_file="${output_file%.csv}"

sqlite3 -header -csv samples.db "SELECT * FROM TPMSSamples;" > outputs/$output_file.csv 

echo "Converted sql to csv under outputs/$outputfile.csv"