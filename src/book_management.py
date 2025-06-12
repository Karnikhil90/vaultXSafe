
book = {
    "product_id":"FRC0001",
    "title": "Default Book Title",
    "author": "Default Author",
    "isbn": "000-0-00-000000-0",
    "field": "Friction",
    "published_year": 2023,
    "publisher": "Default Publisher",
    # "tages": ["friction", "novel"],
    "price" : 0.0,
    "created_time": "2023-10-01T00:00:00Z",
    "last_updated_time": "2023-10-01T00:00:00Z",
}

# "tags" : "tag_code"___ which will later help in my book code___ tag_code + index number in that field

class BookManagement:
    def __int__(self, file_path: str = "./src/config/config_app.json"):
        self.file_path = file_path