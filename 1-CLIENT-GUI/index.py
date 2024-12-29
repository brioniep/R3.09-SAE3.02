import sys
import socket
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import re

class MaFenetre(QWidget):
    def __init__(self, authenticated=False):  
        super().__init__()

        if not authenticated:
            QMessageBox.critical(None, "Erreur", "Accès non autorisé. Veuillez vous connecter.")
            sys.exit() 

        self.setWindowTitle("Client PyQt6 - Connexion au Serveur")
        self.socket_client = None
        self.est_connecte = False
        self.initUI()

    def initUI(self):
        disposition_grille = QGridLayout()

        self.ip = QLabel("@IP srv: ")
        self.ip_input = QLineEdit("192.168.1.1")
        self.port = QLabel("Port: ")
        self.port_input = QLineEdit("1234")
        self.connecter = QPushButton("Connexion")
        self.deconnecter = QPushButton("Déconnexion")

        self.selection_fichier = QPushButton("Sélectionner un fichier")
        self.selection_fichier.setEnabled(False)
        self.telecharger = QPushButton("Envoyer")
        self.telecharger.setEnabled(False)

        self.chemin = QLineEdit()
        self.chemin.setReadOnly(True)
        self.fichiers_recus = QTextEdit()
        self.fichiers_recus.setReadOnly(True)

        self.historique_logs = QTextEdit()
        self.historique_logs.setReadOnly(True)

        self.quitter = QPushButton("Quitter")
        self.aide = QPushButton("Aide ?")


        disposition_grille.addWidget(self.ip, 0, 0)
        disposition_grille.addWidget(self.ip_input, 0, 1)
        disposition_grille.addWidget(self.port, 1, 0)
        disposition_grille.addWidget(self.port_input, 1, 1)
        disposition_grille.addWidget(self.connecter, 2, 0, 1, 2)
        disposition_grille.addWidget(self.historique_logs, 3, 0, 1, 2)
        disposition_grille.addWidget(self.deconnecter, 4, 0, 1, 2)

        disposition_grille.addWidget(self.selection_fichier, 0, 2)
        disposition_grille.addWidget(self.telecharger, 0, 3)
        disposition_grille.addWidget(self.chemin, 1, 2, 1, 2)
        disposition_grille.addWidget(self.fichiers_recus, 2, 2, 3, 2)

        disposition_grille.addWidget(self.quitter, 5, 0, 1, 2)
        disposition_grille.addWidget(self.aide, 5, 2, 1, 2)    


        self.quitter.clicked.connect(self.quitter_app)
        self.aide.clicked.connect(self.aide_util)

        self.setLayout(disposition_grille)

        self.connecter.clicked.connect(self.connexion_au_serveur)
        self.deconnecter.clicked.connect(self.deconnexion_du_serveur)

        self.selection_fichier.clicked.connect(self.selectionner_fichier)
        self.telecharger.clicked.connect(self.envoyer_fichier)

    def quitter_app(self):
        if self.est_connecte:
            self.deconnexion_du_serveur()
        self.close()



    def aide_util(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information) 
        message_box.setWindowTitle("Aide")             

        # Définir le texte d'aide avec toutes les informations importantes
        message_box.setText(
            "Client PyQt6 - Connexion au Serveur\n\n"
            "1. Connexion au serveur\n"
            "   - Entrez l'IP et le port du serveur.\n"
            "   - Cliquez sur 'Connexion' pour vous connecter.\n"
            "   - Si déjà connecté, un message d'erreur s'affichera.\n\n"
            "2. Sélection de fichier\n"
            "   - Cliquez sur 'Sélectionner un fichier' pour choisir un fichier à envoyer.\n"
            "   - Les formats supportés sont C, C++, Java, Python.\n\n"
            "3. Envoi de fichier\n"
            "   - Après la sélection, cliquez sur 'Envoyer' pour transmettre le fichier au serveur.\n\n"
            "4. Historique des logs\n"
            "   - Affiche les messages de connexion, déconnexion et envoi/réception de fichiers.\n\n"
            "5. Déconnexion\n"
            "   - Cliquez sur 'Déconnexion' pour fermer la connexion avec le serveur.\n\n"
            "6. Quitter\n"
            "   - Ferme l'application.\n\n"
            "Pour plus de précisions, consultez la documentation."
        )
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def connexion_au_serveur(self):
        ip = self.ip_input.text()
        port = self.port_input.text()

        ip_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not ip_regex.match(ip):
            QMessageBox.warning(self, "Erreur de syntaxe", "L'adresse IP est incorrecte.")
            return

        if not port.isdigit() or not (0 <= int(port) <= 65535):
            QMessageBox.warning(self, "Erreur de syntaxe", "Le port est incorrect.")
            return

        port = int(port)

        if self.est_connecte:
            self.historique_logs.append("<span style='color: red;'>[-]</span> Déjà connecté au serveur.")
            return

        def essayer_connexion():
            while not self.est_connecte:
                try:
                    self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket_client.settimeout(3)
                    self.socket_client.connect((ip, port))
                    self.socket_client.settimeout(None)
                    self.est_connecte = True
                    self.selection_fichier.setEnabled(True)
                    self.telecharger.setEnabled(True)

                    self.recepteur_thread = QThread(self)
                    self.recepteur_thread.run = self.recevoir_donnees
                    self.recepteur_thread.start()

                    self.historique_logs.append(f"<span style='color: green;'>[+]</span>Connexion réussie à {ip}:{port}")
                except socket.timeout:
                    self.historique_logs.append(f"<span style='color: red;'>[-]</span> Erreur : Connexion au serveur {ip}:{port} a expiré. Réessai dans 5 secondes.")
                    print(f"[-] Erreur : Connexion au serveur {ip}:{port} a expiré. Réessai dans 5 secondes.")
                    QThread.sleep(5)
                except Exception as e:
                    self.historique_logs.append(f"<span style='color: red;'>[-]</span> Erreur lors de la connexion : {e}. Réessai dans 5 secondes.")
                    print(f"[-] Erreur lors de la connexion : {e}. Réessai dans 5 secondes.")
                    QThread.sleep(5)

        self.connexion_thread = QThread(self)
        self.connexion_thread.run = essayer_connexion
        self.connexion_thread.start()

    def deconnexion_du_serveur(self):
        if self.est_connecte:
            try:
                self.socket_client.close()
                self.est_connecte = False
                self.selection_fichier.setEnabled(False)
                self.telecharger.setEnabled(False)
                self.historique_logs.append("<span style='color: green;'>[+]</span> Déconnexion réussie.")
                print("Déconnexion réussie.")
                if self.recepteur_thread:
                    self.recepteur_thread.quit()
                    self.recepteur_thread = None
            except Exception as e:
                self.historique_logs.append(f"<span style='color: red;'>[-]</span> Erreur lors de la déconnexion : {e}")
                print(f"[-] Erreur lors de la déconnexion : {e}")
        else:
            self.historique_logs.append("<span style='color: red;'>[-]</span> Pas de connexion active.")

    def selectionner_fichier(self):
        fichier = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "Tous les fichiers (*);;Fichiers texte (*.txt);;Images (*.png *.xpm *.jpg)")
        
        if fichier[0]:
            extension = os.path.splitext(fichier[0])[1]
            if extension not in ['.c', '.cpp', '.java', '.py']:
                QMessageBox.warning(self, "Format de fichier incorrect", "Le format du fichier sélectionné n'est pas supporté. Veuillez choisir un fichier C, C++, Java ou Python.")
                return
        
        self.chemin.setText(fichier[0])

    def envoyer_fichier(self):
        if not self.est_connecte:
            self.historique_logs.append("<span style='color: red;'>[-] Erreur : </span>Pas de connexion au serveur.")
            return
        chemin_fichier = self.chemin.text()

        if not chemin_fichier or not os.path.isfile(chemin_fichier):
            self.historique_logs.append("<span style='color: red;'>[-] Erreur : </span>Aucun fichier valide sélectionné.")
            return

        try:
            with open(chemin_fichier, 'rb') as f:
                fichier_nom = os.path.basename(chemin_fichier)
                self.socket_client.sendall(fichier_nom.encode('utf-8') + b"\n")
                contenu_fichier = f.read()
                try:
                    self.socket_client.sendall(contenu_fichier)
                    self.socket_client.sendall(b"\0")
                except Exception as e:
                    print(f"Erreur lors de l'envoi du fichier : {e}")
                    return

            fichier_nom = os.path.basename(chemin_fichier)
            self.historique_logs.append(f"<span style='color: green;'>[+]</span> Fichier '{fichier_nom}' envoyé avec succès.")
            self.chemin.clear()

        except Exception as e:
            self.historique_logs.append(f"<span style='color: red;'>Erreur</span> : lors de l'envoi du fichier : {e}")

    def recevoir_donnees(self):
        while self.est_connecte:
            try:
                donnees = self.socket_client.recv(4096).decode('utf-8')
                if donnees:
                    nom_fichier, contenu_fichier = donnees.split('|||', 1)
                    self.afficher_message(nom_fichier, contenu_fichier)
                else:
                    break
            except Exception as e:
                print(f"Erreur de réception : {e}")
                break

    def afficher_message(self, nom_fichier, contenu_fichier):
        extention = os.path.splitext(nom_fichier)[1]

        prompt = ""
        if extention == ".py":
            prompt = f"<span style='color: blue;'>╔═[</span>user@client:~/workspace]<br><span style='color: blue;'>╚═══> $</span> {nom_fichier}"
        elif extention == ".c":
            prompt = f"<span style='color: green;'>╔═[</span>user@client:~/workspace]<br><span style='color: green;'>╚═══> $</span> {nom_fichier}"
        elif extention == ".cpp":
            prompt = f"<span style='color: orange;'>╔═[</span>user@client:~/workspace]<br><span style='color: orange;'>╚═══> $</span> {nom_fichier}"
        elif extention == ".java":
            prompt = f"<span style='color: red;'>╔═[</span>user@client:~/workspace]<br><span style='color: red;'>╚═══> $</span> {nom_fichier}"

        self.fichiers_recus.append(prompt)
        self.fichiers_recus.append(contenu_fichier)
        self.historique_logs.append(f"<span style='color: green;'>[+]</span> Fichier '{nom_fichier}' reçu avec succès : {nom_fichier}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(800, 500)
    fenetre.show()
    sys.exit(app.exec())
