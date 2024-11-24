import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
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
        self.bonjour = QPushButton("bonjour")
        self.label2 = QLabel("")

        layout.addWidget(self.text)
        layout.addWidget(self.bouton)
        layout.addWidget(self.label)
        layout.addWidget(self.quitter)
        layout.addWidget(self.label2)


        self.quitter.clicked.connect(QApplication.instance().quit)
        self.bouton.clicked.connect(self.afficher_message)
        self.text.returnPressed.connect(self.afficher_message)
        self.bonjour.clicked.connect(self.bienvenue)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def afficher_message(self):
        if self.text.text() == "":
            self.label.setText("Vous n'avez pas entré de nom")
    
        
        else:
            nom = self.text.text()
            self.label.setText(f"Bonjour {nom}")
            self.text.clear()



    def effacer_message(self):
        self.label2.clear()  # Efface le texte du label


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = MainWindow()
    fenetre.resize(300, 200)
    fenetre.show()
    sys.exit(app.exec())





