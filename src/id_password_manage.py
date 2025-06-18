# It will help to manage BASIC CURD of id&password as seprate file

"""
    choice: list[str]

    basic structure 
    
    "google" or "facebook" or "other" {
        index: int
        user_id: str 
        user_password: str
        create_time 
        last_edit_time
    }
    
"""


from datetime import datetime
# from src.lib.JsonEditor import JsonEditor
# from src.lib.FileAccess import FileAccess
from src.vaultEngine import VaultEngine 
from src.lib.database.DBHandler import DBHandler 

"""
    Here we are using an SQL database for the entry


    id               INT AUTO_INCREMENT PRIMARY KEY
    field            VARCHAR(100)        -- e.g., gmail, facebook
    user_id          VARCHAR(255)
    user_password    VARCHAR(255)
    created_time     DATETIME            -- ISO 8601 format: 'YYYY-MM-DDTHH:MM:SS'
    last_edited_time DATETIME

"""

class ID_PASSWORD_MANAGE:
    def __init__(self, file_path: str = ""):
        # self.file = FileAccess(file_path, False)
        self.engine = VaultEngine()
        db = DBHandler()
        print(db)

    def _get_timestamp(self):
        return datetime.now().isoformat()

    def add(self, user_id, user_password, choice):
        if choice not in self.data:
            self.data[choice] = []

        new_entry = {
            "index": 0,
            "user_id": user_id,
            "user_password": user_password,
            "create_time": self._get_timestamp(),
            "last_edit_time": self._get_timestamp()
        }

    def update(self, choice, index, user_id=None, user_password=None):
        pass

    def delete(self, choice, index):
        pass

    def get_all(self, choice):
        pass

    def get_by_index(self, choice, index):
        pass

ID_PASSWORD_MANAGE()