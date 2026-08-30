"""
08 一个下拉选择框。
"""

from NanUI import Window, ComboBox
from NanUI.utils.theme_manager import apply_theme
from PySide6.QtWidgets import QApplication, QVBoxLayout

class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口可被鼠标调整大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle('一个下拉选择框')  # 设置窗口标题

        self.cbb = ComboBox(items=['选项1', '选项2', '选项3'])  # 定义一个下拉选择框，并传入初始选项
        # 选中项发生变化时，输出当前选中的文本
        self.cbb.currentTextChanged.connect(lambda text: print(f'当前选中：{text}'))
        # 想整组换掉选项可以用 setItems()，例如 self.cbb.setItems(['甲', '乙', '丙'])
        # 默认 read_only=True，只能从列表里选；传 read_only=False 就变成可以直接输入的组合框

        self.mainLayout = QVBoxLayout()  # 定义一个垂直布局
        self.mainLayout.addWidget(self.cbb)  # 将下拉选择框加入布局
        self.setLayout(self.mainLayout)  # 将布局 mainLayout 设置为窗口的主布局

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')  # 设置主题
    window = MainWindow()
    window.show()
    app.exec()
