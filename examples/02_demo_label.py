"""
02 一个标签。
"""

from NanUI import Label, Window
from NanUI.utils import apply_theme

from PySide6.QtWidgets import QApplication, QVBoxLayout


class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口可调整大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle("一个标签")  # 设置窗口标题

        self.lb = Label("标签")  # 定义一个标签，设置文本为'标签'
        self.mainLayout = QVBoxLayout()  # 创建一个垂直布局
        self.mainLayout.addWidget(self.lb)  # 将标签添加进布局
        self.setLayout(self.mainLayout)  # 将布局设置为窗口的主布局


if __name__ == "__main__":
    app = QApplication([])
    apply_theme(app, "light")  # 设置主题
    window = MainWindow()
    window.show()
    app.exec()
