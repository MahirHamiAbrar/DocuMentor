from typing import Tuple
from PyQt6 import uic, QtGui, QtCore, QtWidgets
from documentor.utils import get_ui_file_path, get_ui_icon_path


class BaseWidget(QtWidgets.QWidget):

    def __init__(self, 
        parent: QtWidgets.QWidget | None = None,
        flags: QtCore.Qt.WindowType | None = None
    ) -> None:
        if flags:
            super().__init__(parent, flags)
        else:
            QtWidgets.QWidget.__init__(self, parent)
    
    def load_ui(self, ui_file_name: str) -> None:
        self._ui_fp = get_ui_file_path(ui_file_name)
        self._ui = uic.loadUi(self._ui_fp, self)
    
    def set_button_icon(self,
        icon_name: str,
        button: QtWidgets.QPushButton,
        size: Tuple | None = None,
        clear_text: bool = False
    ) -> QtGui.QIcon:
        
        if clear_text:
            button.setText('')
        
        icon = QtGui.QIcon(
            get_ui_icon_path(icon_name)
        )
        button.setIcon(icon)

        if size:
            button.setIconSize(QtCore.QSize(size[0], size[1]))

        return icon
