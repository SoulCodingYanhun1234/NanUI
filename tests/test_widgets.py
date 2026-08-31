"""控件基础测试（第 21 项：框架落地；第 22 项：每个控件至少一条）。

约定：
- 通过 `qapp` fixture 拿全局唯一 QApplication（定义在 conftest.py）。
- 不做任何视觉断言（那是第 23 项视觉回归测试的事），只验证"能创建、
  关键信号正常、主题切换不崩"。
- 主题测试结束后必须切回 light，避免污染其它测试。

运行（在 NanUI 仓库根目录）：
    python -m pytest tests/ -v
"""

from NanUI import (
    Card,
    CheckBox,
    ComboBox,
    Label,
    LineEdit,
    ProgressBar,
    PushButton,
    RadioButton,
    ScrollArea,
    TextEdit,
    Window,
)
from NanUI.utils.theme_manager import apply_theme, current_theme

from PySide6.QtWidgets import QVBoxLayout, QWidget

# ---------- 顶层导出 ----------


def test_top_level_import():
    """`from NanUI import ...` 应能拿到全部 11 个控件。"""
    assert all(
        cls is not None
        for cls in (
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
    )


# ---------- 控件创建与基础行为 ----------


def test_window_create(qapp):
    """Window 可创建，setTitle 更新标题栏文字。"""
    w = Window(resizable=True)
    w.setTitle("测试标题")
    assert w.title_label.text() == "测试标题"  # setTitle 更新的是标题栏 label
    w.close()


def test_label_text(qapp):
    """Label 文本初始化。"""
    lb = Label("你好")
    assert lb.text() == "你好"


def test_pushbutton_clicked_signal(qapp):
    """PushButton 的 clicked 信号正常发射。"""
    btn = PushButton("点我")
    fired = []
    btn.clicked.connect(lambda: fired.append(True))
    btn.click()
    assert fired == [True]


def test_lineedit_placeholder(qapp):
    """LineEdit 占位文字。"""
    le = LineEdit(placeholder="请输入")
    assert le.placeholderText() == "请输入"


def test_textedit_content(qapp):
    """TextEdit 读写文本。"""
    te = TextEdit()
    te.setPlainText("多行文本")
    assert te.toPlainText() == "多行文本"


def test_checkbox_toggle(qapp):
    """CheckBox 初始状态 + 重写的 toggle()。"""
    cb = CheckBox("选项", checked=False)
    assert not cb.isChecked()
    cb.toggle()
    assert cb.isChecked()


def test_checkbox_toggled_signal(qapp):
    """CheckBox 的 toggled 信号携带新状态。"""
    cb = CheckBox("选项")
    states = []
    cb.toggled.connect(states.append)
    cb.toggle()
    assert states == [True]


def test_radiobutton_exclusive(qapp):
    """同一父控件下 RadioButton 自动互斥。"""
    host = QWidget()
    r1 = RadioButton("A")
    r2 = RadioButton("B")
    r1.setParent(host)
    r2.setParent(host)
    r1.setChecked(True)
    r2.setChecked(True)
    assert not r1.isChecked()
    assert r2.isChecked()


def test_combobox_items(qapp):
    """ComboBox 初始选项 + 选中变化信号。"""
    cbb = ComboBox(items=["一", "二", "三"])
    assert cbb.count() == 3
    assert not cbb.isEditable()  # read_only 默认 True
    changed = []
    cbb.currentTextChanged.connect(changed.append)
    cbb.setCurrentIndex(1)
    assert changed == ["二"]


def test_progressbar_value(qapp):
    """ProgressBar 初始值 + setValue 更新。"""
    pg = ProgressBar(value=40)
    assert (pg.minimum(), pg.maximum()) == (0, 100)
    assert pg.value() == 40
    pg.setValue(80)
    assert pg.value() == 80


def test_card_layout(qapp):
    """Card 创建并挂入子控件。"""
    card = Card(layout="V")
    lb = Label("卡片内容")
    card.layout.addWidget(lb)
    assert card.layout.count() == 1


def test_scrollarea_widget(qapp):
    """ScrollArea 可容纳子控件。"""
    sa = ScrollArea()
    content = QWidget()
    content.setLayout(QVBoxLayout())
    sa.setContentLayout(content.layout())
    assert sa.widget() is not None


# ---------- 主题系统 ----------


def test_theme_switch_roundtrip(qapp):
    """light → dark 切换成功，且能切回。"""
    assert apply_theme(qapp, "light") is True
    assert current_theme() == "light"
    assert apply_theme(qapp, "dark") is True
    assert current_theme() == "dark"
    assert apply_theme(qapp, "light") is True  # 还原，避免污染后续测试
    assert current_theme() == "light"


def test_theme_missing_file(qapp):
    """不存在的主题返回 False 且不抛异常。"""
    assert apply_theme(qapp, "nope") is False
    apply_theme(qapp, "light")  # 还原


def test_window_renders(qapp):
    """Window 离屏渲染不崩，图像尺寸正确（视觉回归雏形）。"""
    w = Window()
    w.resize(300, 200)
    w.show()
    qapp.processEvents()
    img = w.grab().toImage()
    assert img.width() == 300
    assert img.height() == 200
    w.close()
