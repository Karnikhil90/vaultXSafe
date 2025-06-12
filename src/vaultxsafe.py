import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QMainWindow, QStackedWidget,
    QCheckBox, QListWidget, QComboBox, QRadioButton, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from src.lib.JsonEditor import JsonEditor
from src.lib.FileAccess import FileAccess
from src.vaultEngine import VaultEngine as ve


# DEFAULT values

file_path = "./src/config/config_app.json" 
config_fallback : list[dict[any]]= [
    {
        "setting":{
            "title":"VaultXSafe v1.0a",
            "geometry": [500,500],
            "position" :[500,200]
    },
        
        "file":{
            "icon":{
                "app":"./icon/app.ico"
            },
            "css":{
                "root" : "./css",
                "button": "button.css"
            },
            "database": {
                "root":"./database",
                "sql":False
            }
        }
    }
]


file = ve(file_path)


class vaultXSafe:
    def __init__(self):
        pass

    @staticmethod
    def main():
        print(__name__)