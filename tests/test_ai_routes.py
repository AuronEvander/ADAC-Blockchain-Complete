import pytest
from datetime import datetime
from src.api.ai_routes import ai_bp
from flask import Flask, json
import numpy as np

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_market_data():
    return {
        'demand': 3000,
        'price': 5.0,
        'transaction_volume': 50000,
        'staking_ratio': 0.5,
        'current_supply': 5000000
    }

@pytest.fixture
def sample_transactions():
    transactions = []
    base_time = datetime.now()
    for i in range(10):
        transactions.append({
            'amount': float(np.random.uniform(10, 1000)),
            'timestamp': base_time.isoformat(),
            'gas_price': float(np.random.uniform(1, 100)),
            'block_time': float(np.random.uniform(1, 15))
        })
    return transactions

def test_predict_supply(client, sample_market_data):
    response = client.post(
        '/api/ai/supply/predict',
        json=sample_market_data
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'predicted_supply' in data
    assert isinstance(data['predicted_supply'], float)
    assert data['predicted_supply'] > 0
    assert 'timestamp' in data

def test_analyze_transactions(client, sample_transactions):
    response = client.post(
        '/api/ai/transactions/analyze',
        json=sample_transactions
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert len(data['results']) == len(sample_transactions)
    assert 'anomaly_count' in data
    assert 'total_transactions' in data
    assert data['total_transactions'] == len(sample_transactions)

def test_market_sentiment(client, sample_transactions):
    data = {
        'transactions': sample_transactions,
        'social_data': [
            {
                'sentiment': 0.8,
                'timestamp': datetime.now().isoformat(),
                'source': 'twitter',
                'volume': 1000
            }
        ]
    }
    
    response = client.post(
        '/api/ai/market/sentiment',
        json=data
    )
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'sentiment_score' in result
    assert 'confidence' in result
    assert -1 <= result['sentiment_score'] <= 1
    assert 0 <= result['confidence'] <= 1

def test_supply_recommendation(client, sample_market_data):
    response = client.post(
        '/api/ai/supply/recommendation',
        json=sample_market_data
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'recommended_supply' in data
    assert 'recommended_change' in data
    assert 'price_trend' in data
    assert 'market_sentiment' in data

def test_model_training(client, sample_transactions):
    training_data = {
        'supply_training_data': {
            'demand': [3000, 4000, 5000],
            'price': [5.0, 5.5, 6.0],
            'transaction_volume': [50000, 60000, 70000],
            'staking_ratio': [0.5, 0.6, 0.7],
            'optimal_supply': [5000000, 5500000, 6000000]
        },
        'transaction_data': sample_transactions
    }
    
    response = client.post(
        '/api/ai/models/train',
        json=training_data
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'models_trained' in data
    assert 'timestamp' in data
    assert 'status' in data
    assert data['status'] == 'success'

def test_historical_data_update(client, sample_transactions):
    update_data = {
        'prices': [100.0, 101.0, 102.0],
        'volumes': [50000, 51000, 52000],
        'transactions': sample_transactions,
        'supply': [5000000, 5100000, 5200000]
    }
    
    response = client.post(
        '/api/ai/data/update',
        json=update_data
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'updated_fields' in data
    assert 'status' in data
    assert data['status'] == 'success'

def test_price_trend(client):
    response = client.get('/api/ai/price/trend?window_size=24')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data
    assert 'confidence' in data
    assert 'window_size' in data
    assert data['window_size'] == 24

def test_ai_stats(client):
    response = client.get('/api/ai/stats')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'historical_data_points' in data
    assert 'models' in data
    assert 'timestamp' in data

def test_health_check(client):
    response = client.get('/api/ai/health')
    
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    assert 'status' in data
    assert 'models_loaded' in data
    assert 'has_historical_data' in data
    assert 'last_update' in data

def test_error_handling_missing_fields(client):
    # Test missing required fields in supply prediction
    response = client.post(
        '/api/ai/supply/predict',
        json={'demand': 3000}  # Missing other required fields
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_error_handling_invalid_data(client):
    # Test invalid data types
    response = client.post(
        '/api/ai/supply/predict',
        json={
            'demand': 'invalid',  # Should be number
            'price': 5.0,
            'transaction_volume': 50000,
            'staking_ratio': 0.5,
            'current_supply': 5000000
        }
    )
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data

def test_error_handling_invalid_transactions(client):
    # Test invalid transaction data
    response = client.post(
        '/api/ai/transactions/analyze',
        json={'not_a_list': True}  # Should be a list
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_model_training_edge_cases(client):
    # Test training with empty data
    response = client.post(
        '/api/ai/models/train',
        json={}
    )
    assert response.status_code == 200  # Should succeed but train no models
    data = json.loads(response.data)
    assert len(data['models_trained']) == 0

def test_historical_data_validation(client):
    # Test update with invalid data types
    response = client.post(
        '/api/ai/data/update',
        json={
            'prices': ['invalid', 'prices'],  # Should be numbers
            'volumes': [50000, 51000]
        }
    )
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data

def test_concurrent_requests(client, sample_market_data):
    """Test handling multiple requests concurrently"""
    import threading
    
    def make_request():
        response = client.post(
            '/api/ai/supply/predict',
            json=sample_market_data
        )
        assert response.status_code == 200
    
    threads = []
    for _ in range(5):  # Make 5 concurrent requests
        t = threading.Thread(target=make_request)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

def test_large_data_handling(client):
    # Test with a large number of transactions
    large_transactions = []
    base_time = datetime.now()
    for i in range(1000):  # Create 1000 transactions
        large_transactions.append({
            'amount': float(np.random.uniform(10, 1000)),
            'timestamp': base_time.isoformat(),
            'gas_price': float(np.random.uniform(1, 100)),
            'block_time': float(np.random.uniform(1, 15))
        })
    
    response = client.post(
        '/api/ai/transactions/analyze',
        json=large_transactions
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['results']) == 1000

def test_rate_limiting(client, sample_market_data):
    """Test rapid repeated requests"""
    responses = []
    for _ in range(50):  # Make 50 rapid requests
        response = client.post(
            '/api/ai/supply/predict',
            json=sample_market_data
        )
        responses.append(response.status_code)
    
    # All requests should either succeed or be rate limited
    assert all(status in [200, 429] for status in responses)

def test_invalid_window_size(client):
    # Test price trend with invalid window size
    response = client.get('/api/ai/price/trend?window_size=-1')
    assert response.status_code == 400
    
    response = client.get('/api/ai/price/trend?window_size=1001')  # Too large
    assert response.status_code == 400

def test_model_persistence(client, sample_market_data, tmp_path):
    # Train models
    response = client.post(
        '/api/ai/models/train',
        json={
            'supply_training_data': {
                'demand': [3000, 4000],
                'price': [5.0, 5.5],
                'transaction_volume': [50000, 60000],
                'staking_ratio': [0.5, 0.6],
                'optimal_supply': [5000000, 5500000]
            }
        }
    )
    assert response.status_code == 200
    
    # Make prediction
    response1 = client.post(
        '/api/ai/supply/predict',
        json=sample_market_data
    )
    pred1 = json.loads(response1.data)['predicted_supply']
    
    # Make another prediction (should use same model)
    response2 = client.post(
        '/api/ai/supply/predict',
        json=sample_market_data
    )
    pred2 = json.loads(response2.data)['predicted_supply']
    
    # Predictions should be identical since using same model
    assert pred1 == pred2
