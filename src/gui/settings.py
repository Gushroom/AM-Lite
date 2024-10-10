from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        
        # Example setting - placeholder label and close button
        layout.addWidget(QLabel("Settings go here..."))
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
