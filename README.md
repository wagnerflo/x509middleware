# x509middleware: Working with (client) certificates

This Python package contains middleware classes for working with
certificates. Currently it only contains support for extracting client
certificates from the ASGI scope and from headers set by a reverse
proxy.

Note: The package is rather small but solves an immediate need for some
projectes of mine while possibly being generally helpful to other
people. As I chose a rather generic package name, patches or pull
requests with support for other protocols than ASGI as well as
additional functionallty are very welcome.

## Installation

```shell
$ pip install x509middleware
```

## Requirements

* Python v3.3+ (only 3.6+ is being
  [tested](https://github.com/wagnerflo/x509middleware/actions?query=workflow%3Aintegration_tests)).
* The [asn1crypto](https://pypi.org/project/asn1crypto/) package.

## Contents

### x509middleware.asgi.ClientCertificateMiddleware

This middlware class will try to find and parse a client certificate for
a ASGI http or websocket request. It supports the proposed
[tls extension](../../../../django/asgiref/pull/192) to the ASGI protocol
as well as pulling the certificate from a header supplied by a reverse
proxy your app is deployed behind.

It will set the key `scope['client_cert']` to a
*asn1crypto.x509.Certificate* object or *None* if it can't find or parse
a certificate.

#### Parameters
* **app** *(async callable)* – ...
* **use_tls_extension** *(bool=True)* – ...
* **proxy_header** *(str=None)* – Name of the header to try parsing as a
  client certificate or *None* to disable proxy header support. The
  header value can be line-folded, URL/percent-encoded or base64 encoded
  as well as in PEM or DER format. The correct way to decode will be
  detected automatically.

#### Configuring your reverse proxy
You will need to choose a header name when configuring your reverse proxy
as well as the middlware class. Commonly used names are:

* `CLIENT-CERT` – [IETF Draft](https://tools.ietf.org/html/draft-bdc-something-something-certificate-04#section-2).
* `X-SSL-CLIENT-CERT`
* `X-CLIENT-CERT`
* `X-CLIENT-CERTIFICATE`
* `X-CLIENT-CRT`
* `X-SSL-CERT`
* `SSLClientCertb64` – F5 products seem to use or suggest this.

##### Apache / mod_proxy & mod_headers
```apache
ProxyPass / http://127.0.0.1:8000/
RequestHeader unset CLIENT-CERT
RequestHeader set   CLIENT-CERT "%{SSL_CLIENT_CERT}s"
```
##### NGINX
```nginx
location / {
    proxy_pass http://127.0.0.1:8000/;
    proxy_set_header CLIENT-CERT $ssl_client_escaped_cert;
}
```
##### HAProxy
Support for passing the certificate as a DER blob is available starting
version 1.6-dev1. Since DER is a binary format this needs to be base64
encoded.
```
backend back
  mode http
  server app 127.0.0.1:8000
  http-request set-header CLIENT-CERT %[ssl_c_der,base64]
```

#### Using it in Starlette

```python
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
```

#### Using it directly

```python
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
```
