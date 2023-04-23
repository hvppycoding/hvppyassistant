from functools import partial
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class MessageManager(QObject):
    def __init__(self, mainapp: QObject) -> None:
        super().__init__(mainapp)
        self.message_pool: list[QLabel] = []
        
    def initialize(self):
        pass
        
    def show_message(self, title: str, msg: str, duration: int=3000) -> None:
        label = QLabel(title + "\n" + msg)
        QTimer.singleShot(duration, label.close)
        label.setWindowFlags(label.windowFlags() | Qt.WindowStaysOnTopHint)
        label.show()
        label.activateWindow()
        label.raise_()
        self.message_pool.append(label)
        label.destroyed.connect(partial(self.on_message_destroyed, label))
        
    def on_message_destroyed(self, label: QLabel):
        self.message_pool.remove(label)
        