import sys
import logging
from PySide6.QtWidgets import QApplication, QMainWindow
from hvppyassistant.clipboardwatcher import ClipboardWatcher


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
    app.setOrganizationName("hvppycoding")
    app.setApplicationName("hvppyassistant")
    app.setApplicationVersion("0.0.1")
    
    window = QMainWindow()
    window.show()
    
    clipboard_watcher = ClipboardWatcher()
    app.exec()
    

if __name__ == "__main__":
    main()