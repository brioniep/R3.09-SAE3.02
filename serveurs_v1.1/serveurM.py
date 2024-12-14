import os
import socket
import threading

class ServeurEsclave:

    def __init__(self, port=1111, hote_client='127.0.0.1'):
        self.port = port
        self.hote_client = hote_client
        self.socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def lancer_serveur_esclave(self):
        self.socket_esclave.bind(('0.0.0.0', self.port))
        self.socket_esclave.listen(5)
        print(f"Serveur esclave en écoute sur le port {self.port}...")

        while True:
            client_socket, client_address = self.socket_esclave.accept()
            print(f"Connexion acceptée de {client_address}")
            threading.Thread(target=self.gestion_fichier, args=(client_socket,)).start()

    def gestion_fichier(self, client_socket):
        try:
            while True:
                directory_attente = 'file-attente'
                directory_envoie = 'liste-envoie'
                parent_directory = os.path.dirname(os.getcwd())

                os.makedirs(directory_attente, exist_ok=True)
                os.makedirs(directory_envoie, exist_ok=True)

                filename = b""
                try:
                    while b"\n" not in filename:
                        part = client_socket.recv(1024)
                        if not part:
                            raise ConnectionError("Connexion interrompue par le client.")
                        filename += part
                    filename = filename.strip(b"\n").decode('utf-8')
                except socket.timeout:
                    print("Erreur : Temps d'attente dépassé lors de la réception du nom.")
                    break
                
                print(f"Nom du fichier reçu : {filename}")
                filepath_attente = os.path.join(directory_attente, filename)

                try:
                    with open(filepath_attente, 'wb') as f:
                        while True:
                            data = client_socket.recv(1024)
                            if data.endswith(b"END"):
                                f.write(data[:-3])
                                print("Fichier reçu correctement.")
                                break
                            elif not data:
                                raise ConnectionError("Connexion interrompue pendant la réception.")
                            f.write(data)
                except socket.timeout:
                    print("Erreur : Temps d'attente dépassé lors de la réception du fichier.")
                    break

                execution_directory = os.path.join(parent_directory, f"execution_{os.path.splitext(filename)[0]}")
                os.makedirs(execution_directory, exist_ok=True)

                filepath_execution = os.path.join(execution_directory, filename)
                os.rename(filepath_attente, filepath_execution)
                print(f"Fichier déplacé pour exécution dans : {filepath_execution}")

                extension = os.path.splitext(filename)[1]
                result_filepath = os.path.join(directory_envoie, f"{filename}_result.txt")

                try:
                    if extension == ".py":
                        command_execution = f"python3 {filepath_execution} 2>&1"

                    elif extension in [".c", ".cpp"]:
                        compiled_file = os.path.join(execution_directory, os.path.splitext(filename)[0])
                        compile_command = f"gcc {filepath_execution} -o {compiled_file} 2>&1" if extension == ".c" else f"g++ {filepath_execution} -o {compiled_file} 2>&1"
                        compilation_result = os.popen(compile_command).read()

                        if "error" in compilation_result.lower():
                            raise RuntimeError(f"Erreur de compilation :\n{compilation_result}")

                        command_execution = f"{compiled_file} 2>&1"

                    elif extension == ".java":
                        compile_command = f"javac {filepath_execution} 2>&1"
                        compilation_result = os.popen(compile_command).read()

                        if "error" in compilation_result.lower():
                            raise RuntimeError(f"Erreur de compilation :\n{compilation_result}")

                        class_name = os.path.splitext(filename)[0]
                        command_execution = f"java -cp {execution_directory} {class_name} 2>&1"

                    else:
                        raise ValueError("Erreur : Type de fichier non supporté.")

                    execution_result = os.popen(command_execution).read()

                    with open(result_filepath, 'w') as result_file:
                        result_file.write("=== Résultat de l'exécution ===\n")
                        result_file.write(execution_result)

                except Exception as e:
                    with open(result_filepath, 'w') as result_file:
                        result_file.write("=== Erreur rencontrée ===\n")
                        result_file.write(str(e) + "\n")

                print(f"Résultat enregistré dans : {result_filepath}")

                for root, dirs, files in os.walk(execution_directory, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(execution_directory)
                print(f"Dossier d'exécution supprimé : {execution_directory}")

                self.envoyer_resultat(client_socket, result_filepath)

        except (ConnectionError, BrokenPipeError):
            print("Le client s'est déconnecté.")
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            client_socket.close()

    def envoyer_resultat(self, client_socket, result_filepath):
        try:
            with open(result_filepath, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.sendall(data)

            client_socket.sendall(b"END")
            print(f"Résultat envoyé au client depuis : {result_filepath}")

        except FileNotFoundError:
            print(f"Erreur : Le fichier de résultat {result_filepath} est introuvable.")
            client_socket.sendall(f"Erreur : Le fichier de résultat {result_filepath} est introuvable.\nEND".encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du fichier : {e}")
            client_socket.sendall(f"Erreur lors de l'envoi du fichier : {e}\nEND".encode('utf-8'))

if __name__ == "__main__":
    serveur = ServeurEsclave()
    try:
        serveur.lancer_serveur_esclave()
    except KeyboardInterrupt:
        print("Arrêt du serveur...")
        serveur.socket_esclave.close()

























import subprocess
import time
import threading

def get_container_stats(container_name):
    """
    Exécute la commande docker stats pour un conteneur spécifique et récupère les stats en format texte.
    """
    command = ["docker", "stats", container_name, "--no-stream", "--format", "'{{.Name}}: {{.MemUsage}}'"]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de la commande pour {container_name}: {result.stderr}")
        print("Commande exécutée : ", " ".join(command))  # Afficher la commande pour vérifier
        return f"Erreur: Impossible d'obtenir les stats pour {container_name}"
    
    return result.stdout.strip()  

def monitor_container(container_name):
    """
    Surveille la consommation de la RAM d'un conteneur esclave spécifique.
    """
    while True:
        stats = get_container_stats(container_name)
        print(stats)
        time.sleep(10)

def monitor_containers():
    """
    Surveille la consommation de la RAM de tous les conteneurs esclaves en utilisant des threads.
    """
    slave_containers = [
        "sae-server-esclave1-1",
        "sae-server-esclave2-1",
        "sae-server-esclave3-1",
        "sae-server-esclave4-1"
    ]
    
    threads = []
    for container in slave_containers:
        thread = threading.Thread(target=monitor_container, args=(container,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    monitor_containers()






























import socket
import os
import threading

# Répertoire de base pour les dossiers clients
REPERTOIRE_BASE = "./clients"
if not os.path.exists(REPERTOIRE_BASE):
    os.makedirs(REPERTOIRE_BASE)

# Correspondance des extensions de fichiers aux ports des serveurs esclaves
SERVEURS_ESCLAVES = {
    ".py": 1111,   # Python
    ".c": 2222,    # C
    ".cpp": 2222,  # C++
    ".java": 3333  # Java
}

# Gestionnaire de connexion client
def gerer_client(socket_client, adresse_client, id_client):
    dossier_client = os.path.join(REPERTOIRE_BASE, f"client-{id_client}")
    os.makedirs(dossier_client, exist_ok=True)
    print(f"[+] Client {adresse_client} connecté. Dossier créé : {dossier_client}")

    try:
        while True:
            # Réception du nom du fichier
            nom_fichier = socket_client.recv(1024).decode('utf-8').strip()
            if not nom_fichier:
                break
            chemin_fichier = os.path.join(dossier_client, nom_fichier)

            # Réception du contenu du fichier
            with open(chemin_fichier, 'wb') as fichier:
                while True:
                    donnees = socket_client.recv(1024)
                    if donnees.endswith(b"END"):
                        fichier.write(donnees[:-3])
                        break
                    fichier.write(donnees)

            print(f"[Client-{id_client}] Fichier reçu : {nom_fichier}")
            chemin_resultat = envoyer_fichier_aux_esclaves(chemin_fichier, nom_fichier)
            envoyer_resultat_au_client(socket_client, chemin_resultat)

    except Exception as e:
        print(f"[-] Erreur avec le client-{id_client}: {e}")
    finally:
        socket_client.close()
        print(f"[-] Client {adresse_client} déconnecté.")
        supprimer_dossier(dossier_client)
        print(f"[INFO] Dossier client-{id_client} supprimé.")

# Fonction pour envoyer le fichier au serveur esclave approprié
# Fonction pour envoyer le fichier au serveur esclave approprié
def envoyer_fichier_aux_esclaves(chemin_fichier, nom_fichier):
    extension = os.path.splitext(nom_fichier)[1]
    port_esclave = SERVEURS_ESCLAVES.get(extension)

    if not port_esclave:
        print(f"[ERREUR] Extension {extension} non supportée.")
        return None

    # Remplacer "127.0.0.1" par l'adresse IP du conteneur correspondant
    ip_esclave = {
        1111: "172.18.0.2",  # IP pour le conteneur qui écoute sur le port 1111 (Python)
        2222: "172.18.0.3",  # IP pour le conteneur qui écoute sur le port 2222 (C/C++)
        3333: "172.18.0.4",  # IP pour le conteneur qui écoute sur le port 3333 (Java)
    }.get(port_esclave)

    if not ip_esclave:
        print(f"[ERREUR] Aucun conteneur trouvé pour le port {port_esclave}.")
        return None

    try:
        socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_esclave.connect((ip_esclave, port_esclave))  # Connexion à l'IP fixe du conteneur

        # Envoi du nom du fichier
        socket_esclave.sendall(f"{nom_fichier}\n".encode('utf-8'))
        
        # Envoi du contenu du fichier
        with open(chemin_fichier, 'rb') as fichier:
            while True:
                donnees = fichier.read(1024)
                if not donnees:
                    break
                socket_esclave.sendall(donnees)
        socket_esclave.sendall(b"END")
        print(f"[INFO] Fichier {nom_fichier} envoyé à {ip_esclave}:{port_esclave}.")

        # Réception du résultat depuis l'esclave
        return recevoir_resultat(socket_esclave)

    except Exception as e:
        print(f"[ERREUR] Impossible d'envoyer {nom_fichier} à {ip_esclave}:{port_esclave}: {e}")
        return None
    finally:
        socket_esclave.close()


def recevoir_resultat(socket_esclave):
    try:
        resultat = b""
        while True:
            donnees = socket_esclave.recv(1024)
            if not donnees:
                raise Exception("Connexion interrompue.")
            resultat += donnees
            if b"END" in donnees:
                resultat = resultat.replace(b"END", b"")
                break
        print("[INFO] Résultat reçu de l'esclave.")
        return resultat
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la réception du résultat: {e}")
        return None



# Fonction pour envoyer le résultat au client
def envoyer_resultat_au_client(socket_client, chemin_resultat):
    if chemin_resultat and os.path.exists(chemin_resultat):
        try:
            with open(chemin_resultat, 'rb') as fichier_resultat:
                while True:
                    donnees = fichier_resultat.read(1024)
                    if not donnees:
                        break
                    socket_client.sendall(donnees)
            socket_client.sendall(b"END")
            print(f"[INFO] Résultat envoyé au client.")
        except Exception as e:
            print(f"[ERREUR] Envoi du résultat échoué: {e}")

# Fonction de suppression de dossier
def supprimer_dossier(dossier):
    for racine, dossiers, fichiers in os.walk(dossier, topdown=False):
        for fichier in fichiers:
            os.remove(os.path.join(racine, fichier))
        for dossier_vide in dossiers:
            os.rmdir(os.path.join(racine, dossier_vide))
    os.rmdir(dossier)

# Serveur principal
def main():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("0.0.0.0", 1234))
    serveur.listen(5)
    print("[SERVEUR] En attente de connexions...")
    id_client = 0

    try:
        while True:
            socket_client, adresse_client = serveur.accept()
            id_client += 1
            thread_client = threading.Thread(
                target=gerer_client, 
                args=(socket_client, adresse_client, id_client)
            )
            thread_client.start()
    except KeyboardInterrupt:
        print("[SERVEUR] Arrêté par l'utilisateur.")
    finally:
        serveur.close()

if __name__ == "__main__":
    main()
