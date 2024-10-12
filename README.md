This repository holds scripts used for recording and analysis of EM signals for V2V research.

# SDR TPMS Monitoring

To record TPMS signals a specific device set up is required.

You will first need `rtl_433`, `obd` and `rtl-sdr` installed on your machine.\
You will also need a python environment installed and activated using the provided `requirements.txt`.\
Your (Linux) device will need some RTL-SDR reader attached to read TPMS signals.\
Your device will also need an OBD connection made from the car to read vehicle speed.

With all requirements met, you should be able to record TPMS data. Use the `record_tpms.sh` script under the `bash_scripts/` directory to start. It will read 315MHz by default but this can be modified to any desired frequency. `record_tpms.sh 433.95` will switch to reading on the 433.95 channel.

Decoded TPMS data will be saved under a local Sqlite database called `samples.db` in the project root directory. This format is great as it can be efficiently queried and filtered.

You can convert the table itself to a more easily usable csv via the `tpms_csv.sh` script under `bash_scripts/` as well. It will be saved under the `outputs/` directory. You can specify a different file name using `tpms_csv.sh <filename>.csv` (extension optional).
