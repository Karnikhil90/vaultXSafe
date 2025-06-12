from src.lib.FileAccess import FileAccess  # Ensure to import your FileAccess module
# import json

class JsonEditor:
    def __init__(self, file_path):
        print("DEBUG: JsonEditor Running...",file_path,"....")
        self.file_path = file_path
        self.file_access = FileAccess(file_path)
        self.data = self.file_access.readData()

    def _save_json(self):
        try:
            # Use FileAccess to write the data
            self.file_access.write_json(self.data)
        except Exception as e:
            print(f"Error saving JSON file: {e}")

    def _update_field(self, field_path, new_value):
        if not self.data:
            print("No data loaded.")
            return
        
        keys = field_path.split('.')
        d = self.data[0]  # Access the first item in the list
        for key in keys[:-1]:
            d = d.get(key, {})
        d[keys[-1]] = new_value

    def get_setting(self, setting_key):
        return self._get_field(f"setting.{setting_key}")

    def set_setting(self, setting_key, new_value):
        self._update_field(f"setting.{setting_key}", new_value)
        self._save_json()

    def get_filepath(self, filepath_key):
        return self._get_field(f"filepath.{filepath_key}")

    def set_filepath(self, filepath_key, new_value):
        self._update_field(f"filepath.{filepath_key}", new_value)
        self._save_json()

    def _get_field(self, field_path):
        if not self.data:
            print("No data loaded.")
            return None
        
        keys = field_path.split('.')
        d = self.data[0]
        for key in keys:
            if key in d:
                d = d[key]
            else:
                return None
        return d

    def get_configuration(self):
        if not self.data:
            print("No data loaded.")
            return {}
        return self.data[0]

    def reload(self):
        self.data = self.file_access.readData()

    def remove_field(self, field_path):
        if not self.data:
            print("No data loaded.")
            return
        
        keys = field_path.split('.')
        d = self.data[0]
        for key in keys[:-1]:
            d = d.get(key, {})
        if keys[-1] in d:
            del d[keys[-1]]
            self._save_json()
        else:
            raise KeyError(f"{field_path} not found in the configuration.")
    
    def list_fields(self, d=None, parent_key=''):
        if not self.data:
            print("No data loaded.")
            return []
        
        if d is None:
            d = self.data[0]
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.list_fields(v, new_key))
            else:
                items.append(new_key)
        return items
    def print_json(self,data:any=None):
        self.file_access.print_json(self.get_configuration())
        