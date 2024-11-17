import sys, re , socket
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ServerChoiceWindow(QMainWindow):
    from style_server_choice import apply_styles
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configuration du Serveur")
        self.setMinimumSize(800, 500)

        self.configurations = []

        self.ip_label = QLabel("@IP du Serveur:")
        self.ip_input = QLineEdit()
        self.ip_input.setFont(self.font())

        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.port_input.setFont(self.font())

        self.name_label = QLabel("Nom:")
        self.name_input = QLineEdit()
        self.name_input.setFont(self.font())

        self.save_button = QPushButton("Enregistrer")
        self.save_button.setFont(self.font())
        self.save_button.clicked.connect(self.save_configuration)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.ip_label)
        left_layout.addWidget(self.ip_input)
        left_layout.addWidget(self.port_label)
        left_layout.addWidget(self.port_input)
        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.name_input)
        left_layout.addWidget(self.save_button)

        self.config_list = QListWidget()
        self.config_list.setFont(self.font())
        self.config_list.setStyleSheet("font-size: 22px;")

        self.delete_button = QPushButton("Supprimer")
        self.delete_button.setFont(self.font())
        self.delete_button.clicked.connect(self.delete_configuration)

        self.connect_button = QPushButton("Se connecter")
        self.connect_button.setFont(self.font())
        self.connect_button.clicked.connect(self.connect_to_server)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.config_list)
        right_layout.addWidget(self.delete_button)
        right_layout.addWidget(self.connect_button)

        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        right_widget = QWidget()

        left_widget.setLayout(left_layout)
        right_widget.setLayout(right_layout)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)

        self.disconnect_button = QPushButton("Quitter")
        self.disconnect_button.setFont(self.font())
        self.disconnect_button.clicked.connect(self.disconnect)
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.disconnect_button)
        bottom_layout.setAlignment(self.disconnect_button, Qt.AlignBottom)
        main_layout.addLayout(bottom_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.apply_styles()

        self.add_default_configuration()

    

    def save_configuration(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        name = self.name_input.text()

        if not self.is_valid_ip(ip):
            QMessageBox.warning(self, "Erreur", "L'adresse IP saisie est invalide !")
            return
        
        if not self.is_valid_port(port):
            QMessageBox.warning(self, "Erreur", "Le port doit être un nombre entier entre 1 et 65535.")
            return
        
        if not name:
            QMessageBox.warning(self, "Erreur", "Le nom ne peut pas être vide.")
            return

        self.configurations.append((ip, port, name))
        self.config_list.addItem(f"{name} ({ip}:{port})")
        self.ip_input.clear()
        self.port_input.clear()
        self.name_input.clear()

    def connect_to_server(self):
        selected_item = self.config_list.currentItem()
        if selected_item:
            selected_text = selected_item.text()
            name, address = selected_text.split(" (")
            ip, port = address[:-1].split(":")
            QMessageBox.information(self, "Connexion", f"Connexion à {name} ({ip}:{port}) réussie!")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une configuration !")

    def delete_configuration(self):
        selected_item = self.config_list.currentItem()
        if (selected_item):
            row = self.config_list.row(selected_item)
            self.config_list.takeItem(row)
            del self.configurations[row]
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une configuration à supprimer !")

    def disconnect(self):
        self.close()
        open_login()

    def add_default_configuration(self):
        self.configurations.append(("192.168.1.1", "1234", "server-maitre"))
        self.config_list.addItem("server-maitre (192.168.1.1:1234)")

    def is_valid_ip(self, ip):
        regex = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return re.match(regex, ip) is not None

    def is_valid_port(self, port):
        try:
            port = int(port)
            return 1 <= port <= 65535
        except ValueError:
            return False

def open_login():
    from connexion import LoginWindow
    window = LoginWindow()
    window.show()











if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerChoiceWindow()
    window.show()
    sys.exit(app.exec())
