import binascii


def parse_encryption_key(hex_key: str) -> bytes:
    """
    Converts a hex string to bytes and checks the length for AES (16, 24, 32 bytes).
    """
    try:
        key_bytes = binascii.unhexlify(hex_key)
    except binascii.Error:
        raise ValueError("Encryption key must be a valid hex string")

    if len(key_bytes) not in (16, 24, 32):
        raise ValueError("Encryption key must be 16, 24, or 32 bytes long")

    return key_bytes
