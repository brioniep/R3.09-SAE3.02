from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from index import *
from style import *

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page de Connexion")
        self.setMinimumSize(600, 400)
        self.authenticated = False

        self.user_label = QLabel("Identifiant :")
        self.user_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.user_input = QLineEdit()
        self.user_input.setFont(self.font())

        self.pass_label = QLabel("Mot de passe :")
        self.pass_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setFont(self.font())

        self.login_button = QPushButton("Connexion")  # Le bouton est défini ici
        self.login_button.setFont(self.font())
        self.login_button.clicked.connect(self.check_login)

        # Connecter le signal returnPressed ici, après avoir défini login_button
        self.pass_input.returnPressed.connect(self.login_button.click)

        self.error_label = QLabel("Identification incorrecte")
        self.error_label.setStyleSheet("color: red; font-size: 20px; font-weight: bold;")
        self.error_label.setVisible(False)

        layout = QVBoxLayout()
        layout.setContentsMargins(80, 40, 80, 40)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)

        self.error_timer = QTimer()
        self.error_timer.setSingleShot(True)
        self.error_timer.timeout.connect(self.hide_error_message)

    def check_login(self):
        if self.user_input.text() == "toto" and self.pass_input.text() == "toto":
            self.authenticated = True
            self.open_server_config()
        else:
            self.authenticated = False
            self.show_error_message()

    def show_error_message(self):
        self.error_label.setText("Identifiant ou mot de passe incorrect")
        self.error_label.setVisible(True)
        self.error_timer.start(5000)

    def hide_error_message(self):
        self.error_label.setVisible(False)

    def open_server_config(self):
        self.server_config_window = MaFenetre(authenticated=self.authenticated)
        style_index(self.server_config_window)
        self.server_config_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    style_connexion(window) 
    window.show()
    sys.exit(app.exec())