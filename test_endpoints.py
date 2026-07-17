import requests

base_url = 'https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com'
endpoints = [
    '/api/v1/customers',
    '/api/customers',
    '/customers',
    '/exec/command-center'
]

for ep in endpoints:
    try:
        res = requests.get(base_url + ep)
        print(f'{ep}: {res.status_code} {res.text[:100]}')
    except Exception as e:
        print(f'{ep}: ERROR {e}')
