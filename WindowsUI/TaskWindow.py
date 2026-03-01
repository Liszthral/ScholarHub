"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - TaskWindow
    Version: Alpha 1.0.1
    UpdateTime: 2026-0115-1030
"""

import csv, time
from main import MAIN_PATH
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QGridLayout, QScrollArea, QFrame, QHBoxLayout
)



class TaskWindow(QWidget):

    index = 2
    name = 'TaskWindow'
    UrgAndImt = []  # Imt = Important
    UrgNotImt = []  # Urg = Urgent
    ImtNotUrg = []
    NotUrgImt = []

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI
        self.setObjectName("TaskWindow")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()
        self.loadLocalTask()

    def initUI(self):
        self.layout.addWidget(self.UI.turnWidgetButton('HomeWindow'))
        self.initQUAD()

    def loadLocalTask(self):
        with open(MAIN_PATH / 'Data' / 'TaskWindow' / 'Task.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                self.QUAD1Layout.addWidget(TaskWidget(
                    content=row['content'],
                    createTime=row['createTime'],
                    endTime=row['endTime'],
                    finishTime=row['finishTime'],
                    loopMode=row['loopMode'],
                    sonTask=row['sonTask']
                ))

    def initQUAD(self):

        # 创建四个内容部件（用于放置任务项）
        self.QUAD1 = QWidget()
        self.QUAD2 = QWidget()
        self.QUAD3 = QWidget()
        self.QUAD4 = QWidget()

        # 为每个内容部件设置垂直布局
        self.QUAD1Layout = QVBoxLayout()
        self.QUAD2Layout = QVBoxLayout()
        self.QUAD3Layout = QVBoxLayout()
        self.QUAD4Layout = QVBoxLayout()

        self.QUAD1.setLayout(self.QUAD1Layout)
        self.QUAD2.setLayout(self.QUAD2Layout)
        self.QUAD3.setLayout(self.QUAD3Layout)
        self.QUAD4.setLayout(self.QUAD4Layout)

        # 设置内容部件背景色（浅色，便于阅读）
        self.QUAD1.setObjectName("QUAD1")
        self.QUAD2.setObjectName("QUAD2")
        self.QUAD3.setObjectName("QUAD3")
        self.QUAD4.setObjectName("QUAD4")

        # 为每个内容部件创建滚动区域
        self.scroll1 = QScrollArea()
        self.scroll2 = QScrollArea()
        self.scroll3 = QScrollArea()
        self.scroll4 = QScrollArea()

        for scroll in (self.scroll1, self.scroll2, self.scroll3, self.scroll4):
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.Shape.NoFrame)

        # 将内容部件设置到对应的滚动区域中
        self.scroll1.setWidget(self.QUAD1)
        self.scroll2.setWidget(self.QUAD2)
        self.scroll3.setWidget(self.QUAD3)
        self.scroll4.setWidget(self.QUAD4)

        # 创建网格布局，放入四个滚动区域
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.scroll1, 0, 0)
        grid_layout.addWidget(self.scroll2, 0, 1)
        grid_layout.addWidget(self.scroll3, 1, 0)
        grid_layout.addWidget(self.scroll4, 1, 1)

        # 设置行列拉伸，使四个象限均匀分布
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        # 将网格布局添加到主布局
        self.layout.addLayout(grid_layout)

        # 为每个象限添加测试数据
        self.addTestData()

    def addTestData(self):
        """为四个象限添加测试任务项"""
        # 定义每个象限的标题和对应的布局
        quadrants = [
            ("重要且紧急", self.QUAD1Layout),
            ("重要不紧急", self.QUAD2Layout),
            ("不重要但紧急", self.QUAD3Layout),
            ("不重要不紧急", self.QUAD4Layout),
        ]

        for title, layout in quadrants:
            # 添加标题
            title_label = QLabel(f"【{title}】")
            # title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
            layout.addWidget(title_label)
            # 底部添加弹簧，使内容靠上排列
            layout.addStretch()


class TaskWidget(QWidget):

    def __init__(self,
                 content="Default task", createTime=int(time.time()), endTime=int(time.time()),
                 finishTime=None, loopMode="once", sonTask=None):
        super().__init__()
        self.content = content
        self.createTime = createTime
        self.endTime = endTime
        self.finishTime = finishTime
        self.loopMode = loopMode
        self.sonTask = sonTask

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # IMPORTANT!
        self.setObjectName("TaskWidget")
        self.initWidget()

    def initWidget(self):

        self.layout = QVBoxLayout()
        self.layout.setObjectName("TaskWidget")
        self.setLayout(self.layout)

        self.InfoBar = QHBoxLayout()
        self.InfoBarLeft = QVBoxLayout()
        self.InfoBarRight = QVBoxLayout()

        self.ContentLabel = QLabel(str(self.content))
        self.ContentLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ContentLabel.setObjectName("ContentLabel")

        CreateTime = time.gmtime(int(self.createTime))
        self.CreateTimeLabel = QLabel("创建于：" + str(time.strftime("%Y-%m-%d %H:%M:%S", CreateTime)))
        self.CreateTimeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.CreateTimeLabel.setObjectName("CreateTimeLabel")

        EndTime = time.gmtime(int(self.endTime))
        self.EndTimeLabel = QLabel("截止于：" + str(time.strftime("%Y-%m-%d %H:%M:%S", EndTime)))
        self.EndTimeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.EndTimeLabel.setObjectName("EndTimeLabel")

        FinishTime = time.gmtime(int(self.finishTime))
        self.FinishTimeLabel = QLabel("完成于：" + str(time.strftime("%Y-%m-%d %H:%M:%S", FinishTime)))
        self.FinishTimeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.FinishTimeLabel.setObjectName("FinishTimeLabel")

        self.InfoBarLeft.addWidget(self.ContentLabel)
        self.InfoBarLeft.addWidget(self.CreateTimeLabel)
        self.InfoBarLeft.addWidget(self.EndTimeLabel)
        self.InfoBarLeft.addWidget(self.FinishTimeLabel)

        self.ConfigButton = QPushButton('更改')
        self.ConfigButton.setObjectName("ConfigButton")
        self.ConfigButton.clicked.connect(self.configTask)

        self.CompleteButton = QPushButton('完成')
        self.CompleteButton.setObjectName("CompleteButton")
        self.CompleteButton.clicked.connect(self.completeTask)

        self.DeleteButton = QPushButton('删除')
        self.DeleteButton.setObjectName("DeleteButton")
        self.DeleteButton.clicked.connect(self.deleteTask)

        self.InfoBarRight.addWidget(self.ConfigButton)
        self.InfoBarRight.addWidget(self.CompleteButton)
        self.InfoBarRight.addWidget(self.DeleteButton)

        self.InfoBar.addLayout(self.InfoBarLeft)
        self.InfoBar.addStretch()
        self.InfoBar.addLayout(self.InfoBarRight)
        self.layout.addLayout(self.InfoBar)

        self.SonTaskBar = QVBoxLayout()

    def configTask(self):
        print(1)

    def completeTask(self):
        print(2)

    def deleteTask(self):
        self.destroy()


