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
        password TEXT NOT NULL);
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

    def insert_keys(self, password_hash):        
        insert_password = """INSERT INTO masterpassword(password) VALUES(?) """
        self.cursor.execute(insert_password, ((password_hash),))
        
        self.db.commit()

