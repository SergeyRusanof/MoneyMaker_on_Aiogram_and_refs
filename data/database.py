import sqlite3

class DataBase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def check_id(self, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM referal WHERE user_id=?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referer_id=None):
        with self.conn:
            if referer_id != None:
                return self.cursor.execute('INSERT OR IGNORE INTO refs (user_id, referer_id) VALUES (?, ?)', (user_id, referer_id))
            else:
                return self.cursor.execute('INSERT OR IGNORE INTO refs (user_id) VALUES (?)', (user_id,))

    def count_ref(self, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM referal WHERE referer_id=?', (user_id,)).fetchall()
            return len(result)

    def all_balance(self, amount):
        with self.conn:
            result = self.cursor.execute('UPDATE users SET balance=balance+?', (amount,))

    def income_day(self, amount):
        with self.conn:
            result = self.cursor.execute('UPDATE users SET income=?', (amount,))


    def users_in_bot(self):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM users').fetchall()
            return result
    def add_data_user(self, user_id, user_name, balance, rbalance, income):
        with self.conn:
            result = self.cursor.execute('INSERT INTO users (user_id, user_name, balance, rbalance, income) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, balance, rbalance, income))

    def profile_data(self, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchall()[0]
            return result

    def up_balance(self, user_id, amount_up):
        with self.conn:
            result = self.cursor.execute('UPDATE users SET balance=? WHERE user_id=?', (amount_up, user_id))

    def chek_id_adm(self, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id, )).fetchall()
            return result

    def is_refer(self, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT referer_id FROM referal WHERE user_id=?', (user_id,)).fetchone()
            return result

    def refs_bonus(self, user_id, bonus):
        with self.conn:
            result = self.cursor.execute('UPDATE users SET rbalance=rbalance+? WHERE user_id=?', (bonus, user_id))
            self.conn.commit()
