from sklearn.linear_model import Lasso
from data_client import DataClient
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
        nt = intern.NTradesFeature()
        pb = intern.PercentBuyFeature()
        ps = intern.PercentSellFeature()
        ftv = intern.FiveTickVolumeFeature()

        cpp_trades = [
            [trade["price"], trade["amount"], trade["type"] == "buy"] for trade in data
        ]

        nt.compute_feature(cpp_trades)
        pb.compute_feature(cpp_trades)
        ps.compute_feature(cpp_trades)
        ftv.compute_feature(cpp_trades)

        return [nt, pb, ps, ftv]

    def train(self) -> None:
        X = [tick[1:] for tick in self.buffer]
        y = [tick[0] for tick in self.buffer]
        self.model.fit(X, y)
        prediction = self.model.predict([X[-1]])
        if prediction > y[-1]:
            print("BUY\n")
        else:
            print("SELL\n")

    def on_tick(self) -> None:
        data = self.client.get_data()
        features = self.compute_features(data)

        bb = 0.0
        ba = float("inf")
        for trade in data:
            if trade["type"] == "buy" and trade["price"]:
                bb = max(bb, trade["price"])
            elif trade["type"] == "sell" and trade["price"]:
                ba = min(ba, trade["price"])
        midprice = (bb + ba) / 2

        if len(self.buffer) == 10:
            features.insert(0, midprice)
            self.buffer.append(features)
            print("Training...")
            self.train()
        else:
            print("Collecting data...")
            features.insert(0, midprice)
            self.buffer.append(features)

    def run(self, tick_size: int) -> None:
        while True:
            self.on_tick()
            time.sleep(tick_size)
