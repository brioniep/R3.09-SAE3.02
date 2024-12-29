"""
La documentation développeur des serveurs esclaves est centralisée dans ce fichier,
car les autres fichiers de serveurs esclaves sont identiques à l'exception des ports.
"""

import os , socket , threading , subprocess

class ServeurEsclave:

    def __init__(self, port_esclave=1111):
        self.port_esclave = port_esclave
        self.socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def lancer_serveur_esclave(self): 
        """
        Démarre le serveur esclave en attente de connexions des serveurs maîtres.
        
        Variables :
            socket_esclave (socket.socket) : Le socket utilisé pour accepter les connexions des serveurs maîtres.
            port_esclave (int) : Le port sur lequel le serveur esclave écoute les connexions entrantes.
            client_socket (socket.socket) : Le socket de communication utilisé pour échanger des données avec un serveur maître.
            client_address (tuple) : L'adresse IP et le port du serveur maître qui se connecte au serveur esclave.
            t1 (threading.Thread) : Le thread lancé pour gérer la réception du fichier une fois la connexion établie.

        Méthodes appelées :
            socket.setsockopt() : Configure le socket pour permettre la réutilisation de l'adresse locale.
            socket.bind() : Associe le socket à une adresse et un port spécifiques.
            socket.listen() : Configure le socket pour écouter les connexions entrantes.
            socket.accept() : Accepte une connexion entrante et retourne un nouveau socket pour la communication avec le client.
            threading.Thread() : Crée un nouveau thread pour gérer la réception du fichier.
            reception_fichier() : La méthode qui sera exécutée dans un thread pour gérer la réception du fichier envoyé par le serveur maître.
        """
        self.socket_esclave.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_esclave.bind(('0.0.0.0', self.port_esclave))
        self.socket_esclave.listen(5)
        print(f"[+] Serveur esclave en écoute sur le port {self.port_esclave}...")

        while True:
            client_socket, client_address = self.socket_esclave.accept()
            print(f"[+] Connexion acceptée du serveur maître : {client_address}")
            t1 = threading.Thread(target=self.reception_fichier, args=(client_socket,))
            t1.start()


    def reception_fichier(self, client_socket):
        """
        Réceptionne un fichier envoyé par le serveur maître via une connexion socket.

        Variables :
            client_socket (socket.socket) : Le socket de communication avec le serveur maître.
            donnees (str) : Les données reçues du serveur maître, encodées en UTF-8.
            fichier_info (list) : La liste obtenue en séparant `donnees` en trois parties distinctes : ID client, nom du fichier et contenu du fichier.
            id_client (str) : L'identifiant du client qui a envoyé le fichier.
            nom_fichier (str) : Le nom du fichier envoyé par le client.
            contenu_fichier (str) : Le contenu du fichier envoyé par le client.

        Méthodes appelées :
            enregistrement_fichier() : Méthode utilisée pour enregistrer le fichier sur le serveur après sa réception.
        """
        try:
            donnees = client_socket.recv(4096).decode('utf-8')
            if not donnees:
                print("[-] Aucune donnée reçue.")
                return

            fichier_info = donnees.split('|', 2)
            if len(fichier_info) != 3:
                print("[-] Données reçues incorrectes.")
                return

            id_client, nom_fichier, contenu_fichier = fichier_info
            print(f"[+] ID Client: {id_client}, Nom du fichier: {nom_fichier}")
            print(f"[+] Contenu du fichier:\n{contenu_fichier}")

            self.enregistrement_fichier(id_client, nom_fichier, contenu_fichier)

        except Exception as e:
            print(f"[!] Erreur lors de la réception du fichier: {e}")


    def enregistrement_fichier(self, id_client, nom_fichier, contenu_fichier):
        """
        Enregistre le fichier reçu sur le serveur dans un dossier dédié à l'ID du client.

        Variables :
            id_client (str) : L'identifiant du client qui envoie le fichier.
            nom_fichier (str) : Le nom du fichier à enregistrer.
            contenu_fichier (str) : Le contenu du fichier à enregistrer.
            dossier_client (str) : Le chemin du dossier créé pour le client, basé sur l'ID du client.
            chemin_fichier (str) : Le chemin complet où le fichier sera enregistré.
            _ (str) : La partie non utilisée de l'extension du fichier, utilisée pour récupérer l'extension.
            extension (str) : L'extension du fichier, extraite du nom du fichier.

        Méthodes appelées :
            résultat_execution() : Méthode utilisée pour traiter le fichier après son enregistrement, en fonction de son extension.
        """
        try:
            dossier_client = os.path.join(os.getcwd(), str(id_client))
            os.makedirs(dossier_client, exist_ok=True)

            chemin_fichier = os.path.join(dossier_client, nom_fichier)

            with open(chemin_fichier, 'w') as f:
                f.write(contenu_fichier)

            print(f"[+] Fichier enregistré dans {chemin_fichier}")

            _, extension = os.path.splitext(nom_fichier)

            self.résultat_execution(chemin_fichier, extension)

        except Exception as e:
            print(f"[!] Erreur lors de l'enregistrement du fichier: {e}")





    def résultat_execution(self, fichier_path, extension):
        """
        Exécute un fichier en fonction de son extension et envoie le résultat au serveur maître.

        Variables :
            fichier_path (str) : Le chemin complet du fichier à exécuter.
            extension (str) : L'extension du fichier, utilisée pour déterminer quel type d'exécution appliquer.
            result (str) : Le résultat de l'exécution du fichier, qui peut être un message d'erreur ou un résultat spécifique.
            id_client (str) : L'identifiant du client, extrait du chemin du fichier.
            nom_fichier (str) : Le nom du fichier, extrait du chemin complet.

        Méthodes appelées :
            executer_python() : Exécute un fichier Python si l'extension est ".py".
            compiler_et_executer_c() : Compile et exécute un fichier C si l'extension est ".c".
            compiler_et_executer_cpp() : Compile et exécute un fichier C++ si l'extension est ".cpp".
            compiler_et_executer_java() : Compile et exécute un fichier Java si l'extension est ".java".
            envoie_srv_maitre() : Envoie le résultat de l'exécution du fichier au serveur maître.
            nettoyer_fichier() : Supprime les fichiers temporaires ou exécutés.

        """
        try:
            result = ""
            print(f"[+] Exécution du fichier avec extension {extension}: {fichier_path}")

            # Vérifie l'extension du fichier et choisit la méthode d'exécution appropriée
            if extension == ".py":
                result = self.executer_python(fichier_path)
            elif extension == ".c":
                result = self.compiler_et_executer_c(fichier_path)
            elif extension == ".cpp":
                result = self.compiler_et_executer_cpp(fichier_path)
            elif extension == ".java":
                result = self.compiler_et_executer_java(fichier_path)
            else:
                result = "Type de fichier non pris en charge."

            print(f"[+] Résultat de l'exécution: {result}")

            id_client = os.path.basename(os.path.dirname(fichier_path))
            nom_fichier = os.path.basename(fichier_path)
            self.envoie_srv_maitre(id_client, nom_fichier, result)
            self.nettoyer_fichier(fichier_path)

            return result

        except Exception as e:
            print(f"[!] Erreur lors de l'exécution : {e}")
            return f"Erreur : {e}"

        

    def executer_python(self, fichier_path):
        """
        Exécute un fichier Python à l'aide de `subprocess.run` et capture sa sortie.

        Variables :
            fichier_path (str) : Le chemin complet du fichier Python à exécuter.

        Méthodes appelées :
            subprocess.run() : Exécute le fichier Python et capture la sortie.
        """
        try:
            print(f"[-] Exécution du fichier Python: {fichier_path}")
            
            result = subprocess.run(['python3', fichier_path], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[!] Erreur d'exécution Python : {result.stderr}")
                return f"[!] Erreur d'exécution Python : {result.stderr}"
            
            print(f"Sortie d'exécution Python : {result.stdout}")
            return result.stdout
        except Exception as e:
            print(f"[!] Erreur lors de l'exécution Python : {e}")
            return f"[!] Erreur d'exécution Python : {e}"



    def compiler_et_executer_c(self, fichier_path):
        """
        Compile et exécute un fichier source C.

        Variables :
            fichier_path (str) : Le chemin complet du fichier source C à compiler et à exécuter.

        Méthodes appelées :
            subprocess.run() : Exécute la commande `gcc` pour compiler le fichier C et exécute le programme compilé.
        """
        try:
            output = subprocess.run(['gcc', fichier_path, '-o', 'a.out'], capture_output=True, text=True)
            
            if output.returncode != 0:
                return f"[!] Erreur de compilation C : {output.stderr}"

            result = subprocess.run(['./a.out'], capture_output=True, text=True)
            
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"[!] Erreur d'exécution C : {e}"



    def compiler_et_executer_cpp(self, fichier_path):
        """
        Compile et exécute un fichier source C++.

        Variables :
            fichier_path (str) : Le chemin complet du fichier source C++ à compiler et exécuter.

        Méthodes appelées :
            subprocess.run() : Exécute la commande `g++` pour compiler le fichier C++ et exécute le programme compilé.
        """
        try:
            output = subprocess.run(['g++', fichier_path, '-o', 'a.out'], capture_output=True, text=True)
            
            if output.returncode != 0:
                return f"[!] Erreur de compilation C++ : {output.stderr}"

            result = subprocess.run(['./a.out'], capture_output=True, text=True)
            
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"[!] Erreur d'exécution C++ : {e}"


    def compiler_et_executer_java(self, fichier_path):
        """
        Compile et exécute un fichier source Java.

        Variables :
            fichier_path (str) : Le chemin complet du fichier source Java à compiler et exécuter.
            class_name (str) : Le nom de la classe Java sans extension (déduit du fichier source).
            directory (str) : Le répertoire contenant le fichier source Java.
            class_file (str) : Le chemin du fichier `.class` généré après la compilation.

        Méthodes appelées :
            subprocess.run() : Exécute la commande `javac` pour compiler le fichier Java et `java` pour exécuter le fichier compilé.
            os.path.splitext() : Utilisé pour obtenir le nom de la classe sans son extension.
            os.path.basename() : Utilisé pour obtenir le nom de fichier sans son chemin.
            os.path.dirname() : Utilisé pour obtenir le répertoire du fichier source Java.
            os.path.exists() : Vérifie si le fichier `.class` a été généré après la compilation.
        """
        try:
            class_name = os.path.splitext(os.path.basename(fichier_path))[0]
            directory = os.path.dirname(fichier_path)
            
            output = subprocess.run(['javac', fichier_path], capture_output=True, text=True, cwd=directory)
            if output.returncode != 0:
                return f"[!] Erreur de compilation Java : {output.stderr}"

            class_file = os.path.join(directory, f'{class_name}.class')
            if not os.path.exists(class_file):
                return f"[!] Erreur : le fichier {class_file} n'a pas été généré."

            result = subprocess.run(['java', '-cp', directory, class_name], capture_output=True, text=True)

            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"[!] Erreur d'exécution Java : {e}"


    def envoie_srv_maitre(self, id_client, nom_fichier, resultat_execution):
        """
        Envoie un message contenant les informations d'un fichier exécuté au serveur maître.

        Variables :
            id_client (str) : L'identifiant du client qui a envoyé le fichier.
            nom_fichier (str) : Le nom du fichier exécuté.
            resultat_execution (str) : Le résultat de l'exécution du fichier.

        Méthodes appelées :
            socket.socket() : Crée un socket pour la communication réseau.
            s.connect() : Connecte le socket au serveur maître (adresse IP et port spécifiés).
            s.sendall() : Envoie le message formé au serveur maître.
            encode() : Encode le message en UTF-8 avant de l'envoyer.
        """
        try:
            # Création et ouverture d'un socket pour se connecter au serveur maître
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('172.17.0.1', 5555))
                
                # Création du message à envoyer
                message = f"{id_client}|{nom_fichier}|{resultat_execution}"
                
                # Envoi du message encodé au serveur maître
                s.sendall(message.encode('utf-8'))
                print(f"[+] Message envoyé au serveur maître: {message}")
        except Exception as e:
            print(f"[!] Erreur lors de l'envoi au serveur maître: {e}")





def nettoyer_fichier(self, fichier_path):
    """
    Supprime le dossier contenant le fichier spécifié après l'exécution.

    Variables :
        fichier_path (str) : Le chemin du fichier dont le dossier contenant sera supprimé.

    Méthodes appelées :
        os.path.dirname() : Extrait le répertoire parent du fichier spécifié.
        os.path.exists() : Vérifie si le répertoire spécifié existe.
        subprocess.run() : Exécute une commande shell pour supprimer le dossier.
    """
    try:
        dossier_client = os.path.dirname(fichier_path)
        
        if os.path.exists(dossier_client):
            subprocess.run(['rm', '-rf', dossier_client])
            print(f"[-] Dossier supprimé : {dossier_client}")
        else:
            print(f"[-] Le dossier {dossier_client} n'existe pas.")
    except Exception as e:
        print(f"[!] Erreur lors de la suppression du dossier : {e}")


if __name__ == "__main__":
    serveur = ServeurEsclave()
    try:
        serveur.lancer_serveur_esclave()
    except KeyboardInterrupt:
        print("Arrêt du serveur...")
        serveur.socket_esclave.close()
