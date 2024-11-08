import socket

def client_program():
    host = '127.0.0.1'  # Adresse IP du serveur
    port = 12345  # Port du serveur

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Entrez le message : ")

        if message.lower() == 'arret':
            client_socket.send(message.encode())
            break
        if message.lower() == 'exit':
            client_socket.send(message.encode())
            break

        client_socket.send(message.encode())

        data = client_socket.recv(1024).decode()  # Recevoir la réponse du serveur
        print(f"Réponse du serveur : {data}")

    client_socket.close()  # Fermer la connexion

if __name__ == "__main__":
    client_program()
