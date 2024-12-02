# Packaging python projects

# PyInstaller

[PyInstaller](https://pyinstaller.org/en/stable/) bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules. PyInstaller supports Python 3.8 and newer, and correctly bundles many major Python packages such as numpy, matplotlib, PyQt, wxPython, and others.

PyInstaller is tested against Windows, MacOS X, and Linux.

However, it is not a cross-compiler; to make a Windows app you run PyInstaller on Windows, and to make a Linux app you run it on Linux, etc.

## Minimal example