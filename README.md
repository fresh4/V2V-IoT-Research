This repository holds scripts used for recording and analysis of EM signals for V2V research.

# Installation and Dependencies

The code in this repository are meant to be run on Linux based systems such as the Raspberry Pi.\
The `setup.sh` script under `bash_scripts/` should set up your environment and dependencies, but should it fail, here's what's required.

`rtl-433` version 23.11 or greater. Depending on your system, your package manager may have a lower version in its repositories. In that case you will need to manually install it from a repository that has the proper version.\
`rtl-sdr` installed from the same repository as `rtl-433`, preferably. `rtl-433` depends on `rtl-sdr`, so they must both be up to date.\
`sqlite3` for running sqlite commands.\
`python3.10` or greater. You will need to create a virtual environment in python using venv (or conda) and install the dependencies in the `requirements.txt`

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# SDR TPMS Monitoring

To record TPMS signals a specific device set up is required.

You will first need `rtl_433`, and `rtl-sdr` installed on your machine.\
You will also need a python environment installed and activated using the provided `requirements.txt`.\
Your (Linux) device will need some RTL-SDR reader attached to read TPMS signals.\
Your device will also need an OBD connection made from the car to read vehicle speed.

With all requirements met, you should be able to record TPMS data. Use the `record_tpms.sh` script under the `bash_scripts/` directory to start. It will read 315MHz by default but this can be modified to any desired frequency. `record_tpms.sh -f 433.95M` will switch to reading on the 433.95 channel. Any arguments compatible with `rtl_433` will work if appended after the script, too. The script does run certain arguments by default, however, so check out the script.

Decoded TPMS data will be saved under a local Sqlite database called `samples.db` in the project root directory. This format is great as it can be efficiently queried and filtered.

You can convert the table itself to a more easily usable csv via the `tpms_csv.sh` script under `bash_scripts/` as well. It will be saved under the `outputs/` directory. You can specify a different file name using `tpms_csv.sh <filename>.csv` (extension optional).
