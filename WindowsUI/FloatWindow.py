"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - FloatWindow
    Version: Alpha 1.0.5
    UpdateTime: 2026-0215-1830
"""

import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,QPushButton)
from Utils.FloatMessage import FloatMessage


class FloatShow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.Parent = parent
        self.popup = None
        # 右键拖拽相关变量
        self.right_drag_active = False      # 是否正在右键拖动
        self.drag_start_pos = QPoint()      # 鼠标按下时的全局位置
        self.window_start_pos = QPoint()    # 鼠标按下时的窗口位置

        self.initWindowProperty()
        self.initWindowLocation()
        self.initWindowPopup()

        self.show()

    def initWindowProperty(self) -> bool:
        """ <1> Set window flags and attributes for a frameless, topmost, transparent window. """
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.ToolTip
        )
        # Enable per-window translucency for opacity animations
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        """ <2> Initialize layout. """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        return True

    def initWindowLocation(self) -> bool:
        self.resize(40, 40)
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - self.width(), screen.height() - self.height())
        self.setWindowOpacity(0.5)  # Initial Transparency.
        return True

    def initWindowPopup(self):
        """ <1> Init PopUpButton in screen. """
        self.PopUpButton = QPushButton()
        self.PopUpButton.setText('≡')
        self.PopUpButton.setFixedSize(40, 40)
        """ <2> Set PopUpButton style. """
        self.PopUpButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 120, 215, 100);
                border-radius: 20px;
                color: white;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 215, 255);
            }
        """)
        """ <3> Bind signal. """
        self.PopUpButton.clicked.connect(self.togglePopup)

        self.layout.addWidget(self.PopUpButton)

    # ---------- 右键拖拽逻辑 ----------
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # 右键按下：记录起始位置，准备拖动
            self.drag_start_pos = event.globalPosition().toPoint()
            self.window_start_pos = self.pos()
            self.right_drag_active = True
            event.accept()  # 阻止事件继续传播（避免触发按钮的右键菜单）
        else:
            super().mousePressEvent(event)  # 左键等交给默认处理（按钮会接收）

    def mouseMoveEvent(self, event):
        if self.right_drag_active and event.buttons() & Qt.MouseButton.RightButton:
            # 右键拖动中：移动窗口
            delta = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(self.window_start_pos + delta)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.right_drag_active:
            # 右键释放：结束拖动
            self.right_drag_active = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.setWindowOpacity(1.0)

    def leaveEvent(self, event):
        self.setWindowOpacity(0.5)

    def moveEvent(self, event):
        super().moveEvent(event)
        if self.popup and self.popup.isVisible():
            self.updatePopupPosition()

    def togglePopup(self):
        if self.popup is not None and self.popup.isVisible():
            self.popup.close()
        else:
            self.showPopup()

    def showPopup(self):
        if self.popup is None:
            self.popup = PopupWindow(parent=self.Parent)
            self.popup.destroyed.connect(self.onPopupDestroyed)
        self.updatePopupPosition()
        self.popup.show()

    def onPopupDestroyed(self):
        self.popup = None

    def updatePopupPosition(self):
        if self.popup is None:
            return False

        btn_geo = self.PopUpButton.geometry()
        global_btn_top_left = self.mapToGlobal(btn_geo.topLeft())
        popup_width = self.popup.width()
        popup_height = self.popup.height()
        screen = QApplication.primaryScreen().availableGeometry()

        x = global_btn_top_left.x() + btn_geo.width()
        y = global_btn_top_left.y()

        if x + popup_width > screen.right():
            x = global_btn_top_left.x() - popup_width
            if x < screen.left():
                x = screen.right() - popup_width

        if y + popup_height > screen.bottom():
            y = screen.bottom() - popup_height
        if y < screen.top():
            y = screen.top()

        self.popup.move(x, y)
        return True


class PopupWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initWindowConfig()
        self.initWindowStyle()
        self.initUI()

    def initWindowConfig(self) -> bool:
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Popup
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setContentsMargins(10, 10, 10, 10)
        self.resize(200, 150)
        return True

    def initWindowStyle(self) -> bool:
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 220);
                border: 1px solid #cccccc;
                border-radius: 8px;
            }
        """)
        return True

    def initUI(self):
        label = QLabel("这是一个弹出窗口")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

        CallMain = QPushButton('主窗口')
        CallMain.clicked.connect(self.manageMainWindowShow)
        self.layout.addWidget(CallMain)

    def manageMainWindowShow(self) -> bool:
        # Ensure that the parent window exists.
        if not self.parent():
            FloatMessage(text='未找到主程序', bg_color='#ff2020', text_color='#000000')
            return False
        # Determine the operation based on the actual display situation of the window.
        self.parent().hide()
        self.parent().showMaximized()
        FloatMessage(text='已呼起主程序窗口', bg_color='#33cc33', text_color='#000000')
        return True

        """if self.parent().windowState() == Qt.WindowState.WindowMaximized:
            FloatMessage(text='主程序窗口已在显示', bg_color='#aec423', text_color='#000000')
            return False
        else:
            self.parent().showMaximized()
            FloatMessage(text='已呼起主程序窗口', bg_color='#33cc33', text_color='#000000')
            return True
        """

if __name__ == '__main__':

    app = QApplication(sys.argv)
    sys.exit(app.exec())
