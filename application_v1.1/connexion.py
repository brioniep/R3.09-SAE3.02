import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from server_choice import ServerChoiceWindow

class LoginWindow(QWidget):
    from style_connexion import apply_styles
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page de Connexion")
        self.setMinimumSize(600, 400)

        self.user_label = QLabel("Identifiant:")
        self.user_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.user_input = QLineEdit()
        self.user_input.setFont(self.font())

        self.pass_label = QLabel("Mot de passe:")
        self.pass_label.setStyleSheet("font-²size: 24px; font-weight: bold;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFont(self.font())

        self.login_button = QPushButton("Connexion")
        self.login_button.setFont(self.font())
        self.login_button.clicked.connect(self.check_login)

        self.error_label = QLabel("Identification incorrecte")
        self.error_label.setStyleSheet("color: red; font-size: 20px; font-weight: bold;")
        self.error_label.setVisible(False)

        layout = QVBoxLayout()
        layout.setContentsMargins(80, 40, 80, 40)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
        self.apply_styles()

        self.error_timer = QTimer()
        self.error_timer.setSingleShot(True)
        self.error_timer.timeout.connect(self.hide_error_message)

    
    def check_login(self):
        username = "toto"
        password = "toto"

        if self.user_input.text() == username and self.pass_input.text() == password:
            self.open_server_config()
        else:
            self.show_error_message()

    def show_error_message(self):
        self.error_label.setVisible(True)
        self.error_timer.start(5000)

    def hide_error_message(self):
        self.error_label.setVisible(False)

    def open_server_config(self):
        self.server_config_window = ServerChoiceWindow()
        self.server_config_window.show()
        self.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.isMaximized():
            self.setGeometry(0, 0, QApplication.primaryScreen().availableGeometry().width(), QApplication.primaryScreen().availableGeometry().height())
        else:
            self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
