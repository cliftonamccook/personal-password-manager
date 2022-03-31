import sqlite3


class DBControl:
    """
    Handles database connection
    """
    def __init__(self):
        self.file = 'mypasswords.db'
        self.cursor = None
        self.db = None

    def start(self):
        self.db = sqlite3.connect(self.file)
        self.cursor = self.db.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS masterpassword(
        id INTEGER PRIMARY KEY,
        password TEXT NOT NULL,
        recovery_key TEXT NOT NULL);
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        note TEXT);
        """)

        self.cursor.execute('SELECT * FROM masterpassword')
        return True

    def clearmasterpassword(self):
        sql = "DELETE FROM masterpassword WHERE id = 1"
        self.cursor.execute(sql)

    def fetch_master_pwd(self, password_hash):
        self.cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND password = ?', [(password_hash)])
        return self.cursor.fetchall()

    def insert_keys(self, password_hash, recovery_key):
        insert_password = """INSERT INTO masterpassword(password, recovery_key) VALUES(?, ?) """
        self.cursor.execute(insert_password, ((password_hash), (recovery_key)))
        self.db.commit()

    def delete_entry(self, input):
        self.cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        self.db.commit()

    def insert_entry(self, obj):
        insert_fields = """INSERT INTO vault(name, url, username, password, note) VALUES(?, ?, ?, ?, ?) """
        name = obj.name
        url = obj.url
        username = obj.username
        password = obj.password
        notes = obj.notes
        self.cursor.execute(insert_fields, (name, url, username, password, notes))
        self.db.commit()

    def fetchRKey(self, recovery_key_hash):
        self.cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND recovery_key = ?', [(recovery_key_hash)])
        return self.cursor.fetchall()

    def fetch_entries(self):
        objs = []
        self.cursor.execute('SELECT * FROM vault')
        if self.cursor.fetchall() is not None:
            i = 0
            while True:
                self.cursor.execute('SELECT * FROM vault')
                encrypted_entries = self.cursor.fetchall()

                if len(encrypted_entries) == 0:
                    break

                objs.append({
                    "id": encrypted_entries[i][0],
                    "name": encrypted_entries[i][1],
                    "url": encrypted_entries[i][2],
                    "username": encrypted_entries[i][3],
                    "password": encrypted_entries[i][4],
                    "notes": encrypted_entries[i][5]
                })

                i = i + 1

                self.cursor.execute('SELECT * FROM vault')
                if len(self.cursor.fetchall()) <= i:
                    break
            return objs
