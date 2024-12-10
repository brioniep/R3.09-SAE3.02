import socket
import sys
import subprocess
import time

HOST = 'localhost'
PORT = 5551

def start_slave():
    try:
        result = subprocess.run(["docker", "ps", "-a", "--filter", "name=server-esclave1", "--format", "{{.Status}}"], capture_output=True, text=True)
        
        if "Exited" in result.stdout:
            print("Le serveur esclave est arrêté, lancement du conteneur...")
            subprocess.run(["docker", "start", "server-esclave1"])
        else:
            print("Le serveur esclave est déjà en cours d'exécution.")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur esclave : {e}")

def stop_slave():
    try:
        result = subprocess.run(["docker", "ps", "--filter", "name=server-esclave1", "--format", "{{.Status}}"], capture_output=True, text=True)
        
        if "Up" in result.stdout:
            print("Arrêt du serveur esclave...")
            subprocess.run(["docker", "stop", "server-esclave1"])
        else:
            print("Le serveur esclave n'est pas en cours d'exécution.")
            
    except Exception as e:
        print(f"Erreur lors de l'arrêt du serveur esclave : {e}")

def communicate_with_slave():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connecté au serveur esclave {HOST}:{PORT}")
            
            message = "Exécuter la commande"
            s.sendall(message.encode())
            print(f"Message envoyé au serveur esclave : {message}")
            
            data = s.recv(1024)
            print(f"Réponse du serveur esclave : {data.decode()}")
            
    except Exception as e:
        print(f"Erreur lors de la communication avec le serveur esclave : {e}")

if __name__ == "__main__":
    try:
        while True:
            user_input = input("Tapez 'start_slave' pour démarrer le serveur esclave, 'stop_slave' pour arrêter le serveur esclave, ou 'exit' pour quitter : ")
            
            if user_input == "start_slave":
                start_slave()
                communicate_with_slave()
            elif user_input == "stop_slave":
                stop_slave()
            elif user_input == "exit":
                print("Arrêt du serveur maître.")
                break
            else:
                print("Commande inconnue. Essayez à nouveau.")
                
    except KeyboardInterrupt:
        print("\nArrêt du serveur maître.")
        sys.exit(0)
