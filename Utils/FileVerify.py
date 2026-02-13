"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - Utils - FileVerify
    Version: Release 1.0.0
    UpdateTime: 2026-0212-1513
"""

import re

ILLEGAL_CHARS = r'\\/:*?"<>|'  # This does not include '.', pay attention to preventing path crossing!
RETAIN_KEYWORDS = [
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
]

def verifyFileName(fileName: str) -> tuple[bool, str]:
    fileName = str(fileName)
    """ <1> Check for illegal characters. """
    if re.search(rf'[{ILLEGAL_CHARS}]', fileName):
        return False, 'include illegal characters'
    """ <2> Check for retain keywords. """
    part = fileName.split('.')[0]
    if part in RETAIN_KEYWORDS:
        return False, 'Include retain keywords'
    """ <3> Check for path traversal. """
    if ('..' in fileName) or (fileName == '..') or (fileName == '.'):
        return False, 'Perhaps path traversal'
    """ <4> None of the 3 detected guard statements triggered an alarm. """
    return True, 'Correct'
