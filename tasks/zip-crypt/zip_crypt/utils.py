import os
import zlib

from zip_crypt.settings import CIPHER_TYPE
from zip_crypt.crypto import aes128cbc_encrypt, aes128ctr_encrypt


def block_encrypt(plaintext):
    key = os.urandom(32)
    iv = os.urandom(16)
    return aes128cbc_encrypt(plaintext, key, iv)


def stream_encrypt(plaintext):
    key = os.urandom(32)
    nonce = os.urandom(16)
    return aes128ctr_encrypt(plaintext, key, nonce)


def encrypt(data):
    if CIPHER_TYPE == 'block':
        return block_encrypt(data)
    elif CIPHER_TYPE == 'stream':
        return stream_encrypt(data)
    else:
        raise ValueError('CYPHER_TYPE should be set to either \'block\' or \'stream\'')


def compress(data):
    return zlib.compress(data, level=1)


def generate_secure_message(user_text, flag):
    secret_text = f'Long time no see! {flag}'
    data = f'{secret_text}\n{user_text}'.encode('utf-8')
    return encrypt(compress(data))
