import os
import re

pages_dir = r"d:\SAMUEL\HACK 2 SKILL\IDBI MSME\Project AAROHAN-AWS\apps\customer-portal\src\pages"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find patterns like:
    # if (res.ok) setStats(await res.json());
    # and change them to:
    # if (!res.ok) throw new Error(); setStats(await res.json());
    
    modified = content
    
    # Simple one-liners:
    # if (res.ok) setConsents(await res.json()); -> if (!res.ok) throw new Error(); setConsents(await res.json());
    modified = re.sub(r'if\s*\((.*?)\.ok\)\s*(set.*?\(.*?\));', r'if (!\1.ok) throw new Error(); \2;', modified)
    
    # Block ones:
    # if (res.ok) {
    #   const record = await res.json();
    # ...
    # } else {
    #   setError(...);
    # }
    
    # Let's do manual replacement for the block ones or let the script just add the throw
    # If the file has "else {\n        setError", we can replace the else block with throw new Error.
    modified = re.sub(r'\} else \{\s*setError\(.*?\);\s*\}', r'} else { throw new Error(); }', modified)
    
    if modified != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Fixed {os.path.basename(filepath)}")

for filename in os.listdir(pages_dir):
    if filename.endswith(".tsx"):
        fix_file(os.path.join(pages_dir, filename))
