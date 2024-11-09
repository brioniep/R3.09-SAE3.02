import socket
import threading
import os
import subprocess

def ouverture(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Serveur en écoute sur le port {port}...")

    while True:
        conn, address = server_socket.accept()
        print(f"Connexion acceptée de {address}")

        try:
            filename = conn.recv(1024).decode()
            if not filename:
                print("Nom du fichier non reçu, connexion fermée.")
                break

            filesize = conn.recv(1024).decode()
            if not filesize:
                print("Taille du fichier non reçue, connexion fermée.")
                break
            filesize = int(filesize)

            with open(filename, 'wb') as f:
                bytes_received = 0
                while bytes_received < filesize:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)

            file_extension = os.path.splitext(filename)[1]
            output_file = "output"
            compilation_result = ""

            if file_extension == '.c':
                compilation_command = f"gcc {filename} -o {output_file}"
                compilation_result = subprocess.run(compilation_command, shell=True, capture_output=True, text=True)
                send_file = output_file

            elif file_extension in ['.cpp', '.cxx', '.cc']:
                compilation_command = f"g++ {filename} -o {output_file}"
                compilation_result = subprocess.run(compilation_command, shell=True, capture_output=True, text=True)
                send_file = output_file

            elif file_extension == '.java':
                compilation_command = f"javac {filename}"
                compilation_result = subprocess.run(compilation_command, shell=True, capture_output=True, text=True)
                send_file = filename.replace(".java", ".class")

            elif file_extension == '.py':
                execution_command = f"python {filename}"
                compilation_result = subprocess.run(execution_command, shell=True, capture_output=True, text=True)
                send_file = None

            if compilation_result.returncode != 0:
                conn.send("error".encode())
                conn.send(compilation_result.stderr.encode())
            else:
                if send_file and os.path.exists(send_file):
                    conn.send("file".encode())
                    with open(send_file, 'rb') as f:
                        conn.sendall(f.read())
                else:
                    conn.send("output".encode())
                    conn.send(compilation_result.stdout.encode())

            os.remove(filename)
            if send_file and os.path.exists(send_file):
                os.remove(send_file)

        except Exception as e:
            print("Erreur lors de la réception ou de la compilation :", e)
        finally:
            conn.close()

if __name__ == "__main__":
    port = 12345
    thread = threading.Thread(target=ouverture, args=(port,))
    thread.start()
    thread.join()
