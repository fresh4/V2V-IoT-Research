import subprocess
import sqlite3 as sql
import sys, json, obd
import utils

def process(data: str):
    # Parse piped data to json
    try:
        tpms_data = json.loads(data)
    except:
        print("Could not parse input as json")
        return
    
    # Get vehicle speed from OBD sensor
    speed = get_speed()

    # Construct final data tuple and write to local database
    output = (
            tpms_data["time"], 
            tpms_data["id"], 
            tpms_data["model"], 
            speed, 
            tpms_data["temperature_F"], 
            tpms_data["pressure_PSI"], 
            tpms_data["noise"]
            )
    write_tpms_to_sql(output)

    print(tpms_data)

def get_speed() -> float:
    speed = obd_connection.query(obd.commands.SPEED)
    return speed.value.magnitude if speed.value else 0

def write_tpms_to_sql(data: tuple):
    cursor.execute('''
        INSERT INTO TPMSSamples
        (timestamp, id, model, speed, temperature, pressure, noise)
        VALUES (?,?,?,?,?,?,?)
    ''', data)
    sql_connection.commit()
    
if __name__ == "__main__":
    # DEFINE PERSISTENT SERVICE CONNECTIONS
    obd_connection = obd.OBD()
    sql_connection = sql.connect("samples.db")
    cursor = sql_connection.cursor()
    utils.create_tpms_table() # Creates sqlite db tables if they don't exist

    # READ DATA STREAM FROM PIPED INPUT
    # rtl_433 -f 315M -M level -M time -C customary -F json | python3 scripts/record_tpms.py
    try:
        while True:
            process(input())
    except KeyboardInterrupt:
        obd_connection.close()
        sql_connection.close()
        pass