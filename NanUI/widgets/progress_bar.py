from typing import Optional

from NanUI.utils import get_font

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressBar, QWidget


class ProgressBar(QProgressBar):
    """
    进度条控件。

    继承自 QProgressBar。预设了统一字体和主题样式（由 QSS 主题控制）。
    支持自定义范围、初始值和显示格式。

    Args:
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str, optional): 字体族名称。默认为 None，即使用全局默认字体（微软雅黑）。
        font_size (int): 字体大小（磅值）。默认为 12。
        minimum (int): 最小值。默认为 0。
        maximum (int): 最大值。默认为 100。
        value (int): 初始值。默认为 0。
        format (str): 显示格式。默认为 "%p%"（显示百分比）。
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        font: Optional[str] = None,
        font_size: int = 12,
        minimum: int = 0,
        maximum: int = 100,
        value: int = 0,
        format: str = "%p%",
    ) -> None:
        super().__init__(parent)

        self.setFont(get_font(size=font_size, family=font))

        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setFormat(format)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
