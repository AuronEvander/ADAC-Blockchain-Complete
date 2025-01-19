import pytest
from datetime import datetime, timedelta
from src.ai.ai_manager import AIManager
import pandas as pd
import numpy as np

@pytest.fixture
def ai_manager():
    return AIManager()

@pytest.fixture
def sample_training_data():
    return pd.DataFrame({
        'demand': np.random.uniform(1000, 5000, 100),
        'price': np.random.uniform(0.1, 10.0, 100),
        'transaction_volume': np.random.uniform(10000, 100000, 100),
        'staking_ratio': np.random.uniform(0.1, 0.9, 100),
        'optimal_supply': np.random.uniform(1000000, 10000000, 100)
    })

@pytest.fixture
def sample_transactions():
    transactions = []
    base_time = datetime.now()
    
    for i in range(100):
        transactions.append({
            'amount': float(np.random.uniform(10, 1000)),
            'timestamp': base_time + timedelta(hours=i),
            'gas_price': float(np.random.uniform(1, 100)),
            'block_time': float(np.random.uniform(1, 15))
        })
    
    return transactions

def test_supply_model_training(ai_manager, sample_training_data):
    # Test model training
    ai_manager.train_supply_model(sample_training_data)
    
    # Test prediction
    current_data = {
        'demand': 3000,
        'price': 5.0,
        'transaction_volume': 50000,
        'staking_ratio': 0.5,
        'current_supply': 5000000
    }
    
    prediction = ai_manager.predict_optimal_supply(current_data)
    assert isinstance(prediction, float)
    assert prediction > 0
    assert prediction >= 1000000  # Minimum supply threshold

def test_anomaly_detection(ai_manager, sample_transactions):
    # Train anomaly detector
    ai_manager.train_anomaly_detector(sample_transactions)
    
    # Test anomaly detection
    results = ai_manager.detect_anomalies(sample_transactions[:10])
    assert isinstance(results, list)
    assert len(results) == 10
    assert all(isinstance(x, bool) for x in results)

def test_price_trend_prediction(ai_manager):
    # Add historical prices
    ai_manager.historical_prices = list(np.random.uniform(1, 100, 50))
    
    # Test prediction
    prediction, confidence = ai_manager.predict_price_trend(window_size=24)
    assert isinstance(prediction, float)
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 1