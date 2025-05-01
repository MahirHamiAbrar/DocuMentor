from PyQt6 import uic, QtGui, QtCore, QtWidgets

from documentor.ui.widgets.base_widget import BaseWidget
from documentor.ui.widgets.ai_message_widget import AIMessageWidget
from documentor.ui.widgets.user_message_widget import UserMessageWidget


class MessageBoxWidget(BaseWidget):
    msgScrollArea: QtWidgets.QScrollArea
    scrollAreaWidgetContents: QtWidgets.QWidget
    msgScrollVerticalLayout: QtWidgets.QVBoxLayout

    def __init__(self, 
        parent: QtWidgets.QWidget | None = None,
        flags: QtCore.Qt.WindowType | None = None
    ) -> None:
        BaseWidget.__init__(self, parent, flags)
        
        # initialize the UI
        self.init_ui()
    
    def init_ui(self) -> None:
        self.load_ui('message-box-ui.ui')
    
    def add_user_message(self, text: str) -> None:
        msg = UserMessageWidget(self)
        msg.set_text(text)
        self.msgScrollVerticalLayout.addWidget(msg)
    
    def add_ai_message(self, text: str) -> None:
        msg = AIMessageWidget(self)
        msg.set_text(text)
        self.msgScrollVerticalLayout.addWidget(msg)
    

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MessageBoxWidget()
    widget.add_user_message('this is a user text')
    widget.add_ai_message('this is an AI text')
    widget.show()
    sys.exit(app.exec())
