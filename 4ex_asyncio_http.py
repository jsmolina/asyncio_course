import asyncio
import aiohttp
from aiohttp import web
import json

non_eligible_users = ['1234', '456']
url = 'http://google.com'

@asyncio.coroutine
def queue_event(msisdn):
    template = {
            "id": "12345678",
            "notifiedEvent": [
                'super_event'
            ]
        }
    template = json.dumps(template)
    response = yield from aiohttp.request('POST', url, data=template)
    return (yield from response.read())

@asyncio.coroutine
def activate_service(request):
    msisdn = request.match_info.get('msisdn', "")
    msisdn = msisdn.replace('tel:+', '')

    if msisdn not in non_eligible_users:
        yield from queue_event(msisdn)
        content = {
                "status": "Operation in progress",
                "transaction_id": "12345"
            }
        return web.Response(body=bytes(json.dumps(content), encoding='utf-8'))
    else:
        content = {"exceptionId": "SVC4006",
                       "exceptionText": "User not eligible"}

        return web.Response(body=bytes(json.dumps(content), encoding='utf-8'), status=403)


@asyncio.coroutine
def update_service(request):
    return web.Response(body=b'ok')

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/{msisdn}/services', activate_service)
    app.router.add_route('GET', '/{msisdn}/services/{service_id}', update_service)

    srv = yield from loop.create_server(app.make_handler(),
                                        '127.0.0.1', 8080)
    print("Server started at http://127.0.0.1:8080")
    return srv



loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()