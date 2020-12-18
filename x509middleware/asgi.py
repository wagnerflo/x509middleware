from .util import load_certificate,decode_header

# common proxy headers are
#   CLIENT-CERT
#   X-SSL-CLIENT-CERT
#   X-CLIENT-CERT
#   X-CLIENT-CERTIFICATE
#   X-CLIENT-CRT
#   X-SSL-CERT
#   SSLClientCertb64

class ClientCertificateMiddleware:
    def __init__(self, app, *, use_tls_extension=True, proxy_header=None):
        self.app = app
        self.use_tls_extension = use_tls_extension
        if proxy_header is not None:
            if isinstance(proxy_header, str):
                proxy_header = proxy_header.encode('ascii')
            proxy_header = proxy_header.lower()
        self.proxy_header = proxy_header

    async def find_certificate(self, scope):
        # try per upcoming asgi tls extension (https://git.io/JL4dO)
        if self.use_tls_extension:
            try:
                return load_certificate(
                    next(iter(scope['extensions']['tls']['tls_client_cert_chain']))
                )
            except (KeyError, StopIteration):
                pass

        # try configured proxy header
        if self.proxy_header:
            for name,value in scope['headers']:
                if name == self.proxy_header:
                    return load_certificate(decode_header(value))

        return None

    async def __call__(self, scope, receive, send):
        if scope['type'] in ('http', 'websocket'):
            scope['client_cert'] = await self.find_certificate(scope)
        return await self.app(scope, receive, send)
