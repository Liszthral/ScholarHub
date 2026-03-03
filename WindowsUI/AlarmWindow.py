"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - AlarmWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""
import csv

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QFrame, \
    QDialog

from main import MAIN_PATH


class AlarmWindow(QWidget):

    name = 'AlarmWindow'
    row = 0
    line = 0
    alarm = []

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()
        self.layout.addStretch()

    def initUI(self):
        self.TopBar = QHBoxLayout()
        self.TopBar.addWidget(self.UI.turnWidgetButton('HomeWindow'))
        self.TopBar.addStretch()
        self.layout.addLayout(self.TopBar)

        self.AlarmArea = QWidget()
        self.AlarmArea.setObjectName("AlarmWindow-AlarmWidget")
        self.AlarmScroll = QScrollArea()
        self.AlarmLayout = QGridLayout()
        self.AlarmScroll.setWidgetResizable(True)
        self.AlarmScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.AlarmScroll.setWidget(self.AlarmArea)
        self.AlarmArea.setLayout(self.AlarmLayout)
        self.layout.addWidget(self.AlarmScroll)

        self.LoadLocalAlarm()

    def addAlarmWidget(self, RingTime='12:00:00', LoopMode='once', Remark='Default Alarm',
                       RetainMode='delete after ring', RingMusic='test'):
        print('添加闹钟控件1')
        self.AlarmLayout.addWidget(AlarmWidget(RingTime, LoopMode, Remark, RetainMode, RingMusic), 0, 0)
        print('添加闹钟控件2')

    def LoadLocalAlarm(self):
        with open(MAIN_PATH / "Data" / "AlarmWindow" / "Alarm.csv", "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                self.addAlarmWidget(
                    RingTime=row['RingTime'],
                    LoopMode=row['LoopMode'],
                    Remark=row['Remark'],
                    RetainMode=row['RetainMode'],
                    RingMusic=row['RingMusic']
                )
                print('读取本地闹钟文件')

    def createAlarm(self):
        CreateDiaLog = QDialog()
        CreateDiaLog.show()




class AlarmWidget(QWidget):

    def __init__(self, RingTime='12:00:00', LoopMode='once', Remark='Default Alarm',
                 RetainMode='delete after ring', RingMusic='test'):
        super().__init__()
        self.RingTime = RingTime
        self.LoopMode = LoopMode
        self.Remark = Remark
        self.RetainMode = RetainMode
        self.RingMusic = RingMusic

        self.setObjectName("AlarmWidget")
        self.setMaximumHeight(100)
        self.setMaximumWidth(220)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()

    def initUI(self):
        print('AlarmWidget 开始初始化UI')
        self.InfoBar = QHBoxLayout()
        self.InfoBarLeft = QVBoxLayout()
        self.InfoBarRight = QVBoxLayout()

        self.RingTimeLabel = QLabel(str(self.RingTime))
        self.RingTimeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.RingTimeLabel.setObjectName("RingTimeLabel")

        self.RemarkLabel = QLabel(str(self.Remark))
        self.RemarkLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.RemarkLabel.setObjectName("RemarkLabel")

        self.ModeLabel = QLabel(f"{self.LoopMode} | {self.RetainMode}")
        self.ModeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ModeLabel.setObjectName("ModeLabel")

        self.InfoBarLeft.addWidget(self.RingTimeLabel)
        self.InfoBarLeft.addWidget(self.RemarkLabel)
        self.InfoBarLeft.addWidget(self.ModeLabel)

        self.ConfigButton = QPushButton('更改')
        self.ConfigButton.setObjectName("ConfigButton")
        self.ConfigButton.clicked.connect(self.configAlarm)

        self.CompleteButton = QPushButton('完成')
        self.CompleteButton.setObjectName("CompleteButton")
        self.CompleteButton.clicked.connect(self.completeAlarm)

        self.DeleteButton = QPushButton('删除')
        self.DeleteButton.setObjectName("DeleteButton")
        self.DeleteButton.clicked.connect(self.deleteAlarm)

        self.InfoBarRight.addWidget(self.ConfigButton)
        self.InfoBarRight.addWidget(self.CompleteButton)
        self.InfoBarRight.addWidget(self.DeleteButton)

        self.InfoBar.addLayout(self.InfoBarLeft)
        self.InfoBar.addStretch()
        self.InfoBar.addLayout(self.InfoBarRight)
        self.layout.addLayout(self.InfoBar)

    def configAlarm(self):
        print(1)

    def completeAlarm(self):
        print(2)

    def deleteAlarm(self):
        self.destroy()
