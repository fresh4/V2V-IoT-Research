import sqlite3 as sql
import json, sys, obd
import utils
from utils import bcolors as c
from obd_server import query_obd

# NOTE:
# This script operates by taking and parsing lines input into the script
# from the command line. This means you need to "pipe" the outputs into this script.
# It does not run the required command as a subprocess (though that might be a good idea).
# See the record_tpms.sh script under /bash_scripts/ for actual use of this script.

def process(data: str):
    # Parse piped data to json
    try:
        tpms_data: dict = json.loads(data)
    except:
        print(c.FAIL, "Could not parse input as json, got: ", c.ENDC, data)
        return
    
    # Get vehicle speed from OBD sensor
    speed = get_speed()

    # Construct final data tuple and write to local database
    try:
        # FSK (Frequency Shift Key) will give multiple frequency codes
        if tpms_data["mod"] == "FSK":
            freq1 = tpms_data["freq1"]
            freq2 = tpms_data["freq2"]
        else:
            freq1 = tpms_data["freq"]
            freq2 = ""
        # freq = tpms_data.get("freq") or tpms_data.get("freq1")
        output = (
                tpms_data["time"], 
                tpms_data["id"], 
                tpms_data["model"], 
                speed, 
                tpms_data.get("temperature_F", 0),
                tpms_data["pressure_PSI"], 
                tpms_data["noise"],
                tpms_data["rssi"],
                tpms_data["snr"],
                freq1,
                freq2
                )
    except:
        print(c.FAIL, "Received signal is not TPMS, got: ", c.ENDC, tpms_data)
        return
    
    write_tpms_to_sql(output)

    print(tpms_data, speed)

def get_speed() -> float:
    if isinstance(obd_connection, obd.OBD):
        speed = obd_connection.query(obd.commands.SPEED)
        return speed.value.magnitude if speed.value else 0
    else:
        return query_obd("SPEED")['data']

def write_tpms_to_sql(data: tuple):
    cursor.execute('''
        INSERT INTO TPMSSamples
        (timestamp, id, model, speed, temperature, pressure, noise, RSSI, SNR, freq1, freq2)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    ''', data)
    sql_connection.commit()

def connect_obd() -> obd.OBD | bool:
    # Decide between a direct OBD connection or connecting to an OBD-II socket server
    query = query_obd("SPEED") # Attempts to get speed from running OBD server.
    if query and "data" in query:
        # Server is running and connection is made, use socket.
        return True
    else:
        # No server is running; try to connect directly via USB wire.
        return obd.OBD()

if __name__ == "__main__":
    args = sys.argv
    filename = args[1] if len(args) == 2 else "samples.db"
    # DEFINE PERSISTENT SERVICE CONNECTIONS
    obd_connection = connect_obd()
    sql_connection = sql.connect(filename)
    cursor = sql_connection.cursor()
    utils.create_tpms_table(filename) # Creates sqlite db tables if they don't exist

    connected = obd_connection.is_connected() if isinstance(obd_connection, obd.OBD) else obd_connection
    print(f"OBD Connected:{c.OKGREEN if connected else c.FAIL}", connected, c.ENDC)

    # READ DATA STREAM FROM PIPED INPUT, ie:
    # rtl_433 -f 315M -M level -M time -C customary -F json | python3 scripts/record_tpms.py
    try:
        while True:
            process(input())
    except KeyboardInterrupt:
        if isinstance(obd_connection, obd.OBD):
            obd_connection.close()
        sql_connection.close()