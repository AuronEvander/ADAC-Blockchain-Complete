from typing import Dict, List, Optional
from decimal import Decimal
import time
import hashlib

class StateChannel:
    def __init__(self, participant1: str, participant2: str):
        self.participants = [participant1, participant2]
        self.state = {}
        self.nonce = 0
        self.is_open = True
        self.balance = {participant1: Decimal('0'), participant2: Decimal('0')}
        self.channel_id = self._generate_channel_id()

    def _generate_channel_id(self) -> str:
        channel_string = f"{self.participants[0]}{self.participants[1]}{time.time()}"
        return hashlib.sha256(channel_string.encode()).hexdigest()

    def update_state(self, new_state: Dict, signer: str) -> bool:
        if not self.is_open or signer not in self.participants:
            return False
        self.state = new_state
        self.nonce += 1
        return True

class PlasmaChain:
    def __init__(self, operator: str):
        self.operator = operator
        self.blocks: List[Dict] = []
        self.exits: Dict[str, Dict] = {}
        self.deposits: Dict[str, Decimal] = {}

    def submit_block(self, transactions: List[Dict]) -> str:
        block = {
            'transactions': transactions,
            'timestamp': time.time(),
            'operator': self.operator,
            'previous_hash': self.blocks[-1]['hash'] if self.blocks else '0',
        }
        block['hash'] = self._calculate_block_hash(block)
        self.blocks.append(block)
        return block['hash']

    def _calculate_block_hash(self, block: Dict) -> str:
        block_string = f"{block['transactions']}{block['timestamp']}{block['operator']}{block['previous_hash']}"
        return hashlib.sha256(block_string.encode()).hexdigest()