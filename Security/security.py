from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import hashlib
#import os


class SecurityManager:
    """
    Handles the encryption and decryption of plaintext entries
    """

    def __init__(self):
        self.salt = b'7139'
#        self.salt = os.urandom(16)
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
        obj1 = {"name": self.encrypt(obj["name"], self.encryption_key),
                "url": self.encrypt(obj["url"], self.encryption_key),
                "username": self.encrypt(obj["username"], self.encryption_key),
                "password": self.encrypt(obj["password"], self.encryption_key),
                "notes": self.encrypt(obj["notes"], self.encryption_key)
                }
        return obj1

    def decrypt_fields(self, array):
        results = []
        for obj in array:
            id = obj["id"]
            name = obj["name"]
            url = obj["url"]
            username = obj["username"]
            password = obj["password"]
            note = obj["notes"]
            results.append({"id": id,
                            "name": self.decrypt(name, self.encryption_key),
                            "url": self.decrypt(url, self.encryption_key),
                            "username": self.decrypt(username, self.encryption_key),
                            "password": self.decrypt(password, self.encryption_key),
                            "notes": self.decrypt(note, self.encryption_key)
                            })
        return results

