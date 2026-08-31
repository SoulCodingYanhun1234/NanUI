"""
06 一个复选框。
"""

from NanUI import Window, CheckBox
from NanUI.utils import apply_theme
from PySide6.QtWidgets import QApplication, QVBoxLayout

class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口可被鼠标调整大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle('一个复选框')  # 设置窗口标题

        self.cb = CheckBox('复选框')  # 定义一个复选框，文本为'复选框'
        # 选中状态发生变化时，输出当前是否被选中
        self.cb.toggled.connect(lambda checked: print(f'复选框被选中：{checked}'))
        # 也可以在代码里用 toggle() 手动切换选中状态，例如 self.cb.toggle()

        self.mainLayout = QVBoxLayout()  # 定义一个垂直布局
        self.mainLayout.addWidget(self.cb)  # 将复选框加入布局
        self.setLayout(self.mainLayout)  # 将布局 mainLayout 设置为窗口的主布局

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')  # 设置主题
    window = MainWindow()
    window.show()
    app.exec()
