from PySide6.QtWidgets import QTextEdit, QMenu, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from NanUI.utils import get_font

class TextEdit(QTextEdit):
    """
    多行文本框控件。

    继承自 QTextEdit。预设了圆角、有无焦点时的样式，并可自定义字体和字体大小。
    右键菜单与 LineEdit 风格保持一致。

    Args:
        parent (QWidget, optional): 父控件对象，默认为 None。
        font (str): 字体族名称，若不传则使用全局默认。
        font_size (int): 字体大小，默认为 11。
        placeholder (str): 占位提示文本（若 PySide6 版本支持）。
    """
    def __init__(self, parent=None, font: str = None, font_size: int = 11, placeholder: str = ''):
        super().__init__(parent)

        self.setFont(get_font(size=font_size, family=font))
        if placeholder:
            self.setPlaceholderText(placeholder)

        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # ---- 撤回 ----
        acUndo = QAction('撤回', self)
        acUndo.triggered.connect(self.undo)
        acUndo.setEnabled(self.document().isUndoAvailable())
        acUndo.setShortcut(QKeySequence.Undo)

        # ---- 重做 ----
        acRedo = QAction('重做', self)
        acRedo.triggered.connect(self.redo)
        acRedo.setEnabled(self.document().isRedoAvailable())
        acRedo.setShortcut(QKeySequence.Redo)

        # ---- 剪切 ----
        acCut = QAction('剪切', self)
        acCut.triggered.connect(self.cut)
        acCut.setEnabled(self.textCursor().hasSelection())
        acCut.setShortcut(QKeySequence.Cut)

        # ---- 复制 ----
        acCopy = QAction('复制', self)
        acCopy.triggered.connect(self.copy)
        acCopy.setEnabled(self.textCursor().hasSelection())
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
        acDelete.setEnabled(True)

        # ---- 全选 ----
        acSelectAll = QAction('全选', self)
        acSelectAll.triggered.connect(self.selectAll)
        acSelectAll.setEnabled(True)
        acSelectAll.setShortcut(QKeySequence.SelectAll)

        # ---- 清空 ----
        acDeleteAll = QAction('清空', self)
        acDeleteAll.triggered.connect(lambda: self.setText(''))

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

    def _delete_action(self):
        """删除选中的文本，如果无选中则删除光标后一个字符（相当于 Delete 键）"""
        cursor = self.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()   # 删除选中部分
        else:
            cursor.deleteChar()           # 删除光标后面的一个字符
        # 不需要 self.setTextCursor(cursor)，因为 cursor 是对内部光标对象的引用，修改已生效