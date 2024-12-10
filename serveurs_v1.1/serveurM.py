import os
import socket
import threading

class ServeurPrincipal:

    def __init__(self, port_principal=1234, port_client=9999, hote_client='127.0.0.1'):
        self.port_principal = port_principal
        self.port_client = port_client
        self.hote_client = hote_client
        self.socket_principal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def lancer_serveur_principal(self):
        self.socket_principal.bind(('0.0.0.0', self.port_principal))
        self.socket_principal.listen(5)
        print(f"Serveur principal en écoute sur le port {self.port_principal}...")

        while True:
            client_socket, client_address = self.socket_principal.accept()
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
    serveur = ServeurPrincipal()
    try:
        serveur.lancer_serveur_principal()
    except KeyboardInterrupt:
        print("Arrêt du serveur...")
        serveur.socket_principal.close()
