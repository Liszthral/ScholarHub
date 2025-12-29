"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - MainWindow
    Version: Alpha 1.0.0
    UpdateTime: 2025-1228-2350
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon

class MainWindow:
    def __init__(self, MainConfig):
        """ <1> Basic window construction information """
        self.MainWindow = QWidget()
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowTitle(MainConfig.get("ProgramInformation", "Name"))
        self.MainWindow.resize(1920, 1080)
        self.MainWindow.setWindowIcon(QIcon(MainConfig.get("ProgramInformation", "IconPath")))


        self.MainWindow.showMaximized()
