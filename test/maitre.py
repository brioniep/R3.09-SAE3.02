import socket
import threading









import socket
import os
import threading

class ServerMaitre:
    def __init__(self, host='0.0.0.0', port=1234, host_esclave='0.0.0.0', port_esclave=5555):
        self.host = host
        self.port = port
        self.host_esclave = host_esclave
        self.port_esclave = port_esclave
        
        # Initialisation des clients connectés
        self.clients = {}


    def start_srv_client(self):
        """
        Démarre le serveur maître, écoute les connexions des clients et gère leur traitement.
        """
        self.socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_serveur.bind((self.host, self.port))
        self.socket_serveur.listen(5)
        print("[SERVEUR] En attente de connexions...")

        try:
            while True:
                socket_client, adresse_client = self.socket_serveur.accept()
                print(f"[+] Connexion acceptée de {adresse_client}")
                threading.Thread(target=self.gestion_client, args=(socket_client, adresse_client)).start()
        except KeyboardInterrupt:
            print("Arrêt du serveur...")
        finally:
            self.socket_serveur.close()
            print("Socket serveur fermé.")



    def start_srv_esclave(self):
        self.socket_serveur_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_serveur_esclave.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_serveur_esclave.bind((self.host_esclave, self.port_esclave))
        self.socket_serveur_esclave.listen(5)
        print("[SERVEUR] En attente de connexions d'un esclave ...")

        try:
            while True:
                socket_esclave, adresse_esclave = self.socket_serveur_esclave.accept()
                print(f"[+] Connexion acceptée de l'esclave : {adresse_esclave}")

                threading.Thread(target=self.reception_srv_esclave, args=(adresse_esclave, socket_esclave)).start()

        except KeyboardInterrupt:
            print("Arrêt du serveur esclave...")
        finally:
            self.socket_serveur_esclave.close()
            print("Socket serveur esclave fermé.")












    def gestion_client(self, socket_client, adresse_client):
        id_client = threading.get_ident()
        self.clients[id_client] = socket_client  # Stockage du client
        print(f"[+] Client {adresse_client} connecté avec ID {id_client}.")

        try:
            while True:
                nom_fichier = socket_client.recv(1024).decode('utf-8').strip()
                if not nom_fichier:
                    break

                contenu_fichier = b""
                while True:
                    donnees = socket_client.recv(1024)
                    if not donnees:
                        break
                    contenu_fichier += donnees
                    if b"\x00" in donnees:
                        break

                if contenu_fichier.endswith(b'\x00'):
                    contenu_fichier = contenu_fichier[:-1]

                contenu_fichier_str = contenu_fichier.decode('utf-8', errors='replace')

                fichier_info = [id_client, nom_fichier, contenu_fichier_str]
                print(f"[Client-{id_client}] Liste créée : {fichier_info}")
                self.envoie_server1(fichier_info)

        except Exception as e:
            print(f"[-] Erreur avec le client-{id_client}: {e}")
        finally:
            del self.clients[id_client]  # Supprimer le client après déconnexion
            socket_client.close()
            print(f"[-] Client {id_client} déconnecté.")







    def envoie_server1(self, fichier_info):
        try:
            print("[SERVEUR] Tentative de connexion au serveur esclave 1...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('localhost', 1111))
            print("[SERVEUR] Connexion établie avec le serveur esclave 1.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 1: {e}")
            return

        try:
            # Convertir la liste en chaîne formatée
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[SERVEUR] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 1: {e}")







    def reception_srv_esclave(self,address_esclave,socket_esclave):
        print(f"[+] SRV {address_esclave} connecté.")

        try:

            donnees = socket_esclave.recv(4096).decode('utf-8')
            if not donnees:
                print("Aucune donnée reçue.")
                return
            
            fichier_info = donnees.split('|', 2)
            if len(fichier_info) != 3:
                print("Données reçues incorrectes.")
                return
            
            id_client, nom_fichier, contenu_fichier = fichier_info
            print(f"[RECEPTION] ID Client: {id_client}, Nom du fichier: {nom_fichier}")
            print(f"[RECEPTION] Contenu du résultat du fichier:\n{contenu_fichier}")

        except Exception as e:
            print(f"[-] Erreur lors de la réception du fichier executé: {e}")

        
        self.envoie_client(fichier_info)







    def envoie_client(self, fichier_info):
        id_client = int(fichier_info[0])
        contenu_fichier = fichier_info[2]
        print(f"Envoie au client {id_client} le contenu du fichier")

        # Trouver le socket du client correspondant à l'id_client
        socket_client = self.clients.get(id_client)
        if not socket_client:
            print(f"[-] Client avec ID {id_client} non trouvé.")
            return

        try:
            socket_client.sendall(contenu_fichier.encode('utf-8'))
            print(f"[SERVEUR] Contenu envoyé au client {id_client}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au client {id_client}: {e}")






if __name__ == "__main__":
    server = ServerMaitre()
    t1 = threading.Thread(target=server.start_srv_client)
    t2 = threading.Thread(target=server.start_srv_esclave)
    t1.start()
    t2.start()
