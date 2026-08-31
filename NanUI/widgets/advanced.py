from __future__ import annotations

from typing import Iterable, Optional, Sequence

from PySide6.QtCore import Property, QEasingCurve, QPoint, QPropertyAnimation, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QDragEnterEvent, QDropEvent, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import (
    QAbstractItemView,
    QColorDialog,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMenu,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSlider,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

from NanUI.utils.theme_manager import current_theme


def _theme(light: str, dark: str) -> str:
    return dark if current_theme() == "dark" else light


class Switch(QPushButton):
    """胶囊滑动开关。使用 ``toggled(bool)`` 监听即时布尔值变化。"""

    def __init__(self, checked: bool = False, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(checked)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(46, 26)
        self.setObjectName("nanSwitch")
        self.toggled.connect(self.update)

    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        track = QColor(_theme("#c7ccd4", "#484852"))
        if self.isChecked():
            track = QColor(_theme("#4f86f7", "#7aa2f7"))
        if not self.isEnabled():
            track.setAlpha(110)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(track)
        p.drawRoundedRect(QRectF(1, 3, 44, 20), 10, 10)
        knob = QColor(_theme("#ffffff", "#f4f4f6"))
        p.setBrush(knob)
        x = 24 if self.isChecked() else 4
        p.drawEllipse(QRectF(x, 5, 16, 16))


class Slider(QSlider):
    """现代滑块；支持 Qt 原生连续/步进、键盘和鼠标拖动行为。"""

    def __init__(self, minimum: int = 0, maximum: int = 100, value: int = 0,
                 orientation: Qt.Orientation = Qt.Orientation.Horizontal,
                 parent: Optional[QWidget] = None, step: int = 1) -> None:
        super().__init__(orientation, parent)
        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setSingleStep(step)
        self.setObjectName("nanSlider")


class SpinBox(QSpinBox):
    def __init__(self, minimum: int = 0, maximum: int = 100, value: int = 0,
                 parent: Optional[QWidget] = None, step: int = 1) -> None:
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setSingleStep(step)
        self.setValue(value)
        self.setObjectName("nanSpinBox")


class SegmentedControl(QWidget):
    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, items: Sequence[str] = (), current: int = 0,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("segmentedControl")
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(3, 3, 3, 3)
        self._layout.setSpacing(2)
        self._buttons: list[QPushButton] = []
        self._index = -1
        for text in items:
            self.addSegment(text)
        if self._buttons:
            self.setCurrentIndex(max(0, min(current, len(self._buttons) - 1)))

    def addSegment(self, text: str) -> int:
        idx = len(self._buttons)
        b = QPushButton(text, self)
        b.setCheckable(True)
        b.setObjectName("segmentButton")
        b.clicked.connect(lambda _=False, i=idx: self.setCurrentIndex(i))
        self._layout.addWidget(b)
        self._buttons.append(b)
        return idx

    def count(self) -> int:
        return len(self._buttons)

    def currentIndex(self) -> int:
        return self._index

    def currentText(self) -> str:
        return self._buttons[self._index].text() if 0 <= self._index < len(self._buttons) else ""

    def setCurrentIndex(self, index: int) -> None:
        if not 0 <= index < len(self._buttons) or index == self._index:
            return
        self._index = index
        for i, b in enumerate(self._buttons):
            b.setChecked(i == index)
        self.currentIndexChanged.emit(index)
        self.currentTextChanged.emit(self.currentText())


class ToolTip:
    """QToolTip 的轻量包装。"""
    @staticmethod
    def show(text: str, pos: QPoint, widget: Optional[QWidget] = None, msec: int = 2500) -> None:
        QToolTip.showText(pos, text, widget, msec=msec)

    @staticmethod
    def hide() -> None:
        QToolTip.hideText()


class Badge(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("badge")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(18, 18)
        self.adjustSize()

    def setCount(self, count: int, maximum: int = 99) -> None:
        self.setText(str(count) if count <= maximum else f"{maximum}+")
        self.setVisible(count > 0)
        self.adjustSize()


class Toast(QFrame):
    closed = Signal()

    def __init__(self, text: str, kind: str = "info", parent: Optional[QWidget] = None,
                 duration: int = 2500) -> None:
        super().__init__(parent)
        self.setObjectName("toast")
        self.setProperty("kind", kind)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 9, 14, 9)
        label = QLabel(text, self)
        label.setObjectName("toastLabel")
        layout.addWidget(label)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.close)
        if duration > 0:
            self._timer.start(duration)

    @classmethod
    def showMessage(cls, parent: QWidget, text: str, kind: str = "info", duration: int = 2500) -> "Toast":
        toast = cls(text, kind, parent, duration)
        toast.adjustSize()
        x = max(12, (parent.width() - toast.width()) // 2)
        toast.move(x, 18)
        toast.show()
        toast.raise_()
        return toast

    def closeEvent(self, event) -> None:
        self.closed.emit()
        super().closeEvent(event)


class Dialog(QDialog):
    def __init__(self, title: str = "", content: Optional[QWidget] = None,
                 parent: Optional[QWidget] = None, buttons: bool = True) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setObjectName("nanDialog")
        self.layout = QVBoxLayout(self)
        if title:
            t = QLabel(title, self); t.setObjectName("dialogTitle"); self.layout.addWidget(t)
        if content:
            self.layout.addWidget(content)
        if buttons:
            row = QHBoxLayout(); row.addStretch(1)
            cancel = QPushButton("取消", self); ok = QPushButton("确定", self)
            cancel.clicked.connect(self.reject); ok.clicked.connect(self.accept)
            row.addWidget(cancel); row.addWidget(ok); self.layout.addLayout(row)

    @staticmethod
    def message(parent: Optional[QWidget], title: str, text: str,
                icon: QMessageBox.Icon = QMessageBox.Icon.Information) -> QMessageBox.StandardButton:
        box = QMessageBox(icon, title, text, QMessageBox.StandardButton.Ok, parent)
        return box.exec()


class Skeleton(QFrame):
    """带轻量呼吸动画的骨架占位块。"""
    def __init__(self, parent: Optional[QWidget] = None, radius: int = 8) -> None:
        super().__init__(parent)
        self.setObjectName("skeleton")
        self._radius = radius
        self._phase = 0
        self.setMinimumHeight(18)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(90)

    def _tick(self) -> None:
        self._phase = (self._phase + 1) % 20
        self.update()

    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        base = QColor(_theme("#e5eaf0", "#33333a"))
        # 三角波透明度，避免依赖复杂渐变/动画对象。
        alpha = 190 + int(45 * (1 - abs(self._phase - 10) / 10))
        base.setAlpha(alpha)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(base)
        p.drawRoundedRect(QRectF(self.rect()), self._radius, self._radius)


class LoadingIndicator(QWidget):
    def __init__(self, parent: Optional[QWidget] = None, size: int = 28) -> None:
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._angle = 0
        self._timer = QTimer(self); self._timer.timeout.connect(self._tick); self._timer.start(70)

    def _tick(self) -> None:
        self._angle = (self._angle + 30) % 360; self.update()

    def paintEvent(self, event) -> None:
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(_theme("#4f86f7", "#7aa2f7")), 3); pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        r = self.rect().adjusted(4, 4, -4, -4)
        p.drawArc(r, int((-self._angle) * 16), int(250 * 16))


class NavigationSideBar(QFrame):
    currentIndexChanged = Signal(int)
    def __init__(self, items: Sequence[str] = (), parent: Optional[QWidget] = None,
                 collapsible: bool = True) -> None:
        super().__init__(parent); self.setObjectName("navigationSideBar")
        self._collapsible = collapsible; self._collapsed = False; self._buttons = []
        self.layout = QVBoxLayout(self); self.layout.setContentsMargins(6, 6, 6, 6); self.layout.setSpacing(4)
        for text in items: self.addItem(text)
        self.layout.addStretch(1)
        if collapsible:
            toggle = QPushButton("≡", self); toggle.setObjectName("navCollapseButton"); toggle.clicked.connect(self.toggleCollapsed); self.layout.addWidget(toggle)

    def addItem(self, text: str) -> int:
        i = len(self._buttons); b = QPushButton(text, self); b.setCheckable(True); b.setObjectName("navItem")
        b.clicked.connect(lambda _=False, idx=i: self.setCurrentIndex(idx)); self.layout.insertWidget(i, b); self._buttons.append(b)
        if i == 0: self.setCurrentIndex(0)
        return i

    def setCurrentIndex(self, index: int) -> None:
        if not 0 <= index < len(self._buttons): return
        for i,b in enumerate(self._buttons): b.setChecked(i == index)
        self.currentIndexChanged.emit(index)

    def toggleCollapsed(self) -> None:
        self._collapsed = not self._collapsed
        self.setFixedWidth(64 if self._collapsed else 190)
        for b in self._buttons:
            full = b.property("fullText") or b.text(); b.setProperty("fullText", full); b.setText(full[:1] if self._collapsed else full)


class TabWidget(QTabWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent); self.setObjectName("nanTabWidget"); self.setDocumentMode(True)

TabBar = TabWidget


class Divider(QFrame):
    def __init__(self, text: str = "", orientation: Qt.Orientation = Qt.Orientation.Horizontal,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent); self.setObjectName("divider")
        self.layout = QHBoxLayout(self) if orientation == Qt.Orientation.Horizontal else QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0); self.layout.setSpacing(8)
        a = QFrame(self); a.setObjectName("dividerLine"); a.setFrameShape(QFrame.Shape.HLine if orientation == Qt.Orientation.Horizontal else QFrame.Shape.VLine)
        self.layout.addWidget(a)
        if text:
            label = QLabel(text, self); label.setObjectName("dividerText"); self.layout.addWidget(label)
            b = QFrame(self); b.setObjectName("dividerLine"); b.setFrameShape(a.frameShape()); self.layout.addWidget(b)


class Collapsible(QFrame):
    toggled = Signal(bool)
    def __init__(self, title: str = "", content: Optional[QWidget] = None,
                 expanded: bool = False, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent); self.setObjectName("collapsible")
        self.layout = QVBoxLayout(self); self.layout.setContentsMargins(0,0,0,0); self.layout.setSpacing(0)
        self.header = QPushButton(title, self); self.header.setCheckable(True); self.header.setChecked(expanded); self.header.setObjectName("collapsibleHeader")
        self.layout.addWidget(self.header); self.content = content or QWidget(self); self.content.setObjectName("collapsibleContent"); self.layout.addWidget(self.content)
        self.header.toggled.connect(self.setExpanded); self.setExpanded(expanded)

    def isExpanded(self) -> bool: return self.header.isChecked()
    def setExpanded(self, expanded: bool) -> None:
        self.header.blockSignals(True); self.header.setChecked(expanded); self.header.blockSignals(False); self.content.setVisible(expanded); self.toggled.emit(expanded)

Accordion = Collapsible


class Table(QTableWidget):
    def __init__(self, rows: int = 0, columns: int = 0, parent: Optional[QWidget] = None,
                 headers: Sequence[str] = ()) -> None:
        super().__init__(rows, columns or len(headers), parent); self.setObjectName("nanTable")
        self.setAlternatingRowColors(True); self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSortingEnabled(True); self.verticalHeader().setVisible(False)
        if headers: self.setHorizontalHeaderLabels(list(headers))

    def setRows(self, rows: Iterable[Sequence[object]]) -> None:
        data = list(rows); self.setSortingEnabled(False); self.setRowCount(len(data))
        max_cols = max((len(r) for r in data), default=self.columnCount()); self.setColumnCount(max(self.columnCount(), max_cols))
        for r, row in enumerate(data):
            for c, value in enumerate(row): self.setItem(r, c, QTableWidgetItem(str(value)))
        self.setSortingEnabled(True)


class ListView(QListWidget):
    def __init__(self, items: Sequence[str] = (), parent: Optional[QWidget] = None) -> None:
        super().__init__(parent); self.setObjectName("nanListView"); self.addItems(list(items)); self.setAlternatingRowColors(True)


class ColorPicker(QPushButton):
    colorChanged = Signal(QColor)
    def __init__(self, color: str | QColor = "#4f86f7", parent: Optional[QWidget] = None, alpha: bool = True) -> None:
        super().__init__(parent); self.setObjectName("colorPicker"); self._color = QColor(color); self._alpha = alpha; self.clicked.connect(self.pick); self._sync()
    def color(self) -> QColor: return QColor(self._color)
    def setColor(self, color: str | QColor) -> None:
        c = QColor(color)
        if c.isValid() and c != self._color: self._color = c; self._sync(); self.colorChanged.emit(QColor(c))
    def pick(self) -> None:
        opts = QColorDialog.ColorDialogOption.ShowAlphaChannel if self._alpha else QColorDialog.ColorDialogOption(0)
        c = QColorDialog.getColor(self._color, self, "选择颜色", opts)
        if c.isValid(): self.setColor(c)
    def _sync(self) -> None:
        self.setText(self._color.name(QColor.NameFormat.HexArgb if self._alpha else QColor.NameFormat.HexRgb)); self.setStyleSheet(f"QPushButton#colorPicker{{border-left:24px solid {self._color.name()};}}")


class FilePicker(QWidget):
    filesSelected = Signal(list)
    def __init__(self, parent: Optional[QWidget] = None, multiple: bool = False, filter: str = "所有文件 (*)") -> None:
        super().__init__(parent); self.multiple = multiple; self.filter = filter; self.paths: list[str] = []
        layout = QHBoxLayout(self); layout.setContentsMargins(0,0,0,0); self.label = QLabel("未选择文件", self); self.label.setObjectName("filePickerLabel")
        button = QPushButton("选择文件", self); button.clicked.connect(self.pick); layout.addWidget(self.label, 1); layout.addWidget(button)
    def pick(self) -> None:
        if self.multiple: paths, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", self.filter)
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", self.filter); paths = [path] if path else []
        if paths: self.setFiles(paths)
    def setFiles(self, paths: Sequence[str]) -> None:
        self.paths = list(paths); self.label.setText("; ".join(self.paths)); self.filesSelected.emit(self.paths)


class DropZone(QFrame):
    filesDropped = Signal(list)
    def __init__(self, text: str = "拖拽文件到此处，或点击选择", parent: Optional[QWidget] = None, multiple: bool = True) -> None:
        super().__init__(parent); self.setObjectName("dropZone"); self.setAcceptDrops(True); self.multiple = multiple
        layout = QVBoxLayout(self); label = QLabel(text, self); label.setObjectName("dropZoneLabel"); label.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(label)
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.multiple: paths, _ = QFileDialog.getOpenFileNames(self, "选择文件")
            else:
                path, _ = QFileDialog.getOpenFileName(self, "选择文件"); paths = [path] if path else []
            if paths: self.filesDropped.emit(paths)
        super().mousePressEvent(event)
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls(): event.acceptProposedAction()
    def dropEvent(self, event: QDropEvent) -> None:
        paths = [u.toLocalFile() for u in event.mimeData().urls() if u.isLocalFile()]
        if not self.multiple: paths = paths[:1]
        if paths: self.filesDropped.emit(paths); event.acceptProposedAction()


class ContextMenu(QMenu):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent); self.setObjectName("nanContextMenu")
    def addItem(self, text: str, callback=None, enabled: bool = True, submenu: Optional["ContextMenu"] = None):
        if submenu is not None: action = self.addMenu(submenu); action.setText(text)
        else: action = self.addAction(text); action.setEnabled(enabled); action.triggered.connect(callback) if callback else None
        return action
    def attach(self, widget: QWidget) -> None:
        widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        widget.customContextMenuRequested.connect(lambda p: self.exec(widget.mapToGlobal(p)))
