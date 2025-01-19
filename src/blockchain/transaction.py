from dataclasses import dataclass
from datetime import datetime
import hashlib
from typing import Optional

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    timestamp: float = datetime.now().timestamp()
    signature: Optional[str] = None
    
    def calculate_hash(self) -> str:
        transaction_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def sign(self, private_key: str) -> None:
        # Implement actual signature logic here
        self.signature = hashlib.sha256(
            (self.calculate_hash() + private_key).encode()
        ).hexdigest()
    
    def is_valid(self) -> bool:
        if self.sender == "0":
            return True  # Mining reward
        if not self.signature:
            return False
        return True  # Add actual signature verification