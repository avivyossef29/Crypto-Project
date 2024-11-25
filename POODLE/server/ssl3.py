from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64

def encrypt(text: str, cbc_key: bytes, cbc_iv: bytes, mac_key: bytes, mac_iv: bytes) -> bytes:
    text = text.encode()
    # append mac
    mac_cipher = AES.new(mac_key, AES.MODE_CBC, mac_iv)
    text += create_mac(text, mac_cipher)
    # pad & encrypt
    cbc_cipher = AES.new(cbc_key, AES.MODE_CBC, cbc_iv)
    ciphertext = cbc_cipher.encrypt(pad(text, AES.block_size))
    return ciphertext

def decrypt(ciphertext: bytes, cbc_key: bytes, cbc_iv: bytes, mac_key: bytes, mac_iv: bytes) -> str:
    # decrypt & unpad
    cbc_cipher = AES.new(cbc_key, AES.MODE_CBC, cbc_iv)
    text = cbc_cipher.decrypt(ciphertext)
    text = unpad(text)
    mac = text[-AES.block_size:]
    text = text[:-AES.block_size]
    # verify mac
    mac_cipher = AES.new(mac_key, AES.MODE_CBC, mac_iv)
    if not verify_mac(text, mac_cipher, mac):
        raise Exception('Wrong MAC')
    return text.decode()

def create_mac(text: bytes, cipher) -> bytes:
    return cipher.encrypt(pad(text, AES.block_size))[-AES.block_size:]

def verify_mac(text: bytes, cipher, mac: bytes) -> bool:
    return create_mac(text, cipher) == mac

def unpad(text: bytes):
    return text[:-text[-1]]

def bytes_to_str(text: bytes) -> str:
    return base64.b64encode(text).decode()

def str_to_bytes(text: str) -> bytes:
    return base64.b64decode(text)