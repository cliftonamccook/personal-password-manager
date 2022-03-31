import uuid
import re
import base64
from DBController.dbconnect import DBControl
from Security.security import SecurityManager
from Controller.entrymanager import EntryManager, Entry


class Controller:
    def __init__(self):
        self.security = SecurityManager()
        self.db = DBControl()
        self.createDatabase()
        self.entryman = EntryManager()
        self.messages = {}

    def createDatabase(self):
        self.db.start()

    def openvault(self, k):
        entered_pwd = k.encode('utf-8') # self.ui.login_window.get_masterpwdtxt().encode('utf-8') # send this in as a parameter
        password_hash = self.security.hashpassword(entered_pwd)
        self.security.encryption_key = base64.urlsafe_b64encode(
            self.security.getKDF().derive(k.encode())) # self.ui.login_window.get_masterpwdtxt().encode())
        password = self.db.fetch_master_pwd(password_hash)
        if password:
            self.messages["Password"] = True
            self.refreshall()
        else:
            self.messages["Password"] = False
            # self.ui.login_window.master_password_text.delete(0, 'end')
            # self.ui.login_window.error_text.config(text="Wrong Password")


    def addentry(self, obj):
        obj2 = Entry(obj["name"], obj["url"], obj["username"], obj["password"], obj["notes"])
        obj2.encode()
        encrypted_fields = self.security.encrypt_fields(obj2)
        self.db.insert_entry(encrypted_fields)
        self.refreshall()

    def deleteentry(self, entryID):
        self.db.delete_entry(entryID)
        self.refreshall()

    def search(self, string):
        print(string)
        txt = string # self.ui.password_vault_window.search_field.get()
        for i in self.entryman.entries:
            if not any([re.search(txt, i.name.decode()), re.search(txt, i.url.decode()), re.search(txt, i.username.decode()), re.search(txt, i.password.decode()), re.search(txt, i.notes.decode())]):
                self.entryman.entries.remove(i)
        # self.searchrefresh()

    def loadentries(self):
        enc = self.db.fetch_entries()
        for i in enc:
            entry = Entry(i["name"], i["url"], i["username"], i["password"], i["notes"], i["id"])
            e = self.security.decrypt_fields(entry)
            self.entryman.entries.append(e)

    def refreshall(self):
        self.entryman.flush()
        self.loadentries()
        # self.ui.password_vault_window.start()

    # def searchrefresh(self):
    #     self.ui.password_vault_window.start()

    def savemasterpassword(self, p, cpwd):
        password = p # self.ui.initial_window.get_masterpwdtxt()
        confirmation = cpwd # self.ui.initial_window.get_confirmpwdtxt()
        if password == confirmation:
            password = p # self.ui.initial_window.get_masterpwdtxt()
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
            self.messages["key"] = key
            # self.ui.recovery_window.startRecovery(key)
            # self.ui.show_frame(RecoveryFrame(key))
        else:
            self.messages["key"] = ""
            # self.ui.initial_window.show_msg("Passwords don't match")
            # pass


    def checkrecoverykey(self, txt):
        recovery_key_hash = self.security.hashpassword(str(txt).encode('utf-8')) # self.ui.reset_window.rkey_text.get()
        self.db.cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND recovery_key = ?', [(recovery_key_hash)])
        checked = self.db.cursor.fetchall()
        
        if checked:
            self.messages["checked"] = True
            # self.ui.initial_window.start()
        else:
            self.messages["checked"] = False
            # self.ui.reset_window.rkey_text.delete(0, 'end')
            # self.ui.reset_window.message_label.config(text='Wrong Key')
