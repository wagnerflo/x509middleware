# Copyright 2020 Florian Wagner <florian@wagner-flo.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .util import load_certificate,decode_header

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

__all__ = (
    'ClientCertificateMiddleware',
)
