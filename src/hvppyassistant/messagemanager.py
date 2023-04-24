from functools import partial
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class MessageDialog(QWidget):
    def __init__(self, title: str, message: str, duration: int=2000) -> None:
        super().__init__()
        # Qt.SubWindow: Do not show in the windows' taskbar
        # https://stackoverflow.com/questions/4055506/qt-hide-taskbar-item
        self.setWindowFlags(Qt.SubWindow | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setLayout(QVBoxLayout())
        self.title = QLabel(title, self)
        bold_font = self.title.font()
        bold_font.setPointSize(14)
        bold_font.setBold(True)
        self.title.setFont(bold_font)
        self.textedit = QTextEdit(self)
        self.textedit.setFontPointSize(10)
        self.textedit.setReadOnly(True)
        self.textedit.setPlainText(message)
        self.layout().addWidget(self.title)
        self.layout().addWidget(self.textedit)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.resize(400, 256)
        screen_size = QGuiApplication.primaryScreen().availableGeometry()
        self.move(screen_size.width() - self.width(), screen_size.height() - self.height())
        self.opacity_animation = QPropertyAnimation(self, b"opacity", self)
        self.opacity_animation.finished.connect(self.close)
        self.duration = duration

    def showEvent(self, event: QShowEvent) -> None:
        QTimer.singleShot(1000, self.animated_close)
        return super().showEvent(event)
        
    def enterEvent(self, event: QEvent) -> None:
        self.opacity_animation.stop()
        self.opacity = 1
        return super().enterEvent(event)
        
    def leaveEvent(self, event: QEvent) -> None:
        QTimer.singleShot(0, self.animated_close)
        return super().leaveEvent(event)
    
    def animated_close(self):
        if self.opacity_animation.state() == QAbstractAnimation.State.Running:
            return
        if self.underMouse():
            return
        self.opacity_animation.setDuration(self.duration)
        self.opacity_animation.setStartValue(1)
        self.opacity_animation.setEndValue(0)
        self.opacity_animation.start()
        
    @Property(float)
    def opacity(self):
        return self.windowOpacity()
    
    @opacity.setter
    def opacity(self, value):
        self.setWindowOpacity(value)
        self.update()
        

class MessageManager(QObject):
    def __init__(self, mainapp: QObject) -> None:
        super().__init__(mainapp)
        self.message_pool: list[QLabel] = []
        
    def initialize(self):
        pass
        
    def show_message(self, title: str, msg: str, duration: int=2000) -> None:
        dialog = MessageDialog(title, msg, duration)
        # QTimer.singleShot(duration, label.close)
        dialog.show()
        dialog.activateWindow()
        dialog.raise_()
        self.message_pool.append(dialog)
        dialog.destroyed.connect(partial(self.on_message_destroyed, dialog))
        
    def on_message_destroyed(self, label: QLabel):
        self.message_pool.remove(label)
        