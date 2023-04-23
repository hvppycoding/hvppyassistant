import enum
from collections import namedtuple
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from hvppyassistant import resource_rc

class Section(enum.IntEnum):
    FILE = 1
    EDIT = 2
    EXIT = 3

ActionInfo = namedtuple("ActionInfo", ["section", "priority", "action"])

class TrayIconManager(QObject):
    def __init__(self, mainapp: QObject):
        super().__init__(mainapp)
        self.mainapp = mainapp
        
    def initialize(self):
        self.icon = QIcon(":/hvppyassistant_icon.png")
        self.tray_icon: QSystemTrayIcon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.show()
        self.action_info_list: list[ActionInfo] = []
        
    def create_context_menu(self) -> QMenu:
        self.menu = QMenu()
        for section, actions in sorted(self.group_by_section().items()):
            for action in actions:
                self.menu.addAction(action)
            self.menu.addSeparator()
        self.tray_icon.setContextMenu(self.menu)
        
    def show_message(self, title: str, msg: str, duration: int=3000) -> None:
        self.tray_icon.showMessage(title, msg, self.icon, msecs=duration)
    
    def group_by_section(self) -> dict[int, list[QAction]]:
        section_dict: dict[int, list[QAction]] = {}
        for action_info in self.action_info_list:
            if action_info.section not in section_dict:
                section_dict[action_info.section] = []
            section_dict[action_info.section].append(action_info.action)
        return section_dict
        
    def add_action(self, section: Section, priority: int, action: QAction):
        self.action_info_list.append(ActionInfo(section, priority, action))
        
        