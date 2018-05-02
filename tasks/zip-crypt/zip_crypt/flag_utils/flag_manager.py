import os
import hashlib

from zip_crypt.flag_utils.base64url import base64url_encode, base64url_decode
from zip_crypt.flag_utils.tokens import try_decode_team_id, generate_token


class InvalidTokenError(ValueError):
    pass


class FlagManager:
    def __init__(self, secret, task_name, flag_format):
        encoded_key, encoded_iv, encoded_flag_secret = secret.split(';')
        self._key = base64url_decode(encoded_key)
        self._iv = base64url_decode(encoded_iv)
        self._flag_secret = base64url_decode(encoded_flag_secret)

        self._task_name = task_name
        self._flag_format = flag_format

    @staticmethod
    def generate_secret(key=None, iv=None, flag_secret=None):
        if key is None:
            key = base64url_encode(os.urandom(32))
        if iv is None:
            iv = base64url_encode(os.urandom(16))
        if flag_secret is None:
            flag_secret = base64url_encode(os.urandom(16))
        return f'{key};{iv};{flag_secret}'

    def team_hash(self, team_id):
        return hashlib.sha256(f'{team_id};{self._task_name};{self._flag_secret}'.encode('utf-8')).hexdigest()

    def flag_by_team_id(self, team_id):
        team_hash = self.team_hash(team_id)
        return self._flag_format.format(team_hash=team_hash)

    def token_by_team_id(self, team_id):
        return generate_token(team_id, self._task_name, self._key, self._iv)

    def team_id_by_token(self, token):
        team_id = try_decode_team_id(token, self._task_name, self._key, self._iv)
        if team_id is None:
            raise InvalidTokenError
        return team_id

    def flag_by_token(self, token):
        return self.flag_by_team_id(self.team_id_by_token(token))
