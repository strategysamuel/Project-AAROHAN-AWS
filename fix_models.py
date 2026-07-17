import glob, re
for p in glob.glob('d:/SAMUEL/HACK 2 SKILL/IDBI MSME/Project AAROHAN-AWS/services/*/app/models.py'):
    with open(p, 'r') as f: content = f.read()
    new_content = re.sub(r"(__tablename__\s*=\s*['\"].*['\"])", r"\1\n    __table_args__ = {'extend_existing': True}", content)
    if new_content != content:
        with open(p, 'w') as f: f.write(new_content)
