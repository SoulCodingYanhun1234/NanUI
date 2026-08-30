from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="NanUI",
    version="0.2.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    description="一个基于 PySide6 的自定义 UI 组件库",
    python_requires=">=3.8",
    author="NanbeiTnT",
    license="MIT",

    include_package_data=True,
    package_data={
        "NanUI": [
            "styles/*.qss",
            "resources/*.py",
        ],
    },
)