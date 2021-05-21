import datetime
import socket
import sqlite3
import threading


def threaded(client_data):
    while True:

        last_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
        data = str(client_data.recv(1024).decode('utf-8'))
        if not data:
            break
        list_of_data = data.split('*')
        list_of_data.append(last_date)
        Create_DB(list_of_data)
        client_data.send(b"Alive")
    client_data.close()


def data_Server():
    host = '127.0.0.1'
    port = 2345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            print("Server In Process...")
            print('**kone**' * 10)
            s.listen(5)
        except Exception as e:
            raise SystemExit(f"ERROR: could not bind the server on host :${host} to port: ${port}, because: {e}")

        while True:
            try:
                c, addr = s.accept()
                t = threading.Thread(target=threaded, args=(c,))
                t.daemon = True
                t.start()
            except KeyboardInterrupt:
                print("The process is completed.")
                s.close()
                break


def Create_DB(list_of_data):
    print("The server is listening in every60 Seconds..\n"
          "", end='', flush=True)
    conn = sqlite3.connect(r'C:\Desktop\pythonProject1\pythonfinalproject_kone_2021\data.db')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS station_status
    (station_id INT,
    alarm1 INT,
    alarm2 INT,
    last_date TEXT,
    PRIMARY KEY(station_id))
    ''')

    conn.execute(""" INSERT OR REPLACE INTO station_status(station_id,alarm1,alarm2,last_date)

    VALUES(?,?,?,?)""", (list_of_data[0], list_of_data[1], list_of_data[2], str(list_of_data[3])))

    conn.commit()
    conn.close()


def main():
    data_Server()


main()
