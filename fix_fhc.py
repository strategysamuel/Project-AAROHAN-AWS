import sqlite3

conn = sqlite3.connect('/app/data/aarohan_local.db')
c = conn.cursor()

# Create fhc_score_history table
c.execute('''
CREATE TABLE IF NOT EXISTS fhc_score_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INTEGER,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    score_value FLOAT,
    rating VARCHAR(50),
    FOREIGN KEY(card_id) REFERENCES fhc_cards(id)
)
''')

# Update null columns in fhc_cards to defaults
columns_to_zero = [
    'identity_trust_score', 'business_compliance_score', 'gst_health_score',
    'banking_behaviour_dim_score', 'cash_flow_stability_score', 'liquidity_dim_score',
    'revenue_growth_score', 'working_capital_score', 'profitability_score',
    'payroll_stability_score', 'corporate_governance_score', 'operational_stability_score',
    'business_continuity_score', 'digital_adoption_score', 'overall_financial_strength_score',
    'identity_score', 'identity_weight', 'compliance_score', 'compliance_weight',
    'liquidity_score', 'liquidity_weight', 'revenue_score', 'revenue_weight',
    'cash_flow_score', 'cash_flow_weight', 'business_stability_score', 'business_stability_weight',
    'governance_score', 'governance_weight', 'workforce_score', 'workforce_weight',
    'banking_behaviour_score', 'banking_behaviour_weight', 'growth_score', 'growth_weight'
]

for col in columns_to_zero:
    try:
        c.execute(f"UPDATE fhc_cards SET {col} = 0.0 WHERE {col} IS NULL")
    except sqlite3.OperationalError:
        pass

c.execute("UPDATE fhc_cards SET is_overridden = 0 WHERE is_overridden IS NULL")
c.execute("UPDATE fhc_cards SET created_at = '2023-01-01 00:00:00' WHERE created_at IS NULL")
c.execute("UPDATE fhc_cards SET updated_at = '2023-01-01 00:00:00' WHERE updated_at IS NULL")

# Insert a dummy history
c.execute("INSERT INTO fhc_score_history (card_id, score_value, rating) VALUES (1, 85.0, 'Excellent')")

conn.commit()
conn.close()
print("FHC fixed!")
