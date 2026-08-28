from PySide6.QtWidgets import QRadioButton
from NanUI.utils import get_font

class RadioButton(QRadioButton):
    """
    单选按钮控件。

    继承自 QRadioButton。预设了统一字体和主题样式（由 QSS 控制）。
    支持自定义字体、字号和初始选中状态。
    添加了 toggle() 用于便捷切换选中状态。

    Args:
        text(str): 控件里显示的文本。
        parent(QWidget, optional): 父控件。
        font(str): 字体。
        font_size(int): 字体大小。
        checked(bool): 是否被选中。
    """
    def __init__(self, text: str = '', parent = None, font: str = None, font_size: int = 14, checked: bool = False):
        super().__init__(text, parent)

        self.setFont(get_font(size=font_size, family=font))
        self.setChecked(checked)

    def toggle(self):
        self.setChecked(not self.isChecked())