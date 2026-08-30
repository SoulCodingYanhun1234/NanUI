from PySide6.QtWidgets import QComboBox
from NanUI.utils import get_font

class ComboBox(QComboBox):
    """
    下拉选择框控件。

    继承自 QComboBox，预设了统一字体和主题样式（由 QSS 控制）。
    支持自定义字体、字号和初始选项列表。
    另外添加了 setItems(items) 方法，用于便捷编辑可选择选项。

    Args:
        parent (QWidget, optional): 父控件对象，默认为 None。
        font (str, optional): 字体族名称，若不传则使用全局默认。
        font_size (int): 字体大小（磅值），默认为 12。
        items (list[str], optional): 初始选项列表，默认为空。
        read_only (bool): 是否只读，默认为 True
    """

    def __init__(self, parent = None, font: str = None, font_size: int = 12, items: list = None, read_only: bool = True):
        super().__init__(parent = parent)

        self.setFont(get_font(size = font_size, family = font))
        self.setEditable(not read_only)
        if (items):
            self.setItems(items)

    def setItems(self, items: list = None):
        self.clear()
        self.addItems(items)