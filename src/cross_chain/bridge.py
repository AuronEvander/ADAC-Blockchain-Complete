from typing import Dict, List
from datetime import datetime
import hashlib

class CrossChainBridge:
    def __init__(self):
        self.locked_tokens: Dict[str, Dict[str, float]] = {}
        self.pending_transfers: List[Dict] = []
        self.completed_transfers: List[Dict] = []
        self.validators: List[str] = []
        self.required_validations = 2
        
    def lock_tokens(self, chain_id: str, token_address: str, amount: float, recipient: str) -> str:
        transfer_id = hashlib.sha256(
            f"{chain_id}{token_address}{amount}{recipient}{datetime.now().timestamp()}".encode()
        ).hexdigest()
        
        if chain_id not in self.locked_tokens:
            self.locked_tokens[chain_id] = {}
        
        self.locked_tokens[chain_id][token_address] = \
            self.locked_tokens[chain_id].get(token_address, 0) + amount
            
        self.pending_transfers.append({
            'id': transfer_id,
            'chain_id': chain_id,
            'token_address': token_address,
            'amount': amount,
            'recipient': recipient,
            'status': 'pending',
            'validations': [],
            'timestamp': datetime.now().timestamp()
        })
        
        return transfer_id
        
    def validate_transfer(self, transfer_id: str, validator: str) -> bool:
        if validator not in self.validators:
            return False
            
        transfer = next((t for t in self.pending_transfers if t['id'] == transfer_id), None)
        if not transfer:
            return False
            
        if validator in transfer['validations']:
            return False
            
        transfer['validations'].append(validator)
        
        if len(transfer['validations']) >= self.required_validations:
            transfer['status'] = 'completed'
            self.completed_transfers.append(transfer)
            self.pending_transfers.remove(transfer)
            
        return True
        
    def get_transfer_status(self, transfer_id: str) -> Dict:
        transfer = next(
            (t for t in self.pending_transfers + self.completed_transfers 
             if t['id'] == transfer_id),
            None
        )
        
        if not transfer:
            return {'status': 'not_found'}
            
        return {
            'status': transfer['status'],
            'validations': len(transfer['validations']),
            'required_validations': self.required_validations
        }