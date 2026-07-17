# AAR-DATABASE-SCHEMA

## aa-service
- Tables: aa_linked_accounts, aa_transactions, aa_analytics, aa_consents
- Primary Keys: id, id, id, id
- Foreign Keys: account_id -> aa_linked_accounts.id

## auth-service
- Tables: permissions, roles, users, refresh_tokens
- Primary Keys: id, id, id, id
- Foreign Keys: role_id -> roles.id

## cam-service
- Tables: cam_records, cam_versions, cam_approvals, cam_templates, cam_config
- Primary Keys: id, id, id, id, id
- Foreign Keys: cam_id -> cam_records.id, cam_id -> cam_records.id

## ckyc-service
- Tables: ckyc_records, ckyc_verification_logs, onboarding_customers, onboarding_addresses
- Primary Keys: id, id, id, id
- Foreign Keys: 

## consent-service
- Tables: consent_purposes, consents, consent_artifacts
- Primary Keys: id, id, id
- Foreign Keys: consent_id -> consents.id

## credit-engine
- Tables: ai_credit_decisions, human_approval_logs, credit_engine_config, fhc_cards, onboarding_customers, onboarding_businesses, ckyc_records, ckyc_verification_logs, gst_analytics, aa_analytics, epfo_analytics, mca_company_profiles, mca_governance_analytics
- Primary Keys: id, id, id, id, id, id, id, id, id, id, id, id, id
- Foreign Keys: decision_id -> ai_credit_decisions.id

## document-service
- Tables: documents, document_metadata
- Primary Keys: id, id
- Foreign Keys: document_id -> documents.id

## epfo-service
- Tables: epfo_profiles, epfo_contributions, epfo_employees, epfo_analytics
- Primary Keys: id, id, id, id
- Foreign Keys: profile_id -> epfo_profiles.id, profile_id -> epfo_profiles.id, profile_id -> epfo_profiles.id

## ews-service
- Tables: ews_watchlist, ews_alerts, ews_risk_cases
- Primary Keys: id, id, id
- Foreign Keys: 

## exec-service
- Tables: exec_kpis, exec_branch_performance
- Primary Keys: id, id
- Foreign Keys: 

## fhc-service
- Tables: fhc_cards, fhc_score_history, fhc_config, onboarding_customers, onboarding_businesses, ckyc_records, ckyc_verification_logs, gst_profiles, gst_analytics, aa_analytics, epfo_profiles, epfo_analytics, mca_company_profiles, mca_governance_analytics, mca_directors, mca_charges
- Primary Keys: id, id, id, id, id, id, id, id, id, id, id, id, id, id, id, id
- Foreign Keys: card_id -> fhc_cards.id

## gst-service
- Tables: gst_profiles, gst_returns, gst_analytics
- Primary Keys: id, id, id
- Foreign Keys: profile_id -> gst_profiles.id, profile_id -> gst_profiles.id

## mca-service
- Tables: mca_company_profiles, mca_directors, mca_charges, mca_company_filings, mca_financial_statements, mca_governance_analytics
- Primary Keys: id, id, id, id, id, id
- Foreign Keys: company_id -> mca_company_profiles.id, company_id -> mca_company_profiles.id, company_id -> mca_company_profiles.id, company_id -> mca_company_profiles.id, company_id -> mca_company_profiles.id

## ocen-uli-service
- Tables: ocen_lenders, ocen_loan_products, ocen_partners, ocen_loan_applications, ocen_loan_offers, ocen_marketplace_matches, ocen_marketplace_config, ocen_audit_logs
- Primary Keys: id, id, id, id, id, id, id, id
- Foreign Keys: application_id -> ocen_loan_applications.id, application_id -> ocen_loan_applications.id

## onboarding-service
- Tables: onboarding_customers, onboarding_businesses, onboarding_directors, onboarding_addresses, onboarding_documents
- Primary Keys: id, id, id, id, id
- Foreign Keys: customer_id -> onboarding_customers.id, business_id -> onboarding_businesses.id, customer_id -> onboarding_customers.id, customer_id -> onboarding_customers.id

## portfolio-service
- Tables: portfolio_simulations
- Primary Keys: id
- Foreign Keys: 

## rbi-fraud-service
- Tables: rbi_fraud_records, rbi_fraud_watchlist, rbi_fraud_config, onboarding_customers, onboarding_businesses, ckyc_verification_logs, aa_analytics, mca_governance_analytics
- Primary Keys: id, id, id, id, id, id, id, id
- Foreign Keys: 

## rm-workspace-service
- Tables: rm_tasks, rm_leads, rm_alerts, rm_interactions
- Primary Keys: id, id, id, id
- Foreign Keys: 

## treds-service
- Tables: treds_buyers, treds_invoices
- Primary Keys: id, id
- Foreign Keys: 

## Duplicated Customer Tables
- ckyc-service.onboarding_customers
- credit-engine.onboarding_customers
- credit-engine.onboarding_businesses
- credit-engine.mca_company_profiles
- epfo-service.epfo_profiles
- fhc-service.onboarding_customers
- fhc-service.onboarding_businesses
- fhc-service.gst_profiles
- fhc-service.epfo_profiles
- fhc-service.mca_company_profiles
- gst-service.gst_profiles
- mca-service.mca_company_profiles
- onboarding-service.onboarding_customers
- onboarding-service.onboarding_businesses
- rbi-fraud-service.onboarding_customers
- rbi-fraud-service.onboarding_businesses

## Isolated Datasets
All services previously had isolated SQLite DBs. With Phase 2, they all share `aarohan_local.db` but they still use duplicated tables (e.g., `ckyc_records`, `gst_profiles`) representing the same logical entity without a central unified `customer` table enforcing foreign keys globally.

## Broken Relationships
Because there is no central `customers` table that `ckyc_records.customer_id` or `gst_profiles.customer_id` strictly references via a database constraint across all microservices, the relationship is logical. If `customer_id` does not match exactly across these tables, the dashboard breaks. This is identified as a broken relationship.
