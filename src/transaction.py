# src/transaction.py
from datetime import datetime

class TransactionStatus:
    ACTIVE = "active"
    ABORTED = "aborted"
    COMMITTED = "committed"

class Transaction:
    def __init__(self, tid: str, timestamp: int):
        self.id = tid
        self.timestamp = timestamp
        self.status = TransactionStatus.ACTIVE
        self.operations = []

    def __repr__(self):
        return f"T{self.id}(TS={self.timestamp}, {self.status})"
