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
            self.ui.login_window.show_error()

    def refresh(self):
        self.ui.password_vault_window.start()

    def savemasterpassword(self):
        password = self.ui.initial_window.get_masterpwdtxt()
        confirmation = self.ui.initial_window.get_confirmpwdtxt()
        if password == confirmation:
            password = self.ui.initial_window.get_masterpwdtxt()
            password = password.encode('utf-8')

            self.db.clearmasterpassword()

            password_hash = self.security.hashpassword(password)

            self.security.encryption_key = base64.urlsafe_b64encode(
                self.security.getKDF().derive(password)
            )

            self.db.insert_keys(password_hash)
            self.refresh()
        else:
            self.ui.initial_window.show_msg("Passwords don't match")


