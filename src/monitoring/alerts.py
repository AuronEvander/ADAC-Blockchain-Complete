from typing import List, Dict, Callable
from datetime import datetime

class Alert:
    def __init__(self, name: str, description: str, severity: str = 'info'):
        self.name = name
        self.description = description
        self.severity = severity
        self.timestamp = datetime.now()

class AlertManager:
    def __init__(self):
        self.alerts: List[Alert] = []
        self.handlers: Dict[str, List[Callable]] = {}
        self.severity_levels = ['info', 'warning', 'error', 'critical']
        
    def add_alert(self, alert: Alert) -> None:
        self.alerts.append(alert)
        self._notify_handlers(alert)
        
    def register_handler(self, severity: str, handler: Callable) -> None:
        if severity not in self.handlers:
            self.handlers[severity] = []
        self.handlers[severity].append(handler)
        
    def _notify_handlers(self, alert: Alert) -> None:
        handlers = self.handlers.get(alert.severity, [])
        for handler in handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Error in alert handler: {str(e)}")
                
    def get_active_alerts(self, severity: str = None) -> List[Alert]:
        if not severity:
            return self.alerts
        return [alert for alert in self.alerts if alert.severity == severity]
        
    def clear_alert(self, alert_name: str) -> bool:
        initial_length = len(self.alerts)
        self.alerts = [alert for alert in self.alerts if alert.name != alert_name]
        return len(self.alerts) < initial_length