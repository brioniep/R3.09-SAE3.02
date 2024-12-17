import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphique PyQtGraph - Donuts")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)

        self.categories = ['Server 1', 'Server 2', 'Server 3', 'Server 4']  # Noms des serveurs
        self.colors = [(255, 215, 0), (135, 206, 250), (240, 128, 128), (144, 238, 144)]
        self.donuts = []
        self.text_items = []  # Texte pour le pourcentage au centre du donut
        self.server_text_items = []  # Texte pour le nom du serveur sous le donut
        self.target_values = [0] * len(self.categories)
        self.current_values = [0] * len(self.categories)
        self.contours = []  # Liste pour les contours des donuts
        self.inner_contours = []  # Liste pour les contours intérieurs des donuts

        self.initialize_plot()

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_donuts)
        self.animation_timer.start(50)

    def initialize_plot(self):
        # Fond blanc
        self.plot_widget.setBackground("w")

        # Espacement encore plus grand pour les donuts
        x_positions = np.linspace(-3.5, 3.5, len(self.categories))  # Plage plus large

        # Créer chaque donut (cercles) et leur valeur associée
        for i, color in enumerate(self.colors):
            donut = pg.PlotDataItem(pen=pg.mkPen(color=color, width=10))  # Réduire l'épaisseur du bord du donut
            self.plot_widget.addItem(donut)
            self.donuts.append(donut)

            # Ajouter un contour visible pour chaque donut (cercles de contour)
            contour = pg.PlotDataItem(pen=pg.mkPen(color=(0, 0, 0), width=3))  # Couleur noire pour les contours
            self.plot_widget.addItem(contour)
            self.contours.append(contour)

            # Ajouter un contour intérieur pour chaque donut, collé au bord de la couleur
            inner_contour = pg.PlotDataItem(pen=pg.mkPen(color=color, width=3))  # Contour intérieur avec la même couleur que le donut
            self.plot_widget.addItem(inner_contour)
            self.inner_contours.append(inner_contour)

            # Ajout du texte pour le pourcentage au centre du donut
            text_item = pg.TextItem(text="0%", anchor=(0.5, 0.5), color="black")  # Positionner le texte au centre
            self.plot_widget.addItem(text_item)
            self.text_items.append(text_item)

            # Ajouter le texte pour le nom du serveur sous chaque donut
            server_text_item = pg.TextItem(text=self.categories[i], anchor=(0.5, 0), color="black")  # Positionner le texte en dessous
            self.plot_widget.addItem(server_text_item)
            self.server_text_items.append(server_text_item)

            # Positionner les donuts et les textes
            donut.setPos(x_positions[i], 0)
            text_item.setPos(x_positions[i], 0)  # Positionner le texte au centre du donut
            server_text_item.setPos(x_positions[i], -1.5)  # Positionner le texte du serveur sous le donut

            # Positionner les contours
            contour.setPos(x_positions[i], 0)
            inner_contour.setPos(x_positions[i], 0)  # Positionner également le contour intérieur

        self.plot_widget.setTitle("Graphique PyQtGraph - Donuts")
        self.plot_widget.setAspectLocked(True)
        self.plot_widget.setXRange(-4, 4)  # Plage horizontale encore plus large
        self.plot_widget.setYRange(-2, 2)  # Plage verticale pour laisser de l'espace

        # Désactiver les axes
        self.plot_widget.getAxis('bottom').setVisible(False)
        self.plot_widget.getAxis('left').setVisible(False)

        self.update_data()

    def update_data(self):
        # Mettre à jour les valeurs cibles (entre 5 et 100)
        self.target_values = [random.randint(5, 100) for _ in self.categories]

    def animate_donuts(self):
        # Animer l'augmentation des valeurs des donuts
        for i, (donut, contour, inner_contour, target) in enumerate(zip(self.donuts, self.contours, self.inner_contours, self.target_values)):
            self.current_values[i] += (target - self.current_values[i]) * 0.1
            self.update_donut(i, self.current_values[i])
            # Mettre à jour le texte au centre de chaque donut (avec pourcentage)
            self.text_items[i].setText(f"{int(self.current_values[i])}%")  # Afficher la valeur en pourcentage

            # Dessiner les contours du donut et du contour intérieur
            self.update_contour(i)
            self.update_inner_contour(i)

    def update_donut(self, index, value):
        # Calculer l'angle et les coordonnées pour chaque donut
        angle = np.linspace(0, 2 * np.pi * value / 100, 100)
        x = np.cos(angle) * 0.8  # Taille fixe pour tous les donuts
        y = np.sin(angle) * 0.8  # Taille fixe pour tous les donuts
        self.donuts[index].setData(x, y)

    def update_contour(self, index):
        # Créer un cercle pour le contour visible du donut
        angle = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(angle)  # Contour avec rayon 1 pour le donut
        y = np.sin(angle)
        self.contours[index].setData(x, y)

    def update_inner_contour(self, index):
        # Créer un cercle pour le contour intérieur (le trou du donut) exactement collé à la couleur
        angle = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(angle) * 0.8  # Le même rayon que le donut
        y = np.sin(angle) * 0.8  # Le même rayon que le donut
        self.inner_contours[index].setData(x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
