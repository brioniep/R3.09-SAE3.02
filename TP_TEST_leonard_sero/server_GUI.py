
import sys, socket, threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


# https://github.com/brioniep/tp_test_leonard_sero

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Le serveur de chat")
        self.client_socket = None  
        self.initUI()


    def initUI(self):
        # Création du QGridLayout
        grid_layout = QGridLayout()

        # Création des widgets
        self.ip = QLabel("@IP srv: ")
        self.ip_input = QLineEdit("0.0.0.0")

        self.port = QLabel("Port: ")
        self.port_input = QLineEdit("4200")

        self.nombre_clients = QLabel("Nombre de client maximum : ")
        self.nombre_client_input = QLineEdit("5")

        self.connect = QPushButton("Démarrage du serveur")

        # Zone d'affichage de l'historique des messages
        self.history = QTextEdit()
        self.history.setReadOnly(True)

        self.quitter = QPushButton("Quitter")

        grid_layout.addWidget(self.ip, 0, 0)
        grid_layout.addWidget(self.ip_input, 0, 1)
        grid_layout.addWidget(self.port, 1, 0)
        grid_layout.addWidget(self.port_input, 1, 1)
        grid_layout.addWidget(self.nombre_clients, 2, 0)
        grid_layout.addWidget(self.nombre_client_input, 2, 1)
        grid_layout.addWidget(self.connect, 3, 0, 1, 2)

        grid_layout.addWidget(self.history, 4, 0, 1, 2)

        grid_layout.addWidget(self.quitter, 5, 0, 1, 2)

        self.quitter.clicked.connect(QApplication.instance().quit)
        self.connect.clicked.connect(self.demmarrage_thread)
        self.setLayout(grid_layout)


    def demmarrage_thread(self,):
        t1 = threading.Thread(target=self.demarrage)
        t1.start()


    def demarrage(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr_ip = self.ip_input.text()
        port_srv = int(self.port_input.text())
        nb_clients = int(self.nombre_client_input.text())

        server_socket.bind((addr_ip, port_srv)) 
        server_socket.listen(nb_clients)
        self.connect.setText("Arret du serveur")
        


 
        while True: # L'affichage des messages ne se fait que dans le terminal, pas réussit a l'afficher dans l'interface graphique
        

            """if self.connect.clicked.connect():   # Ce if permet de fermer le serveur si le bouton connect est presser
                conn.close()                          mais il est commenté car il ne marche pas...
                server_socket.close()
            else:"""

            try:
                conn, address = server_socket.accept()  
                print(f"Client connecté")

                while True:
                    message = conn.recv(1024).decode()

                    if not message:
                        break

                    print(f"Message reçu : {message}")

                    if message.lower() == "deco-server":
                        print("Fermeture du serveur...")
                        conn.close()
                        server_socket.close()
                        return
                    if message == "bye":
                        print("Le client a été déconnecté")
                        break
            except OSError as e:
                print(f"Socket error: {e}")
                break




if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(350, 400) 
    fenetre.show()
    sys.exit(app.exec())
