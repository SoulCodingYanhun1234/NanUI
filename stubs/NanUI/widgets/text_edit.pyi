from NanUI.utils import get_font as get_font
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QTextEdit, QWidget

class TextEdit(QTextEdit):
    def __init__(self, parent: QWidget | None = None, font: str | None = None, font_size: int = 11, placeholder: str = '') -> None: ...
    def contextMenuEvent(self, event: QContextMenuEvent) -> None: ...
