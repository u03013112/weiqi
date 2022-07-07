from aiohttp import web
import aiohttp_cors

import sys
sys.path.append('/core')

from core import Core8X8

core = Core8X8()

async def test(request):
    outData = {'status': 'success'}    
    return web.json_response(outData)

async def start(request):
    core = Core8X8()
    outData = core.getStatus()    
    return web.json_response(outData)

async def do(request):
    inData = await request.json()
    x = inData['x']
    y = inData['y']
    core.do(x,y)
    outData = core.getStatus()    
    return web.json_response(outData)

app = web.Application()
cors = aiohttp_cors.setup(app)

app.add_routes([web.get('/test', test)])
app.add_routes([web.get('/start', start)])
app.add_routes([web.post('/do', do)])

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app)