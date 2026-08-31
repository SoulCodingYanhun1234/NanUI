from typing import Optional

from NanUI.utils import get_font

from PySide6.QtWidgets import QCheckBox, QWidget


class CheckBox(QCheckBox):
    """
    复选框控件。

    继承自 QCheckBox。预设了统一字体和主题样式（由 QSS 主题控制）。
    支持自定义字体、字号和初始选中状态；重写了 toggle()，方便在代码里手动切换选中状态。

    Args:
        text (str): 复选框旁显示的文本。默认为空字符串。
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str, optional): 字体族名称。默认为 None，即使用全局默认字体（微软雅黑）。
        font_size (int): 字体大小（磅值）。默认为 14。
        checked (bool): 是否在创建时处于选中状态。默认为 False。
    """

    def __init__(
        self,
        text: str = "",
        parent: Optional[QWidget] = None,
        font: Optional[str] = None,
        font_size: int = 14,
        checked: bool = False,
    ) -> None:
        super().__init__(text, parent)

        self.setFont(get_font(size=font_size, family=font))
        self.setChecked(checked)

    def toggle(self) -> None:
        self.setChecked(not self.isChecked())
