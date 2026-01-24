"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - VocabularyWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class VocabularyWindow(QWidget):

    # index = 1

    def __init__(self, main_window_ref=None):
        super().__init__()
        self.main_window = main_window_ref  # 保存对主窗口的引用

        self.setObjectName("VocabularyWindow")
        self.setStyleSheet("""
            background-color: rgb(240, 240, 240);
            font-family: Arial;
        """)

        # 添加一些示例内容
        layout = QVBoxLayout()

        label = QLabel("工程设置窗口")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(label)

        # 添加返回按钮
        back_button = QPushButton("返回主界面")
        back_button.clicked.connect(self.go_back_to_main)
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

    def go_back_to_main(self):
        """返回到主界面"""
        if self.main_window:
            self.main_window.toHomePage()
        else:
            print("not found main window")
