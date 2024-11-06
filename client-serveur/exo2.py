import socket



# CLIENT

message = "hello"
host = "127.1.1.1"
port = 8080

client_socket = socket.socket()
client_socket.connect((host, port))
client_socket.send(message.encode())
reply = client_socket.recv(1024).decode()
client_socket.close()




# SERVEUR
server_socket = socket.socket()
port = 8080
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)
conn, address = server_socket.accept()
message = conn.recv(1024).decode()
conn.send(reply.encode())
conn.close()
server_socket.close()