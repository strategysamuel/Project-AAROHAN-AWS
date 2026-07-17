import os

scripts = [
    "start-identity-platform.sh",
    "start-lending-intelligence.sh",
    "start-executive-intelligence.sh"
]

for s in scripts:
    if os.path.exists(s):
        with open(s, "r") as f:
            content = f.read()
        
        # Replace PYTHONPATH="... with PYTHONPATH="/app:...
        content = content.replace('PYTHONPATH="', 'PYTHONPATH="/app:')
        
        with open(s, "w") as f:
            f.write(content)

print("Updated PYTHONPATH in shell scripts")
