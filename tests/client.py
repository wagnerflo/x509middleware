import httpx

client_conf = dict(
    verify='tests/ca.crt',
    cert=('tests/client.crt', 'tests/client.key'),
)

servers = {
    '8001': ('base64pem', 'encode', 'plain'),
    '8002': ('nginx',),
    '8003': ('base64der',)
}

with httpx.Client(**client_conf) as client:
    for port,paths in servers.items():
        for path in paths:
            res = client.get(f"https://127.0.0.1:{port}/{path}/")
            if res.text != 'client':
                raise AssertionError(res.text)
