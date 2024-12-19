from PyQt6.QtGui import QFont, QColor, QPalette

def apply_stylesheet(app):
    # Set the font
    font = QFont("Arial", 10)
    app.setFont(font)

    # Set the palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    # Set the stylesheet
    stylesheet = """
    QWidget {
        background-color: #f0f0f0;
    }
    QLabel {
        font-size: 12px;
        color: #333;
    }
    QLineEdit {
        border: 1px solid #ccc;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton {
        background-color: #0078d7;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }
    QPushButton:disabled {
        background-color: #cccccc;
    }
    QTextEdit {
        border: 1px solid #ccc;
        padding: 5px;
        border-radius: 3px;
    }
    QMessageBox {
        background-color: #f0f0f0;
    }
    """
    app.setStyleSheet(stylesheet)