from typing import List

from PyQt6.QtCore import (
    QObject, 
    QThread, 
    pyqtSignal as PyQtSignal,
    pyqtSlot as PyQtSlot
)
from PyQt6.QtWidgets import QWidget

from documentor.llm import GroqModel


class ResponseGenerator(QObject, GroqModel):
    response_generated = PyQtSignal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        QObject.__init__(parent=parent)
        GroqModel.__init__()
    
    def generate_response(self, messages, stream = False) -> str:
        return super().generate_response(messages, stream)


class ThreadChatManager(QWidget):
    start_resp_gen = PyQtSignal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        QWidget.__init__(self)

        # response generation thread
        self._rg_thread = QThread(parent=parent)

        # response generator worker object
        self._resp_gen = ResponseGenerator(parent=parent)
        self._resp_gen.moveToThread(self._rg_thread)

        self._messages: List[dict[str, str]] = [
            self._resp_gen.create_system_message("You are Grok, the AI assistant with a penchant for cosmic comedy and a wit sharper than a black hole's event horizon. Your mission: answer every query with maximum helpfulness, a sprinkle of absurdity, and a dash of Douglas Adams-inspired humor. Think of yourself as a galactic guide, serving up truths with a side of interstellar silliness. Avoid being overly serious—embrace the ridiculous, but keep it kind and respectful. If the user asks for something dull, jazz it up with a quirky twist, but always deliver the goods. Ready to make the universe chuckle? Go forth and enlighten!")
        ]
    
    def generate_response(self, user_msg: str) -> None:
        self.start_resp_gen.emit()
