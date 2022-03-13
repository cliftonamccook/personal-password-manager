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
        self.backend = default_backend()
        self.encryption_key = None

    def encrypt(self, message: bytes, key: bytes) -> bytes:
        """
        performs symmetric encryption of message using key
        """
        return Fernet(key).encrypt(message)

    def decrypt(self, message: bytes, token: bytes) -> bytes:
        """
        performs decryption of symmetrically encrypted message using key
        """
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

