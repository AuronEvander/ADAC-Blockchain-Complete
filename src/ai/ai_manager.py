import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

class AIManager:
    def __init__(self):
        self.supply_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.price_predictor = LinearRegression()
        self.transaction_classifier = LogisticRegression(random_state=42)
        self.scaler = StandardScaler()
        
        # Historical data storage
        self.historical_prices = []
        self.historical_volumes = []
        self.historical_transactions = []
        self.historical_supply = []
        
        # Model file paths
        self.model_paths = {
            'supply': 'models/supply_model.joblib',
            'anomaly': 'models/anomaly_detector.joblib',
            'price': 'models/price_predictor.joblib',
            'transaction': 'models/transaction_classifier.joblib',
            'scaler': 'models/scaler.joblib'
        }

    def train_supply_model(self, training_data: pd.DataFrame) -> None:
        """Train the supply prediction model"""
        try:
            X = training_data[['demand', 'price', 'transaction_volume', 'staking_ratio']]
            y = training_data['optimal_supply']
            
            X_scaled = self.scaler.fit_transform(X)
            self.supply_model.fit(X_scaled, y)
            
            # Save the model
            joblib.dump(self.supply_model, self.model_paths['supply'])
            joblib.dump(self.scaler, self.model_paths['scaler'])
            
        except Exception as e:
            print(f"Error training supply model: {str(e)}")

    def predict_optimal_supply(self, current_data: Dict) -> float:
        """Predict optimal token supply based on current market conditions"""
        try:
            features = np.array([[
                current_data['demand'],
                current_data['price'],
                current_data['transaction_volume'],
                current_data['staking_ratio']
            ]])
            
            features_scaled = self.scaler.transform(features)
            predicted_supply = self.supply_model.predict(features_scaled)[0]
            
            # Apply constraints
            min_supply = 1000000  # Minimum supply threshold
            max_adjustment = 0.1  # Maximum 10% adjustment per prediction
            
            current_supply = current_data.get('current_supply', 0)
            max_change = current_supply * max_adjustment
            
            predicted_change = predicted_supply - current_supply
            if abs(predicted_change) > max_change:
                predicted_supply = current_supply + (max_change if predicted_change > 0 else -max_change)
            
            return max(predicted_supply, min_supply)
            
        except Exception as e:
            print(f"Error predicting supply: {str(e)}")
            return current_data.get('current_supply', min_supply)

    def train_anomaly_detector(self, historical_transactions: List[Dict]) -> None:
        """Train the anomaly detection model"""
        try:
            # Extract relevant features
            features = []
            for tx in historical_transactions:
                features.append([
                    tx['amount'],
                    tx['timestamp'].hour,
                    tx['gas_price'],
                    tx['block_time']
                ])
            
            X = np.array(features)
            X_scaled = self.scaler.fit_transform(X)
            
            self.anomaly_detector.fit(X_scaled)
            joblib.dump(self.anomaly_detector, self.model_paths['anomaly'])
            
        except Exception as e:
            print(f"Error training anomaly detector: {str(e)}")

    def detect_anomalies(self, transactions: List[Dict]) -> List[bool]:
        """Detect anomalous transactions"""
        try:
            features = []
            for tx in transactions:
                features.append([
                    tx['amount'],
                    tx['timestamp'].hour,
                    tx['gas_price'],
                    tx['block_time']
                ])
            
            X = np.array(features)
            X_scaled = self.scaler.transform(X)
            
            # -1 for anomalies, 1 for normal transactions
            predictions = self.anomaly_detector.predict(X_scaled)
            
            # Convert to boolean (True for anomalies)
            return [pred == -1 for pred in predictions]
            
        except Exception as e:
            print(f"Error detecting anomalies: {str(e)}")
            return [False] * len(transactions)

    def predict_price_trend(self, window_size: int = 24) -> Tuple[float, float]:
        """Predict price trend for the next time window"""
        try:
            if len(self.historical_prices) < window_size:
                return 0.0, 0.0

            recent_prices = self.historical_prices[-window_size:]
            X = np.array(range(window_size)).reshape(-1, 1)
            y = np.array(recent_prices)
            
            self.price_predictor.fit(X, y)
            
            # Predict next point
            next_point = self.price_predictor.predict([[window_size]])[0]
            
            # Calculate confidence based on R² score
            confidence = self.price_predictor.score(X, y)
            
            return next_point, confidence
            
        except Exception as e:
            print(f"Error predicting price trend: {str(e)}")
            return 0.0, 0.0

    def analyze_market_sentiment(self, 
                               transactions: List[Dict], 
                               social_data: Optional[List[Dict]] = None) -> Dict:
        """Analyze market sentiment based on transaction patterns and social data"""
        try:
            sentiment_score = 0.0
            confidence = 0.0
            
            # Analyze transaction patterns
            if transactions:
                volumes = [tx['amount'] for tx in transactions]
                avg_volume = sum(volumes) / len(volumes)
                volume_trend = (volumes[-1] / avg_volume) - 1  # Relative to average
                
                # Transaction frequency analysis
                times = [tx['timestamp'] for tx in transactions]
                time_diffs = np.diff([t.timestamp() for t in times])
                freq_trend = np.mean(time_diffs[-10:]) / np.mean(time_diffs) - 1
                
                sentiment_score += 0.4 * volume_trend + 0.3 * freq_trend
                confidence += 0.6
            
            # Incorporate social sentiment if available
            if social_data:
                social_sentiments = [item['sentiment'] for item in social_data]
                avg_social_sentiment = sum(social_sentiments) / len(social_sentiments)
                sentiment_score += 0.3 * avg_social_sentiment
                confidence += 0.4
            
            # Normalize sentiment score to [-1, 1] range
            sentiment_score = max(min(sentiment_score, 1.0), -1.0)
            confidence = min(confidence, 1.0)
            
            return {
                'sentiment_score': sentiment_score,
                'confidence': confidence,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"Error analyzing market sentiment: {str(e)}")
            return {
                'sentiment_score': 0.0,
                'confidence': 0.0,
                'timestamp': datetime.now()
            }

    def update_historical_data(self, 
                             new_prices: List[float] = None,
                             new_volumes: List[float] = None,
                             new_transactions: List[Dict] = None,
                             new_supply: List[float] = None) -> None:
        """Update historical data with new information"""
        if new_prices:
            self.historical_prices.extend(new_prices)
            # Keep last 30 days of data
            self.historical_prices = self.historical_prices[-720:]  # 24*30
            
        if new_volumes:
            self.historical_volumes.extend(new_volumes)
            self.historical_volumes = self.historical_volumes[-720:]
            
        if new_transactions:
            self.historical_transactions.extend(new_transactions)
            self.historical_transactions = self.historical_transactions[-1000:]
            
        if new_supply:
            self.historical_supply.extend(new_supply)
            self.historical_supply = self.historical_supply[-720:]

    def get_supply_adjustment_recommendation(self, current_data: Dict) -> Dict:
        """Get comprehensive supply adjustment recommendation"""
        try:
            # Predict optimal supply
            optimal_supply = self.predict_optimal_supply(current_data)
            
            # Get price trend
            price_prediction, price_confidence = self.predict_price_trend()
            
            # Analyze market sentiment
            sentiment = self.analyze_market_sentiment(
                self.historical_transactions[-100:] if self.historical_transactions else []
            )
            
            # Calculate recommended adjustment
            current_supply = current_data.get('current_supply', 0)
            supply_change = optimal_supply - current_supply
            
            # Adjust based on sentiment
            if sentiment['sentiment_score'] < -0.5 and sentiment['confidence'] > 0.6:
                supply_change *= 0.5  # Reduce adjustment in negative sentiment
            elif sentiment['sentiment_score'] > 0.5 and sentiment['confidence'] > 0.6:
                supply_change *= 1.2  # Increase adjustment in positive sentiment
            
            return {
                'recommended_supply': optimal_supply,
                'recommended_change': supply_change,
                'price_trend': price_prediction,
                'price_confidence': price_confidence,
                'market_sentiment': sentiment,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"Error generating supply recommendation: {str(e)}")
            return {
                'recommended_supply': current_data.get('current_supply', 0),
                'recommended_change': 0,
                'price_trend': 0,
                'price_confidence': 0,
                'market_sentiment': {
                    'sentiment_score': 0,
                    'confidence': 0,
                    'timestamp': datetime.now()
                },
                'timestamp': datetime.now()
            }

    def save_models(self) -> None:
        """Save all trained models"""
        try:
            joblib.dump(self.supply_model, self.model_paths['supply'])
            joblib.dump(self.anomaly_detector, self.model_paths['anomaly'])
            joblib.dump(self.price_predictor, self.model_paths['price'])
            joblib.dump(self.transaction_classifier, self.model_paths['transaction'])
            joblib.dump(self.scaler, self.model_paths['scaler'])
        except Exception as e:
            print(f"Error saving models: {str(e)}")

    def load_models(self) -> None:
        """Load all trained models"""
        try:
            self.supply_model = joblib.load(self.model_paths['supply'])
            self.anomaly_detector = joblib.load(self.model_paths['anomaly'])
            self.price_predictor = joblib.load(self.model_paths['price'])
            self.transaction_classifier = joblib.load(self.model_paths['transaction'])
            self.scaler = joblib.load(self.model_paths['scaler'])
        except Exception as e:
            print(f"Error loading models: {str(e)}")
