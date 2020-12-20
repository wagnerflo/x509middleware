from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import Response
from starlette.routing import Route,Mount
from x509middleware.asgi import ClientCertificateMiddleware

async def common_name(request):
    client_cert = request.scope.get('client_cert')
    if client_cert is None:
        return Response('None', media_type='text/plain')
    return Response(
        f"{client_cert.subject.native['common_name']}",
        media_type='text/plain'
    )

def create_sub_app(proxy_header):
    return Starlette(
        routes=[Route('/', common_name)],
        middleware=[
            Middleware(
                ClientCertificateMiddleware,
                proxy_header=proxy_header
            )
        ]
    )

app = Starlette(
    debug=True,
    routes=[
        Route('/', common_name),
        Mount('/base64', create_sub_app('client-cert-base64')),
        Mount('/encode', create_sub_app('client-cert-encode')),
        Mount('/plain',  create_sub_app('client-cert-plain')),
        Mount('/nginx',  create_sub_app('client-cert-nginx')),
    ],
)
