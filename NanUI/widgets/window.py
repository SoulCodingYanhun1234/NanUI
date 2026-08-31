"""
注：本文件部分代码由 Deepseek 网页端和 TraeCode-cn Windows 端辅助开发。
"""

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QPoint, QPointF, QRectF, QEvent, QSize
from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen, QFont
from NanUI.utils import get_font
from NanUI.utils.theme_manager import get_color


class CaptionButton(QPushButton):
    """
    标题栏按钮（Win11 风格）。

    继承自 QPushButton。图标由 QPainter 自绘，背景和图标颜色取自当前主题
    （theme_manager.THEME_COLORS），所以 QSS 改不动它的颜色，只能改尺寸相关属性。

    Args:
        icon_type (str): 图标类型。可选值：'minimize'（最小化）、'maximize'（最大化）、
            'restore'（恢复）、'close'（关闭）。默认为 'minimize'。
        parent (QWidget, optional): 父控件对象。默认为 None。
    """

    def __init__(self, icon_type: str = "minimize", parent=None):
        super().__init__(parent)
        self._icon_type = icon_type
        self.setFixedSize(30, 30)
        # 尺寸相关的修正放在主题的 QSS 里（QPushButton#captionButton），
        # 不再用内联样式表，否则会挡住 app 级 QSS、用户改不动。
        # 按钮外观本身由下面的 paintEvent 自绘，颜色取自当前主题。
        self.setObjectName("captionButton")

    def set_icon_type(self, icon_type: str):
        self._icon_type = icon_type
        self.update()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_hover = self.underMouse()
        is_pressed = self.isDown()
        is_close = (self._icon_type == "close")

        # ---------- 背景色 ----------
        # 自绘内容不经过 QSS，颜色统一从主题配色表取
        if is_pressed:
            bg = QColor(get_color("caption_close_pressed" if is_close else "caption_pressed"))
        elif is_hover:
            bg = QColor(get_color("caption_close_hover" if is_close else "caption_hover"))
        else:
            bg = QColor("transparent")

        # ---------- 图标色 ----------
        if (is_hover or is_pressed) and is_close:
            fg = QColor(get_color("caption_fg_active"))
        else:
            fg = QColor(get_color("caption_fg"))

        # 画背景（圆角）
        painter.setBrush(bg)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(self.rect()), 6, 6)

        # 画图标
        pen = QPen(fg, 1.2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        cx = self.width() / 2
        cy = self.height() / 2
        s = 5  # 图标半尺寸（10×10 图标在 30×30 按钮内）

        if self._icon_type == "minimize":
            painter.drawLine(QPointF(cx - s, cy), QPointF(cx + s, cy))

        elif self._icon_type == "maximize":
            painter.drawRect(QRectF(cx - s, cy - s, 2 * s, 2 * s))

        elif self._icon_type == "restore":
            # 前面方框（左上）
            front_rect = QRectF(cx - s, cy - s + 2, 2 * s - 2, 2 * s - 2)
            # 后面方框（右下）
            back_rect = QRectF(cx - s + 2, cy - s, 2 * s - 2, 2 * s - 2)
            # 绘制后面方框时排除前面方框的区域，实现遮挡效果
            painter.save()
            clip_path = QPainterPath()
            clip_path.addRect(QRectF(self.rect()))
            front_path = QPainterPath()
            front_path.addRect(front_rect)
            clip_path = clip_path.subtracted(front_path)
            painter.setClipPath(clip_path)
            painter.drawRect(back_rect)
            painter.restore()
            # 绘制前面方框（完整）
            painter.drawRect(front_rect)

        elif self._icon_type == "close":
            painter.drawLine(QPointF(cx - s, cy - s), QPointF(cx + s, cy + s))
            painter.drawLine(QPointF(cx + s, cy - s), QPointF(cx - s, cy + s))


class Window(QWidget):
    """
    无边框圆角窗口基类。

    继承自 QWidget。无系统边框，带圆角，标题栏可拖动窗口（仅标题栏区域），
    内置最小化、最大化/恢复、关闭三个按钮，用 setTitle() 设置窗口标题。
    可选是否允许鼠标拖动窗口边缘调整大小。

    Args:
        parent (QWidget, optional): 父控件对象。默认为 None。
        radius (int): 窗口圆角半径（像素）。默认为 12。
        resizable (bool): 是否允许调整窗口大小。默认为 False。
    """

    def __init__(self, parent=None, radius: int = 12, resizable: bool = False):
        super().__init__(parent)

        # ---------- 属性初始化（提前，防止事件处理时未定义） ----------
        self._radius = radius
        self._original_radius = radius
        self._resizable = resizable
        self._dragging = False
        self._drag_pos = QPoint()
        self._edge_margin = 8
        self._resize_direction = None
        self._resize_start_pos = None
        self._resize_start_geo = None

        # ---------- 窗口标志与透明背景 ----------
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_Hover, True)  # 启用 Hover 事件，用于光标管理
        self.setMouseTracking(True)
        self.setMinimumSize(300, 200)

        # ---------- 创建标题栏 ----------
        self.title_bar = QWidget(self)
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(40)  # 标题栏高度

        # 标题栏内的布局
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(8)

        # 标题标签（使用更细腻的字体）
        self.title_label = QLabel("窗口标题")
        self.title_label.setObjectName("titleLabel")
        # font = QFont("Microsoft YaHei", 12)
        font = get_font(size=12, weight=QFont.Normal)
        # font.setWeight(QFont.Normal)  # 常规字重，不粗
        font.setStyleStrategy(QFont.PreferAntialias)  # 抗锯齿 + 亚像素渲染
        font.setHintingPreference(QFont.PreferVerticalHinting)  # 仅垂直 hinting，中文更平滑
        self.title_label.setFont(font)
        title_layout.addWidget(self.title_label)

        # 弹簧将按钮推到右侧
        title_layout.addStretch()

        # 最小化按钮
        self.btn_min = CaptionButton("minimize", self.title_bar)
        self.btn_min.clicked.connect(self.showMinimized)

        # 最大化/恢复按钮
        self.btn_max = CaptionButton("maximize", self.title_bar)
        self.btn_max.clicked.connect(self._toggle_maximize)

        # 关闭按钮（悬停变红）
        self.btn_close = CaptionButton("close", self.title_bar)
        self.btn_close.clicked.connect(self.close)

        title_layout.addWidget(self.btn_min)
        title_layout.addWidget(self.btn_max)
        title_layout.addWidget(self.btn_close)

        # ---------- 内容容器 ----------
        self.content_widget = QWidget(self)
        self.content_widget.setObjectName("contentWidget")

        # ---------- 主布局（垂直排列标题栏 + 内容） ----------
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._main_layout.addWidget(self.title_bar)
        self._main_layout.addWidget(self.content_widget)

        # 内容区域的默认布局（用户可以通过 setLayout 重设）
        self._content_layout = QVBoxLayout(self.content_widget)
        self._content_layout.setContentsMargins(15, 15, 15, 15)

        # ---------- 保存窗口最大化前的几何（用于恢复） ----------
        self._normal_geometry = None

        # 记录"去圆角"是否已应用到标题栏/内容区，避免 resize 时反复重设样式表
        self._squared_corners = None

    # ---------- 设置窗口标题 ----------
    def setTitle(self, title: str):
        self.title_label.setText(title)

    # ---------- 重写布局设置（将布局应用到内容区域） ----------
    def setLayout(self, layout):
        """用户调用此方法时，将布局应用到 content_widget 上"""
        if self._content_layout:
            # 清除原有的内容布局
            QWidget().setLayout(self._content_layout)  # 换掉旧布局
        self._content_layout = layout
        self.content_widget.setLayout(layout)

    # ---------- 窗口状态切换 ----------
    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.btn_max.set_icon_type("maximize")
        else:
            self.showMaximized()
            self.btn_max.set_icon_type("restore")

    # ---------- 窗口事件处理（调整大小与光标） ----------
    def event(self, event):
        if self._resizable:
            event_type = event.type()

            # HoverMove：光标管理（无按键时）
            # HoverMove 会向父级传播，即使鼠标在子控件上方，窗口也能收到
            if event_type == QEvent.HoverMove:
                pos = event.position().toPoint()
                direction = self._getResizeDirection(pos)
                if direction is not None:
                    self._setCursorShape(direction)
                else:
                    self.unsetCursor()

            # HoverLeave：鼠标离开窗口时恢复光标
            elif event_type == QEvent.HoverLeave:
                self.unsetCursor()

            # MouseButtonPress：开始调整大小（整个窗口边缘均可触发）
            elif event_type == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    pos = event.position().toPoint()
                    direction = self._getResizeDirection(pos)
                    if direction is not None:
                        self._resize_direction = direction
                        self._resize_start_pos = event.globalPosition().toPoint()
                        self._resize_start_geo = self.geometry()
                        return True

            # MouseMove：执行调整大小（仅按键拖拽时）
            elif event_type == QEvent.MouseMove:
                if self._resize_direction is not None:
                    self._performResize(event)
                    return True

            # MouseButtonRelease：结束调整大小
            elif event_type == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton and self._resize_direction is not None:
                    self._resize_direction = None
                    self._resize_start_pos = None
                    self._resize_start_geo = None
                    return True

        return super().event(event)

    # ---------- 鼠标拖动（仅标题栏区域） ----------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 判断点击位置是否在标题栏上（包括标题栏本身及其子控件）
            pos = event.position().toPoint()
            if self.title_bar.geometry().contains(pos):
                global_pos = event.globalPosition().toPoint()

                if self.isMaximized():
                    # 记录鼠标在窗口中的水平比例，用于恢复后保持相对位置
                    ratio = global_pos.x() / self.width()
                    click_y = pos.y()
                    # 恢复窗口
                    self.showNormal()
                    self.btn_max.set_icon_type("maximize")
                    # 按恢复后的宽度计算拖拽偏移，保持鼠标在标题栏同一相对位置
                    self._drag_pos = QPoint(int(self.width() * ratio), click_y)
                    self.move(global_pos - self._drag_pos)
                else:
                    self._drag_pos = global_pos - self.frameGeometry().topLeft()

                self._dragging = True
                event.accept()
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._dragging:
            self._dragging = False
            # 拖动到屏幕顶部释放时最大化（模拟 Windows Aero Snap）
            global_pos = event.globalPosition().toPoint()
            screen = QApplication.screenAt(global_pos)
            if screen and global_pos.y() <= screen.geometry().top():
                self.showMaximized()
                self.btn_max.set_icon_type("restore")
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    # ---------- 辅助方法（调整大小相关） ----------
    def _getResizeDirection(self, pos):
        if not self._resizable:
            return None
        if self.isMaximized():
            return None  # 最大化时不允许调整大小
        rect = self.rect()  # 使用窗口自身的 rect 作为边缘检测基准
        left = pos.x() < self._edge_margin
        right = pos.x() > rect.width() - self._edge_margin
        top = pos.y() < self._edge_margin
        bottom = pos.y() > rect.height() - self._edge_margin
        if left and top:
            return "top-left"
        elif right and top:
            return "top-right"
        elif left and bottom:
            return "bottom-left"
        elif right and bottom:
            return "bottom-right"
        elif left:
            return "left"
        elif right:
            return "right"
        elif top:
            return "top"
        elif bottom:
            return "bottom"
        return None

    def _setCursorShape(self, direction):
        shapes = {
            "top-left": Qt.SizeFDiagCursor,
            "bottom-right": Qt.SizeFDiagCursor,
            "top-right": Qt.SizeBDiagCursor,
            "bottom-left": Qt.SizeBDiagCursor,
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
        }
        cursor = shapes.get(direction, Qt.ArrowCursor)
        self.setCursor(cursor)

    def _performResize(self, event):
        if self._resize_direction is None or self._resize_start_pos is None:
            return
        delta = event.globalPosition().toPoint() - self._resize_start_pos
        geo = self._resize_start_geo
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()
        dir_ = self._resize_direction
        if "left" in dir_:
            new_w = w - delta.x()
            if new_w >= self.minimumWidth():
                x += delta.x()
                w = new_w
        if "right" in dir_:
            new_w = w + delta.x()
            if new_w >= self.minimumWidth():
                w = new_w
        if "top" in dir_:
            new_h = h - delta.y()
            if new_h >= self.minimumHeight():
                y += delta.y()
                h = new_h
        if "bottom" in dir_:
            new_h = h + delta.y()
            if new_h >= self.minimumHeight():
                h = new_h
        self.setGeometry(x, y, w, h)

    # ---------- 绘制窗口背景（圆角） ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self._radius, self._radius)
        painter.fillPath(path, QColor(get_color("window_bg")))
        painter.setPen(QPen(QColor(get_color("window_border")), 1))
        painter.drawPath(path)

    # ---------- 窗口状态变化（最大化/恢复时切换圆角） ----------
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self._update_appearance()
        super().changeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_appearance()

    def _update_appearance(self):
        if self.isMaximized():
            self._radius = 0
        else:
            self._radius = self._original_radius

        # 光把窗口自己的圆角清零还不够：标题栏和内容区的背景是 QSS 画的，
        # 它们各自带着 8px 圆角，会在四角戳出直角缺口。
        # 最大化时必须连它们一起抹平，恢复时再交还给主题 QSS。
        if self._squared_corners != self.isMaximized():
            self._squared_corners = self.isMaximized()
            self._apply_corner_style(self._squared_corners)

    def _apply_corner_style(self, squared: bool):
        """
        给标题栏和内容区设定圆角，使其与窗口自身的圆角一致。

        这里只写圆角属性，不碰背景色——Qt 的样式表是逐属性覆盖的，
        控件级规则不会吃掉 app 级 QSS 提供的背景色。

        圆角值取自 self._radius，不再由 QSS 写死。之前主题 QSS 里写的是 8px，
        而窗口默认 radius 是 12，子控件圆角比窗口小就会在四角戳出直角缺口。
        改成动态取值后，无论 Window(radius=?) 传多少都能自动对齐。

        Args:
            squared(bool): True 表示最大化，抹平圆角；False 表示用当前窗口圆角。
        """
        r = 0 if squared else self._radius
        self.title_bar.setStyleSheet(
            "QWidget#titleBar {"
            f" border-top-left-radius: {r}px;"
            f" border-top-right-radius: {r}px;"
            " }"
        )
        self.content_widget.setStyleSheet(
            "QWidget#contentWidget {"
            f" border-bottom-left-radius: {r}px;"
            f" border-bottom-right-radius: {r}px;"
            " }"
        )

    # ---------- 窗口显示时更新外观与按钮图标 ----------
    def showEvent(self, event):
        super().showEvent(event)
        self._update_appearance()
        if self.isMaximized():
            self.btn_max.set_icon_type("restore")
        else:
            self.btn_max.set_icon_type("maximize")