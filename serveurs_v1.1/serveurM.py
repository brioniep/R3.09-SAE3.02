import socket
import threading
import os
import subprocess

def handle_client(conn, address):
    send_file = None  # Initialiser la variable dès le début
    result_file = "compilation_result.txt"  # Fichier texte pour enregistrer le résultat
    try:
        print(f"Connexion acceptée de {address}")

        # Réception du nom de fichier
        filename = conn.recv(1024).decode()
        if not filename:
            raise Exception("Nom du fichier non reçu.")
        conn.send("Nom du fichier reçu".encode())  # Confirmation après avoir reçu le nom du fichier

        # Réception de la taille du fichier
        filesize = conn.recv(1024).decode()
        if not filesize:
            raise Exception("Taille du fichier non reçue.")
        filesize = int(filesize)
        conn.send("Taille du fichier reçue".encode())  # Confirmation après avoir reçu la taille

        # Réception du fichier
        print(f"Réception du fichier {filename} ({filesize} octets)")
        with open(filename, 'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)

        print(f"Fichier {filename} reçu avec succès.")

        # Détection de l'extension et traitement
        file_extension = os.path.splitext(filename)[1]
        output_file = "output"
        compilation_result = None

        if file_extension == '.c':
            # Commande de compilation
            compilation_command = f"gcc {filename} -o {output_file}"
            compilation_result = subprocess.run(compilation_command, shell=True, capture_output=True, text=True)

            # Vérifiez si la compilation a réussi
            if compilation_result.returncode == 0:
                send_file = output_file  # Définit le fichier à envoyer
                print(f"Compilation réussie. Exécutable : {send_file}")

                # Exécuter le programme si nécessaire
                execution_command = f"./{output_file}"
                execution_result = subprocess.run(execution_command, shell=True, capture_output=True, text=True)

                if execution_result.returncode == 0:
                    print(f"Exécution réussie : {execution_result.stdout}")
                    result_content = f"Exécution réussie:\n{execution_result.stdout}"
                else:
                    print(f"Erreur à l'exécution : {execution_result.stderr}")
                    result_content = f"Erreur à l'exécution :\n{execution_result.stderr}"
            else:
                print(f"Erreur à la compilation : {compilation_result.stderr}")
                result_content = f"Erreur à la compilation :\n{compilation_result.stderr}"

        elif file_extension in ['.cpp', '.cxx', '.cc']:
            compilation_command = f"g++ {filename} -o {output_file}"
            compilation_result = subprocess.run(compilation_command, shell=True, capture_output=True, text=True)
            send_file = output_file
            result_content = compilation_result.stdout if compilation_result.returncode == 0 else compilation_result.stderr

        elif file_extension == '.java':
            compilation_command = f"javac {filename}"
            compilation_result = subprocess.run(compilation_command, shell=True, capture_output=True, text=True)
            send_file = filename.replace(".java", ".class")
            result_content = compilation_result.stdout if compilation_result.returncode == 0 else compilation_result.stderr

        elif file_extension == '.py':
            execution_command = f"python {filename}"
            compilation_result = subprocess.run(execution_command, shell=True, capture_output=True, text=True)
            send_file = None
            result_content = compilation_result.stdout if compilation_result.returncode == 0 else compilation_result.stderr

        else:
            raise Exception(f"Extension de fichier non prise en charge : {file_extension}")

        # Écrire le résultat dans un fichier texte
        with open(result_file, 'w') as result_f:
            result_f.write(result_content)

        # Envoi du fichier résultat au client
        conn.send("file_result".encode())  # Indiquer qu'un fichier résultat sera envoyé
        with open(result_file, 'rb') as result_f:
            conn.sendall(result_f.read())  # Envoyer le contenu du fichier résultat

        print(f"Traitement du fichier {filename} terminé et résultat envoyé.")

    except Exception as e:
        print(f"Erreur : {e}")
        conn.send("error".encode())
        conn.send(str(e).encode())

    finally:
        # Nettoyage des fichiers temporaires
        if filename and os.path.exists(filename):
            os.remove(filename)
        if send_file and os.path.exists(send_file):
            os.remove(send_file)
        if os.path.exists(result_file):
            os.remove(result_file)  # Supprimer le fichier résultat après l'envoi

        conn.close()
        print(f"Connexion avec {address} terminée.")

def ouverture(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Serveur en écoute sur le port {port}...")

    while True:
        conn, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()

if __name__ == "__main__":
    port = 12345
    ouverture(port)
