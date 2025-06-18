import mysql.connector , os

"""
=====================================================================================
DBHandler: Core Database Utility for VaultXSafe and Other Secure Modules
=====================================================================================

Overview:
---------
This class acts as a general-purpose MySQL database handler for secure ID and password
storage or similar structured data. Designed to work across various modules (email,
passwords, tokens, etc.), it handles CRUD operations on a pre-defined table structure
with full control via Python.

You can integrate this class across your system wherever structured record access
with custom timestamping is needed.

=====================================================================================
"""

class DBHandler:
    def __init__(self, host : str = os.getenv("DB_HOST"), 
                    user  : str = os.getenv("DB_USER"),
                    password : str = os.getenv('DB_PASSWORD'),
                    database : str = os.getenv("DB_NAME")
                ):
        """
        Initialize and connect to the MySQL database.

        :param host: MySQL server address
        :param user: Username for the DB
        :param password: Password for the DB
        :param database: Target database name (must already exist)
        """
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def commad(self, commad : str):
        self.cursor.execute(commad)
        self.conn.commit()

    def delete(self, entry_id: str) -> bool:
        """
        Delete a record by ID.

        :param entry_id: Record ID
        :return: True if deleted
        """
        self.commad(f"DELETE FROM user_id_password WHERE id = {entry_id}")
        return self.cursor.rowcount > 0
    
    def update(self, var_type: str, old_value: str, new_value: str) -> bool:
        """
        Update entries based on a specific field and value.

        :param var_type: Which column to update. Allowed: 'uid', 'password', 'field'
        :param old_value: The existing value in the column
        :param new_value: The value to replace it with
        :return: True if at least one row was updated
        """
        column_map = {
            "uid": "user_id",
            "password": "user_password",
            "field": "field"
        }

        if var_type not in column_map:
            raise ValueError(f"Invalid var_type '{var_type}'. Must be one of: {', '.join(column_map.keys())}")

        column = column_map[var_type]

        sql = f"UPDATE user_id_password SET {column} = %s WHERE {column} = %s"
        self.cursor.execute(sql, (new_value, old_value))
        self.conn.commit()

        return self.cursor.rowcount > 0

    def close(self):
        """Cleanly close the database connection."""
        self.cursor.close()
        self.conn.close()
