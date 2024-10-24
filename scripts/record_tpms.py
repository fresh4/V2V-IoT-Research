import sqlite3 as sql
import json, obd
import utils
from utils import bcolors as c
# NOTE:
# This script operates by taking and parsing lines input into the script
# from the command line. This means you need to "pipe" the outputs into this script.
# It does not run the required command as a subprocess (though that might be a good idea).
# See the record_tpms.sh script under /bash_scripts/ for actual use of this script.

def process(data: str):
    # Parse piped data to json
    try:
        tpms_data = json.loads(data)
    except:
        print(c.FAIL, "Could not parse input as json, got: ", c.ENDC, data)
        return
    
    # Get vehicle speed from OBD sensor
    speed = get_speed()

    # Construct final data tuple and write to local database
    try:
        # TODO: If necessary, post-process data to get consistent key values.
        freq = tpms_data.get("freq") or tpms_data.get("freq1")
        output = (
                tpms_data["time"], 
                tpms_data["id"], 
                tpms_data["model"], 
                speed, 
                tpms_data["temperature_F"],
                tpms_data["pressure_PSI"], 
                tpms_data["noise"],
                freq
                )
    except:
        print(c.FAIL, "Received signal is not TPMS, got: ", c.ENDC, tpms_data)
        return
    
    write_tpms_to_sql(output)

    print(tpms_data, speed)

def get_speed() -> float:
    speed = obd_connection.query(obd.commands.SPEED)
    return speed.value.magnitude if speed.value else 0

def write_tpms_to_sql(data: tuple):
    cursor.execute('''
        INSERT INTO TPMSSamples
        (timestamp, id, model, speed, temperature, pressure, noise, frequency)
        VALUES (?,?,?,?,?,?,?,?)
    ''', data)
    sql_connection.commit()
    
if __name__ == "__main__":
    # DEFINE PERSISTENT SERVICE CONNECTIONS
    obd_connection = obd.OBD()
    sql_connection = sql.connect("samples.db")
    cursor = sql_connection.cursor()
    utils.create_tpms_table() # Creates sqlite db tables if they don't exist

    connected = obd_connection.is_connected()
    print(f"OBD Connected:{c.OKGREEN if connected else c.FAIL}", connected, c.ENDC)

    # READ DATA STREAM FROM PIPED INPUT, ie:
    # rtl_433 -f 315M -M level -M time -C customary -F json | python3 scripts/record_tpms.py
    try:
        while True:
            process(input())
    except KeyboardInterrupt:
        obd_connection.close()
        sql_connection.close()
        pass