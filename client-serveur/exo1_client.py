import socket


def connect_to_server(host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    return client_socket


