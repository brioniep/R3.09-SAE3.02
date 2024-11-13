import threading
import socket

def ouverture(port, reply):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)  # Permettre jusqu'à 5 connexions en attente
    print(f"Serveur en écoute sur le port {port}...")

    while True:
        conn, address = server_socket.accept()
        print(f"Client connecté")

        while True:
            message = conn.recv(1024).decode()

            if not message:
                break

            print(f"Message reçu : {message}")
            conn.send(reply.encode())
            print("Réponse envoyée")

            if message.lower() == "arret":
                print("Fermeture du serveur...")
                conn.close()
                server_socket.close()
                return
            if message == "bye":
                print("Le client a été déconnecté")
                break


if __name__ == "__main__":
    port = 12345 
    reply = "Message reçu"  # Réponse du serveur
    thread = threading.Thread(target=ouverture, args=(port, reply))
    thread.start()
    thread.join()