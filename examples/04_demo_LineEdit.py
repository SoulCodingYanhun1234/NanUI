"""
一个单行输入框。
"""

from NanUI import Window, LineEdit
from NanUI.utils.theme_manager import apply_theme
from PySide6.QtWidgets import QApplication, QVBoxLayout

class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)
        self.resize(700, 500)
        self.setTitle('单行输入框')

        self.le = LineEdit(placeholder='请输入文本')  # 定义一个单行输入框，占位文本为'请输入文本'
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.le)
        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')
    window = MainWindow()
    window.show()
    app.exec()