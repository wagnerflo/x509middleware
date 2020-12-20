from os import environ
from x509middleware.asgi import ClientCertificateMiddleware

async def hello_common_name(scope, receive, send):
    client_cert = scope.get('client_cert')
    if client_cert:
        cn = client_cert.subject.native['common_name']
    else:
        cn = 'unknown'
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'text/plain; charset=utf-8'),
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': f'Hello, {cn}!'.encode('utf8'),
    })

app = ClientCertificateMiddleware(
    hello_common_name,
    proxy_header=environ.get('CLIENT_CERT_HEADER'),
)
