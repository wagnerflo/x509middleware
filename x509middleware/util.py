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
        _,_,der = pem.unarmor(data)
        return x509.Certificate.load(der)
    except:
        return None
