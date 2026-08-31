from typing import Optional

from NanUI.utils import get_font
from NanUI.utils.theme_manager import apply_themed_shadow

from PySide6.QtWidgets import QPushButton, QWidget


class PushButton(QPushButton):
    """
    按钮控件。

    继承自 QPushButton。预设了圆角样式（由 QSS 主题控制），并可自定义字体和字号。

    Args:
        text (str): 按钮上显示的文本。默认为空字符串。
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str, optional): 字体族名称。默认为 None，即使用全局默认字体（微软雅黑）。
        font_size (int): 字体大小（磅值）。默认为 12。
        shadow (bool): 是否添加投影。默认为 True。投影颜色随主题变化，
            取值见 theme_manager.THEME_COLORS 里的 "shadow" 键。
    """

    def __init__(
        self,
        text: str = "",
        parent: Optional[QWidget] = None,
        font: Optional[str] = None,
        font_size: int = 12,
        shadow: bool = True,
    ) -> None:
        super().__init__(text, parent)

        self.font_, self.font_size = font, font_size

        # self.setFont(QFont(self.font_, self.font_size))
        self.setFont(get_font(size=self.font_size, family=self.font_))

        if shadow:
            self._add_shadow()

    def _add_shadow(self) -> None:
        """
        为按钮添加投影。

        颜色交给 theme_manager.apply_themed_shadow()，随主题切换自动更新：
        浅色主题是 #a0a0a4，深色主题是 #000000（深色下投影要压得比所在面更暗）。
        """
        apply_themed_shadow(self)
