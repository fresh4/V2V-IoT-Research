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

echo "########## STARTING READERS ##########"
(rtl_433 -f 315M -w sdr1.cu8 -d 0) &
(rtl_433 -f 315M -w sdr2.cu8 -d 1) &
wait
