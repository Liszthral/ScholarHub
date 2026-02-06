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

    index = 0
    name = 'HomeWindow'

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

    ButtonObject = []


    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI  # 保存对主窗口的引用
        self.initUI()


    def initUI(self):

        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(10, 10, 10, 10)
        self.Layout.addStretch()
        self.ButtonGrid = QGridLayout()

        self.SettingsW = QPushButton("SettingsWindow")
        self.TaskW = QPushButton("TaskWindow")
        self.BufferW = QPushButton("BufferWindow")
        self.DeviceMgrW = QPushButton("DeviceMgrWindow")
        self.FocusW = QPushButton("FocusWindow")
        self.GradeRecordW = QPushButton("GradeRecordWindow")
        self.VocabularyW = QPushButton("VocabularyWindow")
        self.PoemW = QPushButton("PoemWindow")
        self.TeachingAIDSW = QPushButton("TeachingAIDSWindow")
        self.PaperMgrW = QPushButton("PaperMgrWindow")
        self.LadderW = QPushButton("LadderWindow")
        self.AchievementW = QPushButton("AchievementWindow")
        self.MusicW = QPushButton("MusicWindow")
        self.PitchW = QPushButton("PitchWindow")
        self.MusicalityW = QPushButton("MusicalityWindow")
        self.AlarmW = QPushButton("AlarmWindow")
        self.FileProtectW = QPushButton("FileProtectWindow")
        self.ButtonObject = [
            self.SettingsW, self.TaskW, self.BufferW, self.DeviceMgrW, self.FocusW,
            self.GradeRecordW, self.VocabularyW, self.PoemW, self.TeachingAIDSW, self.PaperMgrW,
            self.LadderW, self.AchievementW, self.MusicW, self.PitchW, self.MusicalityW,
            self.AlarmW, self.FileProtectW
        ]

        self.SettingsW.clicked.connect(self.gotoSettingsW.emit)
        self.TaskW.clicked.connect(self.gotoTaskW.emit)
        self.BufferW.clicked.connect(self.gotoBufferW.emit)
        self.DeviceMgrW.clicked.connect(self.gotoDeviceMgrW.emit)
        self.FocusW.clicked.connect(self.gotoFocusW.emit)
        self.GradeRecordW.clicked.connect(self.gotoGradeRecordW.emit)
        self.VocabularyW.clicked.connect(self.gotoVocabularyW.emit)
        self.PoemW.clicked.connect(self.gotoPoemW.emit)
        self.TeachingAIDSW.clicked.connect(self.gotoTeachingAIDSW.emit)
        self.PaperMgrW.clicked.connect(self.gotoPaperMgrW.emit)
        self.LadderW.clicked.connect(self.gotoLadderW.emit)
        self.AchievementW.clicked.connect(self.gotoAchievementW.emit)
        self.MusicW.clicked.connect(self.gotoMusicW.emit)
        self.PitchW.clicked.connect(self.gotoPitchW.emit)
        self.MusicalityW.clicked.connect(self.gotoMusicalityW.emit)
        self.AlarmW.clicked.connect(self.gotoAlarmW.emit)
        self.FileProtectW.clicked.connect(self.gotoFileProtectW.emit)

        x, y = 0, 0
        for obj in self.ButtonObject:
            obj.setObjectName('FuncButton')
            obj.setMinimumHeight(40)
            self.ButtonGrid.addWidget(obj, x, y)
            y += 1
            if y >= 5: x += 1; y = 0
        self.Layout.addLayout(self.ButtonGrid)



