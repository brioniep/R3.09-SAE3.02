import socket
import threading

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 12345))  # Adresse IP et port du serveur
        self.lock = threading.Lock()

    def envoie(self):
        while True:
            message = input("Entrez le message (ou 'q' pour quitter) : ")
            if message.lower() == 'q':
                self.client_socket.close()
                break
            with self.lock:
                self.client_socket.send(message.encode())

    def reception(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                with self.lock:
                    print(f"Réponse du serveur : {data}")
            except ConnectionAbortedError:
                break

if __name__ == "__main__":
    client = Client()

    t1 = threading.Thread(target=client.reception)
    t2 = threading.Thread(target=client.envoie)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


