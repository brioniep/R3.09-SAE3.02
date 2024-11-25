from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
import os
import socket

class IndexWindow(QMainWindow):
    disconnect_signal = pyqtSignal()  # Signal pour revenir à la fenêtre précédente

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page d'Envoi de Fichier")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        # Zone pour afficher le chemin du fichier
        self.file_path_display = QLineEdit()
        self.file_path_display.setPlaceholderText("Aucun fichier sélectionné")
        self.file_path_display.setReadOnly(True)

        # Bouton pour sélectionner un fichier
        self.select_file_button = QPushButton("Sélectionner un fichier")
        self.select_file_button.clicked.connect(self.select_file)

        # Bouton pour envoyer le fichier
        self.send_file_button = QPushButton("Envoyer le fichier")
        self.send_file_button.setEnabled(False)  # Désactivé par défaut jusqu'à ce qu'un fichier soit sélectionné
        self.send_file_button.clicked.connect(self.send_file)

        # Label pour afficher le statut de l'envoi
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 16px; color: gray;")

        # Bouton pour déconnexion
        self.disconnect_button = QPushButton("Déconnecter")
        self.disconnect_button.clicked.connect(self.disconnect)

        # Ajouter les widgets au layout
        layout.addWidget(self.file_path_display)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.send_file_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.disconnect_button)

        # Créer le conteneur principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Attribut pour le chemin du fichier sélectionné
        self.file_path = None

    def select_file(self):
        """Ouvre un dialogue pour sélectionner un fichier et affiche le chemin."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier")
        if file_path:
            self.file_path = file_path
            self.file_path_display.setText(file_path)
            self.send_file_button.setEnabled(True)  # Activer le bouton d'envoi
            self.status_label.setText("")  # Réinitialiser le statut

    def send_file(self):
        """Envoie le fichier au serveur."""
        if not self.file_path:
            self.status_label.setText("Aucun fichier sélectionné.")
            self.status_label.setStyleSheet("font-size: 16px; color: red;")
            return

        try:
            # Connexion au serveur
            server_address = ('192.168.1.14', 12345)  # Adresse et port du serveur
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(server_address)

                # Envoi du nom du fichier
                filename = os.path.basename(self.file_path)
                s.send(filename.encode())
                response = s.recv(1024)  # Attendre confirmation du nom
                print(response.decode())

                # Envoi de la taille du fichier
                filesize = os.path.getsize(self.file_path)
                s.send(str(filesize).encode())
                response = s.recv(1024)  # Attendre confirmation de la taille
                print(response.decode())

                # Envoi des données du fichier
                with open(self.file_path, 'rb') as f:
                    while (data := f.read(1024)):
                        s.send(data)

                # Attente de la réponse et du fichier résultat
                response = s.recv(1024).decode()
                if response == "file_result":
                    with open("compilation_result.txt", 'wb') as f:
                        data = s.recv(1024)
                        while data:
                            f.write(data)
                            data = s.recv(1024)

                    self.status_label.setText("Résultat de l'exécution disponible sous 'compilation_result.txt'.")
                    self.status_label.setStyleSheet("font-size: 16px; color: green;")

        except Exception as e:
            self.status_label.setText(f"Erreur lors de l'envoi : {str(e)}")
            self.status_label.setStyleSheet("font-size: 16px; color: red;")

    def disconnect(self):
        """Émettre un signal pour revenir à la fenêtre de connexion."""
        self.disconnect_signal.emit()  # Émettre le signal pour retourner à la fenêtre précédente


if __name__ == "__main__":
    app = QApplication([])
    window = IndexWindow()
    window.show()
    app.exec_()
