from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from NanUI.utils import get_font

class Label(QLabel):
    """
    标签控件。

    继承自 QLabel。预设了圆角样式（由 QSS 主题控制），并可自定义字体和字号。

    Args:
        text (str): 标签上显示的文本。默认为空字符串。
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str, optional): 字体族名称。默认为 None，即使用全局默认字体（微软雅黑）。
        font_size (int): 字体大小（磅值）。默认为 12。
    """

    def __init__(self, text: str = '', parent = None, font: str = None, font_size: int = 12):
        super().__init__(text, parent)

        self.font_size = font_size
        self.font_ = font

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(get_font(size=font_size, family = font))
