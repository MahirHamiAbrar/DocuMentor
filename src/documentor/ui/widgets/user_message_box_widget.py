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
        
        # initialize the UI
        self.init_ui()
    
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
    

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = UserMessageBoxWidget()
    widget.show()
    sys.exit(app.exec())
