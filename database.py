import sqlite3

class DataBase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def check_id(self, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM refs WHERE user_id=?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referer_id=None):
        with self.conn:
            if referer_id != None:
                return self.cursor.execute('INSERT OR IGNORE INTO refs (user_id, referer_id) VALUES (?, ?)', (user_id, referer_id))
            else:
                return self.cursor.execute('INSERT OR IGNORE INTO refs (user_id) VALUES (?)', (user_id,))

    def count_ref(self, user_id):
        with self.conn:
            return self.cursor.execute('SELECT COUNT (id) as count FROM refs WHERE user_id=?', (user_id,)).fetchone()[0]