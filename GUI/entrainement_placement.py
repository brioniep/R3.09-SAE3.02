import sys
from PyQt5.QtWidgets import *

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()  # Appelle le constructeur parent
        self.setWindowTitle("QGridLayout avec une classe")
        self.initUI()  # Méthode pour créer l'interface utilisateur

    def initUI(self):
        # Création du QGridLayout
        grid_layout = QGridLayout()

        # Création des widgets
        self.label1 = QLabel("Température : ")
        self.input1 = QLineEdit()
        self.label2 = QLabel("°C")

        self.bouton1 = QPushButton("Convertir")
        self.option1 = QComboBox()  # Utilisation de self.option1
        self.option1.addItems(["°C -> K", "K -> °C"])

        self.label3 = QLabel("Conversion : ")
        self.label4 = QLabel("0")
        self.label5 = QLabel("K")

        self.bouton2 = QPushButton("?")

        # Ajout des widgets dans le QGridLayout
        grid_layout.addWidget(self.label1, 0, 0)
        grid_layout.addWidget(self.input1, 0, 1)
        grid_layout.addWidget(self.label2, 0, 2)

        grid_layout.addWidget(self.bouton1, 1, 1)
        grid_layout.addWidget(self.option1, 1, 2)

        grid_layout.addWidget(self.label3, 2, 0)
        grid_layout.addWidget(self.label4, 2, 1)
        grid_layout.addWidget(self.label5, 2, 2)

        grid_layout.addWidget(self.bouton2, 3, 3)

        # Connexion du signal currentIndexChanged à la méthode de conversion
        self.option1.currentIndexChanged.connect(self.update_label)
        self.bouton1.clicked.connect(self.conversion)

        # Appliquer le layout à la fenêtre
        self.setLayout(grid_layout)

    def update_label(self, index):
        # Récupérer l'option sélectionnée
        option = self.option1.currentText()
        
        # Logique de mise à jour de label2 en fonction de l'option choisie
        if option == "°C -> K":
            self.label2.setText("°C")
            self.label5.setText("K")
        elif option == "K -> °C":
            self.label2.setText("K")
            self.label5.setText("°C")



    def conversion(self):
        # Récupérer la température
        temperature = self.input1.text()
        try:
            temperature = float(temperature)
        except ValueError:
            self.label4.setText("Erreur")
            return

        # Récupérer l'option sélectionnée
        option = self.option1.currentText()

        if option == 0:
            temperature = 0

        # Logique de conversion
        if option == "°C -> K":
            temperature += 273.15
        elif option == "K -> °C":
            temperature -= 273.15







        # Mettre à jour le label4
        self.label4.setText(str(temperature))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(300, 200)
    fenetre.show()
    sys.exit(app.exec_())
