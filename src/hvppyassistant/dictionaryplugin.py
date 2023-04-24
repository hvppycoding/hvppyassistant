from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


def _change_list_to_string(target):
    if not isinstance(target, list):
        print("Unexpected type: " + str(type(target)))
        return ""
    if len(target) == 1 and isinstance(target[0], str):
        return target[0]
    output = []
    for item in target:
        if isinstance(item, str):
            output.append(item)
        elif isinstance(item, list):
            output.append(_change_list_to_string(item))
        else:
            print("Unexpected type: " + str(type(item)))
    return output

def to_string(target):
    output = ""
    if isinstance(target, str):
        return target
    elif isinstance(target, list):
        if all(isinstance(item, str) for item in target):
            output += " ".join(target) + "\n"
        else:
            for item in target:
                output += to_string(item)
    else:
        print("Unexpected type: " + str(type(target)))
        return ""
    return output

def get_korean_translation(word: str) -> str:
    import requests
    import json
    
    # Set up the API request
    url = "https://ac.dict.naver.com/enko/ac?st=11001&r_format=json&r_enc=utf-8&q=" + word

    # Send the request and get the response
    response = requests.get(url)
    response_json = json.loads(response.text)

    # Extract the Korean translation from the response
    if response_json["items"]: 
        korean_word = to_string(_change_list_to_string(response_json["items"]))
    else:
        korean_word = ""
    return korean_word

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
        
    def is_english_word(self, text: str) -> bool:
        return text.isalpha()
        
    def on_clipboard_changed(self):
        clipboard_text: str = self.clipboard_watcher.text().strip().lower()
        if self.is_english_word(clipboard_text):
            definition = get_korean_translation(clipboard_text)
            self.message_manager.show_message("hvppyassistant", definition, duration=2000)