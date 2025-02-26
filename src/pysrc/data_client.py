import requests
import json
from typing import Any


class DataClient:
    def __init__(self) -> None:
        self.symbol = "btcusd"
        self.limit = 100

    def _query_api(self) -> Any:
        url = f"https://api.gemini.com/v1/trades/{self.symbol}"
        params = {
            "symbol": self.symbol,
            "limit": str(self.limit),
        }
        response = requests.get(url, params=params)

        return response.json()  # Return parsed JSON data from the API

    def _parse_message(self, message: str) -> dict:
        parsed_message = json.loads(message)
        fields = ["type", "amount", "timestampms", "price"]
        return {key: parsed_message[key] for key in fields if key in parsed_message}

    def get_data(self) -> list:
        response = self._query_api()
        return [self._parse_message(trade) for trade in response]
