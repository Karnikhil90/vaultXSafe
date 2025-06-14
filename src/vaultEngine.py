
from src.lib.JsonEditor import JsonEditor
from src.lib.FileAccess import FileAccess
from src.book_management import BookManagement

# Fallback configuration in case JSON config file is missing or unreadable

config_fallback: list[dict] = [
    {
        "setting": {
            "title": "VaultXSafe v1.0a",
            "geometry": [500, 500],
            "position": [500, 200]
        },
        "file": {
            "icon": {
                "app": "./icon/app.ico"
            },
            "css": {
                "root": "./css",
                "button": "button.css"
            },
            "database": {
                "root": "./database",
                "sql": False
            }
        }
    }
]

class VaultEngine:
    def __init__(self, file_path: str = "./src/config/config_app.json"):
        self.file_path = file_path
        self.file = FileAccess(file_path)
        self.file_path_exists: bool = self.file.exists()

    def getdata(self, file_path :str) -> dict:
        """Reads JSON config or returns fallback."""
        path = file_path if file_path else self.file_path
        try:
            file = FileAccess(path)
            data = file.read_json()
            return data[0] if data else config_fallback[0]
        except Exception:
            return config_fallback[0]

    def getTitle(self) -> str:
        """Returns the app title from config or fallback."""
        return self.getdata(self.file_path).get("setting", {}).get("title", "VaultXSafe (Default)")

    def getfile(self, file_path: str = None) -> str | None:
        """Returns raw content of the config file."""
        try:
            file = FileAccess(file_path)
            return file.read()
        except Exception:
            return None
        
    def getdata_file(self, file_type: str= None):
        return self.getdata(self.file_path).get("file", {}).get(file_type, {})

    def getGeometry(self) -> tuple[int]:
        """Returns window position and size: (x, y, width, height)."""
        data = self.getdata(self.file_path)
        geometry = data.get("setting", {}).get("geometry", [500, 500])
        position = data.get("setting", {}).get("position", [500, 200])
        return position[0], position[1], geometry[0], geometry[1]

    def getfile_css(self, css_file_name: str = None) -> str | None:
        """Returns full path for a given CSS file name."""
        file : str = self.getdata_file("css").get("root", None) + self.getdata_file("css").get(css_file_name, None) 
        return self.getfile(file) if file else None
        
    def getfile_icon(self, icon_file_name: str = None) -> str | None:
        """Returns full path for a given icon file name."""
        return self.getdata_file("icon").get("root", None) + self.getdata_file("icon").get(icon_file_name, None)
        
    def get_password_categories(self)-> list[str]:
        return ["Gmail", "Facebook", "Email"]