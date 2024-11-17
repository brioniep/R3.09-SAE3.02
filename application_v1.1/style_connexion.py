def apply_styles(self):
        self.setStyleSheet("""
            background-color: #2E3440;
            color: #D8DEE9;
            font-family: Arial;
        """)

        input_style = """
            background-color: #3B4252;
            border: 1px solid #4C566A;
            padding: 15px;
            border-radius: 6px;
            color: #D8DEE9;
            font-size: 22px;
            max-width: 400px;
        """
        self.user_input.setFixedHeight(50)
        self.user_input.setStyleSheet(input_style)
        
        self.pass_input.setFixedHeight(50)
        self.pass_input.setStyleSheet(input_style)

        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                padding: 18px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 22px;
                max-width: 400px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #4C566A;
            }
        """)
