import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.dashboard import DashboardWindow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

def main():
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
