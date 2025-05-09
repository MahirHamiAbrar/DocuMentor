from PyQt6 import uic, QtGui, QtCore, QtWidgets
from documentor.ui.widgets.base_widget import BaseWidget


class AIMessageWidget(BaseWidget):
    textEdit: QtWidgets.QPlainTextEdit

    def __init__(self,
        parent: QtWidgets.QWidget | None = None,
        flags: QtCore.Qt.WindowType | None = None
    ) -> None:
        BaseWidget.__init__(self, parent, flags)
        
        # initialize the UI
        self.init_ui()
    
    def init_ui(self) -> None:
        self.load_ui('ai-message-widget-ui.ui')
        self.textEdit.setMinimumHeight(100)
    
    def clear_text(self) -> str:
        self.textEdit.clear()
    
    def current_text(self) -> str:
        return self.textEdit.toPlainText()
    
    def set_text(self, text: str) -> None:
        self.textEdit.setPlainText(text)
    
    def append_text(self, text: str) -> None:
        self.textEdit.setPlainText(
            self.textEdit.toPlainText() + text
        )


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = AIMessageWidget()
    widget.show()
    sys.exit(app.exec())
