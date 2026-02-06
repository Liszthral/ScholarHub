"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - TeachingAIDSWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""
import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget


class TeachingAIDSWindow(QWidget):

    index = 9
    name = 'TeachingAIDSWindow'
    UI = None

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI

        self.setObjectName("TeachingAIDSWindow")
        self.VLayout = QVBoxLayout()
        self.setLayout(self.VLayout)

        self.StackPage = QStackedWidget()
        self.VLayout.addWidget(self.StackPage)

        self.initUI()

        self.VLayout.addStretch()


    def initUI(self):
        """ <1> Top information bar. """
        self.VLayout.addWidget(self.UI.turnHomeButton())
        """ <2> Iterate and render classification based on the corresponding directory. """
        Dir1 = QVBoxLayout()
        Dir1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        for i in os.listdir('./TeachingAIDS'):
            Button = QPushButton(i)
            Button.setMinimumHeight(30)
            Button.clicked.connect(lambda: self.turnDir2Render(i))
            Dir1.addWidget(Button)
        self.VLayout.addLayout(Dir1)


    def turnDir2Render(self, path):

        self.StackPage.addWidget(ShowAIDSInfo(path))
        print(path)
        self.StackPage.setCurrentIndex(0)

    def go_back_to_main(self):
        """返回到主界面"""
        if self.UI:
            self.UI.toHomePage()
        else:
            print("not found main window")


class ShowAIDSInfo(QWidget):

    def __init__(self, path):
        super().__init__()
        layout = QHBoxLayout()
        button = QPushButton(path)
        layout.addWidget(button)
        self.setLayout(layout)

        self.show()
