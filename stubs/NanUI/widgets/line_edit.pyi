from NanUI.utils import get_font as get_font
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QLineEdit, QWidget

class LineEdit(QLineEdit):
    def __init__(self, text: str = '', parent: QWidget | None = None, font: str | None = None, font_size: int = 14, placeholder: str = '') -> None: ...
    def contextMenuEvent(self, event: QContextMenuEvent) -> None: ...
