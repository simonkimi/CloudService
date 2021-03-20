import asyncio

from sanic import Sanic
from sanic.response import json
from asyncTask.tasks import get_token
from celery.result import AsyncResult

app = Sanic("App Name")


@app.post("/")
async def test(request):
    if type(request.json) is dict:
        username = request.json['username']
        password = request.json['password']
        server = request.json['server']
        count = 0
        result: AsyncResult = get_token.delay(username, password, server)
        while result.result is None and count < 10:
            await asyncio.sleep(1)
        if result.result is not None:
            return json(result.result)
        return json({
            'error': '400',
            'errmsg': '超时!'
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
