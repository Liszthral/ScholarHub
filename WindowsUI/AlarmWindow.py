"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - AlarmWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class AlarmWindow(QWidget):

    index = 2

    def __init__(self, main_window_ref=None):
        super().__init__()
        self.main_window = main_window_ref


