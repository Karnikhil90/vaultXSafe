import os
import json


"""
file_access.py

This module contains the FileAccess class to help work with JSON files easily.

It helps you:
- Create a file if it doesn't exist.
- Create folders/directories if missing.
- Read data from a JSON file.
- Write or add new data to a JSON file.
- Clear the file or print data in a clean JSON format.

Example:
---------
    file = FileAccess("data/user.json")
    file.addData({"name": "Nikhil", "age": 20})
    print(file.read_json())

Classes:
---------
FileAccess:
    A helper class for basic file operations with JSON data.

    Methods:
    --------

    __init__(fileAddress: str)
        Initializes the class with the given file path.
        Also creates the folder and file if they do not exist.

        @param fileAddress: Path to the JSON file.

    ensure_directory_exists()
        Makes sure the folder path of the file exists. Creates it if missing.

    ensure_file_exists()
        Checks if the file exists. If not, creates a new empty JSON file.

    addData(receive_data: dict = None)
        Adds (appends) a dictionary to the existing JSON data in the file.

        @param receive_data: Dictionary to add to the JSON list.

    write_json(recive_data: dict)
        Overwrites the entire JSON file with new data.

        @param recive_data: A dictionary or list to write into the file.

    read() -> str
        Reads and returns the raw string content of the file.

        @return: File content as a string.

    read_json() -> list
        Reads and returns the JSON data as a list.

        @return: List of JSON objects from the file.

    CreateFile()
        Creates a new JSON file with empty list `[]` if not already present.

    WriteData(content: str = "[]")
        Clears the file and writes the provided string (usually `[]`).

        @param content: A string to overwrite the file content.

    print_json(recived_data: any = {})
        Prints JSON data in a readable format in the terminal.

        @param recived_data: Any Python object (like dict or list) to print.
"""

class FileAccess:
    def __init__(self, fileAddress):
        self.file_address = fileAddress
        # print(fileAddress)
        try:
            self.ensure_directory_exists()
            self.ensure_file_exists()
        except Exception as e:
            print(f"Initialization error: {e}")

    def ensure_directory_exists(self):
        """Ensure that the directory for the file exists."""
        try:
            dir_name = os.path.dirname(self.file_address)
            if dir_name and not os.path.exists(dir_name):  # Add this condition
                os.makedirs(dir_name)
        except Exception as e:
            print(f"Error ensuring directory exists: {e}")

    def ensure_file_exists(self):
        """Ensure that the file exists; create it if not."""
        try:
            if not os.path.isfile(self.file_address):
                self.CreateFile()
        except Exception as e:
            print(f"Error ensuring file exists: {e}")

    def addData(self, receive_data: dict = None):
        print(receive_data)
        file_path = self.file_address
        try:
            # Attempt to read existing data
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                # If file does not exist, initialize with an empty list
                data = []
            except json.JSONDecodeError:
                # Handle the case where the file is empty or corrupted
                data = []

            # Add new data and write it to the file
            if receive_data:
                data.append(receive_data)

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error adding data to file: {e}")
    
    def write_json(self,recive_data): 
        """Write data to JSON file."""
        try:
            with open(self.file_address, 'w') as file:
                json.dump(recive_data, file, indent=4)
        except Exception as e:
            print(f"Error writing data to JSON file: {e}")

    def read(self) -> str:
        """Read the raw content of the file as a string."""
        try:
            with open(self.file_address, 'r') as file:
                data = file.read()
                # print(data)
                return data
        except Exception as e:
            print(f"Error reading file as string: {e}")
            return ""

    def read_json(self) -> list:
        file_path = self.file_address
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}. Returning empty list.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}. Returning empty list.")
            return []
        except Exception as e:
            print(f"Error reading data from file: {e}")
            return []

    def CreateFile(self):
        try:
            with open(self.file_address, 'w') as file:
                file.write("[]")
                print("Created a new file with an empty list.")
        except FileExistsError:
            print(f"File already exists: {self.file_address}")
        except Exception as e:
            print(f"Error creating file: {e}")
    
    def WriteData(self,content:str = "[]"):
        """Clear the content of the JSON file by overwriting it with an empty array."""
        try:
            with open(self.file_address, 'w') as file:
                file.write(content)
                print(f"Cleared the content of the file: {self.file_address}")
        except Exception as e:
            print(f"Error clearing file content: {e}")
    
    def print_json(self,recived_data:any={}):
        try:
            print(json.dumps(recived_data, indent=4))
        except Exception as e:
            print(f"Error printing JSON: {e}")