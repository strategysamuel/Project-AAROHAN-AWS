import abc
import datetime
import uuid
import os
from typing import List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class AAAdapter(abc.ABC):
    @abc.abstractmethod
    def discover_financial_accounts(self, customer_mobile: str) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def fetch_transaction_ledger(self, account_ref_num: str) -> List[Dict[str, Any]]:
        pass

class SimulationAAAdapter(AAAdapter):
    def discover_financial_accounts(self, customer_mobile: str) -> List[Dict[str, Any]]:
        from app.database import SessionLocal
        db = SessionLocal()
        accounts = []
        try:
            # Query ESE customers/businesses to find customer mapping by mobile
            cust_row = db.execute(
                "SELECT id, legal_name FROM onboarding_customers WHERE mobile_number = :mobile",
                {"mobile": customer_mobile}
            ).fetchone()
            if cust_row:
                cust_id = cust_row[0]
                
                # Check if there are transactions in ese_transactions for this customer
                # Find distinct account refs
                rows = db.execute(
                    "SELECT DISTINCT account_ref_num FROM ese_transactions WHERE customer_id = :cust_id",
                    {"cust_id": cust_id}
                ).fetchall()
                
                for idx, r in enumerate(rows):
                    acc_ref = r[0]
                    # Query last transaction to get balance
                    bal_row = db.execute(
                        "SELECT balance FROM ese_transactions WHERE customer_id = :cust_id AND account_ref_num = :acc_ref "
                        "ORDER BY id DESC LIMIT 1", {"cust_id": cust_id, "acc_ref": acc_ref}
                    ).fetchone()
                    balance = bal_row[0] if bal_row else 150000.0
                    
                    accounts.append({
                        "account_ref_num": acc_ref,
                        "masked_acc_num": f"XXXXXX{1234 + idx}",
                        "bank_name": "IDBI Bank" if idx % 2 == 0 else "State Bank of India",
                        "account_type": "CURRENT" if "curr" in acc_ref.lower() or idx % 2 == 0 else "SAVINGS",
                        "balance": float(balance),
                        "currency": "INR"
                    })
                
                if accounts:
                    return accounts
        except Exception:
            pass
        finally:
            db.close()
            
        # Fallback default active accounts
        return [
            {
                "account_ref_num": f"SBI-ACC-CURRENT",
                "masked_acc_num": "XXXXXX4321",
                "bank_name": "State Bank of India",
                "account_type": "CURRENT",
                "balance": 450000.0,
                "currency": "INR"
            },
            {
                "account_ref_num": f"IDBI-ACC-SAVINGS",
                "masked_acc_num": "XXXXXX9876",
                "bank_name": "IDBI Bank",
                "account_type": "SAVINGS",
                "balance": 125000.0,
                "currency": "INR"
            }
        ]

    def fetch_transaction_ledger(self, account_ref_num: str) -> List[Dict[str, Any]]:
        from app.database import SessionLocal
        db = SessionLocal()
        ledger = []
        try:
            # Query ese_transactions matching account_ref_num
            rows = db.execute(
                "SELECT txn_ref_num, txn_date, amount, type, description "
                "FROM (SELECT id as txn_ref_num, transaction_date as txn_date, amount, type, description "
                "FROM ese_transactions WHERE account_ref_num = :ref) "
                "ORDER BY txn_date ASC", {"ref": account_ref_num}
            ).fetchall()
            
            for r in rows:
                txn_ref = f"TXN-SIM-{r[0]}"
                txn_date_str = r[1]
                amount = r[2]
                txn_type = r[3].upper() # CREDIT, DEBIT
                narration = r[4] or "UPI / Vendor payment"
                
                # Parse date
                try:
                    txn_date = datetime.datetime.fromisoformat(txn_date_str.replace("Z", ""))
                except Exception:
                    txn_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=10)
                
                ledger.append({
                    "txn_ref_num": txn_ref,
                    "txn_date": txn_date,
                    "amount": float(amount),
                    "txn_type": txn_type,
                    "narration": narration
                })
            if ledger:
                return ledger
        except Exception:
            pass
        finally:
            db.close()
            
        # Fallback default transactions
        base_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=90)
        for i in range(12):
            # Inflow
            ledger.append({
                "txn_ref_num": f"TXN-IN-{uuid.uuid4().hex[:8].upper()}",
                "txn_date": base_date + datetime.timedelta(days=i * 7),
                "amount": 180000.0 if i % 2 == 0 else 60000.0,
                "txn_type": "CREDIT",
                "narration": "UPI CLIENT SETTLEMENT / AUTOPARTS" if i % 2 == 0 else "IMPS TRANSFER FROM CUSTOMER"
            })
            # Outflow
            ledger.append({
                "txn_ref_num": f"TXN-OUT-{uuid.uuid4().hex[:8].upper()}",
                "txn_date": base_date + datetime.timedelta(days=i * 7 + 3),
                "amount": 75000.0 if i % 2 == 0 else 30000.0,
                "txn_type": "DEBIT",
                "narration": "NEFT SUPPLIER SETTLEMENT" if i % 2 == 0 else "LOAN EMI AUTOMATIC DEBIT"
            })
        return ledger

class SandboxAAAdapter(AAAdapter):
    def discover_financial_accounts(self, customer_mobile: str) -> List[Dict[str, Any]]:
        return [
            {
                "account_ref_num": "SANDBOX-SB-01",
                "masked_acc_num": "XXXXXX1111",
                "bank_name": "Sandbox Test Bank",
                "account_type": "SAVINGS",
                "balance": 99000.0,
                "currency": "INR"
            }
        ]

    def fetch_transaction_ledger(self, account_ref_num: str) -> List[Dict[str, Any]]:
        base_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=10)
        return [
            {
                "txn_ref_num": "TXN-SAND-01",
                "txn_date": base_date,
                "amount": 10000.0,
                "txn_type": "CREDIT",
                "narration": "SANDBOX INTEREST CREDITED"
            }
        ]

class ProductionAAAdapter(AAAdapter):
    def discover_financial_accounts(self, customer_mobile: str) -> List[Dict[str, Any]]:
        return []

    def fetch_transaction_ledger(self, account_ref_num: str) -> List[Dict[str, Any]]:
        return []

# Configurable Factory Selector
def get_aa_adapter() -> AAAdapter:
    profile = os.getenv("AA_ADAPTER_PROFILE", "SIMULATION").upper()
    if profile in ("REAL", "PRODUCTION"):
        return ProductionAAAdapter()
    elif profile == "SANDBOX":
        return SandboxAAAdapter()
    else:
        return SimulationAAAdapter()

# Deprecated compatibility alias
AccountAggregatorMockProvider = SimulationAAAdapter
