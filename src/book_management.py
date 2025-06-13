
book = {
    "product_id":"FRC0001",
    "title": "Default Book Title",
    "author": "Default Author",
    "isbn": "000-0-00-000000-0",
    "field": "Friction",
    "published_year": 2023,
    "publisher": "Default Publisher",
    "price" : 0.0,
    "created_time": "2023-10-01T00:00:00Z",
    "last_updated_time": "2023-10-01T00:00:00Z",
}

# "tags" : "tag_code"___ which will later help in my book code___ tag_code + index number in that field

class BookManagement:
    def __int__(self, file_path: str = "./src/config/config_app.json"):
        self.file_path = file_path

    def add_book(self, book: dict):
        """Add a new book to the collection."""
        # Here you would implement the logic to add the book to your data store
        pass
    def remove_book(self, product_id: str):
        """Remove a book from the collection by its product ID."""
        # Here you would implement the logic to remove the book from your data store
        pass
    def update_book(self, product_id: str, updated_info: dict):
        """Update the information of an existing book."""
        # Here you would implement the logic to update the book in your data store
        pass
    def get_book(self, product_id: str) -> dict:
        """Retrieve a book's information by its product ID."""
        # Here you would implement the logic to get the book from your data store
        return {}
    def list_books(self) -> list:
        """List all books in the collection."""
        # Here you would implement the logic to list all books from your data store
        return []