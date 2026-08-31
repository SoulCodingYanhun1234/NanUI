"""视觉回归测试（第 23 项：离屏渲染 + 逐像素对比）。

作用
----
把每个控件在 light / dark 两个主题下的离屏渲染结果存成 PNG 基线，
之后每次运行都与基线逐像素对比 —— 任何 QSS / 主题色板 / 自绘代码的改动，
只要让界面出现像素变化，就会在这里暴露出来。

这是 ROADMAP 第 23 项的产品化形态：之前验证 QSS 改动时手写的探测脚本
（offscreen 渲染 + 逐像素比差异，见项目记忆"QSS 验证方法"），
收敛成一个正式的 pytest 测试文件，改样式后跑一遍即可自动验证零回归。

运行（在 NanUI 仓库根目录）
--------------------------
    python -m pytest tests/test_visual_regression.py -v    # 对比基线
    python -m pytest tests/test_visual_regression.py --update-baseline  # 重新生成基线

基线机制
--------
- 基线按平台分目录存放：tests/baselines/<platform>/<theme>/<case>.png
  （不同操作系统的字体渲染不同，分目录才能在 CI 上各用各的，不互相污染）。
- 基线缺失时自动生成并跳过对比（首次运行会看到一堆 "新基线" 的 SKIPPED）。
- --update-baseline 强制全部重新生成（改完 QSS、确认新效果是预期时用）。
- 对比失败时差异图写到 tests/baselines/_diffs/<case>.png（已 gitignore），
  差异像素涂红，方便肉眼定位改动了哪里。

覆盖范围
--------
- 11 个控件 × light / dark 两主题 × 关键状态（hover / pressed / disabled / checked）。
- 含 Window 标题栏按钮（自绘控件）与最大化后的直角圆角。
- 不覆盖弹层类（QMenu、ComboBox 下拉列表）与 focus 态：
  弹层渲染时机不稳定；focus 态带闪烁光标，两次渲染相位不同会误报回归。

技术要点（踩坑记录）
--------------------
- 普通控件不直接 grab 自身：PushButton 的投影（QGraphicsDropShadowEffect）
  在控件 rect 之外，直接 grab 会把投影裁掉。统一放进"中性灰画布容器"
  （palette + autoFillBackground，注意不能用 setStyleSheet——父控件样式会
  污染子控件，见项目记忆），留 20px 边距让投影完整落入画面。
- hover 态用 QTest.mouseMove(widget, pos) 触发，实测有效（会移动虚拟光标
  并派发 hover 事件）；pressed 态用 QTest.mousePress 保持按下后 grab。
- 对比用 bytes(QImage.constBits()) 做整块内存比较，完全一致时直接通过，
  只有不一致才进逐像素统计——所以平时跑得飞快，失败时才慢一点。
"""

import sys
from pathlib import Path

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
from NanUI.utils.theme_manager import apply_theme

import pytest
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QImage, QPalette
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

# ---------- 路径与阈值 ----------

BASELINE_DIR = Path(__file__).parent / "baselines"
DIFF_DIR = BASELINE_DIR / "_diffs"
PLATFORM = sys.platform  # win32 / linux / darwin，基线按平台隔离

# 允许差异像素占比（默认 0.5%）。同一台机器上 offscreen 渲染是确定性的，
# 正常情况 0 差异；阈值只用来容忍跨机器字体渲染的微小差异。
TOLERANCE_RATIO = 0.005

# ---------- 渲染辅助 ----------


def _container_with(widget, size, qapp):
    """把控件放进中性灰画布容器并显示，返回容器。

    Args:
        widget (QWidget): 要渲染的控件。
        size (tuple): 容器尺寸 (宽, 高)，需比控件大 40px 以上，
            给投影 / 边框留出边距。
        qapp (QApplication): 全局 QApplication。
    """
    container = QWidget()
    # 画布背景固定为中性灰 #c0c0c0（两主题统一），保证基线可复现。
    # 用 palette + autoFillBackground 而不是 setStyleSheet：
    # 父控件的内联样式表会继承污染子控件（项目记忆里的坑）。
    palette = container.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#c0c0c0"))
    container.setPalette(palette)
    container.setAutoFillBackground(True)

    container.resize(*size)
    layout = QVBoxLayout(container)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.addWidget(widget)
    container.show()
    qapp.processEvents()
    return container


def _grab(container):
    """把容器渲染成 ARGB32 QImage，并清理容器。"""
    img = container.grab().toImage().convertToFormat(QImage.Format.Format_ARGB32)
    container.hide()
    container.deleteLater()
    return img


def _render_plain(widget, size, qapp):
    """渲染控件普通态。"""
    return _grab(_container_with(widget, size, qapp))


def _render_hover(widget, size, qapp):
    """渲染控件 hover 态：把虚拟光标移到控件中心再 grab。"""
    container = _container_with(widget, size, qapp)
    QTest.mouseMove(widget, widget.rect().center())
    qapp.processEvents()
    return _grab(container)


def _render_pressed(widget, size, qapp):
    """渲染控件 pressed 态：按住不松再 grab，之后释放。"""
    container = _container_with(widget, size, qapp)
    QTest.mousePress(widget, Qt.MouseButton.LeftButton, pos=widget.rect().center())
    qapp.processEvents()
    img = _grab(container)
    QTest.mouseRelease(widget, Qt.MouseButton.LeftButton, pos=widget.rect().center())
    return img


# ---------- 对比与基线 ----------


def _compare_images(expected: QImage, actual: QImage):
    """逐像素比较两张 QImage。

    Returns:
        (是否通过, 说明文字)。先做整块内存比较，一致直接通过；
        不一致才逐像素统计差异数和最大通道差。
    """
    if expected.size() != actual.size():
        return False, f"尺寸不同：基线 {expected.size()} vs 实际 {actual.size()}"
    expected_bytes = bytes(expected.constBits())
    actual_bytes = bytes(actual.constBits())
    if expected_bytes == actual_bytes:
        return True, "完全一致"

    pixel_count = len(expected_bytes) // 4
    diff_pixels = 0
    max_channel_diff = 0
    for i in range(0, len(expected_bytes), 4):
        if expected_bytes[i : i + 4] != actual_bytes[i : i + 4]:
            diff_pixels += 1
            for j in range(4):
                diff = abs(expected_bytes[i + j] - actual_bytes[i + j])
                if diff > max_channel_diff:
                    max_channel_diff = diff
    ratio = diff_pixels / pixel_count
    ok = ratio <= TOLERANCE_RATIO
    return (
        ok,
        f"差异像素 {diff_pixels}/{pixel_count}（{ratio:.2%}），最大通道差 {max_channel_diff}",
    )


def _save_diff(expected: QImage, actual: QImage, case: str) -> Path:
    """把差异像素涂红生成差异图，保存到 _diffs/ 目录。"""
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    diff_img = actual.copy()
    expected_bytes = bytes(expected.constBits())
    actual_bytes = bytes(actual.constBits())
    width = actual.width()
    for i in range(0, len(expected_bytes), 4):
        if expected_bytes[i : i + 4] != actual_bytes[i : i + 4]:
            index = i // 4
            diff_img.setPixelColor(index % width, index // width, QColor(255, 0, 0))
    path = DIFF_DIR / f"{case}.png"
    diff_img.save(str(path))
    return path


def _check_snapshot(case: str, theme: str, img: QImage, update_baseline: bool):
    """与基线对比（或生成 / 更新基线）。

    Args:
        case (str): 场景名，如 "pushbutton_hover"。
        theme (str): 主题名，如 "light"。
        img (QImage): 本次渲染结果。
        update_baseline (bool): True 时强制重新生成基线，不做对比。
    """
    base_dir = BASELINE_DIR / PLATFORM / theme
    path = base_dir / f"{case}.png"

    # 更新模式或基线不存在：写基线，跳过对比
    if update_baseline or not path.exists():
        base_dir.mkdir(parents=True, exist_ok=True)
        img.save(str(path))
        if update_baseline:
            return
        pytest.skip(f"已生成新基线：{path}")

    expected = QImage(str(path))
    ok, message = _compare_images(expected, img)
    if not ok:
        diff_path = _save_diff(expected, img, case)
        pytest.fail(
            f"[{case} / {theme}] 视觉回归！{message}\n"
            f"差异图（差异像素涂红）：{diff_path}"
        )


# ---------- 主题 fixture ----------


@pytest.fixture
def themed(qapp, theme):
    """应用参数化进来的主题，测试结束切回 light，避免污染后续测试。"""
    apply_theme(qapp, theme)
    yield
    apply_theme(qapp, "light")


# ---------- 普通控件场景 ----------


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_label(themed, update_baseline, qapp, theme):
    """Label 基础外观（圆角底色 + 文字）。"""
    lb = Label("你好，NanUI")
    lb.setFixedSize(160, 40)
    img = _render_plain(lb, (220, 120), qapp)
    _check_snapshot("label", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_pushbutton(themed, update_baseline, qapp, theme):
    """PushButton 普通态（含投影，主题色随主题变化）。"""
    btn = PushButton("确定")
    btn.setFixedSize(120, 44)
    img = _render_plain(btn, (200, 140), qapp)
    _check_snapshot("pushbutton", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_pushbutton_hover(themed, update_baseline, qapp, theme):
    """PushButton hover 态（浅色压暗 / 深色提亮，两主题方向相反）。"""
    btn = PushButton("确定")
    btn.setFixedSize(120, 44)
    img = _render_hover(btn, (200, 140), qapp)
    _check_snapshot("pushbutton_hover", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_pushbutton_pressed(themed, update_baseline, qapp, theme):
    """PushButton pressed 态。"""
    btn = PushButton("确定")
    btn.setFixedSize(120, 44)
    img = _render_pressed(btn, (200, 140), qapp)
    _check_snapshot("pushbutton_pressed", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_pushbutton_disabled(themed, update_baseline, qapp, theme):
    """PushButton disabled 态（不能比正常态还亮，暗色主题的已知坑）。"""
    btn = PushButton("确定")
    btn.setFixedSize(120, 44)
    btn.setEnabled(False)
    img = _render_plain(btn, (200, 140), qapp)
    _check_snapshot("pushbutton_disabled", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_lineedit(themed, update_baseline, qapp, theme):
    """LineEdit 占位文字（QSS 的 ::placeholder 无效，颜色走 palette）。"""
    le = LineEdit(placeholder="请输入内容")
    le.setFixedSize(240, 44)
    img = _render_plain(le, (320, 140), qapp)
    _check_snapshot("lineedit", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_textedit(themed, update_baseline, qapp, theme):
    """TextEdit 多行内容。"""
    te = TextEdit()
    te.setPlainText("多行文本内容\n第二行")
    te.setFixedSize(260, 110)
    img = _render_plain(te, (340, 190), qapp)
    _check_snapshot("textedit", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_checkbox(themed, update_baseline, qapp, theme):
    """CheckBox 未选中。"""
    cb = CheckBox("记住我")
    cb.setFixedSize(120, 36)
    img = _render_plain(cb, (200, 120), qapp)
    _check_snapshot("checkbox", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_checkbox_checked(themed, update_baseline, qapp, theme):
    """CheckBox 选中（勾选图标随主题换 dark 版本）。"""
    cb = CheckBox("记住我", checked=True)
    cb.setFixedSize(120, 36)
    img = _render_plain(cb, (200, 120), qapp)
    _check_snapshot("checkbox_checked", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_radiobutton(themed, update_baseline, qapp, theme):
    """RadioButton 未选中。"""
    rb = RadioButton("选项 A")
    rb.setFixedSize(120, 36)
    img = _render_plain(rb, (200, 120), qapp)
    _check_snapshot("radiobutton", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_radiobutton_checked(themed, update_baseline, qapp, theme):
    """RadioButton 选中（实心圆点）。"""
    rb = RadioButton("选项 A")
    rb.setChecked(True)
    rb.setFixedSize(120, 36)
    img = _render_plain(rb, (200, 120), qapp)
    _check_snapshot("radiobutton_checked", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_combobox(themed, update_baseline, qapp, theme):
    """ComboBox（下拉箭头图标随主题换 dark 版本）。"""
    cbb = ComboBox(items=["选项一", "选项二", "选项三"])
    cbb.setFixedSize(200, 44)
    img = _render_plain(cbb, (280, 140), qapp)
    _check_snapshot("combobox", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_progressbar(themed, update_baseline, qapp, theme):
    """ProgressBar 半值（chunk 长度 + 百分比文字）。"""
    pg = ProgressBar(value=60)
    pg.setFixedSize(240, 36)
    img = _render_plain(pg, (320, 130), qapp)
    _check_snapshot("progressbar", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_card(themed, update_baseline, qapp, theme):
    """Card 容器 + 内部 Label。"""
    card = Card(layout="V")
    card.layout.addWidget(Label("卡片内容"))
    card.setFixedSize(220, 100)
    img = _render_plain(card, (300, 180), qapp)
    _check_snapshot("card", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_scrollarea(themed, update_baseline, qapp, theme):
    """ScrollArea 内容超高，垂直滚动条出现（验证滚动条 QSS）。"""
    sa = ScrollArea()
    content = QWidget()
    content.setLayout(QVBoxLayout())
    content.layout().addWidget(QLabel("很长的内容\n" * 20))
    sa.setContentLayout(content.layout())
    sa.setFixedSize(240, 130)
    img = _render_plain(sa, (320, 210), qapp)
    _check_snapshot("scrollarea", theme, img, update_baseline)


# ---------- Window 场景 ----------


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_window(themed, update_baseline, qapp, theme):
    """Window 整窗：标题栏 + 三个自绘按钮 + 内容区 + 圆角。"""
    w = Window()
    w.resize(320, 220)
    w.show()
    qapp.processEvents()
    img = w.grab().toImage().convertToFormat(QImage.Format.Format_ARGB32)
    w.hide()
    _check_snapshot("window", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_window_caption_hover(themed, update_baseline, qapp, theme):
    """Window 关闭按钮 hover（自绘按钮的悬停底色 / 图标变白）。"""
    w = Window()
    w.resize(320, 220)
    w.show()
    qapp.processEvents()
    # 光标移到关闭按钮中心（坐标相对 Window 映射）
    pos = w.btn_close.mapTo(w, w.btn_close.rect().center())
    QTest.mouseMove(w, pos)
    qapp.processEvents()
    img = w.grab().toImage().convertToFormat(QImage.Format.Format_ARGB32)
    w.hide()
    _check_snapshot("window_caption_hover", theme, img, update_baseline)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_window_maximized_corner(themed, update_baseline, qapp, theme):
    """Window 最大化后左上角 60x60：圆角必须抹平成直角（历史 bug）。

    顺带做两个功能断言：最大化走真实交互路径（点最大化按钮），
    图标应切回 restore、窗口圆角半径应归零。
    """
    w = Window()
    w.resize(320, 220)
    w.show()
    qapp.processEvents()
    w.btn_max.click()  # 走真实交互路径：最大化 + 图标切 restore
    qapp.processEvents()
    assert w.isMaximized()
    assert w._radius == 0
    assert w.btn_max._icon_type == "restore"
    img = (
        w.grab(QRect(0, 0, 60, 60))
        .toImage()
        .convertToFormat(QImage.Format.Format_ARGB32)
    )
    w.hide()
    _check_snapshot("window_maximized_corner", theme, img, update_baseline)
