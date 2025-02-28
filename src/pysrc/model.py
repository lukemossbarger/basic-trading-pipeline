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
        self.model = Lasso(alpha=0.01)
        self.tick = 0

    def compute_features(self, data: list[Dict[str, Any]]) -> list[float]:
        cpp_trades = [
            (float(trade["price"]), float(trade["amount"]), trade["type"] == "buy")
            for trade in data
        ]

        nt = intern.NTradesFeature().compute_feature(cpp_trades)
        pb = intern.PercentBuyFeature().compute_feature(cpp_trades)
        ps = intern.PercentSellFeature().compute_feature(cpp_trades)
        ftv = intern.FiveTickVolumeFeature().compute_feature(cpp_trades)

        return [nt, pb, ps, ftv]

    def train(self) -> None:
        X = [tick[1:] for tick in self.buffer]
        y = [tick[0] for tick in self.buffer]
        self.model.fit(X, y)
        prediction = round(float(self.model.predict([X[-1]])), 3)
        print("Prediction: " + str(prediction))
        if prediction > y[-1]:
            print("BUY")
        else:
            print("SELL")

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
            features.insert(0, midprice)
            self.buffer.append(features)
            print("Training...")
            self.train()
        else:
            print("Collecting data...")
            features.insert(0, midprice)
            self.buffer.append(features)
        print("Midprice: " + str(midprice) + "\n")

    def run(self, tick_size: int) -> None:
        while True:
            self.on_tick()
            time.sleep(tick_size)
