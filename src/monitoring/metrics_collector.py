from prometheus_client import Counter, Gauge, Histogram
import time
from typing import Dict

class MetricsCollector:
    def __init__(self):
        # Transaction metrics
        self.transaction_counter = Counter(
            'transactions_total',
            'Total number of transactions'
        )
        self.transaction_volume = Counter(
            'transaction_volume_total',
            'Total transaction volume'
        )
        
        # Block metrics
        self.block_time_gauge = Gauge(
            'block_time_seconds',
            'Time to mine last block'
        )
        self.block_size_gauge = Gauge(
            'block_size_bytes',
            'Size of the last block'
        )
        
        # Network metrics
        self.peer_count_gauge = Gauge(
            'peer_count',
            'Number of connected peers'
        )
        self.network_latency = Histogram(
            'network_latency_seconds',
            'Network latency'
        )
        
        # DeFi metrics
        self.total_value_locked = Gauge(
            'total_value_locked',
            'Total value locked in DeFi protocols'
        )
        self.active_validators = Gauge(
            'active_validators',
            'Number of active validators'
        )

    def record_transaction(self, amount: float):
        self.transaction_counter.inc()
        self.transaction_volume.inc(amount)

    def update_block_metrics(self, time_seconds: float, size_bytes: int):
        self.block_time_gauge.set(time_seconds)
        self.block_size_gauge.set(size_bytes)