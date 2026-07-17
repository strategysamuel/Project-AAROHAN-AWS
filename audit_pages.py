import os, re

pages_dir = r"d:\SAMUEL\HACK 2 SKILL\IDBI MSME\Project AAROHAN-AWS\apps\customer-portal\src\pages"

for fname in sorted(os.listdir(pages_dir)):
    if not fname.endswith('.tsx'):
        continue
    path = os.path.join(pages_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_fetch = 'await fetch(' in content
    has_mock = bool(re.search(r'Mock|mock|fallback|Fallback', content))
    has_throw = 'throw new Error' in content
    has_api_url = 'apiUrl' in content
    has_localhost = 'localhost' in content
    has_catch = '} catch' in content
    
    # Count fetch calls
    fetch_count = content.count('await fetch(')
    
    # Check for "if (res.ok)" without throw (the broken pattern)
    broken_pattern = len(re.findall(r'if\s*\(\w+\.ok\)\s+set', content))
    
    # Check for the fixed pattern "if (!res.ok) throw"  
    fixed_pattern = len(re.findall(r'if\s*\(!\w+\.ok\)\s+throw', content))
    
    status = "OK" if (not has_fetch or (has_mock and not has_localhost)) else "NEEDS FIX"
    if has_localhost:
        status = "HAS LOCALHOST"
    if broken_pattern > 0:
        status = f"BROKEN ({broken_pattern} unfixed)"
        
    print(f"{fname:40s} fetch={fetch_count:2d}  mock={has_mock!s:5s}  throw={has_throw!s:5s}  apiUrl={has_api_url!s:5s}  localhost={has_localhost!s:5s}  broken={broken_pattern}  fixed={fixed_pattern}  => {status}")
