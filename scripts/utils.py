import sqlite3

def create_tpms_table():
    conn = sqlite3.connect('samples.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS TPMSSamples
                    (
                        timestamp DATETIME, 
                        id TEXT, 
                        model TEXT, 
                        speed REAL, 
                        temperature REAL, 
                        pressure REAL, 
                        noise REAL, 
                        frequency REAL
                    )''')
    conn.commit()
    conn.close()

def find_value(search_list: list, data: dict) -> any:
    for item in search_list:
        if item in data:
            return data[item]
    return None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
