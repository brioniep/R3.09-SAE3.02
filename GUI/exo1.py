import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

class MainWindow(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Première fenêtre")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Entrez votre nom :"))
        self.text = QLineEdit()
        self.bouton = QPushButton("ok")
        self.label = QLabel("")
        self.quitter = QPushButton("quitter")

        layout.addWidget(self.text)
        layout.addWidget(self.bouton)
        layout.addWidget(self.label)
        layout.addWidget(self.quitter)

        self.quitter.clicked.connect(QApplication.instance().quit)
        self.bouton.clicked.connect(self.afficher_message)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def afficher_message(self):
        nom = self.text.text()
        self.label.setText(f"Bonjour {nom}")
        self.text.clear()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = MainWindow()
    fenetre.resize(300, 200)
    fenetre.show()
    sys.exit(app.exec())
