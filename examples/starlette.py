from starlette.applications import Starlette
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.responses import Response
from starlette.routing import Route
from x509middleware.asgi import ClientCertificateMiddleware

async def hello_common_name(request):
    client_cert = request.scope.get('client_cert')
    if client_cert:
        cn = client_cert.subject.native['common_name']
    else:
        cn = 'unknown'
    return Response(f'Hello, {cn}!', media_type='text/plain')

config = Config('.env')
app = Starlette(
    routes=[ Route('/', hello_common_name) ],
    middleware=[
        Middleware(
            ClientCertificateMiddleware,
            proxy_header=config('CLIENT_CERT_HEADER', default=None)
        )
    ]
)
