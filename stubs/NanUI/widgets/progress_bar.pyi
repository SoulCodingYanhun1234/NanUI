from NanUI.utils import get_font as get_font
from PySide6.QtWidgets import QProgressBar, QWidget

class ProgressBar(QProgressBar):
    def __init__(self, parent: QWidget | None = None, font: str | None = None, font_size: int = 12, minimum: int = 0, maximum: int = 100, value: int = 0, format: str = '%p%') -> None: ...
