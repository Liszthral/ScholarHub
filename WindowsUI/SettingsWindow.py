"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - SettingsWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class SettingsWindow(QWidget):

    index = 1
    name = 'SettingsWindow'

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI

        self.setObjectName("SettingsWindow")
        self.setStyleSheet("""
            background-color: rgb(250, 250, 250);
            font-family: Arial;
        """)

        # 添加一些示例内容
        layout = QVBoxLayout()

        label = QLabel("SettingsWindow")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(label)

        label1 = QLabel("CNM")
        label1.move(20, 200)
        label1.setStyleSheet("color: #353;")
        layout.addWidget(label1)

        # 添加返回按钮
        back_button = QPushButton("返回主界面")
        back_button.clicked.connect(self.go_back_to_main)
        back_button.setMaximumWidth(50)
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

        layout.addWidget(self.UI.turnHomeButton())



        layout.addStretch()
        self.setLayout(layout)

    def go_back_to_main(self):
        """返回到主界面"""
        if self.UI:
            self.UI.toHomePage()
        else:
            print("not found main window")

    def getName(self):
        return self.name
