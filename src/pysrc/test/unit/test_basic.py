import pytest
from typing import Any
from unittest import mock
from pysrc.data_client import DataClient
from pysrc.model import Model
import numpy as np


@pytest.fixture
def mock_query_api() -> Any:
    with mock.patch.object(DataClient, "_query_api") as mock_method:
        mock_method.return_value = [
            {
                "type": "trade",
                "amount": "0.1",
                "timestampms": 1617288123456,
                "price": "50000",
            },
            {
                "type": "trade",
                "amount": "0.05",
                "timestampms": 1617288134567,
                "price": "50500",
            },
        ]
        yield mock_method


def test_parse_message() -> None:
    data_client = DataClient()
    message = {
        "type": "trade",
        "amount": "0.1",
        "timestampms": 1617288123456,
        "price": "50000",
    }

    parsed = data_client._parse_message(message)

    assert parsed == {
        "type": "trade",
        "amount": "0.1",
        "timestampms": 1617288123456,
        "price": "50000",
    }


def test_get_data(mock_query_api: Any) -> None:
    data_client = DataClient()

    result = data_client.get_data()

    assert result == [
        {
            "type": "trade",
            "amount": "0.1",
            "timestampms": 1617288123456,
            "price": "50000",
        },
        {
            "type": "trade",
            "amount": "0.05",
            "timestampms": 1617288134567,
            "price": "50500",
        },
    ]

    mock_query_api.assert_called_once()


def test_buffer() -> None:
    model = Model()
    fake_trade_data = [
        [
            {"price": 84150.75, "amount": 0.25, "type": True},
            {"price": 84150.80, "amount": 0.50, "type": False},
        ],
        [{"price": 84151.00, "amount": 1.00, "type": True}],
        [
            {"price": 84149.90, "amount": 0.75, "type": False},
            {"price": 84152.20, "amount": 0.30, "type": True},
            {"price": 84148.50, "amount": 1.25, "type": False},
        ],
        [{"price": 84150.95, "amount": 0.40, "type": True}],
        [
            {"price": 84151.10, "amount": 0.60, "type": False},
            {"price": 84149.80, "amount": 0.90, "type": True},
        ],
        [{"price": 84150.60, "amount": 1.10, "type": False}],
        [
            {"price": 84151.25, "amount": 0.55, "type": True},
            {"price": 84149.95, "amount": 0.85, "type": False},
        ],
        [
            {"price": 84152.00, "amount": 0.20, "type": True},
            {"price": 84148.75, "amount": 1.50, "type": False},
        ],
        [{"price": 84150.85, "amount": 0.35, "type": True}],
        [
            {"price": 84151.50, "amount": 0.75, "type": False},
            {"price": 84149.70, "amount": 1.20, "type": True},
        ],
        [{"price": 84152.40, "amount": 0.45, "type": False}],
        [
            {"price": 84150.20, "amount": 0.95, "type": True},
            {"price": 84148.90, "amount": 1.30, "type": False},
        ],
        [{"price": 84151.75, "amount": 0.50, "type": True}],
        [
            {"price": 84149.60, "amount": 1.00, "type": False},
            {"price": 84150.30, "amount": 0.70, "type": True},
        ],
        [{"price": 84152.10, "amount": 0.25, "type": False}],
        [
            {"price": 84151.90, "amount": 0.40, "type": True},
            {"price": 84148.60, "amount": 1.40, "type": False},
        ],
        [{"price": 84150.45, "amount": 0.80, "type": True}],
        [
            {"price": 84151.30, "amount": 0.65, "type": False},
            {"price": 84149.50, "amount": 1.10, "type": True},
        ],
        [{"price": 84152.50, "amount": 0.30, "type": False}],
        [
            {"price": 84150.10, "amount": 0.85, "type": True},
            {"price": 84148.70, "amount": 1.25, "type": False},
        ],
    ]

    midprices = [
        84150.775,
        84151.0,
        84150.35,
        84150.95,
        84150.45,
        84150.6,
        84150.6,
        84150.375,
        84150.85,
        84150.6,
        84152.4,
        84149.55,
        84151.75,
        84149.95,
        84152.1,
        84150.25,
        84150.45,
        84150.4,
        84152.5,
        84149.4,
    ]

    for i in range(len(fake_trade_data) - 1):
        features = model.compute_features(fake_trade_data[i])
        print(features)
        if i >= 10:
            model.train(features, midprices[i])
        else:
            features.insert(0, midprices[i])
            model.buffer.append(features)

    assert len(midprices) == len(fake_trade_data)
    assert isinstance(model.model.coef_, np.ndarray)
    assert isinstance(model.model.intercept_, float)
    prediction = model.model.predict([model.compute_features(fake_trade_data[i])])[0]
    assert isinstance(prediction, float)
    assert prediction != 0.0
