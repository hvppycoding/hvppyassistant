from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class DictionaryPlugin(QObject):
    def __init__(self, mainapp: QObject) -> None:
        super().__init__(mainapp)
        self.mainapp = mainapp
        
    def initialize(self):
        from hvppyassistant.clipboardwatcher import ClipboardWatcher
        from hvppyassistant.messagemanager import MessageManager
        self.clipboard_watcher: ClipboardWatcher  = self.mainapp.clipboard_watcher
        self.message_manager: MessageManager = self.mainapp.message_manager
        self.clipboard_watcher.sig_clipboard_changed.connect(self.on_clipboard_changed)
        
    def on_clipboard_changed(self):
        clipboard_text: str = self.clipboard_watcher.text()
        self.message_manager.show_message("Dictionary", clipboard_text, duration=1000)