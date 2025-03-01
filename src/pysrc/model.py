from sklearn.linear_model import Lasso
from pysrc.data_client import DataClient
from collections import deque
from typing import Any, Dict, Deque
import time
from pysrc import intern


class Model:
    def __init__(self) -> None:
        self.buffer: Deque[list[float]] = deque(maxlen=10)
        self.client = DataClient()
        self.model = Lasso(alpha=1)
        self.tick = 0
        self.features = [
            intern.NTradesFeature(),
            intern.PercentBuyFeature(),
            intern.PercentSellFeature(),
            intern.FiveTickVolumeFeature(),
        ]

    def compute_features(self, data: list[Dict[str, Any]]) -> list[float]:
        cpp_trades = [
            (float(trade["price"]), float(trade["amount"]), trade["type"] == "buy")
            for trade in data
        ]
        return [feature.compute_feature(cpp_trades) for feature in self.features]

    def train(self, features: list[float], midprice: float) -> None:
        X = [tick[1:] for tick in self.buffer]
        y = [tick[0] for tick in self.buffer]
        self.model.fit(X, y)
        prediction = round(float(self.model.predict([features])), 3)
        print("Prediction: " + str(prediction))
        if prediction > midprice:
            print("BUY")
        else:
            print("SELL")
        features.insert(0, midprice)
        self.buffer.append(features)

    def on_tick(self) -> None:
        data = self.client.get_data()
        features = self.compute_features(data)

        bb = 0.0
        ba = float("inf")
        for trade in data:
            if trade["type"] == "buy":
                bb = max(bb, round(float(trade["price"]), 3))
            elif trade["type"] == "sell":
                ba = min(ba, float(trade["price"]))
        if not bb and ba == float("inf"):
            midprice = 0.0
        elif not bb:
            midprice = ba
        elif ba == float("inf"):
            midprice = bb
        midprice = round(((bb + ba) / 2), 3)

        if len(self.buffer) == 10:
            print("Training...")
            print("Midprice: " + str(midprice) + "\n")
            self.train(features, midprice)
        else:
            print("Collecting data...")
            features.insert(0, midprice)
            self.buffer.append(features)
            print("Midprice: " + str(midprice) + "\n")

    def run(self, tick_size: int) -> None:
        while True:
            self.on_tick()
            time.sleep(tick_size)
