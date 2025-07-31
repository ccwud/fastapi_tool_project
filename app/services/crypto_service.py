from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib


def encrypt_des(text: str, key: str) -> str:
    # 将任意长度的密钥转换为8字节的DES密钥
    key_bytes = _prepare_des_key(key)
    cipher = DES.new(key_bytes, DES.MODE_ECB)

    padded_text = pad(text.encode('utf-8'), DES.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)

    # 使用 Base64 编码以便于传输
    return base64.b64encode(encrypted_bytes).decode('utf-8')


def decrypt_des(encrypted_text: str, key: str) -> str:
    # 将任意长度的密钥转换为8字节的DES密钥
    key_bytes = _prepare_des_key(key)
    encrypted_bytes = base64.b64decode(encrypted_text)
    cipher = DES.new(key_bytes, DES.MODE_ECB)

    decrypted_padded_bytes = cipher.decrypt(encrypted_bytes)

    # 去除填充并解码
    unpadded_bytes = unpad(decrypted_padded_bytes, DES.block_size)
    return unpadded_bytes.decode('utf-8')


def _prepare_des_key(key: str) -> bytes:
    """将任意长度的密钥转换为8字节的DES密钥"""
    key_bytes = key.encode('utf-8')
    
    if len(key_bytes) == 8:
        return key_bytes
    elif len(key_bytes) < 8:
        # 如果密钥太短，用零填充到8字节
        return key_bytes.ljust(8, b'\x00')
    else:
        # 如果密钥太长，使用MD5哈希的前8字节
        hash_obj = hashlib.md5(key_bytes)
        return hash_obj.digest()[:8]