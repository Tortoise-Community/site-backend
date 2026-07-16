import random
import hashlib
import binascii

from django.contrib.auth import settings


class Hashing(object):
    def __init__(self, method="sha256",
                 salt=settings.ENCRYPTION_SALT,
                 iterations=int(settings.ENCRYPTION_ITERATION)):
        self.method = method
        self.salt = bytes(salt, 'utf-8')
        self.iterations = iterations

    def _position_randomizer(self, text_hash: str):
        random.seed(self.iterations)
        return "".join(random.sample(text_hash, len(text_hash)))

    def encrypted_hash_gen(self, *args):
        concat_text = "".join(arg for arg in args)
        random_text = self._position_randomizer(concat_text)
        return hashlib.sha256(random_text.encode()).hexdigest()

    @staticmethod
    def get_sha1(text_hash):
        return hashlib.sha1(text_hash.encode()).hexdigest()

    def get_hashed_pass(self, text):
        hash_obj = hashlib.pbkdf2_hmac(self.method,
                                       bytes(text, 'utf-8'), self.salt, self.iterations)
        return str(binascii.hexlify(hash_obj))

    def hashed_user_pass(self, email, user_id):
        text_hash = self.encrypted_hash_gen(email, user_id)
        sha256_hash = self.get_hashed_pass(text_hash)
        return self.get_sha1(sha256_hash)
