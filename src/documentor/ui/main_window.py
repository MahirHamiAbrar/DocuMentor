import sys

from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from documentor.ui.widgets import MessageBoxWidget
from documentor.utils import get_ui_file_path, get_ui_stylesheet_path

class AppMainWindow(QMainWindow):
    messageBox: MessageBoxWidget

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self.init_ui()
    
    def init_ui(self) -> None:
        self._ui_fp = get_ui_file_path('main_window_ui.ui')
        self._ui = uic.loadUi(self._ui_fp, self)

        self.messageBox.add_user_message('this is a user text')
        self.messageBox.add_ai_message('this is an AI text')
        self.messageBox.add_user_message('this is a user text')
        self.messageBox.add_ai_message('this is an AI text')
        self.messageBox.add_user_message('this is a user text')


def launch_app() -> None:
    styles = get_ui_stylesheet_path('dark-style.css')
    with open(styles, 'r') as file:
        stylesheet = file.read()
    
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    window = AppMainWindow()
    window.setWindowTitle('DocuMentor-Chat')
    window.resize(1400, 720)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    launch_app()
