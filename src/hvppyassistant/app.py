import sys
import logging
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class MainApplication(QObject):
    def __init__(self) -> None:
        super().__init__()
        
        from hvppyassistant.clipboardwatcher import ClipboardWatcher
        self.clipboard_watcher = ClipboardWatcher(self)
        
        from hvppyassistant.trayiconmanager import TrayIconManager, Section
        self.trayicon_manager = TrayIconManager(self)
        
        from hvppyassistant.messagemanager import MessageManager
        self.message_manager = MessageManager(self)
        
        from hvppyassistant.dictionaryplugin import DictionaryPlugin
        self.dictionary_plugin = DictionaryPlugin(self)
        
        self.clipboard_watcher.initialize()
        self.trayicon_manager.initialize()
        self.message_manager.initialize()
        self.dictionary_plugin.initialize()

        self.exit_action: QAction = QAction("Exit", self)
        self.exit_action.triggered.connect(self.on_exit)
        self.trayicon_manager.add_action(Section.EXIT, 0, self.exit_action)
        
        self.trayicon_manager.create_context_menu()
    
    @Slot()
    def on_exit(self):
        QApplication.quit()


def setup_logger(filepath: str = "", use_stream: bool = True):
    from logging import FileHandler, StreamHandler

    fmt = "%(asctime)s [%(levelname)s] [%(name)s] -> %(message)s"
    handlers = []
    if filepath:
        handlers.append(FileHandler(filepath, "w"))
    if use_stream:
        handlers.append(StreamHandler())

    logging.basicConfig(
        format=fmt,
        handlers=handlers,
    )

def main():
    setup_logger()
    
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    
    app.setOrganizationName("hvppycoding")
    app.setApplicationName("hvppyassistant")
    app.setApplicationVersion("0.0.1")
    
    mainapp = MainApplication()
    sys.exit(app.exec())
