import sqlite3
import os

db_path = "aarohan_local.db"
db_path = "/app/data/aarohan_local.db" if os.path.exists("/app/data") else "aarohan_local.db"

def seed_data():
    print("====================================================")
    print("PHASE 4: MASTER SEED ORCHESTRATOR (DYNAMIC IDs)")
    print("====================================================")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    def ensure_column(table, column, col_type="VARCHAR"):
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError:
            pass
            
    # Fix schemas created by duplicate models in microservices
    for col in ["aadhaar_masked", "district", "persona_name"]:
        ensure_column("onboarding_customers", col)
    for col in ["is_active", "is_deleted"]:
        ensure_column("onboarding_customers", col, "BOOLEAN")
    for col in ["email", "pan", "workflow_id"]:
        ensure_column("onboarding_customers", col)
    for col in ["created_at", "updated_at"]:
        ensure_column("onboarding_customers", col, "DATETIME")
        
    for col in ["address_line2", "city", "state", "pincode", "address_type"]:
        ensure_column("onboarding_addresses", col)

    for col in ["legal_name", "registration_date", "business_constitution", "trade_name", "filing_frequency"]:
        ensure_column("gst_profiles", col)

    for col in ["full_name", "dob", "pan", "aadhaar_masked", "address", "mobile", "email"]:
        ensure_column("ckyc_records", col)

    for col in ["account_ref_num", "masked_acc_num", "bank_name", "account_type"]:
        ensure_column("aa_linked_accounts", col)
    ensure_column("aa_linked_accounts", "balance", "FLOAT")
    ensure_column("aa_linked_accounts", "is_active", "BOOLEAN")

    for col in ["establishment_id", "establishment_name", "status"]:
        ensure_column("epfo_profiles", col)
    ensure_column("epfo_profiles", "average_monthly_payroll", "FLOAT")

    for col in ["cin", "company_name", "incorporation_date", "company_status", "class_of_company", "registered_office", "roc"]:
        ensure_column("mca_company_profiles", col)
    for col in ["authorized_capital", "paid_up_capital"]:
        ensure_column("mca_company_profiles", col, "FLOAT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fhc_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER UNIQUE,
            overall_score FLOAT,
            rating VARCHAR,
            cash_flow_score FLOAT,
            compliance_score FLOAT,
            business_stability_score FLOAT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_credit_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER UNIQUE,
            confidence_score FLOAT,
            recommendation VARCHAR,
            eligible_loan_amount FLOAT,
            recommended_interest_rate FLOAT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cam_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER UNIQUE,
            cam_reference VARCHAR,
            status VARCHAR,
            recommended_loan_amount FLOAT,
            recommended_interest_rate FLOAT,
            recommended_tenure_months INTEGER,
            section_executive_summary TEXT,
            section_applicant_profile TEXT,
            section_business_profile TEXT,
            section_loan_requirement TEXT,
            section_identity_verification TEXT,
            section_gst_compliance TEXT,
            section_banking_behaviour TEXT,
            section_workforce_stability TEXT,
            section_corporate_governance TEXT,
            section_fhc_summary TEXT,
            section_credit_decision TEXT,
            section_fraud_screening TEXT,
            section_ocen_marketplace TEXT,
            section_recommended_offer TEXT,
            section_key_risks TEXT,
            section_risk_mitigation TEXT,
            section_banker_recommendation TEXT,
            section_approval_matrix TEXT
        )
    """)
    
    for col in ["overall_score", "rating"]:
        ensure_column("fhc_cards", col)
    for col in ["cash_flow_score", "compliance_score", "business_stability_score"]:
        ensure_column("fhc_cards", col, "FLOAT")

    ensure_column("ai_credit_decisions", "recommendation")
    for col in ["confidence_score", "eligible_loan_amount", "recommended_interest_rate"]:
        ensure_column("ai_credit_decisions", col, "FLOAT")

    for table in ["gst_profiles", "ckyc_records", "aa_linked_accounts", "epfo_profiles", "mca_company_profiles", "fhc_cards", "ai_credit_decisions", "cam_records"]:
        ensure_column(table, "last_synced_at", "DATETIME")
        
    # Disable foreign keys temporarily
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    print("\n--- 1. Creating Customer ---")
    cursor.execute("""
        INSERT OR REPLACE INTO onboarding_customers 
        (id, legal_name, mobile_number, email, pan, aadhaar_masked, district, persona_name, onboarding_status, is_active, is_deleted)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (99, "Priya Textile Works", "9876543210", "priya@textileworks.in", "PRXPT0001K", "XXXXXXXX1234", "Surat", "Priya Textile Works", "SUBMITTED", 1, 0))
    
    cursor.execute("UPDATE onboarding_customers SET created_at = '2023-01-01 00:00:00', updated_at = '2023-01-01 00:00:00' WHERE id = 99")
    
    customer_id = 99
    pan = "PRXPT0001K"
    print(f"✅ Created Customer! ID: {customer_id} | PAN: {pan}")

    print("\n--- 1.5 Seeding Address ---")
    cursor.execute("""
        INSERT OR REPLACE INTO onboarding_addresses (customer_id, address_line1, state, pincode, address_type)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, "123 Textile Market", "Gujarat", "395002", "OFFICE"))
    print("✅ Address Seeded")


    print("\n--- 2. Seeding GST ---")
    cursor.execute("""
        INSERT OR REPLACE INTO gst_profiles (customer_id, gstin, legal_name, registration_date, status, business_constitution)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, "27SIMPT0001K1Z5", "Priya Textile Works", "2015-05-20", "Active", "Regular"))
    print("✅ GST Synced")

    print("\n--- 3. Seeding CKYC ---")
    cursor.execute("""
        INSERT OR REPLACE INTO ckyc_records (customer_id, ckyc_number, full_name, dob, pan, aadhaar_masked, address, mobile, email, kyc_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer_id, "30049281726355", "Priya Textile Works", "12-08-1988", pan, "XXXXXXXX1234", "123 Demo St", "9876543210", "priya@textileworks.in", "CLEAN"))
    print("✅ CKYC Seeded")

    print("\n--- 4. Seeding Account Aggregator ---")
    cursor.execute("""
        INSERT OR REPLACE INTO aa_linked_accounts (customer_id, account_ref_num, masked_acc_num, bank_name, account_type, balance, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (customer_id, "REF123456", "XXXX-XXXX-1234", "HDFC Bank", "CURRENT", 250000.00, 1))
    print("✅ AA Linked")

    print("\n--- 5. Seeding EPFO ---")
    cursor.execute("""
        INSERT OR REPLACE INTO epfo_profiles (customer_id, establishment_id, establishment_name, status, number_of_employees, average_monthly_payroll)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, "MHBAN0000012000", "Priya Textile Works", "ACTIVE", 87, 1500000.0))
    print("✅ EPFO Synced")

    print("\n--- 6. Seeding MCA ---")
    cursor.execute("""
        INSERT OR REPLACE INTO mca_company_profiles (customer_id, cin, company_name, incorporation_date, company_status, class_of_company, authorized_capital, paid_up_capital, registered_office, roc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer_id, "U12345MH2020P123456", "Priya Textile Works Pvt Ltd", "2012-05-15", "Active", "Private", 1000000.0, 500000.0, "Mumbai", "RoC-Mumbai"))
    print("✅ MCA Synced")

    print("\n--- 7. Generating Financial Health Card ---")
    cursor.execute("""
        INSERT OR REPLACE INTO fhc_cards (customer_id, overall_score, rating, cash_flow_score, compliance_score, business_stability_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, 85.5, "Excellent", 88.0, 92.0, 80.0))
    print("✅ Financial Health Card Generated")

    print("\n--- 8. Credit Decision ---")
    cursor.execute("""
        INSERT OR REPLACE INTO ai_credit_decisions (customer_id, confidence_score, recommendation, eligible_loan_amount, recommended_interest_rate)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, 91.0, "APPROVED", 5000000.0, 10.5))
    print("✅ Credit Evaluated")

    print("\n--- 9. CAM Service ---")
    cursor.execute("""
        INSERT OR REPLACE INTO cam_records (
            customer_id, cam_reference, status, recommended_loan_amount, recommended_interest_rate, recommended_tenure_months,
            section_executive_summary, section_applicant_profile, section_business_profile, section_loan_requirement,
            section_identity_verification, section_gst_compliance, section_banking_behaviour, section_workforce_stability,
            section_corporate_governance, section_fhc_summary, section_credit_decision, section_fraud_screening,
            section_ocen_marketplace, section_recommended_offer, section_key_risks, section_risk_mitigation,
            section_banker_recommendation, section_approval_matrix
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer_id, "CAM-DEMO-001", "APPROVED", 5000000.0, 10.5, 36,
          "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))
    print("✅ CAM Generated")
    
    # Fix last_synced_at defaults
    for table in ["gst_profiles", "ckyc_records", "aa_linked_accounts", "epfo_profiles", "mca_company_profiles", "fhc_cards", "ai_credit_decisions", "cam_records"]:
        cursor.execute(f"UPDATE {table} SET last_synced_at = '2023-01-01 00:00:00'")
    
    cursor.execute("UPDATE gst_profiles SET filing_frequency = 'Monthly'")
        
    conn.commit()
    conn.close()
    print("\n[SUCCESS] Master Seeding Completed using Dynamic IDs via SQLite.")

if __name__ == "__main__":
    seed_data()
