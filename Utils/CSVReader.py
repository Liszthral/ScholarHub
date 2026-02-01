"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - Utils - CSVReader
    Version: Alpha 1.0.0
    UpdateTime: 2026-0126-2344
"""
import csv


def test(path):
    with open(path, 'r', encoding='utf-8') as f:
        csvr = csv.reader(f, delimiter=',', quotechar='"')
    print(csvr)


# class CSVReader:
#
#     data = {}
#
#     def __init__(self, path):
#         self.path = path
#         self.read()
#
#     def read(self):
#         with open(self.path, 'r', encoding='utf-8') as f:
#             print(f.read())

if __name__ == '__main__':
    test(r'test.csv')
    # a = CSVReader()