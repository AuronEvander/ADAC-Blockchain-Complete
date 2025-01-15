from typing import List, Dict
import time
import asyncio

class AlertManager:
    def __init__(self):
        self.alerts = []
        self.alert_handlers = {
            'high_latency': self._handle_high_latency,
            'low_peers': self._handle_low_peers,
            'attack_detected': self._handle_attack,
            'node_down': self._handle_node_down
        }

    async def monitor_network(self):
        while True:
            metrics = self._collect_metrics()
            await self._analyze_metrics(metrics)
            await asyncio.sleep(60)

    async def _analyze_metrics(self, metrics: Dict):
        if metrics['latency'] > 1000:  # 1 second
            await self._create_alert('high_latency', metrics)
            
        if metrics['peer_count'] < 3:
            await self._create_alert('low_peers', metrics)

    async def _create_alert(self, alert_type: str, data: Dict):
        alert = {
            'type': alert_type,
            'data': data,
            'timestamp': time.time()
        }
        self.alerts.append(alert)
        
        if alert_type in self.alert_handlers:
            await self.alert_handlers[alert_type](alert)