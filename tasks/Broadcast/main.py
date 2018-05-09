from sanic import Sanic, response
import asyncio

app = Sanic(__name__)
app.static('/static', './static')

FLAG = "QCTF{{y0u_h4ve_13arnt_w3bs0cket_m4agic_{}}}".format("abrakadabra")

MESSAGES = ["> Wake up, hero!", "> We need your help!", "> Hurry up!", "> Sending our coordinates..."]
with open("index.html") as index:
    INDEX_PAGE = index.read()


@app.route('/')
async def index(request):
    return response.html(INDEX_PAGE)


@app.websocket('/broadcast')
async def feed(request, ws):
    for msg in MESSAGES:
        await asyncio.sleep(4)
        await ws.send(msg)
        await asyncio.sleep(8)
    await ws.send(b'now, send us this \'alohomora\' key as bytes and we will open you our coords...')
    if await ws.recv() == b'alohomora':
        await ws.send(FLAG)
    ws.close()


if __name__ == '__main__':
    app.run("0.0.0.0", 8080, workers=4)
