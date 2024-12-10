import sys
import socket
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client PyQt6 - Connexion au Serveur")
        self.socket_client = None
        self.est_connecte = False
        self.initUI()

    def initUI(self):
        disposition_grille = QGridLayout()

        self.ip = QLabel("@IP srv: ")
        self.ip_input = QLineEdit("192.168.1.11")
        self.port = QLabel("Port: ")
        self.port_input = QLineEdit("1234")
        self.connecter = QPushButton("Connexion")
        self.deconnecter = QPushButton("Déconnexion")

        self.selection_fichier = QPushButton("Sélectionner un fichier")
        self.telecharger = QPushButton("Envoyer")
        self.chemin = QLineEdit()
        self.fichiers_recus = QTextEdit()
        self.fichiers_recus.setReadOnly(True)

        self.historique_logs = QTextEdit()
        self.historique_logs.setReadOnly(True)

        self.quitter = QPushButton("Quitter")

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

        disposition_grille.addWidget(self.quitter, 5, 0, 1, 4)
        self.quitter.clicked.connect(self.quitter_app)

        self.setLayout(disposition_grille)

        self.connecter.clicked.connect(self.connexion_au_serveur)
        self.deconnecter.clicked.connect(self.deconnexion_du_serveur)

        self.selection_fichier.clicked.connect(self.selectionner_fichier)
        self.telecharger.clicked.connect(self.envoyer_fichier)


    def quitter_app(self):
        if self.est_connecte:
            self.deconnexion_du_serveur()
        self.close()




    def connexion_au_serveur(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())

        if self.est_connecte:
            self.historique_logs.append("Déjà connecté au serveur.")
            return
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((ip, port))
            self.est_connecte = True
            self.historique_logs.append(f"Connexion réussie à {ip}:{port}")

        except socket.error as e:
            self.socket_client = None
            self.est_connecte = False
            self.historique_logs.append(f"Erreur de connexion : {e}")
            print(f"Erreur de connexion : {e}")

    def deconnexion_du_serveur(self):
        if self.est_connecte:
            try:
                self.socket_client.close()
                self.est_connecte = False
                self.historique_logs.append("Déconnexion réussie.")
                print("Déconnexion réussie.")
            except Exception as e:
                self.historique_logs.append(f"Erreur lors de la déconnexion : {e}")
                print(f"Erreur lors de la déconnexion : {e}")
        else:
            self.historique_logs.append("Pas de connexion active.")
            print("Pas de connexion active.")

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
            self.historique_logs.append("Erreur : Pas de connexion au serveur.")
            return
        chemin_fichier = self.chemin.text()

        if not chemin_fichier or not os.path.isfile(chemin_fichier):
            self.historique_logs.append("Erreur : Aucun fichier valide sélectionné.")
            return
        try:
            with open(chemin_fichier, 'rb') as f:
                fichier_nom = os.path.basename(chemin_fichier)
                self.socket_client.sendall(fichier_nom.encode('utf-8') + b"\n")

                while (chunk := f.read(1024)):
                    try:
                        self.socket_client.sendall(chunk)
                    except socket.error as e:
                        self.historique_logs.append(f"Erreur d'envoi : {e}")
                        self.est_connecte = False
                        return
                self.socket_client.sendall(b"END")
            self.historique_logs.append(f"Fichier '{chemin_fichier}' envoyé avec succès.")
            self.chemin.clear()
            self.reception_resultat()
        except Exception as e:
            self.historique_logs.append(f"Erreur lors de l'envoi du fichier : {e}")


    def reception_resultat(self):
        try:
            self.socket_client.settimeout(10)  # Définir un délai d'attente
            resultat = b""
            while True:
                data = self.socket_client.recv(1024)
                if not data:
                    raise Exception("Connexion interrompue.")
                resultat += data
                if b"END" in data:
                    resultat = resultat.replace(b"END", b"")
                    break
            self.fichiers_recus.setPlainText(resultat.decode('utf-8'))
            self.historique_logs.append("Résultat reçu et affiché.")
        except socket.timeout:
            self.historique_logs.append("Erreur : Délai d'attente dépassé.")
        except Exception as e:
            self.historique_logs.append(f"Erreur lors de la réception : {e}")


    def closeEvent(self, event):
        if self.est_connecte:
            self.deconnexion_du_serveur()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(800, 500)
    fenetre.show()
    sys.exit(app.exec())
