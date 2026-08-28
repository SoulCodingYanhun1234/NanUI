from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from NanUI.utils import get_font
from PySide6.QtCore import Qt

class PushButton(QPushButton):
    """
    按钮控件。

    继承自 QPushButton。可以通过传参的方式调整字体和字体大小。

    Args:
        text (str): 按钮显示的初始文本。默认为空字符串。
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str): 按钮文本的字体。默认为微软雅黑。
        font_size (int): 按钮文本的大小。默认为 12 (px)。
    """

    def __init__(self, text: str = '', parent = None, font: str = None, font_size: int = 12, shadow: bool = True):
        super().__init__(text, parent)

        self.font_, self.font_size = font, font_size

        # self.setFont(QFont(self.font_, self.font_size))
        self.setFont(get_font(size=self.font_size, family=self.font_))

        if shadow:
            self._add_shadow()

    def _add_shadow(self):
        """
        为按钮添加阴影。
        此方法代码由 DeepSeek 网页版提供。
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setOffset(0, 1)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)