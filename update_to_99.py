import sqlite3

db = sqlite3.connect('aarohan_local.db')
c = db.cursor()
c.execute("SELECT id FROM onboarding_customers WHERE pan='PRXPT0001K'")
rows = c.fetchall()
for row in rows:
    old_id = row[0]
    if old_id == 99:
        continue
    print("Found old ID:", old_id)
    tables = [
        "onboarding_customers",
        "onboarding_addresses",
        "onboarding_businesses",
        "onboarding_directors",
        "gst_profiles",
        "gst_returns",
        "gst_invoices",
        "ckyc_records",
        "ckyc_verification_logs",
        "aa_linked_accounts",
        "aa_transactions",
        "epfo_profiles",
        "epfo_remittances",
        "mca_company_profiles",
        "mca_directors",
        "mca_charges",
        "fhc_cards",
        "fhc_metrics",
        "fhc_recommendations",
        "credit_decisions",
        "credit_reasons",
        "cam_records",
        "cam_financials",
        "cam_covenants",
        "exec_kpis",
        "exec_alerts"
    ]
    for t in tables:
        try:
            if t == "onboarding_customers":
                c.execute(f"UPDATE {t} SET id=99 WHERE id=?", (old_id,))
            else:
                c.execute(f"UPDATE {t} SET customer_id=99 WHERE customer_id=?", (old_id,))
            print(f"Updated {t}")
        except Exception as e:
            print(f"Error on {t}: {e}")

db.commit()
print("Done updating to 99")
