import socket
import sys
import os

def receive_command(sock, expected_command):
    data_received = b''
    while not data_received.endswith(expected_command):
        data = sock.recv(1)
        if not data:
            raise Exception("Connection closed by the server")
        data_received += data
    return data_received

def send_confirmation(sock, message):
    sock.sendall(message)

def send_file(sock, filename):
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(10000)
            if not chunk:
                break
            sock.sendall(chunk)

def main(hostname, port, filename):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((hostname, int(port)))

            receive_command(s, b'accio\r\n')
            send_confirmation(s, b'confirm-accio\r\n')
            receive_command(s, b'accio\r\n')
            send_confirmation(s, b'confirm-accio-again\r\n\r\n')

            send_file(s, filename)

    except socket.gaierror:
        sys.stderr.write("ERROR: Invalid hostname or unable to resolve hostname\n")
        sys.exit(1)
    except socket.error as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"ERROR: Unexpected error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write("ERROR: Usage: python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>\n")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
