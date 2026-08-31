"""
05 一个多行文本框。
"""

from NanUI import Window, TextEdit
from NanUI.utils import apply_theme
from PySide6.QtWidgets import QApplication, QVBoxLayout

class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口可被鼠标调整大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle('一个多行文本框')  # 设置窗口标题

        self.te = TextEdit(placeholder='请输入文本')  # 定义一个多行文本框，占位文本为'请输入文本'
        # 在框内点击右键可以唤出自定义菜单（撤回、重做、剪切、复制、粘贴、删除、全选、清空）
        # 文本内容发生变化时，输出当前的内容
        self.te.textChanged.connect(lambda: print(f'当前文本：{self.te.toPlainText()}'))

        self.mainLayout = QVBoxLayout()  # 定义一个垂直布局
        self.mainLayout.addWidget(self.te)  # 将多行文本框加入布局
        self.setLayout(self.mainLayout)  # 将布局 mainLayout 设置为窗口的主布局

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')  # 设置主题
    window = MainWindow()
    window.show()
    app.exec()
