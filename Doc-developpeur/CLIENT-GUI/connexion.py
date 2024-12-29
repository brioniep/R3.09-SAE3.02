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

        self.login_button = QPushButton("Connexion") 
        self.login_button.setFont(self.font())
        self.login_button.clicked.connect(self.verifier_connexion)

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
        self.error_timer.timeout.connect(self.cacher_message_erreur)


    def verifier_connexion(self):
        """
        Vérifie les identifiants saisis par l'utilisateur et déclenche les actions correspondantes.

        Variables :
            user_input (QLineEdit) : Champ de saisie pour le nom d'utilisateur.
            pass_input (QLineEdit) : Champ de saisie pour le mot de passe.
            authenticated (bool) : Indique si l'utilisateur est authentifié après la vérification.
        """
        if self.user_input.text() == "toto" and self.pass_input.text() == "toto":
            self.authenticated = True
            self.ouvrir_config_serveur()
        else:
            self.authenticated = False
            self.afficher_message_erreur()


    def afficher_message_erreur(self):
        """
        Affiche un message d'erreur lorsque l'authentification échoue.

        Variables :
            error_label (QLabel) : Label utilisé pour afficher le message d'erreur.
            error_timer (QTimer) : Timer qui contrôle la durée d'affichage du message d'erreur.
        """
        self.error_label.setText("Identifiant ou mot de passe incorrect")
        self.error_label.setVisible(True)
        self.error_timer.start(5000)


    def cacher_message_erreur(self):
        """
        Cache le message d'erreur affiché.

        Variables :
            error_label (QLabel) : Label utilisé pour afficher le message d'erreur.
        """
        self.error_label.setVisible(False)


    def ouvrir_config_serveur(self):
        """
        Ouvre la fenêtre d'envoie de fichier au serveur après authentification.

        Variables :
            server_config_window (MaFenetre) : Nouvelle fenêtre de configuration du serveur.
            authenticated (bool) : Indique si l'utilisateur est authentifié pour initialiser la fenêtre.
        
        Méthodes appelées :
            style_index(window) : Applique un style à la fenêtre de configuration.
        """
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