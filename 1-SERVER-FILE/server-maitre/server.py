import socket, threading, subprocess

class ServerMaitre:
    def __init__(self, host='0.0.0.0', port=1234, host_esclave='0.0.0.0', port_esclave=5555):
        self.host = host
        self.port = port
        self.host_esclave = host_esclave
        self.port_esclave = port_esclave
        self.clients = {}

    def start_srv_client(self):
        """
        Démarre le serveur maître, écoute les connexions des clients et gère leur traitement.
        """
        self.socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_serveur.bind((self.host, self.port))
        self.socket_serveur.listen(5)
        print("[+] Serveur démaré avec succès ! ...")
        print("[+] En attente de connexions des clients ...")

        try:
            while True:
                socket_client, adresse_client = self.socket_serveur.accept()
                print(f"[+] Connexion acceptée de {adresse_client}")
                threading.Thread(target=self.gestion_client, args=(socket_client, adresse_client)).start()
        except KeyboardInterrupt:
            print("[-] Arrêt du serveur...")
        finally:
            self.socket_serveur.close()
            print("[-] Socket serveur fermé.")



    def start_srv_esclave(self):
        self.socket_serveur_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_serveur_esclave.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_serveur_esclave.bind((self.host_esclave, self.port_esclave))
        self.socket_serveur_esclave.listen(5)
        print("[+] En attente de connexions d'un serveur esclave ...")

        try:
            while True:
                socket_esclave, adresse_esclave = self.socket_serveur_esclave.accept()
                print(f"[+] Connexion acceptée de l'esclave : {adresse_esclave}")

                threading.Thread(target=self.reception_srv_esclave, args=(adresse_esclave, socket_esclave)).start()

        except KeyboardInterrupt:
            print("[-] Arrêt du serveur esclave...")
        finally:
            self.socket_serveur_esclave.close()
            print("[-] Socket serveur esclave fermé.")

    def gestion_client(self, socket_client, adresse_client):
        id_client = threading.get_ident()
        self.clients[id_client] = socket_client  # Stockage du client
        print(f"[+] Client {adresse_client} connecté avec pour ID -> {id_client}.")

        # Récupérer les informations sur l'utilisation de la mémoire des serveurs esclaves
        sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1 = self.ram_conteneur()

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

                # Passer les informations de mémoire à la fonction choix_esclave
                self.choix_esclave(fichier_info, sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1)

        except Exception as e:
            print(f"[-] Erreur avec le client-{id_client}: {e}")
        finally:
            del self.clients[id_client]  # Supprimer le client après déconnexion
            socket_client.close()
            print(f"[-] Client {id_client} déconnecté.")






    def ram_conteneur(self):
        try:
            result = subprocess.run(['docker', 'stats', '--no-stream', '--format', '{{.Name}}\t{{.MemPerc}}'], stdout=subprocess.PIPE)
            containers_stats = result.stdout.decode('utf-8').strip().split('\n')
            
            mem_usage = {}
            for line in containers_stats:
                if '\t' not in line:
                    continue

                name, mem_perc = line.split('\t')

                if mem_perc == 'N/A':
                    mem_usage[name] = 0.0
                else:
                    try:
                        mem_usage[name] = float(mem_perc.rstrip('%'))
                    except ValueError:
                        print(f"[-] Impossible de convertir la mémoire pour {name} : {mem_perc}")
                        mem_usage[name] = 0.0

            sae_server_esclave1_1 = mem_usage.get('server-file_server-esclave1_1', 0.0)
            sae_server_esclave2_1 = mem_usage.get('server-file_server-esclave2_1', 0.0)
            sae_server_esclave3_1 = mem_usage.get('server-file_server-esclave3_1', 0.0)
            sae_server_esclave4_1 = mem_usage.get('server-file_server-esclave4_1', 0.0)

            return sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0, 0.0, 0.0, 0.0





    def choix_esclave(self, fichier_info, sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1):
        extention = fichier_info[1].split('.')[-1]

        # Actualiser les informations de mémoire des serveurs esclaves
        sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1 = self.ram_conteneur()



        print(f"\033[94mConteneur esclave 1: {sae_server_esclave1_1} % de mémoire utilisée\033[0m")
        print(f"\033[94mConteneur esclave 2: {sae_server_esclave2_1} % de mémoire utilisée\033[0m")
        print(f"\033[94mConteneur esclave 3: {sae_server_esclave3_1} % de mémoire utilisée\033[0m")
        print(f"\033[94mConteneur esclave 4: {sae_server_esclave4_1} % de mémoire utilisée\033[0m")

        # Si l'extension est py, on envoie au premier serveur disponible en respectant les priorités
        if extention == "py":
            if float(sae_server_esclave1_1) <= 50:
                self.envoie_server1(fichier_info)
            elif float(sae_server_esclave2_1) <= 50:
                self.envoie_server2(fichier_info)
            elif float(sae_server_esclave3_1) <= 50:
                self.envoie_server3(fichier_info)
            elif float(sae_server_esclave4_1) <= 50:
                self.envoie_server4(fichier_info)
            else:
                self.envoie_server1(fichier_info)

        # Si l'extension est java
        elif extention == "java":
            if float(sae_server_esclave2_1) <= 50:
                self.envoie_server2(fichier_info)
            elif float(sae_server_esclave3_1) <= 50:
                self.envoie_server3(fichier_info)
            elif float(sae_server_esclave4_1) <= 50:
                self.envoie_server4(fichier_info)
            elif float(sae_server_esclave1_1) <= 50:
                self.envoie_server1(fichier_info)
            else:
                self.envoie_server2(fichier_info)

        # Si l'extension est c
        elif extention == "c":
            if float(sae_server_esclave3_1) <= 50:
                self.envoie_server3(fichier_info)
            elif float(sae_server_esclave4_1) <= 50:
                self.envoie_server4(fichier_info)
            elif float(sae_server_esclave1_1) <= 50:
                self.envoie_server1(fichier_info)
            elif float(sae_server_esclave2_1) <= 50:
                self.envoie_server2(fichier_info)
            else:
                self.envoie_server3(fichier_info)

        # Si l'extension est cpp
        elif extention == "cpp":
            if float(sae_server_esclave4_1) <= 50:
                self.envoie_server4(fichier_info)
            elif float(sae_server_esclave1_1) <= 50:
                self.envoie_server1(fichier_info)
            elif float(sae_server_esclave2_1) <= 50:
                self.envoie_server2(fichier_info)
            elif float(sae_server_esclave3_1) <= 50:
                self.envoie_server3(fichier_info)
            else:
                self.envoie_server4(fichier_info)









    def envoie_server1(self, fichier_info):
        try:
            print("[+] Tentative de connexion au serveur esclave 1...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('172.18.0.2', 1111))
            print("[+] Connexion établie avec le serveur esclave 1.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 1: {e}")
            return

        try:
            # Convertir la liste en chaîne formatée
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[+] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 1: {e}")

    def envoie_server2(self, fichier_info):
        try:
            print("[+] Tentative de connexion au serveur esclave 2...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('172.18.0.3', 2222))
            print("[+] Connexion établie avec le serveur esclave 2.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 2: {e}")
            return

        try:
            # Convertir la liste en chaîne formatée
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[+] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 2: {e}")

    def envoie_server3(self, fichier_info):
        try:
            print("[+] Tentative de connexion au serveur esclave 3...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('172.18.0.4', 3333))
            print("[+] Connexion établie avec le serveur esclave 3.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 3: {e}")
            return

        try:
            # Convertir la liste en chaîne formatée
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[+] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 3: {e}")

    def envoie_server4(self, fichier_info):
        try:
            print("[+] Tentative de connexion au serveur esclave 4...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('172.18.0.5', 4444))
            print("[+] Connexion établie avec le serveur esclave 4.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 4: {e}")
            return

        try:
            # Convertir la liste en chaîne formatée
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[+] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 4: {e}")


    def reception_srv_esclave(self,address_esclave,socket_esclave):
        print(f"[+] serveur {address_esclave} connecté.")

        try:

            donnees = socket_esclave.recv(4096).decode('utf-8')
            if not donnees:
                print("[-] Aucune donnée reçue.")
                return
            
            fichier_info = donnees.split('|', 2)
            if len(fichier_info) != 3:
                print("[-] Données reçues incorrectes.")
                return
            
            id_client, nom_fichier, contenu_fichier = fichier_info
            print(f"[+] ID Client: {id_client}, Nom du fichier: {nom_fichier}")
            print(f"[+] Contenu du résultat du fichier:\n{contenu_fichier}")

        except Exception as e:
            print(f"[-] Erreur lors de la réception du fichier executé: {e}")

        
        self.envoie_client(fichier_info)

    def envoie_client(self, fichier_info):
        id_client = int(fichier_info[0])
        nom_fichier = fichier_info[1]
        contenu_fichier = fichier_info[2]
        print(f"[+] Envoie au client {id_client} le contenu du fichier et le nom du fichier")

        socket_client = self.clients.get(id_client)
        if not socket_client:
            print(f"[-] Client avec ID {id_client} non trouvé.")
            return

        try:
            donnees = f"{nom_fichier}|||{contenu_fichier}"
            socket_client.sendall(donnees.encode('utf-8'))
            print(f"[+] Contenu envoyé au client {id_client}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au client {id_client}: {e}")



if __name__ == "__main__":
    server = ServerMaitre()
    t1 = threading.Thread(target=server.start_srv_client)
    t2 = threading.Thread(target=server.start_srv_esclave)
    t1.start()
    t2.start()
