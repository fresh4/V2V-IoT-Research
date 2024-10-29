#!/bin/bash
# This script is specifically for running multiple instances and recording two SDRs at the same time
# If you want to change any arguments just change them in this file. It does not handle passing in
# arguments from the CLI.
cd "$(dirname "$0")"
cd ..

trap killgroup SIGINT

killgroup(){
  echo killing...
  kill 0
}

echo "########## STARTING SERVER ##########"
./env/bin/python3 scripts/obd_server.py &

while ! nc -z localhost 48484; do   
  sleep 1  # wait for server to start
done

echo "########## STARTING READERS ##########"
(rtl_433 -M level -M time -C customary -F json -f 315M -d 0 | ./env/bin/python3 scripts/record_tpms.py samples1.db) &
(rtl_433 -M level -M time -C customary -F json -f 315M -d 1 | ./env/bin/python3 scripts/record_tpms.py samples2.db) &
wait
