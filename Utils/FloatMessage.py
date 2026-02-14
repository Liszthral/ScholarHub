"""
    Copyright: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - Utils - FloatMessage
    Version: Alpha 1.0.1
    UpdateTime: 2026-0214-2250
"""

import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


class FloatMessage(QWidget):
    """
        A floating pop-up window that automatically fades in, stays for a while,
        then fades out and destroys itself.
    """

    def __init__(self, text='default', bg_color='#ffffff', text_color='#000000',
                 font_size=14, parent=None, duration=1800):
        """
        Initialize the floating message.

        :param text: Message content (length <= 70 chars)
        :param bg_color: Background color of the label (hex string)
        :param text_color: Text color (hex string)
        :param font_size: Font size in pixels
        :param parent: Parent widget (default None)
        :param duration: Total display time in milliseconds before fade-out
        """
        super().__init__(parent)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_size = font_size
        self.duration = duration

        # Set up layout and window attributes
        self.layout = QVBoxLayout(self)
        self._configure_window()
        self._create_label()
        self.adjustSize()                 # Let window shrink to fit content
        self._setup_animations()
        self._show_at_position()

    def _configure_window(self):
        """Set window flags and attributes for a frameless, topmost, transparent window."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.ToolTip
        )
        # Allow mouse events to pass through the window
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        # Enable per-window translucency for opacity animations
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def _create_label(self):
        """Create and style the message label, add it to the layout."""
        self.label = QLabel(self.text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(f"""
            background-color: {self.bg_color};
            color: {self.text_color};
            font-size: {self.font_size}px;
            border-radius: 10px;
            padding: 15px 25px;
        """)
        # Remove any margins around the label
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)

    def _setup_animations(self):
        """Create fade-in and fade-out animations, plus a timer for auto-hide."""
        # Start fully transparent
        self.setWindowOpacity(0.0)

        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out.finished.connect(self.close)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._start_fade_out)

    def _show_at_position(self):
        """
        Position the window at the top center of the screen (1/5 from the top),
        then show it and start animations.
        """
        # Ensure size is up-to-date (in case text changed)
        self.adjustSize()

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = screen.height() // 15   # approx 1/15 from top.

        self.move(x, y)
        self.show()                # not maximized, just normal window

        self.fade_in.start()
        self.timer.start(self.duration)

    def _start_fade_out(self):
        """Trigger fade-out animation (stop fade-in if still running)."""
        if self.fade_in.state() == QPropertyAnimation.State.Running:
            self.fade_in.stop()
        self.fade_out.start()

    def closeEvent(self, event):
        """Ensure proper cleanup when the window is closed."""
        self.deleteLater()
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    sys.exit(app.exec())
