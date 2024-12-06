from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QThread, QObject
import os
import socket

class MonitorConnectionWorker(QObject):
    """Un worker pour surveiller la connexion au serveur"""
    connection_lost = pyqtSignal()  # Émet lorsque la connexion est perdue

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self._running = True

    def stop(self):
        """Arrêter la surveillance de la connexion"""
        self._running = False

    def monitor_connection(self):
        """Surveille la connexion et émet un signal si la connexion est perdue"""
        while self._running:
            try:
                self.client_socket.send(b"ping")  # Envoie un "ping" pour tester la connexion
                self.client_socket.recv(1024)  # Attendre une réponse
            except (socket.error, socket.timeout):
                self.connection_lost.emit()  # Émettre un signal si la connexion est perdue
                break

class IndexWindow(QMainWindow):
    disconnect_signal = pyqtSignal()  # Signal pour revenir à la fenêtre précédente

    def __init__(self, client_socket=None):
        super().__init__()
        self.setWindowTitle("Page d'Envoi de Fichier")
        self.setMinimumSize(600, 400)

        self.client_socket = client_socket  # Conserver la socket si elle est passée
        if not self.client_socket:
            self.status_label.setText("Pas de connexion au serveur.")
            return

        layout = QVBoxLayout()
        self.file_path_display = QLineEdit()
        self.file_path_display.setPlaceholderText("Aucun fichier sélectionné")
        self.file_path_display.setReadOnly(True)

        self.select_file_button = QPushButton("Sélectionner un fichier")
        self.select_file_button.clicked.connect(self.select_file)

        self.send_file_button = QPushButton("Envoyer le fichier")
        self.send_file_button.setEnabled(False)
        self.send_file_button.clicked.connect(self.send_file)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 16px; color: gray;")

        self.disconnect_button = QPushButton("Déconnecter")
        self.disconnect_button.clicked.connect(self.disconnect)

        layout.addWidget(self.file_path_display)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.send_file_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.disconnect_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.file_path = None

        # Lancer la surveillance de la connexion
        self.monitor_thread = QThread()
        self.monitor_worker = MonitorConnectionWorker(self.client_socket)
        self.monitor_worker.moveToThread(self.monitor_thread)
        self.monitor_worker.connection_lost.connect(self.on_connection_lost)

        self.monitor_thread.started.connect(self.monitor_worker.monitor_connection)
        self.monitor_thread.start()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier")
        if file_path:
            self.file_path = file_path
            self.file_path_display.setText(file_path)
            self.send_file_button.setEnabled(True)
            self.status_label.setText("")

    def send_file(self):
        if not self.file_path:
            self.status_label.setText("Aucun fichier sélectionné.")
            self.status_label.setStyleSheet("font-size: 16px; color: red;")
            return

        if not self.client_socket:
            self.status_label.setText("Erreur : Pas de connexion serveur.")
            return

        try:
            filename = os.path.basename(self.file_path)
            self.client_socket.send(filename.encode())
            response = self.client_socket.recv(1024)
            print(response.decode())

            filesize = os.path.getsize(self.file_path)
            self.client_socket.send(str(filesize).encode())
            response = self.client_socket.recv(1024)
            print(response.decode())

            with open(self.file_path, 'rb') as f:
                while (data := f.read(1024)):
                    self.client_socket.send(data)

            response = self.client_socket.recv(1024).decode()
            if response == "file_result":
                with open("compilation_result.txt", 'wb') as f:
                    data = self.client_socket.recv(1024)
                    while data:
                        f.write(data)
                        data = self.client_socket.recv(1024)

                self.status_label.setText("Résultat de l'exécution disponible sous 'compilation_result.txt'.")
                self.status_label.setStyleSheet("font-size: 16px; color: green;")

        except Exception as e:
            self.status_label.setText(f"Erreur lors de l'envoi : {str(e)}")
            self.status_label.setStyleSheet("font-size: 16px; color: red;")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.disconnect_signal.emit()
        self.close()

    def on_connection_lost(self):
        """Lorsque la connexion est perdue, fermer la fenêtre"""
        self.status_label.setText("Connexion au serveur perdue.")
        self.status_label.setStyleSheet("font-size: 16px; color: red;")
        self.close()
