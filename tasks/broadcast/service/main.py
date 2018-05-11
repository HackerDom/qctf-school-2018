from sanic import Sanic, response
import asyncio
from hashlib import sha1

from flags import FLAGS as TOKENS

app = Sanic(__name__)
app.static('/static', './static')


SECRET = "secret? really?"
MESSAGES = ["< Wake up, hero!", "< We need your help!", "< Hurry up!", "< Sending our coordinates..."]
with open("index.html") as index:
    INDEX_PAGE = index.read()


@app.route('/<token>/')
async def index(request, token):
    if token not in TOKENS:
        return response.text("Not Found! \nIncorrect token could be used!", 404)
    return response.html(INDEX_PAGE)


@app.websocket('/<token>/broadcast')
async def feed(request, ws, token):
    if token not in TOKENS:
        return response.text("Not Found! \nIncorrect token could be used!", 404)
    for msg in MESSAGES:
        await asyncio.sleep(4)
        await ws.send(msg)
        await asyncio.sleep(7)

    await ws.send(
        b'now, send us back this \'' +
        sha1((token + SECRET).encode()).hexdigest().encode('ascii') +
        b'\' key as bytes and we will send you our coords...'
    )
    if await ws.recv() == sha1((token + SECRET).encode()).hexdigest().encode('ascii'):
        await ws.send(TOKENS[token])
    ws.close()


if __name__ == '__main__':
    app.run(workers=4)
