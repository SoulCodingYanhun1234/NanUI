from typing import Optional

from NanUI.utils import get_font

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QContextMenuEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QMenu, QTextEdit, QWidget


class TextEdit(QTextEdit):
    """
    多行文本框控件。

    继承自 QTextEdit。预设了圆角、有无焦点时的样式（由 QSS 主题控制），
    并可自定义字体和字号。右键菜单与 LineEdit 风格保持一致。

    Args:
        parent (QWidget, optional): 父控件对象。默认为 None。
        font (str, optional): 字体族名称。默认为 None，即使用全局默认字体（微软雅黑）。
        font_size (int): 字体大小（磅值）。默认为 11。
        placeholder (str): 框内没有文本时显示的提示文本。默认为空字符串。
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        font: Optional[str] = None,
        font_size: int = 11,
        placeholder: str = "",
    ) -> None:
        super().__init__(parent)

        self.setFont(get_font(size=font_size, family=font))
        if placeholder:
            self.setPlaceholderText(placeholder)

        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)

        # ---- 撤回 ----
        acUndo = QAction("撤回", self)
        acUndo.triggered.connect(self.undo)
        acUndo.setEnabled(self.document().isUndoAvailable())
        acUndo.setShortcut(QKeySequence.StandardKey.Undo)

        # ---- 重做 ----
        acRedo = QAction("重做", self)
        acRedo.triggered.connect(self.redo)
        acRedo.setEnabled(self.document().isRedoAvailable())
        acRedo.setShortcut(QKeySequence.StandardKey.Redo)

        # ---- 剪切 ----
        acCut = QAction("剪切", self)
        acCut.triggered.connect(self.cut)
        acCut.setEnabled(self.textCursor().hasSelection())
        acCut.setShortcut(QKeySequence.StandardKey.Cut)

        # ---- 复制 ----
        acCopy = QAction("复制", self)
        acCopy.triggered.connect(self.copy)
        acCopy.setEnabled(self.textCursor().hasSelection())
        acCopy.setShortcut(QKeySequence.StandardKey.Copy)

        # ---- 粘贴 ----
        acPaste = QAction("粘贴", self)
        acPaste.triggered.connect(self.paste)
        clipboard = QApplication.clipboard()
        acPaste.setEnabled(bool(clipboard.text()))
        acPaste.setShortcut(QKeySequence.StandardKey.Paste)

        # ---- 删除 ----
        acDelete = QAction("删除", self)
        acDelete.triggered.connect(self._delete_action)
        acDelete.setEnabled(True)

        # ---- 全选 ----
        acSelectAll = QAction("全选", self)
        acSelectAll.triggered.connect(self.selectAll)
        acSelectAll.setEnabled(True)
        acSelectAll.setShortcut(QKeySequence.StandardKey.SelectAll)

        # ---- 清空 ----
        acDeleteAll = QAction("清空", self)
        acDeleteAll.triggered.connect(lambda: self.setText(""))

        # ---- 添加到菜单 ----
        menu.addAction(acUndo)
        menu.addAction(acRedo)
        menu.addSeparator()
        menu.addAction(acCut)
        menu.addAction(acCopy)
        menu.addAction(acPaste)
        menu.addAction(acDelete)
        menu.addSeparator()
        menu.addAction(acSelectAll)
        menu.addAction(acDeleteAll)

        menu.exec(event.globalPos())

    def _delete_action(self) -> None:
        """删除选中的文本，如果无选中则删除光标后一个字符（相当于 Delete 键）"""
        cursor = self.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()  # 删除选中部分
        else:
            cursor.deleteChar()  # 删除光标后面的一个字符
        # 不需要 self.setTextCursor(cursor)，因为 cursor 是对内部光标对象的引用，修改已生效
