"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - PaperMgrWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class PaperMgrWindow(QWidget):

    index = 10
    name = 'PaperMgrWindow'

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI
        self.setObjectName("PaperMgrWindow")



        self.setStyleSheet("""
            background-color: rgb(240, 240, 240);
            font-family: Arial;
        """)

        # 添加一些示例内容
        layout = QVBoxLayout()

        label = QLabel("PaperMgrWindow")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(label)

        # 添加返回按钮
        back_button = QPushButton("返回主界面")
        back_button.clicked.connect(lambda: self.toHomeWindow())
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
        layout.addWidget(back_button)

        layout.addStretch()
        self.setLayout(layout)

    def toHomeWindow(self):
        if self.UI:
            self.UI.toHomePage()
        else:
            print("not found main window")
