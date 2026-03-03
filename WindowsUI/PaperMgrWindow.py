"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - PaperMgrWindow
    Version: Alpha 1.0.1
    UpdateTime: 2026-0303-1800
"""

import csv
from main import MAIN_PATH
from Utils import FloatMessage

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QFormLayout, QLineEdit, QSpinBox, QTextEdit,
    QDialogButtonBox, QMessageBox
)


class PaperMgrWindow(QWidget):
    """试卷管理主窗口：以表格形式展示所有试卷，支持增删改查"""

    index = 10
    name = "PaperMgrWindow"

    # CSV 字段定义（与表头顺序一致）
    FIELDS = ["Name", "Number", "TotalCount", "WrongNumbers", "Remark"]

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI
        self.setObjectName("PaperMgrWindow")
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)

        self.initUI()
        self.loadData()

    def initUI(self):
        """初始化界面：顶部工具栏 + 试卷表格"""
        # 顶部工具栏
        topBar = QHBoxLayout()
        topBar.addWidget(self.UI.turnWidgetButton("HomeWindow"))

        # 新增试卷按钮
        self.AddButton = QPushButton("新增试卷")
        self.AddButton.setObjectName("AddPaperButton")
        self.AddButton.clicked.connect(self.addPaper)
        topBar.addWidget(self.AddButton)

        # 手动保存按钮（每次修改会自动保存，但保留以符合用户习惯）
        self.SaveButton = QPushButton("保存")
        self.SaveButton.setObjectName("SavePaperButton")
        self.SaveButton.clicked.connect(lambda: self.saveToCSV(showMsg=True))
        topBar.addWidget(self.SaveButton)

        topBar.addStretch()
        self.Layout.addLayout(topBar)

        # 试卷表格
        self.Table = QTableWidget()
        self.Table.setObjectName("PaperTable")
        self.Table.setColumnCount(len(self.FIELDS) + 1)  # 多一列操作用
        self.Table.setHorizontalHeaderLabels(self.FIELDS + ["操作"])
        self.Table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.Table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 禁止直接编辑
        self.Table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.Table.verticalHeader().setVisible(False)

        self.Layout.addWidget(self.Table)

    def loadData(self):
        """从 CSV 文件加载数据并填充表格（兼容旧版单字段 TotalQuestions）"""
        csvPath = MAIN_PATH / "Data" / "PaperMgrWindow" / "Paper.csv"
        if not csvPath.exists():
            # 创建空文件并写入表头（新表头）
            csvPath.parent.mkdir(parents=True, exist_ok=True)
            with open(csvPath, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDS, delimiter=";")
                writer.writeheader()
            self.UI.logger.info(f"PaperMgrWindow - 创建空文件 {csvPath}")
            return

        try:
            with open(csvPath, "r", encoding="utf-8-sig") as f:
                # 读取第一行判断字段数，以兼容旧文件
                first_line = f.readline().strip()
                f.seek(0)  # 重置文件指针
                delimiter = ';'
                if first_line:
                    fields = first_line.split(delimiter)
                else:
                    fields = []

                # 如果是旧版文件（只有4列：Name,Number,TotalQuestions,Remark）
                if len(fields) == 4 and fields[2] == "TotalQuestions":
                    self.UI.logger.warning("PaperMgrWindow - 检测到旧版CSV格式，将自动转换为新版")
                    # 读取旧数据
                    reader = csv.DictReader(f, delimiter=delimiter)
                    old_rows = list(reader)
                    # 转换为新数据：TotalQuestions 拆分为 TotalCount 和 WrongNumbers（错题号默认空）
                    new_rows = []
                    for row in old_rows:
                        total_q = row.get("TotalQuestions", "0")
                        # 如果 total_q 包含逗号，可能已包含错题号？但旧版没有错题号，所以直接作为总题量，错题号留空
                        new_row = {
                            "Name": row.get("Name", ""),
                            "Number": row.get("Number", ""),
                            "TotalCount": total_q,
                            "WrongNumbers": "",  # 旧数据无法提取错题号，留空
                            "Remark": row.get("Remark", "")
                        }
                        new_rows.append(new_row)
                    # 用新数据重新写入文件
                    with open(csvPath, "w", encoding="utf-8-sig", newline="") as fw:
                        writer = csv.DictWriter(fw, fieldnames=self.FIELDS, delimiter=delimiter)
                        writer.writeheader()
                        writer.writerows(new_rows)
                    # 重新读取新文件
                    f = open(csvPath, "r", encoding="utf-8-sig")
                    reader = csv.DictReader(f, delimiter=delimiter)
                    rows = list(reader)
                    f.close()
                else:
                    # 正常读取新格式
                    reader = csv.DictReader(f, delimiter=delimiter)
                    rows = list(reader)

            self.Table.setRowCount(len(rows))
            for rowIdx, rowData in enumerate(rows):
                # 确保所有字段都存在（防止旧数据缺失 WrongNumbers）
                for field in self.FIELDS:
                    if field not in rowData:
                        rowData[field] = ""

                for colIdx, field in enumerate(self.FIELDS):
                    item = QTableWidgetItem(rowData[field])
                    # 设置对齐方式：TotalCount 列居中，其他居左
                    if field == "TotalCount":
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    else:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.Table.setItem(rowIdx, colIdx, item)

                # 在最后一列添加“编辑”和“删除”按钮
                self._addActionButtons(rowIdx)

            self.UI.logger.info(f"PaperMgrWindow - 成功加载 {len(rows)} 条试卷记录")
        except Exception as e:
            FloatMessage.FloatMessage(f"加载试卷失败：{e}", bg_color="#ff2020", text_color="#000000")
            self.UI.logger.error(f"PaperMgrWindow - loadData 异常：{e}")

    def _addActionButtons(self, row):
        """为指定行添加操作按钮（编辑、删除）"""
        btnWidget = QWidget()
        layout = QHBoxLayout(btnWidget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)

        editBtn = QPushButton("编辑")
        editBtn.setObjectName("EditPaperButton")
        editBtn.clicked.connect(lambda checked, r=row: self.editPaper(r))
        layout.addWidget(editBtn)

        deleteBtn = QPushButton("删除")
        deleteBtn.setObjectName("DeletePaperButton")
        deleteBtn.clicked.connect(lambda checked, r=row: self.deletePaper(r))
        layout.addWidget(deleteBtn)

        self.Table.setCellWidget(row, len(self.FIELDS), btnWidget)

    def saveToCSV(self, showMsg=False):
        """将表格当前内容保存到 CSV 文件（分号分隔）"""
        csvPath = MAIN_PATH / "Data" / "PaperMgrWindow" / "Paper.csv"
        rows = self.Table.rowCount()
        data = []
        for row in range(rows):
            rowDict = {}
            for col, field in enumerate(self.FIELDS):
                item = self.Table.item(row, col)
                rowDict[field] = item.text() if item else ""
            data.append(rowDict)

        try:
            with open(csvPath, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDS, delimiter=";")
                writer.writeheader()
                writer.writerows(data)
            if showMsg:
                FloatMessage.FloatMessage("试卷已保存", bg_color="#33cc33", text_color="#000000")
            self.UI.logger.info("PaperMgrWindow - 保存 CSV 成功")
        except Exception as e:
            FloatMessage.FloatMessage(f"保存失败：{e}", bg_color="#ff2020", text_color="#000000")
            self.UI.logger.error(f"PaperMgrWindow - saveToCSV 异常：{e}")

    def addPaper(self):
        """弹出新增试卷对话框，添加记录后自动保存"""
        dialog = AddPaperDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            row = self.Table.rowCount()
            self.Table.insertRow(row)

            # 填充数据
            for col, field in enumerate(self.FIELDS):
                item = QTableWidgetItem(data[field])
                if field == "TotalCount":
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.Table.setItem(row, col, item)

            # 添加操作按钮
            self._addActionButtons(row)

            # 自动保存
            self.saveToCSV(showMsg=False)
            FloatMessage.FloatMessage("试卷已添加", bg_color="#33cc33", text_color="#000000")
            self.UI.logger.info(f"PaperMgrWindow - 新增试卷：{data['Name']}")

    def editPaper(self, row):
        """弹出编辑试卷对话框，更新指定行"""
        # 获取当前行数据
        currentData = {}
        for col, field in enumerate(self.FIELDS):
            item = self.Table.item(row, col)
            currentData[field] = item.text() if item else ""

        dialog = EditPaperDialog(self, currentData)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            newData = dialog.getData()
            # 更新表格行
            for col, field in enumerate(self.FIELDS):
                item = self.Table.item(row, col)
                item.setText(newData[field])
                if field == "TotalCount":
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            # 自动保存
            self.saveToCSV(showMsg=False)
            FloatMessage.FloatMessage("试卷已更新", bg_color="#33cc33", text_color="#000000")
            self.UI.logger.info(f"PaperMgrWindow - 编辑试卷：{newData['Name']}")

    def deletePaper(self, row):
        """删除指定行，需二次确认"""
        nameItem = self.Table.item(row, 0)  # 试卷名称列
        paperName = nameItem.text() if nameItem else "未知"
        reply = QMessageBox.question(
            self,
            "确认删除",
            f'确定要删除试卷“{paperName}”吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.Table.removeRow(row)
            self.saveToCSV(showMsg=False)
            FloatMessage.FloatMessage("试卷已删除", bg_color="#33cc33", text_color="#000000")
            self.UI.logger.info(f"PaperMgrWindow - 删除试卷：{paperName}")


class AddPaperDialog(QDialog):
    """新增试卷对话框（包含总题量和错题序号两个输入）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新增试卷")
        self.setObjectName("AddPaperDialog")
        self.resize(450, 350)
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # 试卷名称
        self.NameEdit = QLineEdit()
        self.NameEdit.setMaxLength(100)
        layout.addRow("试卷名称：", self.NameEdit)

        # 试卷编号
        self.NumberEdit = QLineEdit()
        self.NumberEdit.setMaxLength(50)
        layout.addRow("试卷编号：", self.NumberEdit)

        # 总题量（整数）
        self.TotalSpin = QSpinBox()
        self.TotalSpin.setRange(0, 9999)
        self.TotalSpin.setValue(0)
        layout.addRow("总题量：", self.TotalSpin)

        # 错题序号（英文逗号分隔）
        self.WrongEdit = QLineEdit()
        self.WrongEdit.setPlaceholderText("例如：1,3,5-7,9（支持连字符）")
        layout.addRow("错题序号：", self.WrongEdit)

        # 备注
        self.RemarkEdit = QTextEdit()
        self.RemarkEdit.setMaximumHeight(100)
        layout.addRow("备注：", self.RemarkEdit)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def getData(self):
        """返回符合 FIELDS 顺序的字典"""
        return {
            "Name": self.NameEdit.text().strip(),
            "Number": self.NumberEdit.text().strip(),
            "TotalCount": str(self.TotalSpin.value()),
            "WrongNumbers": self.WrongEdit.text().strip(),
            "Remark": self.RemarkEdit.toPlainText().strip()
        }


class EditPaperDialog(QDialog):
    """编辑试卷对话框，预填已有数据"""

    def __init__(self, parent, currentData):
        super().__init__(parent)
        self.currentData = currentData
        self.setWindowTitle("编辑试卷")
        self.setObjectName("EditPaperDialog")
        self.resize(450, 350)
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.NameEdit = QLineEdit(self.currentData.get("Name", ""))
        layout.addRow("试卷名称：", self.NameEdit)

        self.NumberEdit = QLineEdit(self.currentData.get("Number", ""))
        layout.addRow("试卷编号：", self.NumberEdit)

        self.TotalSpin = QSpinBox()
        self.TotalSpin.setRange(0, 9999)
        try:
            self.TotalSpin.setValue(int(self.currentData.get("TotalCount", 0)))
        except ValueError:
            self.TotalSpin.setValue(0)
        layout.addRow("总题量：", self.TotalSpin)

        self.WrongEdit = QLineEdit(self.currentData.get("WrongNumbers", ""))
        self.WrongEdit.setPlaceholderText("例如：1,3,5-7,9（支持连字符）")
        layout.addRow("错题序号：", self.WrongEdit)

        self.RemarkEdit = QTextEdit()
        self.RemarkEdit.setMaximumHeight(100)
        self.RemarkEdit.setPlainText(self.currentData.get("Remark", ""))
        layout.addRow("备注：", self.RemarkEdit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def getData(self):
        return {
            "Name": self.NameEdit.text().strip(),
            "Number": self.NumberEdit.text().strip(),
            "TotalCount": str(self.TotalSpin.value()),
            "WrongNumbers": self.WrongEdit.text().strip(),
            "Remark": self.RemarkEdit.toPlainText().strip()
        }
