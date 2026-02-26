"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - Utils - Logger
    Version: Release 1.1.1
    UpdateTime: 2026-0215-2300
"""

import os
import time
import threading

def out(func):
    def wrapper(self, msg):
        content = func(self, msg)
        print(content, end='')
        return content
    return wrapper

class Logger:
    _instance = None
    _init_flag = False
    _mutex = threading.Lock()

    LogTemp = """"""

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._mutex:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        memo[id(self)] = self
        return self

    def __init__(self, APath):
        """
        :param APath: Absolute path of log file.
        """
        if Logger._init_flag:
            return
        with Logger._mutex:
            if Logger._init_flag:
                return
            DirPath = os.path.dirname(APath)
            if DirPath and not os.path.exists(DirPath):
                os.makedirs(DirPath, exist_ok=True)
            try:
                with open(APath, "a+", encoding="utf-8") as f:
                    f.write('\n')
            except (IOError, OSError) as e:
                raise ValueError(f"Failed to initialize log file: {e}") from e
            self.APath = APath
            Logger._init_flag = True

    def reset(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        self.APath = path

    @out
    def info(self, msg):
        content = self.get_time() + " [INFO] " + str(msg) + "\n"
        self.LogTemp += content
        return content

    @out
    def error(self, msg):
        content = self.get_time() + " [ERROR] " + str(msg) + "\n"
        self.LogTemp += content
        return content

    @out
    def warning(self, msg):
        content = self.get_time() + " [WARNING] " + str(msg) + "\n"
        self.LogTemp += content
        return content

    @out
    def critical(self, msg):
        content = self.get_time() + " [CRITICAL] " + str(msg) + "\n"
        self.LogTemp += content
        return content

    def save_log(self):
        with open(self.APath, "a+", encoding="utf-8") as f:
            f.write(self.LogTemp)
        self.LogTemp = ""

    @staticmethod
    def get_time():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
