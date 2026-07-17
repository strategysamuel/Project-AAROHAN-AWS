import random
import time
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_helper import Base, get_active_dataset_path
from models import (
    ESECustomer, ESEBusiness, ESEGSTRecord, ESETransaction,
    ESECKYCRecord, ESEEPFORecord, ESEMCARecord, ESELoanApplication
)

logger = logging.getLogger("ese-core")

class DatasetGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.random = random.Random(seed)
        
    def generate(self, profile_size: str = "tiny") -> dict:
        """
        Generates simulated dataset and saves it to SQLite banking.db.
        """
        start_time = time.time()
        
        # Determine customer count based on profile size
        counts = {
            "tiny": 25,
            "small": 100,
            "medium": 500,
            "large": 1000,
            "enterprise": 10000
        }
        num_customers = counts.get(profile_size.lower(), 25)
        
        db_path = get_active_dataset_path()
        logger.info(f"Generating simulated dataset size: {profile_size} ({num_customers} customers) at {db_path}")
        
        from services.shared.database import SessionLocal, engine
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        
        try:
            # Seed structures
            states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat", "Delhi"]
            districts = {
                "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
                "Karnataka": ["Bangalore", "Mysore", "Hubli"],
                "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
                "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
                "Delhi": ["New Delhi", "North Delhi", "South Delhi"]
            }
            sectors = ["Manufacturing", "Services", "Retail", "Agriculture", "Logistics"]
            scenarios = [
                "Healthy Business", "High Growth", "Seasonal Business", "Cash Flow Stress",
                "GST Default", "EPFO Default", "RBI Blacklisted", "Startup", "Exporter"
            ]
            personas = ["MSME Retailer", "Manufacturing Exporter", "Service Provider", "Tech Startup"]
            
            customers = []
            businesses = []
            gst_records = []
            transactions = []
            ckyc_records = []
            epfo_records = []
            mca_records = []
            loans = []
            
            for i in range(1, num_customers + 1):
                # 1. Customer
                state = self.random.choice(states)
                district = self.random.choice(districts[state])
                pan = f"ABCDE{self.random.randint(1000, 9999)}F"
                mobile = f"9{self.random.randint(100000000, 999999999)}"
                legal_name = f"Customer {i} PVT LTD"
                persona = self.random.choice(personas)
                scenario = self.random.choice(scenarios)
                
                cust = ESECustomer(
                    id=i,
                    pan=pan,
                    legal_name=legal_name,
                    mobile_number=mobile,
                    email=f"contact@customer{i}.com",
                    persona_name=persona,
                    scenario_id=scenario
                )
                customers.append(cust)
                
                # 2. Business details
                gstin = f"27{pan}{self.random.randint(1, 9)}Z{self.random.randint(1, 9)}"
                cin = f"U{self.random.randint(10000, 99999)}MH{self.random.randint(2000, 2026)}PTC{self.random.randint(100000, 999999)}"
                turnover = float(self.random.randint(10, 1000) * 100000) # 10L to 10Cr
                biz = ESEBusiness(
                    id=i,
                    customer_id=i,
                    trade_name=f"Trade Name {i}",
                    gstin=gstin,
                    cin=cin,
                    annual_turnover=turnover,
                    industry_segment=self.random.choice(sectors)
                )
                businesses.append(biz)
                
                # 3. CKYC
                kyc_status = "CLEAN"
                if scenario == "RBI Blacklisted":
                    kyc_status = "INCOMPLETE"
                ckyc = ESECKYCRecord(
                    id=i,
                    customer_id=i,
                    pan=pan,
                    ckyc_number=f"CKYC{self.random.randint(1000000000, 9999999999)}",
                    full_name=legal_name,
                    dob="1985-05-15",
                    kyc_status=kyc_status
                )
                ckyc_records.append(ckyc)
                
                # 4. GST
                for month in ["2026-01", "2026-02", "2026-03"]:
                    status = "FILED"
                    if scenario == "GST Default" and month == "2026-03":
                        status = "PENDING"
                    gst = ESEGSTRecord(
                        customer_id=i,
                        gstin=gstin,
                        filing_month=month,
                        revenue=turnover / 12.0,
                        gst_paid=(turnover / 12.0) * 0.18,
                        filing_status=status
                    )
                    gst_records.append(gst)
                    
                # 5. EPFO Compliance
                emp_count = self.random.randint(5, 100)
                pf_score = 95.0
                if scenario == "EPFO Default":
                    pf_score = 45.0
                epfo = ESEEPFORecord(
                    id=i,
                    customer_id=i,
                    establishment_id=f"EST{self.random.randint(10000000, 99999999)}",
                    employee_count=emp_count,
                    pf_compliance_score=pf_score,
                    last_month_contribution=float(emp_count * 1500)
                )
                epfo_records.append(epfo)
                
                # 6. MCA Records
                mca_status = "ACTIVE"
                if scenario == "RBI Blacklisted":
                    mca_status = "INACTIVE"
                mca = ESEMCARecord(
                    id=i,
                    customer_id=i,
                    cin=cin,
                    company_name=legal_name,
                    date_of_incorporation="2015-08-20",
                    status=mca_status
                )
                mca_records.append(mca)
                
                # 7. Transactions
                balance = 500000.0
                for tx_id in range(1, 11):
                    tx_type = self.random.choice(["CREDIT", "DEBIT"])
                    amount = float(self.random.randint(1000, 50000))
                    if tx_type == "CREDIT":
                        balance += amount
                    else:
                        balance -= amount
                    tx = ESETransaction(
                        customer_id=i,
                        account_ref_num=f"ACC{i}0001",
                        transaction_date=f"2026-03-{tx_id:02d}",
                        amount=amount,
                        type=tx_type,
                        balance=balance,
                        description=f"Transaction Ref {tx_id}"
                    )
                    transactions.append(tx)
                    
                # 8. Loan application
                loan = ESELoanApplication(
                    id=i,
                    customer_id=i,
                    requested_amount=turnover * 0.2,
                    tenure_months=12,
                    status="DISBURSED" if scenario == "Healthy Business" else "ACCEPTED",
                    interest_rate=11.5
                )
                loans.append(loan)
                
            # Insert everything in bulk
            db.add_all(customers)
            db.add_all(businesses)
            db.add_all(ckyc_records)
            db.add_all(gst_records)
            db.add_all(epfo_records)
            db.add_all(mca_records)
            db.add_all(transactions)
            db.add_all(loans)
            db.commit()
            
            duration = time.time() - start_time
            logger.info(f"Generated {num_customers} customer trees in {duration:.2f} seconds.")
            return {
                "status": "success",
                "profile": profile_size,
                "customers": len(customers),
                "businesses": len(businesses),
                "transactions": len(transactions),
                "duration_seconds": duration
            }
        except Exception as e:
            logger.error(f"Error during simulation generation: {str(e)}")
            db.rollback()
            raise e
        finally:
            db.close()
