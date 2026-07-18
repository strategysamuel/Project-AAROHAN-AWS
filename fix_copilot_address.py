import json
import os

WORKSPACE_ROOT = r"d:\SAMUEL\HACK 2 SKILL\IDBI MSME\Project AAROHAN-AWS"

# 1. Update AiBankingCopilotPanel.tsx
panel_file = os.path.join(WORKSPACE_ROOT, "apps", "customer-portal", "src", "components", "AiBankingCopilotPanel.tsx")
with open(panel_file, "r", encoding="utf-8") as f:
    panel_content = f.read()

# Remove history load
panel_content = panel_content.replace(
    "if (Array.isArray(parsed) && parsed.length > 0) {\n          setMessages(parsed.slice(-20));\n        }",
    "// Empty history for every new session as requested\n        // setMessages(parsed.slice(-20));"
)

with open(panel_file, "w", encoding="utf-8") as f:
    f.write(panel_content)

# 2. Update SCN-001_priya_textile_works.json
priya_file = os.path.join(WORKSPACE_ROOT, "ese", "personas", "SCN-001_priya_textile_works.json")
with open(priya_file, "r", encoding="utf-8") as f:
    priya_data = json.load(f)

priya_data["address_line1"] = "123 Textile Market"
priya_data["state"] = "Gujarat"
priya_data["pincode"] = "395002"
priya_data["district"] = "Surat"

with open(priya_file, "w", encoding="utf-8") as f:
    json.dump(priya_data, f, indent=2)

# 3. Update main.py to read these new fields
main_py_file = os.path.join(WORKSPACE_ROOT, "services", "onboarding-service", "app", "main.py")
with open(main_py_file, "r", encoding="utf-8") as f:
    main_py_content = f.read()

main_py_content = main_py_content.replace(
    '"district": persona.get("district", ""),',
    '"district": persona.get("district", ""),\n                        "address_line1": persona.get("address_line1", ""),\n                        "state": persona.get("state", ""),\n                        "pincode": persona.get("pincode", ""),',
    1
)

with open(main_py_file, "w", encoding="utf-8") as f:
    f.write(main_py_content)

# 4. Update seed_master_sqlite.py to insert address
seed_file = os.path.join(WORKSPACE_ROOT, "seed_master_sqlite.py")
with open(seed_file, "r", encoding="utf-8") as f:
    seed_content = f.read()

address_insert = """
    print("\\n--- 1.5 Seeding Address ---")
    cursor.execute(\"\"\"
        INSERT OR REPLACE INTO onboarding_addresses (customer_id, address_line1, state, pincode, address_type)
        VALUES (?, ?, ?, ?, ?)
    \"\"\", (customer_id, "123 Textile Market", "Gujarat", "395002", "OFFICE"))
    print("✅ Address Seeded")
"""

if "--- 1.5 Seeding Address ---" not in seed_content:
    seed_content = seed_content.replace(
        'print(f"✅ Created Customer! ID: {customer_id} | PAN: {pan}")',
        f'print(f"✅ Created Customer! ID: {{customer_id}} | PAN: {{pan}}")\n{address_insert}'
    )

with open(seed_file, "w", encoding="utf-8") as f:
    f.write(seed_content)

print("Updates completed successfully.")
