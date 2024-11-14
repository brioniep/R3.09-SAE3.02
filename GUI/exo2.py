import sys
from PyQt6.QtWidgets import *
class MainWindow(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertion de Température")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Température :"))
        self.text = QLineEdit()
        self.label = QLabel("°C")
        self.bouton = QPushButton("convertir")
        self.combo = QComboBox()
        self.label = QLabel("")

        self.combo.addItems(["°C -> K", "F -> °C"])

        layout.addWidget(self.combo)
        layout.addWidget(self.text)
        layout.addWidget(self.bouton)
        layout.addWidget(self.label)
        layout.addWidget(self.combo)






        self.bouton.setStyleSheet("background-color: lightblue; color: black; font-weight: bold;")
        self.text.setStyleSheet("border: 1px solid gray; padding: 5px; font-size: 14px;")



        


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)




    def convertisseur(self,)->float:


        if self.text.text() == "":
            self.label.setText("Vous n'avez pas entré de température")

        elif self.text.text() != float:
            self.label.setText("Erreur ! Veuillez entrer un nombre")
        


        if self.combo.currentText() == "°C -> K":
            temperature = float(self.text.text())
            temperature += 273.15

            self.label.setText(f"{temperature} K")

        elif self.combo.currentText() == "F -> °C":
            temperature = float(self.text.text())
            temperature = (temperature - 32) * 5/9

            self.label.setText(f"{temperature} °C")

        

def main():
    app = QApplication(sys.argv)
    fenetre = MainWindow()
    fenetre.resize(300, 200)
    fenetre.show()
    sys.exit(app.exec())
        
if __name__ == '__main__':
    main()





