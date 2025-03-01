from sklearn.linear_model import Lasso
from collections import deque
from typing import Any, Dict, Deque
import time
from pysrc import intern


class Model:
    def __init__(self) -> None:
        self.buffer: Deque[list[float]] = deque(maxlen=10)
        self.client = intern.DataClient()
        self.model = Lasso(alpha=1)
        self.tick = 0
        self.last_midprice = 0.0
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

    def train(self) -> None:
        X = [tick[1:] for tick in self.buffer]
        y = [tick[0] for tick in self.buffer]
        self.model.fit(X, y)

    def predict(self, features: list[float]) -> float:
        prediction = round(float(self.model.predict([features])[0]), 5)
        return prediction

    def on_tick(self) -> None:
        print("Tick: " + str(self.tick + 1))
        data = self.client.get_data()
        features = self.compute_features(data)

        bb = 0.0
        ba = float("inf")
        for trade in data:
            if trade["type"] == "buy":
                bb = max(bb, round(float(trade["price"]), 5))
            elif trade["type"] == "sell":
                ba = min(ba, float(trade["price"]))
        if not bb and ba == float("inf"):
            midprice = 0.0
        elif not bb:
            midprice = ba
        elif ba == float("inf"):
            midprice = bb
        midprice = round(((bb + ba) / 2), 3)

        if self.tick >= 11:
            prediction = self.predict(features)
            with open("out.txt", "a") as file:
                file.write(
                    str(prediction)
                    + ", "
                    + str(round(float((midprice - self.last_midprice) / midprice), 5))
                    + "\n"
                )
            self.train()
        elif self.tick == 10:
            self.train()

        if self.tick:
            features.insert(0, (midprice - self.last_midprice) / midprice)
            self.buffer.append(features)
        else:
            features.insert(0, 0.0)
            self.buffer.append(features)

        self.last_midprice = midprice
        self.tick += 1

    def run(self, tick_size: int) -> None:
        while True:
            self.on_tick()
            time.sleep(tick_size)
