import socket
import sys

def receive_command(sock, expected_command):
    response = b''
    while not response.endswith(b'\r\n'):
        try:
            data = sock.recv(1)
            if not data:
                raise ConnectionError("Server closed the connection")
            response += data
        except socket.timeout:
            raise TimeoutError("Timeout while waiting for server command")
    if response != expected_command:
        raise ValueError(f"Unexpected response from server: {response}")
    return response

def send_confirmation(sock, confirmation_message):
    sock.sendall(confirmation_message + b'\r\n')

def send_file(sock, filename):
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(10000)
            if not chunk:
                break
            try:
                sock.sendall(chunk)
            except socket.timeout:
                raise TimeoutError("Timeout while sending file data")

def main(hostname, port, filename):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((hostname, int(port)))

            # Receive and confirm two 'accio\r\n' commands from the server
            for _ in range(2):
                receive_command(s, b'accio\r\n')
                send_confirmation(s, b'confirm-accio')

            # File Transfer
            send_file(s, filename)

    except ValueError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)
    except (socket.gaierror, ConnectionError, TimeoutError) as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"ERROR: Unexpected error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write("ERROR: Incorrect usage. Expected format: python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>\n")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
