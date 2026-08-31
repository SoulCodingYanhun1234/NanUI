"""pytest 全局配置（第 21 项：测试框架落地）。

作用：
1. 在 import PySide6 之前把 Qt 切到 offscreen 平台 —— 无显示器环境（CI）也能渲染。
   注意：这行必须放在本文件最顶部，任何 Qt 相关 import 之前。
2. 提供全局唯一的 QApplication（Qt 不允许创建第二个实例，所以用 session 级 fixture）。

用法（在 NanUI 仓库根目录）：
    python -m pytest          # 跑全部测试
    python -m pytest -k theme # 只跑名字里带 theme 的测试
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """全局唯一 QApplication。session 级：整个测试过程只创建一次。

    用 `QApplication.instance()` 先取再建，保证即使测试之外已经建过
    （比如某个调试脚本先跑）也不会创建第二个实例。
    """
    app = QApplication.instance() or QApplication([])
    yield app


def pytest_addoption(parser):
    """命令行选项：--update-baseline 重新生成视觉回归基线。

    用于第 23 项的 tests/test_visual_regression.py：改完 QSS / 主题色板、
    确认新效果是预期时，用该参数把 tests/baselines/ 下的 PNG 全部重新生成，
    之后恢复正常模式对比新基线。
    """
    parser.addoption(
        "--update-baseline",
        action="store_true",
        default=False,
        help="重新生成视觉回归基线（tests/baselines/），不做逐像素对比",
    )


@pytest.fixture
def update_baseline(request):
    """是否处于 --update-baseline 模式。"""
    return request.config.getoption("--update-baseline")
