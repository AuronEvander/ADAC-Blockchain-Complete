import psutil
from typing import Dict
from datetime import datetime

class SystemHealthMonitor:
    def __init__(self, alert_manager=None):
        self.alert_manager = alert_manager
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0
        }
        
    def check_system_health(self) -> Dict:
        health_metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(),
            'memory': self._get_memory_metrics(),
            'disk': self._get_disk_metrics(),
            'network': self._get_network_metrics()
        }
        
        self._check_thresholds(health_metrics)
        return health_metrics
        
    def _get_memory_metrics(self) -> Dict:
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used
        }
        
    def _get_disk_metrics(self) -> Dict:
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
        
    def _get_network_metrics(self) -> Dict:
        network = psutil.net_io_counters()
        return {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv
        }
        
    def _check_thresholds(self, metrics: Dict) -> None:
        if not self.alert_manager:
            return
            
        if metrics['cpu_percent'] > self.thresholds['cpu_percent']:
            self.alert_manager.add_alert(Alert(
                name='high_cpu_usage',
                description=f"CPU usage is at {metrics['cpu_percent']}%",
                severity='warning'
            ))
            
        if metrics['memory']['percent'] > self.thresholds['memory_percent']:
            self.alert_manager.add_alert(Alert(
                name='high_memory_usage',
                description=f"Memory usage is at {metrics['memory']['percent']}%",
                severity='warning'
            ))
            
        if metrics['disk']['percent'] > self.thresholds['disk_percent']:
            self.alert_manager.add_alert(Alert(
                name='high_disk_usage',
                description=f"Disk usage is at {metrics['disk']['percent']}%",
                severity='warning'
            ))