"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: logging
    Version: Alpha 1.0.0
    UpdateTime: 2025-1104-2356
"""

import os
import time

class Logger:

    def __init__(self, APath):
        """
        :param APath: The absolute path of the program whose logs are being recorded.
        """
        if not os.path.exists(APath):
            os.makedirs(APath)
        self.APath = APath + r"/RunLog.log"
