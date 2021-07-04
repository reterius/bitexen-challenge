import hashlib


def hash_sha256(password: str):
    hash_object = hashlib.sha256(str(password).encode())
    return hash_object.hexdigest()


def hash_md5(password: str):
    hash_object = hashlib.md5(str(password).encode())
    return hash_object.hexdigest()
