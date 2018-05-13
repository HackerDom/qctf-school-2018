from flask import Flask, make_response, request, render_template
from utils import load_file
from flags import FLAGS as TOKENS


app = Flask(__name__)

FILE_BYTES = load_file("coordinates.gif")


@app.route("/<token>/")
def main_route(token):
    if token not in TOKENS:
        return "Missing token in abspath!", 404
    return render_template("index.html")


@app.route("/<token>/coordinates.gif")
def test_route(token):
    if token not in TOKENS:
        return "Missing token in abspath!", 404
    full_content = FILE_BYTES + TOKENS[token].encode()
    full_content_length = len(full_content)
    if request.range:
        if request.range.units != "bytes":
            return make_response("Only 'bytes' range is acceptable!", 416)
        file_range = request.range.ranges[0]
        if not all(x is not None for x in file_range):
            return make_response("Range accepts only limited interval of bytes!", 416)
        parsed_bytes = return_file_bytes(*file_range, full_content)
        if parsed_bytes is None:
            return make_response("Bad range!", 416)
        resp = make_response(parsed_bytes, 200 if parsed_bytes == full_content else 206)
        resp.headers["Content-Range"] = "bytes {}-{}/{}".format(file_range[0], file_range[1]-1, full_content_length)
    else:
        resp = make_response(return_file_bytes(0, len(FILE_BYTES), full_content), 206)
        resp.headers["Content-Range"] = "bytes 0-{}/{}".format(len(FILE_BYTES) - 1, full_content_length)

    resp.headers["Content-Type"] = "application/octet-stream"
    return resp


def return_file_bytes(start, end, full_content):
    if not (len(full_content) > start >= 0 and start < end <= len(full_content)):
        return None
    return full_content[start:end]


if __name__ == '__main__':
    app.run(threaded=True)
