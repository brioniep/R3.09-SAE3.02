import socket
import os
import time
import threading

class ServeurPrincipal:

    def __init__(self, port_principal=1234, port_secondaire=5678, port_client=9999, hote_client='127.0.0.1'):
        self.port_principal = port_principal
        self.port_secondaire = port_secondaire
        self.port_client = port_client   # Port du client qui recevra les informations
        self.hote_client = hote_client   # Adresse IP du client qui recevra les informations
        self.socket_principal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_secondaire = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secondaire_lance = False  
        self.secondaire_actif = False  
        self.cores_cpu = self.obtenir_cores_cpu()  

    def infos_ram(self):
        donnees_ram = os.popen("free -m | awk '/Mem:/ {print $2, $3}'").read().strip().split()
        ram_totale = int(donnees_ram[0])
        ram_utilisee = int(donnees_ram[1])
        pourcentage_ram = (ram_utilisee / ram_totale) * 100
        return pourcentage_ram

    def infos_cpu(self):
        charge_moyenne = float(os.popen("uptime | awk -F'load average:' '{print $2}' | cut -d ',' -f1").read().strip())
        pourcentage_cpu = (charge_moyenne / self.cores_cpu) * 100
        return pourcentage_cpu

    def obtenir_cores_cpu(self):
        return int(os.popen("nproc").read().strip())

    def lancer_serveur_principal(self):
        self.socket_principal.bind(('0.0.0.0', self.port_principal))
        self.socket_principal.listen(5)
        print(f"Serveur principal en écoute sur le port {self.port_principal}...")

        while True:
            utilisation_ram = self.infos_ram()
            utilisation_cpu = self.infos_cpu()

            print(f"RAM utilisée : {utilisation_ram:.2f}%")
            print(f"Charge CPU : {utilisation_cpu:.2f}%")

            if utilisation_ram >= 60.0 and not self.secondaire_lance:
                self.secondaire_actif = True
                threading.Thread(target=self.lancer_serveur_secondaire, daemon=True).start()
                self.secondaire_lance = True

            elif utilisation_ram < 60.0 and self.secondaire_lance:
                self.arreter_serveur_secondaire()
                self.secondaire_lance = False

            time.sleep(5)

    def lancer_serveur_secondaire(self):
        try:
            self.socket_secondaire.bind(('0.0.0.0', self.port_secondaire))
            self.socket_secondaire.listen(5)
            print(f"Serveur secondaire démarré sur le port {self.port_secondaire}...")

            while self.secondaire_actif:
                try:
                    self.socket_secondaire.settimeout(1)
                    client_socket, adresse = self.socket_secondaire.accept()
                    print(f"Connexion établie avec {adresse}")
                    client_socket.send(b"Bonjour depuis le serveur secondaire !")
                    client_socket.close()
                except socket.timeout:
                    continue
        except OSError as e:
            print(f"Erreur lors du démarrage du serveur secondaire : {e}")

    def arreter_serveur_secondaire(self):
        self.secondaire_actif = False
        self.socket_secondaire.close()
        self.socket_secondaire = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Serveur secondaire arrêté proprement.")

if __name__ == "__main__":
    serveur = ServeurPrincipal()
    serveur.lancer_serveur_principal()
