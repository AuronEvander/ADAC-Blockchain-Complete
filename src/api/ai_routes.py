from flask import Blueprint, request, jsonify
from ..ai.ai_manager import AIManager
from datetime import datetime

ai_bp = Blueprint('ai', __name__)
ai_manager = AIManager()

@ai_bp.route('/supply/predict', methods=['POST'])
def predict_supply():
    """Predict optimal token supply based on current market conditions"""
    try:
        data = request.json
        required_fields = ['demand', 'price', 'transaction_volume', 'staking_ratio', 'current_supply']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        prediction = ai_manager.predict_optimal_supply(data)
        
        return jsonify({
            'predicted_supply': prediction,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/transactions/analyze', methods=['POST'])
def analyze_transactions():
    """Detect anomalies in transactions"""
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({'error': 'Expected list of transactions'}), 400

        anomalies = ai_manager.detect_anomalies(data)
        
        # Pair transactions with their anomaly status
        analysis_results = [
            {
                'transaction': tx,
                'is_anomaly': is_anomaly
            }
            for tx, is_anomaly in zip(data, anomalies)
        ]
        
        return jsonify({
            'results': analysis_results,
            'anomaly_count': sum(anomalies),
            'total_transactions': len(anomalies),
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/market/sentiment', methods=['POST'])
def analyze_market_sentiment():
    """Analyze market sentiment based on transactions and social data"""
    try:
        data = request.json
        transactions = data.get('transactions', [])
        social_data = data.get('social_data')
        
        sentiment = ai_manager.analyze_market_sentiment(transactions, social_data)
        
        return jsonify(sentiment), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/supply/recommendation', methods=['POST'])
def get_supply_recommendation():
    """Get comprehensive supply adjustment recommendation"""
    try:
        data = request.json
        required_fields = ['demand', 'price', 'transaction_volume', 'staking_ratio', 'current_supply']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        recommendation = ai_manager.get_supply_adjustment_recommendation(data)
        
        return jsonify(recommendation), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/models/train', methods=['POST'])
def train_models():
    """Train AI models with new data"""
    try:
        data = request.json
        training_summary = {
            'models_trained': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Train supply model if training data provided
        if 'supply_training_data' in data:
            ai_manager.train_supply_model(data['supply_training_data'])
            training_summary['models_trained'].append('supply_model')
        
        # Train anomaly detector if transaction data provided
        if 'transaction_data' in data:
            ai_manager.train_anomaly_detector(data['transaction_data'])
            training_summary['models_trained'].append('anomaly_detector')
        
        # Save trained models
        ai_manager.save_models()
        training_summary['status'] = 'success'
        
        return jsonify(training_summary), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed',
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_bp.route('/data/update', methods=['POST'])
def update_historical_data():
    """Update historical data used by AI models"""
    try:
        data = request.json
        update_summary = {
            'updated_fields': [],
            'timestamp': datetime.now().isoformat()
        }
        
        if 'prices' in data:
            ai_manager.update_historical_data(new_prices=data['prices'])
            update_summary['updated_fields'].append('prices')
            
        if 'volumes' in data:
            ai_manager.update_historical_data(new_volumes=data['volumes'])
            update_summary['updated_fields'].append('volumes')
            
        if 'transactions' in data:
            ai_manager.update_historical_data(new_transactions=data['transactions'])
            update_summary['updated_fields'].append('transactions')
            
        if 'supply' in data:
            ai_manager.update_historical_data(new_supply=data['supply'])
            update_summary['updated_fields'].append('supply')
        
        update_summary['status'] = 'success'
        return jsonify(update_summary), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed',
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_bp.route('/price/trend', methods=['GET'])
def get_price_trend():
    """Get price trend prediction"""
    try:
        window_size = request.args.get('window_size', default=24, type=int)
        prediction, confidence = ai_manager.predict_price_trend(window_size)
        
        return jsonify({
            'prediction': prediction,
            'confidence': confidence,
            'window_size': window_size,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/stats', methods=['GET'])
def get_ai_stats():
    """Get statistics about the AI system"""
    try:
        stats = {
            'historical_data_points': {
                'prices': len(ai_manager.historical_prices),
                'volumes': len(ai_manager.historical_volumes),
                'transactions': len(ai_manager.historical_transactions),
                'supply': len(ai_manager.historical_supply)
            },
            'models': {
                'supply_model': {
                    'trained': hasattr(ai_manager.supply_model, 'n_features_in_'),
                    'last_updated': datetime.fromtimestamp(
                        getattr(ai_manager.supply_model, '_last_updated', 0)
                    ).isoformat()
                },
                'anomaly_detector': {
                    'trained': hasattr(ai_manager.anomaly_detector, 'offset_'),
                    'last_updated': datetime.fromtimestamp(
                        getattr(ai_manager.anomaly_detector, '_last_updated', 0)
                    ).isoformat()
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/health', methods=['GET'])
def health_check():
    """Check the health status of the AI system"""
    try:
        # Check if models are loaded
        models_loaded = all([
            hasattr(ai_manager.supply_model, 'n_features_in_'),
            hasattr(ai_manager.anomaly_detector, 'offset_'),
            hasattr(ai_manager.price_predictor, 'coef_'),
            hasattr(ai_manager.transaction_classifier, 'classes_')
        ])

        # Check if we have historical data
        has_historical_data = all([
            len(ai_manager.historical_prices) > 0,
            len(ai_manager.historical_volumes) > 0,
            len(ai_manager.historical_transactions) > 0
        ])

        status = {
            'status': 'healthy' if models_loaded and has_historical_data else 'degraded',
            'models_loaded': models_loaded,
            'has_historical_data': has_historical_data,
            'last_update': datetime.now().isoformat()
        }

        return jsonify(status), 200 if status['status'] == 'healthy' else 503

    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
