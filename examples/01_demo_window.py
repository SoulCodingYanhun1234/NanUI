"""
01 一个基础的窗口。
"""

from NanUI import Window
from NanUI.utils.theme_manager import apply_theme
from PySide6.QtWidgets import QApplication

class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口是否可被鼠标调整大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle('这是一个窗口')  # 设置窗口标题

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')  # 设置主题，不加这行代码 QSS 不生效
    window = MainWindow()
    window.show()
    app.exec()