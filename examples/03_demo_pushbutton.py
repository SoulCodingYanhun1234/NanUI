"""
03 一个按钮。
"""

from NanUI import PushButton, Window
from NanUI.utils import apply_theme

from PySide6.QtWidgets import QApplication, QVBoxLayout


class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口可被鼠标改变大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle("一个按钮")  # 设置窗口标题

        self.btn = PushButton("按钮")  # 定义一个按钮，文本为 '按钮'
        # 给按钮绑定事件，如果按钮被点击，则输出'按钮被点击了！'
        self.btn.clicked.connect(lambda: print("按钮被点击了！"))

        self.mainLayout = QVBoxLayout()  # 定义一个垂直布局
        self.mainLayout.addWidget(self.btn)  # 将按钮加入布局
        self.setLayout(self.mainLayout)  # 将布局 mainLayout 设置为窗口的主布局


if __name__ == "__main__":
    app = QApplication([])
    apply_theme(app, "light")  # 设置主题
    window = MainWindow()
    window.show()
    app.exec()
