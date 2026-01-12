"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - EngSettingsWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""

from PyQt6.QtWidgets import QWidget

class EngSettingsWindow:

    def __init__(self):
        """ <1> Basic window construction information. """
        self.EngSettingsWindow = QWidget()
        self.EngSettingsWindow.resize(800, 600)
        self.EngSettingsWindow.setObjectName("EngSettingsWindow")
        self.EngSettingsWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.EngSettingsWindow.showFullScreen()
