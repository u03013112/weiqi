from aiohttp import web
import aiohttp_cors

import sys
sys.path.append('/src')

async def test(request):
    outData = {'status': 'success'}    
    return web.json_response(outData)

app = web.Application()
cors = aiohttp_cors.setup(app)
app.add_routes([web.get('/test', test)])

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