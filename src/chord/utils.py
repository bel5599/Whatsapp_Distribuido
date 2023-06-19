from hashlib import sha256


def generate_id(text: str, bits=64):
    return int(sha256(text.encode()).hexdigest(), 16) % 2**bits
