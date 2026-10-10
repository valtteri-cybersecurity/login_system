import hashlib
import hmac
import secrets


def create_salt():
    return secrets.token_bytes(16)


def create_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
        dklen=32
    )


def compare_hash(stored_hash, new_hash):
    return hmac.compare_digest(stored_hash, new_hash)
