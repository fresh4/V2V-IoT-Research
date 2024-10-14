#!/bin/bash
cd "$(dirname "$0")"
cd ..
mkdir -p outputs/raw_iq

# Argument for specifying frequency
frequency="315"
if [ -n "$1" ]; then
    frequency="$1"
fi

# Run the recorder until interrupted.
rtl_433 -f ${frequency}M -M level -M time -C customary -F json -S known | ./env/bin/python3 scripts/record_tpms.py

# Clean up and move *.cu8 files to the raw_iq outputs folder
ls *.cu8  >/dev/null || exit
echo "Cleaning up..."
dirname=$(date | tr ' ' '-')
mkdir outputs/raw_iq/$dirname
mv *.cu8 outputs/raw_iq/$dirname
echo "Saved output files under outputs/raw_iq/$dirname"