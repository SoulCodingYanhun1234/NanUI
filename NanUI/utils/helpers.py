from PySide6.QtWidgets import QApplication, QWidget


def center_window(window: QWidget) -> None:
    """
    把窗口移动到所在屏幕可用区域的中央。

    使用窗口所在屏幕（支持多显示器）的可用区域（排除任务栏）来计算，
    因此窗口不会跑到主屏去，也不会被任务栏挡住。

    Args:
        window (QWidget): 要居中的窗口。一般传已 resize 过的窗口。

    Returns:
        None。
    """
    screen = window.screen() or QApplication.primaryScreen()
    if screen is None:  # 极端情况下没有屏幕，直接放弃
        return
    geo = screen.availableGeometry()
    size = window.size()
    x = geo.x() + (geo.width() - size.width()) // 2
    y = geo.y() + (geo.height() - size.height()) // 2
    window.move(x, y)
