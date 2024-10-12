#!/bin/bash
cd "$(dirname "$0")"
cd ..

# Argument for specifying frequency
frequency="315"
if [ -n "$1" ]; then
    frequency="$1"
fi

rtl_433 -f ${frequency}M -M level -M time -C customary -F json | ./env/bin/python3 scripts/record_tpms.py