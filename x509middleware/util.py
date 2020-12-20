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

from asn1crypto import x509,pem
from base64 import b64decode
from urllib.parse import unquote_to_bytes

BEGIN_LEN = 27
END_LEN = 25

def decode_header(hdr):
    if hdr.startswith(b'-----BEGIN'):
        if hdr[10:13] == b'%20':
            return unquote_to_bytes(hdr)

        return (
            hdr[:BEGIN_LEN] +
            hdr[BEGIN_LEN:-END_LEN].replace(b' ', b'\n') +
            hdr[-END_LEN:]
        )

    try:
        return b64decode(hdr, validate=True)
    except:
        return None

def load_certificate(data):
    try:
        _,_,data = pem.unarmor(data)
    finally:
        try:
            return x509.Certificate.load(data)
        except:
            return None
