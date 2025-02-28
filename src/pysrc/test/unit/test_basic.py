import pytest
from typing import Any
from unittest import mock
from pysrc.data_client import DataClient
from pysrc.model import Model


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
