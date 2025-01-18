import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from src.ai.ai_manager import AIManager

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
            'amount': np.random.uniform(10, 1000),
            'timestamp': base_time + timedelta(hours=i),
            'gas_price': np.random.uniform(1, 100),
            'block_time': np.random.uniform(1, 15)
        })
    
    return transactions

@pytest.fixture
def sample_social_data():
    base_time = datetime.now()
    return [
        {
            'sentiment': np.random.uniform(-1, 1),
            'timestamp': base_time + timedelta(hours=i),
            'source': 'twitter',
            'volume': np.random.randint(100, 1000)
        }
        for i in range(50)
    ]

def test_supply_model_training(ai_manager, sample_training_data):
    # Test model training
    ai_manager.train_supply_model(sample_training_data)
    
    # Test prediction with sample data
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

def test_market_sentiment_analysis(ai_manager, sample_transactions, sample_social_data):
    # Test without social data
    sentiment_result = ai_manager.analyze_market_sentiment(sample_transactions)
    assert isinstance(sentiment_result, dict)
    assert 'sentiment_score' in sentiment_result
    assert 'confidence' in sentiment_result
    assert -1 <= sentiment_result['sentiment_score'] <= 1
    assert 0 <= sentiment_result['confidence'] <= 1

    # Test with social data
    sentiment_result = ai_manager.analyze_market_sentiment(
        sample_transactions, 
        sample_social_data
    )
    assert isinstance(sentiment_result, dict)
    assert -1 <= sentiment_result['sentiment_score'] <= 1
    assert 0 <= sentiment_result['confidence'] <= 1

def test_historical_data_update(ai_manager):
    # Test updating price data
    new_prices = [10.0, 11.0, 12.0]
    ai_manager.update_historical_data(new_prices=new_prices)
    assert len(ai_manager.historical_prices) == len(new_prices)
    assert ai_manager.historical_prices == new_prices

    # Test updating volume data
    new_volumes = [1000, 2000, 3000]
    ai_manager.update_historical_data(new_volumes=new_volumes)
    assert len(ai_manager.historical_volumes) == len(new_volumes)
    assert ai_manager.historical_volumes == new_volumes

    # Test length limit
    long_prices = [float(i) for i in range(1000)]
    ai_manager.update_historical_data(new_prices=long_prices)
    assert len(ai_manager.historical_prices) == 720  # Max history length

def test_supply_adjustment_recommendation(ai_manager, sample_transactions):
    # Initialize with some historical data
    ai_manager.historical_transactions = sample_transactions
    ai_manager.historical_prices = list(np.random.uniform(1, 100, 50))

    current_data = {
        'demand': 3000,
        'price': 5.0,
        'transaction_volume': 50000,
        'staking_ratio': 0.5,
        'current_supply': 5000000
    }

    # Get recommendation
    recommendation = ai_manager.get_supply_adjustment_recommendation(current_data)
    
    assert isinstance(recommendation, dict)
    assert 'recommended_supply' in recommendation
    assert 'recommended_change' in recommendation
    assert 'price_trend' in recommendation
    assert 'market_sentiment' in recommendation
    assert isinstance(recommendation['market_sentiment'], dict)

def test_model_persistence(ai_manager, sample_training_data, tmp_path):
    # Modify model paths to use temporary directory
    for key in ai_manager.model_paths:
        ai_manager.model_paths[key] = str(tmp_path / f"{key}_model.joblib")

    # Train models
    ai_manager.train_supply_model(sample_training_data)
    
    # Save models
    ai_manager.save_models()

    # Create new instance and load models
    new_ai_manager = AIManager()
    new_ai_manager.model_paths = ai_manager.model_paths
    new_ai_manager.load_models()

    # Test prediction with both instances
    current_data = {
        'demand': 3000,
        'price': 5.0,
        'transaction_volume': 50000,
        'staking_ratio': 0.5,
        'current_supply': 5000000
    }

    pred1 = ai_manager.predict_optimal_supply(current_data)
    pred2 = new_ai_manager.predict_optimal_supply(current_data)
    
    assert abs(pred1 - pred2) < 1e-10  # Should be identical

def test_edge_cases(ai_manager):
    # Test with empty transaction list
    sentiment = ai_manager.analyze_market_sentiment([])
    assert sentiment['sentiment_score'] == 0.0
    assert sentiment['confidence'] == 0.0

    # Test with insufficient price history
    prediction, confidence = ai_manager.predict_price_trend()
    assert prediction == 0.0
    assert confidence == 0.0

    # Test with invalid current data
    invalid_data = {
        'demand': -1000,  # Invalid negative demand
        'price': 0,
        'transaction_volume': -5000,
        'staking_ratio': 2.0,  # Invalid ratio > 1
        'current_supply': 0
    }
    supply = ai_manager.predict_optimal_supply(invalid_data)
    assert supply >= 1000000  # Should return minimum supply

def test_model_constraints(ai_manager, sample_training_data):
    ai_manager.train_supply_model(sample_training_data)

    # Test maximum adjustment constraint
    current_data = {
        'demand': 10000,  # Very high demand
        'price': 100.0,   # Very high price
        'transaction_volume': 1000000,
        'staking_ratio': 0.9,
        'current_supply': 5000000
    }
    
    new_supply = ai_manager.predict_optimal_supply(current_data)
    max_allowed_change = current_data['current_supply'] * 0.1  # 10% max adjustment
    actual_change = abs(new_supply - current_data['current_supply'])
    
    assert actual_change <= max_allowed_change

def test_sentiment_analysis_components(ai_manager, sample_transactions):
    # Test transaction pattern analysis
    recent_tx = sample_transactions[-20:]  # Last 20 transactions
    sentiment = ai_manager.analyze_market_sentiment(recent_tx)
    
    assert 'sentiment_score' in sentiment
    assert 'confidence' in sentiment
    assert -1 <= sentiment['sentiment_score'] <= 1
    assert 0 <= sentiment['confidence'] <= 1
    assert isinstance(sentiment['timestamp'], datetime)

def test_real_time_updates(ai_manager):
    # Simulate real-time data updates
    base_time = datetime.now()
    
    for i in range(10):
        # Create new data point
        new_price = 100 + np.random.normal(0, 5)
        new_volume = 1000 + np.random.normal(0, 100)
        new_transaction = {
            'amount': new_volume,
            'timestamp': base_time + timedelta(hours=i),
            'gas_price': 50 + np.random.normal(0, 5),
            'block_time': 5 + np.random.normal(0, 0.5)
        }

        # Update historical data
        ai_manager.update_historical_data(
            new_prices=[new_price],
            new_volumes=[new_volume],
            new_transactions=[new_transaction]
        )

        # Verify data was updated correctly
        assert ai_manager.historical_prices[-1] == new_price
        assert ai_manager.historical_volumes[-1] == new_volume
        assert ai_manager.historical_transactions[-1] == new_transaction
