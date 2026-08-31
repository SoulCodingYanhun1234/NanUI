from NanUI.utils import get_font as get_font
from PySide6.QtWidgets import QLabel, QWidget
from _typeshed import Incomplete

class Label(QLabel):
    font_size: Incomplete
    font_: Incomplete
    def __init__(self, text: str = '', parent: QWidget | None = None, font: str | None = None, font_size: int = 12) -> None: ...
