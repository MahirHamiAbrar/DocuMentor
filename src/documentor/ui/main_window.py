import sys

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from PyQt6.uic.load_ui import loadUi


class AppMainWindow(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)


def launch_app() -> None:
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec())
