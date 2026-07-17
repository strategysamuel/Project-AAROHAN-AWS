# AAR-DATABASE-AUDIT

## aa-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: aa_linked_accounts, aa_transactions, aa_analytics, aa_consents
- Seed Scripts: 
- Health Endpoint: Yes

## auth-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: permissions, roles, users, refresh_tokens
- Seed Scripts: main.py
- Health Endpoint: Yes

## cam-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: cam_records, cam_versions, cam_approvals, cam_templates, cam_config
- Seed Scripts: 
- Health Endpoint: Yes

## ckyc-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: ckyc_records, ckyc_verification_logs, onboarding_customers, onboarding_addresses
- Seed Scripts: 
- Health Endpoint: Yes

## consent-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: consent_purposes, consents, consent_artifacts
- Seed Scripts: 
- Health Endpoint: Yes

## credit-engine
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: ai_credit_decisions, human_approval_logs, credit_engine_config, fhc_cards, onboarding_customers, onboarding_businesses, ckyc_records, ckyc_verification_logs, gst_analytics, aa_analytics, epfo_analytics, mca_company_profiles, mca_governance_analytics
- Seed Scripts: 
- Health Endpoint: Yes

## document-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: documents, document_metadata
- Seed Scripts: main.py
- Health Endpoint: Yes

## epfo-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: epfo_profiles, epfo_contributions, epfo_employees, epfo_analytics
- Seed Scripts: 
- Health Endpoint: Yes

## ese-admin-service
- database.py: Yes
- DATABASE_URL: Unknown
- SQLAlchemy Engine: No
- SessionLocal: No
- Base: No
- ORM Models: 
- Seed Scripts: main.py
- Health Endpoint: Yes

## ews-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: ews_watchlist, ews_alerts, ews_risk_cases
- Seed Scripts: 
- Health Endpoint: Yes

## exec-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: exec_kpis, exec_branch_performance
- Seed Scripts: 
- Health Endpoint: Yes

## fhc-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: fhc_cards, fhc_score_history, fhc_config, onboarding_customers, onboarding_businesses, ckyc_records, ckyc_verification_logs, gst_profiles, gst_analytics, aa_analytics, epfo_profiles, epfo_analytics, mca_company_profiles, mca_governance_analytics, mca_directors, mca_charges
- Seed Scripts: 
- Health Endpoint: Yes

## gst-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: gst_profiles, gst_returns, gst_analytics
- Seed Scripts: 
- Health Endpoint: Yes

## mca-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: mca_company_profiles, mca_directors, mca_charges, mca_company_filings, mca_financial_statements, mca_governance_analytics
- Seed Scripts: 
- Health Endpoint: Yes

## ocen-uli-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: ocen_lenders, ocen_loan_products, ocen_partners, ocen_loan_applications, ocen_loan_offers, ocen_marketplace_matches, ocen_marketplace_config, ocen_audit_logs
- Seed Scripts: main.py
- Health Endpoint: Yes

## onboarding-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: onboarding_customers, onboarding_businesses, onboarding_directors, onboarding_addresses, onboarding_documents
- Seed Scripts: 
- Health Endpoint: Yes

## portfolio-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: portfolio_simulations
- Seed Scripts: 
- Health Endpoint: Yes

## rbi-fraud-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: rbi_fraud_records, rbi_fraud_watchlist, rbi_fraud_config, onboarding_customers, onboarding_businesses, ckyc_verification_logs, aa_analytics, mca_governance_analytics
- Seed Scripts: main.py
- Health Endpoint: Yes

## rm-workspace-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: rm_tasks, rm_leads, rm_alerts, rm_interactions
- Seed Scripts: 
- Health Endpoint: Yes

## treds-service
- database.py: Yes
- DATABASE_URL: import os
- SQLAlchemy Engine: Yes
- SessionLocal: Yes
- Base: Yes
- ORM Models: treds_buyers, treds_invoices
- Seed Scripts: 
- Health Endpoint: Yes

