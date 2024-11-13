import threading
import socket

class Serveur:

    def __init__(self, port=12345, server_socket=None):
        if server_socket is None:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.server_socket = server_socket
        self.client_socket = None

    def ouverture_connexion(self):
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)
        print(f"Serveur ouvert sur le port {self.port}...")

    def reception(self):
        while True:
            self.client_socket, address = self.server_socket.accept()
            print(f"Client connecté ")
            
            while True:
                message = self.client_socket.recv(1024).decode()

                if not message:
                    break

                print(f"Message reçu : {message}")

                if message.lower() == "bye":
                    print("Le client s'est déconnecté...")
                    break

                if message.lower() == "arret":
                    print("Fermeture du serveur...")
                    self.client_socket.close()
                    self.server_socket.close()
                    return

    def envoie(self):
        while True:
            message = input("Entrez le message : ")
            if message.lower() == "arret":
                self.client_socket.send(message.encode())
                self.client_socket.close()
                break
            if self.client_socket:
                self.client_socket.send(message.encode())

if __name__ == "__main__":
    serveur1 = Serveur()
    serveur1.ouverture_connexion()

    thread_reception = threading.Thread(target=serveur1.reception)
    thread_envoie = threading.Thread(target=serveur1.envoie)

    thread_reception.start()
    thread_envoie.start()

    thread_reception.join()
    thread_envoie.join()
