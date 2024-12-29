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
        
        Variables :
            socket_serveur (socket.socket) : Le socket utilisé pour accepter les connexions des clients.
            host (str) : L'adresse IP ou le nom d'hôte sur lequel le serveur maître écoute.
            port (int) : Le port sur lequel le serveur maître écoute les connexions entrantes.
            socket_client (socket.socket) : Le socket de communication utilisé pour échanger des données avec un client.
            adresse_client (tuple) : L'adresse IP et le port du client qui se connecte au serveur maître.
        
        Méthodes appelées :
            socket.socket() : Crée un objet socket pour la communication réseau.
            setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) : Configure le socket pour réutiliser l'adresse en cas de redémarrage du serveur.
            bind() : Lie le socket à une adresse et un port donnés pour commencer à écouter.
            listen(5) : Configure le socket pour accepter jusqu'à 5 connexions simultanées.
            accept() : Attends une connexion entrante et retourne un nouveau socket pour la communication avec le client.
            threading.Thread() : Crée un thread pour gérer chaque client sans bloquer l'exécution du serveur principal.
            gestion_client() : Méthode appelée dans un thread pour gérer la communication avec un client.
            close() : Ferme le socket du serveur à la fin de l'exécution ou en cas d'erreur.
        """
        
        self.socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_serveur.bind((self.host, self.port))
        self.socket_serveur.listen(5)
        print("[+] Serveur démarré avec succès ! ...")
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
        """
        Démarre le serveur esclave, écoute les connexions des serveurs maîtres et gère leur traitement.
        
        Variables :
            socket_serveur_esclave (socket.socket) : Le socket utilisé pour accepter les connexions des serveurs maîtres.
            host_esclave (str) : L'adresse IP ou le nom d'hôte sur lequel le serveur esclave écoute.
            port_esclave (int) : Le port sur lequel le serveur esclave écoute les connexions entrantes.
            socket_esclave (socket.socket) : Le socket de communication utilisé pour échanger des données avec un serveur maître.
            adresse_esclave (tuple) : L'adresse IP et le port du serveur maître qui se connecte au serveur esclave.
        
        Méthodes appelées :
            socket.socket() : Crée un objet socket pour la communication réseau.
            setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) : Configure le socket pour réutiliser l'adresse en cas de redémarrage du serveur.
            bind() : Lie le socket à une adresse et un port donnés pour commencer à écouter.
            listen(5) : Configure le socket pour accepter jusqu'à 5 connexions simultanées.
            accept() : Attends une connexion entrante et retourne un nouveau socket pour la communication avec le serveur maître.
            threading.Thread() : Crée un thread pour gérer chaque connexion sans bloquer l'exécution du serveur principal.
            reception_srv_esclave() : Méthode appelée dans un thread pour gérer la réception des données du serveur maître.
            close() : Ferme le socket du serveur à la fin de l'exécution ou en cas d'erreur.
        """
        
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
        """
        Gère la connexion d'un client, réceptionne les fichiers envoyés par ce client, et les passe à un serveur esclave approprié.
        
        Variables :
            socket_client (socket.socket) : Le socket de communication utilisé pour échanger des données avec le client.
            adresse_client (tuple) : L'adresse IP et le port du client qui se connecte au serveur maître.
            id_client (int) : L'identifiant unique du client, généré par le thread pour chaque connexion.
            clients (dict) : Dictionnaire contenant les clients connectés, indexés par leur identifiant de thread.
            sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1 (str) : Informations sur l'utilisation de la mémoire des serveurs esclaves, récupérées via `ram_conteneur()`.
            contenu_fichier (bytes) : Les données du fichier envoyé par le client, en format binaire.
            contenu_fichier_str (str) : Les données du fichier converties en chaîne de caractères.
            fichier_info (list) : Liste contenant l'ID du client, le nom du fichier et le contenu du fichier.

        Méthodes appelées :
            threading.get_ident() : Retourne l'identifiant du thread courant, utilisé pour identifier de manière unique chaque client.
            ram_conteneur() : Récupère les informations sur l'utilisation de la mémoire des serveurs esclaves.
            socket.recv() : Reçoit des données envoyées par le client via le socket.
            choix_esclave() : Choisit un serveur esclave pour traiter le fichier envoyé par le client en fonction des informations de mémoire.
            socket_client.close() : Ferme la connexion avec le client après le traitement.
        """
        
        id_client = threading.get_ident()
        self.clients[id_client] = socket_client 
        print(f"[+] Client {adresse_client} connecté avec pour ID -> {id_client}.")

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

                self.choix_esclave(fichier_info, sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1)

        except Exception as e:
            print(f"[-] Erreur avec le client-{id_client}: {e}")
        finally:
            del self.clients[id_client]  
            socket_client.close()
            print(f"[-] Client {id_client} déconnecté.")



    def ram_conteneur(self):
        """
        Récupère l'utilisation de la mémoire des conteneurs Docker en cours d'exécution, puis renvoie les informations spécifiques
        pour quatre serveurs esclaves.

        Variables :
            result (subprocess.CompletedProcess) : L'objet retourné par `subprocess.run()` contenant le résultat de la commande Docker.
            containers_stats (list) : Liste des statistiques des conteneurs récupérées après avoir exécuté la commande Docker.
            mem_usage (dict) : Dictionnaire contenant les pourcentages d'utilisation de la mémoire pour chaque conteneur.
            sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1 (float) : Les pourcentages d'utilisation de la mémoire pour les quatre serveurs esclaves.

        Méthodes appelées :
            subprocess.run() : Exécute la commande Docker pour récupérer les statistiques des conteneurs.
            stdout.decode() : Décodage des données binaires renvoyées par `subprocess.run()` en chaîne de caractères.
            str.split() : Sépare les informations des conteneurs en lignes et en colonnes.
            str.split('\t') : Sépare chaque ligne en nom de conteneur et pourcentage de mémoire.
            float() : Convertit le pourcentage de mémoire en valeur numérique.
            mem_usage.get() : Récupère l'utilisation de la mémoire pour des conteneurs spécifiques par leur nom.

        """
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
        """
        Choisit un serveur esclave approprié pour traiter le fichier en fonction de son extension et de l'utilisation de la mémoire des serveurs esclaves.

        Variables :
            extention (str) : L'extension du fichier reçu, utilisée pour déterminer le serveur esclave à choisir.
            sae_server_esclave1_1, sae_server_esclave2_1, sae_server_esclave3_1, sae_server_esclave4_1 (float) : L'utilisation de la mémoire (en pourcentage) pour chaque serveur esclave.
            fichier_info (list) : Liste contenant des informations sur le fichier à traiter, comprenant l'ID du client, le nom du fichier et son contenu.
        
        Méthodes appelées :
            ram_conteneur() : Récupère l'utilisation de la mémoire des serveurs esclaves en cours d'exécution.
            envoie_server1(), envoie_server2(), envoie_server3(), envoie_server4() : Envoie le fichier au serveur esclave approprié en fonction de l'extension du fichier et de l'utilisation de la mémoire.

        """
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
        """
        Envoie les informations du fichier au serveur esclave 1 après une connexion réussie.

        Variables :
            fichier_info (list) : Liste contenant des informations sur le fichier à envoyer au serveur esclave.
                - fichier_info[0] : ID du client.
                - fichier_info[1] : Nom du fichier.
                - fichier_info[2] : Contenu du fichier.

        Méthodes appelées :
            socket.socket() : Crée un nouveau socket pour la communication avec le serveur esclave.
            socket.connect() : Établit la connexion avec le serveur esclave 1 à l'adresse IP et au port spécifiés.
            socket.sendall() : Envoie les données au serveur esclave en utilisant une connexion socket.
            encode('utf-8') : Encode les données à envoyer dans le format UTF-8.
        """
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
        """
        Envoie les informations du fichier au serveur esclave 2 après une connexion réussie.

        Variables :
            fichier_info (list) : Liste contenant des informations sur le fichier à envoyer au serveur esclave.
                - fichier_info[0] : ID du client.
                - fichier_info[1] : Nom du fichier.
                - fichier_info[2] : Contenu du fichier.

        Méthodes appelées :
            socket.socket() : Crée un nouveau socket pour la communication avec le serveur esclave.
            socket.connect() : Établit la connexion avec le serveur esclave 2 à l'adresse IP et au port spécifiés.
            socket.sendall() : Envoie les données au serveur esclave en utilisant une connexion socket.
            encode('utf-8') : Encode les données à envoyer dans le format UTF-8.
        """
        try:
            print("[+] Tentative de connexion au serveur esclave 2...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('172.18.0.3', 2222))
            print("[+] Connexion établie avec le serveur esclave 2.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 2: {e}")
            return

        try:
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[+] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 2: {e}")


    def envoie_server3(self, fichier_info):
        """
        Envoie les informations du fichier au serveur esclave 3 après une connexion réussie.

        Variables :
            fichier_info (list) : Liste contenant des informations sur le fichier à envoyer au serveur esclave.
                - fichier_info[0] : ID du client.
                - fichier_info[1] : Nom du fichier.
                - fichier_info[2] : Contenu du fichier.

        Méthodes appelées :
            socket.socket() : Crée un nouveau socket pour la communication avec le serveur esclave.
            socket.connect() : Établit la connexion avec le serveur esclave 3 à l'adresse IP et au port spécifiés.
            socket.sendall() : Envoie les données au serveur esclave en utilisant une connexion socket.
            encode('utf-8') : Encode les données à envoyer dans le format UTF-8.
        """
        try:
            print("[+] Tentative de connexion au serveur esclave 3...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('172.18.0.4', 3333))
            print("[+] Connexion établie avec le serveur esclave 3.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 3: {e}")
            return

        try:
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[+] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 3: {e}")


    def envoie_server4(self, fichier_info):
        """
        Envoie les informations du fichier au serveur esclave 4 après une connexion réussie.

        Variables :
            fichier_info (list) : Liste contenant des informations sur le fichier à envoyer au serveur esclave.
                - fichier_info[0] : ID du client.
                - fichier_info[1] : Nom du fichier.
                - fichier_info[2] : Contenu du fichier.

        Méthodes appelées :
            socket.socket() : Crée un nouveau socket pour la communication avec le serveur esclave.
            socket.connect() : Établit la connexion avec le serveur esclave 4 à l'adresse IP et au port spécifiés.
            socket.sendall() : Envoie les données au serveur esclave en utilisant une connexion socket.
            encode('utf-8') : Encode les données à envoyer dans le format UTF-8.
        """
        try:
            print("[+] Tentative de connexion au serveur esclave 4...")
            socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_esclave.connect(('172.18.0.5', 4444))
            print("[+] Connexion établie avec le serveur esclave 4.")
        except Exception as e:
            print(f"[-] Erreur de connexion au serveur esclave 4: {e}")
            return

        try:
            donnees = f"{fichier_info[0]}|{fichier_info[1]}|{fichier_info[2]}"
            socket_esclave.sendall(donnees.encode('utf-8'))
            print(f"[+] Liste fichier_info envoyée : {fichier_info}")
        except Exception as e:
            print(f"[-] Erreur lors de l'envoi au serveur esclave 4: {e}")



    def reception_srv_esclave(self, address_esclave, socket_esclave):
        """
        Gère la réception des données envoyées par un serveur esclave et transmet les informations au client.

        Variables :
            address_esclave (tuple) : L'adresse IP et le port du serveur esclave qui envoie les données.
            socket_esclave (socket.socket) : Le socket utilisé pour recevoir les données du serveur esclave.

        Méthodes appelées :
            socket.recv() : Reçoit les données envoyées par le serveur esclave via le socket.
            decode('utf-8') : Décode les données reçues en chaîne de caractères au format UTF-8.
            split() : Sépare les données reçues en une liste en utilisant le séparateur '|' pour extraire les informations.
            envoie_client() : Envoie les informations du fichier au client.
        """
        print(f"[+] Serveur {address_esclave} connecté.")

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
            print(f"[-] Erreur lors de la réception du fichier exécuté: {e}")

        self.envoie_client(fichier_info)


    def envoie_client(self, fichier_info):
        """
        Envoie les informations du fichier (nom et contenu) au client spécifié par l'ID.

        Variables :
            fichier_info (list) : Liste contenant les informations du fichier à envoyer au client.
                - fichier_info[0] : ID du client (int).
                - fichier_info[1] : Nom du fichier (str).
                - fichier_info[2] : Contenu du fichier (str).

        Méthodes appelées :
            int() : Convertit l'ID client en entier.
            self.clients.get() : Récupère le socket du client à partir du dictionnaire `clients` en utilisant l'ID du client.
            socket.sendall() : Envoie les données au client via le socket.
            encode('utf-8') : Encode les données à envoyer dans le format UTF-8.
        """
        id_client = int(fichier_info[0])
        nom_fichier = fichier_info[1]
        contenu_fichier = fichier_info[2]
        print(f"[+] Envoie au client {id_client} le contenu du fichier et le nom du fichier")

        socket_client = self.clients.get(id_client)
        if not socket_client:
            print(f"[-] Client avec ID {id_client} non trouvé.")
            return

        try:
            # Utiliser un délimiteur unique comme "|||"
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
