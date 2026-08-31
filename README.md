# NanUI

> 一个基于 PySide6 的轻量级 UI 库，帮你快速搭建美观的 Windows 桌面界面。

[![GitHub license](https://img.shields.io/github/license/NanbeiTnT/NanUI)](LICENSE)
[![Python version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PySide6 version](https://img.shields.io/badge/PySide6-6.5.0%2B-blue)](https://doc.qt.io/qtforpython-6/)

> 该库仍处于早期开发阶段，API 可能在后续版本中调整。

## 特性

- **11 个开箱即用的基础控件**：Window、Label、PushButton、LineEdit、TextEdit、CheckBox、RadioButton、ComboBox、ProgressBar、Card、ScrollArea
- **双主题**：内置浅色（light）与深色（dark），启动时指定，运行时也可随时切换
- **纯 QSS 定制**：控件样式全部集中在 `styles/` 下的 QSS 文件里，改外观不用动 Python 代码
- **类型标注（PEP 561）**：全库 type hints + `py.typed` 标记 + `.pyi` 存根，IDE 补全与类型检查友好
- **完整测试覆盖**：52 项 pytest 测试（控件基础行为 + 双主题视觉回归）

## 安装方法

首先请保证电脑上拥有 Python 3.8 或以上版本，建议使用虚拟环境测试。

### 1. 使用 pip 安装

目前 NanUI 还没有上传到 PyPI，在命令行运行下面这行代码来安装：

```bash
pip install git+https://github.com/NanbeiTnT/NanUI.git
```

### 2. 从源码安装

```bash
git clone https://github.com/NanbeiTnT/NanUI.git
cd NanUI
pip install -e .
```

## 快速开始

你可以使用下面这段代码，来测试 NanUI 里的控件：

```python
from NanUI import (
    Window,
    Label,
    PushButton,
    LineEdit,
    TextEdit,
    CheckBox,
    RadioButton,
    ComboBox,
    ProgressBar,
    Card,
    ScrollArea,
)
from NanUI.utils.theme_manager import apply_theme
from NanUI.resources import resources_rc  # 注册 QSS 用到的图标资源（对勾、下拉箭头等）
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout


class MainWindow(Window):
    def __init__(self):
        super().__init__(resizable=True)
        self.resize(1050, 700)
        self.setTitle("NanUI 测试窗口")

        self.lbTest = Label("Label 控件测试")
        self.btnTest = PushButton("PushButton 控件测试")
        self.leTest = LineEdit(placeholder="LineEdit 控件测试")
        self.teTest = TextEdit(placeholder="TextEdit 控件测试")
        self.cbTest = CheckBox("CheckBox 控件测试")
        self.rbtnTest = RadioButton("RadioButton 控件测试1", checked=True)
        self.rbtnTest1 = RadioButton("RadioButton 控件测试2")
        self.cbbTest = ComboBox(items=["选项1", "选项2", "选项3"])
        self.pgBarTest = ProgressBar(value=90)

        self.cardTest = Card(layout="H")
        self.cardLbTest = Label("Card 容器测试")
        self.cardBtnTest = PushButton("Card 容器测试")
        self.cardTest.layout.addWidget(self.cardLbTest)
        self.cardTest.layout.addWidget(self.cardBtnTest)

        self.saTest = ScrollArea()
        self.saLayout = QVBoxLayout()
        for i in range(10):
            self.saLayout.addWidget(PushButton(f"ScrollArea 容器测试{i + 1}"))
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


if __name__ == "__main__":
    app = QApplication([])
    apply_theme(app, "light")
    window = MainWindow()
    window.show()
    app.exec()
```

这段代码的完整版可以在 `examples/10_demo_all.py`（全控件合集）里找到，每个控件也都有单独示例（`examples/01_demo_Window.py` ~ `09_demo_ProgressBar.py`）。

## 已实现控件列表

| 控件 | 说明 |
| --- | --- |
| **Window** | 无边框圆角窗口（可拖动/调整大小，内置标题栏） ✅ |
| **Label** | 圆角标签（带底色，可自定义字体/字号） ✅ |
| **PushButton** | 圆角按钮（悬停/按下/禁用状态） ✅ |
| **LineEdit** | 单行输入框（圆角/焦点高亮/占位文字） ✅ |
| **TextEdit** | 多行文本框（自定义右键菜单） ✅ |
| **CheckBox** | 复选框（自定义对勾图标） ✅ |
| **RadioButton** | 单选按钮（实心圆点风格） ✅ |
| **ComboBox** | 下拉选择框（圆角/自定义箭头/默认只读，支持 `setItems()`） ✅ |
| **ProgressBar** | 进度条（胶囊圆角/纯色填充） ✅ |
| **Card** | 卡片容器（可容纳其他组件） ✅ |
| **ScrollArea** | 滚动区域（可容纳其他组件/细滚动条） ✅ |

## 主题切换

NanUI 内置浅色（light）与深色（dark）两套主题，在启动时指定即可：

```python
from NanUI.utils.theme_manager import apply_theme

# 浅色主题（默认）
apply_theme(app, "light")
# 深色主题
apply_theme(app, "dark")
```

### 新增自定义主题

一个主题由三部分组成，缺一不可：

1. **QSS 样式文件**：在 `NanUI/styles/` 下新建 `{主题名}_theme.qss`，参考已有主题覆盖各控件样式。
2. **THEME_COLORS 取色登记**：在 `NanUI/utils/theme_manager.py` 的 `THEME_COLORS` 里加一份同名配色。自绘控件（窗口底色/描边、标题栏三个按钮的图标）和投影色不走 QSS，只从这里取色；不登记会回落到 light 的配色。
3. **标题栏按钮规则**：QSS 里必须带 `QPushButton#captionButton` 规则，否则标题栏三个按钮的普通态会露出全局按钮的底色。

其他注意点：

- `window_bg` 必须与主题 QSS 里 `QWidget#contentWidget` 的底色一致，否则窗口四角会露出色差。
- 主题 QSS 里最好同时覆盖 `QMenu`、下拉列表等弹层控件，否则切主题后会残留浅色弹层。
- `apply_theme()` 找不到主题文件时会打印警告并返回 `False`。

## 类型标注（PEP 561）

全库源码都带有完整的类型标注，并同时提供两条通道让 IDE / 类型检查器获取类型信息：

- **`py.typed` 标记**：随包分发，`pip install` 后 mypy / Pyright / IDE 直接从源码读取类型，无需额外配置。
- **`.pyi` 存根**：`stubs/` 目录下由 mypy stubgen 生成，供需要独立存根的消费场景使用。

源码与存根均已通过 mypy 严格校验（0 错误），可自行复验：

```bash
mypy NanUI/   # 校验源码
mypy stubs/   # 校验存根
```

## 运行测试

项目用 pytest 做单元与回归测试，共 **52 项**（16 项控件基础行为 + 36 项双主题视觉回归，与基线截图逐像素对比）：

```bash
pip install -r requirements-dev.txt
pytest
```

- 测试在 `QT_QPA_PLATFORM=offscreen` 下运行，没有显示器（如 CI）也能跑。
- 视觉回归的基线图存放在 `tests/baselines/`；外观改动后如果测试失败，会输出差异图供人工确认。

## 参与开发

开发依赖单独放在 `requirements-dev.txt`（与运行时依赖分离，普通用户安装 NanUI 不会装到它们）：

```bash
pip install -r requirements-dev.txt
```

提交代码前请保证以下检查全部通过：

| 检查 | 命令 | 说明 |
| --- | --- | --- |
| 代码规范 | `ruff check .` / `ruff format .` | lint + 格式化（规则见 `pyproject.toml`） |
| 类型检查 | `mypy NanUI/` | 全库类型校验 |
| 单元测试 | `pytest` | 52 项全绿 |

仓库已配置 **pre-commit 钩子**，`git commit` 时自动跑 ruff 检查，不通过会阻止提交：

```bash
pre-commit install           # 首次安装钩子
pre-commit run --all-files   # 手动对全仓库跑一遍
```

## 项目结构

```plain
NanUI/
├── NanUI/                  # 源代码
│   ├── widgets/            # 控件类（11 个，每个一个文件）
│   ├── styles/             # QSS 样式表（light_theme.qss / dark_theme.qss）
│   ├── utils/              # 工具函数（fonts.py / theme_manager.py）
│   ├── resources/          # 图片资源（resources.qrc + 编译产物 resources_rc.py）
│   └── py.typed            # PEP 561 类型标记（随包分发）
├── examples/               # 控件示例（01~09 单控件 + 10 全控件合集）
├── tests/                  # pytest 测试（基础行为 + 视觉回归，baselines/ 存基线图）
├── stubs/                  # .pyi 类型存根（mypy stubgen 生成）
├── setup.py                # 安装脚本
├── pyproject.toml          # ruff 等工具链配置
├── pytest.ini              # 测试配置
├── requirements.txt        # 运行时依赖（仅 PySide6）
├── requirements-dev.txt    # 开发依赖（ruff / pre-commit / mypy / pytest）
├── .pre-commit-config.yaml # git 提交钩子
├── MANIFEST.in             # 打包清单
├── ROADMAP.md              # 开发路线图
├── LICENSE                 # 许可证
└── README.md
```

## 许可证

本项目采用 MIT 许可证，你可以自由使用、修改、分发，包括商业用途。
