import json

from zip_crypt.crypto import aes128cbc_encrypt, aes128cbc_decrypt
from zip_crypt.flag_utils.base64url import base64url_encode, base64url_decode, Base64UrlDecodeError


def generate_token(team_id, task_name, key, iv):
    token_payload = {
        'task': task_name,
        'team': team_id
    }
    plaintext = json.dumps(token_payload).encode('utf-8')
    ciphertext = aes128cbc_encrypt(plaintext, key, iv)
    return base64url_encode(ciphertext)


def decode_team_id(token, task_name, key, iv):
    decoded_token = base64url_decode(token)
    decrypted_token = aes128cbc_decrypt(decoded_token, key, iv)
    token_payload = json.loads(decrypted_token.decode('utf-8'))
    token_task_name = token_payload.get('task')
    if token_task_name != task_name:
        raise ValueError(f'Task name mismatch in the token. Expected: {task_name}, actual: {token_task_name}')
    return int(token_payload['team'])


def try_decode_team_id(token, task_name, key, iv):
    try:
        return decode_team_id(token, task_name, key, iv)
    except (Base64UrlDecodeError, ValueError, UnicodeDecodeError, json.decoder.JSONDecodeError, KeyError):
        return None
