import os
from PySide6.QtWidgets import QApplication

def apply_theme(app: QApplication, theme_name: str = "light") -> bool:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    styles_dir = os.path.join(current_dir, "..", "styles")
    theme_file = os.path.join(styles_dir, f"{theme_name}_theme.qss")
    try:
        with open(theme_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        return True
    except FileNotFoundError:
        print(f"警告：未找到主题文件 {theme_file}")
        return False