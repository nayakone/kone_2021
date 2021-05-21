
import socket
import time

TimeToWait= 10 # Time to sleep it can be set to any number for testing (1,2 etc)


def data_Of_Client():
    flag = b'Alive'
    host = '127.0.0.1'
    port = 2345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except Exception as e:
            raise SystemExit(f"ERROR: Failed to connect: {host} on port: {port}, because: {e}")
        while flag == b'Alive':
            try:
                s.sendall(read_status().encode('utf-8'))
                flag = s.recv(1024)
                time.sleep(TimeToWait)
                print('Received', repr(flag))
            except KeyboardInterrupt:
                print("finish", flush=True)
                s.close()

                break


def read_status():
    with open("status_3.txt", "r") as status:
        data = status.read()

    str_data = data.replace('\n', '*').strip('*')

    return str_data


def main():
    data_Of_Client()


main()
