import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta

class TransactionPredictor:
    def __init__(self):
        self.historical_data: List[Dict] = []
        self.training_window = 30  # Days of historical data to use
        
    def add_transaction(self, transaction: Dict) -> None:
        self.historical_data.append({
            'timestamp': transaction['timestamp'],
            'amount': transaction['amount'],
            'type': transaction['type']
        })
        
    def predict_network_load(self) -> Dict:
        if not self.historical_data:
            return {'prediction': 0, 'confidence': 0}
            
        recent_data = self._get_recent_data()
        if not recent_data:
            return {'prediction': 0, 'confidence': 0}
            
        # Simple moving average prediction
        avg_transactions = np.mean([d['amount'] for d in recent_data])
        std_dev = np.std([d['amount'] for d in recent_data])
        
        return {
            'prediction': avg_transactions,
            'confidence': 1 - (std_dev / avg_transactions) if avg_transactions else 0
        }
        
    def _get_recent_data(self) -> List[Dict]:
        cutoff_time = datetime.now() - timedelta(days=self.training_window)
        return [tx for tx in self.historical_data 
                if datetime.fromtimestamp(tx['timestamp']) > cutoff_time]