#!/bin/bash
cd "$(dirname "$0")"
cd ..

trap killgroup SIGINT

killgroup(){
  echo killing...
  kill 0
}

(rtl_433 -M level -M time -C customary -F json -f 315M -d 0 | ./env/bin/python3 scripts/record_tpms.py samples1.db) &
(rtl_433 -M level -M time -C customary -F json -f 315M -d 1 | ./env/bin/python3 scripts/record_tpms.py samples2.db) &
wait
sleep 0.5
echo "Done!"
