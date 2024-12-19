import sys
import socket
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import re
import time

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client PyQt6 - Connexion au Serveur")
        self.socket_client = None
        self.initUI()

    def initUI(self):
        disposition_grille = QGridLayout()

        self.port = QLabel("Port client: ")
        self.port_input = QLineEdit("1234")
        self.demarrer = QPushButton("Démarrer")

        self.chemin = QLineEdit()
        self.chemin.setReadOnly(True)
        self.fichiers_recus = QTextEdit()
        self.fichiers_recus.setReadOnly(True)

        self.historique_logs = QTextEdit()
        self.historique_logs.setReadOnly(True)

        self.quitter = QPushButton("Quitter")

        disposition_grille.addWidget(self.port, 1, 0)
        disposition_grille.addWidget(self.port_input, 1, 1)
        disposition_grille.addWidget(self.demmarrer, 2, 0, 1, 2)
        disposition_grille.addWidget(self.historique_logs, 3, 0, 1, 2)

        disposition_grille.addWidget(self.chemin, 1, 2, 1, 2)
        disposition_grille.addWidget(self.fichiers_recus, 2, 2, 3, 2)

        disposition_grille.addWidget(self.quitter, 5, 0, 1, 4)

        self.setLayout(disposition_grille)





   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(800, 500)
    fenetre.show()
    sys.exit(app.exec())