#!/bin/bash
cd "$(dirname "$0")"
cd ..
mkdir -p outputs/raw_iq

# Default args, replaced if any args are manually input
args="-f 315M"
dbname=""
if [ -n "$1" ]; then
    args=""
    for arg in "$@"; do
        if [[ $arg == *"--dbname="* ]]; then
            dbname="${arg#--dbname=}"
            continue
        fi
        args+="$arg "
    done
fi

# Run the recorder until interrupted. -S known
rtl_433 -M level -M time -C customary -F json ${args} | ./env/bin/python3 scripts/record_tpms.py ${dbname}

# Clean up and move *.cu8 files to the raw_iq outputs folder
ls *.cu8  &> /dev/null || exit
echo "Cleaning up..."
dirname=$(date | tr ' ' '-')
mkdir outputs/raw_iq/$dirname
mv *.cu8 outputs/raw_iq/$dirname
echo "Saved output files under outputs/raw_iq/$dirname"