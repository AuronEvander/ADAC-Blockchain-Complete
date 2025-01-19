from typing import List, Dict
import numpy as np
from datetime import datetime, timedelta

class AnomalyDetector:
    def __init__(self):
        self.transaction_history: List[Dict] = []
        self.threshold = 3  # Standard deviations for anomaly detection
        
    def add_transaction(self, transaction: Dict) -> None:
        self.transaction_history.append(transaction)
        
    def detect_anomalies(self, new_transaction: Dict) -> Dict:
        if len(self.transaction_history) < 10:
            return {'is_anomaly': False, 'confidence': 0}
            
        # Calculate statistics from history
        amounts = [tx['amount'] for tx in self.transaction_history]
        mean_amount = np.mean(amounts)
        std_amount = np.std(amounts)
        
        # Z-score calculation
        z_score = abs(new_transaction['amount'] - mean_amount) / std_amount
        
        return {
            'is_anomaly': z_score > self.threshold,
            'confidence': min(1.0, z_score / self.threshold),
            'z_score': z_score
        }
        
    def get_anomaly_report(self) -> Dict:
        total_transactions = len(self.transaction_history)
        if total_transactions == 0:
            return {'anomaly_rate': 0, 'total_transactions': 0}
            
        anomalies = sum(1 for tx in self.transaction_history 
                       if self.detect_anomalies(tx)['is_anomaly'])
                       
        return {
            'anomaly_rate': anomalies / total_transactions,
            'total_transactions': total_transactions,
            'total_anomalies': anomalies
        }