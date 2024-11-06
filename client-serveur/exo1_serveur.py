import socket


def ouverture_port(port):
    server_socket = socket.socket()
    port = 8080
    server_socket.bind(('0.0.0.0', port))



def écoute():
    server_socket.listen(1)
    conn, address = server_socket.accept()
    message = conn.recv(1024).decode()
    conn.send(reply.encode())
    conn.close()
    server_socket.close()



server_socket = socket.socket()
port = 8080
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)
conn, address = server_socket.accept()
message = conn.recv(1024).decode()
conn.send(reply.encode())
conn.close()
server_socket.close()