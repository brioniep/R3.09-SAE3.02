import socket
import time
import threading

class Client:

    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connexion(self):
        while True:
            try:
                self.client_socket.connect((self.host, self.port))
                print("Connexion réussie")
                break
            except:
                print(f"Erreur de connexion, nouvel essai dans 3 secondes")
                time.sleep(3)

    def reception(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()  # Recevoir la réponse du serveur
                if not data:  # Si la connexion est fermée
                    break
                print(f"Réponse du serveur : {data}")
            except:
                print("Erreur lors de la réception des messages")
                break

    def envoi(self):
        while True:
            message = input("Entrez le message : ")

            if message.lower() == 'arret':
                self.client_socket.send(message.encode())
                break
            if message.lower() == 'bye':
                self.client_socket.send(message.encode())
                break

            self.client_socket.send(message.encode())

        self.client_socket.close()  # Fermer la connexion

if __name__ == "__main__":
    client1 = Client()
    client1.connexion()

    t1 = threading.Thread(target=client1.reception)
    t2 = threading.Thread(target=client1.envoi)

    t1.start()
    t2.start()

    # Attendre que les threads se terminent
    t1.join()
    t2.join()
