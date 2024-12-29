def style_connexion(widget):

    dark_style = """
        QWidget {
            background-color: #2b2b2b;
            color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        QLabel {
            font-size: 18px;
        }
        QLineEdit {
            background-color: #3c3c3c;
            color: #f0f0f0;
            border: 1px solid #5c5c5c;
            border-radius: 4px;
            padding: 6px;
        }
        QPushButton {
            background-color: #3c3c3c;
            color: #f0f0f0;
            border: 1px solid #5c5c5c;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #4c4c4c;
        }
        QPushButton:pressed {
            background-color: #2c2c2c;
        }
        QLabel#error_label {
            color: #e74c3c;
        }
    """
    widget.setStyleSheet(dark_style)





def style_index(widget):

    dark_style = """
        QWidget {
            background-color: #1e1e1e;
            color: #e0e0e0;
            font-family: Arial, sans-serif;
        }
        QLabel {
            font-size: 16px;
        }
        QLineEdit {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 6px;
        }
        QPushButton {
            background-color: #0066cc; /* Couleur vive : bleu */
            color: #ffffff;
            border: 2px solid #004080;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* Ombre pour le relief */
        }
        QPushButton:hover {
            background-color: #0088ff; /* Bleu plus clair au survol */
            border: 2px solid #0059b3;
        }
        QPushButton:pressed {
            background-color: #004080; /* Bleu plus sombre lors du clic */
            box-shadow: none; /* Suppression de l'ombre pour simuler une pression */
        }
        QPushButton#quitter {
            background-color: #e74c3c; /* Rouge vif pour Quitter */
            border: 2px solid #c0392b;
        }
        QPushButton#quitter:hover {
            background-color: #ff6f61; /* Rouge plus clair au survol */
            border: 2px solid #d64030;
        }
        QPushButton#quitter:pressed {
            background-color: #b8322a; /* Rouge plus sombre lors du clic */
        }
        QTextEdit {
            background-color: #292929;
            color: #d0d0d0;
            border: 1px solid #444444;
            border-radius: 4px;
            padding: 4px;
        }
        QTextEdit[readOnly="true"] {
            background-color: #3a3a3a;
            border: 1px solid #555555;
            color: #aaaaaa;
        }
        QMessageBox {
            background-color: #1e1e1e;
            color: #e0e0e0;
        }
        QScrollBar:vertical {
            background: #1e1e1e;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #555555;
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            border: none;
        }
    """
    widget.setStyleSheet(dark_style)
