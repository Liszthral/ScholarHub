"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - Utils - Logger
    Version: Release 1.0.2
    UpdateTime: 2026-0103-2350
"""

import os
import time

class Logger:

    LogTemp = """"""

    def __init__(self, APath):
        """
        :param APath: The absolute path of the program whose logs are being recorded.
        """
        DirPath = os.path.dirname(APath)
        if DirPath and not os.path.exists(DirPath):
            os.makedirs(DirPath, exist_ok=True)
            try:
                with open(APath, "w", encoding="utf-8") as f:
                    pass
            except (IOError, OSError) as e:
                raise ValueError(f"Failed to initialize log file: {e}") from e
        self.APath = APath

    def reset(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self.APath = path

    def info(self, msg):
        content = self.get_time() + " [INFO] " + str(msg) + "\n"
        self.LogTemp += content

    def error(self, msg):
        content = self.get_time() + " [ERROR] " + str(msg) + "\n"
        self.LogTemp += content

    def warning(self, msg):
        content = self.get_time() + " [WARNING] " + str(msg) + "\n"
        self.LogTemp += content

    def critical(self, msg):
        content = self.get_time() + " [CRITICAL] " + str(msg) + "\n"
        self.LogTemp += content

    def save_log(self):
        with open(self.APath, "a+", encoding="utf-8") as f:
            for i in self.LogTemp.split("\n"):
                f.write(i + "\n")
        self.LogTemp = """"""

    @staticmethod
    def get_time():
        RecordTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return RecordTime
