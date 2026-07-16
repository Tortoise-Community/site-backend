import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Encryption(object):

    def __init__(self, key):
        self.key = key

    def encrypt_token(self, token: str) -> dict:
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, token.encode(), None)

        return {
            "ciphertext": ciphertext,
            "nonce": nonce,
        }

    def decrypt_token(self, encrypted_token: bytes, nonce: bytes) -> str:
        aesgcm = AESGCM(self.key)
        plaintext = aesgcm.decrypt(nonce, encrypted_token, None)
        return plaintext.decode()
