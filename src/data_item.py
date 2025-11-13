# src/data_item.py
class DataItem:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.rts = 0  # Read Timestamp
        self.wts = 0  # Write Timestamp

    def __repr__(self):
        return f"{self.name}(RTS={self.rts}, WTS={self.wts})"
