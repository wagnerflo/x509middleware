import httpx

client_conf = dict(
    verify='tests/ca.crt',
    cert=('tests/client.crt', 'tests/client.key'),
)

with httpx.Client(**client_conf) as client:
    for path in ('base64', 'encode', 'plain'):
        res = client.get(f"https://127.0.0.1:8001/{path}/")
        assert res.text == 'client'
