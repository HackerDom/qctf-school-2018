from base64 import b64encode, b64decode
import binascii


BASE64URL_ALTCHARS = b'-_'


class Base64UrlDecodeError(ValueError):
    pass


def base64url_encode(data):
    return b64encode(data, altchars=BASE64URL_ALTCHARS).decode('utf-8').rstrip('=')


def try_b64decode(encoded, altchars=None):
    try:
        return b64decode(encoded, altchars=altchars)
    except binascii.Error:
        return None


def base64url_decode(encoded):
    for padding in ('', '=', '=='):
        result = try_b64decode(encoded + padding, altchars=BASE64URL_ALTCHARS)
        if result is not None:
            break
    else:
        raise Base64UrlDecodeError('Could not find a correct padding')
    return result
