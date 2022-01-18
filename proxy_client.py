import socket
import sys


def create_tcp_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as err:
        print(
            f'Failed to create socket. Error: {err}')
        sys.exit(1)
    return s


def send_data(serversocket, payload):
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print('Send failed')
        sys.exit(1)


def main():
    try:
        PROXY_SERVER_HOST = 'localhost'
        PROXY_SERVER_PORT = 8000

        split_payload = [
            'GET / HTTP/1.0',
            'Host: google.com',
            '\r\n'
        ]

        payload = '\r\n'.join(split_payload)
        buffer_size = 1024

        server_socket = create_tcp_socket()

        server_socket.connect((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        print(f'Sending request to {PROXY_SERVER_HOST}:{PROXY_SERVER_PORT}')
        send_data(server_socket, payload)
        server_socket.shutdown(socket.SHUT_WR)

        received_data = b''
        while True:
            data = server_socket.recv(buffer_size)
            if not data:
                break
            received_data += data
        print(received_data)
    except Exception as e:
        print(e)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
