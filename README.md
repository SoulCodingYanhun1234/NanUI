# NanUI

> 一个基于 PySide6 的简单、美观的 UI 库。

[![GitHub license](https://img.shields.io/github/license/NanbeiTnT/NanUI)](LICENSE)
[![Python version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PySide6 version](https://img.shields.io/badge/PySide6-6.5.0%2B-blue)](https://doc.qt.io/qtforpython-6/)

注：该UI库还处于超超超超早期开发阶段！

## 简介

NanUI 是一套基于 PySide6 的轻量级 UI 库，专为想要快速开发界面美观的 Windows 软件的人们提供。
它提供了一套最基础的控件的美化，你可以通过修改 styles 文件夹下的 QSS 文件或者添加主题来自定义窗口的样式。

> 注：本项目部分代码由 DeepSeek 网页端和 TraeCode-cn 协助完成，项目源代码里所有由它们编写的文件/类/函数等均有提示。

## 安装方法

首先，请先保证电脑上拥有 Python 的 3.8 或以上版本，建议使用虚拟环境测试。

### 1. 使用 pip 安装

目前 NanUI 还没有上传到 PyPI，在命令行运行这行代码

```base
pip install git+https://github.com/NanbeiTnT/NanUI.git
```

来安装。

### 2. 从源码安装

```bash
git clone https://github.com/NanbeiTnT/NanUI.git
cd NanUI
pip install -e .
```

## 快速开始

你可以使用下面这段代码，来测试 NanUI 里的控件。

```py
from NanUI import Window, Label, PushButton, LineEdit, TextEdit, CheckBox, RadioButton, ComboBox, ProgressBar, Card
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

        self.frameTest = Card(layout='H')
        self.frameLbTest = Label('Frame 容器测试')
        self.frameBtnTest = PushButton('Frame 容器测试')
        self.frameTest.layout.addWidget(self.frameLbTest)
        self.frameTest.layout.addWidget(self.frameBtnTest)

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
        self.mainLayout.addWidget(self.frameTest)

        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    app = QApplication([])
    apply_theme(app, 'light')
    window = MainWindow()
    window.show()
    app.exec()
```

这段代码也可以在库的 tests 文件夹里找到。

## 已实现控件列表

- **Window**: 无边框圆角窗口（可拖动/调整大小 ✅
- **Label**: 圆角标签（透明背景/自适应字体） ✅
- **PushButton**: 圆角按钮（悬停/按下/禁用状态） ✅
- **LineEdit**: 单行输入框（圆角/焦点高亮） ✅
- **TextEdit**: 多行文本框（自定义右键菜单） ✅
- **CheckBox**: 复选框（自定义指示器图标） ✅
- **RadioButton**: 单选按钮（实心圆点风格） ✅
- **ComboBox**: 下拉选择框（圆角/自定义箭头） ✅
- **ProgressBar**: 进度条（药丸风格渐变） ✅

## 主题切换

NanUI 支持切换主题（虽然现在只内置了一个 light 主题），你可以在启动时指定：

```py
from NanUI.utils import apply_theme

# 亮色主题（默认）
apply_theme(app, "light")
```

你也可以在 styles 文件夹里添加自己的 QSS 文件。

## 项目结构

```plain
NanUI/
├── NanUI/                  # 源代码
│   ├── widgets/            # 控件类
│   ├── styles/             # QSS 样式表
│   ├── utils/              # 工具函数（字体、主题管理）
│   └── resources/          # 图片资源（可选）
├── tests/                  # 测试示例
├── setup.py                # 安装脚本
├── LICENSE                 # 许可证
└── README.md
```

## 许可证

本项目采用 MIT 许可证，你可以自由使用、修改、分发，包括商业用途。