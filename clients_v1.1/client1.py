import socket
import os
import time

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connexion(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print("Connexion impossible:", e)

    def envoie(self):
        while True:
            message = input("Entrez le message : ")

            if message.lower() == 'arret':
                self.client_socket.send(message.encode())
                break
            if message.lower() == 'bye':
                self.client_socket.send(message.encode())
                break

            if message.lower() == 'fichier':
                chemin = input("Entrez le chemin du fichier : ")
                try:
                    filename = os.path.basename(chemin)
                    self.client_socket.send(filename.encode())
                    time.sleep(0.1)

                    filesize = os.path.getsize(chemin)
                    self.client_socket.send(str(filesize).encode())
                    time.sleep(0.1)

                    with open(chemin, 'rb') as f:
                        data = f.read(1024)
                        while data:
                            self.client_socket.send(data)
                            data = f.read(1024)
                    print("Fichier envoyé")

                    # Recevoir l'en-tête indiquant le type de réponse
                    response_type = self.client_socket.recv(1024).decode()

                    if response_type == "error" or response_type == "output":
                        # Recevoir et afficher les données textuelles
                        response = self.client_socket.recv(4096).decode()
                        print("Réponse du serveur :", response)
                    elif response_type == "file":
                        # Recevoir un fichier binaire
                        with open("output_from_server", 'wb') as f:
                            while True:
                                data = self.client_socket.recv(1024)
                                if not data:
                                    break
                                f.write(data)
                        print("Fichier compilé reçu et sauvegardé sous 'output_from_server'")

                except FileNotFoundError:
                    print("Fichier introuvable")
                    break
                except Exception as e:
                    print("Erreur lors de l'envoi du fichier :", e)
                    break

            else:
                self.client_socket.send(message.encode())

        self.client_socket.close()























if __name__ == "__main__":
    client_1 = Client('127.0.0.1', 12345)
    client_1.connexion()
    client_1.envoie()
