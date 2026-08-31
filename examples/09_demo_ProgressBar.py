"""
09 一个进度条。
"""

from NanUI import ProgressBar, Window
from NanUI.utils import apply_theme

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QVBoxLayout


class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)  # 设置窗口可被鼠标调整大小
        self.resize(700, 500)  # 设置窗口尺寸
        self.setTitle("一个进度条")  # 设置窗口标题

        self.pgBar = ProgressBar(value=0)  # 定义一个进度条，初始值为 0，范围默认 0~100
        # 用定时器每 100 毫秒把进度加 1，用来演示 setValue() 的效果
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._addProgress)
        self.timer.start()

        self.mainLayout = QVBoxLayout()  # 定义一个垂直布局
        self.mainLayout.addWidget(self.pgBar)  # 将进度条加入布局
        self.setLayout(self.mainLayout)  # 将布局 mainLayout 设置为窗口的主布局

    def _addProgress(self):
        """每次被定时器触发时把进度加 1，跑满之后停掉定时器。"""
        self.pgBar.setValue(self.pgBar.value() + 1)
        if self.pgBar.value() >= self.pgBar.maximum():
            self.timer.stop()
            print("进度跑满了！")


if __name__ == "__main__":
    app = QApplication([])
    apply_theme(app, "light")  # 设置主题
    window = MainWindow()
    window.show()
    app.exec()
