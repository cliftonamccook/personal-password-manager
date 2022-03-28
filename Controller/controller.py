import uuid
import re
import base64
from DBController.dbconnect import DBControl
from Security.security import SecurityManager
from Controller.entrymanager import EntryManager, Entry


class Controller:
    def __init__(self):
        self.ui = None
        self.security = SecurityManager()
        self.db = DBControl()
        self.createDatabase()
        self.entryman = EntryManager()

    def createDatabase(self):
        self.db.start()

    def openvault(self):
        entered_pwd = self.ui.login_window.get_masterpwdtxt().encode('utf-8')
        password_hash = self.security.hashpassword(entered_pwd)
        self.security.encryption_key = base64.urlsafe_b64encode(
            self.security.getKDF().derive(self.ui.login_window.get_masterpwdtxt().encode()))
        password = self.db.fetch_master_pwd(password_hash)
        if password:
            self.refreshall()
        else:
            self.ui.login_window.master_password_text.delete(0, 'end')
            self.ui.login_window.error_text.config(text="Wrong Password")

    def addentry(self, obj):
        obj2 = Entry(obj["name"], obj["url"], obj["username"], obj["password"], obj["notes"])
        obj2.encode()
        encrypted_fields = self.security.encrypt_fields(obj2)
        self.db.insert_entry(encrypted_fields)
        self.refreshall()

    def deleteentry(self, entryID):
        self.db.delete_entry(entryID)
        self.refreshall()

    def search(self):
        txt = self.ui.password_vault_window.search_field.get()
        for i in self.entryman.entries:
            if not any([re.search(txt, i.name.decode()), re.search(txt, i.url.decode()), re.search(txt, i.username.decode()), re.search(txt, i.password.decode()), re.search(txt, i.notes.decode())]):
                self.entryman.entries.remove(i)
        self.searchrefresh()

    def loadentries(self):
        enc = self.db.fetch_entries()
        for i in enc:
            entry = Entry(i["name"], i["url"], i["username"], i["password"], i["notes"], i["id"])
            e = self.security.decrypt_fields(entry)
            self.entryman.entries.append(e)

    def refreshall(self):
        self.entryman.flush()
        self.loadentries()
        self.ui.password_vault_window.start()

    def searchrefresh(self):
        self.ui.password_vault_window.start()

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
            # self.ui.show_frame(RecoveryFrame(key))
        else:
            self.ui.initial_window.show_msg("Passwords don't match")
            # pass

    def resetpassword(self):
        self.ui.reset_window.start()

    def checkrecoverykey(self):
        recovery_key_hash = self.security.hashpassword(str(self.ui.reset_window.rkey_text.get()).encode('utf-8'))
        self.db.cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND recovery_key = ?', [(recovery_key_hash)])
        checked = self.db.cursor.fetchall()

        if checked:
            self.ui.initial_window.start()
        else:
            self.ui.reset_window.rkey_text.delete(0, 'end')
            self.ui.reset_window.message_label.config(text='Wrong Key')
