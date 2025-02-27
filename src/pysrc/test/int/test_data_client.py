import pytest
from pysrc.data_client import DataClient


def test_integration() -> None:
    data_client = DataClient()

    result = data_client.get_data()

    for trade in result:
        assert trade["type"]
        assert trade["amount"]
        assert trade["timestampms"]
        assert trade["price"]
        assert (
            trade["type"] == "trade"
            or trade["type"] == "buy"
            or trade["type"] == "sell"
        )
        assert type(float(trade["amount"])) is float
        assert type(trade["timestampms"]) is int
        assert type(float(trade["price"])) is float
