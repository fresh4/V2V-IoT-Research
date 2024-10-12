import sqlite3

def create_tpms_table():
    conn = sqlite3.connect('samples.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS TPMSSamples
                    (timestamp DATETIME, id TEXT, model TEXT, speed REAL, temperature REAL, pressure REAL, noise REAL)''')
    conn.commit()
    conn.close()