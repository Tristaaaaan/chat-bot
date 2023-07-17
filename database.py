import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect('contents.db')
        self.cursor = self.con.cursor()
        self.create_database()

    def create_database(self):
        """Create tasks table"""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS history(id integer PRIMARY KEY AUTOINCREMENT, content varchar(50) NOT NULL, identity varchar(20) NOT NULL)")
        self.con.commit()

    def insert_data(self, chat_content, category):
        """Create a task"""
        self.cursor.execute("INSERT INTO history(content, identity) VALUES(?, ?)",
                            (chat_content, category,))
        self.con.commit()

        # GETTING THE LAST ENTERED ITEM SO WE CAN ADD IT TO THE TASK LIST
        created_task = self.cursor.execute(
            "SELECT content, identity FROM history").fetchall()

        return created_task[-1]

    def get_data(self):
        """Get tasks"""
        history = self.cursor.execute(
            "SELECT content, identity FROM history").fetchall()

        return history

    def close_db_connection(self):
        self.data_con.close()
