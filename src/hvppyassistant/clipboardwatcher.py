import logging
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QLabel


logger = logging.getLogger(__name__)


class ClipboardWatcher(QObject):
    sig_clipboard_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.text = ""
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    @Slot()
    def on_clipboard_changed(self):
        clipboard_text: str = self.clipboard.text()
        if clipboard_text and self.text != clipboard_text:
            self.text = clipboard_text
            self.sig_clipboard_changed.emit()
            self.label = QLabel(self.text)
            self.label.show()