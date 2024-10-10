from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
from utils.task_creator import create_task 

class CreateTaskDialog(QDialog):
    task_created = pyqtSignal()  # Signal to refresh task list in the main window

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Task")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()

        # Task Name
        self.name_label = QLabel("Task Name")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Task Code
        self.code_label = QLabel("Task Script")
        self.code_input = QTextEdit()
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_input)

        # Submit Button
        self.submit_button = QPushButton("Create Task")
        self.submit_button.clicked.connect(self.create_task)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def create_task(self):
        task_name = self.name_input.text().strip()
        code_content = self.code_input.toPlainText().strip()
        
        if not task_name or not code_content:
            QMessageBox.warning(self, "Input Error", "Please fill in both fields.")
            return

        # Create the task in the backend
        create_task(task_name, code_content)
        
        QMessageBox.information(self, "Task Created", f"Task '{task_name}' has been created.")
        self.task_created.emit()  # Emit signal to refresh task list
        self.close()
