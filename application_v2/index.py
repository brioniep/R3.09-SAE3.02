import sys
import socket
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import time

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

        self.setLayout(disposition_grille)

        self.connecter.clicked.connect(self.connexion_au_serveur)
        self.deconnecter.clicked.connect(self.deconnexion_du_serveur)

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

    def closeEvent(self, event):
        if self.est_connecte:
            self.deconnexion_du_serveur()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(500, 300)
    fenetre.show()
    sys.exit(app.exec())
