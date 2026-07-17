import re

alb_rules = {
    '/auth/*': '9000',
    '/ese/*': '9090',
    '/customers/*': '9001',
    '/consents/*': '9002',
    '/gst/*': '9003',
    '/aa/*': '9004',
    '/fhc/*': '9005',
    '/credit/*': '9006',
    '/cam/*': '9007',
    '/ocen/*': '9008',
    '/ckyc/*': '9011',
    '/mca/*': '9012',
    '/epfo/*': '9013',
    '/exec/*': '9009',
    '/rm/*': '9010'
}

frontend_calls = [
    '/aa/',
    '/cam/',
    '/ckyc/',
    '/credit/',
    '/customers/',
    '/epfo/',
    '/exec/',
    '/fhc/',
    '/gst/',
    '/mca/',
    '/ese/',
    '/auth/',
    '/rbi/',
    '/ocen/'
]

fastapi_prefixes = {
    '9000': '/auth/',
    '9001': '/customers/',
    '9002': '/consents/',
    '9003': '/gst/',
    '9004': '/aa/',
    '9005': '/fhc/',
    '9006': '/credit/',
    '9007': '/cam/',
    '9008': '/ocen/',
    '9009': '/exec/',
    '9010': '/rm/',
    '9011': '/ckyc/',
    '9012': '/mca/',
    '9013': '/epfo/',
    '9090': '/ese/'
}

print("Checking Frontend -> ALB")
for call in frontend_calls:
    matched = False
    for rule in alb_rules.keys():
        if rule.startswith(call) or call.startswith(rule.replace('*', '')):
            matched = True
    if not matched:
        print(f"Frontend calls {call} but no ALB rule matches.")

print("Checking ALB -> FastAPI")
for rule, port in alb_rules.items():
    prefix = rule.replace('/*', '/')
    if not fastapi_prefixes[port].startswith(prefix) and not prefix.startswith(fastapi_prefixes[port]):
         print(f"ALB rule {rule} goes to port {port}, but FastAPI prefix is {fastapi_prefixes[port]}")
