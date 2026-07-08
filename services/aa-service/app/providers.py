import abc
import datetime
import uuid
from typing import List, Dict, Any

class AAProviderInterface(abc.ABC):
    @abc.abstractmethod
    def discover_financial_accounts(self, customer_mobile: str) -> List[Dict[str, Any]]:
        """Query banks associated with user mobile using Account Aggregator registry"""
        pass

    @abc.abstractmethod
    def fetch_transaction_ledger(self, account_ref_num: str) -> List[Dict[str, Any]]:
        """Fetch bank transaction logs for a linked account"""
        pass

class AccountAggregatorMockProvider(AAProviderInterface):
    def discover_financial_accounts(self, customer_mobile: str) -> List[Dict[str, Any]]:
        # Mock discovery of active accounts at State Bank of India & IDBI Bank
        return [
            {
                "account_ref_num": f"SBI-ACC-{uuid.uuid4().hex[:6].upper()}",
                "masked_acc_num": "XXXXXX4321",
                "bank_name": "State Bank of India",
                "account_type": "CURRENT",
                "balance": 450000.0,
                "currency": "INR"
            },
            {
                "account_ref_num": f"IDBI-ACC-{uuid.uuid4().hex[:6].upper()}",
                "masked_acc_num": "XXXXXX9876",
                "bank_name": "IDBI Bank",
                "account_type": "SAVINGS",
                "balance": 125000.0,
                "currency": "INR"
            }
        ]

    def fetch_transaction_ledger(self, account_ref_num: str) -> List[Dict[str, Any]]:
        # Simulate 12 months transactions with categorizable narration patterns
        ledger = []
        base_date = datetime.datetime.utcnow() - datetime.timedelta(days=180)
        
        # Inflow / Income transactions
        for i in range(6):
            ledger.append({
                "txn_ref_num": f"TXN-IN-{uuid.uuid4().hex[:8].upper()}",
                "txn_date": base_date + datetime.timedelta(days=(i * 30) + 1),
                "amount": 250000.0,
                "txn_type": "CREDIT",
                "narration": "NEFT CLIENT SETTLEMENT / AUTO PARTS MFG"
            })
            
        # Outflow / Rent / Vendor / Utility transactions
        for i in range(6):
            # Rent (Recurring)
            ledger.append({
                "txn_ref_num": f"TXN-OUT-{uuid.uuid4().hex[:8].upper()}",
                "txn_date": base_date + datetime.timedelta(days=(i * 30) + 5),
                "amount": 45000.0,
                "txn_type": "DEBIT",
                "narration": "RENT DEPOSIT PAYMENT / INDUSTRIAL PLOT"
            })
            # Vendor payment
            ledger.append({
                "txn_ref_num": f"TXN-OUT-{uuid.uuid4().hex[:8].upper()}",
                "txn_date": base_date + datetime.timedelta(days=(i * 30) + 12),
                "amount": 95000.0,
                "txn_type": "DEBIT",
                "narration": "RTGS METAL SUPPLIER INDIA PVT"
            })
            
        return ledger
