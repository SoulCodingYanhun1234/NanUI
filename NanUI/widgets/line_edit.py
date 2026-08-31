from PySide6.QtWidgets import QApplication, QLineEdit, QMenu
from NanUI.utils import get_font
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction, QKeySequence

class LineEdit(QLineEdit):
    """
    单行输入框控件。

    继承自 QLineEdit。预设了圆角、有无焦点时的样式（由 QSS 主题控制），
    并可自定义字体和字号。拥有自定义右键菜单（撤回、重做、剪切、复制、粘贴、删除、全选、清空）。

    Args:
        text (str): 输入框内的初始文本。默认为空字符串。
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str, optional): 字体族名称。默认为 None，即使用全局默认字体（微软雅黑）。
        font_size (int): 字体大小（磅值）。默认为 14。
        placeholder (str): 框内没有文本时显示的提示文本。默认为空字符串。
    """
    def __init__(self, text: str = '', parent = None, font: str = None, font_size: int = 14, placeholder: str = ''):
        super().__init__(text, parent)

        self.setFont(get_font(size=font_size, family=font))
        if placeholder:
            self.setPlaceholderText(placeholder)

        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # ---- 撤回 ----
        acUndo = QAction('撤回', self)
        acUndo.triggered.connect(self.undo)
        acUndo.setEnabled(self.isUndoAvailable())
        acUndo.setShortcut(QKeySequence.Undo)

        # ---- 重做 ----
        acRedo = QAction('重做', self)
        acRedo.triggered.connect(self.redo)
        acRedo.setEnabled(self.isRedoAvailable())
        acRedo.setShortcut(QKeySequence.Redo)

        # ---- 剪切 ----
        acCut = QAction('剪切', self)
        acCut.triggered.connect(self.cut)
        acCut.setEnabled(self.hasSelectedText())
        acCut.setShortcut(QKeySequence.Cut)

        # ---- 复制 ----
        acCopy = QAction('复制', self)
        acCopy.triggered.connect(self.copy)
        acCopy.setEnabled(self.hasSelectedText())
        acCopy.setShortcut(QKeySequence.Copy)

        # ---- 粘贴 ----
        acPaste = QAction('粘贴', self)
        acPaste.triggered.connect(self.paste)
        clipboard = QApplication.clipboard()
        acPaste.setEnabled(bool(clipboard.text()))
        acPaste.setShortcut(QKeySequence.Paste)

        # ---- 删除 ----
        acDelete = QAction('删除', self)
        acDelete.triggered.connect(self._delete_action)
        acDelete.setEnabled(self.hasSelectedText())

        # ---- 全选 ----
        acSelectAll = QAction('全选', self)
        acSelectAll.triggered.connect(self.selectAll)
        acSelectAll.setEnabled(True)
        acSelectAll.setShortcut(QKeySequence.SelectAll)

        # ---- 清空 ----
        acClear = QAction('清空', self)
        acClear.triggered.connect(self.clear)
        acClear.setEnabled(bool(self.text()))

        # ---- 组装菜单 ----
        menu.addAction(acUndo)
        menu.addAction(acRedo)
        menu.addSeparator()
        menu.addAction(acCut)
        menu.addAction(acCopy)
        menu.addAction(acPaste)
        menu.addAction(acDelete)
        menu.addSeparator()
        menu.addAction(acSelectAll)
        menu.addAction(acClear)

        menu.exec(event.globalPos())

    # ---------- 槽 ----------
    def _delete_action(self):
        """删除选中的文本（如果没有选中则删除光标后一个字符，但 LineEdit 通常只删除选中）"""
        if self.hasSelectedText():
            cursor_pos = self.cursorPosition()
            start = self.selectionStart()
            end = start + len(self.selectedText())
            self.setText(self.text()[:start] + self.text()[end:])
            self.setCursorPosition(start)