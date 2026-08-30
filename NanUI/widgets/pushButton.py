from PySide6.QtWidgets import QPushButton
from NanUI.utils import get_font
from NanUI.utils.theme_manager import apply_themed_shadow

class PushButton(QPushButton):
    """
    按钮控件。

    继承自 QPushButton。可以通过传参的方式调整字体和字体大小。

    Args:
        text (str): 按钮显示的初始文本。默认为空字符串。
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str): 按钮文本的字体。默认为微软雅黑。
        font_size (int): 按钮文本的大小。默认为 12 (px)。
        shadow (bool): 是否添加投影。默认为 True。投影颜色随主题变化，
            取值见 theme_manager.THEME_COLORS 里的 "shadow" 键。
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
        为按钮添加投影。

        颜色交给 theme_manager.apply_themed_shadow()，随主题切换自动更新：
        浅色主题是 #a0a0a4，深色主题是 #000000（深色下投影要压得比所在面更暗）。
        """
        apply_themed_shadow(self)