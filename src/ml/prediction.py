import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from typing import List, Dict

class PricePredictor:
    def __init__(self, sequence_length: int, features: int):
        self.sequence_length = sequence_length
        self.features = features
        self.model = self._build_model()
        self.scaler = StandardScaler()

    def _build_model(self) -> Sequential:
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(self.sequence_length, self.features)),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train(self, X_train: np.ndarray, y_train: np.ndarray, epochs: int = 100):
        # Scale data
        X_scaled = self.scaler.fit_transform(X_train.reshape(-1, self.features))
        X_scaled = X_scaled.reshape(-1, self.sequence_length, self.features)
        
        # Train model
        self.model.fit(X_scaled, y_train, epochs=epochs, batch_size=32, validation_split=0.2)

    def predict(self, X: np.ndarray) -> np.ndarray:
        X_scaled = self.scaler.transform(X.reshape(-1, self.features))
        X_scaled = X_scaled.reshape(-1, self.sequence_length, self.features)
        return self.model.predict(X_scaled)