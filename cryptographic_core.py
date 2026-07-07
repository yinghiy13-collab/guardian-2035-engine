from cryptography.fernet import Fernet
import hashlib

class GuardianCrypto:
    def __init__(self, key: str):
        try:
            self.cipher = Fernet(key.encode())
        except Exception:
            print("⚠️ ใช้คีย์ชั่วคราว — ตั้งค่า GUARDIAN_SECRET จริงก่อนใช้งานจริง")
            self.cipher = Fernet(Fernet.generate_key())

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self.cipher.decrypt(token.encode()).decode()

    @staticmethod
    def hash_sha256(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
      
