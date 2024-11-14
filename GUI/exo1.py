import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


class MainWindow(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Première fenêtre")

        # Création du layout
        layout = QVBoxLayout()

        # Ajout des widgets au layout
        layout.addWidget(QLabel("Entrez votre nom :"))
        self.text = QLineEdit()
        self.bouton = QPushButton("ok")
        self.label = QLabel("")
        self.quitter = QPushButton("quitter")

        layout.addWidget(self.text)
        layout.addWidget(self.bouton)
        layout.addWidget(self.label)
        layout.addWidget(self.quitter)

        # Connecter le bouton quitter à la fermeture de l'application
        self.quitter.clicked.connect(QApplication.instance().quit)

        # Connecter le bouton "ok" à la méthode pour afficher le message
        self.bouton.clicked.connect(self.afficher_message)

        # Création d'un widget central pour y ajouter le layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Méthode pour afficher le message de bienvenue
    def afficher_message(self):
        nom = self.text.text()  # Récupère le texte du QLineEdit
        self.label.setText(f"Bonjour {nom}")  # Met à jour le QLabel
        self.text.clear()
        


if __name__ == '__main__':
    # Initialisation de l'application
    app = QApplication(sys.argv)
    fenetre = MainWindow()
    fenetre.resize(300, 200)
    fenetre.show()
    sys.exit(app.exec())
