import os


def getenv(key):
    value = os.getenv(key)
    if value is None:
        raise ValueError('Please provide a value for the environment variable {}'.format(key))
    return value


CIPHER_TYPE = getenv('CIPHER_TYPE')

FLAG_MANAGER_SECRET = getenv('FLAG_MANAGER_SECRET')
TASK_NAME = 'zip_crypt'
FLAG_FORMAT = 'QCTF{{WATCH_YOUR_SIDE_CHANNELS_{team_hash:.8}}}'
