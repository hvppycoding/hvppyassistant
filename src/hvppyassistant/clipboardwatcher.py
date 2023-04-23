import logging
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


logger = logging.getLogger(__name__)


class ClipboardWatcher(QObject):
    sig_clipboard_changed = Signal()
    
    def __init__(self, mainapp: QObject):
        super().__init__(mainapp)
        self.mainapp = mainapp
        self._text: str = ""
        
    def text(self) -> str:
        return self._text
        
    def initialize(self):
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    @Slot()
    def on_clipboard_changed(self):
        clipboard_text: str = self.clipboard.text()
        if clipboard_text and self._text != clipboard_text:
            self._text = clipboard_text
            self.sig_clipboard_changed.emit()
