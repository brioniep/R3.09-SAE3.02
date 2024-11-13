import sys
from PyQt6.QtWidgets import QApplication, QWidget
app = QApplication(sys.argv)
root = QWidget()
root.resize(350, 200)
root.setWindowTitle("Une première fenetre !")





root.show()
if __name__ == '__main__':
 sys.exit(app.exec())