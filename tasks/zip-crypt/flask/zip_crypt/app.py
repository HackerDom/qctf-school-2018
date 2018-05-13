import functools
import io

from flask import Flask, request, abort, render_template, send_file

from zip_crypt.utils import generate_secure_message
from zip_crypt.settings import FLAG_MANAGER_SECRET, TASK_NAME, FLAG_FORMAT
from zip_crypt.flag_utils.flag_manager import FlagManager, InvalidTokenError


app = Flask(__name__)


flag_manager = FlagManager(FLAG_MANAGER_SECRET, TASK_NAME, FLAG_FORMAT)


def token_to_flag(f):
    @functools.wraps(f)
    def decorated(token, *args, **kwargs):
        try:
            flag = flag_manager.flag_by_token(token)
        except InvalidTokenError:
            return abort(403)
        return f(flag, *args, **kwargs)
    return decorated


@app.route('/<token>/')
@token_to_flag
def root(flag):
    return render_template('index.html')


@app.route('/<token>/encrypt', methods=['POST'])
@token_to_flag
def encrypt(flag):
    user_text = request.form.get('text')
    message = generate_secure_message(user_text, flag)
    message_fp = io.BytesIO(message)
    return send_file(
        message_fp,
        as_attachment=True,
        attachment_filename='encrypted_message.bin',
        mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
