"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - TaskWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QScrollArea

class TaskWindow(QWidget):

    index = 2
    name = 'TaskWindow'

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI  # 保存对主窗口的引用
        self.setObjectName("TaskWindow")

        # 添加返回按钮
        back_button = QPushButton("返回主界面")
        back_button.clicked.connect(lambda: self.UI.toHomePage())
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # 主垂直布局：顶部放返回按钮，下方放四象限网格
        self.layout = QVBoxLayout()
        self.layout.addWidget(back_button)
        self.setLayout(self.layout)

        self.initQUAD()

    def initQUAD(self):
        """ 创建四个象限区域，并使用网格布局排列成2×2的四象限形式 """
        # 创建四个象限控件
        self.QUAD1 = QWidget(self)
        self.QUAD2 = QWidget(self)
        self.QUAD3 = QWidget(self)
        self.QUAD4 = QWidget(self)

        # 设置对象名
        self.QUAD1.setObjectName("QUAD1")
        self.QUAD2.setObjectName("QUAD2")
        self.QUAD3.setObjectName("QUAD3")
        self.QUAD4.setObjectName("QUAD4")

        # 为每个象限创建垂直布局（方便后续添加内容）
        self.QUAD1Layout = QVBoxLayout()
        self.QUAD2Layout = QVBoxLayout()
        self.QUAD3Layout = QVBoxLayout()
        self.QUAD4Layout = QVBoxLayout()

        # 将布局设置给对应的象限控件
        self.QUAD1.setLayout(self.QUAD1Layout)
        self.QUAD2.setLayout(self.QUAD2Layout)
        self.QUAD3.setLayout(self.QUAD3Layout)
        self.QUAD4.setLayout(self.QUAD4Layout)

        # 设置背景色（仍使用红色，您可以根据需要修改）
        self.QUAD1.setStyleSheet('background-color: #f02050;')
        self.QUAD2.setStyleSheet('background-color: #20f050;')
        self.QUAD3.setStyleSheet('background-color: #2050f0;')
        self.QUAD4.setStyleSheet('background-color: #20f500;')

        # 创建网格布局，将四个象限放置于2×2网格中
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.QUAD1, 0, 0)
        grid_layout.addWidget(self.QUAD2, 0, 1)
        grid_layout.addWidget(self.QUAD3, 1, 0)
        grid_layout.addWidget(self.QUAD4, 1, 1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        # scroll.setWidget(self.ButtonWidget)

        # 设置网格行列拉伸，使四个象限均匀分布
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        # 将网格布局添加到主垂直布局中（位于返回按钮下方）
        self.layout.addLayout(grid_layout)
