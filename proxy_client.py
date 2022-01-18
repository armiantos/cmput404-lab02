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
        proxy_server_host = 'localhost'
        proxy_server_port = 8000

        target_host = 'google.com'

        payload = f'GET / HTTP/1.0\r\nHost: {target_host}\r\n\r\n'
        buffer_size = 4096

        server_socket = create_tcp_socket()

        server_socket.connect((proxy_server_host, proxy_server_port))
        print(f'Socket Connected to {proxy_server_host}:{proxy_server_port}')

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
