from PyQt6 import QtGui, QtCore, QtWidgets
from documentor.ui.widgets.base_widget import BaseWidget


class HistoryWidget(BaseWidget):
    historyWidgetTitleLabel: QtWidgets.QLabel
    historyWidgetChatList: QtWidgets.QListWidget
    historyWidgetNewChatBtn: QtWidgets.QPushButton

    def __init__(self, 
        parent: QtWidgets.QWidget | None = None,
        flags: QtCore.Qt.WindowType | None = None
    ) -> None:
        BaseWidget.__init__(self, parent, flags)
        
        # initialize the UI
        self.init_ui()

        self.historyWidgetNewChatBtn.clicked.connect(
            lambda: self.add_to_chats('chat-X (NEW)')
        )
    
    def init_ui(self) -> None:
        self.load_ui('history-widget-ui.ui')
        self.set_button_icon(
            icon_name='icons8-plus-math-30.png',
            button=self.historyWidgetNewChatBtn
        )

        # clear list widget
        self.historyWidgetChatList.clear()
    
    def add_to_chats(self, chat_name: str) -> int:
        self.historyWidgetChatList.addItem(chat_name)
        
        chat_id = self.historyWidgetChatList.count() - 1
        self.historyWidgetChatList.setCurrentItem(
            self.historyWidgetChatList.item(chat_id)
        )
        
        return chat_id
    
    def remove_chat(self, chat_id: str) -> None:
        self.historyWidgetChatList.removeItemWidget(
            self.historyWidgetChatList.item(chat_id)
        )
    

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = HistoryWidget()
    widget.show()
    sys.exit(app.exec())
