#!/bin/bash
cd "$(dirname "$0")"
cd ..

FOLDER_NAME="env"

# Install local software for RTL SDR
sudo apt install rtl-sdr rtl-433 -y

if [-d "$FOLDER_NAME"]; then
    echo "Python environment already exists"
else
    echo "Creating Python environment"
    python -m venv env
    ./env/bin/python -m pip install -r requirements.txt