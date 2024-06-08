import base64
from cryptography.fernet import Fernet
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class Chiffrement:
    def __init__(self):
        self.fernet = None
        self.key = None

    def generate_key(self):
        try:
            self.key = Fernet.generate_key()
            return self.key
        except Exception as e:
            print("Error generating key:", e)

    def generate_uuid(self):
        try:
            self.uuidkey = uuid.uuid4().bytes
            return self.uuidkey
        except Exception as e:
            print("Error generating UUID:", e)

    def runfernet(self, key, uuidkey):
        try:
            keyfusion = self.fusion(key, uuidkey)
            self.fernet = Fernet(keyfusion)
        except Exception as e:
            print("Error setting up Fernet:", e)

    def encrypt_password(self, password):
        try:
            if not self.key:
                raise ValueError("Key not generated. Please generate a key first.")
            encrypted_password = self.fernet.encrypt(password.encode())
            return encrypted_password
        except Exception as e:
            print("Encryption failed:", e)

    def fusion(self, key, uuidkey):
        try:
            combined_key = key + uuidkey
            hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
            hasher.update(combined_key)
            derived_key = hasher.finalize()
            derived_key = derived_key[:32]
            encoded_key = base64.urlsafe_b64encode(derived_key)
            return encoded_key
        except Exception as e:
            print("Key fusion failed:", e)

    def decrypt_password(self, encrypted_password, key, uuidkey):
        try:
            derived_key = self.fusion(key, uuidkey)
            fernet = Fernet(derived_key)
            decrypted_password = fernet.decrypt(encrypted_password).decode()
            return decrypted_password
        except Exception as e:
            print("Decryption failed:", e)

    def runFromStringg(self, key, uuidkey, password):
        try:
            key = key.encode()
            uuidkey = uuid.UUID(uuidkey).bytes
            self.runfernet(key, uuidkey)
            encrypted_password = self.decrypt_password(password, key, uuidkey)
            return encrypted_password
        except Exception as e:
            print("Error running from string:", e)

def run():
    try:
        password_manager = Chiffrement()
        key = password_manager.generate_key()
        print("Clé secrète:", key)
        uuidkey = password_manager.generate_uuid()
        print("UUID généré:", uuidkey)
        password_manager.runfernet(key, uuidkey)
        password_to_encrypt = "MotDePasseSecret123"
        encrypted_password = password_manager.encrypt_password(password_to_encrypt)
        print("Mot de passe chiffré:", encrypted_password)
        received_key = key
        print("Clé secrète:", received_key)
        decrypted_password = password_manager.decrypt_password(encrypted_password, received_key, uuidkey)
        print("Mot de passe déchiffré:", decrypted_password)
    except Exception as e:
        print("Error in run():", e)

def test(uuidkey, key, passwordchiffre):
    try:
        print("UUID:", uuidkey)
        print("Clé secrète:", key)
        print("Mot de passe chiffré à déchiffrer :", passwordchiffre)
        password_manager = Chiffrement()
        res = password_manager.runFromStringg(key, uuidkey, passwordchiffre)
        print("Mot de passe déchiffré:", res)
    except Exception as e:
        print("Error in test():", e)

test(
   uuidkey="e771380c-0718-4be3-8f4c-907d2f47c09f",
   key="RdWWUGi_rwP_NoP45z24YGn30Qto0n3BMHTmDcyLdhU=",
   passwordchiffre="gAAAAABmZEUWx0p_M1k2vkqgJZO0ED436eH-N4VnXK87LK4TOTuxiMGoo9STNGx5UgItIq3-zXsutpRptFr5bcYosLbfKkdTSQ=="
)
