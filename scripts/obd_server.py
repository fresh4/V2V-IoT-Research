import socket
import json
import obd

HOST = 'localhost'
PORT = 48484

def query_obd(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str(command).encode('utf-8'))
        data = s.recv(1024)
        response = json.loads(data.decode('utf-8'))
        return response

def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode('utf-8').strip()
            response: obd.OBDResponse = connection.query(obd.commands[command])
            if response.value is not None:
                conn.sendall(json.dumps({'data': response.value.magnitude}).encode('utf-8'))
            else:
                conn.sendall(json.dumps({'error': 'Invalid command or no response'}).encode('utf-8'))

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'OBD-II Server listening on {HOST}:{PORT}')
        while True:
            conn, addr = s.accept()
            print(f'Connected by {addr}')
            handle_client(conn)

if __name__ == '__main__':
    print("Starting OBD-II server")
    connection = obd.OBD()
    try:
        start_server()
    except KeyboardInterrupt:
        print("Closing OBD-II connection...")
        connection.close()
