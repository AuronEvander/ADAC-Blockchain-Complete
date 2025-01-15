import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class PricePredictor:
    def __init__(self):
        self.model = self._build_model()
        self.scaler = StandardScaler()

    def _build_model(self):
        model = Sequential([
            LSTM(50, activation='relu', input_shape=(60, 1), return_sequences=True),
            LSTM(50, activation='relu'),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def prepare_data(self, data):
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
        X, y = [], []
        for i in range(60, len(scaled_data)):
            X.append(scaled_data[i-60:i, 0])
            y.append(scaled_data[i, 0])
        return np.array(X), np.array(y)

    def train(self, historical_data):
        X, y = self.prepare_data(historical_data)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        self.model.fit(X, y, epochs=50, batch_size=32)

    def predict(self, sequence):
        sequence = self.scaler.transform(sequence.reshape(-1, 1))
        sequence = sequence.reshape((1, 60, 1))
        prediction = self.model.predict(sequence)
        return self.scaler.inverse_transform(prediction)[0, 0]