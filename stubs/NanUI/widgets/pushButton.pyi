from NanUI.utils import get_font as get_font
from NanUI.utils.theme_manager import apply_themed_shadow as apply_themed_shadow
from PySide6.QtWidgets import QPushButton, QWidget

class PushButton(QPushButton):
    def __init__(self, text: str = '', parent: QWidget | None = None, font: str | None = None, font_size: int = 12, shadow: bool = True) -> None: ...
