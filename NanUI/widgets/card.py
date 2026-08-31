from typing import Optional

from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget


class Card(QFrame):
    """
    卡片控件。

    继承自 QFrame。自带圆角样式（由 QSS 主题控制），并可指定默认布局。

    Args:
        parent (QWidget, optional): 父控件对象。默认为 None。
        layout (str): 默认布局类型。'V' 为垂直布局，'H' 为横向布局，
            其他值表示不添加布局。默认为 'V'。
    """

    def __init__(self, parent: Optional[QWidget] = None, layout: str = "V") -> None:
        super().__init__(parent)
        self.layout_ = layout
        self.setObjectName("card")

        if self.layout_ == "V":
            self.layout = QVBoxLayout(self)
        elif self.layout_ == "H":
            self.layout = QHBoxLayout(self)
        else:
            pass
