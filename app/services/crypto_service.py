from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64


def encrypt_des(text: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    cipher = DES.new(key_bytes, DES.MODE_ECB)

    padded_text = pad(text.encode('utf-8'), DES.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)

    # 使用 Base64 编码以便于传输
    return base64.b64encode(encrypted_bytes).decode('utf-8')


def decrypt_des(encrypted_text: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    encrypted_bytes = base64.b64decode(encrypted_text)
    cipher = DES.new(key_bytes, DES.MODE_ECB)

    decrypted_padded_bytes = cipher.decrypt(encrypted_bytes)

    # 去除填充并解码
    unpadded_bytes = unpad(decrypted_padded_bytes, DES.block_size)
    return unpadded_bytes.decode('utf-8')