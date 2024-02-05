import socket
import sys

def receive_command(sock, expected_command):
    response = b''
    while not response.endswith(b'\r\n'):
        data = sock.recv(1)
        if not data:
            raise ConnectionError("Server closed the connection")
        response += data
    if response != expected_command:
        raise ValueError(f"Unexpected response from server: {response}")

def send_confirmation(sock, confirmation_message):
    sock.sendall(confirmation_message)

def send_file(sock, filename):
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(10000)
            if not chunk:
                break
            sock.sendall(chunk)

def main(hostname, port, filename):
    if len(sys.argv) != 4:
        sys.stderr.write("ERROR: Usage: python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>\n")
        sys.exit(1)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((hostname, int(port)))

            receive_command(s, b'accio\r\n')
            send_confirmation(s, b'confirm-accio\r\n')
            receive_command(s, b'accio\r\n')
            send_confirmation(s, b'confirm-accio-again\r\n')

            send_file(s, filename)

    except socket.gaierror:
        sys.stderr.write("ERROR: Invalid hostname or unable to resolve hostname\n")
        sys.exit(1)
    except socket.timeout:
        sys.stderr.write("ERROR: Connection to the server timed out\n")
        sys.exit(1)
    except socket.error as e:
        sys.stderr.write(f"ERROR: Socket error: {e}\n")
        sys.exit(1)
    except ValueError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"ERROR: Unexpected error: {e}\n")
        sys.exit(1)
    else:
        print("File transfer completed successfully")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

