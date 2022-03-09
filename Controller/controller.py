import uuid
#import re
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
            self.refresh()
        else:
            self.ui.login_window.master_password_text.delete(0, 'end')
            self.ui.login_window.error_text.config(text="Wrong Password")

#    def resetpassword(self):
#        self.ui.reset_window.start()

    def encode_values(self, obj):
        obj1 = {"name": obj["name"].encode(),
                "url": obj["url"].encode(),
                "username": obj["username"].encode(),
                "password": obj["password"].encode(),
                "notes": obj["notes"].encode()
                }
        return obj1

    def encrypt_fields(self, obj):
        obj1 = self.security.encrypt_fields(obj)
        return obj1

    def addentry(self, obj):
        encoded_fields = self.encode_values(obj)
        encrypted_fields = self.encrypt_fields(encoded_fields)
        self.db.insert_entry(encrypted_fields)
        self.refresh()

    def refresh(self):
        self.decrypt_entries()
        self.ui.password_vault_window.start()

    def get_entries(self):
        enc = self.db.fetch_entries()
        return enc

    def decrypt_entries(self):
        enc = self.get_entries()
        obj = self.security.decrypt_fields(enc)
        self.results = obj

    def deleteentry(self,input):
        self.db.delete_entry(input)
        self.refresh()

#    def savemasterpassword(self):
#        password = self.ui.initial_window.get_masterpwdtxt()
#        confirmation = self.ui.initial_window.get_confirmpwdtxt()
#        if password == confirmation:
#            password = self.ui.initial_window.get_masterpwdtxt()
#            password = password.encode('utf-8')
#            # print(password)
#
#            self.db.clearmasterpassword()
#
#            password_hash = self.security.hashpassword(password)
#            key = str(uuid.uuid4().hex)
#            recovery_key = self.security.hashpassword(key.encode('utf-8'))
#
#            self.security.encryption_key = base64.urlsafe_b64encode(
#                self.security.getKDF().derive(password)
#            )
#
#            self.db.insert_keys(password_hash, recovery_key)
#
#            self.ui.recovery_window.startRecovery(key)
#        else:
#            self.ui.initial_window.show_msg("Passwords don't match")

    def savemasterpassword(self):
        password = self.ui.initial_window.get_masterpwdtxt()
        confirmation = self.ui.initial_window.get_confirmpwdtxt()
        if password == confirmation:
            password = self.ui.initial_window.get_masterpwdtxt()
            password = password.encode('utf-8')
            # print(password)

            self.db.clearmasterpassword()

            password_hash = self.security.hashpassword(password)
#            key = str(uuid.uuid4().hex)
#            recovery_key = self.security.hashpassword(key.encode('utf-8'))

            self.security.encryption_key = base64.urlsafe_b64encode(
                self.security.getKDF().derive(password)
            )

#            self.db.insert_keys(password_hash, recovery_key)
            self.db.insert_keys(password_hash)

#            self.ui.recovery_window.startRecovery(key)
            self.refresh()
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

    # def search(self, txt):
    #     ids = []
    #     for entry in self.results:
    #         x = re.findall(txt, entry["name"])
    #         y = re.findall(txt, entry["url"])
    #         z = re.findall(txt, entry["username"])
    #         a = re.findall(txt, entry["password"])
    #         b = re.findall(txt, entry["notes"])
    #         if len(x) > 0 or len(y) > 0 or len(z) > 0 or len(a) > 0 or len(b) > 0:
    #             ids.append(entry["id"])
    #     if len(ids) > 0:
    #         entries = self.db.fetch_ids(ids)
    #         self.results = entries

