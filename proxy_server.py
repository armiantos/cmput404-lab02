import socket
from multiprocessing import Process

from echo_server import BUFFER_SIZE

HOST = 'localhost'
PORT = 8000
BUFFER_SIZE = 1024


def get_google_response(client_request):
    google_host = 'www.google.com'
    google_port = 80
    google_ip = socket.gethostbyname(google_host)

    received_data = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as google_socket:
        google_socket.connect((google_ip, google_port))
        google_socket.sendall(client_request)
        while True:
            data = google_socket.recv(BUFFER_SIZE)
            if not data:
                break
            received_data += data
    return received_data


def handle_request(client_socket, client_addr):
    client_host, client_port = client_addr
    print(f'Received request from {client_host}:{client_port}')

    client_request = b''
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        client_request += data

    google_response = get_google_response(client_request)

    client_socket.sendall(google_response)
    client_socket.shutdown(socket.SHUT_WR)
    client_socket.close()
    print(f'Closed connection from {client_host}:{client_port}')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)

        print(f'Server listening at {HOST}:{PORT}')

        while True:
            client_socket, client_addr = server_socket.accept()
            p = Process(target=handle_request, args=(
                client_socket, client_addr,))
            p.daemon = True
            p.start()
            print(f'Started process ID {p.pid}')


if __name__ == "__main__":
    main()
