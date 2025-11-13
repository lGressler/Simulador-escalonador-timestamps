# src/transaction.py
from datetime import datetime

class TransactionStatus:
    ACTIVE = "active"
    ABORTED = "aborted"
    COMMITTED = "committed"

class Transaction:
    _counter = 0

    def __init__(self, tid: str):
        Transaction._counter += 1
        self.id = tid
        self.timestamp = datetime.now().timestamp() + Transaction._counter  # garante unicidade
        self.status = TransactionStatus.ACTIVE
        self.operations = []  # lista de operações realizadas

    def __repr__(self):
        return f"T{self.id}(TS={self.timestamp:.0f}, {self.status})"
