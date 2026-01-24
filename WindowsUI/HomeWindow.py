"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - HomeWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0124-2114
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout
from PyQt6.QtCore import pyqtSignal


class HomeWindow(QWidget):

    gotoSettingsW = pyqtSignal()
    gotoTaskW = pyqtSignal()
    gotoBufferW = pyqtSignal()
    gotoDeviceMgrW = pyqtSignal()
    gotoFocusW = pyqtSignal()
    gotoGradeRecordW = pyqtSignal()
    gotoVocabularyW = pyqtSignal()
    gotoPoemW = pyqtSignal()
    gotoTeachingAIDSW = pyqtSignal()
    gotoPaperMgrW = pyqtSignal()
    gotoLadderW = pyqtSignal()
    gotoAchievementW = pyqtSignal()
    gotoMusicW = pyqtSignal()
    gotoPitchW = pyqtSignal()
    gotoMusicalityW = pyqtSignal()
    gotoAlarmW = pyqtSignal()
    gotoFileProtectW = pyqtSignal()



    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):

        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(10, 10, 10, 10)
        self.Layout.addStretch()
        self.ButtonGrid = QGridLayout()

        x, y = 0, 0
        for i in range(17):
            if y >= 5:
                y = 0
                x += 1
            btn = QPushButton(f"页面{i}")
            btn.setMinimumHeight(60)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #2c3e50;
                    color: white;
                }
            """)
            self.ButtonGrid.addWidget(btn, x, y)
            btn.clicked.connect(self.gotoLadderW.emit)
            y += 1

        self.Layout.addLayout(self.ButtonGrid)



