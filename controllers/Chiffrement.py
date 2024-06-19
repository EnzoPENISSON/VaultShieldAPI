import base64

from cryptography.fernet import Fernet
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Chiffrement:
    def __init__(self, uuidkey):
        self.fernet = None
        self.uuidkey = uuidkey
        self.key = None


    def generate_key(self):
        self.key = Fernet.generate_key()
        return self.key

    def runfernet(self, key, uuidkey):
        keyfusion = self.fusion(key, uuidkey)

        self.fernet = Fernet(keyfusion)

    def encrypt_password(self, password):
        if not self.key:
            raise ValueError("Key not generated. Please generate a key first.")
        encrypted_password = self.fernet.encrypt(password.encode())
        return encrypted_password

    def fusion(self, key, uuidkey):
        # Concatenate the keys
        combined_key = key + uuidkey

        # Use a cryptographic hash function to derive a single key
        hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hasher.update(combined_key)
        derived_key = hasher.finalize()

        # Ensure the key is 32 bytes long
        derived_key = derived_key[:32]

        # Encode the key in URL-safe base64
        encoded_key = base64.urlsafe_b64encode(derived_key)

        return encoded_key

    def decrypt_password(self, encrypted_password, key, uuidkey):
        # Derive a single key from the combination of main key and UUID key
        derived_key = self.fusion(key, uuidkey)

        # Initialize Fernet with the derived key
        fernet = Fernet(derived_key)

        try:
            # Decrypt the password
            decrypted_password = fernet.decrypt(encrypted_password).decode()
            return decrypted_password
        except Exception as e:
            return "Decryption failed"

    def isChiffrer(self, element):
        # return True if the element is encrypted (to avoid double encryption)
        if isinstance(element, bytes):
            if element.startswith(b"gAAAAA"):
                return True
            else:
                return False
        elif isinstance(element, str):
            if element.startswith("gAAAAA"):
                return True
            else:
                return False

    def ChiffrerVault(self, vaultclass):
        self.generate_key()

        self.runfernet(self.key, self.uuidkey)

        vaultclass.username = self.encrypt_password(vaultclass.username)
        vaultclass.email = self.encrypt_password(vaultclass.email)
        vaultclass.password = self.encrypt_password(vaultclass.password)
        vaultclass.note = self.encrypt_password(vaultclass.note)

        return vaultclass

    def updateVault(self, vaultclass, fusionkey):
        self.key = fusionkey.encode()
        self.runfernet(self.key, self.uuidkey)
        if not self.isChiffrer(vaultclass.username):
            vaultclass.username = self.encrypt_password(vaultclass.username)
        if not self.isChiffrer(vaultclass.email):
            vaultclass.email = self.encrypt_password(vaultclass.email)
        if not self.isChiffrer(vaultclass.password):
            vaultclass.password = self.encrypt_password(vaultclass.password)
        if not self.isChiffrer(vaultclass.note):
            vaultclass.note = self.encrypt_password(vaultclass.note)

        return vaultclass