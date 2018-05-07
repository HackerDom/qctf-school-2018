from flask import Flask, make_response, request, render_template
from utils import load_file


app = Flask(__name__)


FLAG = "QCTF{h3re_is_y0ur_R4ng3d_st4Sh}".encode()
FILE_BYTES = load_file("coordinates.gif")
FULL_CONTENT = FILE_BYTES + FLAG
FULL_CONTENT_LENGTH = len(FULL_CONTENT)


@app.route("/")
def main_route():
    return render_template("index.html")


@app.route("/coordinates.gif")
def test_route():
    if request.range:
        if request.range.units != "bytes":
            return make_response("Only 'bytes' range is acceptable!", 416)
        file_range = request.range.ranges[0]
        if not all(x is not None for x in file_range):
            return make_response("Range accepts only limited interval of bytes!", 416)
        parsed_bytes = return_file_bytes(*file_range)
        if parsed_bytes is None:
            return make_response("Bad range!", 416)
        resp = make_response(parsed_bytes, 200 if parsed_bytes == FULL_CONTENT else 206)
        resp.headers["Content-Range"] = "bytes {}-{}/{}".format(file_range[0], file_range[1]-1, FULL_CONTENT_LENGTH)
    else:
        resp = make_response(return_file_bytes(0, len(FILE_BYTES)), 206)
        resp.headers["Content-Range"] = "bytes 0-{}/{}".format(len(FILE_BYTES) - 1, FULL_CONTENT_LENGTH)

    resp.headers["Content-Type"] = "application/octet-stream"
    return resp


def return_file_bytes(start, end):
    if not (len(FULL_CONTENT) > start >= 0 and start < end <= len(FULL_CONTENT)):
        return None
    return FULL_CONTENT[start:end]


if __name__ == '__main__':
    app.run("0.0.0.0", 8080, threaded=True)
