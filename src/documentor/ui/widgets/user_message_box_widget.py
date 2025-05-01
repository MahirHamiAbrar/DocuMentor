from typing import Callable
from PyQt6 import uic, QtGui, QtCore, QtWidgets

from documentor.ui.widgets.base_widget import BaseWidget
from documentor.utils import get_ui_file_path, get_ui_icon_path


class UserMessageBoxWidget(BaseWidget):
    userMessageContainerFrame: QtWidgets.QFrame
    userMessageTextEdit: QtWidgets.QPlainTextEdit
    userMessageSendBtn: QtWidgets.QPushButton
    userMessageImagesBtn: QtWidgets.QPushButton

    def __init__(self, 
        parent: QtWidgets.QWidget | None = None,
        flags: QtCore.Qt.WindowType | None = None
    ) -> None:
        BaseWidget.__init__(self, parent, flags)

        self._callback: Callable | None = None
        
        # initialize the UI
        self.init_ui()
    
    def set_send_button_callback(self, cb: Callable) -> None:
        assert callable(cb), 'Must be a function!'
        self._callback = cb
    
    def init_ui(self) -> None:
        self.load_ui('user-message-box-widget-ui.ui')
        self.set_button_icon(
            icon_name='icons8-paper-plane-26.png',
            button=self.userMessageSendBtn
        )
        self.set_button_icon(
            icon_name='icons8-photos-96.png',
            button=self.userMessageImagesBtn,
            size=(22, 22)
        )

        self.userMessageSendBtn.clicked.connect(self.send_message)
    
    def send_message(self) -> None:
        if self._callback:
            self._callback(self.userMessageTextEdit.toPlainText())
    

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = UserMessageBoxWidget()
    widget.show()
    sys.exit(app.exec())
