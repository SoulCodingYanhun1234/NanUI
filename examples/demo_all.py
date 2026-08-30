"""
演示所有 NanUI 支持的控件。
"""

from NanUI import Window, Label, PushButton, LineEdit, TextEdit, CheckBox, RadioButton, ComboBox, ProgressBar, Card, ScrollArea
from NanUI.utils.theme_manager import apply_theme
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout
from NanUI.resources import resources_rc

class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)
        self.resize(1050, 700)
        self.setTitle('NanUI 测试窗口')

        self.lbTest = Label('Label 控件测试')
        self.btnTest = PushButton('PushButton 控件测试')
        self.leTest = LineEdit(placeholder='LineEdit 控件测试')
        self.teTest = TextEdit(placeholder='TextEdit 控件测试')
        self.cbTest = CheckBox('CheckBox 控件测试')
        self.rbtnTest = RadioButton('RadioButton 控件测试1', checked=True)
        self.rbtnTest1 = RadioButton('RadioButton 控件测试2')
        self.cbbTest = ComboBox()
        self.cbbTest.addItems(['选项1', '选项2', '选项3'])
        self.pgBarTest = ProgressBar(value=90)

        self.cardTest = Card(layout='H')
        self.cardLbTest = Label('Card 容器测试')
        self.cardBtnTest = PushButton('Card 容器测试')
        self.cardTest.layout.addWidget(self.cardLbTest)
        self.cardTest.layout.addWidget(self.cardBtnTest)

        self.saTest = ScrollArea()
        self.saLayout = QVBoxLayout()
        for i in range(10):
            self.saLayout.addWidget(PushButton(f'ScrollArea 容器测试{i+1}'))
        self.saLayout.addStretch()
        self.saTest.setContentLayout(self.saLayout)

        self.subLayout = QHBoxLayout()
        self.subLayout.addWidget(self.cbTest)
        self.subLayout.addWidget(self.rbtnTest)
        self.subLayout.addWidget(self.rbtnTest1)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.lbTest)
        self.mainLayout.addWidget(self.btnTest)
        self.mainLayout.addWidget(self.leTest)
        self.mainLayout.addWidget(self.teTest)
        self.mainLayout.addLayout(self.subLayout)
        self.mainLayout.addWidget(self.cbbTest)
        self.mainLayout.addWidget(self.pgBarTest)
        self.mainLayout.addWidget(self.cardTest)
        self.mainLayout.addWidget(self.saTest)

        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')
    window = MainWindow()
    window.show()
    app.exec()