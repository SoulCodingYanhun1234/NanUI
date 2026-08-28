from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from NanUI.utils import get_font

class Label(QLabel):
    """
    按钮控件。

    继承自 QPushButton。预设了圆角、悬停/按下/禁用样式，并可自定义字体和大小。

    Args:
        text (str): 按钮显示的初始文本。默认为空字符串。
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str): 按钮文本的字体。默认为微软雅黑。
        font_size (int): 按钮文本的大小。默认为 12 (px)。
    """

    def __init__(self, text: str = '', parent = None, font: str = None, font_size: int = 12):
        super().__init__(text, parent)

        self.font_size = font_size
        self.font_ = font

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(get_font(size=font_size, family = font))
