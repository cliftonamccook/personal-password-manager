from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import hashlib


class SecurityManager:
    """
    Handles the encryption and decryption of plaintext entries
    """

    def __init__(self):
        self.salt = b'7139'
        # self.salt = os.urandom(16)
        self.backend = default_backend()
        self.encryption_key = None

    def encrypt(self, message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(self, message: bytes, token: bytes) -> bytes:
        return Fernet(token).decrypt(message)

    def hashpassword(self, pwd):
        password_hash = hashlib.sha256(pwd)
        password_hash = password_hash.hexdigest()
        return password_hash

    def getKDF(self):
        """
        key derivation function
        derives encryption key from user password
        :return: PBKDF2HMAC
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf

    def encrypt_fields(self, obj):
        enc_obj = obj
        enc_obj.name = self.encrypt(enc_obj.name, self.encryption_key)
        enc_obj.url = self.encrypt(enc_obj.url, self.encryption_key)
        enc_obj.username = self.encrypt(enc_obj.username, self.encryption_key)
        enc_obj.password = self.encrypt(enc_obj.password, self.encryption_key)
        enc_obj.notes = self.encrypt(enc_obj.notes, self.encryption_key)
        return enc_obj

    def decrypt_fields(self, obj):
        dec_obj = obj
        dec_obj.name = self.decrypt(dec_obj.name, self.encryption_key)
        dec_obj.url = self.decrypt(dec_obj.url, self.encryption_key)
        dec_obj.username = self.decrypt(dec_obj.username, self.encryption_key)
        dec_obj.password = self.decrypt(dec_obj.password, self.encryption_key)
        dec_obj.notes = self.decrypt(dec_obj.notes, self.encryption_key)
        return dec_obj
