from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QListWidget, QLabel,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from .settings import SettingsWindow
from .create_task_dialog import CreateTaskDialog
from utils.task_runner import run_task
from utils.models import session, RPATask

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPA Task Dashboard")
        self.setGeometry(100, 100, 500, 400)

        # Central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Title or Header
        self.header_label = QLabel("RPA Task Dashboard")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.header_label)
        
        # Task List Area
        self.task_list = QListWidget()
        self.populate_task_list()
        main_layout.addWidget(self.task_list)
        
        # Display a message if no tasks are available
        if self.task_list.count() == 0:
            self.no_tasks_message = QLabel("No RPA tasks available.")
            self.no_tasks_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(self.no_tasks_message)

        # Buttons area
        buttons_layout = QHBoxLayout()

        # Create New Task button
        self.create_task_button = QPushButton("Create New Task")
        self.create_task_button.clicked.connect(self.open_create_task_dialog)
        buttons_layout.addWidget(self.create_task_button)

        # Run Task button
        self.run_task_button = QPushButton("Run Selected Task")
        self.run_task_button.clicked.connect(self.run_selected_task)
        buttons_layout.addWidget(self.run_task_button)

        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        buttons_layout.addWidget(self.settings_button)

        main_layout.addLayout(buttons_layout)
        self.setCentralWidget(central_widget)

    def populate_task_list(self):
        self.task_list.clear()
        tasks = session.query(RPATask).all()
        if tasks:
            for task in tasks:
                self.task_list.addItem(task.name)
            if hasattr(self, 'no_tasks_message'):
                self.no_tasks_message.hide()
        else:
            if hasattr(self, 'no_tasks_message'):
                self.no_tasks_message.show()

    def open_create_task_dialog(self):
        self.create_task_dialog = CreateTaskDialog(self)
        self.create_task_dialog.task_created.connect(self.populate_task_list)
        self.create_task_dialog.show()

    def run_selected_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_name = selected_item.text()
            task = session.query(RPATask).filter_by(name=task_name).first()
            if task:
                run_task(task.id)  # Execute the backend function to run the task
                QMessageBox.information(self, "Task Execution", f"Task '{task.name}' has been executed.")
            else:
                QMessageBox.warning(self, "Error", "Selected task not found.")
        else:
            QMessageBox.warning(self, "Error", "No task selected.")

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
