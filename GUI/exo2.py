import sys
from PyQt6.QtWidgets import *

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion de température")
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()

        self.label1 = QLabel("Température : ")
        self.input1 = QLineEdit()
        self.label2 = QLabel("°C")

        self.bouton1 = QPushButton("Convertir")
        self.option1 = QComboBox()  
        self.option1.addItems(["°C -> K", "K -> °C"])

        self.label3 = QLabel("Conversion : ")
        self.label4 = QLineEdit("", readOnly=True)
        self.label5 = QLabel("K")

        self.bouton2 = QPushButton("?")

        grid_layout.addWidget(self.label1, 0, 0, 1, 2) 
        grid_layout.addWidget(self.input1, 0, 1)
        grid_layout.addWidget(self.label2, 0, 2)

        grid_layout.addWidget(self.bouton1, 1, 1)
        grid_layout.addWidget(self.option1, 1, 2)

        grid_layout.addWidget(self.label3, 2, 0)
        grid_layout.addWidget(self.label4, 2, 1)
        grid_layout.addWidget(self.label5, 2, 2)

        grid_layout.addWidget(self.bouton2, 3, 3)

        self.option1.currentIndexChanged.connect(self.update_label)
        self.bouton1.clicked.connect(self.conversion)
        self.bouton2.clicked.connect(self.information)

        self.setLayout(grid_layout)

    def update_label(self, index):
        option = self.option1.currentText()
        
        if option == "°C -> K":
            self.label2.setText("°C")
            self.label5.setText("K")
        elif option == "K -> °C":
            self.label2.setText("K")
            self.label5.setText("°C")

    def conversion(self):
        temperature = self.input1.text()
        try:
            temperature = float(temperature)
        except ValueError:
            print("Erreur")
            QMessageBox.about(self, "Erreur", "Veuillez entrer un nombre")
            return

        option = self.option1.currentText()

        if option == 0:
            temperature = 0

        if option == "°C -> K":
            temperature += 273.15
        elif option == "K -> °C":
            temperature -= 273.15

        self.label4.setText(str(temperature))

    def information(self):
        QMessageBox.about(self, "information", "permet de convertir un nombre soit en kelvin vers celcius, soit de celcius vers kelvin")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.resize(300, 200)
    fenetre.show()
    sys.exit(app.exec())
