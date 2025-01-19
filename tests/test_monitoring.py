import pytest
from src.monitoring.metrics import MetricsCollector
from src.monitoring.alerts import AlertManager, Alert

def test_metrics_recording():
    collector = MetricsCollector()
    collector.record_metric("cpu_usage", 75.5)
    
    metrics = collector.get_all_metrics()
    assert "cpu_usage" in metrics
    assert metrics["cpu_usage"]["current"] == 75.5

def test_alert_creation():
    alert_manager = AlertManager()
    alert = Alert(
        name="high_cpu",
        description="CPU usage is too high",
        severity="warning"
    )
    
    alert_manager.add_alert(alert)
    active_alerts = alert_manager.get_active_alerts()
    assert len(active_alerts) == 1
    assert active_alerts[0].name == "high_cpu"

def test_alert_clearing():
    alert_manager = AlertManager()
    alert = Alert(
        name="high_cpu",
        description="CPU usage is too high",
        severity="warning"
    )
    
    alert_manager.add_alert(alert)
    success = alert_manager.clear_alert("high_cpu")
    assert success
    assert len(alert_manager.get_active_alerts()) == 0