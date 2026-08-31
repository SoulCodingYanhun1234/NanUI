from typing import Optional

from NanUI.utils import get_font

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLayout, QScrollArea, QVBoxLayout, QWidget


class ScrollArea(QScrollArea):
    """
    可滚动区域控件。

    提供一个带滚动条的可视区域，用于容纳超出显示范围的内容。
    默认自带一个垂直布局，可直接用 addWidget() 添加控件；
    也可以用 setContentLayout() 换入自定义布局。
    样式由 QSS 主题控制，与 NanUI 整体风格保持一致。
    代码由 DeepSeek 网页版提供。

    Args:
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str, optional): 字体族名称。默认为 None，即使用全局默认字体（微软雅黑）。
        font_size (int): 字体大小（磅值）。默认为 12。
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        font: Optional[str] = None,
        font_size: int = 12,
    ) -> None:
        super().__init__(parent)

        # 1. 设置字体（统一管理）
        self.setFont(get_font(size=font_size, family=font))

        # 2. 核心设置：让内容控件可以随滚动区域自动调整大小
        #    这是保证布局能正常工作的关键[reference:10][reference:11]
        self.setWidgetResizable(True)

        # 3. 设置滚动条策略：需要时显示（默认就是，但显式写出更清晰）
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 4. 【可选】设置一个默认的内容容器，方便用户直接添加控件
        #    这样用户就可以像使用普通布局一样使用 ScrollArea
        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self._content_widget)

    # ---------- 便捷方法 ----------
    def setContentLayout(self, layout: QLayout) -> None:
        """
        将外部创建好的布局设置为滚动区域的内容。
        这提供了比默认垂直布局更大的灵活性。
        """
        # 清除原有内容
        old_widget = self.widget()
        if old_widget is not None:
            old_widget.deleteLater()

        # 创建一个新的容器 widget 并应用传入的布局
        container = QWidget()
        container.setLayout(layout)
        self.setWidget(container)
        # 确保内容能自适应大小
        self.setWidgetResizable(True)

    def addWidget(self, widget: QWidget) -> None:
        """向默认的垂直布局中添加控件（便捷方法）"""
        if self._content_layout:
            self._content_layout.addWidget(widget)
        else:
            raise RuntimeError(
                "默认内容布局不存在，请使用 setContentLayout() 自行设置。"
            )
