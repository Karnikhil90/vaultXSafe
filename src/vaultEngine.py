
from src.lib.JsonEditor import JsonEditor
from src.lib.FileAccess import FileAccess
from src.book_management import BookManagement

class VaultEngine:
    def __init__(self, file_path: str = "./src/config/config_app.json"):
        self.file_path = file_path
    
    def getFilePath(self) -> str:
        return self.file_path
    
    def getdata(self,file_path: str = getFilePath()):
        file = FileAccess(file_path)
        return file.readData()[0]
    
    def getTitle(self,file_path: str = getFilePath()) -> str:
        """Fallback: as Error if Cant find title"""
        return self.getdata(file_path).get('setting', {"title": "DEFAULT: PyQt5"}).get('title', "Errr???")

    def getfile(self,file_path: str = getFilePath()):
        """For now it's only to get the css of button"""
        file = FileAccess(file_path)
        return file.read()