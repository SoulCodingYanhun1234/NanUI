from typing import Optional

from PySide6.QtGui import QFont

DEFAULT_FAMILY = "Microsoft YaHei"


def get_font(
    size: int = 12,
    weight: QFont.Weight = QFont.Weight.Normal,
    family: Optional[str] = None,
    italic: bool = False,
    underline: bool = False,
) -> QFont:
    """
    获取一个配置好的 QFont 对象。

    如果不传入 family，则自动使用全局默认字体（DEFAULT_FAMILY）。
    这样外部调用时只需关心字号和粗细，字体库由库统一管理。

    Args:
        size(int): 字体大小。
        weight(int): 字体粗细，如 QFont.Weight.Normal, QFont.Weight.Bold, QFont.Weight.Light
        family(str): 字体族名称。
        italic(bool): 是否斜体。
        underline(bool): 是否下划线。

    Returns:
        QFont 对象。
    """
    if family is None:
        family = DEFAULT_FAMILY

    font = QFont(family, size)
    font.setWeight(weight)
    font.setItalic(italic)
    font.setUnderline(underline)

    return font


def get_default_font(size: int = 12) -> QFont:
    """获取默认字体（常规粗细）"""
    return get_font(size=size, weight=QFont.Weight.Normal)


def get_bold_font(size: int = 12) -> QFont:
    """获取加粗字体"""
    return get_font(size=size, weight=QFont.Weight.Bold)


def get_light_font(size: int = 12) -> QFont:
    """获取细体字"""
    return get_font(size=size, weight=QFont.Weight.Light)
