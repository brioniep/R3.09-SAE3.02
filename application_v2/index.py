import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout avec une classe")
        self.client_socket = None  # Variable de classe pour la socket
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()

        # Zone de gauche
        self.ip = QLabel("@IP srv: ")
        self.ip_input = QLineEdit("192.168.1.11")
        self.port = QLabel("Port: ")
        self.port_input = QLineEdit("1234")
        self.connect = QPushButton("Connexion")
        self.deconnect = QPushButton("Déconnexion")

        #Zone de droite
        self.file_select = QPushButton("select file")
        self.upload = QPushButton("upload")
        self.chemin = QLineEdit()
        self.received_files = QTextEdit()
        self.received_files.setReadOnly(True)  # Rend la zone de texte non modifiable par l'utilisateur

        # Zone de gauche
        self.log_history = QTextEdit()
        self.log_history.setReadOnly(True)  # Rend la zone de texte non modifiable par l'utilisateur
        grid_layout.addWidget(self.ip, 0, 0)
        grid_layout.addWidget(self.ip_input, 0, 1)
        grid_layout.addWidget(self.port, 1, 0)
        grid_layout.addWidget(self.port_input, 1, 1)
        grid_layout.addWidget(self.connect, 2, 0, 1, 2)
        grid_layout.addWidget(self.log_history, 3, 0, 1, 2)  # Zone pour les logs
        grid_layout.addWidget(self.deconnect, 4, 0, 1, 2)

        # Zone de droite
        grid_layout.addWidget(self.file_select, 0, 2)
        grid_layout.addWidget(self.upload, 0, 3)
        grid_layout.addWidget(self.chemin, 1, 2, 1, 2)
        grid_layout.addWidget(self.received_files, 2, 2, 3, 2)  # Zone pour les fichiers reçus

        self.setLayout(grid_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(500, 300)  # Ajustez la taille de la fenêtre selon vos besoins
    fenetre.show()
    sys.exit(app.exec())
