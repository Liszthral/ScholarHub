"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub
    Version: Alpha 1.0.0
    UpdateTime: 2025-1221-2239
"""
from PyQt6.QtCore import QThread
# import pyttsx3 as speaker
# from docx import Document

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from Utils import JsonReader, Logger
from WindowsUI import HomeWindow
import sys, os, threading



TEMP = {"MAIN_PATH": os.path.dirname(os.path.realpath(__file__)) + "\\"}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        """ <1> Basic window construction information. """
        self.setObjectName("MainWindow")
        self.setWindowTitle("ScholarHub")
        self.resize(1920, 1080)

        """ <2> 关键：创建中央部件 """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # 必须设置中央部件！

        """ <3> 创建布局 """
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        """ <4> Stacked Window. """
        self.StackWidget = QStackedWidget()
        main_layout.addWidget(self.StackWidget)

        """ <5> 创建所有页面 """
        self.create_all_pages()

        """ <6> 连接信号 """
        self.connect_signals()

        """ <7> 显示主页 """
        self.switch_page(0)

    def create_all_pages(self):
        """创建所有页面"""
        # 创建页面实例
        self.home_page = HomeWindow.HomeWindow()

        # 添加到堆叠窗口
        self.StackWidget.addWidget(self.home_page)  # 索引0

    def connect_signals(self):
        """连接所有信号"""
        # 主页按钮 -> 切换到对应页面
        self.home_page.goto_page1_signal.connect(lambda: self.switch_page(1))


        # 子页面返回按钮 -> 返回主页
        # 假设每个子页面都有 go_back_signal 信号

    def switch_page(self, index):
        """切换页面"""
        if 0 <= index < self.StackWidget.count():
            self.StackWidget.setCurrentIndex(index)
            print(f"切换到页面索引: {index}")


class ProcessManager:
    _lock = threading.Lock()
    _instance = None
    _mutex = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._mutex:
                if cls._instance is None:
                    cls._instance = super(ProcessManager, cls).__new__(cls)
        return cls._instance

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        memo[id(self)] = self
        return self

    def __init__(self):
        pass


def ExitProgram():
    MainConfig.save()
    logger.info("Exiting Program Normal")
    logger.save_log()

if __name__ == '__main__':
    logger = Logger.Logger(TEMP["MAIN_PATH"] + r"log\log.log")
    logger.info("Started Initialization")
    MainConfig = JsonReader.JsonReader(TEMP["MAIN_PATH"] + r"Configuration\MainConfig.json", logger)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(ExitProgram)

    TEMP["ScreenSize"] = app.primaryScreen().geometry().getRect()[2:]

    process_manager = ProcessManager()

    window = MainWindow()
    window.show()

    logger.info("Started Successfully")
    sys.exit(app.exec())
