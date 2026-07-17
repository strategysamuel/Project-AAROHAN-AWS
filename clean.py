import glob, re
for p in glob.glob('d:/SAMUEL/HACK 2 SKILL/IDBI MSME/Project AAROHAN-AWS/services/*/app/models.py'):
    with open(p, 'r') as f: content = f.read()
    new_content = content.replace("{\\'extend_existing\\': True}", "")
    new_content = new_content.replace("__table_args__ = \n", "")
    new_content = new_content.replace("    __table_args__ = ", "")
    with open(p, 'w') as f: f.write(new_content)
