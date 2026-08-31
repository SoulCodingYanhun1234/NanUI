"""
07 两个单选按钮。
"""

from NanUI import Window, RadioButton
from NanUI.utils import apply_theme
from PySide6.QtWidgets import QApplication, QVBoxLayout

class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口可被鼠标调整大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle('两个单选按钮')  # 设置窗口标题

        # 放进同一个布局后它们会有同一个父控件，因此自动互斥，选中一个就会取消另一个
        self.rbtn1 = RadioButton('选项1', checked=True)  # 定义一个单选按钮，默认选中
        self.rbtn2 = RadioButton('选项2')  # 定义第二个单选按钮
        # 选中状态发生变化时，输出哪个选项当前是选中的
        self.rbtn1.toggled.connect(lambda checked: print(f'选项1 被选中：{checked}'))
        self.rbtn2.toggled.connect(lambda checked: print(f'选项2 被选中：{checked}'))

        self.mainLayout = QVBoxLayout()  # 定义一个垂直布局
        self.mainLayout.addWidget(self.rbtn1)  # 将第一个单选按钮加入布局
        self.mainLayout.addWidget(self.rbtn2)  # 将第二个单选按钮加入布局
        self.setLayout(self.mainLayout)  # 将布局 mainLayout 设置为窗口的主布局

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')  # 设置主题
    window = MainWindow()
    window.show()
    app.exec()
