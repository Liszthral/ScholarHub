"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - MainWindow
    Version: Alpha 1.0.0
    UpdateTime: 2025-1228-2350
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFontDatabase
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QIcon



class MainWindow:

    ButtonPosLine = 0
    ButtonPosColum = 0

    def __init__(self, MainConfig, logger, TEMP):
        """ <1> Basic window construction information. """
        self.logger = logger
        self.TEMP = TEMP
        self.MainWindow = QWidget()
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowTitle(MainConfig.get("ProgramInformation", "Name"))
        self.MainWindow.resize(1920, 1080)
        self.MainWindow.setWindowIcon(QIcon(MainConfig.get("ProgramInformation", "IconPath")))

        """ <2> Function page jump button combination. """
        self.MainWindowFuncButtonWidget = QtWidgets.QWidget(parent=self.MainWindow)
        self.MainWindowFuncButtonWidget.setGeometry(QtCore.QRect(
            20, self.TEMP["ScreenSize"][1] // 2,
            self.TEMP["ScreenSize"][0] - 50,
            self.TEMP["ScreenSize"][1] - (self.TEMP["ScreenSize"][1] // 2) - 40))
        self.MainWindowFuncButtonWidget.setObjectName("MainWindowFuncButtonWidget")
        self.FuncButtonWidgets = QtWidgets.QGridLayout(self.MainWindowFuncButtonWidget)
        self.FuncButtonWidgets.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.FuncButtonWidgets.setContentsMargins(10, 10, 10, 10)
        self.FuncButtonWidgets.setObjectName("MainWindowFuncButtonWidgets")

        """ <3> render UI. """
        self.LoadQSS(MainConfig.get("QSSPath", "MainWindow"))
        self.MainWindow.showMaximized()

    def RegisterFont(self, path):
        pass

    def LoadQSS(self, path):
        try:
            QFontDatabase.addApplicationFont(r"D:\· ScholarHub\MediaFile\font\CC Round Black.ttf")
            with open(self.TEMP["MAIN_PATH"] + path, "r", encoding="utf-8") as f:
                self.logger.info("Started loading QSS at <MainWindow>")
                content = f.read()
                self.MainWindow.setStyleSheet(content)
                self.logger.info("Loading QSS at <MainWindow> Successfully")
        except FileNotFoundError:
            self.logger.warning("QSS at <MainWindow> not found at <MainWindow>")

    def AddFuncButton(self, name, func):
        Button = QtWidgets.QPushButton(name, self.MainWindow)
        Button.setObjectName("FuncButton")
        Button.clicked.connect(func)
        self.FuncButtonWidgets.addWidget(Button, self.ButtonPosLine, self.ButtonPosColum, 1, 1)
        self.ButtonPosColum += 1
        if self.ButtonPosColum >= 5:
            self.ButtonPosColum = 0
            self.ButtonPosLine += 1
