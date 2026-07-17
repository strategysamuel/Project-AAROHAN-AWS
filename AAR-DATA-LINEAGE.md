# AAR-DATA-LINEAGE

## Core Business Entities

1. **Customer** (`onboarding_customers`)
   - Seed Source: `onboarding-service`
   - Reports: Exec Dashboard (Total applications)
2. **GST** (`gst_profiles`)
   - Seed Source: `gst-service`
   - Reports: GST Consistency (AI Engine)
3. **CKYC** (`ckyc_records`)
   - Seed Source: `ckyc-service`
   - Reports: KYC compliance
4. **Account Aggregator** (`aa_linked_accounts`)
   - Seed Source: `aa-service`
   - Reports: Cash Flow Score (FHC)
5. **EPFO** (`epfo_profiles`)
   - Seed Source: `epfo-service`
   - Reports: Business Stability Score
6. **MCA** (`mca_company_profiles`)
   - Seed Source: `mca-service`
   - Reports: Governance
7. **Credit** (`ai_credit_decisions`)
   - Seed Source: `credit-engine`
   - Reports: Approval metrics
8. **CAM** (`cam_records`)
   - Seed Source: `cam-service`
   - Reports: Loan value

## Dependency Graph

Customer
↓
GST
↓
CKYC
↓
AA
↓
EPFO
↓
MCA
↓
Credit
↓
CAM
↓
Executive
↓
Reports

## Referential Integrity

- All downstream tables successfully use `customer_id` referencing `onboarding_customers.id`.
