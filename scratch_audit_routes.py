import os
import glob
import re

services_dir = "d:\\SAMUEL\\HACK 2 SKILL\\IDBI MSME\\Project AAROHAN-AWS\\services"

def find_routes():
    routes_info = []
    for root, dirs, files in os.walk(services_dir):
        if 'main.py' in files:
            path = os.path.join(root, 'main.py')
            service_name = os.path.basename(os.path.dirname(os.path.dirname(path)))
            if service_name == 'services':
                service_name = os.path.basename(os.path.dirname(path))
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # find @app.get("/...") or @router.post("/...")
            pattern = re.compile(r'@(?:app|router)\.(?:get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]')
            for match in pattern.finditer(content):
                route = match.group(1)
                routes_info.append((service_name, route))
    return routes_info

if __name__ == '__main__':
    routes = find_routes()
    routes = sorted(list(set(routes)))
    for r in routes:
        print(f"{r[0]}: {r[1]}")
