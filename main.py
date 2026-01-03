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

from PyQt6.QtWidgets import QApplication
from WindowsUI import MainWindow
from Utils import JsonReader, Logger
import sys, os, threading

TEMP = {"MAIN_PATH": os.path.dirname(os.path.realpath(__file__)) + "\\"}

class ProcessManager:
    _lock = threading.Lock()
    _instance = None  # 私有静态实例
    _mutex = threading.Lock()  # 互斥锁（线程安全）

    def __new__(cls, *args, **kwargs):
        # 第一次检查（锁外）：由来：性能优化，跳过不必要的加锁
        if cls._instance is None:
            # 加锁：由来：保证临界区原子执行，解决多线程并发问题
            with cls._mutex:
                # 第二次检查（锁内）：由来：防止等待锁的线程重复创建实例
                if cls._instance is None:
                    # 创建实例：由来：依赖父类__new__的内置能力，创建对象
                    cls._instance = super(ProcessManager, cls).__new__(cls)
        # 返回实例：由来：__new__的职责就是返回实例，同时保证每次返回同一个缓存实例
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

    ProcessManager = ProcessManager()



    MainWindow = MainWindow.MainWindow(MainConfig, logger, TEMP)
    for i in range(18):
        MainWindow.AddFuncButton(f"TEST{i}", lambda: print("TEST"))


    # Window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    # ui = uic.loadUi("untitled.ui")
    # ui.show()


    logger.info("Started Successfully")

    sys.exit(app.exec())
