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
        entered_pwd = k.encode('utf-8')
        password_hash = self.security.hashpassword(entered_pwd)
        self.security.encryption_key = base64.urlsafe_b64encode(
            self.security.getKDF().derive(k.encode()))
        password = self.db.fetch_master_pwd(password_hash)
        if password:
            self.messages["Password"] = True
            self.refreshall()
        else:
            self.messages["Password"] = False

    def addentry(self, obj):
        entry = self.entryman.createEntry(obj)
        entry.encode()
        encrypted_fields = self.security.encrypt_fields(entry)
        self.db.insert_entry(encrypted_fields)
        self.refreshall()

    def deleteentry(self, entry_id):
        self.db.delete_entry(entry_id)
        self.refreshall()

    def search(self, string):
        print(string)
        txt = string
        for i in self.entryman.entries:
            if not any([
                re.search(txt, i.name.decode()),
                re.search(txt, i.url.decode()),
                re.search(txt, i.username.decode()),
                re.search(txt, i.password.decode()),
                re.search(txt, i.notes.decode())
            ]):
                self.entryman.entries.remove(i)

    def loadentries(self):
        enc = self.db.fetch_entries()
        for i in enc:
            entry = self.entryman.createEntry(i)
            e = self.security.decrypt_fields(entry)
            self.entryman.entries.append(e)

    def refreshall(self):
        self.entryman.flush()
        self.loadentries()

    def savemasterpassword(self, p, cpwd):
        password = p
        confirmation = cpwd
        if password == confirmation:
            password = p
            password = password.encode('utf-8')
            self.db.clearmasterpassword()
            password_hash = self.security.hashpassword(password)
            key = str(uuid.uuid4().hex)
            recovery_key = self.security.hashpassword(key.encode('utf-8'))
            self.security.encryption_key = base64.urlsafe_b64encode(
                self.security.getKDF().derive(password)
            )
            self.db.insert_keys(password_hash, recovery_key)
            self.messages["key"] = key
        else:
            self.messages["key"] = ""

    def checkrecoverykey(self, txt):
        recovery_key_hash = self.security.hashpassword(str(txt).encode('utf-8'))
        checked = self.db.fetchRKey(recovery_key_hash)
        if checked:
            self.messages["checked"] = True
        else:
            self.messages["checked"] = False
