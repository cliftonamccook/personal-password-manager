import uuid
import re
import base64
from DBController.dbconnect import DBControl
from Security.security import SecurityManager


class Controller:

    def __init__(self):
        self.ui = None
        self.security = SecurityManager()
        self.db = DBControl()
        self.db.start()
        self.results = None
        self.entryman = EntryManager()

    def getmasterpassword(self):
        entered_pwd = self.ui.login_window.get_masterpwdtxt().encode('utf-8')
        password_hash = self.security.hashpassword(entered_pwd)
        self.security.encryption_key = base64.urlsafe_b64encode(
            self.security.getKDF().derive(self.ui.login_window.get_masterpwdtxt().encode()))
        pwd = self.db.fetch_master_pwd(password_hash)
        return pwd

    def checkpassword(self):
        password = self.getmasterpassword()

        if password:
            self.refreshall()
        else:
            self.ui.login_window.master_password_text.delete(0, 'end')
            self.ui.login_window.error_text.config(text="Wrong Password")

    def resetpassword(self):
        self.ui.reset_window.start()

    def encrypt_fields(self, obj):
        obj1 = self.security.encrypt_fields(obj)
        return obj1

    def addentry(self, obj):
        obj2 = Entry(obj["name"], obj["url"], obj["username"], obj["password"], obj["notes"])
        obj2.encode()
        encrypted_fields = self.encrypt_fields(obj2)
        self.db.insert_entry(encrypted_fields)
        self.refreshall()

    def refreshall(self):
        self.entryman.flush()
        self.decrypt_entries()
        self.ui.password_vault_window.start()

    def searchrefresh(self):
        self.ui.password_vault_window.start()

    def get_entries(self):
        enc = self.db.fetch_entries()
        return enc

    def decrypt_entries(self):
        enc = self.get_entries()
        for i in enc:
            entry = Entry(i["name"], i["url"], i["username"], i["password"], i["notes"], i["id"])
            e = self.security.decrypt_fields(entry)
            self.entryman.entries.append(e)

    def deleteentry(self, input):
        self.db.delete_entry(input)
        self.refreshall()

    def savemasterpassword(self):
        password = self.ui.initial_window.get_masterpwdtxt()
        confirmation = self.ui.initial_window.get_confirmpwdtxt()
        if password == confirmation:
            password = self.ui.initial_window.get_masterpwdtxt()
            password = password.encode('utf-8')
            # print(password)

            self.db.clearmasterpassword()

            password_hash = self.security.hashpassword(password)
            key = str(uuid.uuid4().hex)
            recovery_key = self.security.hashpassword(key.encode('utf-8'))

            self.security.encryption_key = base64.urlsafe_b64encode(
                self.security.getKDF().derive(password)
            )

            self.db.insert_keys(password_hash, recovery_key)

            self.ui.recovery_window.startRecovery(key)
        else:
            self.ui.initial_window.show_msg("Passwords don't match")

    def getrecoverykey(self):
        recovery_key_hash = self.security.hashpassword(str(self.ui.reset_window.rkey_text.get()).encode('utf-8'))
        self.db.cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND recovery_key = ?', [(recovery_key_hash)])
        return self.db.cursor.fetchall()

    def checkrecoverykey(self):
        checked = self.getrecoverykey()

        if checked:
            self.ui.initial_window.start()
        else:
            self.ui.reset_window.rkey_text.delete(0, 'end')
            self.ui.reset_window.message_label.config(text='Wrong Key')

    def search(self):
        txt = self.ui.password_vault_window.search_field.get()
        for i in self.entryman.entries:
            if not any([re.search(txt, i.name.decode()), re.search(txt, i.url.decode()), re.search(txt, i.username.decode()), re.search(txt, i.password.decode()), re.search(txt, i.notes.decode())]):
                self.entryman.entries.remove(i)
        self.searchrefresh()


class EntryManager:
    def __init__(self):
        self.entries = []

    def flush(self):
        self.entries.clear()


class Entry:
    def __init__(self, name, url, username, password, notes, id=None):
        self.id = id
        self.name = name
        self.url = url
        self.username = username
        self.password = password
        self.notes = notes

    def encode(self):
        self.name = self.name.encode()
        self.url = self.url.encode()
        self.username = self.username.encode()
        self.password = self.password.encode()
        self.notes = self.notes.encode()