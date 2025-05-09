import sys
from typing import List

from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from documentor.llm import GroqModel
from documentor.ui.widgets import (
    HistoryWidget,

    MessageBoxWidget,
    UserMessageBoxWidget,
    
    AIMessageWidget,
)
from documentor.utils import get_ui_file_path, get_ui_stylesheet_path


class ResponseGenerator(QObject):
    progress = pyqtSignal(str)
    completed = pyqtSignal(bool)

    @pyqtSlot(str)
    def generate_response(self,
        llm: GroqModel,
        messages: List[dict[str, str]],
        stream: bool = False
    ) -> None:
        llm.generate_response(messages, stream)
        self.completed.emit(True)
        

class AppMainWindow(QMainWindow):
    historyWidget: HistoryWidget
    messageView: MessageBoxWidget
    userMessageBox: UserMessageBoxWidget

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self._messages: List[dict[str, str]] = [] 
        self._current_ai_msg_widget: AIMessageWidget | None = None
        
        self._llm = GroqModel()
        self._llm.stream_callback_function = self.stream_callback

        self._worker = ResponseGenerator()
        self._worker_thread = QThread()

        self._worker.completed.connect(
            lambda: print('Done!')
        )
        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.start()

        self.init_ui()
    
    def init_ui(self) -> None:
        self._ui_fp = get_ui_file_path('main_window_ui.ui')
        self._ui = uic.loadUi(self._ui_fp, self)
        
        # set callback functions
        self.userMessageBox.set_send_button_callback(
            self.send_user_message
        )

        self._messages.append(
            self._llm.create_system_message(
                "You are a funny AI assistant who creatively insults the users in such a way that they find it amusing!"
            )
        )
    
    def stream_callback(self, chunk: str) -> None:
        if not self._current_ai_msg_widget:
            self._current_ai_msg_widget = self.messageView.add_ai_message(chunk)
        else:
            self._current_ai_msg_widget.append_text(chunk)
    
    def send_user_message(self, message_text: str) -> None:
        self._current_ai_msg_widget = None
        self.messageView.add_user_message(message_text)

        user_msg = self._llm.create_user_message(message_text)
        self._messages.append(user_msg)

        self._worker.generate_response(
            self._llm,
            self._messages,
            True
        )


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
