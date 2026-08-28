from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout

class Card(QFrame):
    """
    卡片控件。

    继承自 QFrame。自带圆角和阴影。可设置默认布局。

    Args:
        parent (QWidget, optional): 父控件。
        layout (str): 默认布局类型，'V'为垂直布局，'H'为横向布局，其他表示不添加布局。
    """
    def __init__(self, parent = None, layout: str = 'V'):
        super().__init__(parent)
        self.layout_ = layout

        if (self.layout_ == 'V'):
            self.layout = QVBoxLayout(self)
        elif (self.layout_ == 'H'):
            self.layout = QHBoxLayout(self)
        else: pass
        