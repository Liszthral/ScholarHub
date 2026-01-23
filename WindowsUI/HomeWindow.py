"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - MainWindow
    Version: Alpha 1.0.0
    UpdateTime: 2025-1228-2350
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal


class HomeWindow(QWidget):
    goto_page1_signal = pyqtSignal()

    def __init__(self):
        print("HomeWindow运行正常")
        super().__init__()
        self.setup_ui()


    def setup_ui(self):
        """设置主页UI"""
        print("HomeWindow设置UI")
        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("🏠 主页面")
        title.setStyleSheet("color: #2c3e50; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 按钮网格
        grid = QGridLayout()

        # 创建5个按钮
        self.btn1 = QPushButton("📊 页面一")
        self.btn2 = QPushButton("📈 页面二")
        self.btn3 = QPushButton("📉 页面三")
        self.btn4 = QPushButton("📋 页面四")
        self.btn5 = QPushButton("🔧 页面五")

        # 设置按钮样式
        for btn in [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5]:
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

        # 添加到网格
        grid.addWidget(self.btn1, 0, 0)
        grid.addWidget(self.btn2, 0, 1)
        grid.addWidget(self.btn3, 1, 0)
        grid.addWidget(self.btn4, 1, 1)
        grid.addWidget(self.btn5, 2, 0, 1, 2)  # 跨两列

        layout.addLayout(grid)
        layout.addStretch()

        # 连接信号
        self.btn1.clicked.connect(self.goto_page1_signal.emit)





#
# from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
#                              QStackedWidget, QPushButton, QLabel)
# from PyQt6.QtGui import QFontDatabase, QIcon
# from PyQt6 import QtCore, QtWidgets
# from WindowsUI.EngSettingsWindow import EngSettingsWindow
#
# class MainWindow(QWidget):
#     ButtonPosLine = 0
#     ButtonPosColum = 0
#
#     def __init__(self, MainConfig, logger, TEMP):
#         super().__init__()
#
#         self.logger = logger
#         self.TEMP = TEMP
#         self.MainConfig = MainConfig
#         self.pages = {}
#
#         """ <1> 基本窗口构造信息 """
#         self.setObjectName("MainWindow")
#         self.setWindowTitle(MainConfig.get("ProgramInformation", "Name"))
#         self.resize(1920, 1080)
#
#         icon_path = MainConfig.get("ProgramInformation", "IconPath")
#         if icon_path:
#             try:
#                 self.setWindowIcon(QIcon(icon_path))
#             except FileNotFoundError:
#                 self.logger.warning(f"Failed to load icon from {icon_path}")
#
#         """ <2> 创建主布局 """
#         main_layout = QVBoxLayout(self)
#         main_layout.setContentsMargins(20, 20, 20, 20)
#         main_layout.setSpacing(10)
#
#         """ <3> 创建标题区域 """
#         title_label = QLabel(MainConfig.get("ProgramInformation", "Name", "ScholarHub"))
#         title_label.setObjectName("TitleLabel")
#         title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#         title_label.setStyleSheet("""
#             font-size: 24px;
#             font-weight: bold;
#             color: #2c3e50;
#             padding: 10px;
#             border-bottom: 2px solid #3498db;
#         """)
#         main_layout.addWidget(title_label)
#
#         """ <4> 创建按钮区域 """
#         button_widget = QWidget()
#         button_widget.setObjectName("ButtonWidget")
#         self.FuncButtonWidgets = QtWidgets.QGridLayout(button_widget)
#         self.FuncButtonWidgets.setContentsMargins(10, 10, 10, 10)
#         self.FuncButtonWidgets.setSpacing(15)
#
#         # 添加主页按钮
#         home_button = QPushButton("主页")
#         home_button.setObjectName("HomeButton")
#         home_button.clicked.connect(self.switch_to_home)
#         self.FuncButtonWidgets.addWidget(home_button, 0, 0, 1, 1)
#
#         main_layout.addWidget(button_widget)
#
#         """ <5> 创建QStackedWidget用于页面切换 """
#         self.stacked_widget = QStackedWidget()
#         main_layout.addWidget(self.stacked_widget, 1)
#
#         """ <6> 创建主页面 """
#         self.home_page = self.create_home_page()
#         self.stacked_widget.addWidget(self.home_page)
#         self.pages["home"] = 0
#
#         """ <7> 初始化其他窗口 """
#         self.eng_settings_window = None
#
#         """ <8> 渲染UI """
#         # self.LoadQSS(MainConfig.get("QSSPath", "MainWindow", "default.qss"))
#         self.showMaximized()
#
#     def create_home_page(self):
#         """创建主页面"""
#         home_page = QWidget()
#         layout = QVBoxLayout(home_page)
#
#         welcome_label = QLabel("欢迎使用 ScholarHub")
#         welcome_label.setStyleSheet("""
#             font-size: 36px;
#             font-weight: bold;
#             color: #2c3e50;
#             padding: 50px;
#         """)
#         welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(welcome_label)
#
#         instruction_label = QLabel("请点击上方按钮使用功能")
#         instruction_label.setStyleSheet("""
#             font-size: 18px;
#             color: #7f8c8d;
#         """)
#         instruction_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(instruction_label)
#
#         layout.addStretch()
#         return home_page
#
#     def RegisterFont(self, path):
#         try:
#             font_id = QFontDatabase.addApplicationFont(path)
#             if font_id != -1:
#                 self.logger.info(f"Successfully registered font: {path}")
#             else:
#                 self.logger.warning(f"Failed to register font: {path}")
#         except Exception as e:
#             self.logger.error(f"Error registering font {path}: {e}")
#
#     def LoadQSS(self, path):
#         try:
#             full_path = self.TEMP["MAIN_PATH"] + path
#             with open(full_path, "r", encoding="utf-8") as f:
#                 self.logger.info(f"Started loading QSS at {full_path}")
#                 content = f.read()
#                 self.setStyleSheet(content)
#                 self.logger.info("Loading QSS Successfully")
#         except FileNotFoundError:
#             self.logger.warning(f"QSS file not found: {path}")
#             # 设置默认样式
#             self.setStyleSheet("""
#                 QWidget {
#                     font-family: Arial, sans-serif;
#                 }
#                 QPushButton {
#                     background-color: #3498db;
#                     color: white;
#                     border: none;
#                     padding: 10px 20px;
#                     border-radius: 5px;
#                     font-size: 14px;
#                 }
#                 QPushButton:hover {
#                     background-color: #2980b9;
#                 }
#                 QPushButton#HomeButton {
#                     background-color: #2ecc71;
#                 }
#                 QPushButton#HomeButton:hover {
#                     background-color: #27ae60;
#                 }
#                 QLabel#TitleLabel {
#                     font-size: 24px;
#                     font-weight: bold;
#                     color: #2c3e50;
#                 }
#             """)
#
#     def AddFuncButton(self, name, func=None):
#         """添加功能按钮"""
#         # 计算按钮位置
#         row = self.ButtonPosLine
#         col = self.ButtonPosColum + 1  # 跳过第一列的主页按钮
#
#         if col > 5:  # 每行最多5个功能按钮
#             col = 1
#             row += 1
#
#         Button = QPushButton(name, self)
#         Button.setObjectName("FuncButton")
#
#         if func:
#             Button.clicked.connect(func)
#
#         self.FuncButtonWidgets.addWidget(Button, row, col, 1, 1)
#
#         self.ButtonPosColum += 1
#         if self.ButtonPosColum >= 5:  # 每行最多5个功能按钮
#             self.ButtonPosColum = 0
#             self.ButtonPosLine += 1
#
#     def switch_to_eng_settings(self):
#         """切换到工程设置窗口"""
#         if self.eng_settings_window is None:
#             self.eng_settings_window = EngSettingsWindow(self)
#             index = self.stacked_widget.addWidget(self.eng_settings_window)
#             self.pages["eng_settings"] = index
#         else:
#             index = self.pages["eng_settings"]
#
#         self.stacked_widget.setCurrentIndex(index)
#
#     def switch_to_home(self):
#         """切换回主页"""
#         self.stacked_widget.setCurrentIndex(self.pages["home"])