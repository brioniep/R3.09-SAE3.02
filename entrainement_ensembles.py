import sys
import socket
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QGridLayout
from PyQt6.QtCore import pyqtSignal, QObject


class Communicate(QObject):
    update_info = pyqtSignal(str)  # Signal pour mettre à jour l'information de connexion
    update_history = pyqtSignal(str)  # Signal pour mettre à jour l'historique des messages


class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout avec une classe")
        self.client_socket = None  # Variable de classe pour la socket
        self.comm = Communicate()  # Instance pour les signaux

        self.initUI()

        # Connecter les signaux aux méthodes
        self.comm.update_info.connect(self.set_info)
        self.comm.update_history.connect(self.add_to_history)

    def initUI(self):
        # Création du QGridLayout
        grid_layout = QGridLayout()

        # Création des widgets
        self.ip = QLabel("@IP srv: ")
        self.ip_input = QLineEdit("127.0.0.1")
        self.port = QLabel("Port: ")
        self.port_input = QLineEdit("12345")
        self.connect = QPushButton("Connexion")
        self.info = QLabel("En attente de connexion")

        # Zone d'affichage de l'historique des messages
        self.history = QTextEdit()
        self.history.setReadOnly(True)  # Rend la zone de texte non modifiable par l'utilisateur

        self.msg = QLabel("Message : ")
        self.message = QLineEdit()
        self.envoyer = QPushButton("Envoyer")
        self.nettoyer = QPushButton("Nettoyer")
        self.quitter = QPushButton("Quitter")

        grid_layout.addWidget(self.ip, 0, 0)
        grid_layout.addWidget(self.ip_input, 0, 1)
        grid_layout.addWidget(self.port, 1, 0)
        grid_layout.addWidget(self.port_input, 1, 1)
        grid_layout.addWidget(self.connect, 2, 0, 1, 2)
        grid_layout.addWidget(self.info, 3, 0, 1, 2)

        grid_layout.addWidget(self.history, 0, 2, 4, 2)  # Zone pour l'historique

        grid_layout.addWidget(self.msg, 4, 0)
        grid_layout.addWidget(self.message, 4, 1)
        grid_layout.addWidget(self.envoyer, 4, 2, 1, 2)
        grid_layout.addWidget(self.nettoyer, 5, 2)
        grid_layout.addWidget(self.quitter, 5, 3)

        self.quitter.clicked.connect(QApplication.instance().quit)
        self.connect.clicked.connect(self.connexion_thread)
        self.envoyer.clicked.connect(self.envoie_msg_thread)
        self.nettoyer.clicked.connect(self.history.clear)

        self.setLayout(grid_layout)

    def connexion_thread(self):
        t1 = threading.Thread(target=self.connexion)
        t1.start()

    def envoie_msg_thread(self):
        t2 = threading.Thread(target=self.envoie_msg)
        t2.start()

    def connexion(self):
        ip = self.ip_input.text()
        try:
            port = int(self.port_input.text())  # Convertit la chaîne en entier
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))  # Utilise un tuple (ip, port)
            self.comm.update_info.emit("Connexion réussie")

            # Démarrer un thread pour écouter les messages du serveur
            listen_thread = threading.Thread(target=self.ecouter_messages)
            listen_thread.daemon = True  # Permet au thread de se terminer avec l'application
            listen_thread.start()
        except ValueError:
            self.comm.update_info.emit("Port invalide : veuillez entrer un nombre entier.")
        except Exception as e:
            self.comm.update_info.emit(f"Erreur de connexion : {str(e)}")
            self.comm.update_history.emit(f"Erreur : {str(e)}")

    def envoie_msg(self):
        if self.client_socket:
            message = self.message.text()
            try:
                self.client_socket.send(message.encode())
                self.comm.update_history.emit(f"Envoyé : {message}")  # Met à jour l'historique
                self.message.clear()  # Efface le champ de saisie
            except Exception as e:
                self.comm.update_info.emit(f"Erreur d'envoi : {str(e)}")
                self.comm.update_history.emit(f"Erreur d'envoi : {str(e)}")
        else:
            self.comm.update_info.emit("Veuillez d'abord vous connecter au serveur.")
            self.comm.update_history.emit("Tentative d'envoi sans connexion.")

    def ecouter_messages(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode()
                if not response:
                    break  # Déconnexion du serveur
                self.comm.update_history.emit(f"Reçu : {response}")
            except Exception as e:
                self.comm.update_history.emit(f"Erreur de réception : {str(e)}")
                break

    # Méthodes connectées aux signaux pour mettre à jour l'interface graphique
    def set_info(self, text):
        self.info.setText(text)

    def add_to_history(self, text):
        self.history.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(500, 300)  # Ajustez la taille de la fenêtre selon vos besoins
    fenetre.show()
    sys.exit(app.exec())
