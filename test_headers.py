import requests

base_url = 'https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com'
endpoints = [
    '/customers',
    '/api/customers',
    '/customers/1',
    '/exec/command-center'
]

for ep in endpoints:
    try:
        res = requests.get(base_url + ep)
        print(f'{ep}: {res.status_code}')
        print(f'Headers: {res.headers}')
        print(f'Body: {res.text[:100]}\n')
    except Exception as e:
        print(f'{ep}: ERROR {e}')
