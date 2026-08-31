# NanUI 开发路线图

---

### 🧩 第一阶段：常用基础控件（全部完成）

- [x] **1. `Window`**（窗口基类）：无边框圆角窗口，标题栏可拖动，内置最小化/最大化/关闭，可选调整大小
- [x] **2. `Label`**（标签）：圆角样式，可自定义字体和字号
- [x] **3. `PushButton`**（按钮）：圆角 + 悬停/按下/禁用，可选主题化投影
- [x] **4. `LineEdit`**（单行输入框）：圆角 / 占位文字色 / 自定义右键菜单
- [x] **5. `TextEdit`**（多行文本框）：圆角边框 / 自定义右键菜单
- [x] **6. `CheckBox`**（复选框）：QSS 自绘圆角指示器 + 勾选图标
- [x] **7. `RadioButton`**（单选按钮）：圆形指示器，同父控件自动互斥
- [x] **8. `ComboBox`**（下拉选择框）：自定义箭头 / 下拉列表圆角 / `setItems()`
- [x] **9. `ProgressBar`**（进度条）：圆角进度块，可自定义范围 / 格式

---

### 🗂️ 第二阶段：基础设施与项目规范

- [x] **10. 统一颜色方案**：`theme_manager.THEME_COLORS`（light / dark 双色板）
- [x] **11. 统一字体管理**：`utils/fonts.py` 的 `get_font()`，默认微软雅黑
- [x] **12. 顶层导出**：`from NanUI import Window, Label, ...` 可用
- [x] **13. utils 工具函数导出**：`center_window` 已在 `helpers.py` 实现，但  
  `from NanUI.utils import center_window` 还不行 —— 把 helpers 的函数加进 `utils/__init__.py`

---

### 🖼️ 第三阶段：容器与布局

- [x] **14. `Card`**（卡片容器）：圆角样式由 `QFrame#card` 控制，可指定 V/H 布局
- [x] **15. `ScrollArea`**（滚动区域）：滚动条美化，`addWidget()` / `setContentLayout()`

---

### 🎨 第四阶段：主题系统

- [x] **16. 暗色主题**：`styles/dark_theme.qss`（中性石墨色板，7 级海拔梯度）
- [x] **17. ThemeManager**：`apply_theme()` / `get_color()` / `apply_themed_shadow()`
- [x] **18. 动态换肤**：自绘控件、投影、占位文字全部走主题，运行时切换立即生效

---

### 🛠️ 第五阶段：实用工具函数

- [x] **19. 窗口居中**：`utils/helpers.py` 的 `center_window()`（多显示器 + 排除任务栏）
- [x] **20. 资源管理**：`resources.qrc` + `pyside6-rcc` 编译 + 暗色图标

---

### ✅ 第六阶段：测试与质量保障（原第十三阶段提前，重中之重）

- [x] **21. 测试框架落地**：pytest + `QT_QPA_PLATFORM=offscreen`，CI 里能跑
- [x] **22. 控件基础测试**：每个控件至少一条（能创建、关键信号正常、主题切换不崩）
- [x] **23. 视觉回归测试**：离屏渲染 + 逐像素对比，QSS / 主题改动自动验证零回归
  （`tests/test_visual_regression.py`：18 场景 × light/dark 两主题，基线按平台分目录存
  `tests/baselines/<platform>/<theme>/`，`--update-baseline` 重新生成，失败时差异图涂红；
  覆盖 hover / pressed / disabled / checked 态与 Window 最大化圆角）
- [x] **24. 代码规范**：ruff 格式化 + pre-commit 钩子
  （`pyproject.toml` 配置 ruff：py38 目标 / 88 行宽 / isort 保"NanUI 在前"约定 /
  E501 交给 formatter；`.pre-commit-config.yaml` 固定 rev v0.16.5，
  ruff --fix + ruff-format 双钩子；负向验证：违规代码被拦截并自动修复）
- [x] **25. 类型标注**：全库补 type hints，生成 `.pyi` 供 IDE 提示
  （20 源文件全补 `Optional`/`List` 标注（py38 兼容），mypy 严格校验从 57 错误降到 0，
  顺带修复 2 个真实缺陷——`_squared_corners` 可空性、`scroll_area.widget()` None 解引用，
  并全库 Qt6 枚举规范化 `Qt.MouseButton.LeftButton` 等；
  `stubgen` 生成 `stubs/` 19 个 `.pyi` 外置存根（MYPYPATH 指向即生效），
  包内加 `py.typed` 标记，pip 用户直接从源码获得类型提示；
  `setup.py` / `MANIFEST.in` 已纳入打包，`pyproject.toml` 的 ruff exclude 排除生成产物）

---

### 📦 第七阶段：对话框与窗口体系

- [ ] **26. `MessageBox`**（消息弹窗）：信息 / 警告 / 错误三态，自定义标题、文案、按钮
- [ ] **27. `Dialog`**（通用对话框基类）：继承 `Window`，确定 / 取消按钮 + `accept` / `reject` 信号
- [ ] **28. 原生对话框主题化**：`QFileDialog` / `QColorDialog` / `QInputDialog`

---

### 📘 第八阶段：文档与示例

- [x] **29. README.md**：基础内容已写；**待补：控件效果截图 / GIF（当前最大硬伤）**
- [x] **30. examples/**：01 窗口 ~ 09 进度条，一个控件一个文件（已建）
- [x] **31. Docstring 全库统一**：Google 风格 + 统一模板（已完成）
- [ ] **32. 组合示例**：设置页 / 登录页 / 仪表盘，展示控件的组合用法

---

### 🚀 第九阶段：打包与发布

- [x] **33. setup.py**：已有 `include_package_data`；发布前补 `long_description`、`classifiers`，  
  并复核 wheel 里确实带上了 `.qss` 和 `resources_rc.py`
- [x] **34. 全新环境安装测试**：`pip install -e .` 验证（发布前对 wheel 再验一次）
- [x] **35. Git 仓库**：`.gitignore` + main 分支 + 推送到 GitHub
- [ ] **36. 版本策略**：semver 承诺 + 弃用（deprecation）机制，进入 1.0 前定下来

---

### 🔧 第十阶段：高频基础控件补全（新增，P0）

> 写真实应用每天都要用，优先级高于 Tree / Table。

- [ ] **37. `FormLayout`**（表单布局）：设置窗口 / Dialog 的地基，目前完全没有
- [ ] **38. `MenuBar` / `Menu` 控件化**：原生 `QMenu` 已有样式，补 `QMenuBar`
- [ ] **39. `ToolBar`**（工具栏）
- [ ] **40. `StatusBar`**（状态栏）
- [ ] **41. `GroupBox`**（分组框）
- [ ] **42. `StackedWidget`**（页面切换）
- [ ] **43. `ListWidget` / `ListView`**（列表）

---

### 🧩 第十一阶段：高级控件（原第九阶段）

- [ ] **44. `Slider`**（滑块）：滑条 + 手柄美化，支持水平 / 垂直
- [ ] **45. `TabWidget`**（选项卡）：圆角页头 / 选中态 / 关闭按钮 / 滚动
- [ ] **46. `TreeWidget`**（树形控件）
- [ ] **47. `TableWidget`**（表格控件）：表头 / 交替色 / 选中高亮 / 排序
- [ ] **48. `DateEdit` / `DateTimeEdit`**（日期时间选择器）
- [ ] **49. `SpinBox`**（数字输入框）：与 LineEdit 风格一致
- [ ] **50. P1 补充**（可选）：`DoubleSpinBox`、`ToolButton`、`CalendarWidget`、  
  `SearchBox`（LineEdit+图标）、`PasswordBox`（echoMode）

---

### 🎨 第十二阶段：布局与交互增强

- [ ] **51. `Splitter`**（分割器）：可拖拽分割条
- [ ] **52. `ToolTip` 主题化**：悬停提示与主题统一
- [ ] **53. `Notification`**（通知弹窗）：角落滑出，信息 / 成功 / 警告 / 错误，自动消失
- [ ] **54. `LoadingIndicator`**（加载指示器）：旋转 Spinner
- [ ] **55. 动画 / 过渡封装**：hover 过渡、页面切换淡入淡出（`QPropertyAnimation`）
- [ ] **56. 拖放支持**：控件级 drag & drop
- [ ] **57. 高 DPI 图标**：图标资源补 2x 版本

---

### 🛠️ 第十三阶段：开发工具与调试

- [ ] **58. `nanui-cli`**：`nanui create <project>` / `nanui run`
- [ ] **59. `nanui --version`** 与 `print_version()`
- [ ] **60. 调试模式**：`enable_debug()` 打印控件层级、样式加载状态
- [ ] **61. 异常处理友好化**：主题加载 / 资源编译失败时不静默

---

### ⚙️ 第十四阶段：CI 与发布自动化

- [ ] **62. GitHub Actions**：自动测试 + 构建 wheel + Release 时发布 PyPI
- [ ] **63. 覆盖率**：pytest-cov + README 徽章
- [ ] **64. 性能基准**：100+ 控件场景的启动 / 渲染耗时基线

---

### 📚 第十五阶段：文档与社区

- [ ] **65. Sphinx API 文档**：由 docstring 生成，托管 GitHub Pages / Read the Docs
- [ ] **66. "从零开始"教程**：安装与第一个窗口 / 布局与控件 / 主题定制 / 打包发布
- [ ] **67. CONTRIBUTING.md**（贡献指南）
- [ ] **68. CODE_OF_CONDUCT.md**（行为准则）
- [ ] **69. CHANGELOG.md**（更新日志）
- [ ] **70. 架构 / 设计文档**：新控件开发 checklist、主题扩展规范  
  （把项目记忆里的约定产品化：继承原生类 → 外观进 QSS → `get_font` → docstring 模板 → QSS 分区注释）
- [ ] **71. Logo 与品牌**

---

### 🌍 第十六阶段：国际化与可访问性

- [ ] **72. i18n**：右键菜单文案抽取为可翻译字符串，默认中 / 英
- [ ] **73. 键盘导航**：Tab 顺序、快捷键、**focus-visible 焦点环**（现在按 Tab 无视觉反馈）
- [ ] **74. 无障碍与对比度**：`accessibleName`、`QAccessible`、WCAG 对比度检查

---

### 🎨 第十七阶段：更多主题与设计资源

- [ ] **75. "灰白极简"主题**
- [ ] **76. "深蓝科技"主题**
- [ ] **77. 在线主题预览 / 配置器**（可选，高阶目标）

---

### 🧪 第十八阶段：示例应用（Showcase）

- [ ] **78. 记事本**：菜单 / 工具栏 / 状态栏 / 多标签页（会反哺第十阶段的控件）
- [ ] **79. 系统监控**：进度条 / 表格 / 图表（`matplotlib` 或 `pyqtgraph`）

---
