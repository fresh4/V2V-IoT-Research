#!/bin/bash
cd "$(dirname "$0")"
cd ..

FOLDER_NAME="env"

# Install local software for RTL SDR
# MAKE SURE TO INSTALL PROPER VERSIONS: rtl-433 >23.11 and rtl-sdr. 
# Different repositories on different Linux systems may not be up to date, so you'll have to manually get them. 
sudo apt install rtl-sdr rtl-433 sqlite3 -y

if [-d "$FOLDER_NAME"]; then
    echo "Python environment already exists"
else
    echo "Creating Python environment"
    python -m venv env
    ./env/bin/python -m pip install -r requirements.txt