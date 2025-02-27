import pytest
from pysrc.data_client import DataClient


def test_integration() -> None:
    data_client = DataClient()

    result = data_client.get_data()

    correct_data = True
    for trade in result:
        for field in trade:
            if field == "type":
                if trade[field] == "trade":
                    correct_data = True
                else:
                    correct_data = False
            elif field == "amount":
                if type(float(trade[field])) is float:
                    correct_data = True
                else:
                    correct_data = False
            elif field == "timestamps":
                if type(trade[field]) is int:
                    correct_data = True
                else:
                    correct_data = False
            elif field == "price":
                if type(float(trade[field])) is float:
                    correct_data = True
                else:
                    correct_data = False
            else:
                correct_data = False

    assert correct_data
