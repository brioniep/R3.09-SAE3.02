import os
import socket
import threading
import subprocess

class ServeurEsclave:

    def __init__(self, port_esclave=1111):
        self.port_esclave = port_esclave
        self.socket_esclave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def lancer_serveur_esclave(self):
        self.socket_esclave.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_esclave.bind(('0.0.0.0', self.port_esclave))
        self.socket_esclave.listen(5)
        print(f"Serveur esclave en écoute sur le port {self.port_esclave}...")

        while True:
            client_socket, client_address = self.socket_esclave.accept()
            print(f"Connexion acceptée du server maitre : {client_address}")
            t1 = threading.Thread(target=self.reception_fichier, args=(client_socket,))
            t1.start()

    def reception_fichier(self, client_socket):
        try:
            donnees = client_socket.recv(4096).decode('utf-8')
            if not donnees:
                print("Aucune donnée reçue.")
                return

            fichier_info = donnees.split('|', 2)
            if len(fichier_info) != 3:
                print("Données reçues incorrectes.")
                return

            id_client, nom_fichier, contenu_fichier = fichier_info
            print(f"[RECEPTION] ID Client: {id_client}, Nom du fichier: {nom_fichier}")
            print(f"[RECEPTION] Contenu du fichier:\n{contenu_fichier}")

            self.enregistrement_fichier(id_client, nom_fichier, contenu_fichier)

        except Exception as e:
            print(f"[-] Erreur lors de la réception du fichier: {e}")

    def enregistrement_fichier(self, id_client, nom_fichier, contenu_fichier):
        try:
            dossier_client = os.path.join(os.getcwd(), str(id_client))
            os.makedirs(dossier_client, exist_ok=True)

            chemin_fichier = os.path.join(dossier_client, nom_fichier)

            with open(chemin_fichier, 'w') as f:
                f.write(contenu_fichier)

            print(f"[ENREGISTREMENT] Fichier enregistré dans {chemin_fichier}")

            _, extension = os.path.splitext(nom_fichier)

            self.résultat_execution(chemin_fichier, extension)

        except Exception as e:
            print(f"[-] Erreur lors de l'enregistrement du fichier: {e}")

    def résultat_execution(self, fichier_path, extension):
        try:
            result = ""
            
            print(f"Exécution du fichier avec extension {extension}: {fichier_path}")

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

            print(f"Résultat de l'exécution: {result}")
            return result
            
        except Exception as e:
            print(f"[-] Erreur lors de l'exécution : {e}")
            return f"Erreur : {e}"

    def executer_python(self, fichier_path):
        try:
            print(f"Exécution du fichier Python: {fichier_path}")
            
            result = subprocess.run(['python3', fichier_path], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Erreur d'exécution Python : {result.stderr}")
                return f"Erreur d'exécution Python : {result.stderr}"
            
            print(f"Sortie d'exécution Python : {result.stdout}")
            return result.stdout
        except Exception as e:
            print(f"Erreur lors de l'exécution Python : {e}")
            return f"Erreur d'exécution Python : {e}"

    def compiler_et_executer_c(self, fichier_path):
        try:
            output = subprocess.run(['gcc', fichier_path, '-o', 'a.out'], capture_output=True, text=True)
            if output.returncode != 0:
                return f"Erreur de compilation C : {output.stderr}"

            result = subprocess.run(['./a.out'], capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erreur d'exécution C : {e}"

    def compiler_et_executer_cpp(self, fichier_path):
        try:
            output = subprocess.run(['g++', fichier_path, '-o', 'a.out'], capture_output=True, text=True)
            if output.returncode != 0:
                return f"Erreur de compilation C++ : {output.stderr}"

            result = subprocess.run(['./a.out'], capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erreur d'exécution C++ : {e}"

    def compiler_et_executer_java(self, fichier_path):
        try:
            class_name = os.path.splitext(os.path.basename(fichier_path))[0]
            directory = os.path.dirname(fichier_path)
            
            output = subprocess.run(['javac', fichier_path], capture_output=True, text=True, cwd=directory)
            if output.returncode != 0:
                return f"Erreur de compilation Java : {output.stderr}"

            class_file = os.path.join(directory, f'{class_name}.class')
            if not os.path.exists(class_file):
                return f"Erreur : le fichier {class_file} n'a pas été généré."

            result = subprocess.run(['java', '-cp', directory, class_name], capture_output=True, text=True)

            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erreur d'exécution Java : {e}"







if __name__ == "__main__":
    serveur = ServeurEsclave(port_esclave=1111)
    try:
        serveur.lancer_serveur_esclave()
    except KeyboardInterrupt:
        print("Arrêt du serveur...")
        serveur.socket_esclave.close()
